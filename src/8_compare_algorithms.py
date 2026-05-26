"""Compare ANN and rule-based baseline on a landmark CSV."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from posture_baseline import (
    classify_posture_rule_based,
    extract_posture_features,
    landmarks_from_feature_row,
)


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = BASE_DIR / "dataset" / "posture_external_test_2fps.csv"
DEFAULT_MODEL = BASE_DIR / "models" / "ann_best.keras"
DEFAULT_SCALER = BASE_DIR / "models" / "scaler.pkl"
DEFAULT_OUTPUT = BASE_DIR / "reports" / "results" / "algorithm_comparison.csv"
NUM_FEATURES = 99


def feature_columns(df: pd.DataFrame) -> list[str]:
    columns = [
        column
        for column in df.columns
        if column.startswith("landmark_") and column.rsplit("_", 1)[-1] in {"x", "y", "z"}
    ]
    if len(columns) != NUM_FEATURES:
        raise ValueError(f"Expected {NUM_FEATURES} landmark features, found {len(columns)}.")
    return columns


def metric_row(name: str, dataset: str, y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, object]:
    return {
        "algorithm": name,
        "dataset": dataset,
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
        "recall": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
        "f1": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
    }


def compare(args: argparse.Namespace) -> None:
    dataset_path = Path(args.dataset)
    model_path = Path(args.model)
    scaler_path = Path(args.scaler)
    output_path = Path(args.output)
    if not dataset_path.is_absolute():
        dataset_path = BASE_DIR / dataset_path
    if not model_path.is_absolute():
        model_path = BASE_DIR / model_path
    if not scaler_path.is_absolute():
        scaler_path = BASE_DIR / scaler_path
    if not output_path.is_absolute():
        output_path = BASE_DIR / output_path

    df = pd.read_csv(dataset_path).dropna().reset_index(drop=True)
    columns = feature_columns(df)
    y_true = df["label"].astype(int).to_numpy()

    model = tf.keras.models.load_model(model_path)
    scaler = joblib.load(scaler_path)
    X_scaled = scaler.transform(df[columns].astype(np.float32))
    ann_prob = model.predict(X_scaled, verbose=0).ravel()
    ann_pred = (ann_prob >= args.threshold).astype(int)

    baseline_pred = []
    for _, row in df.iterrows():
        landmarks = landmarks_from_feature_row(row)
        features = extract_posture_features(landmarks)
        status, _ = classify_posture_rule_based(features)
        baseline_pred.append(1 if status == "INCORRECT" else 0)
    baseline_pred_array = np.array(baseline_pred, dtype=int)

    rows = [
        metric_row("ANN", dataset_path.name, y_true, ann_pred),
        metric_row("Rule-based", dataset_path.name, y_true, baseline_pred_array),
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output_path, index=False)
    print(pd.DataFrame(rows).to_string(index=False))
    print(f"Saved: {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare ANN and rule-based baseline.")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--model", default=str(DEFAULT_MODEL))
    parser.add_argument("--scaler", default=str(DEFAULT_SCALER))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--threshold", type=float, default=0.5)
    return parser.parse_args()


if __name__ == "__main__":
    compare(parse_args())
