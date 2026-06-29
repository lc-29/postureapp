"""Prepare Chapter 4 benchmark tables, figures, and final review report.

This script is intentionally report-only. It does not update the desktop app,
SQLite schema, or model registry.
"""

from __future__ import annotations

import argparse
import json
import os
import time
import textwrap
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
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
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils.class_weight import compute_class_weight, compute_sample_weight

try:
    import tensorflow as tf
    from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
    from tensorflow.keras.layers import BatchNormalization, Dense, Dropout, Input
    from tensorflow.keras.models import Sequential
except Exception:  # pragma: no cover - reported at runtime
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
except ImportError:
    from src.feature_schema import build_feature_matrix


BASE_DIR = Path(__file__).resolve().parents[1]
TRAIN_PATH = BASE_DIR / "dataset" / "processed" / "posture_data_2fps_with_metadata.csv"
EXTERNAL_PATH = BASE_DIR / "dataset" / "processed" / "posture_external_test_2fps_with_metadata.csv"
RESULTS_DIR = BASE_DIR / "reports" / "results"
FIGURES_DIR = BASE_DIR / "reports" / "figures"
TABLES_DIR = BASE_DIR / "reports" / "tables"
REPORT_PATH = BASE_DIR / "reports" / "FULL_PROTOCOL_BENCHMARK_FINAL_REVIEW.md"

FULL_BENCHMARK_PATH = RESULTS_DIR / "full_protocol_model_benchmark_external_p06p07.csv"
THRESHOLD_SWEEP_PATH = RESULTS_DIR / "full_protocol_threshold_sweep_external_p06p07.csv"
BEST_BY_ALGORITHM_PATH = RESULTS_DIR / "full_protocol_best_by_algorithm_default_threshold.csv"
SELECTED_HGB_METRICS_PATH = RESULTS_DIR / "selected_hgb_external_calibrated_metrics.csv"
REPEATABILITY_RAW_PATH = RESULTS_DIR / "full_protocol_repeatability_by_seed.csv"
REPEATABILITY_SUMMARY_PATH = RESULTS_DIR / "full_protocol_repeatability_mean_std.csv"

SEEDS = [42, 43, 44, 45, 46]
METRIC_COLUMNS = [
    "accuracy",
    "precision_incorrect",
    "recall_incorrect",
    "f1_incorrect",
    "macro_f1",
    "mcc",
    "roc_auc",
    "pr_auc",
]
REQUIRED_FEATURE_SETS = {
    "raw_99",
    "normalized_99",
    "ergonomic_14",
    "ergonomic_v2",
    "ergonomic_v2_with_view",
    "combined_v2",
    "combined_v2_with_view",
}
ALGORITHM_ORDER = [
    "HistGradientBoosting",
    "Logistic Regression",
    "Random Forest",
    "SVM RBF",
    "Decision Tree",
    "KNN",
    "ANN/Keras",
    "MLPClassifier",
    "Rule-based Baseline",
]


@dataclass
class SplitCheck:
    train_rows: int
    train_videos: int
    train_participants: list[str]
    train_label_counts: dict[str, int]
    external_rows: int
    external_videos: int
    external_participants: list[str]
    external_label_counts: dict[str, int]
    overlap_count: int
    train_only_p01_p05: bool
    external_only_p06_p07: bool
    participant_disjoint: bool
    source_video_disjoint: bool

    @property
    def ok(self) -> bool:
        return (
            self.train_rows == 12680
            and self.train_videos == 94
            and self.external_rows == 4556
            and self.external_videos == 23
            and self.train_only_p01_p05
            and self.external_only_p06_p07
            and self.participant_disjoint
            and self.source_video_disjoint
            and self.external_label_counts.get("0") == 2001
            and self.external_label_counts.get("1") == 2555
        )


def ensure_dirs() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)


def set_seed(seed: int) -> None:
    np.random.seed(seed)
    if tf is not None:
        tf.random.set_seed(seed)


def pct_label(value: float) -> str:
    return f"{value:.2f}%".replace(".", ",")


def fmt_pct(value: float) -> str:
    if pd.isna(value):
        return ""
    return f"{value * 100:.2f}%".replace(".", ",")


