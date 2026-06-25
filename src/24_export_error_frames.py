"""Export representative false-positive/false-negative frames and taxonomy CSV."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_PREDICTIONS = BASE_DIR / "reports" / "results" / "final_external_predictions.csv"
DEFAULT_OUTPUT_DIR = BASE_DIR / "reports" / "figures" / "error_cases"
DEFAULT_TAXONOMY = BASE_DIR / "reports" / "results" / "error_taxonomy.csv"
DEFAULT_REPORT = BASE_DIR / "reports" / "ERROR_TAXONOMY_REPORT.md"
DEFAULT_MAX_PER_TYPE = 12


def infer_category(row: pd.Series) -> str:
    source = str(row.get("source_video", "")).lower()
    prob = float(row.get("prob_incorrect", 0.0))
    timestamp = float(row.get("timestamp_sec", 0.0))
    if "correct_004" in source:
        return "label_boundary_or_camera_angle"
    if "incorrect_005" in source:
        return "unseen_posture_type_or_ambiguous_posture"
    if "incorrect_004" in source and prob < 0.10:
        return "low_model_confidence_hard_case"
    if timestamp < 2.0:
        return "startup_transition_frame"
    return "needs_manual_review"


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


def export_frame(video_path: Path, frame_index: int, output_path: Path) -> bool:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return False
    try:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ok, frame = cap.read()
        if not ok or frame is None:
            return False
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return bool(cv2.imwrite(str(output_path), frame))
    finally:
        cap.release()


def export_error_frames(predictions_path: Path, output_dir: Path, taxonomy_path: Path, report_path: Path, max_per_type: int) -> None:
    df = pd.read_csv(predictions_path)
    errors = df[df["error_type"].isin(["false_negative", "false_positive"])].copy()
    if errors.empty:
        raise ValueError(f"No error rows found in {predictions_path}")
    errors["taxonomy_category"] = errors.apply(infer_category, axis=1)

    selected_rows = []
    for error_type, group in errors.groupby("error_type"):
        if error_type == "false_negative":
            selected = group.sort_values("prob_incorrect", ascending=True).head(max_per_type)
        else:
            selected = group.sort_values("prob_incorrect", ascending=False).head(max_per_type)
        for rank, (_, row) in enumerate(selected.iterrows(), start=1):
            source = Path(str(row["source_video"]))
            video_path = BASE_DIR / source
            frame_index = int(row["frame_index"])
            output_path = output_dir / error_type / f"{rank:02d}_{source.stem}_frame_{frame_index}.jpg"
            exported = export_frame(video_path, frame_index, output_path)
            item = row.to_dict()
            item["exported_frame"] = str(output_path.relative_to(BASE_DIR)) if exported else ""
            item["export_success"] = exported
            selected_rows.append(item)

    taxonomy = pd.DataFrame(selected_rows)
    taxonomy_path.parent.mkdir(parents=True, exist_ok=True)
    taxonomy.to_csv(taxonomy_path, index=False, encoding="utf-8-sig")

    counts = (
        errors.groupby(["error_type", "taxonomy_category"])
        .size()
        .reset_index(name="count")
        .sort_values(["error_type", "count"], ascending=[True, False])
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    text = "# Error Taxonomy Report\n\n"
    text += f"Predictions: `{predictions_path}`\n\n"
    text += f"Export directory: `{output_dir}`\n\n"
    text += "## Error Category Counts\n\n"
    text += dataframe_to_markdown(counts)
    text += "\n\n## Exported Representative Frames\n\n"
    cols = [
        "error_type",
        "taxonomy_category",
        "source_video",
        "frame_index",
        "timestamp_sec",
        "label",
        "pred_label",
        "prob_incorrect",
        "exported_frame",
    ]
    text += dataframe_to_markdown(taxonomy[cols])
    text += "\n\n## Manual Review Note\n\n"
    text += (
        "The taxonomy categories are first-pass labels inferred from source video and confidence. "
        "For a paper, representative exported frames should be manually reviewed before final claims.\n"
    )
    report_path.write_text(text, encoding="utf-8")
    print(f"Saved taxonomy: {taxonomy_path}")
    print(f"Saved report: {report_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export representative error frames.")
    parser.add_argument("--predictions", default=str(DEFAULT_PREDICTIONS))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--taxonomy", default=str(DEFAULT_TAXONOMY))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--max-per-type", type=int, default=DEFAULT_MAX_PER_TYPE)
    return parser.parse_args()


def resolve(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else BASE_DIR / path


if __name__ == "__main__":
    args = parse_args()
    export_error_frames(
        resolve(args.predictions),
        resolve(args.output_dir),
        resolve(args.taxonomy),
        resolve(args.report),
        args.max_per_type,
    )

