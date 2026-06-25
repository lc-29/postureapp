"""Run final external, video-wise, and participant-wise evaluation protocol."""

from __future__ import annotations

import argparse
import json
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
from statsmodels.stats.proportion import proportion_confint

try:
    from feature_schema import build_feature_matrix
except ImportError:
    from src.feature_schema import build_feature_matrix


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = BASE_DIR / "models" / "model_registry.json"
DEFAULT_TRAIN = BASE_DIR / "dataset" / "processed" / "posture_data_2fps_combined_features.csv"
DEFAULT_EXTERNAL = BASE_DIR / "dataset" / "processed" / "posture_external_test_2fps_combined_features.csv"
RESULTS_DIR = BASE_DIR / "reports" / "results"
DEFAULT_REPORT = BASE_DIR / "reports" / "FINAL_EVALUATION_REPORT.md"
SEED = 42


def make_model(algorithm: str) -> Any:
    if algorithm == "logistic_regression":
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=SEED)),
            ]
        )
    if algorithm == "svm_rbf":
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", SVC(kernel="rbf", C=3.0, gamma="scale", probability=True, class_weight="balanced")),
            ]
        )
    if algorithm == "random_forest":
        return RandomForestClassifier(n_estimators=250, class_weight="balanced", random_state=SEED, n_jobs=-1)
    if algorithm == "hist_gradient_boosting":
        return HistGradientBoostingClassifier(max_iter=200, random_state=SEED)
    if algorithm == "mlp_sklearn":
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "model",
                    MLPClassifier(
                        hidden_layer_sizes=(96, 48),
                        early_stopping=True,
                        max_iter=160,
                        random_state=SEED,
                    ),
                ),
            ]
        )
    raise ValueError(f"Unsupported algorithm: {algorithm}")


def predict_scores(model: Any, x: pd.DataFrame) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        return np.asarray(model.predict_proba(x))[:, 1]
    decision = np.asarray(model.decision_function(x))
    return 1.0 / (1.0 + np.exp(-decision))


def metric_dict(y_true: np.ndarray, y_score: np.ndarray, threshold: float) -> dict[str, Any]:
    y_pred = (y_score >= threshold).astype(int)
    correct = int((y_true == y_pred).sum())
    ci_low, ci_high = proportion_confint(correct, len(y_true), alpha=0.05, method="wilson")
    return {
        "n": len(y_true),
        "threshold": threshold,
        "accuracy": accuracy_score(y_true, y_pred),
        "accuracy_ci_low": ci_low,
        "accuracy_ci_high": ci_high,
        "precision_incorrect": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
        "recall_incorrect": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
        "f1_incorrect": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "mcc": matthews_corrcoef(y_true, y_pred),
        "roc_auc": roc_auc_score(y_true, y_score) if len(set(y_true.tolist())) == 2 else "",
        "pr_auc": average_precision_score(y_true, y_score) if len(set(y_true.tolist())) == 2 else "",
        "brier_score": brier_score_loss(y_true, y_score),
        "false_positive": int(((y_true == 0) & (y_pred == 1)).sum()),
        "false_negative": int(((y_true == 1) & (y_pred == 0)).sum()),
    }


def bootstrap_f1_ci(y_true: np.ndarray, y_score: np.ndarray, threshold: float, n_bootstrap: int = 400) -> tuple[float, float]:
    rng = np.random.default_rng(SEED)
    values = []
    indexes = np.arange(len(y_true))
    for _ in range(n_bootstrap):
        sample = rng.choice(indexes, size=len(indexes), replace=True)
        y_pred = (y_score[sample] >= threshold).astype(int)
        values.append(f1_score(y_true[sample], y_pred, pos_label=1, zero_division=0))
    return float(np.percentile(values, 2.5)), float(np.percentile(values, 97.5))


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No data._"
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


def load_registry(registry_path: Path, model_id: str | None) -> tuple[str, dict[str, Any], Any, float]:
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    resolved_id = model_id or registry["selected_model_id"]
    entry = registry["entries"][resolved_id]
    model = joblib.load(BASE_DIR / entry["model_path"])
    threshold_path = BASE_DIR / entry["threshold_path"]
    threshold = 0.5
    if threshold_path.exists():
        payload = json.loads(threshold_path.read_text(encoding="utf-8"))
        threshold = float(payload.get("default", threshold))
    return resolved_id, entry, model, threshold