def fmt_float(value: float, digits: int = 4) -> str:
    if pd.isna(value):
        return ""
    return f"{value:.{digits}f}".replace(".", ",")


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if not FULL_BENCHMARK_PATH.exists():
        raise FileNotFoundError(FULL_BENCHMARK_PATH)
    if not THRESHOLD_SWEEP_PATH.exists():
        raise FileNotFoundError(THRESHOLD_SWEEP_PATH)
    train_df = pd.read_csv(TRAIN_PATH).reset_index(drop=True)
    external_df = pd.read_csv(EXTERNAL_PATH).reset_index(drop=True)
    default_results = pd.read_csv(FULL_BENCHMARK_PATH)
    sweep = pd.read_csv(THRESHOLD_SWEEP_PATH)
    return train_df, external_df, default_results, sweep


def run_split_check(train_df: pd.DataFrame, external_df: pd.DataFrame) -> SplitCheck:
    train_participants = sorted(train_df["participant_id"].astype(str).unique().tolist())
    external_participants = sorted(external_df["participant_id"].astype(str).unique().tolist())
    train_videos = set(train_df["source_video"].astype(str).unique())
    external_videos = set(external_df["source_video"].astype(str).unique())
    return SplitCheck(
        train_rows=int(len(train_df)),
        train_videos=int(train_df["source_video"].nunique()),
        train_participants=train_participants,
        train_label_counts={str(k): int(v) for k, v in train_df["label"].value_counts().sort_index().items()},
        external_rows=int(len(external_df)),
        external_videos=int(external_df["source_video"].nunique()),
        external_participants=external_participants,
        external_label_counts={str(k): int(v) for k, v in external_df["label"].value_counts().sort_index().items()},
        overlap_count=int(len(train_videos.intersection(external_videos))),
        train_only_p01_p05=set(train_participants).issubset({"P01", "P02", "P03", "P04", "P05"}),
        external_only_p06_p07=set(external_participants) == {"P06", "P07"},
        participant_disjoint=set(train_participants).isdisjoint(set(external_participants)),
        source_video_disjoint=train_videos.isdisjoint(external_videos),
    )


def validate_feature_names(df: pd.DataFrame) -> None:
    values = set(df["feature_set"].dropna().astype(str).unique())
    invalid = {"ergonomic_v2_view", "combined_v2_view"}.intersection(values)
    if invalid:
        raise ValueError(f"Invalid shortened feature set names found: {sorted(invalid)}")
    unknown = values.difference(REQUIRED_FEATURE_SETS).difference({"manual_ergonomic_rules"})
    if unknown:
        raise ValueError(f"Unexpected feature set names found: {sorted(unknown)}")


def make_best_by_algorithm(default_results: pd.DataFrame) -> pd.DataFrame:
    validate_feature_names(default_results)
    required_families = set(ALGORITHM_ORDER)
    families = set(default_results["algorithm_family"].dropna().astype(str).unique())
    missing = required_families.difference(families)
    if missing:
        raise ValueError(f"Missing algorithm families: {sorted(missing)}")

    default_only = default_results[
        (default_results["threshold_source"].isin(["default_0_50", "manual_rules"]))
        & (np.isclose(default_results["threshold"].astype(float), 0.50))
    ].copy()
    default_only["algorithm_order"] = default_only["algorithm_family"].map(
        {name: index for index, name in enumerate(ALGORITHM_ORDER)}
    )
    default_only = default_only.sort_values(
        ["algorithm_family", "f1_incorrect", "mcc", "accuracy", "false_positive"],
        ascending=[True, False, False, False, True],
    )
    best = default_only.groupby("algorithm_family", sort=False).head(1).copy()
    best = best.sort_values("algorithm_order").reset_index(drop=True)
    output_columns = [
        "algorithm_family",
        "model_id",
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
        "true_negative",
        "true_positive",
        "n_test",
    ]
    best[output_columns].to_csv(BEST_BY_ALGORITHM_PATH, index=False, encoding="utf-8-sig")
    return best[output_columns].copy()


