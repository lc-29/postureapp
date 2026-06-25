from __future__ import annotations

import pandas as pd

from src.feature_schema import (
    ERGONOMIC_FEATURE_COLUMNS,
    build_feature_matrix,
    compute_ergonomic_features,
    compute_normalized_landmarks,
)


def make_pose_df() -> pd.DataFrame:
    row = {}
    for index in range(33):
        row[f"landmark_{index}_x"] = 0.5 + index * 0.002
        row[f"landmark_{index}_y"] = 0.5 + index * 0.003
        row[f"landmark_{index}_z"] = index * 0.001
    row["landmark_11_x"] = 0.4
    row["landmark_11_y"] = 0.5
    row["landmark_12_x"] = 0.6
    row["landmark_12_y"] = 0.5
    row["landmark_23_x"] = 0.42
    row["landmark_23_y"] = 0.8
    row["landmark_24_x"] = 0.58
    row["landmark_24_y"] = 0.8
    row["label"] = 0
    return pd.DataFrame([row])


def test_normalized_landmarks_shape() -> None:
    normalized = compute_normalized_landmarks(make_pose_df())
    assert normalized.shape == (1, 99)
    assert "norm_landmark_0_x" in normalized.columns


def test_ergonomic_features_shape() -> None:
    ergonomic = compute_ergonomic_features(make_pose_df())
    assert ergonomic.shape == (1, len(ERGONOMIC_FEATURE_COLUMNS))
    assert set(ERGONOMIC_FEATURE_COLUMNS).issubset(ergonomic.columns)


def test_build_combined_normalized_ergonomic_matrix() -> None:
    matrix, columns = build_feature_matrix(make_pose_df(), "combined_normalized_ergonomic")
    assert matrix.shape == (1, 113)
    assert len(columns) == 113
    assert "norm_landmark_0_x" in columns
    assert "torso_lean_angle" in columns

