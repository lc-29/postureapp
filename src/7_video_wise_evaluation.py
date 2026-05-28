"""Check whether a CSV is ready for video-wise evaluation."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from statsmodels.stats.proportion import proportion_confint


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = BASE_DIR / "dataset" / "posture_data_2fps.csv"
DEFAULT_MODEL = BASE_DIR / "models" / "ann_best.keras"
DEFAULT_SCALER = BASE_DIR / "models" / "scaler.pkl"
DEFAULT_OUTPUT = BASE_DIR / "reports" / "results" / "video_wise_summary.md"
REQUIRED_COLUMNS = {"source_video", "frame_index", "label"}
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


def metric_row(source_video: str, group: pd.DataFrame, y_prob: np.ndarray, threshold: float) -> dict[str, object]:
    y_true = group["label"].astype(int).to_numpy()
    y_pred = (y_prob >= threshold).astype(int)
    correct_count = int((y_true == y_pred).sum())
    ci_low, ci_high = proportion_confint(correct_count, len(y_true), alpha=0.05, method="wilson")
    return {
        "source_video": source_video,
        "rows": len(group),
        "label": int(group["label"].mode().iloc[0]) if not group.empty else "",
        "accuracy": accuracy_score(y_true, y_pred),
        "accuracy_ci_low": ci_low,
        "accuracy_ci_high": ci_high,
        "precision": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
        "recall": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
        "f1": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
        "mean_prob_incorrect": float(np.mean(y_prob)) if len(y_prob) else 0.0,
        "false_positive": int(((y_true == 0) & (y_pred == 1)).sum()),
        "false_negative": int(((y_true == 1) & (y_pred == 0)).sum()),
    }


def check_dataset(args: argparse.Namespace) -> None:
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

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not dataset_path.exists():
        raise FileNotFoundError(f"CSV not found: {dataset_path}")

    df = pd.read_csv(dataset_path, nrows=20)
    missing = sorted(REQUIRED_COLUMNS.difference(df.columns))

    if missing:
        text = f"""# Video-wise Evaluation Protocol

Status: not runnable yet.

CSV checked: `{dataset_path}`

Missing required columns: `{', '.join(missing)}`

To run video-wise or person-wise evaluation, re-extract features with metadata:

```powershell
python src/2_extract_features.py --include-metadata --output dataset/posture_data_2fps_with_metadata.csv
```

Required metadata:

- `source_video`: source file for each sampled frame.
- `frame_index`: frame index inside the source video.
- `label`: class label.

Do not infer source video from the current frame-only CSV; that would make the
split unverifiable.
"""
        output_path.write_text(text, encoding="utf-8")
        print(text)
        return

    full_df = pd.read_csv(dataset_path).reset_index(drop=True)
    feature_columns = landmark_feature_columns(full_df)
    full_df = full_df.dropna(subset=feature_columns + ["label"]).reset_index(drop=True)

    model = tf.keras.models.load_model(model_path)
    scaler = joblib.load(scaler_path)
    X_scaled = scaler.transform(full_df[feature_columns].astype(np.float32))
    full_df["prob_incorrect"] = model.predict(X_scaled, verbose=0).ravel()

    rows = []
    for source_video, group in full_df.groupby("source_video", sort=True):
        rows.append(
            metric_row(
                str(source_video),
                group,
                group["prob_incorrect"].to_numpy(),
                args.threshold,
            )
        )
    metrics_df = pd.DataFrame(rows)
    metrics_path = output_path.with_name("video_wise_metrics.csv")
    metrics_df.to_csv(metrics_path, index=False, encoding="utf-8-sig")

    source_summary_path = output_path.with_name("video_wise_source_summary.csv")
    (
        full_df.groupby(["source_video", "label"])
        .size()
        .reset_index(name="rows")
        .to_csv(source_summary_path, index=False, encoding="utf-8-sig")
    )

    mean_accuracy = float(metrics_df["accuracy"].mean()) if not metrics_df.empty else 0.0
    std_accuracy = float(metrics_df["accuracy"].std(ddof=0)) if len(metrics_df) > 1 else 0.0
    mean_f1 = float(metrics_df["f1"].mean()) if not metrics_df.empty else 0.0
    worst_videos = metrics_df.sort_values("accuracy").head(5).to_string(index=False)

    text = f"""# Video-wise Evaluation Protocol

Status: metadata is present and current ANN was evaluated per source video.

CSV checked: `{dataset_path}`
Model: `{model_path}`
Scaler: `{scaler_path}`
Threshold: `{args.threshold:.4f}`

Rows: {len(full_df)}
Unique source videos: {full_df['source_video'].nunique()}

## Video-wise summary

| Metric | Value |
|---|---:|
| Mean video accuracy | {mean_accuracy:.6f} |
| Std video accuracy | {std_accuracy:.6f} |
| Mean video F1 incorrect | {mean_f1:.6f} |

Per-video metrics saved to `{metrics_path}`.
Source summary saved to `{source_summary_path}`.

## Worst videos by accuracy

```text
{worst_videos}
```

## Limitation

Day la evaluation per-video cua model da train san tren external metadata CSV.
De co video-wise validation manh hon, can train/evaluate bang split giu lai
video/participant chua tung xuat hien trong train set.
"""
    output_path.write_text(text, encoding="utf-8")
    print(text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate metadata for video-wise evaluation.")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--model", default=str(DEFAULT_MODEL))
    parser.add_argument("--scaler", default=str(DEFAULT_SCALER))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--threshold", type=float, default=0.5)
    return parser.parse_args()


if __name__ == "__main__":
    check_dataset(parse_args())