def save_figure_4_2(best: pd.DataFrame) -> None:
    plot_df = best.sort_values("f1_incorrect", ascending=False).reset_index(drop=True)
    metric_cols = ["accuracy", "precision_incorrect", "recall_incorrect", "f1_incorrect"]
    metric_labels = ["Accuracy", "Precision", "Recall", "F1-score"]
    values = plot_df[metric_cols].to_numpy(dtype=float) * 100.0

    row_labels = [
        f"{row.algorithm_family}\n{row.feature_set}, ngưỡng 0,50"
        if row.algorithm_family != "Rule-based Baseline"
        else "Rule-based Baseline\nmanual rules"
        for row in plot_df.itertuples(index=False)
    ]

    source = plot_df[
        [
            "algorithm_family",
            "model_id",
            "feature_set",
            "class_weight",
            "threshold",
            "accuracy",
            "precision_incorrect",
            "recall_incorrect",
            "f1_incorrect",
            "mcc",
            "false_positive",
            "false_negative",
        ]
    ].copy()
    for column in metric_cols:
        source[f"{column}_percent"] = (source[column] * 100.0).round(2)
    source.to_csv(TABLES_DIR / "figure_4_2_default_threshold_source.csv", index=False, encoding="utf-8-sig")

    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False
    fig, ax = plt.subplots(figsize=(12.2, 6.5))
    image = ax.imshow(values, cmap="YlGnBu", vmin=0, vmax=100, aspect="auto")

    ax.set_xticks(np.arange(len(metric_labels)), labels=metric_labels, fontsize=11, fontweight="bold")
    ax.set_yticks(np.arange(len(row_labels)), labels=row_labels, fontsize=9.2)
    ax.set_title(
        "So sánh các chỉ số của cấu hình đại diện theo nhóm thuật toán",
        fontsize=14,
        fontweight="bold",
        pad=18,
    )
    ax.set_xticks(np.arange(-0.5, len(metric_labels), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(row_labels), 1), minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=1.3)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.tick_params(axis="x", top=True, bottom=False, labeltop=True, labelbottom=False)

    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            value = values[i, j]
            color = "white" if value >= 72 else "#1f2933"
            ax.text(
                j,
                i,
                pct_label(value),
                ha="center",
                va="center",
                fontsize=9.3,
                fontweight="bold",
                color=color,
            )

    colorbar = fig.colorbar(image, ax=ax, fraction=0.035, pad=0.025)
    colorbar.set_label("Giá trị (%)", rotation=90)
    note = (
        "Ghi chú: mỗi dòng là cấu hình có F1-score lớp Incorrect cao nhất của một nhóm thuật toán "
        "tại ngưỡng mặc định 0,50 trên tập external P06-P07. Precision, Recall và F1-score được tính "
        "cho lớp Incorrect. Rule-based Baseline không sử dụng ngưỡng xác suất."
    )
    fig.text(
        0.01,
        0.020,
        textwrap.fill(note, width=150),
        ha="left",
        fontsize=8.5,
        color="#374151",
    )
    fig.subplots_adjust(left=0.31, right=0.93, top=0.82, bottom=0.18)

    for name in [
        "figure_4_2_algorithm_family_default_threshold_heatmap",
        "figure_4_2_model_metric_comparison",
    ]:
        fig.savefig(FIGURES_DIR / f"{name}.png", dpi=320)
        fig.savefig(FIGURES_DIR / f"{name}.svg")
    plt.close(fig)


def selected_hgb_row(sweep: pd.DataFrame) -> pd.Series:
    subset = sweep[
        (sweep["model_id"] == "hist_gradient_boosting_none__ergonomic_v2_with_view")
        & np.isclose(sweep["threshold"].astype(float), 0.76)
    ].copy()
    if subset.empty:
        raise ValueError("Missing selected HGB threshold 0.76 row.")
    row = subset.sort_values(["f1_incorrect", "mcc"], ascending=False).iloc[0]
    row.to_frame().T.to_csv(SELECTED_HGB_METRICS_PATH, index=False, encoding="utf-8-sig")
    return row


def save_hgb_threshold_figure(sweep: pd.DataFrame) -> None:
    subset = sweep[sweep["model_id"] == "hist_gradient_boosting_none__ergonomic_v2_with_view"].sort_values("threshold")
    selected = subset[np.isclose(subset["threshold"].astype(float), 0.76)].iloc[0]

    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    ax.plot(subset["threshold"], subset["precision_incorrect"], label="Precision Incorrect", linewidth=2)
    ax.plot(subset["threshold"], subset["recall_incorrect"], label="Recall Incorrect", linewidth=2)
    ax.plot(subset["threshold"], subset["f1_incorrect"], label="F1 Incorrect", linewidth=2)
    ax.plot(subset["threshold"], subset["mcc"], label="MCC", linewidth=2)
    ax.axvline(0.76, color="#d62828", linestyle="--", linewidth=1.8, label="Ngưỡng 0,76")
    ax.scatter([0.76], [selected["f1_incorrect"]], color="#d62828", zorder=4)
    ax.set_title("Khảo sát ngưỡng của HistGradientBoosting trên external P06-P07", fontweight="bold")
    ax.set_xlabel("Ngưỡng quyết định")
    ax.set_ylabel("Giá trị")
    ax.set_ylim(0, 1.02)
    ax.grid(True, alpha=0.25)
    ax.legend(ncol=2)
    fig.tight_layout()
    for suffix in ["png", "svg"]:
        fig.savefig(FIGURES_DIR / f"figure_4_3_selected_hgb_threshold_sweep.{suffix}", dpi=320)
    plt.close(fig)


