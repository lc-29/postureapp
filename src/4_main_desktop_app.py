"""
Ung dung desktop phat hien loi tu the lam viec qua webcam/video.

Chuc nang chinh:
- Giao dien CustomTkinter light mode.
- Mo webcam, camera IP hoac tep video bang OpenCV.
- Trich xuat 33 landmark MediaPipe Pose thanh vector 99 dac trung.
- Du doan tu the dung/sai bang ANN da train va StandardScaler.
- Canh bao am thanh khi sai tu the lien tuc qua nguong.
- Luu phien lam viec, nhat ky canh bao va thong ke ngay vao SQLite schema
  tieng Viet.
"""

from __future__ import annotations

import os
import math
import subprocess
import sqlite3
import sys
import threading
import time
from collections import deque
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, ttk
from types import SimpleNamespace
from typing import Any

# Giam bot log cua TensorFlow/MediaPipe tren terminal khi chay app.
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import cv2
import customtkinter as ctk
import joblib
import mediapipe as mp
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageTk
from tensorflow.keras.models import load_model

try:
    from statistics_service import get_dashboard_data
except ImportError:
    from src.statistics_service import get_dashboard_data

try:
    from runtime_paths import (
        app_base_dir,
        ensure_runtime_database,
        is_frozen,
        resource_path,
        writable_database_path,
    )
except ImportError:
    from src.runtime_paths import (
        app_base_dir,
        ensure_runtime_database,
        is_frozen,
        resource_path,
        writable_database_path,
    )

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError:
    plt = None
    FigureCanvasTkAgg = None


BASE_DIR = app_base_dir()
DATABASE_PATH = writable_database_path()
MODEL_PATH = resource_path(Path("models") / "ann_best.keras")
SCALER_PATH = resource_path(Path("models") / "scaler.pkl")
ALARM_PATH = resource_path(Path("assets") / "sounds" / "alarm.wav")

NUM_POSE_LANDMARKS = 33
FEATURES_PER_LANDMARK = 3
NUM_FEATURES = NUM_POSE_LANDMARKS * FEATURES_PER_LANDMARK

# =========================
# Nguong rule-based baseline
# =========================
# Cac nguong duoc copy co chon loc tu src/1_rule_based_baseline.py de baseline
# trong app chinh dung dung cong thuc so sanh, khong import file bat dau bang so.
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
FONT = cv2.FONT_HERSHEY_SIMPLEX
APP_FONT_FAMILY = "Segoe UI"

if plt is not None:
    plt.rcParams["font.family"] = APP_FONT_FAMILY
    plt.rcParams["axes.unicode_minus"] = False

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

THEMES = {
    "light": {
        "app_bg": "#f6f8fb",
        "surface": "#ffffff",
        "surface_muted": "#eef2f7",
        "surface_subtle": "#f8fafc",
        "border": "#d7dde8",
        "border_soft": "#e5eaf2",
        "text": "#162033",
        "muted": "#5b677a",
        "muted_light": "#7b8798",
        "success": "#15803d",
        "success_bg": "#dcfce7",
        "danger": "#dc2626",
        "danger_bg": "#fee2e2",
        "warning": "#b45309",
        "warning_bg": "#fef3c7",
        "info": "#2563eb",
        "info_bg": "#dbeafe",
        "neutral": "#64748b",
        "neutral_bg": "#e2e8f0",
    },
    "dark": {
        "app_bg": "#0f172a",
        "surface": "#111827",
        "surface_muted": "#1f2937",
        "surface_subtle": "#172033",
        "border": "#334155",
        "border_soft": "#243244",
        "text": "#f8fafc",
        "muted": "#cbd5e1",
        "muted_light": "#94a3b8",
        "success": "#22c55e",
        "success_bg": "#052e16",
        "danger": "#f87171",
        "danger_bg": "#450a0a",
        "warning": "#fbbf24",
        "warning_bg": "#422006",
        "info": "#60a5fa",
        "info_bg": "#172554",
        "neutral": "#94a3b8",
        "neutral_bg": "#1e293b",
    },
}
THEME = dict(THEMES["light"])


mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


def now_iso() -> str:
    """Tra ve thoi gian hien tai dang ISO de luu SQLite."""
    return datetime.now().isoformat(timespec="seconds")


def today_text() -> str:
    """Tra ve ngay hien tai dang YYYY-MM-DD."""
    return datetime.now().date().isoformat()


def format_duration(seconds: float | int | None) -> str:
    """
    Dinh dang thoi gian de hien thi than thien.

    - Duoi 60 giay: 45s
    - Tu 60 giay den duoi 1 gio: 1p30s
    - Tu 1 gio tro len: 1h30p20s
    """
    if seconds is None or seconds <= 0:
        return "0s"

    total_seconds = int(round(seconds))
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    remaining_seconds = total_seconds % 60

    if hours > 0:
        return f"{hours}h{minutes}p{remaining_seconds}s"
    if minutes > 0:
        return f"{minutes}p{remaining_seconds}s"
    return f"{remaining_seconds}s"


def app_font(size: int, weight: str | None = None) -> ctk.CTkFont:
    """Create a CTk font that renders Vietnamese well on Windows."""
    kwargs: dict[str, Any] = {"family": APP_FONT_FAMILY, "size": size}
    if weight is not None:
        kwargs["weight"] = weight
    return ctk.CTkFont(**kwargs)


def translate_risk_level(level: str | None) -> str:
    return RISK_LEVEL_TEXT.get(str(level or "LOW"), str(level or "LOW"))


def translate_data_quality(note: str | None) -> str:
    if not note:
        return ""
    parts = [part for part in str(note).split(";") if part]
    translated = [DATA_QUALITY_TEXT.get(part, part) for part in parts]
    return "; ".join(translated)


def load_overlay_font(scale: float, bold: bool = False) -> ImageFont.ImageFont:
    """Load a Unicode-capable font for video overlay text."""
    font_size = max(13, int(28 * scale))
    font_names = ["segoeuib.ttf", "segoeui.ttf"] if bold else ["segoeui.ttf", "arial.ttf"]
    for font_name in font_names:
        font_path = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts" / font_name
        if font_path.exists():
            return ImageFont.truetype(str(font_path), font_size)
    return ImageFont.load_default()


def get_db_connection() -> sqlite3.Connection:
    """
    Tao ket noi SQLite va bat foreign key.

    Neu database chua ton tai, app tu tao database runtime lan dau.
    """
    db_path = ensure_runtime_database()

    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def project_path_from_text(path_text: str | None, fallback: Path) -> Path:
    """
    Chuyen duong dan trong database thanh Path tuyet doi theo project.
    """
    if not path_text:
        return fallback

    path = Path(path_text)
    if path.is_absolute():
        return path

    return resource_path(path)


def resolve_source(source_text: str) -> tuple[int | str, str]:
    """
    Phan loai nguon camera/video de mo bang OpenCV.

    - Chuoi so: webcam.
    - http/https/rtsp: ip_camera.
    - File ton tai: video_file.
    - Con lai: xem nhu duong dan video_file de OpenCV tu xu ly.
    """
    source = str(source_text).strip()
    if source == "":
        source = "0"

    if source.isdigit():
        return int(source), "webcam"

    lower_source = source.lower()
    if lower_source.startswith(("http://", "https://", "rtsp://")):
        return source, "ip_camera"

    source_path = Path(source)
    project_source_path = BASE_DIR / source_path
    if source_path.exists():
        return source, "video_file"

    if not source_path.is_absolute() and project_source_path.exists():
        return str(project_source_path), "video_file"

    return source, "video_file"


def draw_text(
    frame: np.ndarray,
    text: str,
    position: tuple[int, int],
    color: tuple[int, int, int],
    scale: float = 0.7,
    thickness: int = 2,
) -> None:
    """Ve chu co vien den de de doc tren video."""
    font = load_overlay_font(scale, bold=thickness >= 2)
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    drawer = ImageDraw.Draw(image)
    x, y = position
    text_position = (x, max(0, y - int(24 * scale)))
    rgb_color = (color[2], color[1], color[0])
    outline_width = max(1, thickness)
    drawer.text(
        text_position,
        text,
        font=font,
        fill=rgb_color,
        stroke_width=outline_width,
        stroke_fill=(0, 0, 0),
    )
    frame[:, :, :] = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)


def create_default_features(valid: bool = False) -> dict[str, float | bool]:
    """Tao bo dac trung mac dinh cho baseline khi thieu landmark."""
    return {
        "valid": valid,
        "shoulder_y_diff": 0.0,
        "shoulder_tilt_angle": 0.0,
        "torso_lean_angle": 0.0,
        "head_offset_x": 0.0,
        "nose_to_shoulder_y": 0.0,
        "visibility": 0.0,
        "left_hand_mouth_distance": 999.0,
        "right_hand_mouth_distance": 999.0,
        "left_hand_mouth_ratio": 999.0,
        "right_hand_mouth_ratio": 999.0,
        "left_hand_face_ratio": 999.0,
        "right_hand_face_ratio": 999.0,
        "left_hand_near_mouth": False,
        "right_hand_near_mouth": False,
        "left_elbow_angle": 0.0,
        "right_elbow_angle": 0.0,
        "left_hand_near_face": False,
        "right_hand_near_face": False,
        "left_chin_rest": False,
        "right_chin_rest": False,
        "chin_rest_detected": False,
        "mouth_center_x": 0.0,
        "mouth_center_y": 0.0,
        "left_nearest_hand_x": 0.0,
        "left_nearest_hand_y": 0.0,
        "right_nearest_hand_x": 0.0,
        "right_nearest_hand_y": 0.0,
    }


def get_landmark(landmarks: list[Any], landmark_enum: Any) -> Any | None:
    """Lay landmark MediaPipe theo enum, tra None neu thieu diem."""
    try:
        return landmarks[landmark_enum.value]
    except (IndexError, AttributeError, TypeError):
        return None


def midpoint(p1: Any, p2: Any) -> tuple[float, float]:
    """Tinh trung diem 2 landmark trong toa do chuan hoa."""
    return ((p1.x + p2.x) / 2.0, (p1.y + p2.y) / 2.0)


def calculate_distance_2d(p1: Any, p2: Any) -> float:
    """Tinh khoang cach 2D bang toa do chuan hoa MediaPipe."""
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def get_visible_landmarks(
    landmarks: list[Any],
    landmark_enums: list[Any],
    min_visibility: float = HAND_POINT_MIN_VISIBILITY,
) -> list[Any]:
    """Lay cac diem co visibility du tot de rule tay/mieng on dinh hon."""
    visible_points: list[Any] = []
    for landmark_enum in landmark_enums:
        point = get_landmark(landmarks, landmark_enum)
        if point is not None and getattr(point, "visibility", 0.0) >= min_visibility:
            visible_points.append(point)
    return visible_points


def calculate_min_distance_to_point(
    points: list[Any], target_point: Any
) -> tuple[float, Any | None]:
    """Tinh khoang cach nho nhat tu danh sach diem den mot diem dich."""
    if not points:
        return 999.0, None

    nearest_point = None
    min_distance = 999.0
    for point in points:
        distance = calculate_distance_2d(point, target_point)
        if distance < min_distance:
            min_distance = distance
            nearest_point = point
    return min_distance, nearest_point


def calculate_angle_3_points(a: Any, b: Any, c: Any) -> float:
    """Tinh goc ABC, dung cho rule goc khuyu tay neu can."""
    ba_x = a.x - b.x
    ba_y = a.y - b.y
    bc_x = c.x - b.x
    bc_y = c.y - b.y

    ba_length = math.sqrt(ba_x**2 + ba_y**2)
    bc_length = math.sqrt(bc_x**2 + bc_y**2)
    if ba_length < 1e-6 or bc_length < 1e-6:
        return 0.0

    cosine_angle = (ba_x * bc_x + ba_y * bc_y) / (ba_length * bc_length)
    cosine_angle = max(-1.0, min(1.0, cosine_angle))
    return math.degrees(math.acos(cosine_angle))


def calculate_line_angle_degrees(p1: Any, p2: Any) -> float:
    """Tinh goc cua duong noi hai diem so voi phuong ngang."""
    dx = abs(p2.x - p1.x)
    dy = abs(p2.y - p1.y)
    return math.degrees(math.atan2(dy, dx))


def calculate_torso_lean_angle(
    mid_shoulder: tuple[float, float], mid_hip: tuple[float, float]
) -> float:
    """Tinh goc lech cua truc than so voi phuong thang dung."""
    dx = abs(mid_shoulder[0] - mid_hip[0])
    dy = abs(mid_shoulder[1] - mid_hip[1])
    if dy < 1e-6:
        return 90.0
    return abs(math.degrees(math.atan2(dx, dy)))


