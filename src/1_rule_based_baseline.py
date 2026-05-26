"""
Baseline rule-based phat hien loi tu the lam viec qua webcam, camera IP
hoac tep video.

Pipeline:
OpenCV video source -> MediaPipe Pose -> Landmark Extraction -> Feature
Engineering -> Rule-based Classification -> Realtime Warning.

Luu y:
- Day la baseline dung nguong thuc nghiem ban dau de so sanh voi mo hinh ANN
  sau nay.
- Cac nguong dua tren nguyen tac cong thai hoc co ban: dau nen gan thang
  hang voi than, vai thu gian/can bang, than khong nghieng qua muc, man hinh
  nen o ngang hoac hoi thap hon tam mat.
- MediaPipe Pose khong co diem cam chinh xac. Dau hieu chong cam / tay gan
  mieng duoc phat hien gian tiep bang diem mieng va cac diem ban tay.
- Day khong phai cong cu chan doan y te.
"""

from __future__ import annotations

import argparse
import math
import os
import sys
import time
from types import SimpleNamespace
from typing import Any

import cv2
import mediapipe as mp


# =========================
# Cac nguong thuc nghiem
# =========================
# Cac nguong nay la nguong thuc nghiem ban dau, can tinh chinh them bang
# du lieu thuc te cua nguoi dung. Baseline nay dung de so sanh voi ANN sau nay.
MIN_VISIBILITY = 0.5
SHOULDER_Y_DIFF_THRESHOLD = 0.06
SHOULDER_TILT_ANGLE_THRESHOLD = 10.0
TORSO_LEAN_ANGLE_THRESHOLD = 12.0
HEAD_OFFSET_X_THRESHOLD = 0.10
NOSE_TO_SHOULDER_Y_THRESHOLD = -0.03
WRONG_POSTURE_SECONDS = 3.0
HAND_TO_FACE_RATIO_THRESHOLD = 0.55
CHIN_REST_ELBOW_MIN_ANGLE = 35.0
CHIN_REST_ELBOW_MAX_ANGLE = 145.0
HAND_HIGH_Y_OFFSET_THRESHOLD = 0.15
HAND_TO_MOUTH_RATIO_THRESHOLD = 0.45
HAND_TO_MOUTH_ABS_THRESHOLD = 0.13
HAND_POINT_MIN_VISIBILITY = 0.35
USE_ELBOW_ANGLE_FOR_CHIN_REST = False


# Thiet lap hien thi.
WINDOW_NAME = "Baseline Rule-based Phat Hien Tu The"
PANEL_WIDTH = 430
VIDEO_FILE_MAX_DISPLAY_WIDTH = 1280
VIDEO_FILE_MAX_DISPLAY_HEIGHT = 720
FONT = cv2.FONT_HERSHEY_SIMPLEX


mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


def create_default_features(valid: bool = False) -> dict[str, float | bool]:
    """Tao bo gia tri mac dinh de tranh loi khi thieu landmark."""
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
    """Lay landmark tu danh sach MediaPipe theo enum."""
    try:
        return landmarks[landmark_enum.value]
    except (IndexError, AttributeError, TypeError):
        return None


def midpoint(p1: Any, p2: Any) -> tuple[float, float]:
    """Tinh trung diem 2 landmark trong he toa do chuan hoa cua MediaPipe."""
    return ((p1.x + p2.x) / 2.0, (p1.y + p2.y) / 2.0)


def calculate_distance_2d(p1: Any, p2: Any) -> float:
    """Tinh khoang cach 2D bang toa do chuan hoa cua MediaPipe."""
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def get_visible_landmarks(
    landmarks: list[Any],
    landmark_enums: list[Any],
    min_visibility: float = HAND_POINT_MIN_VISIBILITY,
) -> list[Any]:
    """
    Tra ve cac landmark ton tai va co visibility du tot.

    Ham nay dung de lay cac diem ung vien cua ban tay nhu wrist, index, pinky,
    thumb. Diem co visibility thap se bi bo qua de giam nhan nham.
    """
    visible_points: list[Any] = []
    for landmark_enum in landmark_enums:
        point = get_landmark(landmarks, landmark_enum)
        if point is not None and getattr(point, "visibility", 0.0) >= min_visibility:
            visible_points.append(point)

    return visible_points


