import importlib.util
import sys
import unicodedata
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

MODULE_PATH = SRC_DIR / "8_compare_algorithms.py"
spec = importlib.util.spec_from_file_location("compare_algorithms", MODULE_PATH)
compare_algorithms = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["compare_algorithms"] = compare_algorithms
spec.loader.exec_module(compare_algorithms)

from posture_baseline import classify_posture_rule_based, extract_posture_features


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    without_marks = "".join(char for char in normalized if unicodedata.category(char) != "Mn")
    return without_marks.replace("đ", "d").replace("Đ", "D").lower()


def make_feature_row(nose_y: float = 0.33) -> pd.Series:
    data = {}
    for index in range(33):
        data[f"landmark_{index}_x"] = 0.5
        data[f"landmark_{index}_y"] = 0.5
        data[f"landmark_{index}_z"] = 0.0

    data.update(
        {
            "landmark_0_x": 0.50,
            "landmark_0_y": nose_y,
            "landmark_9_x": 0.48,
            "landmark_9_y": 0.36,
            "landmark_10_x": 0.52,
            "landmark_10_y": 0.36,
            "landmark_11_x": 0.40,
            "landmark_11_y": 0.42,
            "landmark_12_x": 0.60,
            "landmark_12_y": 0.42,
            "landmark_13_x": 0.35,
            "landmark_13_y": 0.55,
            "landmark_14_x": 0.65,
            "landmark_14_y": 0.55,
            "landmark_15_x": 0.30,
            "landmark_15_y": 0.70,
            "landmark_16_x": 0.70,
            "landmark_16_y": 0.70,
            "landmark_19_x": 0.29,
            "landmark_19_y": 0.72,
            "landmark_20_x": 0.71,
            "landmark_20_y": 0.72,
            "landmark_23_x": 0.42,
            "landmark_23_y": 0.72,
            "landmark_24_x": 0.58,
            "landmark_24_y": 0.72,
            "label": 0,
        }
    )
    return pd.Series(data)


def test_compare_algorithms_can_reconstruct_landmarks_after_baseline_change():
    row = make_feature_row(nose_y=0.405)
    df = pd.DataFrame([row])
    assert len(compare_algorithms.feature_columns(df)) == 99

    landmarks = compare_algorithms.landmarks_from_feature_row(row)
    features = extract_posture_features(landmarks)
    status, warnings = classify_posture_rule_based(features)

    assert status == "INCORRECT"
    assert features["neck_compression_detected"] is True
    assert any("rut co" in normalize_text(warning) for warning in warnings)
