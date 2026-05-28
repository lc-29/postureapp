import importlib.util
import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
MODULE_PATH = SRC_DIR / "16_build_ergonomic_features.py"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

spec = importlib.util.spec_from_file_location("build_ergonomic_features", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["build_ergonomic_features"] = module
spec.loader.exec_module(module)


def make_row() -> pd.Series:
    data = {}
    for index in range(33):
        data[f"landmark_{index}_x"] = 0.5
        data[f"landmark_{index}_y"] = 0.5
        data[f"landmark_{index}_z"] = 0.0
    data.update(
        {
            "landmark_0_x": 0.50,
            "landmark_0_y": 0.33,
            "landmark_9_x": 0.48,
            "landmark_9_y": 0.36,
            "landmark_10_x": 0.52,
            "landmark_10_y": 0.36,
            "landmark_11_x": 0.40,
            "landmark_11_y": 0.42,
            "landmark_12_x": 0.60,
            "landmark_12_y": 0.42,
            "landmark_23_x": 0.42,
            "landmark_23_y": 0.72,
            "landmark_24_x": 0.58,
            "landmark_24_y": 0.72,
        }
    )
    return pd.Series(data)


def test_compute_ergonomic_row_contains_expected_features():
    features = module.compute_ergonomic_row(make_row())

    for column in module.ERGONOMIC_FEATURE_COLUMNS:
        assert column in features
    assert features["shoulder_width"] > 0
    assert features["torso_length"] > 0
    assert features["neck_compression_detected"] in {0, 1}
