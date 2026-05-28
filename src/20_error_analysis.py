"""Generate prediction-level error analysis for external posture CSV."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = BASE_DIR / "dataset" / "processed" / "posture_external_test_2fps_with_metadata.csv"
DEFAULT_MODEL = BASE_DIR / "models" / "ann_best.keras"
DEFAULT_SCALER = BASE_DIR / "models" / "scaler.pkl"
DEFAULT_PREDICTIONS = BASE_DIR / "reports" / "results" / "predictions_external.csv"
DEFAULT_ERRORS = BASE_DIR / "reports" / "results" / "error_cases.csv"
DEFAULT_REPORT = BASE_DIR / "reports" / "ERROR_ANALYSIS_BY_VIDEO_PERSON_VIEW.md"


def landmark_columns(df: pd.DataFrame) -> list[str]:
    columns = [
        column
        for column in df.columns
        if column.startswith("landmark_") and column.rsplit("_", 1)[-1] in {"x", "y", "z"}
    ]
    if len(columns) != 99:
        raise ValueError(f"Expected 99 landmark features, found {len(columns)}.")
    return columns


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
            values.append(f"{value:.6f}" if isinstance(value, float) else str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def summarize_group(df: pd.DataFrame, group_columns: list[str]) -> pd.DataFrame:
    rows = []
    for key, group in df.groupby(group_columns, dropna=False):
        if not isinstance(key, tuple):
            key = (key,)
        y_true = group["label"].astype(int).to_numpy()
        y_pred = group["pred_label"].astype(int).to_numpy()
        item = {column: value for column, value in zip(group_columns, key)}
        item.update(
            {
                "rows": len(group),
                "accuracy": accuracy_score(y_true, y_pred),
                "precision_incorrect": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
                "recall_incorrect": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
                "f1_incorrect": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
                "false_positive": int(((group["label"] == 0) & (group["pred_label"] == 1)).sum()),
                "false_negative": int(((group["label"] == 1) & (group["pred_label"] == 0)).sum()),
                "mean_prob_incorrect": float(group["prob_incorrect"].mean()),
            }
        )
        rows.append(item)
    return pd.DataFrame(rows)


def run_error_analysis(
    dataset: Path,
    model_path: Path,
    scaler_path: Path,
    predictions_path: Path,
    errors_path: Path,
    report_path: Path,
    threshold: float,
) -> None:
    df = pd.read_csv(dataset).reset_index(drop=True)
    features = landmark_columns(df)
    model = tf.keras.models.load_model(model_path)
    scaler = joblib.load(scaler_path)
    x_scaled = scaler.transform(df[features].astype(np.float32))
    df["prob_incorrect"] = model.predict(x_scaled, verbose=0).ravel()
    df["pred_label"] = (df["prob_incorrect"] >= threshold).astype(int)
    df["error_type"] = "correct"
    df.loc[(df["label"] == 0) & (df["pred_label"] == 1), "error_type"] = "false_positive"
    df.loc[(df["label"] == 1) & (df["pred_label"] == 0), "error_type"] = "false_negative"

    predictions_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(predictions_path, index=False, encoding="utf-8-sig")
    error_cases = df[df["error_type"] != "correct"].copy()
    error_cases.to_csv(errors_path, index=False, encoding="utf-8-sig")

    by_video = summarize_group(df, ["source_video", "label"]).sort_values(
        ["false_negative", "false_positive", "rows"], ascending=False
    )
    by_participant = summarize_group(df, ["participant_id"]).sort_values(
        ["false_negative", "false_positive"], ascending=False
    )
    by_view = summarize_group(df, ["view_angle"]).sort_values(
        ["false_negative", "false_positive"], ascending=False
    )
    error_counts = df["error_type"].value_counts().reset_index()
    error_counts.columns = ["error_type", "count"]

    text = "# Error Analysis By Video, Participant, And View\n\n"
    text += f"Dataset: `{dataset}`\n\n"
    text += f"Threshold: `{threshold:.4f}`\n\n"
    text += f"Predictions CSV: `{predictions_path}`\n\n"
    text += f"Error cases CSV: `{errors_path}`\n\n"
    text += "## Error Counts\n\n"
    text += dataframe_to_markdown(error_counts)
    text += "\n\n## Worst Videos\n\n"
    text += dataframe_to_markdown(by_video.head(10))
    text += "\n\n## By Participant\n\n"
    text += dataframe_to_markdown(by_participant)
    text += "\n\n## By View Angle\n\n"
    text += dataframe_to_markdown(by_view)
    text += "\n\n## Interpretation Notes\n\n"
    text += (
        "- High false negative count means incorrect posture was missed.\n"
        "- High false positive count means correct posture was flagged as incorrect.\n"
        "- Use the worst-video table to inspect lighting, camera angle, occlusion, and intermediate posture cases.\n"
    )
    report_path.write_text(text, encoding="utf-8")
    print(f"Saved predictions: {predictions_path}")
    print(f"Saved errors: {errors_path}")
    print(f"Saved report: {report_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run external error analysis.")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--model", default=str(DEFAULT_MODEL))
    parser.add_argument("--scaler", default=str(DEFAULT_SCALER))
    parser.add_argument("--predictions", default=str(DEFAULT_PREDICTIONS))
    parser.add_argument("--errors", default=str(DEFAULT_ERRORS))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--threshold", type=float, default=0.5)
    return parser.parse_args()


def resolve(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else BASE_DIR / path


if __name__ == "__main__":
    args = parse_args()
    run_error_analysis(
        resolve(args.dataset),
        resolve(args.model),
        resolve(args.scaler),
        resolve(args.predictions),
        resolve(args.errors),
        resolve(args.report),
        args.threshold,
    )
