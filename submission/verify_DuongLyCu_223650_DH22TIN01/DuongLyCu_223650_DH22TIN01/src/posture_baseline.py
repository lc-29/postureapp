"""Shared rule-based posture baseline utilities."""

from __future__ import annotations

import math
from types import SimpleNamespace
from typing import Any


MIN_VISIBILITY = 0.5
SHOULDER_Y_DIFF_THRESHOLD = 0.06
SHOULDER_TILT_ANGLE_THRESHOLD = 10.0
TORSO_LEAN_ANGLE_THRESHOLD = 12.0
HEAD_OFFSET_X_THRESHOLD = 0.10
NOSE_TO_SHOULDER_Y_THRESHOLD = -0.03
MIN_NOSE_SHOULDER_CLEARANCE_RATIO = 0.12
HAND_TO_MOUTH_RATIO_THRESHOLD = 0.45
HAND_TO_MOUTH_ABS_THRESHOLD = 0.13
HAND_POINT_MIN_VISIBILITY = 0.35

NOSE = 0
MOUTH_LEFT = 9
MOUTH_RIGHT = 10
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_ELBOW = 13
RIGHT_ELBOW = 14
LEFT_WRIST = 15
RIGHT_WRIST = 16
LEFT_PINKY = 17
RIGHT_PINKY = 18
LEFT_INDEX = 19
RIGHT_INDEX = 20
LEFT_THUMB = 21
RIGHT_THUMB = 22
LEFT_HIP = 23
RIGHT_HIP = 24


