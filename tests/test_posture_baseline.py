import sys
import unicodedata
from pathlib import Path
from types import SimpleNamespace

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from posture_baseline import classify_posture_rule_based, extract_posture_features


def make_landmarks(visibility=1.0):
    landmarks = [
        SimpleNamespace(x=0.5, y=0.5, z=0.0, visibility=visibility)
        for _ in range(33)
    ]
    landmarks[0] = SimpleNamespace(x=0.50, y=0.33, z=0.0, visibility=visibility)
    landmarks[9] = SimpleNamespace(x=0.48, y=0.36, z=0.0, visibility=visibility)
    landmarks[10] = SimpleNamespace(x=0.52, y=0.36, z=0.0, visibility=visibility)
    landmarks[11] = SimpleNamespace(x=0.40, y=0.42, z=0.0, visibility=visibility)
    landmarks[12] = SimpleNamespace(x=0.60, y=0.42, z=0.0, visibility=visibility)
    landmarks[13] = SimpleNamespace(x=0.35, y=0.55, z=0.0, visibility=visibility)
    landmarks[14] = SimpleNamespace(x=0.65, y=0.55, z=0.0, visibility=visibility)
    landmarks[15] = SimpleNamespace(x=0.30, y=0.70, z=0.0, visibility=visibility)
    landmarks[16] = SimpleNamespace(x=0.70, y=0.70, z=0.0, visibility=visibility)
    landmarks[19] = SimpleNamespace(x=0.29, y=0.72, z=0.0, visibility=visibility)
    landmarks[20] = SimpleNamespace(x=0.71, y=0.72, z=0.0, visibility=visibility)
    landmarks[23] = SimpleNamespace(x=0.42, y=0.72, z=0.0, visibility=visibility)
    landmarks[24] = SimpleNamespace(x=0.58, y=0.72, z=0.0, visibility=visibility)
    return landmarks


def classify(landmarks):
    return classify_posture_rule_based(extract_posture_features(landmarks))


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    without_marks = "".join(char for char in normalized if unicodedata.category(char) != "Mn")
    return without_marks.replace("đ", "d").replace("Đ", "D").lower()


def test_rule_based_correct_posture():
    status, warnings = classify(make_landmarks())
    assert status == "CORRECT"
    assert warnings == []


def test_rule_based_shoulder_tilt_incorrect():
    landmarks = make_landmarks()
    landmarks[12].y = 0.55
    status, warnings = classify(landmarks)
    assert status == "INCORRECT"
    assert any("vai" in warning.lower() for warning in warnings)


def test_rule_based_head_offset_incorrect():
    landmarks = make_landmarks()
    landmarks[0].x = 0.75
    status, warnings = classify(landmarks)
    assert status == "INCORRECT"
    assert any("dau" in normalize_text(warning) for warning in warnings)


def test_rule_based_moderate_neck_compression_still_correct():
    landmarks = make_landmarks()
    landmarks[0].y = 0.38
    features = extract_posture_features(landmarks)
    status, warnings = classify_posture_rule_based(features)
    assert features["nose_to_shoulder_y"] == pytest.approx(-0.04)
    assert features["nose_shoulder_clearance_ratio"] > 0.12
    assert status == "CORRECT"
    assert warnings == []


def test_rule_based_deep_neck_compression_incorrect():
    landmarks = make_landmarks()
    landmarks[0].y = 0.405
    features = extract_posture_features(landmarks)
    status, warnings = classify_posture_rule_based(features)
    assert features["nose_to_shoulder_y"] == pytest.approx(-0.015)
    assert features["nose_shoulder_clearance_ratio"] < 0.12
    assert features["neck_compression_detected"] is True
    assert status == "INCORRECT"
    assert any("rut co" in normalize_text(warning) for warning in warnings)


def test_rule_based_hand_near_mouth_incorrect():
    landmarks = make_landmarks()
    landmarks[15].x = 0.50
    landmarks[15].y = 0.36
    status, warnings = classify(landmarks)
    assert status == "INCORRECT"
    assert any("tay" in warning.lower() for warning in warnings)


def test_rule_based_low_visibility_no_person():
    status, warnings = classify(make_landmarks(visibility=0.1))
    assert status == "NO_PERSON_OR_LOW_CONFIDENCE"
    assert warnings == []
