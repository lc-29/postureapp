"""Build temporal window summaries from frame-level posture predictions."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_PREDICTIONS = BASE_DIR / "reports" / "results" / "final_external_predictions.csv"
DEFAULT_OUTPUT = BASE_DIR / "reports" / "results" / "temporal_window_features.csv"
DEFAULT_REPORT = BASE_DIR / "reports" / "TEMPORAL_RISK_INDEX_VALIDATION.md"
DEFAULT_FIGURE = BASE_DIR / "reports" / "figures" / "temporal_smoothing_effect.png"


def consecutive_bad_seconds(flags: pd.Series, sample_fps: float) -> float:
    max_run = 0
    current = 0
    for value in flags.astype(int).tolist():
        if value:
            current += 1
            max_run = max(max_run, current)
        else:
            current = 0
    return max_run / max(sample_fps, 1e-6)


def build_temporal_features(predictions: pd.DataFrame, window_seconds: int) -> pd.DataFrame:
    rows = []
    for source_video, group in predictions.groupby("source_video", sort=True):
        group = group.sort_values("timestamp_sec").reset_index(drop=True)
        sample_fps = float(group["sample_fps"].median()) if "sample_fps" in group.columns else 2.0
        window_size = max(int(round(window_seconds * sample_fps)), 1)
        rolling_prob = group["prob_incorrect"].rolling(window_size, min_periods=1)
        rolling_bad = (group["pred_label"] == 1).astype(int).rolling(window_size, min_periods=1)
        smoothed = group.copy()
        smoothed["window_seconds"] = window_seconds
        smoothed["mean_prob_incorrect"] = rolling_prob.mean()
        smoothed["std_prob_incorrect"] = rolling_prob.std().fillna(0.0)
        smoothed["bad_posture_ratio"] = rolling_bad.mean()
        smoothed["temporal_pred_label"] = (smoothed["mean_prob_incorrect"] >= 0.5).astype(int)
        smoothed["temporal_error_type"] = "correct"
        smoothed.loc[(smoothed["label"] == 0) & (smoothed["temporal_pred_label"] == 1), "temporal_error_type"] = "false_positive"
        smoothed.loc[(smoothed["label"] == 1) & (smoothed["temporal_pred_label"] == 0), "temporal_error_type"] = "false_negative"
        rows.append(smoothed)
    return pd.concat(rows, ignore_index=True)


def metric_summary(df: pd.DataFrame, pred_col: str) -> dict[str, float]:
    y_true = df["label"].astype(int)
    y_pred = df[pred_col].astype(int)
    false_positive = int(((y_true == 0) & (y_pred == 1)).sum())
    false_negative = int(((y_true == 1) & (y_pred == 0)).sum())
    return {
        "accuracy": float((y_true == y_pred).mean()),
        "false_positive": false_positive,
        "false_negative": false_negative,
    }


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


def save_plot(df: pd.DataFrame, output: Path) -> None:
    worst = (
        df.groupby("source_video")
        .apply(lambda g: int((g["temporal_error_type"] != "correct").sum()), include_groups=False)
        .sort_values(ascending=False)
    )
    if worst.empty:
        return
    source = worst.index[0]
    group = df[df["source_video"] == source].sort_values("timestamp_sec")
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(group["timestamp_sec"], group["prob_incorrect"], label="Frame probability", alpha=0.55)
    ax.plot(group["timestamp_sec"], group["mean_prob_incorrect"], label="Temporal mean", linewidth=2)
    ax.axhline(0.5, color="red", linestyle="--", linewidth=1, label="Threshold")
    ax.set_title(f"Temporal smoothing example: {Path(source).name}")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Incorrect probability")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output, dpi=180)
    plt.close(fig)


def run_temporal(predictions_path: Path, output_path: Path, report_path: Path, figure_path: Path, window_seconds: int) -> None:
    predictions = pd.read_csv(predictions_path)
    temporal = build_temporal_features(predictions, window_seconds)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporal.to_csv(output_path, index=False, encoding="utf-8-sig")
    frame_metrics = metric_summary(predictions, "pred_label")
    temporal_metrics = metric_summary(temporal, "temporal_pred_label")
    summary = pd.DataFrame(
        [
            {"method": "frame_level", **frame_metrics},
            {f"method": f"temporal_{window_seconds}s_mean", **temporal_metrics},
        ]
    )
    save_plot(temporal, figure_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    text = "# Temporal Risk Index Validation\n\n"
    text += f"Input predictions: `{predictions_path}`\n\n"
    text += f"Window seconds: `{window_seconds}`\n\n"
    text += "## Frame vs Temporal Smoothing\n\n"
    text += dataframe_to_markdown(summary)
    text += "\n\n## Interpretation\n\n"
    text += (
        "Temporal smoothing is useful when the application should avoid flickering warnings. "
        "It can reduce isolated false alerts, but it may delay detection if the window is too long. "
        "Use this result as session-level risk support, not as medical validation.\n"
    )
    report_path.write_text(text, encoding="utf-8")
    print(f"Saved temporal features: {output_path}")
    print(f"Saved report: {report_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate temporal feature windows from predictions.")
    parser.add_argument("--predictions", default=str(DEFAULT_PREDICTIONS))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--figure", default=str(DEFAULT_FIGURE))
    parser.add_argument("--window-seconds", type=int, default=5)
    return parser.parse_args()


def resolve(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else BASE_DIR / path


if __name__ == "__main__":
    args = parse_args()
    run_temporal(resolve(args.predictions), resolve(args.output), resolve(args.report), resolve(args.figure), args.window_seconds)

