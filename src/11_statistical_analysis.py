"""Statistical analysis for Springer-style reporting.

This script adds two research-reporting artifacts:

- Wilson confidence intervals for accuracy.
- McNemar paired test comparing ANN and rule-based correctness on the same
  external samples.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.proportion import proportion_confint

from posture_baseline import (
    classify_posture_rule_based,
    extract_posture_features,
    landmarks_from_feature_row,
)


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = BASE_DIR / "dataset" / "posture_external_test_2fps.csv"
DEFAULT_MODEL = BASE_DIR / "models" / "ann_best.keras"
DEFAULT_SCALER = BASE_DIR / "models" / "scaler.pkl"
DEFAULT_OUTPUT_DIR = BASE_DIR / "reports" / "results"
NUM_FEATURES = 99


def resolve_path(path_text: str | Path) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else BASE_DIR / path


def landmark_feature_columns(df: pd.DataFrame) -> list[str]:
    columns = [
        column
        for column in df.columns
        if column.startswith("landmark_") and column.rsplit("_", 1)[-1] in {"x", "y", "z"}
    ]
    if len(columns) != NUM_FEATURES:
        raise ValueError(f"Expected {NUM_FEATURES} landmark features, found {len(columns)}.")
    return columns


def compute_ann_predictions(
    df: pd.DataFrame,
    feature_columns: list[str],
    model_path: Path,
    scaler_path: Path,
    threshold: float,
) -> np.ndarray:
    model = tf.keras.models.load_model(model_path)
    scaler = joblib.load(scaler_path)
    X = df[feature_columns].astype(np.float32)
    X_scaled = scaler.transform(X)
    probabilities = model.predict(X_scaled, verbose=0).ravel()
    return (probabilities >= threshold).astype(int)


def compute_rule_based_predictions(df: pd.DataFrame) -> np.ndarray:
    predictions: list[int] = []
    for _, row in df.iterrows():
        landmarks = landmarks_from_feature_row(row)
        features = extract_posture_features(landmarks)
        status, _ = classify_posture_rule_based(features)
        predictions.append(1 if status == "INCORRECT" else 0)
    return np.array(predictions, dtype=int)


def metric_row(name: str, y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, Any]:
    correct_count = int((y_true == y_pred).sum())
    nobs = int(len(y_true))
    ci_low, ci_high = proportion_confint(correct_count, nobs, alpha=0.05, method="wilson")
    return {
        "algorithm": name,
        "n": nobs,
        "correct": correct_count,
        "accuracy": accuracy_score(y_true, y_pred),
        "accuracy_ci_low": ci_low,
        "accuracy_ci_high": ci_high,
        "precision": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
        "recall": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
        "f1": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
    }


def build_mcnemar_table(
    y_true: np.ndarray,
    ann_pred: np.ndarray,
    rule_pred: np.ndarray,
) -> np.ndarray:
    ann_correct = ann_pred == y_true
    rule_correct = rule_pred == y_true
    return np.array(
        [
            [
                int(np.logical_and(ann_correct, rule_correct).sum()),
                int(np.logical_and(ann_correct, ~rule_correct).sum()),
            ],
            [
                int(np.logical_and(~ann_correct, rule_correct).sum()),
                int(np.logical_and(~ann_correct, ~rule_correct).sum()),
            ],
        ]
    )


def run_analysis(args: argparse.Namespace) -> None:
    dataset_path = resolve_path(args.dataset)
    model_path = resolve_path(args.model)
    scaler_path = resolve_path(args.scaler)
    output_dir = resolve_path(args.output_dir)

    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")
    if not scaler_path.exists():
        raise FileNotFoundError(f"Scaler not found: {scaler_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(dataset_path).dropna().reset_index(drop=True)
    if "label" not in df.columns:
        raise ValueError("CSV must contain 'label'.")

    feature_columns = landmark_feature_columns(df)
    y_true = df["label"].astype(int).to_numpy()
    ann_pred = compute_ann_predictions(df, feature_columns, model_path, scaler_path, args.threshold)
    rule_pred = compute_rule_based_predictions(df)

    metric_rows = [
        metric_row("ANN", y_true, ann_pred),
        metric_row("Rule-based", y_true, rule_pred),
    ]
    metrics_df = pd.DataFrame(metric_rows)

    table = build_mcnemar_table(y_true, ann_pred, rule_pred)
    result = mcnemar(table, exact=True)

    metrics_path = output_dir / "statistical_accuracy_ci.csv"
    table_path = output_dir / "paired_mcnemar_table.csv"
    report_path = output_dir / "statistical_analysis.txt"

    metrics_df.to_csv(metrics_path, index=False)
    pd.DataFrame(
        table,
        index=["ann_correct", "ann_incorrect"],
        columns=["rule_correct", "rule_incorrect"],
    ).to_csv(table_path)

    report_text = f"""Statistical Analysis
====================

Dataset: {dataset_path}
Samples: {len(df)}
Decision threshold: {args.threshold:.4f}

Accuracy with Wilson 95% confidence intervals:
{metrics_df.to_string(index=False)}

McNemar paired test on sample-level correctness:
Rows: ANN correctness, columns: rule-based correctness.
Table [[ANN correct and rule correct, ANN correct and rule incorrect],
       [ANN incorrect and rule correct, ANN incorrect and rule incorrect]]:
{table}

Statistic: {float(result.statistic):.6f}
P-value: {float(result.pvalue):.6g}

Interpretation note:
McNemar evaluates whether the two paired classifiers have the same error
probability on the same external samples. It does not replace video-wise or
person-wise validation.
"""
    report_path.write_text(report_text, encoding="utf-8")

    print(report_text)
    print(f"Saved: {metrics_path}")
    print(f"Saved: {table_path}")
    print(f"Saved: {report_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run statistical analysis for paper reporting.")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--model", default=str(DEFAULT_MODEL))
    parser.add_argument("--scaler", default=str(DEFAULT_SCALER))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--threshold", type=float, default=0.5)
    return parser.parse_args()


if __name__ == "__main__":
    run_analysis(parse_args())
