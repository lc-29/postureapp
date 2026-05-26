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


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = BASE_DIR / "dataset" / "posture_data_2fps.csv"
DEFAULT_OUTPUT = BASE_DIR / "reports" / "results" / "ablation_results.csv"
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


def evaluate_group(name: str, df: pd.DataFrame, columns: list[str]) -> dict[str, object]:
    X = df[columns].astype(np.float32)
    y = df["label"].astype(int)
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
        "feature_count": len(columns),
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, pos_label=1, zero_division=0),
        "recall": recall_score(y_test, y_pred, pos_label=1, zero_division=0),
        "f1": f1_score(y_test, y_pred, pos_label=1, zero_division=0),
    }


def run(args: argparse.Namespace) -> None:
    dataset_path = Path(args.dataset)
    output_path = Path(args.output)
    if not dataset_path.is_absolute():
        dataset_path = BASE_DIR / dataset_path
    if not output_path.is_absolute():
        output_path = BASE_DIR / output_path

    df = pd.read_csv(dataset_path).dropna().reset_index(drop=True)
    if args.max_rows is not None:
        df = df.sample(n=min(args.max_rows, len(df)), random_state=SEED).reset_index(drop=True)

    rows = [
        evaluate_group("all_33_landmarks", df, landmark_columns(df)),
        evaluate_group("head_shoulders_hips_hands", df, landmark_columns(df, CORE_LANDMARKS)),
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output_path, index=False)
    print(pd.DataFrame(rows).to_string(index=False))
    print(f"Saved: {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a small landmark feature ablation study.")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--max-rows", type=int, default=None)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())
