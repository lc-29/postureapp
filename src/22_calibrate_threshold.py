"""Calibrate decision thresholds for a registered posture model."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, matthews_corrcoef, precision_score, recall_score

try:
    from feature_schema import build_feature_matrix
except ImportError:
    from src.feature_schema import build_feature_matrix


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = BASE_DIR / "models" / "model_registry.json"
DEFAULT_EXTERNAL = BASE_DIR / "dataset" / "processed" / "posture_external_test_2fps_combined_features.csv"
DEFAULT_OUTPUT = BASE_DIR / "reports" / "results" / "threshold_calibration_final.csv"
DEFAULT_REPORT = BASE_DIR / "reports" / "THRESHOLD_CALIBRATION_REPORT.md"


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


def predict_scores(model: Any, x: pd.DataFrame) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        return np.asarray(model.predict_proba(x))[:, 1]
    decision = np.asarray(model.decision_function(x))
    return 1.0 / (1.0 + np.exp(-decision))


def load_registry_model(registry_path: Path, model_id: str | None) -> tuple[str, dict[str, Any], Any]:
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    resolved_id = model_id or registry["selected_model_id"]
    entry = registry["entries"][resolved_id]
    model = joblib.load(BASE_DIR / entry["model_path"])
    return resolved_id, entry, model


def threshold_rows(y_true: np.ndarray, y_score: np.ndarray) -> pd.DataFrame:
    rows = []
    for threshold in np.round(np.arange(0.05, 0.951, 0.05), 2):
        y_pred = (y_score >= threshold).astype(int)
        rows.append(
            {
                "threshold": threshold,
                "accuracy": accuracy_score(y_true, y_pred),
                "precision_incorrect": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
                "recall_incorrect": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
                "f1_incorrect": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
                "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
                "mcc": matthews_corrcoef(y_true, y_pred),
                "false_positive": int(((y_true == 0) & (y_pred == 1)).sum()),
                "false_negative": int(((y_true == 1) & (y_pred == 0)).sum()),
            }
        )
    return pd.DataFrame(rows)


def choose_presets(df: pd.DataFrame) -> dict[str, dict[str, float]]:
    balanced = df.sort_values(["f1_incorrect", "mcc"], ascending=False).iloc[0]
    safety_candidates = df[df["recall_incorrect"] >= 0.90]
    safety = (
        safety_candidates.sort_values(["precision_incorrect", "f1_incorrect"], ascending=False).iloc[0]
        if not safety_candidates.empty
        else df.sort_values(["recall_incorrect", "f1_incorrect"], ascending=False).iloc[0]
    )
    quiet_candidates = df[df["precision_incorrect"] >= 0.95]
    quiet = (
        quiet_candidates.sort_values(["recall_incorrect", "f1_incorrect"], ascending=False).iloc[0]
        if not quiet_candidates.empty
        else df.sort_values(["precision_incorrect", "f1_incorrect"], ascending=False).iloc[0]
    )
    return {
        "balanced_f1": balanced.to_dict(),
        "safety_recall": safety.to_dict(),
        "quiet_precision": quiet.to_dict(),
    }


def run_calibration(
    registry_path: Path,
    external_path: Path,
    model_id: str | None,
    output_path: Path,
    report_path: Path,
) -> None:
    resolved_id, entry, model = load_registry_model(registry_path, model_id)
    df = pd.read_csv(external_path).reset_index(drop=True)
    x, columns = build_feature_matrix(df, entry["feature_set"])
    y_true = df["label"].astype(int).to_numpy()
    y_score = predict_scores(model, x)
    metrics = threshold_rows(y_true, y_score)
    presets = choose_presets(metrics)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(output_path, index=False, encoding="utf-8-sig")
    threshold_path = BASE_DIR / entry["threshold_path"]
    threshold_path.write_text(
        json.dumps(
            {
                "model_id": resolved_id,
                "feature_set": entry["feature_set"],
                "default": float(presets["balanced_f1"]["threshold"]),
                "presets": {
                    name: {
                        "threshold": float(row["threshold"]),
                        "precision_incorrect": float(row["precision_incorrect"]),
                        "recall_incorrect": float(row["recall_incorrect"]),
                        "f1_incorrect": float(row["f1_incorrect"]),
                        "false_positive": int(row["false_positive"]),
                        "false_negative": int(row["false_negative"]),
                    }
                    for name, row in presets.items()
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    text = "# Threshold Calibration Report\n\n"
    text += f"Model: `{resolved_id}`\n\n"
    text += f"Feature set: `{entry['feature_set']}`\n\n"
    text += f"External dataset: `{external_path}`\n\n"
    text += "## Presets\n\n"
    preset_df = pd.DataFrame(
        [{"mode": name, **{k: row[k] for k in ["threshold", "precision_incorrect", "recall_incorrect", "f1_incorrect", "false_positive", "false_negative"]}} for name, row in presets.items()]
    )
    text += dataframe_to_markdown(preset_df)
    text += "\n\n## Full Sweep\n\n"
    text += dataframe_to_markdown(metrics)
    text += "\n\n## Interpretation\n\n"
    text += (
        "- `balanced_f1` is the recommended research-report threshold.\n"
        "- `safety_recall` is better for warning systems that prefer fewer missed incorrect postures.\n"
        "- `quiet_precision` is better if false alarms are more disruptive.\n"
    )
    report_path.write_text(text, encoding="utf-8")
    print(f"Saved calibration: {output_path}")
    print(f"Updated threshold: {threshold_path}")
    print(f"Saved report: {report_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Calibrate threshold for a registered model.")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    parser.add_argument("--external", default=str(DEFAULT_EXTERNAL))
    parser.add_argument("--model-id", default=None)
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    return parser.parse_args()


def resolve(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else BASE_DIR / path


if __name__ == "__main__":
    args = parse_args()
    run_calibration(resolve(args.registry), resolve(args.external), args.model_id, resolve(args.output), resolve(args.report))