def extract_posture_features(landmarks: list[Any]) -> dict[str, float | bool]:
    """Trich xuat cac dac trung hinh hoc dung cho rule-based baseline."""
    nose = get_landmark(landmarks, mp_pose.PoseLandmark.NOSE)
    left_shoulder = get_landmark(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER)
    right_shoulder = get_landmark(landmarks, mp_pose.PoseLandmark.RIGHT_SHOULDER)
    left_hip = get_landmark(landmarks, mp_pose.PoseLandmark.LEFT_HIP)
    right_hip = get_landmark(landmarks, mp_pose.PoseLandmark.RIGHT_HIP)
    left_elbow = get_landmark(landmarks, mp_pose.PoseLandmark.LEFT_ELBOW)
    right_elbow = get_landmark(landmarks, mp_pose.PoseLandmark.RIGHT_ELBOW)
    left_wrist = get_landmark(landmarks, mp_pose.PoseLandmark.LEFT_WRIST)
    right_wrist = get_landmark(landmarks, mp_pose.PoseLandmark.RIGHT_WRIST)
    mouth_left = get_landmark(landmarks, mp_pose.PoseLandmark.MOUTH_LEFT)
    mouth_right = get_landmark(landmarks, mp_pose.PoseLandmark.MOUTH_RIGHT)

    required_landmarks = [
        nose,
        left_shoulder,
        right_shoulder,
        left_hip,
        right_hip,
    ]
    if any(point is None for point in required_landmarks):
        return create_default_features(valid=False)

    mid_shoulder = midpoint(left_shoulder, right_shoulder)
    mid_hip = midpoint(left_hip, right_hip)

    shoulder_y_diff = abs(left_shoulder.y - right_shoulder.y)
    shoulder_tilt_angle = calculate_line_angle_degrees(left_shoulder, right_shoulder)
    torso_lean_angle = calculate_torso_lean_angle(mid_shoulder, mid_hip)
    head_offset_x = abs(nose.x - mid_shoulder[0])
    nose_to_shoulder_y = nose.y - mid_shoulder[1]
    visibility = sum(point.visibility for point in required_landmarks) / len(
        required_landmarks
    )

    left_hand_mouth_distance = 999.0
    right_hand_mouth_distance = 999.0
    left_hand_mouth_ratio = 999.0
    right_hand_mouth_ratio = 999.0
    left_elbow_angle = 0.0
    right_elbow_angle = 0.0
    left_hand_near_mouth = False
    right_hand_near_mouth = False
    left_chin_rest = False
    right_chin_rest = False

    shoulder_width = calculate_distance_2d(left_shoulder, right_shoulder)

    # MediaPipe khong co diem cam chinh xac, nen baseline dung trung diem mieng
    # lam dai dien vung mieng/cam va lay diem tay gan nhat de phat hien chong cam.
    if mouth_left is not None and mouth_right is not None:
        mouth_x, mouth_y = midpoint(mouth_left, mouth_right)
        mouth_center = SimpleNamespace(x=mouth_x, y=mouth_y)
    else:
        mouth_center = SimpleNamespace(x=nose.x, y=nose.y)

    left_hand_points = get_visible_landmarks(
        landmarks,
        [
            mp_pose.PoseLandmark.LEFT_WRIST,
            mp_pose.PoseLandmark.LEFT_INDEX,
            mp_pose.PoseLandmark.LEFT_PINKY,
            mp_pose.PoseLandmark.LEFT_THUMB,
        ],
    )
    right_hand_points = get_visible_landmarks(
        landmarks,
        [
            mp_pose.PoseLandmark.RIGHT_WRIST,
            mp_pose.PoseLandmark.RIGHT_INDEX,
            mp_pose.PoseLandmark.RIGHT_PINKY,
            mp_pose.PoseLandmark.RIGHT_THUMB,
        ],
    )

    left_hand_mouth_distance, left_nearest_hand_point = calculate_min_distance_to_point(
        left_hand_points, mouth_center
    )
    right_hand_mouth_distance, right_nearest_hand_point = calculate_min_distance_to_point(
        right_hand_points, mouth_center
    )

    if shoulder_width > 1e-6:
        left_hand_mouth_ratio = left_hand_mouth_distance / shoulder_width
        right_hand_mouth_ratio = right_hand_mouth_distance / shoulder_width

    left_hand_near_mouth = (
        left_hand_mouth_ratio < HAND_TO_MOUTH_RATIO_THRESHOLD
        or left_hand_mouth_distance < HAND_TO_MOUTH_ABS_THRESHOLD
    )
    right_hand_near_mouth = (
        right_hand_mouth_ratio < HAND_TO_MOUTH_RATIO_THRESHOLD
        or right_hand_mouth_distance < HAND_TO_MOUTH_ABS_THRESHOLD
    )

    if left_elbow is not None and left_wrist is not None:
        left_elbow_angle = calculate_angle_3_points(
            left_shoulder, left_elbow, left_wrist
        )
    if right_elbow is not None and right_wrist is not None:
        right_elbow_angle = calculate_angle_3_points(
            right_shoulder, right_elbow, right_wrist
        )

    if USE_ELBOW_ANGLE_FOR_CHIN_REST:
        left_elbow_valid = (
            CHIN_REST_ELBOW_MIN_ANGLE
            <= left_elbow_angle
            <= CHIN_REST_ELBOW_MAX_ANGLE
        )
        right_elbow_valid = (
            CHIN_REST_ELBOW_MIN_ANGLE
            <= right_elbow_angle
            <= CHIN_REST_ELBOW_MAX_ANGLE
        )
        left_chin_rest = left_hand_near_mouth and left_elbow_valid
        right_chin_rest = right_hand_near_mouth and right_elbow_valid
    else:
        left_chin_rest = left_hand_near_mouth
        right_chin_rest = right_hand_near_mouth

    chin_rest_detected = left_chin_rest or right_chin_rest
    left_nearest_hand_x = left_nearest_hand_point.x if left_nearest_hand_point else 0.0
    left_nearest_hand_y = left_nearest_hand_point.y if left_nearest_hand_point else 0.0
    right_nearest_hand_x = right_nearest_hand_point.x if right_nearest_hand_point else 0.0
    right_nearest_hand_y = right_nearest_hand_point.y if right_nearest_hand_point else 0.0

    return {
        "valid": True,
        "shoulder_y_diff": shoulder_y_diff,
        "shoulder_tilt_angle": shoulder_tilt_angle,
        "torso_lean_angle": torso_lean_angle,
        "head_offset_x": head_offset_x,
        "nose_to_shoulder_y": nose_to_shoulder_y,
        "visibility": visibility,
        "left_hand_mouth_distance": left_hand_mouth_distance,
        "right_hand_mouth_distance": right_hand_mouth_distance,
        "left_hand_mouth_ratio": left_hand_mouth_ratio,
        "right_hand_mouth_ratio": right_hand_mouth_ratio,
        "left_hand_face_ratio": left_hand_mouth_ratio,
        "right_hand_face_ratio": right_hand_mouth_ratio,
        "left_hand_near_mouth": left_hand_near_mouth,
        "right_hand_near_mouth": right_hand_near_mouth,
        "left_elbow_angle": left_elbow_angle,
        "right_elbow_angle": right_elbow_angle,
        "left_hand_near_face": left_hand_near_mouth,
        "right_hand_near_face": right_hand_near_mouth,
        "left_chin_rest": left_chin_rest,
        "right_chin_rest": right_chin_rest,
        "chin_rest_detected": chin_rest_detected,
        "mouth_center_x": mouth_center.x,
        "mouth_center_y": mouth_center.y,
        "left_nearest_hand_x": left_nearest_hand_x,
        "left_nearest_hand_y": left_nearest_hand_y,
        "right_nearest_hand_x": right_nearest_hand_x,
        "right_nearest_hand_y": right_nearest_hand_y,
    }


def classify_posture_rule_based(
    features: dict[str, float | bool],
) -> tuple[str, list[str]]:
    """Phan loai tu the bang cac nguong rule-based baseline."""
    if not features.get("valid", False):
        return "NO_PERSON_OR_LOW_CONFIDENCE", []

    visibility = float(features["visibility"])
    if visibility < MIN_VISIBILITY:
        return "NO_PERSON_OR_LOW_CONFIDENCE", []

    warnings: list[str] = []

    if (
        float(features["shoulder_y_diff"]) > SHOULDER_Y_DIFF_THRESHOLD
        or float(features["shoulder_tilt_angle"]) > SHOULDER_TILT_ANGLE_THRESHOLD
    ):
        warnings.append("Lệch vai hoặc nghiêng vai")

    if float(features["torso_lean_angle"]) > TORSO_LEAN_ANGLE_THRESHOLD:
        warnings.append("Thân người bị nghiêng")

    if float(features["head_offset_x"]) > HEAD_OFFSET_X_THRESHOLD:
        warnings.append("Đầu lệch khỏi trục vai")

    if float(features["nose_to_shoulder_y"]) > NOSE_TO_SHOULDER_Y_THRESHOLD:
        warnings.append("Có dấu hiệu cúi đầu")

    if bool(features.get("chin_rest_detected", False)):
        warnings.append("Có dấu hiệu chống cằm / tay gần miệng")

    if warnings:
        return "INCORRECT", warnings

    return "CORRECT", []


# Dung module chung de GUI va baseline script co cung logic phan loai.
try:
    from posture_baseline import (
        classify_posture_rule_based,
        create_default_features,
        extract_posture_features,
    )
except ImportError:
    pass


