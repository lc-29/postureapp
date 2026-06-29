"""Runtime constants for the desktop posture application."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from runtime_paths import app_base_dir, resource_path, writable_database_path
except ImportError:
    from src.runtime_paths import app_base_dir, resource_path, writable_database_path


BASE_DIR = app_base_dir()
DATABASE_PATH = writable_database_path()
MODEL_PATH = resource_path(Path("models") / "ann_best.keras")
SCALER_PATH = resource_path(Path("models") / "scaler.pkl")
ALARM_PATH = resource_path(Path("assets") / "sounds" / "alarm.wav")

ANN_MODE_NAME = "ANN"
RULE_BASED_MODE_NAME = "Rule-based Baseline"
HGB_BALANCED_MODE_NAME = "HistGradientBoosting (balanced best)"
HGB_HIGH_RECALL_MODE_NAME = "HistGradientBoosting (high recall demo)"
LEGACY_HGB_MODE_NAME = "HistGradientBoosting (best)"
HGB_DEFAULT_THRESHOLD = 0.50

HGB_MODE_CONFIGS: dict[str, dict[str, Any]] = {
    HGB_BALANCED_MODE_NAME: {
        "model_id": "hist_gradient_boosting__ergonomic_v2_with_view",
        "feature_set": "ergonomic_v2_with_view",
        "fallback_threshold": 0.76,
        "purpose": "Scientific result balanced between false positives and false negatives",
    },
    HGB_HIGH_RECALL_MODE_NAME: {
        "model_id": "hist_gradient_boosting__normalized_99",
        "feature_set": "normalized_99",
        "fallback_threshold": 0.50,
        "purpose": "Realtime demo prioritizing fewer missed incorrect posture frames",
    },
}

DEFAULT_CONFIG_DATA: dict[str, Any] = {
    "nguonCamera": "0",
    "thoiGianCanhBao": 5,
    "thoiGianChoCanhBao": 15,
    "batAmThanh": 1,
    "duongDanAmThanh": "assets/sounds/alarm.wav",
    "duongDanModel": "models/ann_best.keras",
    "duongDanScaler": "models/scaler.pkl",
    "cheDoGiaoDien": "light",
    "smoothingWindowFrames": 5,
    "smoothingThreshold": 0.5,
}

NUM_POSE_LANDMARKS = 33
FEATURES_PER_LANDMARK = 3
NUM_FEATURES = NUM_POSE_LANDMARKS * FEATURES_PER_LANDMARK

# Rule-based baseline thresholds copied from the existing app behavior.
MIN_VISIBILITY = 0.5
SHOULDER_Y_DIFF_THRESHOLD = 0.06
SHOULDER_TILT_ANGLE_THRESHOLD = 10.0
TORSO_LEAN_ANGLE_THRESHOLD = 12.0
HEAD_OFFSET_X_THRESHOLD = 0.10
NOSE_TO_SHOULDER_Y_THRESHOLD = -0.03
HAND_TO_MOUTH_RATIO_THRESHOLD = 0.45
HAND_TO_MOUTH_ABS_THRESHOLD = 0.13
HAND_POINT_MIN_VISIBILITY = 0.35
USE_ELBOW_ANGLE_FOR_CHIN_REST = False
CHIN_REST_ELBOW_MIN_ANGLE = 35.0
CHIN_REST_ELBOW_MAX_ANGLE = 145.0

VIDEO_WIDTH = 760
VIDEO_HEIGHT = 570
INFERENCE_WIDTH = 480
INFERENCE_HEIGHT = 360
LIVE_CAPTURE_WIDTH = 640
LIVE_CAPTURE_HEIGHT = 480
UPDATE_DELAY_MS = 10
CAPTURE_READ_RETRY_DELAY = 0.005
CAPTURE_FAIL_LIMIT = 90

STATUS_TEXT = {
    "DUNG_TU_THE": "TƯ THẾ ĐÚNG",
    "SAI_TU_THE": "SAI TƯ THẾ",
    "KHONG_PHAT_HIEN_NGUOI": "KHÔNG PHÁT HIỆN NGƯỜI",
    "DANG_KIEM_TRA": "ĐANG KIỂM TRA...",
}

RISK_LEVEL_TEXT = {
    "LOW": "Thấp",
    "MEDIUM": "Trung bình",
    "HIGH": "Cao",
    "CRITICAL": "Rất cao",
}

DATA_QUALITY_TEXT = {
    "ok": "Ổn",
    "zero_duration": "Thiếu thời lượng",
    "no_frame_summary": "Thiếu thống kê frame",
    "no_posture_logs": "Thiếu nhật ký tư thế",
    "missing_end_time": "Thiếu thời điểm kết thúc",
}

STATUS_COLORS = {
    "DUNG_TU_THE": "#15803d",
    "SAI_TU_THE": "#dc2626",
    "KHONG_PHAT_HIEN_NGUOI": "#64748b",
    "DANG_KIEM_TRA": "#b45309",
}
