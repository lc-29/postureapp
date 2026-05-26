import importlib.util
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "src" / "12_temporal_risk_index.py"
spec = importlib.util.spec_from_file_location("temporal_risk_index", MODULE_PATH)
temporal_risk_index = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["temporal_risk_index"] = temporal_risk_index
spec.loader.exec_module(temporal_risk_index)


def test_compute_risk_score_uses_configured_weights():
    weights = temporal_risk_index.RiskWeights()
    score = temporal_risk_index.compute_risk_score(
        incorrect_time_ratio=0.5,
        long_bad_posture_ratio=0.4,
        warning_rate_norm=0.3,
        no_person_or_low_confidence_ratio=0.2,
        weights=weights,
    )
    assert score == 39.0


def test_risk_weights_must_sum_to_one():
    weights = temporal_risk_index.RiskWeights(
        incorrect_time=0.5,
        long_bad_posture=0.25,
        warning_rate=0.2,
        no_person=0.15,
    )
    with pytest.raises(ValueError):
        weights.validate()


def test_long_bad_posture_counts_only_long_incorrect_segments():
    logs = pd.DataFrame(
        [
            {"thoiDiem": "2026-05-26T10:00:00", "trangThai": "DUNG_TU_THE"},
            {"thoiDiem": "2026-05-26T10:00:02", "trangThai": "SAI_TU_THE"},
            {"thoiDiem": "2026-05-26T10:00:05", "trangThai": "DUNG_TU_THE"},
            {"thoiDiem": "2026-05-26T10:00:08", "trangThai": "SAI_TU_THE"},
            {"thoiDiem": "2026-05-26T10:00:18", "trangThai": "DUNG_TU_THE"},
        ]
    )
    seconds = temporal_risk_index.estimate_long_bad_posture_seconds(
        logs,
        session_start=datetime.fromisoformat("2026-05-26T10:00:00"),
        session_end=datetime.fromisoformat("2026-05-26T10:00:20"),
        min_bad_segment_seconds=5.0,
    )
    assert seconds == 10.0


def test_warning_rate_norm_is_capped():
    norm = temporal_risk_index.compute_warning_rate_norm(
        warning_count=10,
        duration_seconds=60.0,
        warning_rate_cap_per_hour=12.0,
    )
    assert norm == 1.0


def test_risk_level_boundaries():
    assert temporal_risk_index.risk_level(24.99) == "LOW"
    assert temporal_risk_index.risk_level(25.0) == "MEDIUM"
    assert temporal_risk_index.risk_level(50.0) == "HIGH"
    assert temporal_risk_index.risk_level(75.0) == "CRITICAL"
