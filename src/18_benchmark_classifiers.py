"""Benchmark classical classifiers across raw, ergonomic, and combined features."""

from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = BASE_DIR / "reports" / "results" / "classifier_benchmark_external.csv"
DEFAULT_SUMMARY = BASE_DIR / "reports" / "BENCHMARK_CLASSIFIERS_SUMMARY.md"
SEED = 42

ERGONOMIC_COLUMNS = [
    "shoulder_y_diff",
    "shoulder_tilt_angle",
    "torso_lean_angle",
    "head_offset_x",
    "nose_to_shoulder_y",
    "nose_shoulder_clearance_ratio",
    "neck_compression_detected",
    "left_hand_mouth_ratio",
    "right_hand_mouth_ratio",
    "chin_rest_detected",
    "shoulder_width",
    "torso_length",
    "head_shoulder_distance",
    "min_hand_mouth_ratio",
]


def raw_columns(df: pd.DataFrame) -> list[str]:
    columns = [
        column
        for column in df.columns
        if column.startswith("landmark_") and column.rsplit("_", 1)[-1] in {"x", "y", "z"}
    ]
    if len(columns) != 99:
        raise ValueError(f"Expected 99 raw landmark columns, found {len(columns)}.")
    return columns


def feature_columns(df: pd.DataFrame, feature_set: str) -> list[str]:
    raw = raw_columns(df) if feature_set in {"raw", "combined"} else []
    ergonomic = [column for column in ERGONOMIC_COLUMNS if column in df.columns]
    if feature_set == "raw":
        return raw
    if feature_set == "ergonomic":
        return ergonomic
    if feature_set == "combined":
        return raw + ergonomic
    raise ValueError(f"Unsupported feature_set: {feature_set}")


def candidate_models() -> list[tuple[str, Any]]:
    return [
        (
            "Logistic Regression",
            Pipeline(
                [
                    ("scaler", StandardScaler()),
                    (
                        "classifier",
                        LogisticRegression(max_iter=1000, class_weight="balanced", random_state=SEED),
                    ),
                ]
            ),
        ),
        (
            "KNN",
            Pipeline(
                [
                    ("scaler", StandardScaler()),
                    ("classifier", KNeighborsClassifier(n_neighbors=7)),
                ]
            ),
        ),
        (
            "SVM RBF",
            Pipeline(
                [
                    ("scaler", StandardScaler()),
                    (
                        "classifier",
                        SVC(kernel="rbf", C=3.0, gamma="scale", probability=True, class_weight="balanced"),
                    ),
                ]
            ),
        ),
        (
            "Random Forest",
            RandomForestClassifier(
                n_estimators=250,
                class_weight="balanced",
                random_state=SEED,
                n_jobs=-1,
            ),
        ),
        (
            "HistGradientBoosting",
            HistGradientBoostingClassifier(max_iter=200, random_state=SEED),
        ),
    ]


def predict_scores(model: Any, x_test: pd.DataFrame | np.ndarray) -> np.ndarray | None:
    if hasattr(model, "predict_proba"):
        return np.asarray(model.predict_proba(x_test))[:, 1]
    if hasattr(model, "decision_function"):
        decision = np.asarray(model.decision_function(x_test))
        return 1.0 / (1.0 + np.exp(-decision))
    return None


def metric_row(
    algorithm: str,
    feature_set: str,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_score: np.ndarray | None,
    train_seconds: float,
    predict_seconds: float,
) -> dict[str, object]:
    roc_auc = ""
    pr_auc = ""
    if y_score is not None and len(set(y_true.tolist())) == 2:
        roc_auc = roc_auc_score(y_true, y_score)
        pr_auc = average_precision_score(y_true, y_score)
    return {
        "algorithm": algorithm,
        "feature_set": feature_set,
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
        "recall": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
        "f1": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "mcc": matthews_corrcoef(y_true, y_pred),
        "roc_auc": roc_auc,
        "pr_auc": pr_auc,
        "train_seconds": round(train_seconds, 3),
        "predict_seconds": round(predict_seconds, 3),
    }


def load_pair(feature_set: str, data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    if feature_set == "raw":
        train = data_dir / "posture_data_2fps_with_metadata.csv"
        external = data_dir / "posture_external_test_2fps_with_metadata.csv"
    elif feature_set == "ergonomic":
        train = data_dir / "posture_data_2fps_ergonomic_features.csv"
        external = data_dir / "posture_external_test_2fps_ergonomic_features.csv"
    elif feature_set == "combined":
        train = data_dir / "posture_data_2fps_combined_features.csv"
        external = data_dir / "posture_external_test_2fps_combined_features.csv"
    else:
        raise ValueError(feature_set)
    return pd.read_csv(train), pd.read_csv(external)


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for _, row in df.iterrows():
        values = []
        for column in headers:
            value = row[column]
            values.append(f"{value:.6f}" if isinstance(value, float) else str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def run_benchmark(data_dir: Path, output: Path, summary: Path) -> None:
    rows: list[dict[str, object]] = []
    for feature_set in ["raw", "ergonomic", "combined"]:
        train_df, external_df = load_pair(feature_set, data_dir)
        columns = feature_columns(train_df, feature_set)
        train_df = train_df.dropna(subset=columns + ["label"]).reset_index(drop=True)
        external_df = external_df.dropna(subset=columns + ["label"]).reset_index(drop=True)
        x_train = train_df[columns].astype(np.float32)
        y_train = train_df["label"].astype(int).to_numpy()
        x_test = external_df[columns].astype(np.float32)
        y_test = external_df["label"].astype(int).to_numpy()

        for algorithm, model in candidate_models():
            train_start = time.perf_counter()
            model.fit(x_train, y_train)
            train_seconds = time.perf_counter() - train_start
            predict_start = time.perf_counter()
            y_pred = np.asarray(model.predict(x_test)).astype(int)
            y_score = predict_scores(model, x_test)
            predict_seconds = time.perf_counter() - predict_start
            rows.append(
                metric_row(
                    algorithm,
                    feature_set,
                    y_test,
                    y_pred,
                    y_score,
                    train_seconds,
                    predict_seconds,
                )
            )

    metrics = pd.DataFrame(rows).sort_values(["f1", "pr_auc", "accuracy"], ascending=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(output, index=False, encoding="utf-8-sig")

    summary_text = "# Classifier Benchmark Summary\n\n"
    summary_text += f"Output CSV: `{output}`\n\n"
    summary_text += "## Ranked By Incorrect-Class F1\n\n"
    summary_text += dataframe_to_markdown(metrics.head(15))
    summary_text += "\n\n## Notes\n\n"
    summary_text += (
        "These results compare models within the local project protocol only. "
        "They should not be described as state-of-the-art comparisons against literature.\n"
    )
    summary.write_text(summary_text, encoding="utf-8")
    print(f"Saved metrics: {output}")
    print(f"Saved summary: {summary}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark classifiers on external test set.")
    parser.add_argument("--data-dir", default=str(BASE_DIR / "dataset" / "processed"))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--summary", default=str(DEFAULT_SUMMARY))
    return parser.parse_args()


def resolve(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else BASE_DIR / path


if __name__ == "__main__":
    args = parse_args()
    run_benchmark(resolve(args.data_dir), resolve(args.output), resolve(args.summary))
