"""Compare ANN and rule-based baseline on a landmark CSV."""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from posture_baseline import (
    classify_posture_rule_based,
    extract_posture_features,
    landmarks_from_feature_row,
)


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = BASE_DIR / "dataset" / "posture_external_test_2fps.csv"
DEFAULT_TRAIN_DATASET = BASE_DIR / "dataset" / "posture_data_2fps.csv"
DEFAULT_MODEL = BASE_DIR / "models" / "ann_best.keras"
DEFAULT_SCALER = BASE_DIR / "models" / "scaler.pkl"
DEFAULT_OUTPUT = BASE_DIR / "reports" / "results" / "algorithm_comparison.csv"
DEFAULT_FULL_OUTPUT = BASE_DIR / "reports" / "results" / "algorithm_benchmark_full.csv"
NUM_FEATURES = 99
SEED = 42


def feature_columns(df: pd.DataFrame) -> list[str]:
    columns = [
        column
        for column in df.columns
        if column.startswith("landmark_") and column.rsplit("_", 1)[-1] in {"x", "y", "z"}
    ]
    if len(columns) != NUM_FEATURES:
        raise ValueError(f"Expected {NUM_FEATURES} landmark features, found {len(columns)}.")
    return columns


def metric_row(
    name: str,
    dataset: str,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_score: np.ndarray | None = None,
    train_seconds: float | None = None,
    predict_seconds: float | None = None,
    note: str = "",
) -> dict[str, object]:
    roc_auc = ""
    pr_auc = ""
    if y_score is not None and len(set(y_true.tolist())) == 2:
        roc_auc = roc_auc_score(y_true, y_score)
        pr_auc = average_precision_score(y_true, y_score)
    return {
        "algorithm": name,
        "dataset": dataset,
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
        "recall": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
        "f1": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "mcc": matthews_corrcoef(y_true, y_pred),
        "roc_auc": roc_auc,
        "pr_auc": pr_auc,
        "train_seconds": "" if train_seconds is None else round(train_seconds, 3),
        "predict_seconds": "" if predict_seconds is None else round(predict_seconds, 3),
        "note": note,
    }


def predict_scores(model: object, X: pd.DataFrame | np.ndarray) -> np.ndarray | None:
    if hasattr(model, "predict_proba"):
        return np.asarray(model.predict_proba(X))[:, 1]
    if hasattr(model, "decision_function"):
        decision = np.asarray(model.decision_function(X))
        return 1.0 / (1.0 + np.exp(-decision))
    return None


