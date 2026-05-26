import math
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from utils import calculate_angle


def test_calculate_angle_90_degrees():
    angle = calculate_angle((1, 0), (0, 0), (0, 1))
    assert math.isclose(angle, 90.0, abs_tol=1e-6)


def test_calculate_angle_180_degrees():
    angle = calculate_angle((-1, 0), (0, 0), (1, 0))
    assert math.isclose(angle, 180.0, abs_tol=1e-6)


def test_calculate_angle_zero_length_vector_returns_zero():
    assert calculate_angle((0, 0), (0, 0), (1, 0)) == 0.0


def test_calculate_angle_invalid_input_returns_zero():
    assert calculate_angle(None, (0, 0), (1, 0)) == 0.0
