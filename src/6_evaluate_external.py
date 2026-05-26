"""Evaluate the current ANN model on the external landmark CSV."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = BASE_DIR / "dataset" / "posture_external_test_2fps.csv"
DEFAULT_MODEL = BASE_DIR / "models" / "ann_best.keras"
DEFAULT_SCALER = BASE_DIR / "models" / "scaler.pkl"
DEFAULT_OUTPUT_DIR = BASE_DIR / "reports" / "results"
NUM_FEATURES = 99


def landmark_feature_columns(df: pd.DataFrame) -> list[str]:
    columns = [
        column
        for column in df.columns
        if column.startswith("landmark_") and column.rsplit("_", 1)[-1] in {"x", "y", "z"}
    ]
    if len(columns) != NUM_FEATURES:
        raise ValueError(f"Expected {NUM_FEATURES} landmark features, found {len(columns)}.")
    return columns


def compute_metrics(y_true: np.ndarray, y_prob: np.ndarray, threshold: float) -> dict[str, float]:
    y_pred = (y_prob >= threshold).astype(int)
    return {
        "threshold": float(threshold),
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
        "recall": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
        "f1": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
    }


def evaluate(args: argparse.Namespace) -> None:
    dataset_path = Path(args.dataset)
    model_path = Path(args.model)
    scaler_path = Path(args.scaler)
    output_dir = Path(args.output_dir)

    if not dataset_path.is_absolute():
        dataset_path = BASE_DIR / dataset_path
    if not model_path.is_absolute():
        model_path = BASE_DIR / model_path
    if not scaler_path.is_absolute():
        scaler_path = BASE_DIR / scaler_path
    if not output_dir.is_absolute():
        output_dir = BASE_DIR / output_dir

    if not dataset_path.exists():
        raise FileNotFoundError(f"External CSV not found: {dataset_path}")
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")
    if not scaler_path.exists():
        raise FileNotFoundError(f"Scaler not found: {scaler_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(dataset_path).dropna().reset_index(drop=True)
    if "label" not in df.columns:
        raise ValueError("CSV must contain a 'label' column.")

    feature_columns = landmark_feature_columns(df)
    X = df[feature_columns].astype(np.float32)
    y_true = df["label"].astype(int).to_numpy()

    model = tf.keras.models.load_model(model_path)
    scaler = joblib.load(scaler_path)
    X_scaled = scaler.transform(X)
    y_prob = model.predict(X_scaled, verbose=0).ravel()

    base_metrics = compute_metrics(y_true, y_prob, args.threshold)
    y_pred = (y_prob >= args.threshold).astype(int)
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])

    sweep_rows = [
        compute_metrics(y_true, y_prob, threshold)
        for threshold in np.round(np.arange(0.10, 0.901, 0.05), 2)
    ]
    sweep_df = pd.DataFrame(sweep_rows)
    best_row = sweep_df.sort_values(["f1", "accuracy"], ascending=False).iloc[0]

    metrics_text = f"""External Evaluation Metrics
===========================

Dataset: {dataset_path}
Dataset shape: {df.shape}
Model: {model_path}
Scaler: {scaler_path}

Decision threshold: {args.threshold:.4f}
Accuracy : {base_metrics['accuracy']:.6f}
Precision: {base_metrics['precision']:.6f}
Recall   : {base_metrics['recall']:.6f}
F1-score : {base_metrics['f1']:.6f}

Confusion matrix [[TN, FP], [FN, TP]]:
{cm}

Best threshold by F1 in sweep:
threshold={best_row['threshold']:.2f}, accuracy={best_row['accuracy']:.6f}, precision={best_row['precision']:.6f}, recall={best_row['recall']:.6f}, f1={best_row['f1']:.6f}
"""

    (output_dir / "external_metrics.txt").write_text(metrics_text, encoding="utf-8")
    pd.DataFrame(
        cm,
        index=["true_0_correct", "true_1_incorrect"],
        columns=["pred_0_correct", "pred_1_incorrect"],
    ).to_csv(output_dir / "external_confusion_matrix.csv")
    sweep_df.to_csv(output_dir / "external_threshold_sweep.csv", index=False)

    print(metrics_text)
    print(f"Saved results to: {output_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate ANN on external landmark CSV.")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--model", default=str(DEFAULT_MODEL))
    parser.add_argument("--scaler", default=str(DEFAULT_SCALER))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--threshold", type=float, default=0.5)
    return parser.parse_args()


if __name__ == "__main__":
    evaluate(parse_args())
