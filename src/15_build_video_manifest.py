"""Build a video-level metadata manifest for raw and external datasets."""

from __future__ import annotations

import argparse
import hashlib
import re
from collections import Counter
from pathlib import Path

import cv2
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = BASE_DIR / "dataset" / "metadata" / "video_manifest.csv"
DEFAULT_REPORT = BASE_DIR / "reports" / "DATASET_VIDEO_MANIFEST_SUMMARY.md"
VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".m4v"}


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def infer_label(path: Path) -> tuple[int, str]:
    parent = path.parent.name.lower()
    if parent == "correct":
        return 0, "correct"
    if parent == "incorrect":
        return 1, "incorrect"
    return -1, "unknown"


def infer_participant(path: Path) -> str:
    match = re.search(r"^(P\d+)_", path.name, flags=re.IGNORECASE)
    return match.group(1).upper() if match else "unknown"


def infer_view_angle(path: Path) -> str:
    stem = path.stem.lower()
    if "_front_" in stem:
        return "front"
    if "_side_30_" in stem:
        return "side_30"
    if "_side_90_" in stem:
        return "side_90"
    return "unknown"


def video_properties(path: Path) -> dict[str, float | int]:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        return {
            "duration_sec": 0.0,
            "fps": 0.0,
            "width": 0,
            "height": 0,
            "total_frames": 0,
        }
    try:
        fps = float(cap.get(cv2.CAP_PROP_FPS) or 0.0)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
        duration_sec = float(total_frames / fps) if fps > 0 else 0.0
        return {
            "duration_sec": round(duration_sec, 3),
            "fps": round(fps, 3),
            "width": width,
            "height": height,
            "total_frames": total_frames,
        }
    finally:
        cap.release()


def discover_videos(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in VIDEO_EXTENSIONS
    )


def build_manifest(base_dir: Path = BASE_DIR, include_hash: bool = True) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    roots = [
        ("raw", base_dir / "dataset" / "raw_videos", "training_video"),
        ("external", base_dir / "dataset" / "external_videos", "external_video"),
    ]
    for dataset_split, root, camera_type in roots:
        for path in discover_videos(root):
            label, label_name = infer_label(path)
            props = video_properties(path)
            try:
                source_video = path.relative_to(base_dir).as_posix()
            except ValueError:
                source_video = path.as_posix()
            rows.append(
                {
                    "dataset_split": dataset_split,
                    "source_video": source_video,
                    "file_name": path.name,
                    "label": label,
                    "label_name": label_name,
                    "participant_id": infer_participant(path),
                    "view_angle": infer_view_angle(path),
                    "camera_type": camera_type,
                    "duration_sec": props["duration_sec"],
                    "fps": props["fps"],
                    "width": props["width"],
                    "height": props["height"],
                    "total_frames": props["total_frames"],
                    "file_size_mb": round(path.stat().st_size / (1024 * 1024), 3),
                    "sha256": sha256_file(path) if include_hash else "",
                    "notes": "",
                }
            )
    return pd.DataFrame(rows)


def markdown_count_table(counter: Counter[str], first_header: str) -> str:
    lines = [f"| {first_header} | Count |", "|---|---:|"]
    for key, count in sorted(counter.items()):
        lines.append(f"| {key} | {count} |")
    return "\n".join(lines)


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No data._"
    headers = list(df.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in headers) + " |")
    return "\n".join(lines)


def write_report(df: pd.DataFrame, report_path: Path) -> None:
    raw = df[df["dataset_split"] == "raw"]
    external = df[df["dataset_split"] == "external"]
    total_duration = float(df["duration_sec"].sum()) if not df.empty else 0.0
    total_size = float(df["file_size_mb"].sum()) if not df.empty else 0.0

    text = f"""# Dataset Video Manifest Summary

Updated: 2026-05-28

## Overview

| Item | Value |
|---|---:|
| Total videos | {len(df)} |
| Raw videos | {len(raw)} |
| External videos | {len(external)} |
| Total duration seconds | {total_duration:.3f} |
| Total duration minutes | {total_duration / 60.0:.3f} |
| Total size MB | {total_size:.3f} |

## Videos By Dataset And Label

{dataframe_to_markdown(df.groupby(["dataset_split", "label_name"]).size().reset_index(name="count"))}

## Raw Participants

{markdown_count_table(Counter(raw["participant_id"].astype(str)), "Participant")}

## Raw View Angles

{markdown_count_table(Counter(raw["view_angle"].astype(str)), "View angle")}

## External Participants

{markdown_count_table(Counter(external["participant_id"].astype(str)), "Participant")}

## Notes

- Raw dataset participant IDs should be `P01` to `P05`.
- `source_video` is metadata only; raw videos do not need to be stored in Git.
- SHA256 is included to verify local raw video integrity.
"""
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(text, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build dataset video manifest.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--no-hash", action="store_true", help="Skip SHA256 hashing for faster dry runs.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = Path(args.output)
    report_path = Path(args.report)
    if not output_path.is_absolute():
        output_path = BASE_DIR / output_path
    if not report_path.is_absolute():
        report_path = BASE_DIR / report_path

    df = build_manifest(include_hash=not args.no_hash)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    write_report(df, report_path)
    print(f"Saved manifest: {output_path}")
    print(f"Saved report: {report_path}")
    print(f"Videos: {len(df)}")


if __name__ == "__main__":
    main()