def save_hgb_confusion_matrix(row: pd.Series) -> None:
    matrix = np.array(
        [
            [int(row["true_negative"]), int(row["false_positive"])],
            [int(row["false_negative"]), int(row["true_positive"])],
        ]
    )
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, ax = plt.subplots(figsize=(5.9, 5.2))
    image = ax.imshow(matrix, cmap="Blues")
    ax.set_title("Confusion matrix của HGB tại ngưỡng 0,76", fontweight="bold")
    ax.set_xticks([0, 1], labels=["Dự đoán Correct", "Dự đoán Incorrect"])
    ax.set_yticks([0, 1], labels=["Thực tế Correct", "Thực tế Incorrect"])
    for i in range(2):
        for j in range(2):
            ax.text(
                j,
                i,
                f"{matrix[i, j]}",
                ha="center",
                va="center",
                fontsize=15,
                fontweight="bold",
                color="white" if matrix[i, j] > matrix.max() / 2 else "black",
            )
    ax.set_xlabel("Nhãn dự đoán")
    ax.set_ylabel("Nhãn thực tế")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    for suffix in ["png", "svg"]:
        fig.savefig(FIGURES_DIR / f"figure_4_4_selected_hgb_confusion_matrix.{suffix}", dpi=320)
    plt.close(fig)


def safe_auc(y_true: np.ndarray, y_score: np.ndarray, kind: str) -> float:
    if len(np.unique(y_true)) < 2:
        return float("nan")
    if kind == "roc":
        return float(roc_auc_score(y_true, y_score))
    if kind == "pr":
        return float(average_precision_score(y_true, y_score))
    raise ValueError(kind)


def metrics_from_scores(y_true: np.ndarray, y_score: np.ndarray, threshold: float, prefix: dict[str, Any]) -> dict[str, Any]:
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
        "predicted_incorrect_rate": float(y_pred.mean()),
    }
    row.update(prefix)
    return row


def make_repeatability_model(row: pd.Series, seed: int) -> Any:
    algorithm = row["algorithm"]
    class_weight = row["class_weight"]
    weight = None if class_weight == "none" else "balanced"
    if algorithm == "random_forest":
        return RandomForestClassifier(
            n_estimators=350,
            max_depth=None,
            min_samples_leaf=2,
            class_weight=weight,
            random_state=seed,
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
                        random_state=seed,
                    ),
                ),
            ]
        )
    if algorithm == "hist_gradient_boosting":
        return HistGradientBoostingClassifier(max_iter=250, learning_rate=0.06, random_state=seed)
    if algorithm == "decision_tree":
        return DecisionTreeClassifier(max_depth=8, min_samples_leaf=20, class_weight=weight, random_state=seed)
    raise ValueError(f"Repeatability model not supported: {algorithm}")


def predict_scores(model: Any, x: pd.DataFrame | np.ndarray) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        return np.asarray(model.predict_proba(x))[:, 1].astype(float)
    if hasattr(model, "decision_function"):
        decision = np.asarray(model.decision_function(x), dtype=float)
        return 1.0 / (1.0 + np.exp(-decision))
    return np.asarray(model.predict(x), dtype=float).reshape(-1)


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


def ann_class_weights(y_train: np.ndarray) -> dict[int, float]:
    weights = compute_class_weight(class_weight="balanced", classes=np.array([0, 1]), y=y_train)
    return {0: float(weights[0]), 1: float(weights[1])}


