"""Train candidate posture models and save a reproducible model registry."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    f1_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

try:
    from feature_schema import SUPPORTED_FEATURE_SETS, build_feature_matrix, save_feature_schema
except ImportError:
    from src.feature_schema import SUPPORTED_FEATURE_SETS, build_feature_matrix, save_feature_schema


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_TRAIN = BASE_DIR / "dataset" / "processed" / "posture_data_2fps_combined_features.csv"
DEFAULT_EXTERNAL = BASE_DIR / "dataset" / "processed" / "posture_external_test_2fps_combined_features.csv"
DEFAULT_REGISTRY_DIR = BASE_DIR / "models" / "registry"
DEFAULT_REGISTRY = BASE_DIR / "models" / "model_registry.json"
DEFAULT_REPORT = BASE_DIR / "reports" / "MODEL_SELECTION_REPORT.md"
DEFAULT_RESULTS = BASE_DIR / "reports" / "results" / "model_registry_metrics.csv"
SEED = 42


def candidate_models() -> list[tuple[str, Any]]:
    return [
        (
            "logistic_regression",
            Pipeline(
                [
                    ("scaler", StandardScaler()),
                    (
                        "model",
                        LogisticRegression(max_iter=1000, class_weight="balanced", random_state=SEED),
                    ),
                ]
            ),
        ),
        (
            "svm_rbf",
            Pipeline(
                [
                    ("scaler", StandardScaler()),
                    (
                        "model",
                        SVC(kernel="rbf", C=3.0, gamma="scale", probability=True, class_weight="balanced"),
                    ),
                ]
            ),
        ),
        (
            "random_forest",
            RandomForestClassifier(n_estimators=250, class_weight="balanced", random_state=SEED, n_jobs=-1),
        ),
        (
            "hist_gradient_boosting",
            HistGradientBoostingClassifier(max_iter=200, random_state=SEED),
        ),
        (
            "mlp_sklearn",
            Pipeline(
                [
                    ("scaler", StandardScaler()),
                    (
                        "model",
                        MLPClassifier(
                            hidden_layer_sizes=(96, 48),
                            activation="relu",
                            alpha=1e-4,
                            early_stopping=True,
                            max_iter=160,
                            random_state=SEED,
                        ),
                    ),
                ]
            ),
        ),
    ]


def predict_scores(model: Any, x_test: pd.DataFrame | np.ndarray) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        return np.asarray(model.predict_proba(x_test))[:, 1]
    if hasattr(model, "decision_function"):
        decision = np.asarray(model.decision_function(x_test))
        return 1.0 / (1.0 + np.exp(-decision))
    return np.asarray(model.predict(x_test)).astype(float)


def metrics_row(
    model_id: str,
    algorithm: str,
    feature_set: str,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_score: np.ndarray,
    train_seconds: float,
    predict_seconds: float,
    feature_count: int,
) -> dict[str, Any]:
    return {
        "model_id": model_id,
        "algorithm": algorithm,
        "feature_set": feature_set,
        "feature_count": feature_count,
        "accuracy": accuracy_score(y_true, y_pred),
        "precision_incorrect": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
        "recall_incorrect": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
        "f1_incorrect": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "mcc": matthews_corrcoef(y_true, y_pred),
        "roc_auc": roc_auc_score(y_true, y_score),
        "pr_auc": average_precision_score(y_true, y_score),
        "brier_score": brier_score_loss(y_true, y_score),
        "train_seconds": round(train_seconds, 3),
        "predict_seconds": round(predict_seconds, 3),
    }


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for _, row in df.iterrows():
        values = []
        for column in headers:
            value = row[column]
            values.append(f"{value:.6f}" if isinstance(value, float) else str(value))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def train_registry(
    train_path: Path,
    external_path: Path,
    registry_dir: Path,
    registry_path: Path,
    report_path: Path,
    results_path: Path,
    feature_sets: list[str],
) -> None:
    train_df = pd.read_csv(train_path).reset_index(drop=True)
    external_df = pd.read_csv(external_path).reset_index(drop=True)
    y_train = train_df["label"].astype(int).to_numpy()
    y_external = external_df["label"].astype(int).to_numpy()
    registry_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    entries: dict[str, Any] = {}
    feature_cache: dict[str, tuple[pd.DataFrame, pd.DataFrame, list[str]]] = {}

    for feature_set in feature_sets:
        x_train, columns = build_feature_matrix(train_df, feature_set)
        x_external, external_columns = build_feature_matrix(external_df, feature_set)
        if columns != external_columns:
            raise ValueError(f"Column mismatch for {feature_set}")
        feature_cache[feature_set] = (x_train, x_external, columns)

        for algorithm, model in candidate_models():
            model_id = f"{algorithm}__{feature_set}"
            model_dir = registry_dir / model_id
            model_dir.mkdir(parents=True, exist_ok=True)
            start = time.perf_counter()
            model.fit(x_train, y_train)
            train_seconds = time.perf_counter() - start
            predict_start = time.perf_counter()
            y_score = predict_scores(model, x_external)
            y_pred = (y_score >= 0.5).astype(int)
            predict_seconds = time.perf_counter() - predict_start
            row = metrics_row(
                model_id,
                algorithm,
                feature_set,
                y_external,
                y_pred,
                y_score,
                train_seconds,
                predict_seconds,
                len(columns),
            )
            rows.append(row)
            joblib.dump(model, model_dir / "model.pkl")
            save_feature_schema(model_dir / "feature_schema.json", feature_set, columns)
            (model_dir / "threshold.json").write_text(
                json.dumps({"default": 0.5, "source": "initial registry training"}, indent=2),
                encoding="utf-8",
            )
            (model_dir / "metrics.json").write_text(json.dumps(row, indent=2), encoding="utf-8")
            entries[model_id] = {
                "model_id": model_id,
                "algorithm": algorithm,
                "feature_set": feature_set,
                "feature_count": len(columns),
                "model_path": str((model_dir / "model.pkl").relative_to(BASE_DIR)),
                "feature_schema_path": str((model_dir / "feature_schema.json").relative_to(BASE_DIR)),
                "threshold_path": str((model_dir / "threshold.json").relative_to(BASE_DIR)),
                "metrics_path": str((model_dir / "metrics.json").relative_to(BASE_DIR)),
                "metrics": row,
            }
            print(f"trained {model_id}: f1={row['f1_incorrect']:.4f}")

    metrics_df = pd.DataFrame(rows).sort_values(
        ["f1_incorrect", "recall_incorrect", "mcc"], ascending=False
    )
    results_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_df.to_csv(results_path, index=False, encoding="utf-8-sig")
    best = metrics_df.iloc[0].to_dict()
    registry = {
        "created_at": "2026-05-28",
        "train_dataset": str(train_path.relative_to(BASE_DIR)),
        "external_dataset": str(external_path.relative_to(BASE_DIR)),
        "selection_metric": "f1_incorrect, then recall_incorrect, then mcc",
        "selected_model_id": best["model_id"],
        "entries": entries,
    }
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    text = "# Model Selection Report\n\n"
    text += f"Train dataset: `{train_path}`\n\n"
    text += f"External dataset: `{external_path}`\n\n"
    text += f"Registry: `{registry_path}`\n\n"
    text += f"Selected model: `{best['model_id']}`\n\n"
    text += "Selection rule: highest incorrect-class F1, then recall, then MCC.\n\n"
    text += "## Ranked Models\n\n"
    display_cols = [
        "model_id",
        "feature_count",
        "accuracy",
        "precision_incorrect",
        "recall_incorrect",
        "f1_incorrect",
        "macro_f1",
        "mcc",
        "roc_auc",
        "pr_auc",
        "predict_seconds",
    ]
    text += dataframe_to_markdown(metrics_df[display_cols].head(20))
    text += "\n\n## Interpretation\n\n"
    text += (
        "- The selected model is the best model within this local protocol only.\n"
        "- It must not be described as state-of-the-art against literature because datasets and protocols differ.\n"
        "- If the selected model is not the current ANN app model, the app should load this registry before deployment.\n"
    )
    report_path.write_text(text, encoding="utf-8")
    print(f"Saved registry: {registry_path}")
    print(f"Saved report: {report_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train candidate models and write model registry.")
    parser.add_argument("--train", default=str(DEFAULT_TRAIN))
    parser.add_argument("--external", default=str(DEFAULT_EXTERNAL))
    parser.add_argument("--registry-dir", default=str(DEFAULT_REGISTRY_DIR))
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--results", default=str(DEFAULT_RESULTS))
    parser.add_argument(
        "--feature-sets",
        nargs="+",
        default=[
            "raw_99",
            "ergonomic_14",
            "combined_raw_ergonomic",
            "normalized_99",
            "combined_normalized_ergonomic",
        ],
        choices=SUPPORTED_FEATURE_SETS,
    )
    return parser.parse_args()


def resolve(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else BASE_DIR / path


if __name__ == "__main__":
    args = parse_args()
    train_registry(
        resolve(args.train),
        resolve(args.external),
        resolve(args.registry_dir),
        resolve(args.registry),
        resolve(args.report),
        resolve(args.results),
        args.feature_sets,
    )

