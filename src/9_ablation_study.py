"""Small ablation study for landmark feature groups."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from posture_baseline import extract_posture_features, landmarks_from_feature_row


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = BASE_DIR / "dataset" / "posture_data_2fps.csv"
DEFAULT_OUTPUT = BASE_DIR / "reports" / "results" / "ablation_results.csv"
DEFAULT_FULL_OUTPUT = BASE_DIR / "reports" / "results" / "ablation_full.csv"
SEED = 42
CORE_LANDMARKS = [0, 9, 10, 11, 12, 13, 14, 15, 16, 23, 24]


def landmark_columns(df: pd.DataFrame, indexes: list[int] | None = None) -> list[str]:
    columns: list[str] = []
    selected = indexes if indexes is not None else list(range(33))
    for index in selected:
        columns.extend([f"landmark_{index}_x", f"landmark_{index}_y", f"landmark_{index}_z"])
    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise ValueError(f"Missing landmark columns: {missing[:5]}")
    return columns


def normalized_landmark_dataframe(df: pd.DataFrame, indexes: list[int] | None = None) -> pd.DataFrame:
    """Normalize landmarks theo mid-shoulder va shoulder width."""
    selected = indexes if indexes is not None else list(range(33))
    rows: list[dict[str, float]] = []
    eps = 1e-6
    for _, row in df.iterrows():
        left_shoulder = np.array(
            [
                row["landmark_11_x"],
                row["landmark_11_y"],
                row["landmark_11_z"],
            ],
            dtype=np.float32,
        )
        right_shoulder = np.array(
            [
                row["landmark_12_x"],
                row["landmark_12_y"],
                row["landmark_12_z"],
            ],
            dtype=np.float32,
        )
        center = (left_shoulder + right_shoulder) / 2.0
        scale = float(np.linalg.norm(left_shoulder - right_shoulder))
        if scale < eps:
            left_hip = np.array(
                [row["landmark_23_x"], row["landmark_23_y"], row["landmark_23_z"]],
                dtype=np.float32,
            )
            right_hip = np.array(
                [row["landmark_24_x"], row["landmark_24_y"], row["landmark_24_z"]],
                dtype=np.float32,
            )
            scale = float(np.linalg.norm(center - ((left_hip + right_hip) / 2.0)))
        scale = max(scale, eps)

        normalized_row: dict[str, float] = {}
        for index in selected:
            point = np.array(
                [
                    row[f"landmark_{index}_x"],
                    row[f"landmark_{index}_y"],
                    row[f"landmark_{index}_z"],
                ],
                dtype=np.float32,
            )
            normalized = (point - center) / scale
            normalized_row[f"norm_landmark_{index}_x"] = float(normalized[0])
            normalized_row[f"norm_landmark_{index}_y"] = float(normalized[1])
            normalized_row[f"norm_landmark_{index}_z"] = float(normalized[2])
        rows.append(normalized_row)
    return pd.DataFrame(rows)


def ergonomic_feature_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Tao bang feature giai thich tu posture_baseline."""
    keys = [
        "visibility",
        "shoulder_y_diff",
        "shoulder_tilt_angle",
        "torso_lean_angle",
        "head_offset_x",
        "nose_to_shoulder_y",
        "nose_shoulder_clearance",
        "nose_shoulder_clearance_ratio",
        "mouth_to_left_hand_ratio",
        "mouth_to_right_hand_ratio",
        "mouth_to_left_hand_distance",
        "mouth_to_right_hand_distance",
    ]
    rows: list[dict[str, float]] = []
    for _, row in df.iterrows():
        features = extract_posture_features(landmarks_from_feature_row(row))
        rows.append({key: float(features.get(key, 0.0) or 0.0) for key in keys})
    return pd.DataFrame(rows)


def evaluate_group(name: str, X: pd.DataFrame, y: pd.Series) -> dict[str, object]:
    X = X.astype(np.float32)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=SEED,
        stratify=y,
    )
    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, random_state=SEED)),
        ]
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return {
        "feature_group": name,
        "feature_count": X.shape[1],
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, pos_label=1, zero_division=0),
        "recall": recall_score(y_test, y_pred, pos_label=1, zero_division=0),
        "f1": f1_score(y_test, y_pred, pos_label=1, zero_division=0),
    }


def run(args: argparse.Namespace) -> None:
    dataset_path = Path(args.dataset)
    output_path = Path(args.output)
    full_output_path = Path(args.full_output)
    if not dataset_path.is_absolute():
        dataset_path = BASE_DIR / dataset_path
    if not output_path.is_absolute():
        output_path = BASE_DIR / output_path
    if not full_output_path.is_absolute():
        full_output_path = BASE_DIR / full_output_path

    df = pd.read_csv(dataset_path).reset_index(drop=True)
    raw_columns = landmark_columns(df)
    df = df.dropna(subset=raw_columns + ["label"]).reset_index(drop=True)
    if args.max_rows is not None:
        df = df.sample(n=min(args.max_rows, len(df)), random_state=SEED).reset_index(drop=True)

    y = df["label"].astype(int)
    raw_all = df[raw_columns]
    raw_core = df[landmark_columns(df, CORE_LANDMARKS)]
    normalized_all = normalized_landmark_dataframe(df)
    normalized_core = normalized_landmark_dataframe(df, CORE_LANDMARKS)
    ergonomic = ergonomic_feature_dataframe(df)

    rows = [
        evaluate_group("raw_all_33_landmarks", raw_all, y),
        evaluate_group("raw_head_shoulders_hips_hands", raw_core, y),
        evaluate_group("normalized_all_33_landmarks", normalized_all, y),
        evaluate_group("normalized_head_shoulders_hips_hands", normalized_core, y),
        evaluate_group("ergonomic_indicators", ergonomic, y),
        evaluate_group(
            "normalized_plus_ergonomic",
            pd.concat([normalized_core.reset_index(drop=True), ergonomic.reset_index(drop=True)], axis=1),
            y,
        ),
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df = pd.DataFrame(rows).sort_values("f1", ascending=False)
    results_df.head(2).to_csv(output_path, index=False)
    results_df.to_csv(full_output_path, index=False)
    print(results_df.to_string(index=False))
    print(f"Saved: {output_path}")
    print(f"Saved: {full_output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a small landmark feature ablation study.")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--full-output", default=str(DEFAULT_FULL_OUTPUT))
    parser.add_argument("--max-rows", type=int, default=None)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())
