"""Shared feature schema utilities for posture model training and inference."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

try:
    from posture_baseline import extract_posture_features, landmarks_from_feature_row
except ImportError:
    from src.posture_baseline import extract_posture_features, landmarks_from_feature_row


NUM_POSE_LANDMARKS = 33
RAW_FEATURE_COUNT = NUM_POSE_LANDMARKS * 3

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

ERGONOMIC_V2_EXTRA_COLUMNS = [
    "ear_shoulder_y_ratio_left",
    "ear_shoulder_y_ratio_right",
    "ear_shoulder_y_ratio_mean",
    "nose_ear_dx_ratio",
    "nose_shoulder_dx_ratio",
    "head_forward_ratio",
    "neck_to_shoulder_angle_left",
    "neck_to_shoulder_angle_right",
    "head_neck_torso_angle",
    "shoulder_hip_dx_ratio",
    "shoulder_hip_dy_ratio",
    "torso_side_lean_ratio",
    "hip_shoulder_torso_angle",
]

VIEW_FEATURE_COLUMNS = ["view_front", "view_side_30", "view_side_90", "view_unknown"]

SUPPORTED_FEATURE_SETS = [
    "raw_99",
    "normalized_99",
    "ergonomic_14",
    "combined_raw_ergonomic",
    "combined_normalized_ergonomic",
    "ergonomic_v2",
    "ergonomic_v2_with_view",
    "combined_v2",
    "combined_v2_with_view",
]


def get_raw_landmark_columns(df: pd.DataFrame) -> list[str]:
    columns = [
        column
        for column in df.columns
        if column.startswith("landmark_") and column.rsplit("_", 1)[-1] in {"x", "y", "z"}
    ]
    if len(columns) != RAW_FEATURE_COUNT:
        raise ValueError(f"Expected {RAW_FEATURE_COUNT} raw landmark columns, found {len(columns)}.")
    return columns


def _point(row: pd.Series, index: int) -> tuple[float, float]:
    return float(row[f"landmark_{index}_x"]), float(row[f"landmark_{index}_y"])


def _distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _midpoint(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:
    return (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0


def _safe_div(a: float, b: float) -> float:
    return float(a / b) if abs(b) > 1e-9 else 0.0


def _line_angle_deg(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))


def _angle_at(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> float:
    ba = np.array([a[0] - b[0], a[1] - b[1]], dtype=float)
    bc = np.array([c[0] - b[0], c[1] - b[1]], dtype=float)
    denom = np.linalg.norm(ba) * np.linalg.norm(bc)
    if denom <= 1e-9:
        return 0.0
    cosine = float(np.clip(np.dot(ba, bc) / denom, -1.0, 1.0))
    return float(math.degrees(math.acos(cosine)))


def _body_reference(row: pd.Series) -> tuple[tuple[float, float], float]:
    left_shoulder = _point(row, 11)
    right_shoulder = _point(row, 12)
    left_hip = _point(row, 23)
    right_hip = _point(row, 24)
    shoulder_mid = _midpoint(left_shoulder, right_shoulder)
    hip_mid = _midpoint(left_hip, right_hip)
    shoulder_width = _distance(left_shoulder, right_shoulder)
    torso_length = _distance(shoulder_mid, hip_mid)
    scale = max(shoulder_width, torso_length, 1e-6)
    return shoulder_mid, scale


def compute_normalized_landmarks(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize landmark coordinates by shoulder midpoint and body scale."""
    get_raw_landmark_columns(df)
    rows: list[list[float]] = []
    for _, row in df.iterrows():
        origin, scale = _body_reference(row)
        values: list[float] = []
        for index in range(NUM_POSE_LANDMARKS):
            x = (float(row[f"landmark_{index}_x"]) - origin[0]) / scale
            y = (float(row[f"landmark_{index}_y"]) - origin[1]) / scale
            z = float(row[f"landmark_{index}_z"]) / scale
            values.extend([x, y, z])
        rows.append(values)
    columns: list[str] = []
    for index in range(NUM_POSE_LANDMARKS):
        columns.extend(
            [
                f"norm_landmark_{index}_x",
                f"norm_landmark_{index}_y",
                f"norm_landmark_{index}_z",
            ]
        )
    return pd.DataFrame(rows, columns=columns, index=df.index)


