"""Create ergonomic/geometric feature CSVs from MediaPipe landmark CSVs."""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

try:
    from posture_baseline import extract_posture_features, landmarks_from_feature_row
except ImportError:
    from src.posture_baseline import extract_posture_features, landmarks_from_feature_row


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_TRAIN = BASE_DIR / "dataset" / "processed" / "posture_data_2fps_with_metadata.csv"
RAW_EXTERNAL = BASE_DIR / "dataset" / "processed" / "posture_external_test_2fps_with_metadata.csv"

ERGONOMIC_FEATURE_COLUMNS = [
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

METADATA_COLUMNS = [
    "source_video",
    "frame_index",
    "timestamp_sec",
    "sample_fps",
    "video_fps",
    "participant_id",
    "view_angle",
    "camera_type",
]


def landmark_columns(df: pd.DataFrame) -> list[str]:
    columns = [
        column
        for column in df.columns
        if column.startswith("landmark_") and column.rsplit("_", 1)[-1] in {"x", "y", "z"}
    ]
    if len(columns) != 99:
        raise ValueError(f"Expected 99 landmark columns, found {len(columns)}.")
    return columns


def point(row: pd.Series, index: int) -> tuple[float, float]:
    return float(row[f"landmark_{index}_x"]), float(row[f"landmark_{index}_y"])


def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def midpoint(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:
    return (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0


def compute_extra_geometry(row: pd.Series) -> dict[str, float]:
    nose = point(row, 0)
    left_shoulder = point(row, 11)
    right_shoulder = point(row, 12)
    left_hip = point(row, 23)
    right_hip = point(row, 24)
    shoulder_mid = midpoint(left_shoulder, right_shoulder)
    hip_mid = midpoint(left_hip, right_hip)
    return {
        "shoulder_width": distance(left_shoulder, right_shoulder),
        "torso_length": distance(shoulder_mid, hip_mid),
        "head_shoulder_distance": distance(nose, shoulder_mid),
    }


def compute_ergonomic_row(row: pd.Series) -> dict[str, Any]:
    features = extract_posture_features(landmarks_from_feature_row(row))
    extra = compute_extra_geometry(row)
    left_ratio = float(features.get("left_hand_mouth_ratio", 0.0) or 0.0)
    right_ratio = float(features.get("right_hand_mouth_ratio", 0.0) or 0.0)
    result: dict[str, Any] = {
        "shoulder_y_diff": float(features.get("shoulder_y_diff", 0.0) or 0.0),
        "shoulder_tilt_angle": float(features.get("shoulder_tilt_angle", 0.0) or 0.0),
        "torso_lean_angle": float(features.get("torso_lean_angle", 0.0) or 0.0),
        "head_offset_x": float(features.get("head_offset_x", 0.0) or 0.0),
        "nose_to_shoulder_y": float(features.get("nose_to_shoulder_y", 0.0) or 0.0),
        "nose_shoulder_clearance_ratio": float(
            features.get("nose_shoulder_clearance_ratio", 0.0) or 0.0
        ),
        "neck_compression_detected": int(bool(features.get("neck_compression_detected", False))),
        "left_hand_mouth_ratio": left_ratio,
        "right_hand_mouth_ratio": right_ratio,
        "chin_rest_detected": int(bool(features.get("chin_rest_detected", False))),
        "min_hand_mouth_ratio": min(left_ratio, right_ratio),
        **extra,
    }
    return result


def build_feature_sets(input_csv: Path, ergonomic_csv: Path, combined_csv: Path) -> None:
    df = pd.read_csv(input_csv).reset_index(drop=True)
    raw_columns = landmark_columns(df)
    if "label" not in df.columns:
        raise ValueError(f"Missing label column: {input_csv}")

    ergonomic_rows = [compute_ergonomic_row(row) for _, row in df.iterrows()]
    ergonomic_df = pd.DataFrame(ergonomic_rows, columns=ERGONOMIC_FEATURE_COLUMNS)
    metadata_columns = [column for column in METADATA_COLUMNS if column in df.columns]

    ergonomic_output = pd.concat(
        [ergonomic_df, df[metadata_columns].reset_index(drop=True), df[["label"]].reset_index(drop=True)],
        axis=1,
    )
    combined_output = pd.concat(
        [
            df[raw_columns].reset_index(drop=True),
            ergonomic_df.reset_index(drop=True),
            df[metadata_columns].reset_index(drop=True),
            df[["label"]].reset_index(drop=True),
        ],
        axis=1,
    )

    ergonomic_csv.parent.mkdir(parents=True, exist_ok=True)
    combined_csv.parent.mkdir(parents=True, exist_ok=True)
    ergonomic_output.to_csv(ergonomic_csv, index=False, encoding="utf-8-sig")
    combined_output.to_csv(combined_csv, index=False, encoding="utf-8-sig")


def write_description(report_path: Path) -> None:
    text = """# Ergonomic Features Description

Updated: 2026-05-28

The ergonomic feature set is computed from MediaPipe Pose landmark coordinates.
It is intended to provide interpretable geometric indicators in addition to the
raw 99 landmark coordinates.

| Feature | Meaning |
|---|---|
| `shoulder_y_diff` | Absolute vertical difference between left and right shoulders. |
| `shoulder_tilt_angle` | Shoulder line angle in degrees. |
| `torso_lean_angle` | Torso centerline angle in degrees. |
| `head_offset_x` | Horizontal nose offset from shoulder midpoint. |
| `nose_to_shoulder_y` | Vertical nose position relative to shoulder midpoint. |
| `nose_shoulder_clearance_ratio` | Nose-shoulder clearance normalized by shoulder width. |
| `neck_compression_detected` | Binary indicator for deep neck compression. |
| `left_hand_mouth_ratio` | Left hand to mouth distance normalized by shoulder width. |
| `right_hand_mouth_ratio` | Right hand to mouth distance normalized by shoulder width. |
| `chin_rest_detected` | Binary hand-near-mouth/chin-rest indicator. |
| `shoulder_width` | 2D distance between shoulders. |
| `torso_length` | 2D distance from shoulder midpoint to hip midpoint. |
| `head_shoulder_distance` | 2D nose to shoulder-midpoint distance. |
| `min_hand_mouth_ratio` | Minimum of left/right hand-mouth ratios. |

Visibility note: the current 99-feature CSV stores x/y/z only and does not keep
MediaPipe visibility. Therefore `visibility_mean` is intentionally not used as
a numeric feature in this version.
"""
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(text, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build ergonomic feature CSVs.")
    parser.add_argument("--train-input", default=str(RAW_TRAIN))
    parser.add_argument("--external-input", default=str(RAW_EXTERNAL))
    parser.add_argument("--output-dir", default=str(BASE_DIR / "dataset" / "processed"))
    parser.add_argument("--report", default=str(BASE_DIR / "reports" / "ERGONOMIC_FEATURES_DESCRIPTION.md"))
    return parser.parse_args()


def resolve(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else BASE_DIR / path


def main() -> None:
    args = parse_args()
    output_dir = resolve(args.output_dir)
    train_input = resolve(args.train_input)
    external_input = resolve(args.external_input)
    write_description(resolve(args.report))

    build_feature_sets(
        train_input,
        output_dir / "posture_data_2fps_ergonomic_features.csv",
        output_dir / "posture_data_2fps_combined_features.csv",
    )
    build_feature_sets(
        external_input,
        output_dir / "posture_external_test_2fps_ergonomic_features.csv",
        output_dir / "posture_external_test_2fps_combined_features.csv",
    )
    print("Saved ergonomic and combined feature CSVs.")


if __name__ == "__main__":
    main()