def run_final_protocol(registry_path: Path, train_path: Path, external_path: Path, model_id: str | None, report_path: Path) -> None:
    resolved_id, entry, model, threshold = load_registry(registry_path, model_id)
    train_df = pd.read_csv(train_path).reset_index(drop=True)
    external_df = pd.read_csv(external_path).reset_index(drop=True)
    x_external, _ = build_feature_matrix(external_df, entry["feature_set"])
    y_external = external_df["label"].astype(int).to_numpy()
    y_score = predict_scores(model, x_external)
    y_pred = (y_score >= threshold).astype(int)

    external_metrics = metric_dict(y_external, y_score, threshold)
    f1_low, f1_high = bootstrap_f1_ci(y_external, y_score, threshold)
    external_metrics.update(
        {
            "protocol": "corrected_external_frame_level",
            "model_id": resolved_id,
            "feature_set": entry["feature_set"],
            "f1_ci_low": f1_low,
            "f1_ci_high": f1_high,
        }
    )
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([external_metrics]).to_csv(RESULTS_DIR / "final_evaluation_metrics.csv", index=False, encoding="utf-8-sig")

    predictions = external_df.copy()
    predictions["prob_incorrect"] = y_score
    predictions["pred_label"] = y_pred
    predictions["error_type"] = "correct"
    predictions.loc[(predictions["label"] == 0) & (predictions["pred_label"] == 1), "error_type"] = "false_positive"
    predictions.loc[(predictions["label"] == 1) & (predictions["pred_label"] == 0), "error_type"] = "false_negative"
    predictions.to_csv(RESULTS_DIR / "final_external_predictions.csv", index=False, encoding="utf-8-sig")

    video_rows = []
    for source_video, group in predictions.groupby("source_video", sort=True):
        group_score = group["prob_incorrect"].to_numpy()
        group_true = group["label"].astype(int).to_numpy()
        row = metric_dict(group_true, group_score, threshold)
        row.update(
            {
                "source_video": source_video,
                "participant_id": group["participant_id"].mode().iloc[0] if "participant_id" in group.columns else "",
                "view_angle": group["view_angle"].mode().iloc[0] if "view_angle" in group.columns else "",
                "label": int(group["label"].mode().iloc[0]),
            }
        )
        video_rows.append(row)
    video_df = pd.DataFrame(video_rows).sort_values("accuracy")
    video_df.to_csv(RESULTS_DIR / "final_video_wise_metrics.csv", index=False, encoding="utf-8-sig")

    participant_rows = []
    algorithm = entry["algorithm"]
    feature_set = entry["feature_set"]
    for participant in sorted(train_df["participant_id"].dropna().astype(str).unique()):
        fold_train = train_df[train_df["participant_id"].astype(str) != participant].reset_index(drop=True)
        fold_test = train_df[train_df["participant_id"].astype(str) == participant].reset_index(drop=True)
        if fold_train.empty or fold_test.empty:
            continue
        x_train, _ = build_feature_matrix(fold_train, feature_set)
        y_train = fold_train["label"].astype(int).to_numpy()
        x_test, _ = build_feature_matrix(fold_test, feature_set)
        y_test = fold_test["label"].astype(int).to_numpy()
        fold_model = make_model(algorithm)
        fold_model.fit(x_train, y_train)
        fold_score = predict_scores(fold_model, x_test)
        row = metric_dict(y_test, fold_score, threshold)
        row.update({"held_out_participant": participant, "model_id": resolved_id, "feature_set": feature_set})
        participant_rows.append(row)
    participant_df = pd.DataFrame(participant_rows).sort_values("held_out_participant")
    participant_df.to_csv(RESULTS_DIR / "final_participant_wise_metrics.csv", index=False, encoding="utf-8-sig")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    text = "# Final Evaluation Report\n\n"
    text += f"Model: `{resolved_id}`\n\nFeature set: `{feature_set}`\n\nThreshold: `{threshold:.4f}`\n\n"
    text += "## External Frame-Level Result\n\n"
    text += dataframe_to_markdown(pd.DataFrame([external_metrics]))
    text += "\n\n## Worst External Videos\n\n"
    text += dataframe_to_markdown(video_df.head(10)[["source_video", "label", "n", "accuracy", "precision_incorrect", "recall_incorrect", "f1_incorrect", "false_positive", "false_negative"]])
    text += "\n\n## Participant-Wise Raw Dataset Result\n\n"
    if not participant_df.empty:
        summary = participant_df[["accuracy", "f1_incorrect", "macro_f1", "mcc"]].agg(["mean", "std"]).reset_index()
        text += dataframe_to_markdown(summary)
        text += "\n\n"
        text += dataframe_to_markdown(participant_df[["held_out_participant", "n", "accuracy", "precision_incorrect", "recall_incorrect", "f1_incorrect", "mcc"]])
    else:
        text += "_No participant-wise metrics generated._"
    text += "\n\n## Claim Boundary\n\n"
    text += (
        "These results are suitable for the project final protocol. They still should not be described as "
        "state-of-the-art because the external set is project-specific and currently limited in participant diversity.\n"
    )
    report_path.write_text(text, encoding="utf-8")
    print(f"Saved final metrics in {RESULTS_DIR}")
    print(f"Saved report: {report_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run final evaluation protocol.")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    parser.add_argument("--train", default=str(DEFAULT_TRAIN))
    parser.add_argument("--external", default=str(DEFAULT_EXTERNAL))
    parser.add_argument("--model-id", default=None)
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    return parser.parse_args()


def resolve(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else BASE_DIR / path


if __name__ == "__main__":
    args = parse_args()
    run_final_protocol(resolve(args.registry), resolve(args.train), resolve(args.external), args.model_id, resolve(args.report))

