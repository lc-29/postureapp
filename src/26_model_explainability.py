"""Generate feature-importance report for the selected registry model."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import joblib
import matplotlib
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance

matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    from feature_schema import build_feature_matrix
except ImportError:
    from src.feature_schema import build_feature_matrix


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = BASE_DIR / "models" / "model_registry.json"
DEFAULT_DATASET = BASE_DIR / "dataset" / "processed" / "posture_external_test_2fps_combined_features.csv"
DEFAULT_OUTPUT = BASE_DIR / "reports" / "results" / "feature_importance.csv"
DEFAULT_REPORT = BASE_DIR / "reports" / "FEATURE_IMPORTANCE_REPORT.md"
DEFAULT_FIGURE = BASE_DIR / "reports" / "figures" / "feature_importance_top20.png"
SEED = 42


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


def load_model(registry_path: Path, model_id: str | None) -> tuple[str, dict[str, Any], Any]:
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    resolved_id = model_id or registry["selected_model_id"]
    entry = registry["entries"][resolved_id]
    return resolved_id, entry, joblib.load(BASE_DIR / entry["model_path"])


def direct_importance(model: Any, columns: list[str]) -> pd.DataFrame | None:
    estimator = model
    if hasattr(model, "named_steps"):
        estimator = model.named_steps.get("model", model)
    if hasattr(estimator, "feature_importances_"):
        values = np.asarray(estimator.feature_importances_)
    elif hasattr(estimator, "coef_"):
        values = np.abs(np.asarray(estimator.coef_)).ravel()
    else:
        return None
    return pd.DataFrame({"feature": columns, "importance_mean": values, "importance_std": 0.0})


def run_explainability(
    registry_path: Path,
    dataset_path: Path,
    model_id: str | None,
    output_path: Path,
    report_path: Path,
    figure_path: Path,
    max_rows: int,
) -> None:
    resolved_id, entry, model = load_model(registry_path, model_id)
    df = pd.read_csv(dataset_path).reset_index(drop=True)
    x, columns = build_feature_matrix(df, entry["feature_set"])
    y = df["label"].astype(int).to_numpy()
    if len(x) > max_rows:
        sample = x.sample(n=max_rows, random_state=SEED)
        y_sample = y[sample.index.to_numpy()]
    else:
        sample = x
        y_sample = y

    importance = direct_importance(model, columns)
    method = "direct_model_importance"
    if importance is None:
        result = permutation_importance(
            model,
            sample,
            y_sample,
            n_repeats=5,
            random_state=SEED,
            scoring="f1",
            n_jobs=-1,
        )
        importance = pd.DataFrame(
            {
                "feature": columns,
                "importance_mean": result.importances_mean,
                "importance_std": result.importances_std,
            }
        )
        method = "permutation_importance_f1"

    importance = importance.sort_values("importance_mean", ascending=False).reset_index(drop=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    importance.to_csv(output_path, index=False, encoding="utf-8-sig")

    top = importance.head(20).iloc[::-1]
    figure_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.barh(top["feature"], top["importance_mean"], xerr=top["importance_std"] if "importance_std" in top else None)
    ax.set_title(f"Top 20 Feature Importance ({resolved_id})")
    ax.set_xlabel("Importance")
    fig.tight_layout()
    fig.savefig(figure_path, dpi=180)
    plt.close(fig)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    text = "# Feature Importance Report\n\n"
    text += f"Model: `{resolved_id}`\n\n"
    text += f"Feature set: `{entry['feature_set']}`\n\n"
    text += f"Method: `{method}`\n\n"
    text += "## Top 20 Features\n\n"
    text += dataframe_to_markdown(importance.head(20))
    text += "\n\n## Interpretation\n\n"
    text += (
        "Feature importance helps explain which geometric indicators influence the selected model. "
        "For SVM/ANN models, permutation importance is an approximate diagnostic and should be interpreted with care.\n"
    )
    report_path.write_text(text, encoding="utf-8")
    print(f"Saved importance: {output_path}")
    print(f"Saved report: {report_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Explain selected registry model.")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--model-id", default=None)
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--figure", default=str(DEFAULT_FIGURE))
    parser.add_argument("--max-rows", type=int, default=1200)
    return parser.parse_args()


def resolve(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else BASE_DIR / path


if __name__ == "__main__":
    args = parse_args()
    run_explainability(
        resolve(args.registry),
        resolve(args.dataset),
        args.model_id,
        resolve(args.output),
        resolve(args.report),
        resolve(args.figure),
        args.max_rows,
    )

