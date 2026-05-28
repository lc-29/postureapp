"""Evaluate the current ANN model on the external landmark CSV."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import matplotlib
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.calibration import calibration_curve
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)

matplotlib.use("Agg")
import matplotlib.pyplot as plt


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
    try:
        roc_auc = roc_auc_score(y_true, y_prob)
    except ValueError:
        roc_auc = float("nan")
    try:
        pr_auc = average_precision_score(y_true, y_prob)
    except ValueError:
        pr_auc = float("nan")
    return {
        "threshold": float(threshold),
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
        "recall": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
        "f1": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "mcc": matthews_corrcoef(y_true, y_pred),
        "roc_auc": roc_auc,
        "pr_auc": pr_auc,
        "brier_score": brier_score_loss(y_true, y_prob),
    }


def save_curves(y_true: np.ndarray, y_prob: np.ndarray, output_dir: Path) -> None:
    """Luu ROC, PR va calibration curves cho bao cao."""
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    precision, recall, _ = precision_recall_curve(y_true, y_prob)
    prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=10, strategy="uniform")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(fpr, tpr, label=f"ROC-AUC={roc_auc_score(y_true, y_prob):.3f}")
    ax.plot([0, 1], [0, 1], linestyle="--", color="#64748b", label="chance")
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.set_title("External ROC Curve")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "roc_curve.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(recall, precision, label=f"PR-AUC={average_precision_score(y_true, y_prob):.3f}")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("External Precision-Recall Curve")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "pr_curve.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(prob_pred, prob_true, marker="o", label="model")
    ax.plot([0, 1], [0, 1], linestyle="--", color="#64748b", label="ideal")
    ax.set_xlabel("Mean predicted probability")
    ax.set_ylabel("Fraction of positives")
    ax.set_title("External Calibration Curve")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "calibration_curve.png", dpi=160)
    plt.close(fig)


def write_predictions(
    df: pd.DataFrame,
    y_true: np.ndarray,
    y_prob: np.ndarray,
    threshold: float,
    output_dir: Path,
) -> pd.DataFrame:
    """Export prediction-level CSV, giu metadata neu CSV co san."""
    y_pred = (y_prob >= threshold).astype(int)
    metadata_columns = [
        column
        for column in [
            "source_video",
            "frame_index",
            "timestamp_sec",
            "sample_fps",
            "video_fps",
            "participant_id",
            "view_angle",
            "camera_type",
        ]
        if column in df.columns
    ]
    predictions_df = df[metadata_columns].copy() if metadata_columns else pd.DataFrame(index=df.index)
    predictions_df["row_index"] = np.arange(len(df))
    predictions_df["y_true"] = y_true
    predictions_df["y_pred"] = y_pred
    predictions_df["prob_incorrect"] = y_prob
    predictions_df["threshold"] = float(threshold)
    predictions_df["error_type"] = np.select(
        [
            (y_true == 0) & (y_pred == 1),
            (y_true == 1) & (y_pred == 0),
        ],
        ["false_positive", "false_negative"],
        default="correct",
    )
    predictions_df.to_csv(output_dir / "external_predictions.csv", index=False, encoding="utf-8-sig")
    return predictions_df


def write_error_analysis(
    predictions_df: pd.DataFrame,
    metrics: dict[str, float],
    output_dir: Path,
) -> None:
    error_counts = predictions_df["error_type"].value_counts().to_dict()
    false_positive_count = int(error_counts.get("false_positive", 0))
    false_negative_count = int(error_counts.get("false_negative", 0))
    correct_count = int(error_counts.get("correct", 0))

    group_text = "Metadata columns are not available in this CSV."
    if "source_video" in predictions_df.columns:
        grouped = (
            predictions_df.groupby(["source_video", "error_type"])
            .size()
            .unstack(fill_value=0)
            .reset_index()
        )
        grouped.to_csv(output_dir / "external_error_by_video.csv", index=False, encoding="utf-8-sig")
        group_text = grouped.to_string(index=False)

    hardest_false_negatives = predictions_df[
        predictions_df["error_type"] == "false_negative"
    ].sort_values("prob_incorrect").head(10)
    hardest_false_positives = predictions_df[
        predictions_df["error_type"] == "false_positive"
    ].sort_values("prob_incorrect", ascending=False).head(10)

    report = f"""# Error Analysis

Dataset: external evaluation CSV

## Summary

| Item | Value |
|---|---:|
| Rows | {len(predictions_df)} |
| Correct predictions | {correct_count} |
| False positives | {false_positive_count} |
| False negatives | {false_negative_count} |
| Accuracy | {metrics['accuracy']:.6f} |
| Precision incorrect | {metrics['precision']:.6f} |
| Recall incorrect | {metrics['recall']:.6f} |
| F1 incorrect | {metrics['f1']:.6f} |
| MCC | {metrics['mcc']:.6f} |
| ROC-AUC | {metrics['roc_auc']:.6f} |
| PR-AUC | {metrics['pr_auc']:.6f} |
| Brier score | {metrics['brier_score']:.6f} |

## Main finding

Tai threshold hien tai, loi can uu tien xu ly la false negative: model bo sot frame sai tu the. Neu app uu tien canh bao som, nen xem xet threshold thap hon va temporal smoothing de giam nhap nhay.

## Error by source video

```text
{group_text}
```

## Lowest-probability false negatives

```text
{hardest_false_negatives.to_string(index=False)}
```

## Highest-probability false positives

```text
{hardest_false_positives.to_string(index=False)}
```

## Recommended fixes

1. Re-extract CSV co metadata video/person de phan tich loi theo nguon.
2. Them normalized body-scale features va ergonomic angle features.
3. Chon threshold theo muc tieu recall/precision cua app.
4. Them temporal smoothing truoc khi ghi log/canh bao.
"""
    (output_dir.parent / "ERROR_ANALYSIS.md").write_text(report, encoding="utf-8")


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

    df = pd.read_csv(dataset_path).reset_index(drop=True)
    if "label" not in df.columns:
        raise ValueError("CSV must contain a 'label' column.")

    feature_columns = landmark_feature_columns(df)
    df = df.dropna(subset=feature_columns + ["label"]).reset_index(drop=True)
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
Macro F1 : {base_metrics['macro_f1']:.6f}
MCC      : {base_metrics['mcc']:.6f}
ROC-AUC  : {base_metrics['roc_auc']:.6f}
PR-AUC   : {base_metrics['pr_auc']:.6f}
Brier    : {base_metrics['brier_score']:.6f}

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
    predictions_df = write_predictions(df, y_true, y_prob, args.threshold, output_dir)
    write_error_analysis(predictions_df, base_metrics, output_dir)
    save_curves(y_true, y_prob, output_dir)

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