def calculate_min_distance_to_point(
    points: list[Any], target_point: Any
) -> tuple[float, Any | None]:
    """
    Tinh khoang cach nho nhat tu danh sach diem den target_point.

    Neu danh sach rong thi tra ve 999.0 va None de rule phia sau hieu la khong
    co tay gan mieng.
    """
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
    """
    Tinh goc ABC, trong do b la dinh goc.

    Dung de tinh goc khuyu tay: shoulder-elbow-wrist. Ham xu ly an toan khi
    hai diem trung nhau de tranh chia cho 0.
    """
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
    """
    Tinh goc cua duong noi p1-p2 so voi phuong ngang.

    MediaPipe dung toa do anh chuan hoa: x tang tu trai sang phai, y tang tu
    tren xuong duoi. Lay tri tuyet doi de do muc nghieng cua vai.
    """
    dx = abs(p2.x - p1.x)
    dy = abs(p2.y - p1.y)
    return math.degrees(math.atan2(dy, dx))


def calculate_torso_lean_angle(
    mid_shoulder: tuple[float, float], mid_hip: tuple[float, float]
) -> float:
    """
    Tinh goc lech cua truc than so voi phuong thang dung.

    Neu trung diem vai nam ngay tren trung diem hong thi dx gan 0 va goc lech
    gan 0 do. Goc cang lon nghia la than co xu huong nghieng sang mot ben.
    """
    dx = abs(mid_shoulder[0] - mid_hip[0])
    dy = abs(mid_shoulder[1] - mid_hip[1])

    if dy < 1e-6:
        return 90.0

    return abs(math.degrees(math.atan2(dx, dy)))


def extract_posture_features(landmarks: list[Any]) -> dict[str, float | bool]:
    """
    Trich xuat dac trung hinh hoc tu landmark.

    Cac feature dung toa do chuan hoa [0, 1], giup it phu thuoc vao do phan
    giai webcam/video. Elbow/wrist/finger khong bat buoc de posture cu van
    chay binh thuong.
    """
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

    # Gia tri cang lon/cang gan 0 nghia la mui cang thap so voi vai, thuong la
    # dau hieu cui dau hoac camera dat qua cao. Can hieu chinh bang du lieu that.
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

    # MediaPipe Pose khong co diem cam chinh xac. Vi vay baseline nay dung
    # trung diem MOUTH_LEFT/MOUTH_RIGHT lam dai dien vung mieng/cam, va dung
    # WRIST/INDEX/PINKY/THUMB lam dai dien ban tay. Neu diem tay gan nhat nam
    # gan vung mieng trong nhieu frame lien tuc, smoothing se xem do la dau
    # hieu chong cam / tay ty len mat. Day la rule-based heuristic baseline,
    # khong phai chan doan y te.
    if mouth_left is not None and mouth_right is not None:
        mouth_x, mouth_y = midpoint(mouth_left, mouth_right)
        mouth_center = SimpleNamespace(x=mouth_x, y=mouth_y)
    else:
        # Fallback an toan neu MediaPipe khong bat duoc landmark mieng.
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

    left_nearest_hand_point = None
    right_nearest_hand_point = None
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
        # Giu key cu de tranh loi cac phan hien thi/debug cu.
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
    """Phan loai tu the bang cac luat/nguong thu cong."""
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
        warnings.append("Lech vai hoac nghieng vai")

    if float(features["torso_lean_angle"]) > TORSO_LEAN_ANGLE_THRESHOLD:
        warnings.append("Than nguoi bi nghieng")

    if float(features["head_offset_x"]) > HEAD_OFFSET_X_THRESHOLD:
        warnings.append("Dau lech khoi truc vai")

    if float(features["nose_to_shoulder_y"]) > NOSE_TO_SHOULDER_Y_THRESHOLD:
        warnings.append("Co dau hieu cui dau")

    if bool(features.get("chin_rest_detected", False)):
        warnings.append("Co dau hieu chong cam / tay gan mieng")

    if warnings:
        return "INCORRECT", warnings

    return "CORRECT", []


def draw_text(
    frame: Any,
    text: str,
    position: tuple[int, int],
    color: tuple[int, int, int],
    scale: float = 0.55,
    thickness: int = 1,
) -> None:
    """Ve chu co vien den de de doc tren nen webcam/video."""
    cv2.putText(frame, text, position, FONT, scale, (0, 0, 0), thickness + 2, cv2.LINE_AA)
    cv2.putText(frame, text, position, FONT, scale, color, thickness, cv2.LINE_AA)