def _extra_geometry(row: pd.Series) -> dict[str, float]:
    nose = _point(row, 0)
    left_shoulder = _point(row, 11)
    right_shoulder = _point(row, 12)
    left_hip = _point(row, 23)
    right_hip = _point(row, 24)
    shoulder_mid = _midpoint(left_shoulder, right_shoulder)
    hip_mid = _midpoint(left_hip, right_hip)
    return {
        "shoulder_width": _distance(left_shoulder, right_shoulder),
        "torso_length": _distance(shoulder_mid, hip_mid),
        "head_shoulder_distance": _distance(nose, shoulder_mid),
    }


def _compute_ergonomic_row(row: pd.Series) -> dict[str, Any]:
    features = extract_posture_features(landmarks_from_feature_row(row))
    extra = _extra_geometry(row)
    left_ratio = float(features.get("left_hand_mouth_ratio", 0.0) or 0.0)
    right_ratio = float(features.get("right_hand_mouth_ratio", 0.0) or 0.0)
    return {
        "shoulder_y_diff": float(features.get("shoulder_y_diff", 0.0) or 0.0),
        "shoulder_tilt_angle": float(features.get("shoulder_tilt_angle", 0.0) or 0.0),
        "torso_lean_angle": float(features.get("torso_lean_angle", 0.0) or 0.0),
        "head_offset_x": float(features.get("head_offset_x", 0.0) or 0.0),
        "nose_to_shoulder_y": float(features.get("nose_to_shoulder_y", 0.0) or 0.0),
        "nose_shoulder_clearance_ratio": float(features.get("nose_shoulder_clearance_ratio", 0.0) or 0.0),
        "neck_compression_detected": int(bool(features.get("neck_compression_detected", False))),
        "left_hand_mouth_ratio": left_ratio,
        "right_hand_mouth_ratio": right_ratio,
        "chin_rest_detected": int(bool(features.get("chin_rest_detected", False))),
        "min_hand_mouth_ratio": min(left_ratio, right_ratio),
        **extra,
    }


def compute_ergonomic_features(df: pd.DataFrame) -> pd.DataFrame:
    get_raw_landmark_columns(df)
    rows = [_compute_ergonomic_row(row) for _, row in df.iterrows()]
    return pd.DataFrame(rows, columns=ERGONOMIC_FEATURE_COLUMNS, index=df.index)


def _compute_ergonomic_v2_base_row(row: pd.Series) -> dict[str, float]:
    nose = _point(row, 0)
    left_shoulder = _point(row, 11)
    right_shoulder = _point(row, 12)
    left_hip = _point(row, 23)
    right_hip = _point(row, 24)
    left_wrist = _point(row, 15)
    right_wrist = _point(row, 16)
    left_mouth = _point(row, 9)
    right_mouth = _point(row, 10)
    shoulder_mid = _midpoint(left_shoulder, right_shoulder)
    hip_mid = _midpoint(left_hip, right_hip)
    shoulder_width = max(_distance(left_shoulder, right_shoulder), 1e-6)
    torso_length = max(_distance(shoulder_mid, hip_mid), 1e-6)
    nose_to_shoulder_y = shoulder_mid[1] - nose[1]
    left_hand_mouth_ratio = _distance(left_wrist, left_mouth) / shoulder_width
    right_hand_mouth_ratio = _distance(right_wrist, right_mouth) / shoulder_width
    nose_clearance = nose_to_shoulder_y / shoulder_width
    return {
        "shoulder_y_diff": abs(left_shoulder[1] - right_shoulder[1]),
        "shoulder_tilt_angle": abs(_line_angle_deg(left_shoulder, right_shoulder)),
        "torso_lean_angle": abs(_line_angle_deg(shoulder_mid, hip_mid) - 90.0),
        "head_offset_x": abs(nose[0] - shoulder_mid[0]),
        "nose_to_shoulder_y": nose_to_shoulder_y,
        "nose_shoulder_clearance_ratio": nose_clearance,
        "neck_compression_detected": float(nose_clearance < 0.35),
        "left_hand_mouth_ratio": left_hand_mouth_ratio,
        "right_hand_mouth_ratio": right_hand_mouth_ratio,
        "chin_rest_detected": float(min(left_hand_mouth_ratio, right_hand_mouth_ratio) < 0.55),
        "shoulder_width": shoulder_width,
        "torso_length": torso_length,
        "head_shoulder_distance": _distance(nose, shoulder_mid),
        "min_hand_mouth_ratio": min(left_hand_mouth_ratio, right_hand_mouth_ratio),
    }