def compare(args: argparse.Namespace) -> None:
    train_path = Path(args.train_dataset)
    dataset_path = Path(args.dataset)
    model_path = Path(args.model)
    scaler_path = Path(args.scaler)
    output_path = Path(args.output)
    full_output_path = Path(args.full_output)
    if not train_path.is_absolute():
        train_path = BASE_DIR / train_path
    if not dataset_path.is_absolute():
        dataset_path = BASE_DIR / dataset_path
    if not model_path.is_absolute():
        model_path = BASE_DIR / model_path
    if not scaler_path.is_absolute():
        scaler_path = BASE_DIR / scaler_path
    if not output_path.is_absolute():
        output_path = BASE_DIR / output_path
    if not full_output_path.is_absolute():
        full_output_path = BASE_DIR / full_output_path

    train_df = pd.read_csv(train_path).reset_index(drop=True)
    df = pd.read_csv(dataset_path).reset_index(drop=True)
    train_columns = feature_columns(train_df)
    columns = feature_columns(df)
    train_df = train_df.dropna(subset=train_columns + ["label"]).reset_index(drop=True)
    df = df.dropna(subset=columns + ["label"]).reset_index(drop=True)
    X_train = train_df[train_columns].astype(np.float32)
    y_train = train_df["label"].astype(int).to_numpy()
    X_external = df[columns].astype(np.float32)
    y_true = df["label"].astype(int).to_numpy()

    model = tf.keras.models.load_model(model_path)
    scaler = joblib.load(scaler_path)
    X_scaled = scaler.transform(X_external)
    ann_start = time.perf_counter()
    ann_prob = model.predict(X_scaled, verbose=0).ravel()
    ann_predict_seconds = time.perf_counter() - ann_start
    ann_pred = (ann_prob >= args.threshold).astype(int)

    baseline_pred = []
    for _, row in df.iterrows():
        landmarks = landmarks_from_feature_row(row)
        features = extract_posture_features(landmarks)
        status, _ = classify_posture_rule_based(features)
        baseline_pred.append(1 if status == "INCORRECT" else 0)
    baseline_pred_array = np.array(baseline_pred, dtype=int)

    rows = [
        metric_row(
            "ANN",
            dataset_path.name,
            y_true,
            ann_pred,
            y_score=ann_prob,
            predict_seconds=ann_predict_seconds,
            note=f"loaded keras model, threshold={args.threshold}",
        ),
        metric_row(
            "Rule-based",
            dataset_path.name,
            y_true,
            baseline_pred_array,
            note="interpretable ergonomic baseline",
        ),
    ]

    benchmark_models: list[tuple[str, object]] = [
        (
            "Logistic Regression",
            Pipeline(
                [
                    ("scaler", StandardScaler()),
                    (
                        "classifier",
                        LogisticRegression(max_iter=1000, class_weight="balanced", random_state=SEED),
                    ),
                ]
            ),
        ),
        (
            "KNN",
            Pipeline(
                [
                    ("scaler", StandardScaler()),
                    ("classifier", KNeighborsClassifier(n_neighbors=7)),
                ]
            ),
        ),
        (
            "SVM RBF",
            Pipeline(
                [
                    ("scaler", StandardScaler()),
                    (
                        "classifier",
                        SVC(kernel="rbf", C=3.0, gamma="scale", probability=True, class_weight="balanced"),
                    ),
                ]
            ),
        ),
        (
            "Random Forest",
            RandomForestClassifier(
                n_estimators=250,
                class_weight="balanced",
                random_state=SEED,
                n_jobs=-1,
            ),
        ),
        (
            "HistGradientBoosting",
            HistGradientBoostingClassifier(max_iter=200, random_state=SEED),
        ),
    ]

    for name, candidate in benchmark_models:
        train_start = time.perf_counter()
        candidate.fit(X_train, y_train)
        train_seconds = time.perf_counter() - train_start

        predict_start = time.perf_counter()
        candidate_pred = candidate.predict(X_external)
        candidate_score = predict_scores(candidate, X_external)
        predict_seconds = time.perf_counter() - predict_start

        rows.append(
            metric_row(
                name,
                dataset_path.name,
                y_true,
                np.asarray(candidate_pred, dtype=int),
                y_score=candidate_score,
                train_seconds=train_seconds,
                predict_seconds=predict_seconds,
                note="trained on current train CSV, evaluated on external CSV",
            )
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df = pd.DataFrame(rows)
    results_df[results_df["algorithm"].isin(["ANN", "Rule-based"])].to_csv(output_path, index=False)
    results_df.sort_values("f1", ascending=False).to_csv(full_output_path, index=False)
    print(results_df.sort_values("f1", ascending=False).to_string(index=False))
    print(f"Saved: {output_path}")
    print(f"Saved: {full_output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare ANN and rule-based baseline.")
    parser.add_argument("--train-dataset", default=str(DEFAULT_TRAIN_DATASET))
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--model", default=str(DEFAULT_MODEL))
    parser.add_argument("--scaler", default=str(DEFAULT_SCALER))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--full-output", default=str(DEFAULT_FULL_OUTPUT))
    parser.add_argument("--threshold", type=float, default=0.5)
    return parser.parse_args()


if __name__ == "__main__":
    compare(parse_args())