class PostureApp(ctk.CTk):
    """Ung dung desktop phat hien tu the lam viec realtime."""

    def __init__(self) -> None:
        super().__init__()

        self.title("Ứng dụng phát hiện tư thế làm việc")
        self.geometry("1180x680")
        self.minsize(1080, 640)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Thanh phan AI va video.
        self.model: Any | None = None
        self.scaler: Any | None = None
        self.pose: Any | None = None
        self.cap: cv2.VideoCapture | None = None
        self.capture_thread: threading.Thread | None = None
        self.capture_stop_event = threading.Event()
        self.frame_lock = threading.Lock()
        self.latest_capture_frame: np.ndarray | None = None
        self.latest_capture_time = 0.0
        self.last_consumed_capture_time = 0.0
        self.capture_read_failures = 0
        self.capture_error_message: str | None = None

        # Trang thai phien chay.
        self.is_running = False
        self.current_session_id: int | None = None
        self.current_user_id: int | None = None
        self.current_source: int | str | None = None
        self.current_source_type = "webcam"
        self.frame_index = 0
        self.total_frames = 0
        self.correct_frames = 0
        self.incorrect_frames = 0
        self.no_person_frames = 0
        self.warning_count = 0
        self.confidence_sum = 0.0
        self.confidence_count = 0
        self.incorrect_start_time: float | None = None
        self.incorrect_confirmed = False
        self.confirmed_incorrect_start_time: float | None = None
        self.last_alarm_time = 0.0
        self.last_logged_status: str | None = None
        self.current_status = "DANG_KIEM_TRA"
        self.fps = 0.0
        self.previous_frame_time: float | None = None
        self.warning_seconds = 5.0
        self.warning_cooldown_seconds = 15.0
        self.alarm_enabled = True
        self.prediction_mode = "ANN"
        self.alarm_is_playing = False
        self.alarm_stop_requested = False
        self.alarm_thread: threading.Thread | None = None
        self.session_start_time: datetime | None = None
        self.correct_seconds = 0.0
        self.incorrect_seconds = 0.0
        self.current_prob_incorrect: float | None = None
        self.current_confidence: float | None = None
        self.probability_window: deque[float] = deque(maxlen=5)
        self.smoothing_window_frames = 5
        self.smoothing_threshold = 0.5
        self.last_frame_elapsed = 0.0
        self.update_after_id: str | None = None
        self.metric_labels: dict[str, ctk.CTkLabel] = {}
        self.current_theme_mode = "light"

        # Anh hien thi tren Tkinter can giu reference de khong bi garbage collect.
        self.video_image: ImageTk.PhotoImage | None = None

        # Cau hinh mac dinh neu database chua doc duoc.
        self.config_data = {
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

        self.set_theme_mode("light", rebuild=False)
        ctk.set_default_color_theme("blue")

        self.create_widgets()
        self.initialize_from_database()
        self.update_status_ui("DANG_KIEM_TRA", None)
        self.update_counter_labels()

    # =========================
    # Khoi tao UI
    # =========================
    def set_theme_mode(self, mode: str, rebuild: bool = True) -> None:
        """Doi palette light/dark va dung lai UI khi an toan."""
        normalized_mode = str(mode).lower()
        if normalized_mode not in THEMES:
            normalized_mode = "light"

        if rebuild and self.is_running:
            messagebox.showinfo(
                "Đổi giao diện",
                "Hãy dừng camera/video trước khi đổi Light/Dark mode.",
            )
            if hasattr(self, "theme_segment"):
                self.theme_segment.set(self.current_theme_mode.title())
            return

        self.current_theme_mode = normalized_mode
        self.config_data["cheDoGiaoDien"] = normalized_mode
        THEME.clear()
        THEME.update(THEMES[normalized_mode])
        ctk.set_appearance_mode(normalized_mode)

        if not rebuild:
            return

        for child in self.winfo_children():
            child.destroy()
        self.metric_labels = {}
        self.create_widgets()
        self.apply_config_to_gui()
        self.update_status_ui(self.current_status, self.current_confidence)
        self.update_counter_labels()
        if self.is_rule_based_mode():
            self.baseline_info_frame.grid()
        else:
            self.baseline_info_frame.grid_remove()

    def on_theme_changed(self, selected_mode: str) -> None:
        """Xu ly nguoi dung chon Light/Dark mode."""
        self.set_theme_mode(selected_mode.lower(), rebuild=True)

    def create_widgets(self) -> None:
        """Tao giao dien CustomTkinter light mode."""
        self.configure(fg_color=THEME["app_bg"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.video_frame = ctk.CTkFrame(
            self,
            fg_color=THEME["surface"],
            border_color=THEME["border"],
            border_width=1,
            corner_radius=8,
        )
        self.video_frame.grid(row=0, column=0, padx=(16, 8), pady=16, sticky="nsew")
        self.video_frame.grid_rowconfigure(0, weight=1)
        self.video_frame.grid_rowconfigure(1, weight=0)
        self.video_frame.grid_columnconfigure(0, weight=1)

        self.video_label = ctk.CTkLabel(
            self.video_frame,
            text="Chưa bật camera\nChọn nguồn và bấm Bắt đầu",
            font=app_font(size=24, weight="bold"),
            text_color=THEME["muted"],
            fg_color=THEME["surface_muted"],
            corner_radius=6,
            width=VIDEO_WIDTH,
            height=VIDEO_HEIGHT,
        )
        self.video_label.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")

        self.baseline_info_frame = ctk.CTkFrame(
            self.video_frame,
            fg_color=THEME["surface_subtle"],
            border_color=THEME["border_soft"],
            border_width=1,
            corner_radius=8,
        )
        self.baseline_info_frame.grid(
            row=1,
            column=0,
            padx=12,
            pady=(0, 12),
            sticky="ew",
        )
        self.baseline_info_label = ctk.CTkLabel(
            self.baseline_info_frame,
            text="Baseline: chưa chạy",
            justify="left",
            anchor="w",
            font=app_font(size=13),
            text_color=THEME["text"],
        )
        self.baseline_info_label.pack(padx=12, pady=10, fill="x")
        self.baseline_info_frame.grid_remove()

        self.control_frame = ctk.CTkScrollableFrame(
            self,
            width=380,
            fg_color=THEME["surface"],
            border_color=THEME["border"],
            border_width=1,
            corner_radius=8,
        )
        self.control_frame.grid(row=0, column=1, padx=(8, 16), pady=16, sticky="ns")

        self.title_label = ctk.CTkLabel(
            self.control_frame,
            text="PHÁT HIỆN TƯ THẾ",
            font=app_font(size=24, weight="bold"),
            text_color=THEME["text"],
            anchor="w",
        )
        self.title_label.pack(padx=16, pady=(16, 2), fill="x")

        ctk.CTkLabel(
            self.control_frame,
            text="Giám sát tư thế theo thời gian thực",
            font=app_font(size=13),
            text_color=THEME["muted"],
            anchor="w",
        ).pack(padx=16, pady=(0, 12), fill="x")

        theme_section = self.create_sidebar_section("Giao diện")
        self.theme_segment = ctk.CTkSegmentedButton(
            theme_section,
            values=["Light", "Dark"],
            command=self.on_theme_changed,
            selected_color=THEME["info"],
            selected_hover_color="#1d4ed8",
            unselected_color=THEME["surface"],
            unselected_hover_color=THEME["surface_muted"],
            text_color=THEME["text"],
        )
        self.theme_segment.set(self.current_theme_mode.title())
        self.theme_segment.pack(padx=12, pady=(10, 12), fill="x")

        status_section = self.create_sidebar_section("Trạng thái hiện tại")

        self.status_label = ctk.CTkLabel(
            status_section,
            text="ĐANG KIỂM TRA...",
            font=app_font(size=24, weight="bold"),
            text_color=STATUS_COLORS["DANG_KIEM_TRA"],
            anchor="w",
        )
        self.status_label.pack(padx=12, pady=(10, 4), fill="x")

        self.confidence_label = ctk.CTkLabel(
            status_section,
            text="Độ tin cậy: --",
            font=app_font(size=15),
            text_color=THEME["muted"],
            anchor="w",
        )
        self.confidence_label.pack(padx=12, pady=(0, 4), fill="x")

        self.incorrect_time_label = ctk.CTkLabel(
            status_section,
            text="Thời gian sai: 0.0s / 5.0s",
            font=app_font(size=15),
            text_color=THEME["muted"],
            anchor="w",
        )
        self.incorrect_time_label.pack(padx=12, pady=(0, 12), fill="x")

        source_section = self.create_sidebar_section("Nguồn đầu vào")
        self.source_entry = self.create_labeled_entry(
            source_section,
            "Camera, IP hoặc video",
            "0",
        )

        detection_section = self.create_sidebar_section("Nhận diện")
        mode_label = ctk.CTkLabel(
            detection_section,
            text="Chế độ",
            anchor="w",
            text_color=THEME["muted"],
            font=app_font(size=13),
        )
        mode_label.pack(padx=12, pady=(10, 2), fill="x")

        self.mode_combobox = ctk.CTkComboBox(
            detection_section,
            values=[
                "ANN",
                "Rule-based Baseline",
            ],
            state="readonly",
            command=self.on_mode_changed,
            border_color=THEME["border"],
            button_color=THEME["info"],
            button_hover_color="#1d4ed8",
        )
        self.mode_combobox.set("ANN")
        self.mode_combobox.pack(padx=12, pady=(0, 12), fill="x")

        alert_section = self.create_sidebar_section("Cảnh báo")
        self.warning_entry = self.create_labeled_entry(
            alert_section,
            "Cảnh báo sau (giây)",
            "5",
        )
        self.cooldown_entry = self.create_labeled_entry(
            alert_section,
            "Thời gian chờ giữa cảnh báo (giây)",
            "15",
        )
        self.smoothing_window_entry = self.create_labeled_entry(
            alert_section,
            "Làm mượt xác suất (frame)",
            "5",
        )
        self.smoothing_threshold_entry = self.create_labeled_entry(
            alert_section,
            "Ngưỡng sai sau làm mượt",
            "0.5",
        )

        self.sound_switch = ctk.CTkSwitch(
            alert_section,
            text="Bật âm thanh cảnh báo",
            onvalue=1,
            offvalue=0,
            text_color=THEME["text"],
            progress_color=THEME["info"],
        )
        self.sound_switch.pack(padx=12, pady=(8, 12), anchor="w")
        self.sound_switch.select()

        action_section = self.create_sidebar_section("Thao tác")
        self.start_button = ctk.CTkButton(
            action_section,
            text="Bắt đầu",
            command=self.start_camera,
            height=36,
            fg_color=THEME["info"],
            hover_color="#1d4ed8",
        )
        self.start_button.pack(padx=12, pady=(10, 6), fill="x")

        self.stop_button = ctk.CTkButton(
            action_section,
            text="Dừng",
            command=self.stop_camera,
            height=36,
            fg_color=THEME["danger"],
            hover_color="#b91c1c",
            state="disabled",
        )
        self.stop_button.pack(padx=12, pady=6, fill="x")

        self.save_button = ctk.CTkButton(
            action_section,
            text="Lưu cài đặt",
            command=self.save_cai_dat_from_gui,
            height=34,
            fg_color=THEME["neutral"],
            hover_color="#475569",
        )
        self.save_button.pack(padx=12, pady=6, fill="x")

        self.stats_button = ctk.CTkButton(
            action_section,
            text="Xem thống kê",
            command=self.show_statistics,
            height=34,
            fg_color=THEME["success"],
            hover_color="#166534",
        )
        self.stats_button.pack(padx=12, pady=(6, 12), fill="x")

        summary_section = self.create_sidebar_section("Phiên hiện tại")
        self.metrics_frame = ctk.CTkFrame(summary_section, fg_color="transparent")
        self.metrics_frame.pack(padx=10, pady=(10, 12), fill="x")
        for column_index in range(2):
            self.metrics_frame.grid_columnconfigure(column_index, weight=1, uniform="metric")

        metric_specs = [
            ("total", "Tổng frame"),
            ("correct", "Đúng"),
            ("incorrect", "Sai"),
            ("no_person", "Không người"),
            ("warnings", "Cảnh báo"),
            ("fps", "FPS"),
        ]
        self.metric_labels = {}
        for index, (key, title) in enumerate(metric_specs):
            card = ctk.CTkFrame(
                self.metrics_frame,
                fg_color=THEME["surface_subtle"],
                border_color=THEME["border_soft"],
                border_width=1,
                corner_radius=8,
            )
            card.grid(
                row=index // 2,
                column=index % 2,
                padx=4,
                pady=4,
                sticky="nsew",
            )
            ctk.CTkLabel(
                card,
                text=title,
                font=app_font(size=11),
                text_color=THEME["muted"],
                anchor="w",
            ).pack(padx=10, pady=(8, 0), fill="x")
            value_label = ctk.CTkLabel(
                card,
                text="0",
                font=app_font(size=18, weight="bold"),
                text_color=THEME["text"],
                anchor="w",
            )
            value_label.pack(padx=10, pady=(0, 8), fill="x")
            self.metric_labels[key] = value_label

        self.info_label = ctk.CTkLabel(
            summary_section,
            text="Chế độ ANN lưu thống kê vào SQLite. Rule-based chỉ dùng để kiểm tra baseline.",
            justify="left",
            anchor="w",
            wraplength=320,
            text_color=THEME["muted"],
            font=app_font(size=12),
        )
        self.info_label.pack(padx=12, pady=(0, 12), fill="x")

    def create_sidebar_section(self, title: str) -> ctk.CTkFrame:
        """Tao section card trong sidebar."""
        section = ctk.CTkFrame(
            self.control_frame,
            fg_color=THEME["surface_subtle"],
            border_color=THEME["border_soft"],
            border_width=1,
            corner_radius=8,
        )
        section.pack(padx=16, pady=(0, 12), fill="x")
        ctk.CTkLabel(
            section,
            text=title,
            anchor="w",
            font=app_font(size=14, weight="bold"),
            text_color=THEME["text"],
        ).pack(padx=12, pady=(10, 0), fill="x")
        return section

    def create_labeled_entry(
        self,
        parent: Any,
        label_text: str,
        default_value: str,
    ) -> ctk.CTkEntry:
        """Tao label va entry theo cung style."""
        label = ctk.CTkLabel(
            parent,
            text=label_text,
            anchor="w",
            text_color=THEME["muted"],
            font=app_font(size=13),
        )
        label.pack(padx=12, pady=(10, 2), fill="x")

        entry = ctk.CTkEntry(
            parent,
            border_color=THEME["border"],
            fg_color=THEME["surface"],
            text_color=THEME["text"],
        )
        entry.insert(0, default_value)
        entry.pack(padx=12, pady=(0, 4), fill="x")
        return entry

    def on_mode_changed(self, selected_mode: str) -> None:
        """Cap nhat panel baseline khi nguoi dung doi mode luc chua chay."""
        if self.is_running:
            return

        self.prediction_mode = selected_mode
        if self.is_rule_based_mode():
            self.baseline_info_frame.grid()
            self.baseline_info_label.configure(text="Baseline: chưa chạy")
        else:
            self.baseline_info_frame.grid_remove()

    # =========================
    # Database va cau hinh
    # =========================
    def initialize_from_database(self) -> None:
        """Doc user va cau hinh ban dau tu SQLite."""
        try:
            self.current_user_id = self.get_default_user_id()
            self.config_data = self.load_cai_dat()
            self.apply_config_to_gui()
        except Exception as exc:
            messagebox.showerror("Lỗi database", f"{exc}")
            print(f"ERROR: Khong doc duoc database: {exc}")
            self.start_button.configure(state="disabled")
            self.save_button.configure(state="disabled")
            self.stats_button.configure(state="disabled")

    def get_default_user_id(self) -> int:
        """Lay maNguoiDung cua Admin, tao neu thieu."""
        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT maNguoiDung
                FROM NguoiDung
                WHERE tenDangNhap = ?
                """,
                ("Admin",),
            )
            row = cursor.fetchone()
            if row is not None:
                return int(row[0])

            cursor.execute(
                """
                INSERT INTO NguoiDung (tenDangNhap, ngayTao)
                VALUES (?, ?)
                """,
                ("Admin", now_iso()),
            )
            connection.commit()
            return int(cursor.lastrowid)
        finally:
            connection.close()

    def load_cai_dat(self) -> dict[str, Any]:
        """Doc cau hinh ung dung cua Admin tu bang CaiDat."""
        if self.current_user_id is None:
            raise RuntimeError("Chưa có mã người dùng.")

        connection = get_db_connection()
        try:
            self.ensure_caidat_theme_column(connection)
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    thoiGianCanhBao,
                    thoiGianChoCanhBao,
                    batAmThanh,
                    duongDanAmThanh,
                    nguonCamera,
                    duongDanModel,
                    duongDanScaler,
                    cheDoGiaoDien,
                    smoothingWindowFrames,
                    smoothingThreshold
                FROM CaiDat
                WHERE maNguoiDung = ?
                ORDER BY maCaiDat DESC
                LIMIT 1
                """,
                (self.current_user_id,),
            )
            row = cursor.fetchone()
            if row is None:
                return dict(self.config_data)

            return {
                "thoiGianCanhBao": row["thoiGianCanhBao"],
                "thoiGianChoCanhBao": row["thoiGianChoCanhBao"],
                "batAmThanh": row["batAmThanh"],
                "duongDanAmThanh": row["duongDanAmThanh"],
                "nguonCamera": row["nguonCamera"],
                "duongDanModel": row["duongDanModel"],
                "duongDanScaler": row["duongDanScaler"],
                "cheDoGiaoDien": row["cheDoGiaoDien"],
                "smoothingWindowFrames": row["smoothingWindowFrames"],
                "smoothingThreshold": row["smoothingThreshold"],
            }
        finally:
            connection.close()

    def ensure_caidat_theme_column(self, connection: sqlite3.Connection) -> None:
        """Them cac cot cau hinh moi vao database cu neu chua co."""
        rows = connection.execute("PRAGMA table_info(CaiDat)").fetchall()
        column_names = {str(row[1]) for row in rows}
        changed = False
        if "cheDoGiaoDien" not in column_names:
            connection.execute(
                "ALTER TABLE CaiDat ADD COLUMN cheDoGiaoDien TEXT NOT NULL DEFAULT 'light'"
            )
            changed = True
        if "smoothingWindowFrames" not in column_names:
            connection.execute(
                "ALTER TABLE CaiDat ADD COLUMN smoothingWindowFrames INTEGER NOT NULL DEFAULT 5"
            )
            changed = True
        if "smoothingThreshold" not in column_names:
            connection.execute(
                "ALTER TABLE CaiDat ADD COLUMN smoothingThreshold REAL NOT NULL DEFAULT 0.5"
            )
            changed = True
        if changed:
            connection.commit()

    def apply_config_to_gui(self) -> None:
        """Do cau hinh database len cac control GUI."""
        theme_mode = str(self.config_data.get("cheDoGiaoDien", "light")).lower()
        if theme_mode != self.current_theme_mode:
            self.set_theme_mode(theme_mode, rebuild=True)
            return

        self.source_entry.delete(0, "end")
        self.source_entry.insert(0, str(self.config_data.get("nguonCamera", "0")))

        self.warning_entry.delete(0, "end")
        self.warning_entry.insert(
            0,
            str(self.config_data.get("thoiGianCanhBao", 5)),
        )

        self.cooldown_entry.delete(0, "end")
        self.cooldown_entry.insert(
            0,
            str(self.config_data.get("thoiGianChoCanhBao", 15)),
        )

        self.smoothing_window_entry.delete(0, "end")
        self.smoothing_window_entry.insert(
            0,
            str(self.config_data.get("smoothingWindowFrames", 5)),
        )

        self.smoothing_threshold_entry.delete(0, "end")
        self.smoothing_threshold_entry.insert(
            0,
            str(self.config_data.get("smoothingThreshold", 0.5)),
        )

        if int(self.config_data.get("batAmThanh", 1)) == 1:
            self.sound_switch.select()
        else:
            self.sound_switch.deselect()

        if hasattr(self, "theme_segment"):
            self.theme_segment.set(self.current_theme_mode.title())

    def read_gui_settings(self) -> dict[str, Any]:
        """Doc va validate cau hinh nguoi dung nhap tren GUI."""
        source = self.source_entry.get().strip() or "0"

        try:
            warning_seconds = max(1, int(float(self.warning_entry.get().strip())))
        except ValueError as exc:
            raise ValueError("Thời gian cảnh báo phải là số.") from exc

        try:
            cooldown_seconds = max(1, int(float(self.cooldown_entry.get().strip())))
        except ValueError as exc:
            raise ValueError("Thời gian chờ cảnh báo phải là số.") from exc

        try:
            smoothing_window_frames = max(
                1,
                min(60, int(float(self.smoothing_window_entry.get().strip()))),
            )
        except ValueError as exc:
            raise ValueError("Số frame làm mượt phải là số.") from exc

        try:
            smoothing_threshold = float(self.smoothing_threshold_entry.get().strip())
        except ValueError as exc:
            raise ValueError("Ngưỡng sai sau làm mượt phải là số.") from exc
        if not 0.01 <= smoothing_threshold <= 0.99:
            raise ValueError("Ngưỡng sai sau làm mượt phải nằm trong [0.01, 0.99].")

        return {
            "nguonCamera": source,
            "thoiGianCanhBao": warning_seconds,
            "thoiGianChoCanhBao": cooldown_seconds,
            "batAmThanh": int(self.sound_switch.get()),
            "duongDanAmThanh": self.config_data.get(
                "duongDanAmThanh",
                "assets/sounds/alarm.wav",
            ),
            "duongDanModel": self.config_data.get(
                "duongDanModel",
                "models/ann_best.keras",
            ),
            "duongDanScaler": self.config_data.get(
                "duongDanScaler",
                "models/scaler.pkl",
            ),
            "cheDoGiaoDien": self.current_theme_mode,
            "smoothingWindowFrames": smoothing_window_frames,
            "smoothingThreshold": smoothing_threshold,
        }

    def save_cai_dat_from_gui(self) -> None:
        """Luu cau hinh tren GUI vao bang CaiDat."""
        if self.current_user_id is None:
            messagebox.showerror("Lỗi", "Chưa có người dùng Admin trong database.")
            return

        try:
            settings = self.read_gui_settings()
        except ValueError as exc:
            messagebox.showerror("Lỗi cài đặt", str(exc))
            return

        connection = None
        try:
            connection = get_db_connection()
            self.ensure_caidat_theme_column(connection)
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT maCaiDat
                FROM CaiDat
                WHERE maNguoiDung = ?
                ORDER BY maCaiDat DESC
                LIMIT 1
                """,
                (self.current_user_id,),
            )
            row = cursor.fetchone()

            if row is None:
                cursor.execute(
                    """
                    INSERT INTO CaiDat (
                        maNguoiDung,
                        thoiGianCanhBao,
                        thoiGianChoCanhBao,
                        batAmThanh,
                        duongDanAmThanh,
                        nguonCamera,
                        duongDanModel,
                        duongDanScaler,
                        cheDoGiaoDien,
                        smoothingWindowFrames,
                        smoothingThreshold,
                        ngayCapNhat
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        self.current_user_id,
                        settings["thoiGianCanhBao"],
                        settings["thoiGianChoCanhBao"],
                        settings["batAmThanh"],
                        settings["duongDanAmThanh"],
                        settings["nguonCamera"],
                        settings["duongDanModel"],
                        settings["duongDanScaler"],
                        settings["cheDoGiaoDien"],
                        settings["smoothingWindowFrames"],
                        settings["smoothingThreshold"],
                        now_iso(),
                    ),
                )
            else:
                cursor.execute(
                    """
                    UPDATE CaiDat
                    SET
                        thoiGianCanhBao = ?,
                        thoiGianChoCanhBao = ?,
                        batAmThanh = ?,
                        duongDanAmThanh = ?,
                        nguonCamera = ?,
                        duongDanModel = ?,
                        duongDanScaler = ?,
                        cheDoGiaoDien = ?,
                        smoothingWindowFrames = ?,
                        smoothingThreshold = ?,
                        ngayCapNhat = ?
                    WHERE maCaiDat = ?
                    """,
                    (
                        settings["thoiGianCanhBao"],
                        settings["thoiGianChoCanhBao"],
                        settings["batAmThanh"],
                        settings["duongDanAmThanh"],
                        settings["nguonCamera"],
                        settings["duongDanModel"],
                        settings["duongDanScaler"],
                        settings["cheDoGiaoDien"],
                        settings["smoothingWindowFrames"],
                        settings["smoothingThreshold"],
                        now_iso(),
                        row[0],
                    ),
                )

            connection.commit()
            self.config_data = settings
            self.apply_runtime_settings()
            messagebox.showinfo("Thành công", "Đã lưu cài đặt.")

        except Exception as exc:
            if connection is not None:
                connection.rollback()
            messagebox.showerror("Lỗi database", f"Không lưu được cài đặt: {exc}")
            print(f"ERROR: Khong luu duoc CaiDat: {exc}")

        finally:
            if connection is not None:
                connection.close()

    def start_phien_lam_viec(self, loai_nguon: str, gia_tri_nguon: str) -> int:
        """Tao mot dong phien lam viec moi va tra ve maPhien."""
        if self.current_user_id is None:
            raise RuntimeError("Chưa có người dùng Admin.")

        connection = get_db_connection()
        try:
            cursor = connection.cursor()
            started_at = now_iso()
            cursor.execute(
                """
                INSERT INTO PhienLamViec (
                    maNguoiDung,
                    thoiGianBatDau,
                    loaiNguon,
                    giaTriNguon,
                    ngayTao
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    self.current_user_id,
                    started_at,
                    loai_nguon,
                    gia_tri_nguon,
                    started_at,
                ),
            )
            connection.commit()
            return int(cursor.lastrowid)
        finally:
            connection.close()

    def end_phien_lam_viec(self) -> None:
        """Cap nhat thong tin tong ket khi ket thuc phien lam viec."""
        if self.current_session_id is None:
            return

        avg_confidence = (
            self.confidence_sum / self.confidence_count
            if self.confidence_count > 0
            else 0.0
        )
        ended_at = now_iso()
        session_seconds = self.get_session_seconds()

        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE PhienLamViec
                SET
                    thoiGianKetThuc = ?,
                    tongSoFrame = ?,
                    soFrameDung = ?,
                    soFrameSai = ?,
                    soFrameKhongCoNguoi = ?,
                    tongThoiGianDung = ?,
                    tongThoiGianSai = ?,
                    soLanCanhBao = ?,
                    doTinCayTrungBinh = ?,
                    ghiChu = ?
                WHERE maPhien = ?
                """,
                (
                    ended_at,
                    self.total_frames,
                    self.correct_frames,
                    self.incorrect_frames,
                    self.no_person_frames,
                    self.correct_seconds,
                    self.incorrect_seconds,
                    self.warning_count,
                    avg_confidence,
                    f"Tong thoi gian phien: {session_seconds:.1f}s",
                    self.current_session_id,
                ),
            )
            connection.commit()

        except Exception as exc:
            if connection is not None:
                connection.rollback()
            print(f"ERROR: Khong cap nhat duoc PhienLamViec: {exc}")

        finally:
            if connection is not None:
                connection.close()

        self.update_thong_ke_ngay(session_seconds)
        self.current_session_id = None

    def insert_nhat_ky_tu_the(
        self,
        trang_thai: str,
        nhan_du_doan: int | None,
        xac_suat_sai: float | None,
        do_tin_cay: float | None,
        da_canh_bao: int,
        loai_canh_bao: str,
        chi_so_frame: int,
        fps: float,
        ghi_chu: str,
    ) -> None:
        """Them mot dong nhat ky tu the vao bang NhatKyTuThe."""
        if self.is_rule_based_mode():
            return

        if self.current_session_id is None:
            return

        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO NhatKyTuThe (
                    maPhien,
                    thoiDiem,
                    trangThai,
                    nhanDuDoan,
                    xacSuatSai,
                    doTinCay,
                    daCanhBao,
                    loaiCanhBao,
                    chiSoFrame,
                    fps,
                    ghiChu
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.current_session_id,
                    now_iso(),
                    trang_thai,
                    nhan_du_doan,
                    xac_suat_sai,
                    do_tin_cay,
                    da_canh_bao,
                    loai_canh_bao,
                    chi_so_frame,
                    fps,
                    ghi_chu,
                ),
            )
            connection.commit()

        except Exception as exc:
            if connection is not None:
                connection.rollback()
            print(f"WARNING: Khong ghi duoc NhatKyTuThe: {exc}")

        finally:
            if connection is not None:
                connection.close()

    def update_thong_ke_ngay(self, session_seconds: float) -> None:
        """Cong don thong ke cua phien hien tai vao bang ThongKeNgay."""
        if self.is_rule_based_mode():
            return

        current_day = today_text()
        updated_at = now_iso()

        connection = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    tongSoPhien,
                    tongThoiGianLamViec,
                    tongThoiGianDung,
                    tongThoiGianSai,
                    tongSoCanhBao
                FROM ThongKeNgay
                WHERE ngay = ?
                """,
                (current_day,),
            )
            row = cursor.fetchone()

            if row is None:
                total_sessions = 1
                total_work = session_seconds
                total_correct = self.correct_seconds
                total_incorrect = self.incorrect_seconds
                total_warnings = self.warning_count
                correct_ratio = total_correct / total_work if total_work > 0 else 0.0
                incorrect_ratio = (
                    total_incorrect / total_work if total_work > 0 else 0.0
                )

                cursor.execute(
                    """
                    INSERT INTO ThongKeNgay (
                        ngay,
                        tongSoPhien,
                        tongThoiGianLamViec,
                        tongThoiGianDung,
                        tongThoiGianSai,
                        tongSoCanhBao,
                        tiLeDung,
                        tiLeSai,
                        ngayCapNhat
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        current_day,
                        total_sessions,
                        total_work,
                        total_correct,
                        total_incorrect,
                        total_warnings,
                        correct_ratio,
                        incorrect_ratio,
                        updated_at,
                    ),
                )
            else:
                total_sessions = int(row[0]) + 1
                total_work = float(row[1]) + session_seconds
                total_correct = float(row[2]) + self.correct_seconds
                total_incorrect = float(row[3]) + self.incorrect_seconds
                total_warnings = int(row[4]) + self.warning_count
                correct_ratio = total_correct / total_work if total_work > 0 else 0.0
                incorrect_ratio = (
                    total_incorrect / total_work if total_work > 0 else 0.0
                )

                cursor.execute(
                    """
                    UPDATE ThongKeNgay
                    SET
                        tongSoPhien = ?,
                        tongThoiGianLamViec = ?,
                        tongThoiGianDung = ?,
                        tongThoiGianSai = ?,
                        tongSoCanhBao = ?,
                        tiLeDung = ?,
                        tiLeSai = ?,
                        ngayCapNhat = ?
                    WHERE ngay = ?
                    """,
                    (
                        total_sessions,
                        total_work,
                        total_correct,
                        total_incorrect,
                        total_warnings,
                        correct_ratio,
                        incorrect_ratio,
                        updated_at,
                        current_day,
                    ),
                )

            connection.commit()

        except Exception as exc:
            if connection is not None:
                connection.rollback()
            print(f"ERROR: Khong cap nhat duoc ThongKeNgay: {exc}")

        finally:
            if connection is not None:
                connection.close()

    # =========================
    # Model, video va inference
    # =========================
    def apply_runtime_settings(self) -> None:
        """Cap nhat cac bien runtime tu config hien tai."""
        self.warning_seconds = float(self.config_data.get("thoiGianCanhBao", 5))
        self.warning_cooldown_seconds = float(
            self.config_data.get("thoiGianChoCanhBao", 15)
        )
        self.smoothing_window_frames = int(self.config_data.get("smoothingWindowFrames", 5))
        self.smoothing_threshold = float(self.config_data.get("smoothingThreshold", 0.5))
        if self.probability_window.maxlen != self.smoothing_window_frames:
            self.probability_window = deque(maxlen=self.smoothing_window_frames)
        self.alarm_enabled = int(self.config_data.get("batAmThanh", 1)) == 1

    def is_ann_mode(self) -> bool:
        """Kiem tra app dang chay mode ANN."""
        return self.prediction_mode == "ANN"

    def is_rule_based_mode(self) -> bool:
        """Kiem tra app dang chay mode Rule-based Baseline."""
        return self.prediction_mode == "Rule-based Baseline"

    def load_ai_components(self, source_type: str = "webcam") -> None:
        """Load thanh phan can thiet theo mode hien tai."""
        if self.is_ann_mode():
            model_path = project_path_from_text(
                str(self.config_data.get("duongDanModel", "")),
                MODEL_PATH,
            )
            scaler_path = project_path_from_text(
                str(self.config_data.get("duongDanScaler", "")),
                SCALER_PATH,
            )

            if not model_path.exists():
                if MODEL_PATH.exists():
                    print(
                        f"WARNING: Khong thay model cau hinh, dung fallback: {MODEL_PATH}"
                    )
                    model_path = MODEL_PATH
                else:
                    raise FileNotFoundError(f"Khong tim thay model: {model_path}")

            if not scaler_path.exists():
                if SCALER_PATH.exists():
                    print(
                        f"WARNING: Khong thay scaler cau hinh, dung fallback: {SCALER_PATH}"
                    )
                    scaler_path = SCALER_PATH
                else:
                    raise FileNotFoundError(f"Khong tim thay scaler: {scaler_path}")

            if self.model is None:
                print(f"Dang load model ANN: {model_path}")
                self.model = load_model(model_path)

            if self.scaler is None:
                print(f"Dang load scaler: {scaler_path}")
                self.scaler = joblib.load(scaler_path)
        else:
            print("Baseline mode: chi load MediaPipe Pose, khong load ANN/scaler.")

        if self.pose is None:
            pose_model_complexity = 0 if source_type == "ip_camera" else 1
            self.pose = mp_pose.Pose(
                static_image_mode=False,
                model_complexity=pose_model_complexity,
                enable_segmentation=False,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5,
            )

    def reset_session_counters(self) -> None:
        """Reset cac bien dem cho phien camera moi."""
        self.frame_index = 0
        self.total_frames = 0
        self.correct_frames = 0
        self.incorrect_frames = 0
        self.no_person_frames = 0
        self.warning_count = 0
        self.confidence_sum = 0.0
        self.confidence_count = 0
        self.incorrect_start_time = None
        self.incorrect_confirmed = False
        self.confirmed_incorrect_start_time = None
        self.last_alarm_time = 0.0
        self.alarm_is_playing = False
        self.alarm_stop_requested = False
        self.alarm_thread = None
        self.last_logged_status = None
        self.current_status = "DANG_KIEM_TRA"
        self.fps = 0.0
        self.previous_frame_time = None
        self.session_start_time = datetime.now()
        self.correct_seconds = 0.0
        self.incorrect_seconds = 0.0
        self.current_prob_incorrect = None
        self.current_confidence = None
        self.probability_window.clear()
        self.last_frame_elapsed = 0.0
        self.reset_capture_state()

    def reset_capture_state(self) -> None:
        """Xoa frame cu cua luong doc camera live."""
        self.latest_capture_frame = None
        self.latest_capture_time = 0.0
        self.last_consumed_capture_time = 0.0
        self.capture_read_failures = 0
        self.capture_error_message = None

    def is_live_source(self) -> bool:
        """Nguon live can doc bang thread rieng de tranh don buffer."""
        return self.current_source_type in {"webcam", "ip_camera"}

    def configure_capture(self, cap: cv2.VideoCapture, source_type: str) -> None:
        """Toi uu VideoCapture cho realtime thay vi uu tien buffer/phan giai cao."""
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if source_type in {"webcam", "ip_camera"}:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, LIVE_CAPTURE_WIDTH)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, LIVE_CAPTURE_HEIGHT)
            cap.set(cv2.CAP_PROP_FPS, 30)

            if source_type == "webcam":
                cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

    def start_capture_thread(self) -> None:
        """Doc lien tuc camera live va chi giu frame moi nhat."""
        if self.cap is None or self.capture_thread is not None:
            return

        self.capture_stop_event.clear()
        self.reset_capture_state()
        self.capture_thread = threading.Thread(
            target=self.capture_loop,
            name="LiveCameraCapture",
            daemon=True,
        )
        self.capture_thread.start()

    def capture_loop(self) -> None:
        """Vong doc frame nen, tranh de OpenCV/IP camera tich buffer cu."""
        while not self.capture_stop_event.is_set():
            cap = self.cap
            if cap is None:
                break

            success, frame = cap.read()
            if success and frame is not None:
                with self.frame_lock:
                    self.latest_capture_frame = frame
                    self.latest_capture_time = time.time()
                    self.capture_read_failures = 0
                    self.capture_error_message = None
                continue

            with self.frame_lock:
                self.capture_read_failures += 1
                if self.capture_read_failures >= CAPTURE_FAIL_LIMIT:
                    self.capture_error_message = "Khong doc duoc frame tu camera live."
                    break

            time.sleep(CAPTURE_READ_RETRY_DELAY)

    def stop_capture_thread(self) -> None:
        """Dung thread doc camera live truoc khi release VideoCapture."""
        if self.capture_thread is None:
            return

        self.capture_stop_event.set()
        self.capture_thread.join(timeout=1.0)
        self.capture_thread = None

    def get_latest_live_frame(self) -> np.ndarray | None:
        """Lay frame moi nhat tu thread doc camera, bo qua frame da xu ly."""
        with self.frame_lock:
            if self.latest_capture_frame is None:
                return None

            if self.latest_capture_time <= self.last_consumed_capture_time:
                return None

            frame = self.latest_capture_frame.copy()
            self.last_consumed_capture_time = self.latest_capture_time
            return frame

    def schedule_next_frame(self, delay_ms: int = UPDATE_DELAY_MS) -> None:
        """Lap lich update frame tiep theo neu camera van dang chay."""
        if self.is_running:
            self.update_after_id = self.after(delay_ms, self.update_frame)

    def start_camera(self) -> None:
        """Bat dau doc camera/video va chay pipeline realtime."""
        if self.is_running:
            return

        try:
            self.prediction_mode = self.mode_combobox.get()
            self.config_data = self.read_gui_settings()
            self.apply_runtime_settings()

            if self.is_ann_mode():
                self.save_cai_dat_silent()
                self.config_data = self.load_cai_dat()
                self.apply_runtime_settings()
            else:
                self.current_session_id = None
                print("Dang chay che do Rule-based Baseline - khong luu CSDL.")

            source_text = str(self.config_data.get("nguonCamera", "0")).strip() or "0"
            source_value, source_type = resolve_source(source_text)
            self.current_source = source_value
            self.current_source_type = source_type
            self.load_ai_components(source_type)

            cap = cv2.VideoCapture(source_value)

            if not cap.isOpened():
                raise RuntimeError(f"Không mở được nguồn camera/video: {source_text}")

            self.configure_capture(cap, source_type)

            self.cap = cap
            self.reset_session_counters()
            if self.is_ann_mode():
                self.current_session_id = self.start_phien_lam_viec(
                    source_type,
                    source_text,
                )
            else:
                self.current_session_id = None

            self.is_running = True
            if self.is_live_source():
                self.start_capture_thread()

            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            self.save_button.configure(state="disabled")
            self.mode_combobox.configure(state="disabled")
            self.clear_video_label("")
            self.update_status_ui("DANG_KIEM_TRA", None)
            self.update_counter_labels()
            self.update_baseline_info_panel("DANG_KIEM_TRA", None, [], False)
            self.update_after_id = self.after(0, self.update_frame)

        except Exception as exc:
            self.is_running = False
            self.cancel_pending_frame_update()
            self.release_video_resources()
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.save_button.configure(state="normal")
            self.mode_combobox.configure(state="readonly")
            self.clear_video_label("Chưa bật camera")
            messagebox.showerror("Lỗi khởi động", str(exc))
            print(f"ERROR: Khong khoi dong duoc app: {exc}")

    def save_cai_dat_silent(self) -> None:
        """Luu cau hinh truoc khi bat dau, khong hien messagebox thanh cong."""
        if self.current_user_id is None:
            raise RuntimeError("Chưa có người dùng Admin trong database.")

        settings = dict(self.config_data)
        connection = get_db_connection()
        try:
            self.ensure_caidat_theme_column(connection)
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT maCaiDat
                FROM CaiDat
                WHERE maNguoiDung = ?
                ORDER BY maCaiDat DESC
                LIMIT 1
                """,
                (self.current_user_id,),
            )
            row = cursor.fetchone()

            if row is None:
                cursor.execute(
                    """
                    INSERT INTO CaiDat (
                        maNguoiDung,
                        thoiGianCanhBao,
                        thoiGianChoCanhBao,
                        batAmThanh,
                        duongDanAmThanh,
                        nguonCamera,
                        duongDanModel,
                        duongDanScaler,
                        cheDoGiaoDien,
                        smoothingWindowFrames,
                        smoothingThreshold,
                        ngayCapNhat
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        self.current_user_id,
                        settings["thoiGianCanhBao"],
                        settings["thoiGianChoCanhBao"],
                        settings["batAmThanh"],
                        settings["duongDanAmThanh"],
                        settings["nguonCamera"],
                        settings["duongDanModel"],
                        settings["duongDanScaler"],
                        settings.get("cheDoGiaoDien", self.current_theme_mode),
                        settings.get("smoothingWindowFrames", 5),
                        settings.get("smoothingThreshold", 0.5),
                        now_iso(),
                    ),
                )
            else:
                cursor.execute(
                    """
                    UPDATE CaiDat
                    SET
                        thoiGianCanhBao = ?,
                        thoiGianChoCanhBao = ?,
                        batAmThanh = ?,
                        duongDanAmThanh = ?,
                        nguonCamera = ?,
                        duongDanModel = ?,
                        duongDanScaler = ?,
                        cheDoGiaoDien = ?,
                        smoothingWindowFrames = ?,
                        smoothingThreshold = ?,
                        ngayCapNhat = ?
                    WHERE maCaiDat = ?
                    """,
                    (
                        settings["thoiGianCanhBao"],
                        settings["thoiGianChoCanhBao"],
                        settings["batAmThanh"],
                        settings["duongDanAmThanh"],
                        settings["nguonCamera"],
                        settings["duongDanModel"],
                        settings["duongDanScaler"],
                        settings.get("cheDoGiaoDien", self.current_theme_mode),
                        settings.get("smoothingWindowFrames", 5),
                        settings.get("smoothingThreshold", 0.5),
                        now_iso(),
                        row[0],
                    ),
                )

            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def update_frame(self) -> None:
        """Doc frame, predict tu the, hien thi video va lap lich frame tiep."""
        self.update_after_id = None

        if not self.is_running or self.cap is None:
            return

        if self.is_live_source():
            frame = self.get_latest_live_frame()
            if frame is None:
                if self.capture_error_message:
                    print(f"WARNING: {self.capture_error_message}")
                    self.stop_camera()
                    return

                self.schedule_next_frame(UPDATE_DELAY_MS)
                return
        else:
            success, frame = self.cap.read()
            if not success or frame is None:
                if self.current_source_type == "video_file" and self.cap is not None:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    success, frame = self.cap.read()

                if not success or frame is None:
                    print("WARNING: Khong doc duoc frame, dung camera.")
                    self.stop_camera()
                    return

        if frame is None:
            self.schedule_next_frame(UPDATE_DELAY_MS)
            return

        # IP/phone camera co the day frame moi rat nhanh; bo frame cu giup UI
        # luon xu ly anh gan thoi gian thuc nhat thay vi chay duoi buffer.
        if self.is_live_source():
            extra_frame = self.get_latest_live_frame()
            if extra_frame is not None:
                frame = extra_frame

        current_time = time.time()
        if self.previous_frame_time is None:
            elapsed = 0.0
        else:
            elapsed = max(0.0, current_time - self.previous_frame_time)
            instant_fps = 1.0 / elapsed if elapsed > 0 else 0.0
            self.fps = (
                0.85 * self.fps + 0.15 * instant_fps
                if self.fps > 0
                else instant_fps
            )
        self.previous_frame_time = current_time
        self.last_frame_elapsed = elapsed

        self.frame_index += 1
        self.total_frames += 1

        frame = self.prepare_frame(frame)
        (
            status,
            predicted_label,
            prob_incorrect,
            confidence,
            results,
            baseline_features,
            baseline_warnings,
        ) = self.predict_frame(frame)

        should_alarm, incorrect_confirmed = self.handle_warning_logic(
            status,
            predicted_label,
            prob_incorrect,
            confidence,
            current_time,
        )
        self.update_runtime_counters(
            status=status,
            confidence=confidence,
            elapsed=elapsed,
            incorrect_confirmed=incorrect_confirmed,
        )
        self.handle_status_logging(
            status,
            predicted_label,
            prob_incorrect,
            confidence,
            should_alarm,
            incorrect_confirmed,
        )

        self.draw_frame_overlay(
            frame,
            status,
            prob_incorrect,
            confidence,
            results,
            incorrect_confirmed,
            baseline_features,
            baseline_warnings,
        )
        self.show_frame(frame)
        self.update_baseline_info_panel(
            status,
            baseline_features,
            baseline_warnings,
            incorrect_confirmed,
        )
        self.update_status_ui(status, confidence, incorrect_confirmed)
        self.update_counter_labels()

        self.schedule_next_frame(UPDATE_DELAY_MS)

    def prepare_frame(self, frame: np.ndarray) -> np.ndarray:
        """Chuan hoa frame ve kich thuoc hien thi on dinh."""
        frame = cv2.resize(frame, (VIDEO_WIDTH, VIDEO_HEIGHT), interpolation=cv2.INTER_AREA)
        if self.current_source_type == "webcam":
            frame = cv2.flip(frame, 1)
        return frame

    def predict_frame(
        self,
        frame: np.ndarray,
    ) -> tuple[
        str,
        int | None,
        float | None,
        float | None,
        Any,
        dict[str, Any] | None,
        list[str],
    ]:
        """Dispatcher du doan theo mode nguoi dung da chon."""
        if self.is_rule_based_mode():
            return self.predict_frame_rule_based(frame)
        return self.predict_frame_ann(frame)

    def predict_frame_ann(
        self,
        frame: np.ndarray,
    ) -> tuple[
        str,
        int | None,
        float | None,
        float | None,
        Any,
        dict[str, Any] | None,
        list[str],
    ]:
        """Chay MediaPipe Pose va ANN de lay trang thai tu the."""
        if self.pose is None or self.model is None or self.scaler is None:
            return "KHONG_PHAT_HIEN_NGUOI", None, None, None, None, None, []

        inference_frame = cv2.resize(
            frame,
            (INFERENCE_WIDTH, INFERENCE_HEIGHT),
            interpolation=cv2.INTER_AREA,
        )
        rgb_frame = cv2.cvtColor(inference_frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        results = self.pose.process(rgb_frame)
        rgb_frame.flags.writeable = True

        if not results.pose_landmarks:
            self.current_prob_incorrect = None
            self.current_confidence = None
            self.probability_window.clear()
            return "KHONG_PHAT_HIEN_NGUOI", None, None, None, results, None, []

        landmarks = results.pose_landmarks.landmark
        feature_vector: list[float] = []
        for landmark in landmarks[:NUM_POSE_LANDMARKS]:
            feature_vector.extend(
                [
                    float(landmark.x),
                    float(landmark.y),
                    float(landmark.z),
                ]
            )

        if len(feature_vector) != NUM_FEATURES:
            self.current_prob_incorrect = None
            self.current_confidence = None
            self.probability_window.clear()
            return "KHONG_PHAT_HIEN_NGUOI", None, None, None, results, None, []

        features = np.array([feature_vector], dtype=np.float32)
        features_scaled = self.scaler.transform(features)
        prediction = self.model(features_scaled, training=False)
        raw_prob_incorrect = float(np.asarray(prediction).reshape(-1)[0])
        self.probability_window.append(raw_prob_incorrect)
        prob_incorrect = float(np.mean(self.probability_window))

        # Label 1 = sai tu the, nen sigmoid output la P(sai).
        if prob_incorrect >= self.smoothing_threshold:
            status = "SAI_TU_THE"
            predicted_label = 1
            confidence = prob_incorrect
        else:
            status = "DUNG_TU_THE"
            predicted_label = 0
            confidence = 1.0 - prob_incorrect

        self.current_prob_incorrect = prob_incorrect
        self.current_confidence = confidence
        return status, predicted_label, prob_incorrect, confidence, results, None, []

    def predict_frame_rule_based(
        self,
        frame: np.ndarray,
    ) -> tuple[
        str,
        int | None,
        float | None,
        float | None,
        Any,
        dict[str, Any],
        list[str],
    ]:
        """
        Chay MediaPipe Pose va rule-based baseline de lay trang thai tu the.
        Khong dung ANN, khong dung scaler.
        """
        default_features = create_default_features(False)
        if self.pose is None:
            self.current_prob_incorrect = None
            self.current_confidence = None
            return (
                "KHONG_PHAT_HIEN_NGUOI",
                None,
                None,
                None,
                None,
                default_features,
                [],
            )

        inference_frame = cv2.resize(
            frame,
            (INFERENCE_WIDTH, INFERENCE_HEIGHT),
            interpolation=cv2.INTER_AREA,
        )
        rgb_frame = cv2.cvtColor(inference_frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        results = self.pose.process(rgb_frame)
        rgb_frame.flags.writeable = True

        if not results.pose_landmarks:
            self.current_prob_incorrect = None
            self.current_confidence = None
            return (
                "KHONG_PHAT_HIEN_NGUOI",
                None,
                None,
                None,
                results,
                default_features,
                [],
            )

        features = extract_posture_features(results.pose_landmarks.landmark)
        baseline_status, warnings = classify_posture_rule_based(features)

        if baseline_status == "CORRECT":
            status = "DUNG_TU_THE"
            predicted_label = 0
            prob_incorrect = 0.0
            confidence = float(features.get("visibility", 1.0))
        elif baseline_status == "INCORRECT":
            status = "SAI_TU_THE"
            predicted_label = 1
            prob_incorrect = 1.0
            confidence = float(features.get("visibility", 1.0))
        else:
            status = "KHONG_PHAT_HIEN_NGUOI"
            predicted_label = None
            prob_incorrect = None
            confidence = None

        self.current_prob_incorrect = prob_incorrect
        self.current_confidence = confidence
        return (
            status,
            predicted_label,
            prob_incorrect,
            confidence,
            results,
            features,
            warnings,
        )

    def update_runtime_counters(
        self,
        status: str,
        confidence: float | None,
        elapsed: float,
        incorrect_confirmed: bool = False,
    ) -> None:
        """Cap nhat bo dem frame, thoi gian va do tin cay."""
        self.current_status = status

        if status == "DUNG_TU_THE":
            self.correct_frames += 1
            self.correct_seconds += elapsed
        elif status == "SAI_TU_THE":
            # Sai duoi nguong canh bao chi la giai doan kiem tra,
            # chua tinh vao thong ke sai tu the.
            if incorrect_confirmed:
                self.incorrect_frames += 1
                self.incorrect_seconds += elapsed
        else:
            self.no_person_frames += 1

        if confidence is not None:
            self.confidence_sum += confidence
            self.confidence_count += 1

    def handle_warning_logic(
        self,
        status: str,
        predicted_label: int | None,
        prob_incorrect: float | None,
        confidence: float | None,
        current_time: float,
    ) -> tuple[bool, bool]:
        """Kiem tra nguong sai tu the va phat am thanh neu can."""
        if status != "SAI_TU_THE":
            self.incorrect_start_time = None
            self.incorrect_confirmed = False
            self.confirmed_incorrect_start_time = None
            self.stop_alarm_sound()
            return False, False

        if self.incorrect_start_time is None:
            self.incorrect_start_time = current_time

        incorrect_duration = current_time - self.incorrect_start_time
        incorrect_confirmed = incorrect_duration >= self.warning_seconds
        self.incorrect_confirmed = incorrect_confirmed

        if not incorrect_confirmed:
            self.confirmed_incorrect_start_time = None
            return False, False

        if self.confirmed_incorrect_start_time is None:
            self.confirmed_incorrect_start_time = current_time

        enough_cooldown = (
            self.last_alarm_time <= 0
            or current_time - self.last_alarm_time >= self.warning_cooldown_seconds
        )

        if enough_cooldown:
            if self.is_rule_based_mode():
                # Baseline chi hien thi canh bao tam thoi de so sanh rule,
                # khong phat am thanh va khong ghi bat ky log database nao.
                self.last_alarm_time = current_time
                self.warning_count += 1
                return True, True

            # Neu nguoi dung van sai qua cooldown, cho phep phat lai canh bao.
            # Tren Windows, PlaySound moi se thay the am thanh async cu, khong chong lop.
            if self.alarm_is_playing and os.name == "nt":
                self.alarm_is_playing = False

            self.last_alarm_time = current_time
            alarm_started = True

            if self.alarm_enabled:
                alarm_started = self.play_alarm_async()

            if not alarm_started:
                return False, True

            self.warning_count += 1

            self.insert_nhat_ky_tu_the(
                trang_thai="SAI_TU_THE",
                nhan_du_doan=predicted_label,
                xac_suat_sai=prob_incorrect,
                do_tin_cay=confidence,
                da_canh_bao=1,
                loai_canh_bao="ann_incorrect",
                chi_so_frame=self.frame_index,
                fps=self.fps,
                ghi_chu=(
                    "Sai tu the da xac nhan sau khi vuot nguong thoi gian canh bao"
                ),
            )
            return True, True

        return False, True

    def handle_status_logging(
        self,
        status: str,
        predicted_label: int | None,
        prob_incorrect: float | None,
        confidence: float | None,
        warning_logged: bool,
        incorrect_confirmed: bool = False,
    ) -> None:
        """Ghi log khi trang thai thay doi, tranh ghi moi frame."""
        if self.is_rule_based_mode():
            return

        if status == "SAI_TU_THE" and not incorrect_confirmed:
            # Sai duoi nguong canh bao chi la sai tam thoi, khong ghi log de
            # tranh lam nhieu du lieu thong ke va nhat ky.
            return

        if status == "SAI_TU_THE" and warning_logged:
            self.last_logged_status = "SAI_TU_THE"
            return

        if status == self.last_logged_status:
            return

        self.last_logged_status = status
        warning_type = "no_person" if status == "KHONG_PHAT_HIEN_NGUOI" else "status_changed"
        note = (
            "Khong phat hien nguoi"
            if status == "KHONG_PHAT_HIEN_NGUOI"
            else "Trang thai tu the thay doi"
        )

        self.insert_nhat_ky_tu_the(
            trang_thai=status,
            nhan_du_doan=predicted_label,
            xac_suat_sai=prob_incorrect,
            do_tin_cay=confidence,
            da_canh_bao=0,
            loai_canh_bao=warning_type,
            chi_so_frame=self.frame_index,
            fps=self.fps,
            ghi_chu=note,
        )

        if warning_logged:
            # Canh bao da co log rieng voi daCanhBao = 1.
            return

    def draw_frame_overlay(
        self,
        frame: np.ndarray,
        status: str,
        prob_incorrect: float | None,
        confidence: float | None,
        results: Any,
        incorrect_confirmed: bool = False,
        baseline_features: dict[str, Any] | None = None,
        baseline_warnings: list[str] | None = None,
    ) -> None:
        """Ve skeleton, banner trang thai, P(sai) va FPS len frame."""
        if results is not None and results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
            )

        display_status = (
            "DANG_KIEM_TRA"
            if status == "SAI_TU_THE" and not incorrect_confirmed
            else status
        )

        if display_status == "DUNG_TU_THE":
            color = (80, 220, 80)
        elif display_status == "SAI_TU_THE":
            color = (40, 40, 255)
        elif display_status == "DANG_KIEM_TRA":
            color = (0, 190, 255)
        else:
            color = (180, 180, 180)

        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (VIDEO_WIDTH, 82), (25, 25, 25), -1)
        cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)

        draw_text(
            frame,
            STATUS_TEXT.get(display_status, display_status),
            (18, 34),
            color,
            0.85,
            2,
        )

        if self.is_rule_based_mode():
            draw_text(frame, "CHẾ ĐỘ: RULE-BASED", (18, 62), (245, 245, 245), 0.55, 1)
            draw_text(frame, f"FPS: {self.fps:.1f}", (240, 62), (245, 245, 245), 0.55, 1)
            return

        prob_text = "--" if prob_incorrect is None else f"{prob_incorrect:.3f}"
        conf_text = "--" if confidence is None else f"{confidence * 100:.1f}%"
        draw_text(frame, f"P(sai): {prob_text}", (18, 62), (245, 245, 245), 0.55, 1)
        draw_text(frame, f"Độ tin cậy: {conf_text}", (175, 62), (245, 245, 245), 0.55, 1)
        draw_text(frame, f"FPS: {self.fps:.1f}", (390, 62), (245, 245, 245), 0.55, 1)

    def show_frame(self, frame: np.ndarray) -> None:
        """Hien thi frame BGR len CTkLabel."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb_frame)
        self.video_image = ImageTk.PhotoImage(image=image)
        self.video_label.configure(image=self.video_image, text="")

    def clear_video_label(self, text: str = "Chưa bật camera") -> None:
        """
        Xoa anh hien tai khoi label mot cach an toan.

        Loi image "pyimage..." doesn't exist thuong xay ra khi widget con giu
        ten anh Tk cu nhung object PhotoImage da bi giai phong. Dat image=""
        truoc khi xoa reference giup lan mo camera tiep theo khong bi loi nay.
        """
        self.video_label.configure(image=None, text=text)
        inner_label = getattr(self.video_label, "_label", None)
        if inner_label is not None:
            inner_label.configure(image="")
        self.video_image = None

    def cancel_pending_frame_update(self) -> None:
        """Huy callback update_frame dang cho neu nguoi dung dung/doi nguon."""
        if self.update_after_id is None:
            return

        try:
            self.after_cancel(self.update_after_id)
        except Exception as exc:
            print(f"WARNING: Khong huy duoc callback frame cu: {exc}")
        finally:
            self.update_after_id = None

    def update_status_ui(
        self,
        status: str,
        confidence: float | None,
        incorrect_confirmed: bool = False,
    ) -> None:
        """Cap nhat label trang thai, do tin cay va timer sai tu the."""
        display_status = (
            "DANG_KIEM_TRA"
            if status == "SAI_TU_THE" and not incorrect_confirmed
            else status
        )

        self.status_label.configure(
            text=STATUS_TEXT.get(display_status, display_status),
            text_color=STATUS_COLORS.get(
                display_status,
                STATUS_COLORS["DANG_KIEM_TRA"],
            ),
        )

        if confidence is None:
            self.confidence_label.configure(text="Độ tin cậy: --")
        else:
            self.confidence_label.configure(text=f"Độ tin cậy: {confidence * 100:.2f}%")

        if status == "SAI_TU_THE" and self.incorrect_start_time is not None:
            wrong_duration = max(0.0, time.time() - self.incorrect_start_time)
        else:
            wrong_duration = 0.0

        if status == "SAI_TU_THE" and incorrect_confirmed:
            timer_text = f"Đã cảnh báo: {wrong_duration:.1f}s"
        else:
            timer_text = (
                f"Thời gian sai: {wrong_duration:.1f}s / "
                f"{self.warning_seconds:.1f}s"
            )

        self.incorrect_time_label.configure(text=timer_text)

    def update_counter_labels(self) -> None:
        """Cap nhat thong tin nhanh ben phai."""
        values = {
            "total": str(self.total_frames),
            "correct": str(self.correct_frames),
            "incorrect": str(self.incorrect_frames),
            "no_person": str(self.no_person_frames),
            "warnings": str(self.warning_count),
            "fps": f"{self.fps:.1f}",
        }
        for key, value in values.items():
            label = self.metric_labels.get(key)
            if label is not None:
                label.configure(text=value)

    def update_baseline_info_panel(
        self,
        status: str,
        features: dict[str, Any] | None,
        warnings: list[str],
        incorrect_confirmed: bool,
    ) -> None:
        """Cap nhat panel dac trung baseline nam ngoai khung camera."""
        if not self.is_rule_based_mode():
            self.baseline_info_frame.grid_remove()
            return

        self.baseline_info_frame.grid()
        display_status = (
            "DANG_KIEM_TRA"
            if status == "SAI_TU_THE" and not incorrect_confirmed
            else status
        )
        status_text = STATUS_TEXT.get(display_status, display_status)

        if not features or not bool(features.get("valid", False)):
            self.baseline_info_label.configure(
                text=(
                    "Chế độ: Rule-based Baseline\n"
                    f"Trạng thái: {status_text}\n"
                    "Không phát hiện người / độ tin cậy thấp\n"
                    f"Số lần cảnh báo baseline: {self.warning_count} (không lưu CSDL)\n"
                    f"FPS: {self.fps:.1f}"
                )
            )
            return

        def fmt_float(key: str) -> str:
            value = features.get(key)
            if isinstance(value, (int, float)):
                return f"{float(value):.3f}"
            return "--"

        warning_lines = (
            "\n".join(f"- {warning}" for warning in warnings)
            if warnings
            else "- Không có"
        )
        text = (
            "Chế độ: Rule-based Baseline\n"
            f"Trạng thái: {status_text}\n"
            "Cảnh báo:\n"
            f"{warning_lines}\n"
            "Đặc trưng:\n"
            f"độ lệch vai y: {fmt_float('shoulder_y_diff')}\n"
            f"góc nghiêng vai: {fmt_float('shoulder_tilt_angle')}\n"
            f"góc nghiêng thân: {fmt_float('torso_lean_angle')}\n"
            f"độ lệch đầu x: {fmt_float('head_offset_x')}\n"
            f"mũi so với vai y: {fmt_float('nose_to_shoulder_y')}\n"
            f"khoảng cách mũi-vai tỉ lệ: {fmt_float('nose_shoulder_clearance_ratio')}\n"
            f"rụt cổ sâu: {bool(features.get('neck_compression_detected', False))}\n"
            f"độ tin cậy landmark: {fmt_float('visibility')}\n"
            f"tay trái gần miệng tỉ lệ: {fmt_float('left_hand_mouth_ratio')}\n"
            f"tay phải gần miệng tỉ lệ: {fmt_float('right_hand_mouth_ratio')}\n"
            f"phát hiện chống cằm: {bool(features.get('chin_rest_detected', False))}\n"
            f"Số lần cảnh báo baseline: {self.warning_count} (không lưu CSDL)\n"
            f"FPS: {self.fps:.1f}"
        )
        self.baseline_info_label.configure(text=text)

    # =========================
    # Am thanh va thong ke
    # =========================
    def get_alarm_path(self) -> Path:
        """Lay duong dan file am thanh, fallback ve ALARM_PATH neu can."""
        alarm_text = str(self.config_data.get("duongDanAmThanh", "")).strip()
        alarm_path = project_path_from_text(alarm_text, ALARM_PATH)

        if not alarm_path.exists():
            alarm_path = ALARM_PATH

        return alarm_path

    def stop_alarm_sound(self) -> None:
        """
        Dung am thanh canh bao neu dang phat.

        Khi nguoi dung da sua lai tu the dung hoac khong con sai tu the,
        am thanh phai dung ngay. Tren non-Windows, playsound khong ho tro
        dung giua chung nen chi cap nhat co trang thai de tranh phat tiep.
        """
        if not self.alarm_is_playing and self.alarm_thread is None:
            return

        self.alarm_stop_requested = True

        try:
            if os.name == "nt":
                import winsound

                winsound.PlaySound(None, winsound.SND_PURGE)
        except Exception as exc:
            print(f"WARNING: Khong dung duoc am thanh canh bao: {exc}")
        finally:
            self.alarm_is_playing = False
            self.alarm_thread = None

    def play_alarm_async(self) -> bool:
        """Phat am thanh canh bao bang thread rieng de khong do GUI."""
        if self.alarm_is_playing:
            return False

        alarm_path = self.get_alarm_path()
        if not alarm_path.exists():
            print(f"WARNING: Khong tim thay file am thanh: {alarm_path}")
            return False

        self.alarm_stop_requested = False
        self.alarm_is_playing = True
        self.alarm_thread = threading.Thread(
            target=self.play_alarm_worker,
            args=(alarm_path,),
            daemon=True,
        )
        self.alarm_thread.start()
        return True

    def play_alarm_worker(self, alarm_path: Path) -> None:
        """Worker phat file wav tren Windows, fallback sang playsound."""
        try:
            if os.name == "nt":
                import winsound

                winsound.PlaySound(
                    str(alarm_path),
                    winsound.SND_FILENAME | winsound.SND_ASYNC,
                )
            else:
                from playsound import playsound

                playsound(str(alarm_path))
        except Exception as exc:
            print(f"WARNING: Khong phat duoc am thanh canh bao: {exc}")
            self.alarm_is_playing = False
            self.alarm_thread = None
        finally:
            # Voi winsound SND_ASYNC, lenh PlaySound tra ve ngay nhung am thanh
            # van co the dang phat nen khong reset alarm_is_playing tai day.
            # stop_alarm_sound se reset khi nguoi dung sua tu the hoac dung app.
            if os.name != "nt" and self.alarm_stop_requested:
                self.alarm_is_playing = False
                self.alarm_thread = None

    def show_statistics(self) -> None:
        """Mo cua so dashboard thong ke light mode."""
        try:
            dashboard_data = get_dashboard_data(DATABASE_PATH, today_text())
        except Exception as exc:
            messagebox.showerror("Lỗi database", f"Không đọc được thống kê: {exc}")
            return

        stats_window = ctk.CTkToplevel(self)
        stats_window.title("Dashboard thống kê tư thế")
        stats_window.geometry("1120x760")
        stats_window.minsize(980, 680)
        stats_window.configure(fg_color=THEME["app_bg"])
        stats_window.transient(self)
        stats_window.grid_columnconfigure(0, weight=1)
        stats_window.grid_rowconfigure(0, weight=1)

        main_frame = ctk.CTkScrollableFrame(
            stats_window,
            fg_color=THEME["app_bg"],
            corner_radius=0,
        )
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.render_statistics_dashboard(main_frame, dashboard_data, stats_window)

    def render_statistics_dashboard(
        self,
        main_frame: Any,
        dashboard_data: dict[str, Any],
        stats_window: Any,
    ) -> None:
        """Render dashboard statistics for the selected date."""
        for child in main_frame.winfo_children():
            child.destroy()

        for column_index in range(2):
            main_frame.grid_columnconfigure(column_index, weight=1, uniform="stats")

        selected_date = str(dashboard_data.get("date") or today_text())
        available_dates = dashboard_data.get("available_dates") or [selected_date]
        stats = dashboard_data.get("stats") or {}
        sessions = dashboard_data.get("sessions") or []
        trend = dashboard_data.get("trend") or []

        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, padx=24, pady=(22, 12), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header_frame,
            text="Dashboard thống kê tư thế",
            font=app_font(size=26, weight="bold"),
            text_color=THEME["text"],
            anchor="w",
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            header_frame,
            text="Chế độ ANN được lưu vào SQLite; rule-based chỉ dùng để đối chiếu nhanh.",
            font=app_font(size=13),
            text_color=THEME["muted"],
            anchor="w",
        ).grid(row=1, column=0, pady=(4, 0), sticky="w")

        date_selector = ctk.CTkComboBox(
            header_frame,
            values=available_dates,
            state="readonly",
            width=150,
            command=lambda value: self.reload_statistics_dashboard(
                main_frame,
                stats_window,
                value,
            ),
        )
        date_selector.set(selected_date)
        date_selector.grid(row=0, column=1, rowspan=2, padx=(16, 0), sticky="e")

        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=2, rowspan=2, padx=(10, 0), sticky="e")
        ctk.CTkButton(
            actions_frame,
            text="Xuất CSV",
            font=app_font(size=13, weight="bold"),
            width=110,
            fg_color=THEME["success"],
            hover_color="#166534",
            command=self.export_statistics_from_ui,
        ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            actions_frame,
            text="Đóng",
            font=app_font(size=13, weight="bold"),
            width=90,
            fg_color=THEME["neutral"],
            hover_color="#475569",
            command=stats_window.destroy,
        ).pack(side="left")

        if int(stats.get("tongSoPhien", 0) or 0) == 0 and not sessions:
            empty_frame = ctk.CTkFrame(
                main_frame,
                fg_color=THEME["warning_bg"],
                border_color="#facc15",
                border_width=1,
                corner_radius=8,
            )
            empty_frame.grid(row=1, column=0, columnspan=2, padx=24, pady=(0, 12), sticky="ew")
            ctk.CTkLabel(
                empty_frame,
                text="Chưa có dữ liệu thống kê cho ngày đã chọn.",
                font=app_font(size=14, weight="bold"),
                text_color=THEME["warning"],
                anchor="w",
            ).pack(padx=14, pady=12, fill="x")

        cards_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        cards_frame.grid(row=2, column=0, columnspan=2, padx=24, pady=(0, 16), sticky="ew")
        for column_index in range(4):
            cards_frame.grid_columnconfigure(column_index, weight=1, uniform="stats_card")

        cards = [
            (
                "Tổng thời gian",
                format_duration(stats.get("tongThoiGianLamViec")),
                THEME["info"],
                f"{int(stats.get('tongSoPhien', 0) or 0)} phiên",
            ),
            (
                "Đúng tư thế",
                f"{float(stats.get('tiLeDung') or 0.0) * 100:.1f}%",
                THEME["success"],
                format_duration(stats.get("tongThoiGianDung")),
            ),
            (
                "Sai tư thế",
                f"{float(stats.get('tiLeSai') or 0.0) * 100:.1f}%",
                THEME["danger"],
                format_duration(stats.get("tongThoiGianSai")),
            ),
            (
                "Rủi ro cao nhất",
                f"{float(stats.get('highestRiskIndex') or 0.0):.1f}",
                self.risk_color(str(stats.get("highestRiskLevel") or "LOW")),
                translate_risk_level(str(stats.get("highestRiskLevel") or "LOW")),
            ),
            (
                "Cảnh báo",
                str(int(stats.get("tongSoCanhBao", 0) or 0)),
                THEME["warning"],
                "Tổng trong ngày",
            ),
            (
                "Độ tin cậy TB",
                f"{float(stats.get('doTinCayTrungBinh') or 0.0) * 100:.1f}%",
                THEME["info"],
                "Theo frame đã lưu",
            ),
            (
                "Không xác định",
                f"{float(stats.get('tiLeKhongXacDinh') or 0.0) * 100:.1f}%",
                THEME["neutral"],
                format_duration(stats.get("thoiGianKhongXacDinh")),
            ),
            (
                "Rủi ro trung bình",
                f"{float(stats.get('averageRiskIndex') or 0.0):.1f}",
                THEME["neutral"],
                "TPRI theo phiên",
            ),
        ]
        for index, (title, value, color, subtitle) in enumerate(cards):
            card = self.create_stat_card(cards_frame, title, value, color, subtitle)
            card.grid(row=index // 4, column=index % 4, padx=6, pady=6, sticky="nsew")

        chart_left = self.create_dashboard_panel(main_frame, "Tỷ lệ thời gian")
        chart_left.grid(row=3, column=0, padx=(24, 10), pady=(0, 16), sticky="nsew")
        chart_right = self.create_dashboard_panel(main_frame, "Cảnh báo theo phiên")
        chart_right.grid(row=3, column=1, padx=(10, 24), pady=(0, 16), sticky="nsew")
        self.create_time_distribution_chart(chart_left, stats)
        self.create_warning_bar_chart(chart_right, sessions)

        trend_panel = self.create_dashboard_panel(main_frame, "Xu hướng 7 ngày gần nhất")
        trend_panel.grid(row=4, column=0, columnspan=2, padx=24, pady=(0, 16), sticky="ew")
        self.create_daily_trend_chart(trend_panel, trend)

        table_panel = self.create_dashboard_panel(main_frame, "Bảng phiên trong ngày")
        table_panel.grid(row=5, column=0, columnspan=2, padx=24, pady=(0, 16), sticky="ew")
        self.create_session_table(table_panel, sessions)

        if self.is_running and self.current_session_id is not None:
            current_frame = self.create_dashboard_panel(main_frame, "Phiên đang chạy")
            current_frame.grid(row=6, column=0, columnspan=2, padx=24, pady=(0, 24), sticky="ew")
            current_text = (
                "Phiên hiện tại sẽ được lưu sau khi bấm Dừng. "
                f"Frame: {self.total_frames}, đúng: {self.correct_frames}, "
                f"sai: {self.incorrect_frames}, không có người: {self.no_person_frames}, "
                f"cảnh báo: {self.warning_count}."
            )
            ctk.CTkLabel(
                current_frame,
                text=current_text,
                justify="left",
                anchor="w",
                wraplength=940,
                font=app_font(size=13),
                text_color=THEME["muted"],
            ).pack(padx=14, pady=(0, 14), fill="x")

    def reload_statistics_dashboard(
        self,
        main_frame: Any,
        stats_window: Any,
        date_text: str,
    ) -> None:
        try:
            dashboard_data = get_dashboard_data(DATABASE_PATH, date_text)
        except Exception as exc:
            messagebox.showerror("Lỗi database", f"Không đọc được thống kê: {exc}")
            return
        self.render_statistics_dashboard(main_frame, dashboard_data, stats_window)

    def create_dashboard_panel(self, parent: Any, title: str) -> ctk.CTkFrame:
        panel = ctk.CTkFrame(
            parent,
            fg_color=THEME["surface"],
            border_color=THEME["border"],
            border_width=1,
            corner_radius=8,
        )
        panel.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            panel,
            text=title,
            font=app_font(size=16, weight="bold"),
            text_color=THEME["text"],
            anchor="w",
        ).pack(padx=14, pady=(14, 8), fill="x")
        return panel

    def create_stat_card(
        self,
        parent: Any,
        title: str,
        value: str,
        color: str | None = None,
        subtitle: str | None = None,
    ) -> ctk.CTkFrame:
        """Tao card thong ke gom title va value."""
        card = ctk.CTkFrame(
            parent,
            fg_color=THEME["surface"],
            border_color=THEME["border"],
            border_width=1,
            corner_radius=8,
        )
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card,
            text=title,
            font=app_font(size=12),
            text_color=THEME["muted"],
            anchor="w",
        ).grid(row=0, column=0, padx=14, pady=(12, 2), sticky="ew")

        ctk.CTkLabel(
            card,
            text=value,
            font=app_font(size=22, weight="bold"),
            text_color=color or THEME["text"],
            anchor="w",
        ).grid(row=1, column=0, padx=14, pady=(0, 14), sticky="ew")

        if subtitle:
            ctk.CTkLabel(
                card,
                text=subtitle,
                font=app_font(size=12),
                text_color=THEME["muted_light"],
                anchor="w",
            ).grid(row=2, column=0, padx=14, pady=(0, 12), sticky="ew")

        return card

    def create_time_distribution_chart(self, parent: Any, stats: dict[str, Any]) -> None:
        """Ve stacked horizontal bar cho ty le thoi gian."""
        correct_seconds = float(stats.get("tongThoiGianDung") or 0.0)
        incorrect_seconds = float(stats.get("tongThoiGianSai") or 0.0)
        other_seconds = float(stats.get("thoiGianKhongXacDinh") or 0.0)
        total_seconds = correct_seconds + incorrect_seconds + other_seconds

        if plt is None or FigureCanvasTkAgg is None:
            self.create_time_fallback_chart(parent, stats)
            return

        fig, ax = plt.subplots(figsize=(5.1, 2.6), dpi=100)
        self.apply_light_chart_style(fig, ax)
        if total_seconds > 0:
            left = 0.0
            for label, value, color in [
                ("Đúng", correct_seconds, THEME["success"]),
                ("Sai", incorrect_seconds, THEME["danger"]),
                ("Không xác định", other_seconds, THEME["neutral"]),
            ]:
                ratio = value / total_seconds if total_seconds > 0 else 0.0
                if ratio <= 0:
                    continue
                ax.barh(["Thời gian"], [ratio], left=left, color=color, label=label)
                if ratio >= 0.08:
                    ax.text(
                        left + ratio / 2,
                        0,
                        f"{ratio * 100:.0f}%",
                        ha="center",
                        va="center",
                        color="#ffffff",
                        fontsize=9,
                        fontweight="bold",
                    )
                left += ratio
            ax.set_xlim(0, 1)
            ax.set_xlabel("Tỷ lệ")
            ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
            ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
            ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=3, frameon=False)
        else:
            self.draw_empty_chart(ax, "Chưa có dữ liệu")
        fig.tight_layout()
        self.embed_chart(parent, fig)

    def create_time_fallback_chart(self, parent: Any, stats: dict[str, Any]) -> None:
        """Ve thong ke thoi gian bang CTkProgressBar khi chua co matplotlib."""
        correct_seconds = float(stats.get("tongThoiGianDung") or 0.0)
        incorrect_seconds = float(stats.get("tongThoiGianSai") or 0.0)
        other_seconds = float(stats.get("thoiGianKhongXacDinh") or 0.0)
        total_seconds = correct_seconds + incorrect_seconds + other_seconds

        if total_seconds <= 0:
            ctk.CTkLabel(
                parent,
                text="Chưa có dữ liệu",
                font=app_font(size=13),
                text_color=THEME["muted"],
            ).pack(expand=True, pady=36)
            return

        rows = [
            ("Đúng tư thế", correct_seconds, THEME["success"]),
            ("Sai tư thế", incorrect_seconds, THEME["danger"]),
            ("Khác", other_seconds, THEME["neutral"]),
        ]
        for label, value, color in rows:
            ratio = value / total_seconds if total_seconds > 0 else 0.0
            row_frame = ctk.CTkFrame(parent, fg_color="transparent")
            row_frame.pack(fill="x", padx=18, pady=7)
            row_frame.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                row_frame,
                text=label,
                width=95,
                anchor="w",
                text_color=THEME["text"],
                font=app_font(size=12),
            ).grid(row=0, column=0, sticky="w")
            progress = ctk.CTkProgressBar(
                row_frame,
                height=12,
                progress_color=color,
                fg_color=THEME["surface_muted"],
            )
            progress.grid(row=0, column=1, padx=10, sticky="ew")
            progress.set(ratio)
            ctk.CTkLabel(
                row_frame,
                text=f"{ratio * 100:.1f}% ({format_duration(value)})",
                width=105,
                anchor="e",
                text_color=THEME["muted"],
                font=app_font(size=12),
            ).grid(row=0, column=2, sticky="e")

    def create_warning_fallback_chart(
        self,
        parent: Any,
        sessions: list[dict[str, Any]],
    ) -> None:
        """Ve so canh bao theo phien bang CTkProgressBar khi chua co matplotlib."""
        if not sessions:
            ctk.CTkLabel(
                parent,
                text="Chưa có dữ liệu phiên",
                font=app_font(size=13),
                text_color=THEME["muted"],
            ).pack(expand=True, pady=36)
            return

        warnings = [int(session.get("soLanCanhBao") or 0) for session in sessions]
        max_warning = max(max(warnings, default=0), 1)
        for index, warning_count in enumerate(warnings, start=1):
            row_frame = ctk.CTkFrame(parent, fg_color="transparent")
            row_frame.pack(fill="x", padx=18, pady=7)
            row_frame.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(
                row_frame,
                text=f"Phiên {index}",
                width=70,
                anchor="w",
                text_color=THEME["text"],
                font=app_font(size=12),
            ).grid(row=0, column=0, sticky="w")
            progress = ctk.CTkProgressBar(
                row_frame,
                height=12,
                progress_color=THEME["warning"],
                fg_color=THEME["surface_muted"],
            )
            progress.grid(row=0, column=1, padx=10, sticky="ew")
            progress.set(warning_count / max_warning)
            ctk.CTkLabel(
                row_frame,
                text=str(warning_count),
                width=32,
                anchor="e",
                text_color=THEME["muted"],
                font=app_font(size=12),
            ).grid(row=0, column=2, sticky="e")

    def create_warning_bar_chart(self, parent: Any, sessions: list[dict[str, Any]]) -> None:
        """Ve bar chart so canh bao theo tung phien."""
        if plt is None or FigureCanvasTkAgg is None:
            self.create_warning_fallback_chart(parent, sessions)
            return

        fig, ax = plt.subplots(figsize=(5.1, 2.8), dpi=100)
        self.apply_light_chart_style(fig, ax)
        if sessions:
            recent_sessions = sessions[-15:]
            labels = [f"#{session.get('maPhien')}" for session in recent_sessions]
            warnings = [int(session.get("soLanCanhBao") or 0) for session in recent_sessions]
            bars = ax.bar(labels, warnings, color=THEME["warning"], width=0.55)
            ax.set_ylabel("Số cảnh báo")
            ax.set_ylim(0, max(max(warnings, default=0) + 1, 1))
            for bar, warning_count in zip(bars, warnings):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.05,
                    str(warning_count),
                    ha="center",
                    va="bottom",
                    color=THEME["text"],
                    fontsize=9,
                )
        else:
            self.draw_empty_chart(ax, "Chưa có dữ liệu phiên")

        fig.tight_layout()
        self.embed_chart(parent, fig)

    def create_daily_trend_chart(self, parent: Any, trend: list[dict[str, Any]]) -> None:
        """Ve xu huong 7 ngay gan nhat."""
        if plt is None or FigureCanvasTkAgg is None:
            if not trend:
                ctk.CTkLabel(
                    parent,
                    text="Chưa có dữ liệu xu hướng",
                    font=app_font(size=13),
                    text_color=THEME["muted"],
                ).pack(expand=True, pady=36)
                return
            max_warning = max([int(item.get("tongSoCanhBao") or 0) for item in trend] + [1])
            for item in trend:
                row = ctk.CTkFrame(parent, fg_color="transparent")
                row.pack(fill="x", padx=14, pady=5)
                row.grid_columnconfigure(1, weight=1)
                ctk.CTkLabel(
                    row,
                    text=str(item.get("ngay")),
                    width=95,
                    anchor="w",
                    text_color=THEME["text"],
                ).grid(row=0, column=0, sticky="w")
                progress = ctk.CTkProgressBar(
                    row,
                    height=10,
                    progress_color=THEME["danger"],
                    fg_color=THEME["surface_muted"],
                )
                progress.grid(row=0, column=1, padx=10, sticky="ew")
                progress.set(float(item.get("tiLeSai") or 0.0))
                ctk.CTkLabel(
                    row,
                    text=f"Sai {float(item.get('tiLeSai') or 0.0) * 100:.1f}% | Cảnh báo {int(item.get('tongSoCanhBao') or 0)}/{max_warning}",
                    width=140,
                    anchor="e",
                    text_color=THEME["muted"],
                    font=app_font(size=12),
                ).grid(row=0, column=2, sticky="e")
            return

        fig, ax1 = plt.subplots(figsize=(10.2, 3.0), dpi=100)
        self.apply_light_chart_style(fig, ax1)
        if trend:
            labels = [str(item.get("ngay", ""))[5:] for item in trend]
            incorrect = [float(item.get("tiLeSai") or 0.0) * 100 for item in trend]
            warnings = [int(item.get("tongSoCanhBao") or 0) for item in trend]
            ax1.plot(labels, incorrect, color=THEME["danger"], marker="o", linewidth=2)
            ax1.set_ylabel("Sai tư thế (%)", color=THEME["danger"])
            ax1.tick_params(axis="y", labelcolor=THEME["danger"])
            ax1.set_ylim(0, max(max(incorrect, default=0.0) + 10, 10))

            ax2 = ax1.twinx()
            ax2.bar(labels, warnings, color=THEME["warning"], alpha=0.25, width=0.55)
            ax2.set_ylabel("Cảnh báo", color=THEME["warning"])
            ax2.tick_params(axis="y", labelcolor=THEME["warning"])
            ax2.spines["right"].set_color(THEME["border"])
        else:
            self.draw_empty_chart(ax1, "Chưa có dữ liệu xu hướng")

        fig.tight_layout()
        self.embed_chart(parent, fig)

    def create_session_table(self, parent: Any, sessions: list[dict[str, Any]]) -> None:
        """Hien thi phien trong ngay bang table co cot."""
        if not sessions:
            ctk.CTkLabel(
                parent,
                text="Chưa có phiên trong ngày đã chọn.",
                font=app_font(size=13),
                text_color=THEME["muted"],
            ).pack(padx=14, pady=(0, 16), anchor="w")
            return

        self.style_session_tree()
        columns = (
            "start",
            "duration",
            "correct",
            "incorrect",
            "unknown",
            "warnings",
            "confidence",
            "risk",
        )
        tree = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            height=min(10, max(4, len(sessions))),
        )
        headings = {
            "start": "Bắt đầu",
            "duration": "Thời lượng",
            "correct": "Đúng",
            "incorrect": "Sai",
            "unknown": "Không người",
            "warnings": "Cảnh báo",
            "confidence": "Tin cậy",
            "risk": "Rủi ro",
        }
        widths = {
            "start": 120,
            "duration": 90,
            "correct": 80,
            "incorrect": 80,
            "unknown": 100,
            "warnings": 80,
            "confidence": 80,
            "risk": 110,
        }
        for column in columns:
            tree.heading(column, text=headings[column])
            tree.column(column, width=widths[column], anchor="center", stretch=True)

        for session in sessions:
            start_text = str(session.get("thoiGianBatDau") or "")
            try:
                start_display = datetime.fromisoformat(start_text).strftime("%H:%M:%S")
            except ValueError:
                start_display = start_text[11:19] if len(start_text) >= 19 else "--:--:--"
            risk_text = (
                f"{float(session.get('riskIndex') or 0.0):.1f} "
                f"{translate_risk_level(str(session.get('riskLevel') or 'LOW'))}"
            )
            tree.insert(
                "",
                "end",
                values=(
                    f"#{session.get('maPhien')} {start_display}",
                    format_duration(session.get("durationSeconds")),
                    f"{float(session.get('correctRatio') or 0.0) * 100:.1f}%",
                    f"{float(session.get('incorrectRatio') or 0.0) * 100:.1f}%",
                    f"{float(session.get('noPersonRatio') or 0.0) * 100:.1f}%",
                    int(session.get("soLanCanhBao") or 0),
                    f"{float(session.get('averageConfidence') or 0.0) * 100:.1f}%",
                    risk_text,
                ),
            )

        tree.pack(fill="x", expand=False, padx=14, pady=(0, 14))

    def style_session_tree(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure(
            "Treeview",
            background=THEME["surface"],
            foreground=THEME["text"],
            fieldbackground=THEME["surface"],
            rowheight=28,
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            background=THEME["surface_muted"],
            foreground=THEME["text"],
            relief="flat",
            font=("Segoe UI", 10, "bold"),
        )
        style.map("Treeview", background=[("selected", THEME["info_bg"])])

    def apply_light_chart_style(self, fig: Any, ax: Any) -> None:
        fig.patch.set_facecolor(THEME["surface"])
        ax.set_facecolor(THEME["surface"])
        ax.tick_params(axis="x", colors=THEME["muted"])
        ax.tick_params(axis="y", colors=THEME["muted"])
        ax.grid(axis="y", color=THEME["border_soft"], linestyle="--", linewidth=0.7)
        for spine in ax.spines.values():
            spine.set_color(THEME["border"])
        ax.xaxis.label.set_color(THEME["muted"])
        ax.yaxis.label.set_color(THEME["muted"])

    def draw_empty_chart(self, ax: Any, text: str) -> None:
        ax.text(
            0.5,
            0.5,
            text,
            ha="center",
            va="center",
            color=THEME["muted"],
            fontsize=12,
            transform=ax.transAxes,
        )
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    def embed_chart(self, parent: Any, fig: Any) -> None:
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.configure(bg=THEME["surface"], highlightthickness=0)
        widget.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        parent._chart_canvas = canvas

    def risk_color(self, risk_level_text: str) -> str:
        return {
            "LOW": THEME["success"],
            "MEDIUM": THEME["warning"],
            "HIGH": THEME["danger"],
            "CRITICAL": "#7f1d1d",
        }.get(risk_level_text, THEME["neutral"])

    def export_statistics_from_ui(self) -> None:
        """Chay script export CSV thong ke tu dashboard."""
        if is_frozen():
            messagebox.showinfo(
                "Xuất CSV",
                "Bản desktop đã đóng gói chỉ hỗ trợ xem thống kê trong app. "
                "Hãy dùng bản source Python nếu cần xuất CSV nghiên cứu.",
            )
            return

        script_path = BASE_DIR / "src" / "10_export_statistics.py"
        try:
            subprocess.run(
                [sys.executable, str(script_path)],
                cwd=BASE_DIR,
                check=True,
                capture_output=True,
                text=True,
            )
        except Exception as exc:
            messagebox.showerror("Xuất CSV", f"Không export được thống kê: {exc}")
            return

        messagebox.showinfo(
            "Xuất CSV",
            "Đã export thống kê vào reports/results.",
        )

    # =========================
    # Dung app va giai phong tai nguyen
    # =========================
    def get_session_seconds(self) -> float:
        """Tinh tong thoi gian phien hien tai."""
        if self.session_start_time is None:
            return 0.0
        return max(0.0, (datetime.now() - self.session_start_time).total_seconds())

    def stop_camera(self) -> None:
        """Dung camera/video va cap nhat database."""
        self.stop_alarm_sound()
        self.cancel_pending_frame_update()

        if not self.is_running and self.cap is None:
            self.clear_video_label("Chưa bật camera")
            self.mode_combobox.configure(state="readonly")
            if self.is_rule_based_mode():
                self.baseline_info_frame.grid()
                self.baseline_info_label.configure(text="Baseline: chưa chạy")
            else:
                self.baseline_info_frame.grid_remove()
            return

        was_ann_mode = self.is_ann_mode()
        self.is_running = False
        self.release_video_resources()
        if was_ann_mode and self.current_session_id is not None:
            self.end_phien_lam_viec()
            print("Da dung camera va cap nhat phien lam viec.")
        else:
            self.current_session_id = None
            print("Da dung baseline test. Khong cap nhat database.")

        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.save_button.configure(state="normal")
        self.mode_combobox.configure(state="readonly")
        self.update_status_ui("DANG_KIEM_TRA", None)
        if self.is_rule_based_mode():
            self.baseline_info_frame.grid()
            self.baseline_info_label.configure(text="Baseline: chưa chạy")
        else:
            self.baseline_info_frame.grid_remove()
        self.clear_video_label("Chưa bật camera")

    def release_video_resources(self) -> None:
        """Giai phong VideoCapture va MediaPipe Pose neu dang mo."""
        self.stop_capture_thread()

        if self.cap is not None:
            try:
                self.cap.release()
            except Exception as exc:
                print(f"WARNING: Loi khi release camera: {exc}")
            self.cap = None

        if self.pose is not None:
            try:
                self.pose.close()
            except Exception as exc:
                print(f"WARNING: Loi khi dong MediaPipe Pose: {exc}")
            self.pose = None

    def on_close(self) -> None:
        """Xu ly khi nguoi dung dong cua so app."""
        try:
            self.stop_camera()
            self.stop_alarm_sound()
        finally:
            self.destroy()


def main() -> None:
    """Chay ung dung desktop."""
    app = PostureApp()
    app.mainloop()


if __name__ == "__main__":
    main()