def compute_ergonomic_v2_base_features(df: pd.DataFrame) -> pd.DataFrame:
    if all(column in df.columns for column in ERGONOMIC_FEATURE_COLUMNS):
        return df[ERGONOMIC_FEATURE_COLUMNS].copy().reset_index(drop=True)
    get_raw_landmark_columns(df)
    rows = [_compute_ergonomic_v2_base_row(row) for _, row in df.iterrows()]
    return pd.DataFrame(rows, columns=ERGONOMIC_FEATURE_COLUMNS)


def _compute_ergonomic_v2_extra_row(row: pd.Series) -> dict[str, float]:
    nose = _point(row, 0)
    left_ear = _point(row, 7)
    right_ear = _point(row, 8)
    left_shoulder = _point(row, 11)
    right_shoulder = _point(row, 12)
    left_hip = _point(row, 23)
    right_hip = _point(row, 24)
    shoulder_mid = _midpoint(left_shoulder, right_shoulder)
    hip_mid = _midpoint(left_hip, right_hip)
    ear_mid = _midpoint(left_ear, right_ear)
    shoulder_width = max(_distance(left_shoulder, right_shoulder), 1e-6)
    torso_length = max(_distance(shoulder_mid, hip_mid), 1e-6)
    body_scale = max(shoulder_width, torso_length, 1e-6)
    left_ear_shoulder_y = _safe_div(left_shoulder[1] - left_ear[1], body_scale)
    right_ear_shoulder_y = _safe_div(right_shoulder[1] - right_ear[1], body_scale)
    shoulder_hip_dx = abs(shoulder_mid[0] - hip_mid[0])
    shoulder_hip_dy = abs(shoulder_mid[1] - hip_mid[1])
    return {
        "ear_shoulder_y_ratio_left": left_ear_shoulder_y,
        "ear_shoulder_y_ratio_right": right_ear_shoulder_y,
        "ear_shoulder_y_ratio_mean": (left_ear_shoulder_y + right_ear_shoulder_y) / 2.0,
        "nose_ear_dx_ratio": _safe_div(abs(nose[0] - ear_mid[0]), body_scale),
        "nose_shoulder_dx_ratio": _safe_div(abs(nose[0] - shoulder_mid[0]), body_scale),
        "head_forward_ratio": _safe_div(abs(ear_mid[0] - shoulder_mid[0]), body_scale),
        "neck_to_shoulder_angle_left": abs(_line_angle_deg(left_ear, left_shoulder)),
        "neck_to_shoulder_angle_right": abs(_line_angle_deg(right_ear, right_shoulder)),
        "head_neck_torso_angle": _angle_at(nose, shoulder_mid, hip_mid),
        "shoulder_hip_dx_ratio": _safe_div(shoulder_hip_dx, body_scale),
        "shoulder_hip_dy_ratio": _safe_div(shoulder_hip_dy, body_scale),
        "torso_side_lean_ratio": _safe_div(shoulder_hip_dx, shoulder_hip_dy),
        "hip_shoulder_torso_angle": abs(_line_angle_deg(shoulder_mid, hip_mid) - 90.0),
    }


def compute_ergonomic_v2_features(df: pd.DataFrame) -> pd.DataFrame:
    ergonomic = compute_ergonomic_v2_base_features(df).reset_index(drop=True)
    if all(column in df.columns for column in ERGONOMIC_V2_EXTRA_COLUMNS):
        extra = df[ERGONOMIC_V2_EXTRA_COLUMNS].copy().reset_index(drop=True)
    else:
        get_raw_landmark_columns(df)
        rows = [_compute_ergonomic_v2_extra_row(row) for _, row in df.iterrows()]
        extra = pd.DataFrame(rows, columns=ERGONOMIC_V2_EXTRA_COLUMNS)
    return pd.concat([ergonomic, extra], axis=1)


