"""Model-loading and HGB feature helpers for the desktop app."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import cv2
import joblib
import numpy as np
import pandas as pd

try:
    from app.config.constants import NUM_POSE_LANDMARKS
except ImportError:
    from src.app.config.constants import NUM_POSE_LANDMARKS

try:
    from feature_schema import build_feature_matrix
except ImportError:
    from src.feature_schema import build_feature_matrix

try:
    from runtime_paths import resource_path
except ImportError:
    from src.runtime_paths import resource_path


def load_hgb_model(model_id: str) -> tuple[Any, Path]:
    """Load a registered HistGradientBoosting model by registry id."""
    model_path = resource_path(Path("models") / "registry" / model_id / "model.pkl")
    if not model_path.exists():
        raise FileNotFoundError(f"Khong tim thay model HGB: {model_path}")
    return joblib.load(model_path), model_path


def load_hgb_threshold(model_id: str, fallback_threshold: float) -> float:
    """Read calibrated HGB threshold from the model registry directory."""
    threshold_path = resource_path(Path("models") / "registry" / model_id / "threshold.json")
    if not threshold_path.exists():
        return fallback_threshold

    try:
        payload = json.loads(threshold_path.read_text(encoding="utf-8"))
        return float(payload.get("default", fallback_threshold))
    except Exception as exc:
        print(f"WARNING: Khong doc duoc threshold HGB, dung fallback {fallback_threshold}: {exc}")
        return fallback_threshold


def build_landmark_frame_dataframe(
    landmarks: Any,
    *,
    source_text: str,
    frame_index: int,
    cap: cv2.VideoCapture | None,
    source_type: str,
    session_start_timestamp: float | None,
    view_angle: str,
) -> pd.DataFrame:
    """Create the one-row DataFrame expected by feature_schema."""
    row: dict[str, Any] = {}
    for index, landmark in enumerate(landmarks[:NUM_POSE_LANDMARKS]):
        row[f"landmark_{index}_x"] = float(landmark.x)
        row[f"landmark_{index}_y"] = float(landmark.y)
        row[f"landmark_{index}_z"] = float(landmark.z)

    if cap is not None and source_type == "video_file":
        timestamp_sec = float(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)
    elif session_start_timestamp is not None:
        timestamp_sec = max(0.0, time.time() - session_start_timestamp)
    else:
        timestamp_sec = 0.0

    row.update(
        {
            "source_video": source_text,
            "frame_index": int(frame_index),
            "timestamp_sec": timestamp_sec,
            "sample_fps": 0.0,
            "video_fps": float(cap.get(cv2.CAP_PROP_FPS)) if cap is not None else 0.0,
            "participant_id": "unknown",
            "view_angle": view_angle,
            "camera_type": source_type,
        }
    )
    return pd.DataFrame([row])


def predict_hgb_probability(model: Any, frame_df: pd.DataFrame, feature_set: str) -> float:
    """Build features and return the Incorrect-posture probability."""
    model_input, _ = build_feature_matrix(frame_df, feature_set)
    if hasattr(model, "predict_proba"):
        return float(model.predict_proba(model_input)[0, 1])
    return float(np.asarray(model.predict(model_input))[0])