def draw_status_panel(
    frame: Any,
    status: str,
    warnings: list[str],
    features: dict[str, float | bool],
    wrong_duration: float,
    fps: float = 0.0,
) -> None:
    """Ve panel trang thai, canh bao, dac trung va FPS len frame."""
    height, width = frame.shape[:2]
    panel_x1 = max(width - PANEL_WIDTH, 0)

    overlay = frame.copy()
    cv2.rectangle(overlay, (panel_x1, 0), (width, height), (35, 35, 35), -1)
    cv2.addWeighted(overlay, 0.68, frame, 0.32, 0, frame)

    green = (70, 220, 70)
    orange = (0, 190, 255)
    red = (40, 40, 255)
    white = (245, 245, 245)
    gray = (190, 190, 190)

    x = panel_x1 + 18
    y = 34

    if status == "CORRECT":
        header_text = "TU THE DUNG"
        header_color = green
    elif status == "INCORRECT" and wrong_duration >= WRONG_POSTURE_SECONDS:
        header_text = "CANH BAO: SAI TU THE"
        header_color = red
    elif status == "INCORRECT":
        header_text = "DANG KIEM TRA TU THE..."
        header_color = orange
    else:
        header_text = "KHONG PHAT HIEN NGUOI / DO TIN CAY THAP"
        header_color = gray

    draw_text(frame, header_text, (x, y), header_color, scale=0.58, thickness=2)

    y += 34
    draw_text(frame, f"FPS: {fps:.1f}", (x, y), white)

    if status == "INCORRECT":
        y += 26
        draw_text(
            frame,
            f"Thoi gian sai: {wrong_duration:.1f}s / {WRONG_POSTURE_SECONDS:.1f}s",
            (x, y),
            orange if wrong_duration < WRONG_POSTURE_SECONDS else red,
        )

    y += 36
    draw_text(frame, "Canh bao:", (x, y), white, scale=0.56, thickness=2)

    if warnings:
        for warning in warnings[:5]:
            y += 24
            draw_text(frame, f"- {warning}", (x, y), orange, scale=0.5)
    else:
        y += 24
        draw_text(frame, "- Khong co", (x, y), gray, scale=0.5)

    y += 38
    draw_text(frame, "Dac trung:", (x, y), white, scale=0.56, thickness=2)

    feature_lines = [
        ("do lech vai y", "shoulder_y_diff"),
        ("goc nghieng vai", "shoulder_tilt_angle"),
        ("goc nghieng than", "torso_lean_angle"),
        ("do lech dau x", "head_offset_x"),
        ("mui so voi vai y", "nose_to_shoulder_y"),
        ("do tin cay", "visibility"),
        ("tay trai gan mieng ti le", "left_hand_mouth_ratio"),
        ("tay phai gan mieng ti le", "right_hand_mouth_ratio"),
        ("kc tay trai den mieng", "left_hand_mouth_distance"),
        ("kc tay phai den mieng", "right_hand_mouth_distance"),
        ("tay trai gan mieng", "left_hand_near_mouth"),
        ("tay phai gan mieng", "right_hand_near_mouth"),
        ("goc khuyu tay trai", "left_elbow_angle"),
        ("goc khuyu tay phai", "right_elbow_angle"),
        ("phat hien chong cam", "chin_rest_detected"),
    ]

    for label, key in feature_lines:
        y += 21
        value = features.get(key, 0.0)
        if isinstance(value, bool):
            value_text = str(value)
        else:
            value_text = f"{float(value):.3f}"
        draw_text(frame, f"{label}: {value_text}", (x, y), white, scale=0.42)

    if status == "INCORRECT" and wrong_duration >= WRONG_POSTURE_SECONDS:
        banner_height = 56
        cv2.rectangle(frame, (0, 0), (width, banner_height), red, -1)
        draw_text(
            frame,
            "CANH BAO: SAI TU THE",
            (24, 38),
            (255, 255, 255),
            scale=0.95,
            thickness=2,
        )


def draw_chin_rest_debug(frame: Any, features: dict[str, float | bool]) -> None:
    """
    Ve debug cho rule tay gan mieng/cam.

    Cham do la trung diem mieng. Cham vang/cam la diem ban tay gan mieng nhat
    khi tay duoc danh dau gan mieng. Duong noi giup kiem tra truc quan nguong.
    """
    if not features.get("valid", False):
        return

    height, width = frame.shape[:2]
    mouth_x = float(features.get("mouth_center_x", 0.0))
    mouth_y = float(features.get("mouth_center_y", 0.0))

    if mouth_x <= 0.0 and mouth_y <= 0.0:
        return

    mouth_point = (int(mouth_x * width), int(mouth_y * height))
    cv2.circle(frame, mouth_point, 6, (0, 0, 255), -1)

    debug_specs = [
        (
            "left_hand_near_mouth",
            "left_nearest_hand_x",
            "left_nearest_hand_y",
            (0, 255, 255),
        ),
        (
            "right_hand_near_mouth",
            "right_nearest_hand_x",
            "right_nearest_hand_y",
            (0, 165, 255),
        ),
    ]

    for near_key, x_key, y_key, color in debug_specs:
        if not bool(features.get(near_key, False)):
            continue

        hand_x = float(features.get(x_key, 0.0))
        hand_y = float(features.get(y_key, 0.0))
        if hand_x <= 0.0 and hand_y <= 0.0:
            continue

        hand_point = (int(hand_x * width), int(hand_y * height))
        cv2.circle(frame, hand_point, 7, color, -1)
        cv2.line(frame, mouth_point, hand_point, color, 2)


