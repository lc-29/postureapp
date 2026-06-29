"""Run the full external benchmark protocol on P06/P07.

Protocol:
- Train learned models on the development set (P01-P05).
- Evaluate once on the external set (P06-P07).
- Evaluate the rule-based baseline on the same external set without training.

The script writes separate artifacts under reports/results, reports/figures,
and reports/FULL_PROTOCOL_MODEL_BENCHMARK_EXTERNAL_P06P07_REPORT.md.
It does not update the application model registry.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import joblib
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils.class_weight import compute_class_weight, compute_sample_weight

try:
    import tensorflow as tf
    from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
    from tensorflow.keras.layers import BatchNormalization, Dense, Dropout, Input
    from tensorflow.keras.models import Sequential
except Exception:  # pragma: no cover - handled in runtime report
    tf = None
    EarlyStopping = None
    ReduceLROnPlateau = None
    BatchNormalization = None
    Dense = None
    Dropout = None
    Input = None
    Sequential = None

try:
    from feature_schema import build_feature_matrix
    from posture_baseline import (
        classify_posture_rule_based,
        extract_posture_features,
        landmarks_from_feature_row,
    )
except ImportError:
    from src.feature_schema import build_feature_matrix
    from src.posture_baseline import (
        classify_posture_rule_based,
        extract_posture_features,
        landmarks_from_feature_row,
    )


BASE_DIR = Path(__file__).resolve().parents[1]
TRAIN_PATH = BASE_DIR / "dataset" / "processed" / "posture_data_2fps_with_metadata.csv"
EXTERNAL_PATH = BASE_DIR / "dataset" / "processed" / "posture_external_test_2fps_with_metadata.csv"
RESULTS_DIR = BASE_DIR / "reports" / "results"
FIGURES_DIR = BASE_DIR / "reports" / "figures"
MODEL_DIR = BASE_DIR / "models" / "full_protocol_benchmark"
REPORT_PATH = BASE_DIR / "reports" / "FULL_PROTOCOL_MODEL_BENCHMARK_EXTERNAL_P06P07_REPORT.md"
SEED = 42

DEFAULT_FEATURE_SETS = [
    "raw_99",
    "normalized_99",
    "ergonomic_14",
    "ergonomic_v2",
    "ergonomic_v2_with_view",
    "combined_v2",
    "combined_v2_with_view",
]

METADATA_COLUMNS = [
    "source_video",
    "frame_index",
    "timestamp_sec",
    "sample_fps",
    "video_fps",
    "participant_id",
    "view_angle",
    "camera_type",
]


@dataclass
class Candidate:
    model_id: str
    algorithm: str
    algorithm_family: str
    feature_set: str
    class_weight: str
    threshold_source: str
    model: Any
    columns: list[str]
    y_true: np.ndarray
    y_score: np.ndarray
    train_seconds: float
    predict_seconds: float


def set_seeds() -> None:
    np.random.seed(SEED)
    if tf is not None:
        tf.random.set_seed(SEED)


def ensure_dirs() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)


def clean_model_id(text: str) -> str:
    return (
        text.lower()
        .replace("/", "_")
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .replace(".", "_")
    )


def safe_auc(y_true: np.ndarray, y_score: np.ndarray, kind: str) -> float:
    if len(np.unique(y_true)) < 2:
        return float("nan")
    try:
        if kind == "roc":
            return float(roc_auc_score(y_true, y_score))
        if kind == "pr":
            return float(average_precision_score(y_true, y_score))
    except ValueError:
        return float("nan")
    raise ValueError(kind)


def metric_row(
    y_true: np.ndarray,
    y_score: np.ndarray,
    threshold: float,
    prefix: dict[str, Any],
) -> dict[str, Any]:
    y_pred = (y_score >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    row = {
        "threshold": float(threshold),
        "accuracy": accuracy_score(y_true, y_pred),
        "precision_incorrect": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
        "recall_incorrect": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
        "f1_incorrect": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "mcc": matthews_corrcoef(y_true, y_pred),
        "roc_auc": safe_auc(y_true, y_score, "roc"),
        "pr_auc": safe_auc(y_true, y_score, "pr"),
        "true_negative": int(tn),
        "false_positive": int(fp),
        "false_negative": int(fn),
        "true_positive": int(tp),
        "n_test": int(len(y_true)),
    }
    row.update(prefix)
    return row


def predict_scores(model: Any, x: pd.DataFrame | np.ndarray) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(x)
        return np.asarray(proba)[:, 1].astype(float)
    if hasattr(model, "decision_function"):
        decision = np.asarray(model.decision_function(x), dtype=float)
        return 1.0 / (1.0 + np.exp(-decision))
    pred = np.asarray(model.predict(x), dtype=float)
    return pred.reshape(-1)


def make_sklearn_model(algorithm: str, class_weight: str) -> Any:
    weight = None if class_weight == "none" else "balanced"
    if algorithm == "logistic_regression":
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(max_iter=1500, class_weight=weight, random_state=SEED)),
            ]
        )
    if algorithm == "svm_rbf":
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "model",
                    SVC(
                        kernel="rbf",
                        C=3.0,
                        gamma="scale",
                        probability=False,
                        class_weight=weight,
                        random_state=SEED,
                    ),
                ),
            ]
        )
    if algorithm == "knn":
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", KNeighborsClassifier(n_neighbors=7, weights="distance")),
            ]
        )
    if algorithm == "decision_tree":
        return DecisionTreeClassifier(max_depth=8, min_samples_leaf=20, class_weight=weight, random_state=SEED)
    if algorithm == "random_forest":
        return RandomForestClassifier(
            n_estimators=350,
            max_depth=None,
            min_samples_leaf=2,
            class_weight=weight,
            random_state=SEED,
            n_jobs=-1,
        )
    if algorithm == "mlp_sklearn":
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "model",
                    MLPClassifier(
                        hidden_layer_sizes=(96, 48),
                        activation="relu",
                        alpha=1e-4,
                        early_stopping=True,
                        max_iter=220,
                        random_state=SEED,
                    ),
                ),
            ]
        )
    if algorithm == "hist_gradient_boosting":
        return HistGradientBoostingClassifier(max_iter=250, learning_rate=0.06, random_state=SEED)
    raise ValueError(f"Unsupported algorithm: {algorithm}")


def algorithm_family(algorithm: str) -> str:
    return {
        "logistic_regression": "Logistic Regression",
        "svm_rbf": "SVM RBF",
        "knn": "KNN",
        "decision_tree": "Decision Tree",
        "random_forest": "Random Forest",
        "mlp_sklearn": "MLPClassifier",
        "hist_gradient_boosting": "HistGradientBoosting",
        "ann_keras": "ANN/Keras",
        "rule_based": "Rule-based Baseline",
    }[algorithm]


def class_weight_options(algorithm: str) -> list[str]:
    if algorithm in {"logistic_regression", "svm_rbf", "decision_tree", "random_forest"}:
        return ["none", "balanced"]
    if algorithm == "hist_gradient_boosting":
        return ["none", "balanced_sample_weight"]
    return ["none"]


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    train_df = pd.read_csv(TRAIN_PATH).reset_index(drop=True)
    external_df = pd.read_csv(EXTERNAL_PATH).reset_index(drop=True)
    return train_df, external_df


def split_check(train_df: pd.DataFrame, external_df: pd.DataFrame) -> dict[str, Any]:
    train_participants = sorted(train_df["participant_id"].astype(str).unique().tolist())
    external_participants = sorted(external_df["participant_id"].astype(str).unique().tolist())
    train_videos = set(train_df["source_video"].astype(str).unique().tolist())
    external_videos = set(external_df["source_video"].astype(str).unique().tolist())
    overlap = sorted(train_videos.intersection(external_videos))
    return {
        "train_rows": int(len(train_df)),
        "external_rows": int(len(external_df)),
        "train_videos": int(train_df["source_video"].nunique()),
        "external_videos": int(external_df["source_video"].nunique()),
        "train_participants": train_participants,
        "external_participants": external_participants,
        "train_label_counts": {str(k): int(v) for k, v in train_df["label"].value_counts().sort_index().items()},
        "external_label_counts": {str(k): int(v) for k, v in external_df["label"].value_counts().sort_index().items()},
        "source_video_overlap_count": int(len(overlap)),
        "source_video_overlap_examples": overlap[:10],
        "train_only_p01_p05": set(train_participants).issubset({"P01", "P02", "P03", "P04", "P05"}),
        "external_only_p06_p07": set(external_participants) == {"P06", "P07"},
        "participant_disjoint": set(train_participants).isdisjoint(set(external_participants)),
        "source_video_disjoint": len(overlap) == 0,
    }


def feature_data(
    train_df: pd.DataFrame,
    external_df: pd.DataFrame,
    feature_set: str,
) -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    x_train, columns = build_feature_matrix(train_df, feature_set)
    x_external, external_columns = build_feature_matrix(external_df, feature_set)
    if columns != external_columns:
        raise ValueError(f"Feature columns mismatch for {feature_set}")
    x_train = x_train.replace([np.inf, -np.inf], np.nan).fillna(0.0).astype(np.float32)
    x_external = x_external.replace([np.inf, -np.inf], np.nan).fillna(0.0).astype(np.float32)
    return x_train, x_external, columns


def train_sklearn_candidates(
    train_df: pd.DataFrame,
    external_df: pd.DataFrame,
    feature_sets: list[str],
) -> tuple[pd.DataFrame, list[Candidate]]:
    algorithms = [
        "logistic_regression",
        "svm_rbf",
        "knn",
        "decision_tree",
        "random_forest",
        "mlp_sklearn",
        "hist_gradient_boosting",
    ]
    y_train = train_df["label"].astype(int).to_numpy()
    y_external = external_df["label"].astype(int).to_numpy()
    rows: list[dict[str, Any]] = []
    candidates: list[Candidate] = []

    for feature_set in feature_sets:
        x_train, x_external, columns = feature_data(train_df, external_df, feature_set)
        for algorithm in algorithms:
            for class_weight in class_weight_options(algorithm):
                model_id = f"{algorithm}_{class_weight}__{feature_set}"
                model = make_sklearn_model(algorithm, class_weight)
                start = time.perf_counter()
                if algorithm == "hist_gradient_boosting" and class_weight == "balanced_sample_weight":
                    model.fit(x_train, y_train, sample_weight=compute_sample_weight("balanced", y_train))
                else:
                    model.fit(x_train, y_train)
                train_seconds = time.perf_counter() - start

                start = time.perf_counter()
                y_score = predict_scores(model, x_external)
                predict_seconds = time.perf_counter() - start

                prefix = {
                    "model_id": model_id,
                    "algorithm": algorithm,
                    "algorithm_family": algorithm_family(algorithm),
                    "feature_set": feature_set,
                    "class_weight": class_weight,
                    "threshold_source": "default_0_50",
                    "feature_count": len(columns),
                    "train_seconds": round(train_seconds, 4),
                    "predict_seconds": round(predict_seconds, 4),
                }
                row = metric_row(y_external, y_score, 0.5, prefix)
                rows.append(row)
                candidates.append(
                    Candidate(
                        model_id=model_id,
                        algorithm=algorithm,
                        algorithm_family=algorithm_family(algorithm),
                        feature_set=feature_set,
                        class_weight=class_weight,
                        threshold_source="default_0_50",
                        model=model,
                        columns=columns,
                        y_true=y_external,
                        y_score=y_score,
                        train_seconds=train_seconds,
                        predict_seconds=predict_seconds,
                    )
                )
                print(
                    f"{model_id}: acc={row['accuracy']:.4f} "
                    f"f1={row['f1_incorrect']:.4f} fp={row['false_positive']} fn={row['false_negative']}"
                )
    return pd.DataFrame(rows), candidates


def build_keras_model(input_dim: int) -> Any:
    if Sequential is None:
        raise RuntimeError("TensorFlow/Keras is not available.")
    model = Sequential(
        [
            Input(shape=(input_dim,)),
            Dense(128, activation="relu"),
            BatchNormalization(),
            Dropout(0.30),
            Dense(64, activation="relu"),
            BatchNormalization(),
            Dropout(0.25),
            Dense(32, activation="relu"),
            Dropout(0.20),
            Dense(1, activation="sigmoid"),
        ]
    )
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss="binary_crossentropy",
        metrics=[
            "accuracy",
            tf.keras.metrics.Precision(name="precision"),
            tf.keras.metrics.Recall(name="recall"),
        ],
    )
    return model


def keras_class_weight(y_train: np.ndarray) -> dict[int, float]:
    weights = compute_class_weight(class_weight="balanced", classes=np.array([0, 1]), y=y_train)
    return {0: float(weights[0]), 1: float(weights[1])}


def train_ann_candidates(
    train_df: pd.DataFrame,
    external_df: pd.DataFrame,
    feature_sets: list[str],
    epochs: int,
    patience: int,
) -> tuple[pd.DataFrame, list[Candidate]]:
    if tf is None:
        print("TensorFlow/Keras not available; skipping ANN/Keras.")
        return pd.DataFrame(), []

    y_all = train_df["label"].astype(int).to_numpy()
    y_external = external_df["label"].astype(int).to_numpy()
    rows: list[dict[str, Any]] = []
    candidates: list[Candidate] = []

    for feature_set in feature_sets:
        set_seeds()
        x_all, x_external, columns = feature_data(train_df, external_df, feature_set)
        x_train, x_val, y_train, y_val = train_test_split(
            x_all,
            y_all,
            test_size=0.15,
            random_state=SEED,
            stratify=y_all,
        )
        scaler = StandardScaler()
        x_train_scaled = scaler.fit_transform(x_train)
        x_val_scaled = scaler.transform(x_val)
        x_external_scaled = scaler.transform(x_external)
        model = build_keras_model(x_train_scaled.shape[1])
        callbacks = [
            EarlyStopping(monitor="val_loss", patience=patience, restore_best_weights=True),
            ReduceLROnPlateau(monitor="val_loss", patience=max(2, patience // 2), factor=0.5, min_lr=1e-6),
        ]
        model_id = f"ann_keras_balanced__{feature_set}"
        start = time.perf_counter()
        history = model.fit(
            x_train_scaled,
            y_train,
            validation_data=(x_val_scaled, y_val),
            epochs=epochs,
            batch_size=64,
            callbacks=callbacks,
            class_weight=keras_class_weight(y_train),
            verbose=0,
        )
        train_seconds = time.perf_counter() - start
        start = time.perf_counter()
        y_score = model.predict(x_external_scaled, verbose=0).reshape(-1)
        predict_seconds = time.perf_counter() - start
        prefix = {
            "model_id": model_id,
            "algorithm": "ann_keras",
            "algorithm_family": algorithm_family("ann_keras"),
            "feature_set": feature_set,
            "class_weight": "balanced",
            "threshold_source": "default_0_50",
            "feature_count": len(columns),
            "train_seconds": round(train_seconds, 4),
            "predict_seconds": round(predict_seconds, 4),
            "epochs_run": len(history.history.get("loss", [])),
        }
        row = metric_row(y_external, y_score, 0.5, prefix)
        rows.append(row)

        wrapper = {
            "keras_model": model,
            "scaler": scaler,
        }
        candidates.append(
            Candidate(
                model_id=model_id,
                algorithm="ann_keras",
                algorithm_family=algorithm_family("ann_keras"),
                feature_set=feature_set,
                class_weight="balanced",
                threshold_source="default_0_50",
                model=wrapper,
                columns=columns,
                y_true=y_external,
                y_score=y_score,
                train_seconds=train_seconds,
                predict_seconds=predict_seconds,
            )
        )
        print(
            f"{model_id}: acc={row['accuracy']:.4f} "
            f"f1={row['f1_incorrect']:.4f} fp={row['false_positive']} fn={row['false_negative']}"
        )
    return pd.DataFrame(rows), candidates


def evaluate_rule_based(external_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    predictions: list[int] = []
    statuses: list[str] = []
    warning_texts: list[str] = []
    start = time.perf_counter()
    for _, row in external_df.iterrows():
        features = extract_posture_features(landmarks_from_feature_row(row))
        status, warnings = classify_posture_rule_based(features)
        statuses.append(status)
        warning_texts.append("; ".join(warnings))
        predictions.append(1 if status == "INCORRECT" else 0)
    predict_seconds = time.perf_counter() - start
    y_true = external_df["label"].astype(int).to_numpy()
    y_score = np.asarray(predictions, dtype=float)
    prefix = {
        "model_id": "rule_based_baseline",
        "algorithm": "rule_based",
        "algorithm_family": algorithm_family("rule_based"),
        "feature_set": "manual_ergonomic_rules",
        "class_weight": "none",
        "threshold_source": "manual_rules",
        "feature_count": 0,
        "train_seconds": 0.0,
        "predict_seconds": round(predict_seconds, 4),
    }
    row = metric_row(y_true, y_score, 0.5, prefix)
    predictions_df = external_df[[c for c in METADATA_COLUMNS if c in external_df.columns] + ["label"]].copy()
    predictions_df["model_id"] = "rule_based_baseline"
    predictions_df["prob_incorrect"] = y_score
    predictions_df["pred_label"] = y_score.astype(int)
    predictions_df["rule_status"] = statuses
    predictions_df["rule_warnings"] = warning_texts
    predictions_df["error_type"] = error_type(predictions_df["label"].to_numpy(), predictions_df["pred_label"].to_numpy())
    return pd.DataFrame([row]), predictions_df


def error_type(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    output = np.full(len(y_true), "correct", dtype=object)
    output[(y_true == 0) & (y_pred == 1)] = "false_positive"
    output[(y_true == 1) & (y_pred == 0)] = "false_negative"
    return output


def threshold_sweep(candidates: list[Candidate]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    thresholds = np.round(np.arange(0.05, 0.951, 0.01), 2)
    for candidate in candidates:
        for threshold in thresholds:
            rows.append(
                metric_row(
                    candidate.y_true,
                    candidate.y_score,
                    float(threshold),
                    {
                        "model_id": candidate.model_id,
                        "algorithm": candidate.algorithm,
                        "algorithm_family": candidate.algorithm_family,
                        "feature_set": candidate.feature_set,
                        "class_weight": candidate.class_weight,
                        "threshold_source": "external_threshold_sweep",
                        "feature_count": len(candidate.columns),
                        "train_seconds": round(candidate.train_seconds, 4),
                        "predict_seconds": round(candidate.predict_seconds, 4),
                    },
                )
            )
    return pd.DataFrame(rows)


def predictions_dataframe(external_df: pd.DataFrame, candidate: Candidate, threshold: float) -> pd.DataFrame:
    y_pred = (candidate.y_score >= threshold).astype(int)
    columns = [column for column in METADATA_COLUMNS if column in external_df.columns]
    output = external_df[columns + ["label"]].copy()
    output["model_id"] = candidate.model_id
    output["algorithm_family"] = candidate.algorithm_family
    output["feature_set"] = candidate.feature_set
    output["threshold"] = float(threshold)
    output["prob_incorrect"] = candidate.y_score
    output["pred_label"] = y_pred
    output["error_type"] = error_type(output["label"].astype(int).to_numpy(), y_pred)
    return output


def group_metrics(predictions: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for keys, group in predictions.groupby(group_cols, dropna=False, sort=True):
        if not isinstance(keys, tuple):
            keys = (keys,)
        y_true = group["label"].astype(int).to_numpy()
        y_score = group["prob_incorrect"].astype(float).to_numpy()
        threshold = float(group["threshold"].iloc[0]) if "threshold" in group.columns else 0.5
        row = metric_row(
            y_true,
            y_score,
            threshold,
            {column: value for column, value in zip(group_cols, keys)},
        )
        row["n"] = int(len(group))
        row["majority_pred_label"] = int((group["pred_label"].astype(int).mean()) >= 0.5)
        row["mean_prob_incorrect"] = float(np.mean(y_score))
        rows.append(row)
    return pd.DataFrame(rows)


def top_per_algorithm(default_results: pd.DataFrame) -> pd.DataFrame:
    ranked = default_results.sort_values(
        ["algorithm_family", "f1_incorrect", "mcc", "precision_incorrect"],
        ascending=[True, False, False, False],
    )
    return ranked.groupby("algorithm_family", sort=False).head(1).reset_index(drop=True)


def save_best_models(candidates: list[Candidate], selected_ids: set[str]) -> None:
    for candidate in candidates:
        if candidate.model_id not in selected_ids:
            continue
        out_dir = MODEL_DIR / clean_model_id(candidate.model_id)
        out_dir.mkdir(parents=True, exist_ok=True)
        if candidate.algorithm == "ann_keras":
            model = candidate.model["keras_model"]
            scaler = candidate.model["scaler"]
            model.save(out_dir / "model.keras")
            joblib.dump(scaler, out_dir / "scaler.pkl")
        else:
            joblib.dump(candidate.model, out_dir / "model.pkl")
        (out_dir / "feature_schema.json").write_text(
            json.dumps(
                {
                    "feature_set": candidate.feature_set,
                    "columns": candidate.columns,
                    "source": "full_protocol_external_benchmark",
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )


def save_model_comparison_figure(summary: pd.DataFrame, path: Path) -> None:
    plot_df = summary.sort_values("f1_incorrect", ascending=False).copy()
    labels = plot_df["algorithm_family"].tolist()
    x = np.arange(len(labels))
    width = 0.2
    fig, ax = plt.subplots(figsize=(12, 5.8))
    metrics = [
        ("accuracy", "Accuracy"),
        ("precision_incorrect", "Precision"),
        ("recall_incorrect", "Recall"),
        ("f1_incorrect", "F1"),
    ]
    for offset, (column, label) in zip([-1.5, -0.5, 0.5, 1.5], metrics):
        ax.bar(x + offset * width, plot_df[column] * 100.0, width, label=label)
    ax.set_ylabel("Score (%)")
    ax.set_ylim(0, 100)
    ax.set_title("Full protocol external benchmark by algorithm family")
    ax.set_xticks(x, labels=labels, rotation=25, ha="right")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.13))
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_confusion_matrix_figure(row: pd.Series, path: Path) -> None:
    matrix = np.array(
        [
            [int(row["true_negative"]), int(row["false_positive"])],
            [int(row["false_negative"]), int(row["true_positive"])],
        ]
    )
    fig, ax = plt.subplots(figsize=(5.8, 5.0))
    image = ax.imshow(matrix, cmap="Blues")
    ax.set_title(f"Confusion matrix: {row['algorithm_family']}")
    ax.set_xticks([0, 1], labels=["Pred Correct", "Pred Incorrect"])
    ax.set_yticks([0, 1], labels=["True Correct", "True Incorrect"])
    for i in range(2):
        for j in range(2):
            ax.text(
                j,
                i,
                str(matrix[i, j]),
                ha="center",
                va="center",
                color="white" if matrix[i, j] > matrix.max() / 2 else "black",
                fontsize=14,
                fontweight="bold",
            )
    ax.set_xlabel("Predicted label")
    ax.set_ylabel("Ground-truth label")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_threshold_sweep_figure(sweep: pd.DataFrame, model_id: str, path: Path) -> None:
    subset = sweep[sweep["model_id"] == model_id].sort_values("threshold")
    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    for column, label in [
        ("precision_incorrect", "Precision Incorrect"),
        ("recall_incorrect", "Recall Incorrect"),
        ("f1_incorrect", "F1 Incorrect"),
        ("mcc", "MCC"),
    ]:
        ax.plot(subset["threshold"], subset[column], label=label)
    ax.set_xlabel("Decision threshold")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1.02)
    ax.set_title(f"Threshold sweep: {model_id}")
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def fmt_pct(value: float) -> str:
    if pd.isna(value):
        return ""
    return f"{value * 100:.2f}%"


def markdown_table(df: pd.DataFrame, max_rows: int | None = None) -> str:
    if max_rows is not None:
        df = df.head(max_rows)
    if df.empty:
        return "_No data._"
    lines = [
        "| " + " | ".join(str(column) for column in df.columns) + " |",
        "| " + " | ".join("---" for _ in df.columns) + " |",
    ]
    for _, row in df.iterrows():
        values = []
        for value in row:
            if isinstance(value, float):
                values.append(f"{value:.4f}")
            else:
                values.append(str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def percent_view(df: pd.DataFrame) -> pd.DataFrame:
    output = df.copy()
    for column in ["accuracy", "precision_incorrect", "recall_incorrect", "f1_incorrect", "macro_f1", "roc_auc", "pr_auc"]:
        if column in output.columns:
            output[column] = output[column].map(fmt_pct)
    if "mcc" in output.columns:
        output["mcc"] = output["mcc"].map(lambda value: f"{value:.4f}" if pd.notna(value) else "")
    if "threshold" in output.columns:
        output["threshold"] = output["threshold"].map(lambda value: f"{value:.2f}" if pd.notna(value) else "")
    return output


def write_report(
    split: dict[str, Any],
    default_results: pd.DataFrame,
    calibrated_results: pd.DataFrame,
    family_summary: pd.DataFrame,
    selected_default: pd.Series,
    selected_calibrated: pd.Series,
    video_wise: pd.DataFrame,
    participant_wise: pd.DataFrame,
    rule_based: pd.DataFrame,
    ann_rows: pd.DataFrame,
    hgb_rows: pd.DataFrame,
    feature_sets: list[str],
    ann_feature_sets: list[str],
    args: argparse.Namespace,
) -> None:
    text = "# Full Protocol Model Benchmark on External P06-P07\n\n"
    text += f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    text += "## 1. Muc tieu\n\n"
    text += (
        "Bao cao nay chay lai benchmark day du tren cung protocol: cac mo hinh hoc may "
        "duoc train tren P01-P05 va danh gia tren external P06-P07. Rule-based Baseline "
        "khong train, chi danh gia truc tiep tren external.\n\n"
    )
    text += "## 2. Dataset split va leakage check\n\n"
    text += f"- Train/development: {split['train_rows']} frame, {split['train_videos']} video, participants {', '.join(split['train_participants'])}.\n"
    text += f"- External: {split['external_rows']} frame, {split['external_videos']} video, participants {', '.join(split['external_participants'])}.\n"
    text += f"- Train label counts: {split['train_label_counts']}.\n"
    text += f"- External label counts: {split['external_label_counts']}.\n"
    text += f"- Source video overlap count: {split['source_video_overlap_count']}.\n"
    text += f"- Train only P01-P05: {split['train_only_p01_p05']}.\n"
    text += f"- External only P06-P07: {split['external_only_p06_p07']}.\n"
    text += f"- Participant disjoint: {split['participant_disjoint']}.\n"
    text += f"- Source video disjoint: {split['source_video_disjoint']}.\n\n"
    text += "## 3. Feature sets va thuat toan\n\n"
    text += "- Feature sets: " + ", ".join(f"`{item}`" for item in feature_sets) + ".\n"
    text += "- ANN/Keras feature sets: " + ", ".join(f"`{item}`" for item in ann_feature_sets) + ".\n"
    text += (
        "- Algorithms: Logistic Regression, SVM RBF, KNN, Decision Tree, Random Forest, "
        "MLPClassifier, ANN/Keras, HistGradientBoosting, Rule-based Baseline.\n"
    )
    text += "- Threshold mac dinh cho bang chinh: 0.50 voi cac mo hinh co score/probability.\n"
    text += "- Threshold sweep la phan tich external-calibrated, khong nen goi la blind external test.\n\n"
    text += "## 4. Bang benchmark chinh theo threshold mac dinh 0.50\n\n"
    columns = [
        "model_id",
        "algorithm_family",
        "feature_set",
        "class_weight",
        "threshold",
        "accuracy",
        "precision_incorrect",
        "recall_incorrect",
        "f1_incorrect",
        "macro_f1",
        "mcc",
        "roc_auc",
        "pr_auc",
        "false_positive",
        "false_negative",
        "train_seconds",
        "predict_seconds",
    ]
    text += markdown_table(percent_view(default_results[columns].sort_values(["f1_incorrect", "mcc"], ascending=False)), max_rows=25)
    text += "\n\n"
    text += "Bang tren la so sanh cong bang theo threshold mac dinh. Neu dua vao luan van, co the rut gon thanh top cau hinh dai dien cua tung thuat toan va dua bang day du vao phu luc.\n\n"
    text += "## 5. Cau hinh tot nhat cua tung nhom thuat toan\n\n"
    text += markdown_table(percent_view(family_summary[columns].sort_values("f1_incorrect", ascending=False)))
    text += "\n\n"
    text += "Day la bang nen dua vao muc thuc nghiem cua luan van vi moi nhom thuat toan chi lay cau hinh tot nhat tren protocol hien tai.\n\n"
    text += "## 6. Threshold sweep va ket qua hieu chinh nguong\n\n"
    cal_columns = columns.copy()
    text += markdown_table(percent_view(calibrated_results[cal_columns].sort_values(["f1_incorrect", "mcc"], ascending=False)), max_rows=25)
    text += "\n\n"
    text += (
        "Cac dong trong muc nay duoc chon tu threshold sweep tren external P06-P07. Neu dung de viet bai, "
        "can ghi ro day la phan tich hieu chinh nguong tren external, khong phai ket qua blind test hoan toan.\n\n"
    )
    text += "## 7. Model tot nhat theo default va theo calibrated threshold\n\n"
    text += "Default threshold best:\n\n"
    text += markdown_table(percent_view(pd.DataFrame([selected_default])[columns]))
    text += "\n\nExternal-calibrated best:\n\n"
    text += markdown_table(percent_view(pd.DataFrame([selected_calibrated])[columns]))
    text += "\n\n"
    text += "## 8. Rule-based Baseline\n\n"
    text += markdown_table(percent_view(rule_based[columns]))
    text += "\n\nRule-based khong hoc tu du lieu. Day la baseline giai thich duoc nhung thuong kem linh hoat voi goc camera va khac biet co the nguoi dung.\n\n"
    text += "## 9. ANN/Keras\n\n"
    if ann_rows.empty:
        text += "_ANN/Keras khong duoc chay, co the do TensorFlow/Keras khong kha dung trong moi truong._\n\n"
    else:
        text += markdown_table(percent_view(ann_rows[columns].sort_values(["f1_incorrect", "mcc"], ascending=False)))
        text += "\n\nANN/Keras duoc train lai tren dataset moi, nhung neu ket qua thap hon HGB thi nen trinh bay ANN la neural baseline hoac model tich hop ban dau.\n\n"
    text += "## 10. HistGradientBoosting\n\n"
    text += markdown_table(percent_view(hgb_rows[columns].sort_values(["f1_incorrect", "mcc"], ascending=False)), max_rows=12)
    text += "\n\n"
    text += "## 11. Video-wise external analysis cho selected calibrated model\n\n"
    video_columns = [
        "source_video",
        "participant_id",
        "view_angle",
        "label",
        "n",
        "accuracy",
        "precision_incorrect",
        "recall_incorrect",
        "f1_incorrect",
        "false_positive",
        "false_negative",
        "majority_pred_label",
        "mean_prob_incorrect",
    ]
    text += markdown_table(percent_view(video_wise[video_columns].sort_values(["accuracy", "f1_incorrect"], ascending=True)), max_rows=23)
    text += "\n\n"
    text += "## 12. Participant-wise external analysis cho selected calibrated model\n\n"
    participant_columns = [
        "participant_id",
        "n",
        "accuracy",
        "precision_incorrect",
        "recall_incorrect",
        "f1_incorrect",
        "mcc",
        "false_positive",
        "false_negative",
    ]
    text += markdown_table(percent_view(participant_wise[participant_columns]))
    text += "\n\n"
    text += "## 13. File da xuat\n\n"
    for path in [
        RESULTS_DIR / "full_protocol_model_benchmark_external_p06p07.csv",
        RESULTS_DIR / "full_protocol_threshold_sweep_external_p06p07.csv",
        RESULTS_DIR / "full_protocol_predictions_external_p06p07.csv",
        RESULTS_DIR / "full_protocol_rule_based_external_p06p07.csv",
        RESULTS_DIR / "full_protocol_video_wise_external_p06p07.csv",
        RESULTS_DIR / "full_protocol_participant_wise_external_p06p07.csv",
        FIGURES_DIR / "full_protocol_model_comparison_bar.png",
        FIGURES_DIR / "full_protocol_confusion_matrix_best.png",
        FIGURES_DIR / "full_protocol_threshold_sweep_best.png",
    ]:
        text += f"- `{path.relative_to(BASE_DIR)}`\n"
    text += "\n## 14. Ket luan su dung cho luan van\n\n"
    text += (
        "Ket qua benchmark day du nen thay the bang so sanh 4 cau hinh dai dien neu muc 4.4 dang can minh chung "
        "tat ca thuat toan da duoc chay lai. Trong than luan van, nen dua bang tom tat top cau hinh cua tung "
        "algorithm family; bieu do chi nen minh hoa Accuracy, Precision, Recall va F1 de tranh qua tai thong tin.\n\n"
    )
    text += (
        "Neu model tot nhat khac ANN/Keras, co the trinh bay ANN la neural baseline/model tich hop ban dau, "
        "con model co ket qua external tot hon la model duoc de xuat cho phien ban ung dung cap nhat.\n\n"
    )
    text += "## 15. Checklist\n\n"
    checks = [
        ("Da train Logistic Regression", "Logistic Regression" in set(default_results["algorithm_family"])),
        ("Da train SVM", "SVM RBF" in set(default_results["algorithm_family"])),
        ("Da train KNN", "KNN" in set(default_results["algorithm_family"])),
        ("Da train Decision Tree", "Decision Tree" in set(default_results["algorithm_family"])),
        ("Da train Random Forest", "Random Forest" in set(default_results["algorithm_family"])),
        ("Da train MLPClassifier", "MLPClassifier" in set(default_results["algorithm_family"])),
        ("Da train ANN/Keras", "ANN/Keras" in set(default_results["algorithm_family"])),
        ("Da train HistGradientBoosting", "HistGradientBoosting" in set(default_results["algorithm_family"])),
        ("Da danh gia Rule-based Baseline", "Rule-based Baseline" in set(default_results["algorithm_family"])),
        ("Train/external khong trung participant", split["participant_disjoint"]),
        ("Train/external khong trung source_video", split["source_video_disjoint"]),
        ("Co video-wise report", not video_wise.empty),
        ("Co participant-wise report", not participant_wise.empty),
        ("Co threshold sweep", not calibrated_results.empty),
        ("Khong cap nhat app registry", True),
    ]
    for label, passed in checks:
        text += f"- [{'x' if passed else ' '}] {label}\n"

    if args.no_ann:
        text += "\nGhi chu: lan chay nay dung `--no-ann`, nen ANN/Keras khong duoc train lai.\n"

    REPORT_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run full protocol benchmark on external P06/P07.")
    parser.add_argument("--feature-sets", nargs="*", default=DEFAULT_FEATURE_SETS)
    parser.add_argument("--ann-feature-sets", nargs="*", default=["normalized_99", "ergonomic_v2_with_view"])
    parser.add_argument("--ann-epochs", type=int, default=80)
    parser.add_argument("--ann-patience", type=int, default=10)
    parser.add_argument("--no-ann", action="store_true")
    args = parser.parse_args()

    ensure_dirs()
    set_seeds()
    train_df, external_df = load_data()
    split = split_check(train_df, external_df)
    if not (split["train_only_p01_p05"] and split["external_only_p06_p07"] and split["participant_disjoint"] and split["source_video_disjoint"]):
        raise RuntimeError(f"Dataset split check failed: {json.dumps(split, ensure_ascii=False, indent=2)}")

    sklearn_results, sklearn_candidates = train_sklearn_candidates(train_df, external_df, args.feature_sets)
    ann_results, ann_candidates = (
        (pd.DataFrame(), [])
        if args.no_ann
        else train_ann_candidates(train_df, external_df, args.ann_feature_sets, args.ann_epochs, args.ann_patience)
    )
    rule_results, rule_predictions = evaluate_rule_based(external_df)

    default_results = pd.concat([sklearn_results, ann_results, rule_results], ignore_index=True)
    default_results = default_results.sort_values(["f1_incorrect", "mcc", "precision_incorrect"], ascending=False)
    default_results.to_csv(RESULTS_DIR / "full_protocol_model_benchmark_external_p06p07.csv", index=False, encoding="utf-8-sig")
    rule_predictions.to_csv(RESULTS_DIR / "full_protocol_rule_based_external_p06p07.csv", index=False, encoding="utf-8-sig")

    learned_candidates = sklearn_candidates + ann_candidates
    sweep = threshold_sweep(learned_candidates)
    sweep.to_csv(RESULTS_DIR / "full_protocol_threshold_sweep_external_p06p07.csv", index=False, encoding="utf-8-sig")
    best_per_model = (
        sweep.sort_values(["model_id", "f1_incorrect", "mcc", "precision_incorrect"], ascending=[True, False, False, False])
        .groupby("model_id", sort=False)
        .head(1)
        .reset_index(drop=True)
    )
    calibrated_results = best_per_model.sort_values(["f1_incorrect", "mcc", "precision_incorrect"], ascending=False)

    selected_default = default_results.iloc[0]
    selected_calibrated = calibrated_results.iloc[0]
    selected_candidate = next(candidate for candidate in learned_candidates if candidate.model_id == selected_calibrated["model_id"])
    selected_threshold = float(selected_calibrated["threshold"])
    selected_predictions = predictions_dataframe(external_df, selected_candidate, selected_threshold)
    selected_predictions.to_csv(RESULTS_DIR / "full_protocol_predictions_external_p06p07.csv", index=False, encoding="utf-8-sig")

    video_wise = group_metrics(selected_predictions, ["source_video", "participant_id", "view_angle", "label"])
    participant_wise = group_metrics(selected_predictions, ["participant_id"])
    video_wise.to_csv(RESULTS_DIR / "full_protocol_video_wise_external_p06p07.csv", index=False, encoding="utf-8-sig")
    participant_wise.to_csv(RESULTS_DIR / "full_protocol_participant_wise_external_p06p07.csv", index=False, encoding="utf-8-sig")

    family_summary = top_per_algorithm(default_results)
    save_model_comparison_figure(family_summary, FIGURES_DIR / "full_protocol_model_comparison_bar.png")
    save_confusion_matrix_figure(selected_calibrated, FIGURES_DIR / "full_protocol_confusion_matrix_best.png")
    save_threshold_sweep_figure(sweep, str(selected_calibrated["model_id"]), FIGURES_DIR / "full_protocol_threshold_sweep_best.png")
    selected_ids = {str(selected_default["model_id"]), str(selected_calibrated["model_id"])}
    save_best_models(learned_candidates, selected_ids)

    write_report(
        split=split,
        default_results=default_results,
        calibrated_results=calibrated_results,
        family_summary=family_summary,
        selected_default=selected_default,
        selected_calibrated=selected_calibrated,
        video_wise=video_wise,
        participant_wise=participant_wise,
        rule_based=rule_results,
        ann_rows=default_results[default_results["algorithm_family"] == "ANN/Keras"],
        hgb_rows=default_results[default_results["algorithm_family"] == "HistGradientBoosting"],
        feature_sets=args.feature_sets,
        ann_feature_sets=[] if args.no_ann else args.ann_feature_sets,
        args=args,
    )

    print("\nFull protocol benchmark completed.")
    print(f"Default best: {selected_default['model_id']} f1={selected_default['f1_incorrect']:.4f}")
    print(
        f"External-calibrated best: {selected_calibrated['model_id']} "
        f"threshold={float(selected_calibrated['threshold']):.2f} "
        f"f1={selected_calibrated['f1_incorrect']:.4f}"
    )
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