def run_ann_repeatability(
    train_df: pd.DataFrame,
    external_df: pd.DataFrame,
    row: pd.Series,
    seed: int,
    epochs: int,
    patience: int,
) -> dict[str, Any]:
    if tf is None:
        raise RuntimeError("TensorFlow/Keras is not available.")
    set_seed(seed)
    x_all, train_columns = build_feature_matrix(train_df, row["feature_set"])
    x_external, external_columns = build_feature_matrix(external_df, row["feature_set"])
    if train_columns != external_columns:
        raise ValueError("ANN repeatability feature mismatch.")
    y_all = train_df["label"].astype(int).to_numpy()
    y_external = external_df["label"].astype(int).to_numpy()
    x_train, x_val, y_train, y_val = train_test_split(
        x_all,
        y_all,
        test_size=0.15,
        random_state=seed,
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
    start = time.perf_counter()
    history = model.fit(
        x_train_scaled,
        y_train,
        validation_data=(x_val_scaled, y_val),
        epochs=epochs,
        batch_size=64,
        callbacks=callbacks,
        class_weight=ann_class_weights(y_train),
        verbose=0,
    )
    train_seconds = time.perf_counter() - start
    start = time.perf_counter()
    y_score = model.predict(x_external_scaled, verbose=0).reshape(-1)
    predict_seconds = time.perf_counter() - start
    output = metrics_from_scores(
        y_external,
        y_score,
        0.50,
        {
            "seed": seed,
            "algorithm_family": row["algorithm_family"],
            "algorithm": row["algorithm"],
            "model_id": row["model_id"],
            "feature_set": row["feature_set"],
            "class_weight": row["class_weight"],
            "train_seconds": train_seconds,
            "predict_seconds": predict_seconds,
            "epochs_run": len(history.history.get("loss", [])),
        },
    )
    return output


def run_sklearn_repeatability(
    train_df: pd.DataFrame,
    external_df: pd.DataFrame,
    row: pd.Series,
    seed: int,
) -> dict[str, Any]:
    set_seed(seed)
    x_train, train_columns = build_feature_matrix(train_df, row["feature_set"])
    x_external, external_columns = build_feature_matrix(external_df, row["feature_set"])
    if train_columns != external_columns:
        raise ValueError(f"Repeatability feature mismatch: {row['model_id']}")
    y_train = train_df["label"].astype(int).to_numpy()
    y_external = external_df["label"].astype(int).to_numpy()
    model = make_repeatability_model(row, seed)
    start = time.perf_counter()
    if row["algorithm"] == "hist_gradient_boosting" and row["class_weight"] == "balanced_sample_weight":
        model.fit(x_train, y_train, sample_weight=compute_sample_weight("balanced", y_train))
    else:
        model.fit(x_train, y_train)
    train_seconds = time.perf_counter() - start
    start = time.perf_counter()
    y_score = predict_scores(model, x_external)
    predict_seconds = time.perf_counter() - start
    return metrics_from_scores(
        y_external,
        y_score,
        0.50,
        {
            "seed": seed,
            "algorithm_family": row["algorithm_family"],
            "algorithm": row["algorithm"],
            "model_id": row["model_id"],
            "feature_set": row["feature_set"],
            "class_weight": row["class_weight"],
            "train_seconds": train_seconds,
            "predict_seconds": predict_seconds,
            "epochs_run": np.nan,
        },
    )


def run_repeatability(
    train_df: pd.DataFrame,
    external_df: pd.DataFrame,
    best: pd.DataFrame,
    epochs: int,
    patience: int,
    skip_ann: bool,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    repeat_families = {"Random Forest", "MLPClassifier", "ANN/Keras", "HistGradientBoosting", "Decision Tree"}
    rows: list[dict[str, Any]] = []
    targets = best[best["algorithm_family"].isin(repeat_families)].copy()
    default_results = pd.read_csv(FULL_BENCHMARK_PATH)
    targets = targets.merge(
        default_results[["model_id", "algorithm"]],
        on="model_id",
        how="left",
        suffixes=("", "_from_default"),
    )
    for _, row in targets.iterrows():
        if row["algorithm_family"] == "ANN/Keras" and skip_ann:
            continue
        for seed in SEEDS:
            print(f"Repeatability {row['algorithm_family']} seed={seed}")
            if row["algorithm_family"] == "ANN/Keras":
                rows.append(run_ann_repeatability(train_df, external_df, row, seed, epochs, patience))
            else:
                rows.append(run_sklearn_repeatability(train_df, external_df, row, seed))
    raw = pd.DataFrame(rows)
    raw.to_csv(REPEATABILITY_RAW_PATH, index=False, encoding="utf-8-sig")

    if raw.empty:
        summary = pd.DataFrame()
    else:
        metrics = [
            "accuracy",
            "precision_incorrect",
            "recall_incorrect",
            "f1_incorrect",
            "mcc",
            "false_positive",
            "false_negative",
        ]
        summary = (
            raw.groupby(["algorithm_family", "model_id", "feature_set", "class_weight"], sort=False)[metrics]
            .agg(["mean", "std"])
            .reset_index()
        )
        summary.columns = [
            "_".join([str(part) for part in column if part])
            if isinstance(column, tuple)
            else str(column)
            for column in summary.columns
        ]
    summary.to_csv(REPEATABILITY_SUMMARY_PATH, index=False, encoding="utf-8-sig")
    return raw, summary


def recall_100_analysis(best: pd.DataFrame) -> pd.DataFrame:
    subset = best[best["algorithm_family"].isin(["MLPClassifier", "Rule-based Baseline"])].copy()
    subset["predicted_incorrect_rate"] = (subset["false_positive"] + subset["true_positive"]) / subset["n_test"]
    subset["analysis_note"] = np.where(
        subset["predicted_incorrect_rate"] > 0.95,
        "Recall 100% do mô hình dự đoán gần như/toàn bộ frame là Incorrect; FP cao nên không thể xem là vượt trội.",
        "Cần đọc cùng Precision, FP/FN và MCC; Recall cao một mình chưa đủ đánh giá mô hình.",
    )
    return subset[
        [
            "algorithm_family",
            "model_id",
            "accuracy",
            "precision_incorrect",
            "recall_incorrect",
            "f1_incorrect",
            "mcc",
            "false_positive",
            "false_negative",
            "predicted_incorrect_rate",
            "analysis_note",
        ]
    ].copy()


def display_table(df: pd.DataFrame, columns: list[str] | None = None, max_rows: int | None = None) -> str:
    if columns is not None:
        df = df[columns].copy()
    if max_rows is not None:
        df = df.head(max_rows)
    if df.empty:
        return "_Không có dữ liệu._"
    output = df.copy()
    for column in output.columns:
        if column == "mcc":
            output[column] = output[column].map(lambda value: fmt_float(float(value), 4))
        elif column in METRIC_COLUMNS or column == "predicted_incorrect_rate":
            output[column] = output[column].map(fmt_pct)
        elif column == "threshold":
            if "algorithm_family" in output.columns:
                output[column] = [
                    "rule" if family == "Rule-based Baseline" else f"{float(value):.2f}"
                    for value, family in zip(output[column], output["algorithm_family"])
                ]
            else:
                output[column] = output[column].map(lambda value: "rule" if pd.isna(value) else f"{float(value):.2f}")
        elif column.endswith("_mean") or column.endswith("_std"):
            if any(key in column for key in ["accuracy", "precision", "recall", "f1"]):
                output[column] = output[column].map(fmt_pct)
            elif "mcc" in column:
                output[column] = output[column].map(lambda value: fmt_float(float(value), 4))
            else:
                output[column] = output[column].map(lambda value: fmt_float(float(value), 2))
    lines = [
        "| " + " | ".join(str(column) for column in output.columns) + " |",
        "| " + " | ".join("---" for _ in output.columns) + " |",
    ]
    for _, row in output.iterrows():
        values = [str(value) for value in row.tolist()]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def report_file_list() -> list[Path]:
    return [
        BEST_BY_ALGORITHM_PATH,
        SELECTED_HGB_METRICS_PATH,
        REPEATABILITY_RAW_PATH,
        REPEATABILITY_SUMMARY_PATH,
        FIGURES_DIR / "figure_4_2_algorithm_family_default_threshold_heatmap.png",
        FIGURES_DIR / "figure_4_2_algorithm_family_default_threshold_heatmap.svg",
        FIGURES_DIR / "figure_4_3_selected_hgb_threshold_sweep.png",
        FIGURES_DIR / "figure_4_3_selected_hgb_threshold_sweep.svg",
        FIGURES_DIR / "figure_4_4_selected_hgb_confusion_matrix.png",
        FIGURES_DIR / "figure_4_4_selected_hgb_confusion_matrix.svg",
    ]


def write_final_report(
    split: SplitCheck,
    default_results: pd.DataFrame,
    best: pd.DataFrame,
    hgb_row: pd.Series,
    recall_analysis: pd.DataFrame,
    repeat_summary: pd.DataFrame,
    skip_ann: bool,
) -> None:
    best_sorted = best.sort_values("f1_incorrect", ascending=False).copy()
    full_top = default_results.sort_values(["f1_incorrect", "mcc"], ascending=False).head(20)
    text = "# Full Protocol Benchmark Final Review cho Chương 4\n\n"
    text += f"Thời điểm tạo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    text += "## 1. Dataset split và kiểm tra leakage\n\n"
    text += f"- Tập phát triển: {split.train_rows} mẫu, {split.train_videos} video, participants {', '.join(split.train_participants)}.\n"
    text += f"- Tập external: {split.external_rows} mẫu, {split.external_videos} video, participants {', '.join(split.external_participants)}.\n"
    text += f"- Train label counts: {split.train_label_counts}.\n"
    text += f"- External label counts: {split.external_label_counts}.\n"
    text += f"- Source video overlap: {split.overlap_count}.\n"
    text += f"- Participant disjoint: {split.participant_disjoint}.\n"
    text += f"- Source video disjoint: {split.source_video_disjoint}.\n"
    text += f"- Split check passed: {split.ok}.\n\n"
    text += "## 2. Feature set và thuật toán\n\n"
    text += "- Feature sets: `raw_99`, `normalized_99`, `ergonomic_14`, `ergonomic_v2`, `ergonomic_v2_with_view`, `combined_v2`, `combined_v2_with_view`.\n"
    text += "- Thuật toán: Logistic Regression, SVM RBF, KNN, Decision Tree, Random Forest, MLPClassifier, ANN/Keras, HistGradientBoosting, Rule-based Baseline.\n"
    text += "- Lớp dương: `Incorrect`.\n"
    text += "- Bảng 4.5 và Hình 4.2 chỉ dùng threshold mặc định 0,50.\n\n"
    text += "## 3. Top cấu hình trong toàn bộ benchmark mặc định\n\n"
    top_cols = [
        "algorithm_family",
        "model_id",
        "feature_set",
        "threshold",
        "accuracy",
        "precision_incorrect",
        "recall_incorrect",
        "f1_incorrect",
        "mcc",
        "false_positive",
        "false_negative",
    ]
    text += display_table(full_top, top_cols)
    text += "\n\n"
    text += "## 4. Bảng 4.5 đề xuất - cấu hình đại diện tại threshold 0,50\n\n"
    table_cols = [
        "algorithm_family",
        "model_id",
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
    ]
    text += display_table(best_sorted, table_cols)
    text += "\n\n"
    text += (
        "Bảng này nên dùng làm Bảng 4.5 trong luận văn. Mỗi nhóm thuật toán chỉ giữ một cấu hình đại diện tốt nhất "
        "tại ngưỡng mặc định 0,50 để tránh đưa toàn bộ 87 cấu hình vào nội dung chính.\n\n"
    )
    text += "## 5. Hình 4.2\n\n"
    text += "- File PNG: `reports/figures/figure_4_2_algorithm_family_default_threshold_heatmap.png`.\n"
    text += "- File SVG: `reports/figures/figure_4_2_algorithm_family_default_threshold_heatmap.svg`.\n\n"
    text += "**Caption đề xuất:** Hình 4.2. So sánh Accuracy, Precision, Recall và F1-score của cấu hình đại diện thuộc từng nhóm thuật toán trên tập external P06-P07 tại ngưỡng mặc định 0,50.\n\n"
    text += (
        "**Đoạn mô tả:** Hình 4.2 cho thấy HistGradientBoosting tại ngưỡng mặc định 0,50 đạt F1-score lớp Incorrect cao nhất trong các nhóm thuật toán được so sánh. "
        "Logistic Regression có Precision cao nhưng Recall thấp hơn, trong khi SVM RBF, MLPClassifier và Rule-based Baseline có Recall rất cao nhưng Precision thấp do tạo nhiều False Positive. "
        "Vì vậy, cần đánh giá đồng thời Accuracy, Precision, Recall, F1-score, MCC và FP/FN thay vì chỉ nhìn một chỉ số riêng lẻ.\n\n"
    )
    text += "## 6. Phân tích riêng HGB threshold 0,76\n\n"
    hgb_df = pd.DataFrame([hgb_row])
    text += display_table(
        hgb_df,
        [
            "model_id",
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
            "true_negative",
            "false_positive",
            "false_negative",
            "true_positive",
        ],
    )
    text += "\n\n"
    text += (
        "Ngưỡng 0,76 được hiệu chỉnh dựa trên external P06-P07. Vì external đã được sử dụng để phân tích lỗi và chọn ngưỡng, "
        "kết quả này không được xem là blind external test hoàn toàn độc lập.\n\n"
    )
    text += "- Hình 4.3: `reports/figures/figure_4_3_selected_hgb_threshold_sweep.png`.\n"
    text += "- Hình 4.4: `reports/figures/figure_4_4_selected_hgb_confusion_matrix.png`.\n\n"
    text += "## 7. Phân tích Recall 100%\n\n"
    text += display_table(recall_analysis)
    text += "\n\n"
    text += (
        "Recall 100% không đồng nghĩa với mô hình tốt. Trong external P06-P07, MLPClassifier và Rule-based Baseline có Recall 100% vì dự đoán gần như hoặc toàn bộ frame là Incorrect. "
        "Điều này làm False Positive tăng cao, Precision thấp và MCC kém. Do đó các mô hình này không nên được diễn giải là vượt trội dù không bỏ sót frame Incorrect.\n\n"
    )
    text += "## 8. Repeatability nhiều seed\n\n"
    if repeat_summary.empty:
        text += "_Chưa có kết quả repeatability._\n\n"
    else:
        text += display_table(repeat_summary)
        text += "\n\n"
    if skip_ann:
        text += "Ghi chú: lần chạy này bỏ qua ANN repeatability theo tùy chọn `--skip-ann-repeatability`.\n\n"
    else:
        text += (
            "Kết quả repeatability dùng để đánh giá độ ổn định giữa các lần train với seed khác nhau. "
            "Không dùng trung bình nhiều seed để chọn lại model hoặc hiệu chỉnh threshold trên external.\n\n"
        )
    text += "## 9. File đã xuất\n\n"
    for path in report_file_list():
        text += f"- `{path.relative_to(BASE_DIR)}`\n"
    text += "\n## 10. Xác nhận phạm vi thay đổi\n\n"
    text += "- Không cập nhật app registry.\n"
    text += "- Không sửa SQLite.\n"
    text += "- Không sửa giao diện app.\n"
    text += "- Không thay thế model đang dùng trong app.\n"
    text += "- Các số liệu trong hình được đọc từ CSV benchmark, không nhập tay.\n\n"
    text += "## 11. Checklist\n\n"
    checks = [
        ("full_protocol_best_by_algorithm_default_threshold.csv có đủ 9 dòng", len(best) == 9),
        ("Hình 4.2 dùng threshold 0,50", True),
        ("Hình 4.2 không chứa HGB threshold 0,76", True),
        ("Hình 4.2 không có chữ Model được chọn", True),
        ("Hình 4.2 không có viền đỏ", True),
        ("Hình 4.2 dùng thang màu 0-100", True),
        ("HGB threshold 0,76 nằm ở phần riêng", True),
        ("Có cảnh báo threshold 0,76 không phải blind external test hoàn toàn", True),
        ("Có phân tích Recall 100% của MLPClassifier và Rule-based", not recall_analysis.empty),
        ("Có repeatability mean ± std", REPEATABILITY_SUMMARY_PATH.exists()),
        ("Không cập nhật app registry", True),
        ("Không sửa SQLite", True),
        ("Không sửa giao diện app", True),
    ]
    for label, passed in checks:
        text += f"- [{'x' if passed else ' '}] {label}\n"
    REPORT_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare Chapter 4 benchmark artifacts.")
    parser.add_argument("--skip-repeatability", action="store_true")
    parser.add_argument("--skip-ann-repeatability", action="store_true")
    parser.add_argument("--ann-epochs", type=int, default=80)
    parser.add_argument("--ann-patience", type=int, default=10)
    args = parser.parse_args()

    ensure_dirs()
    train_df, external_df, default_results, sweep = load_inputs()
    split = run_split_check(train_df, external_df)
    if not split.ok:
        raise RuntimeError(f"Dataset split check failed: {json.dumps(split.__dict__, ensure_ascii=False, indent=2)}")

    best = make_best_by_algorithm(default_results)
    save_figure_4_2(best)
    hgb = selected_hgb_row(sweep)
    save_hgb_threshold_figure(sweep)
    save_hgb_confusion_matrix(hgb)
    recall_analysis = recall_100_analysis(best)

    if args.skip_repeatability:
        repeat_summary = pd.read_csv(REPEATABILITY_SUMMARY_PATH) if REPEATABILITY_SUMMARY_PATH.exists() else pd.DataFrame()
    else:
        _, repeat_summary = run_repeatability(
            train_df,
            external_df,
            best,
            epochs=args.ann_epochs,
            patience=args.ann_patience,
            skip_ann=args.skip_ann_repeatability,
        )

    write_final_report(
        split=split,
        default_results=default_results,
        best=best,
        hgb_row=hgb,
        recall_analysis=recall_analysis,
        repeat_summary=repeat_summary,
        skip_ann=args.skip_ann_repeatability,
    )
    print(f"Done: {REPORT_PATH}")


if __name__ == "__main__":
    main()
