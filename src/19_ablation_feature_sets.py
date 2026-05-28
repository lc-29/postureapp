"""Ablation study for posture feature sets."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_TRAIN = BASE_DIR / "dataset" / "processed" / "posture_data_2fps_combined_features.csv"
DEFAULT_EXTERNAL = BASE_DIR / "dataset" / "processed" / "posture_external_test_2fps_combined_features.csv"
DEFAULT_OUTPUT = BASE_DIR / "reports" / "results" / "feature_ablation.csv"
DEFAULT_SUMMARY = BASE_DIR / "reports" / "FEATURE_ABLATION_SUMMARY.md"
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
NECK_COLUMNS = ["nose_to_shoulder_y", "nose_shoulder_clearance_ratio", "neck_compression_detected"]
HAND_COLUMNS = [
    "left_hand_mouth_ratio",
    "right_hand_mouth_ratio",
    "chin_rest_detected",
    "min_hand_mouth_ratio",
]


def raw_columns(df: pd.DataFrame) -> list[str]:
    return [
        column
        for column in df.columns
        if column.startswith("landmark_") and column.rsplit("_", 1)[-1] in {"x", "y", "z"}
    ]


def subset_columns(df: pd.DataFrame, subset: str) -> list[str]:
    raw = raw_columns(df)
    ergonomic = [column for column in ERGONOMIC_COLUMNS if column in df.columns]
    if subset == "raw":
        columns = raw
    elif subset == "ergonomic":
        columns = ergonomic
    elif subset == "combined":
        columns = raw + ergonomic
    elif subset == "combined_without_neck":
        columns = raw + [column for column in ergonomic if column not in NECK_COLUMNS]
    elif subset == "combined_without_hand":
        columns = raw + [column for column in ergonomic if column not in HAND_COLUMNS]
    else:
        raise ValueError(subset)
    if not columns:
        raise ValueError(f"No columns for subset {subset}")
    return columns


def make_model() -> Pipeline:
    return Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "classifier",
                SVC(kernel="rbf", C=3.0, gamma="scale", probability=True, class_weight="balanced", random_state=SEED),
            ),
        ]
    )


def metric_row(subset: str, y_true: np.ndarray, y_pred: np.ndarray, y_score: np.ndarray) -> dict[str, object]:
    return {
        "feature_subset": subset,
        "algorithm": "SVM RBF",
        "accuracy": accuracy_score(y_true, y_pred),
        "precision_incorrect": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
        "recall_incorrect": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
        "f1_incorrect": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "mcc": matthews_corrcoef(y_true, y_pred),
        "roc_auc": roc_auc_score(y_true, y_score),
        "pr_auc": average_precision_score(y_true, y_score),
    }


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for _, row in df.iterrows():
        values = [f"{row[column]:.6f}" if isinstance(row[column], float) else str(row[column]) for column in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def run_ablation(train_path: Path, external_path: Path, output: Path, summary: Path) -> None:
    train_df = pd.read_csv(train_path).reset_index(drop=True)
    external_df = pd.read_csv(external_path).reset_index(drop=True)
    y_train = train_df["label"].astype(int).to_numpy()
    y_true = external_df["label"].astype(int).to_numpy()
    rows = []
    subsets = ["raw", "ergonomic", "combined", "combined_without_neck", "combined_without_hand"]
    for subset in subsets:
        columns = subset_columns(train_df, subset)
        x_train = train_df[columns].astype(np.float32)
        x_external = external_df[columns].astype(np.float32)
        model = make_model()
        model.fit(x_train, y_train)
        y_pred = model.predict(x_external).astype(int)
        y_score = model.predict_proba(x_external)[:, 1]
        rows.append(metric_row(subset, y_true, y_pred, y_score))

    metrics = pd.DataFrame(rows).sort_values(["f1_incorrect", "pr_auc"], ascending=False)
    output.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(output, index=False, encoding="utf-8-sig")

    text = "# Feature Ablation Summary\n\n"
    text += f"Train: `{train_path}`\n\nExternal: `{external_path}`\n\n"
    text += "Model: `SVM RBF`\n\n"
    text += dataframe_to_markdown(metrics)
    text += "\n\n## Interpretation Guide\n\n"
    text += (
        "- If `combined` is better than `raw`, ergonomic features improve the model.\n"
        "- If `combined_without_neck` drops, neck-compression features are useful.\n"
        "- If `combined_without_hand` drops, hand/chin-rest features are useful.\n"
    )
    summary.write_text(text, encoding="utf-8")
    print(f"Saved ablation: {output}")
    print(f"Saved summary: {summary}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run feature ablation study.")
    parser.add_argument("--train", default=str(DEFAULT_TRAIN))
    parser.add_argument("--external", default=str(DEFAULT_EXTERNAL))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--summary", default=str(DEFAULT_SUMMARY))
    return parser.parse_args()


def resolve(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else BASE_DIR / path


if __name__ == "__main__":
    args = parse_args()
    run_ablation(resolve(args.train), resolve(args.external), resolve(args.output), resolve(args.summary))
