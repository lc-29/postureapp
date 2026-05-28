"""Leave-one-participant-out evaluation for posture CSVs with metadata."""

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
DEFAULT_DATASET = BASE_DIR / "dataset" / "processed" / "posture_data_2fps_with_metadata.csv"
DEFAULT_OUTPUT = BASE_DIR / "reports" / "results" / "participant_wise_metrics.csv"
DEFAULT_SUMMARY = BASE_DIR / "reports" / "results" / "participant_wise_summary.md"
SEED = 42


def select_feature_columns(df: pd.DataFrame, feature_set: str) -> list[str]:
    raw = [
        column
        for column in df.columns
        if column.startswith("landmark_") and column.rsplit("_", 1)[-1] in {"x", "y", "z"}
    ]
    ergonomic = [
        column
        for column in [
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
        if column in df.columns
    ]
    if feature_set == "raw":
        columns = raw
    elif feature_set == "ergonomic":
        columns = ergonomic
    elif feature_set == "combined":
        columns = raw + ergonomic
    else:
        raise ValueError(f"Unsupported feature_set: {feature_set}")
    if not columns:
        raise ValueError(f"No feature columns found for feature_set={feature_set}.")
    return columns


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
    participant: str,
    algorithm: str,
    feature_set: str,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_score: np.ndarray | None,
    train_rows: int,
    test_rows: int,
    train_seconds: float,
    predict_seconds: float,
) -> dict[str, object]:
    roc_auc = ""
    pr_auc = ""
    if y_score is not None and len(set(y_true.tolist())) == 2:
        roc_auc = roc_auc_score(y_true, y_score)
        pr_auc = average_precision_score(y_true, y_score)
    return {
        "held_out_participant": participant,
        "algorithm": algorithm,
        "feature_set": feature_set,
        "accuracy": accuracy_score(y_true, y_pred),
        "precision_incorrect": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
        "recall_incorrect": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
        "f1_incorrect": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "mcc": matthews_corrcoef(y_true, y_pred),
        "roc_auc": roc_auc,
        "pr_auc": pr_auc,
        "train_rows": train_rows,
        "test_rows": test_rows,
        "train_seconds": round(train_seconds, 3),
        "predict_seconds": round(predict_seconds, 3),
    }


def run_evaluation(dataset: Path, output: Path, summary: Path, feature_set: str) -> None:
    df = pd.read_csv(dataset).dropna(subset=["label", "participant_id"]).reset_index(drop=True)
    feature_columns = select_feature_columns(df, feature_set)
    df = df.dropna(subset=feature_columns).reset_index(drop=True)
    participants = sorted(str(value) for value in df["participant_id"].dropna().unique())
    rows: list[dict[str, object]] = []

    for participant in participants:
        train_df = df[df["participant_id"].astype(str) != participant]
        test_df = df[df["participant_id"].astype(str) == participant]
        if train_df.empty or test_df.empty:
            continue
        x_train = train_df[feature_columns].astype(np.float32)
        y_train = train_df["label"].astype(int).to_numpy()
        x_test = test_df[feature_columns].astype(np.float32)
        y_test = test_df["label"].astype(int).to_numpy()

        for name, model in candidate_models():
            train_start = time.perf_counter()
            model.fit(x_train, y_train)
            train_seconds = time.perf_counter() - train_start
            predict_start = time.perf_counter()
            y_pred = np.asarray(model.predict(x_test)).astype(int)
            y_score = predict_scores(model, x_test)
            predict_seconds = time.perf_counter() - predict_start
            rows.append(
                metric_row(
                    participant,
                    name,
                    feature_set,
                    y_test,
                    y_pred,
                    y_score,
                    len(train_df),
                    len(test_df),
                    train_seconds,
                    predict_seconds,
                )
            )

    metrics = pd.DataFrame(rows)
    output.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(output, index=False, encoding="utf-8-sig")

    if metrics.empty:
        summary_text = "# Participant-wise Evaluation\n\nNo metrics generated.\n"
    else:
        grouped = (
            metrics.groupby(["algorithm", "feature_set"])
            .agg(
                mean_accuracy=("accuracy", "mean"),
                std_accuracy=("accuracy", "std"),
                mean_f1_incorrect=("f1_incorrect", "mean"),
                std_f1_incorrect=("f1_incorrect", "std"),
                mean_pr_auc=("pr_auc", "mean"),
            )
            .reset_index()
            .sort_values(["mean_f1_incorrect", "mean_accuracy"], ascending=False)
        )
        summary_text = "# Participant-wise Evaluation\n\n"
        summary_text += f"Dataset: `{dataset}`\n\n"
        summary_text += f"Feature set: `{feature_set}`\n\n"
        summary_text += f"Participants: {', '.join(participants)}\n\n"
        summary_text += "## Summary By Algorithm\n\n"
        summary_text += dataframe_to_markdown(grouped)
        summary_text += "\n\n## Notes\n\n"
        summary_text += (
            "This is a stricter protocol than frame-wise random evaluation because "
            "each fold tests on a participant unseen during training.\n"
        )
    summary.write_text(summary_text, encoding="utf-8")
    print(f"Saved metrics: {output}")
    print(f"Saved summary: {summary}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Leave-one-participant-out evaluation.")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--summary", default=str(DEFAULT_SUMMARY))
    parser.add_argument("--feature-set", choices=["raw", "ergonomic", "combined"], default="raw")
    return parser.parse_args()


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No data._"
    headers = list(df.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for _, row in df.iterrows():
        values = []
        for column in headers:
            value = row[column]
            if isinstance(value, float):
                values.append(f"{value:.6f}")
            else:
                values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def resolve(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else BASE_DIR / path


if __name__ == "__main__":
    args = parse_args()
    run_evaluation(
        resolve(args.dataset),
        resolve(args.output),
        resolve(args.summary),
        args.feature_set,
    )