def compute_view_features(df: pd.DataFrame) -> pd.DataFrame:
    if all(column in df.columns for column in VIEW_FEATURE_COLUMNS):
        return df[VIEW_FEATURE_COLUMNS].copy().reset_index(drop=True)
    output = pd.DataFrame(0.0, index=df.index, columns=VIEW_FEATURE_COLUMNS)
    if "view_angle" not in df.columns:
        output["view_unknown"] = 1.0
        return output.reset_index(drop=True)
    views = df["view_angle"].fillna("unknown").astype(str)
    output.loc[views == "front", "view_front"] = 1.0
    output.loc[views == "side_30", "view_side_30"] = 1.0
    output.loc[views == "side_90", "view_side_90"] = 1.0
    output.loc[~views.isin(["front", "side_30", "side_90"]), "view_unknown"] = 1.0
    return output.reset_index(drop=True)


def _available_ergonomic_features(df: pd.DataFrame) -> pd.DataFrame:
    if all(column in df.columns for column in ERGONOMIC_FEATURE_COLUMNS):
        return df[ERGONOMIC_FEATURE_COLUMNS].copy()
    return compute_ergonomic_features(df)


def build_feature_matrix(df: pd.DataFrame, feature_set: str) -> tuple[pd.DataFrame, list[str]]:
    if feature_set not in SUPPORTED_FEATURE_SETS:
        raise ValueError(f"Unsupported feature_set: {feature_set}")
    raw = None
    normalized = None
    ergonomic = None

    if feature_set == "raw_99":
        raw = df[get_raw_landmark_columns(df)].copy()
        matrix = raw
    elif feature_set == "normalized_99":
        normalized = compute_normalized_landmarks(df)
        matrix = normalized
    elif feature_set == "ergonomic_14":
        ergonomic = _available_ergonomic_features(df)
        matrix = ergonomic
    elif feature_set == "combined_raw_ergonomic":
        raw = df[get_raw_landmark_columns(df)].copy()
        ergonomic = _available_ergonomic_features(df)
        matrix = pd.concat([raw.reset_index(drop=True), ergonomic.reset_index(drop=True)], axis=1)
    elif feature_set == "combined_normalized_ergonomic":
        normalized = compute_normalized_landmarks(df)
        ergonomic = _available_ergonomic_features(df)
        matrix = pd.concat([normalized.reset_index(drop=True), ergonomic.reset_index(drop=True)], axis=1)
    elif feature_set == "ergonomic_v2":
        matrix = compute_ergonomic_v2_features(df)
    elif feature_set == "ergonomic_v2_with_view":
        ergonomic_v2 = compute_ergonomic_v2_features(df)
        view = compute_view_features(df)
        matrix = pd.concat([ergonomic_v2.reset_index(drop=True), view.reset_index(drop=True)], axis=1)
    elif feature_set == "combined_v2":
        normalized = compute_normalized_landmarks(df)
        ergonomic_v2 = compute_ergonomic_v2_features(df)
        matrix = pd.concat([normalized.reset_index(drop=True), ergonomic_v2.reset_index(drop=True)], axis=1)
    elif feature_set == "combined_v2_with_view":
        normalized = compute_normalized_landmarks(df)
        ergonomic_v2 = compute_ergonomic_v2_features(df)
        view = compute_view_features(df)
        matrix = pd.concat(
            [normalized.reset_index(drop=True), ergonomic_v2.reset_index(drop=True), view.reset_index(drop=True)],
            axis=1,
        )

    matrix = matrix.astype(np.float32)
    return matrix, list(matrix.columns)


def save_feature_schema(path: str | Path, feature_set: str, columns: list[str]) -> None:
    payload = {
        "schema_version": "2026-05-28",
        "feature_set": feature_set,
        "columns": columns,
        "metadata_columns": METADATA_COLUMNS,
        "supported_feature_sets": SUPPORTED_FEATURE_SETS,
        "notes": (
            "raw_99 uses MediaPipe x/y/z landmarks; normalized_99 centers on the shoulder midpoint "
            "and scales by max(shoulder_width, torso_length); ergonomic_14 contains interpretable "
            "geometric posture indicators."
        ),
    }
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_feature_schema(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))