def _resolve_source(source: Any) -> tuple[int | str, str]:
    """
    Chuan hoa nguon video dau vao.

    Ho tro webcam index, URL camera IP va duong dan tep video. Ham nay chi
    phan loai nguon video de mo bang OpenCV, khong thay doi logic phat hien.
    """
    if source is None:
        return 0, "Webcam (0)"

    if isinstance(source, int):
        return source, f"Webcam ({source})"

    source_str = str(source).strip()
    if source_str.isdigit():
        camera_index = int(source_str)
        return camera_index, f"Webcam ({camera_index})"

    lower_source = source_str.lower()
    if lower_source.startswith(("rtsp://", "http://", "https://")):
        return source_str, "Camera IP"

    if os.path.isfile(source_str):
        return source_str, "Tep Video"

    if "://" in source_str:
        return source_str, "Camera IP"

    return source_str, "Tep Video"


def resize_video_frame_if_needed(frame: Any) -> Any:
    """
    Thu nho frame cua tep video de cua so OpenCV khong vuot qua man hinh.

    Chi scale xuong khi video lon hon gioi han hien thi, giu nguyen ti le anh.
    MediaPipe dung toa do chuan hoa nen viec resize truoc khi xu ly khong lam
    thay doi logic tinh feature/rule-based classification.
    """
    height, width = frame.shape[:2]
    scale = min(
        VIDEO_FILE_MAX_DISPLAY_WIDTH / width,
        VIDEO_FILE_MAX_DISPLAY_HEIGHT / height,
        1.0,
    )

    if scale >= 1.0:
        return frame

    new_size = (int(width * scale), int(height * scale))
    return cv2.resize(frame, new_size, interpolation=cv2.INTER_AREA)


def main(source: Any = "0") -> bool:
    """Chay baseline rule-based realtime bang webcam, camera IP hoac tep video."""
    source_value, source_label = _resolve_source(source)
    window_title = f"{WINDOW_NAME} - {source_label}"
    cap = cv2.VideoCapture(source_value)

    if not cap.isOpened():
        print(f"ERROR: Khong mo duoc nguon video: {source}")
        print("Goi y:")
        print("- Kiem tra webcam index 0/1/2")
        print("- Kiem tra duong dan tep video")
        print("- Kiem tra URL camera IP")
        return False

    wrong_start_time: float | None = None
    previous_time = time.time()
    fps = 0.0
    is_video_file = source_label == "Tep Video"

    print("Dang chay baseline rule-based phat hien tu the.")
    print(f"Nguon video: {source_label}")
    print("Nhan phim 'q' de thoat.")

    try:
        with mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        ) as pose:
            while True:
                success, frame = cap.read()
                if not success or frame is None:
                    if is_video_file:
                        print("Khong doc duoc frame hoac video da ket thuc.")
                    else:
                        print("Khong doc duoc frame tu nguon video.")
                    break

                current_time = time.time()
                elapsed = current_time - previous_time
                previous_time = current_time
                if elapsed > 0:
                    fps = 0.9 * fps + 0.1 * (1.0 / elapsed) if fps > 0 else 1.0 / elapsed

                if is_video_file:
                    frame = resize_video_frame_if_needed(frame)

                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb_frame.flags.writeable = False
                results = pose.process(rgb_frame)
                rgb_frame.flags.writeable = True

                features = create_default_features(valid=False)
                status = "NO_PERSON_OR_LOW_CONFIDENCE"
                warnings: list[str] = []

                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
                    )

                    features = extract_posture_features(results.pose_landmarks.landmark)
                    status, warnings = classify_posture_rule_based(features)
                    draw_chin_rest_debug(frame, features)

                if status == "INCORRECT":
                    if wrong_start_time is None:
                        wrong_start_time = current_time
                    wrong_duration = current_time - wrong_start_time
                else:
                    wrong_start_time = None
                    wrong_duration = 0.0

                draw_status_panel(frame, status, warnings, features, wrong_duration, fps)
                cv2.imshow(window_title, frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    except KeyboardInterrupt:
        print("\nDa dung chuong trinh theo yeu cau nguoi dung.")
    except Exception as exc:
        print(f"ERROR: Loi trong vong lap chinh: {exc}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Da giai phong nguon video va dong cua so.")

    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Baseline rule-based phat hien sai tu the qua webcam, "
            "camera IP hoac tep video."
        )
    )
    parser.add_argument(
        "--source",
        "-s",
        default="0",
        help=(
            "0 cho webcam mac dinh, 1/2 cho webcam khac, URL rtsp/http "
            "cho camera IP, hoac duong dan tep video."
        ),
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    ok = main(args.source)
    if ok is False:
        sys.exit(1)