def create_default_features(valid: bool = False) -> dict[str, float | bool]:
    return {
        "valid": valid,
        "shoulder_y_diff": 0.0,
        "shoulder_tilt_angle": 0.0,
        "torso_lean_angle": 0.0,
        "head_offset_x": 0.0,
        "nose_to_shoulder_y": 0.0,
        "nose_shoulder_clearance": 0.0,
        "nose_shoulder_clearance_ratio": 0.0,
        "neck_compression_detected": False,
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


def get_landmark(landmarks: list[Any], index: int) -> Any | None:
    try:
        return landmarks[index]
    except (IndexError, TypeError):
        return None


def midpoint(p1: Any, p2: Any) -> tuple[float, float]:
    return ((p1.x + p2.x) / 2.0, (p1.y + p2.y) / 2.0)


def calculate_distance_2d(p1: Any, p2: Any) -> float:
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def calculate_angle_3_points(a: Any, b: Any, c: Any) -> float:
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
    return math.degrees(math.atan2(abs(p2.y - p1.y), abs(p2.x - p1.x)))


def calculate_torso_lean_angle(
    mid_shoulder: tuple[float, float], mid_hip: tuple[float, float]
) -> float:
    dx = abs(mid_shoulder[0] - mid_hip[0])
    dy = abs(mid_shoulder[1] - mid_hip[1])
    if dy < 1e-6:
        return 90.0
    return abs(math.degrees(math.atan2(dx, dy)))


def visible_points(landmarks: list[Any], indexes: list[int]) -> list[Any]:
    return [
        point
        for index in indexes
        if (point := get_landmark(landmarks, index)) is not None
        and getattr(point, "visibility", 1.0) >= HAND_POINT_MIN_VISIBILITY
    ]


def nearest_distance(points: list[Any], target: Any) -> tuple[float, Any | None]:
    if not points:
        return 999.0, None
    nearest = min(points, key=lambda point: calculate_distance_2d(point, target))
    return calculate_distance_2d(nearest, target), nearest


def extract_posture_features(landmarks: list[Any]) -> dict[str, float | bool]:
    nose = get_landmark(landmarks, NOSE)
    left_shoulder = get_landmark(landmarks, LEFT_SHOULDER)
    right_shoulder = get_landmark(landmarks, RIGHT_SHOULDER)
    left_hip = get_landmark(landmarks, LEFT_HIP)
    right_hip = get_landmark(landmarks, RIGHT_HIP)

    required_landmarks = [nose, left_shoulder, right_shoulder, left_hip, right_hip]
    if any(point is None for point in required_landmarks):
        return create_default_features(valid=False)

    visibility = sum(getattr(point, "visibility", 1.0) for point in required_landmarks) / len(
        required_landmarks
    )
    if visibility < MIN_VISIBILITY:
        features = create_default_features(valid=False)
        features["visibility"] = float(visibility)
        return features

    mid_shoulder = midpoint(left_shoulder, right_shoulder)
    mid_hip = midpoint(left_hip, right_hip)
    mouth_left = get_landmark(landmarks, MOUTH_LEFT)
    mouth_right = get_landmark(landmarks, MOUTH_RIGHT)
    if mouth_left is not None and mouth_right is not None:
        mouth_center = SimpleNamespace(
            x=(mouth_left.x + mouth_right.x) / 2.0,
            y=(mouth_left.y + mouth_right.y) / 2.0,
        )
    else:
        mouth_center = SimpleNamespace(x=nose.x, y=nose.y)

    shoulder_width = max(calculate_distance_2d(left_shoulder, right_shoulder), 1e-6)
    torso_height = max(mid_hip[1] - mid_shoulder[1], 1e-6)
    # MediaPipe image y increases downward. Small clearance means the nose is
    # close to shoulder height, which indicates deep neck compression.
    nose_shoulder_clearance = mid_shoulder[1] - nose.y
    nose_shoulder_clearance_ratio = nose_shoulder_clearance / torso_height
    neck_compression_detected = (
        nose_shoulder_clearance_ratio < MIN_NOSE_SHOULDER_CLEARANCE_RATIO
    )
    left_hand_points = visible_points(landmarks, [LEFT_WRIST, LEFT_INDEX, LEFT_PINKY, LEFT_THUMB])
    right_hand_points = visible_points(
        landmarks, [RIGHT_WRIST, RIGHT_INDEX, RIGHT_PINKY, RIGHT_THUMB]
    )
    left_distance, left_nearest = nearest_distance(left_hand_points, mouth_center)
    right_distance, right_nearest = nearest_distance(right_hand_points, mouth_center)
    left_ratio = left_distance / shoulder_width
    right_ratio = right_distance / shoulder_width
    left_near = left_ratio < HAND_TO_MOUTH_RATIO_THRESHOLD or left_distance < HAND_TO_MOUTH_ABS_THRESHOLD
    right_near = right_ratio < HAND_TO_MOUTH_RATIO_THRESHOLD or right_distance < HAND_TO_MOUTH_ABS_THRESHOLD

    left_elbow = get_landmark(landmarks, LEFT_ELBOW)
    right_elbow = get_landmark(landmarks, RIGHT_ELBOW)
    left_wrist = get_landmark(landmarks, LEFT_WRIST)
    right_wrist = get_landmark(landmarks, RIGHT_WRIST)
    left_elbow_angle = (
        calculate_angle_3_points(left_shoulder, left_elbow, left_wrist)
        if left_elbow is not None and left_wrist is not None
        else 0.0
    )
    right_elbow_angle = (
        calculate_angle_3_points(right_shoulder, right_elbow, right_wrist)
        if right_elbow is not None and right_wrist is not None
        else 0.0
    )

    return {
        "valid": True,
        "shoulder_y_diff": abs(left_shoulder.y - right_shoulder.y),
        "shoulder_tilt_angle": calculate_line_angle_degrees(left_shoulder, right_shoulder),
        "torso_lean_angle": calculate_torso_lean_angle(mid_shoulder, mid_hip),
        "head_offset_x": abs(nose.x - mid_shoulder[0]),
        "nose_to_shoulder_y": nose.y - mid_shoulder[1],
        "nose_shoulder_clearance": nose_shoulder_clearance,
        "nose_shoulder_clearance_ratio": nose_shoulder_clearance_ratio,
        "neck_compression_detected": neck_compression_detected,
        "visibility": float(visibility),
        "left_hand_mouth_distance": left_distance,
        "right_hand_mouth_distance": right_distance,
        "left_hand_mouth_ratio": left_ratio,
        "right_hand_mouth_ratio": right_ratio,
        "left_hand_face_ratio": left_ratio,
        "right_hand_face_ratio": right_ratio,
        "left_hand_near_mouth": left_near,
        "right_hand_near_mouth": right_near,
        "left_elbow_angle": left_elbow_angle,
        "right_elbow_angle": right_elbow_angle,
        "left_hand_near_face": left_near,
        "right_hand_near_face": right_near,
        "left_chin_rest": left_near,
        "right_chin_rest": right_near,
        "chin_rest_detected": left_near or right_near,
        "mouth_center_x": mouth_center.x,
        "mouth_center_y": mouth_center.y,
        "left_nearest_hand_x": left_nearest.x if left_nearest else 0.0,
        "left_nearest_hand_y": left_nearest.y if left_nearest else 0.0,
        "right_nearest_hand_x": right_nearest.x if right_nearest else 0.0,
        "right_nearest_hand_y": right_nearest.y if right_nearest else 0.0,
    }


def classify_posture_rule_based(features: dict[str, float | bool]) -> tuple[str, list[str]]:
    if not features.get("valid", False):
        return "NO_PERSON_OR_LOW_CONFIDENCE", []
    if float(features["visibility"]) < MIN_VISIBILITY:
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
    if bool(features.get("neck_compression_detected", False)):
        warnings.append("Mũi gần ngang vai / rụt cổ quá sâu")
    if bool(features.get("chin_rest_detected", False)):
        warnings.append("Có dấu hiệu chống cằm / tay gần miệng")

    return ("INCORRECT", warnings) if warnings else ("CORRECT", [])


def landmarks_from_feature_row(row: Any) -> list[SimpleNamespace]:
    landmarks: list[SimpleNamespace] = []
    for index in range(33):
        landmarks.append(
            SimpleNamespace(
                x=float(row[f"landmark_{index}_x"]),
                y=float(row[f"landmark_{index}_y"]),
                z=float(row[f"landmark_{index}_z"]),
                visibility=1.0,
            )
        )
    return landmarks
