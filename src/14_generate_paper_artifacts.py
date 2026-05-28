"""Generate figures and table snapshots for the report/paper."""

from __future__ import annotations

from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "reports" / "results"
FIGURES_DIR = BASE_DIR / "reports" / "figures"
TABLES_DIR = BASE_DIR / "reports" / "tables"


def ensure_dirs() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)


def copy_table(source_name: str, target_name: str) -> None:
    source = RESULTS_DIR / source_name
    if source.exists():
        pd.read_csv(source).to_csv(TABLES_DIR / target_name, index=False, encoding="utf-8-sig")


def plot_confusion_matrix() -> None:
    path = RESULTS_DIR / "external_confusion_matrix.csv"
    if not path.exists():
        return
    cm_df = pd.read_csv(path, index_col=0)
    values = cm_df.to_numpy(dtype=float)

    fig, ax = plt.subplots(figsize=(5.5, 4.8))
    image = ax.imshow(values, cmap="Blues")
    ax.set_xticks(range(values.shape[1]), labels=["Pred correct", "Pred incorrect"])
    ax.set_yticks(range(values.shape[0]), labels=["True correct", "True incorrect"])
    ax.set_title("External Confusion Matrix")
    for row in range(values.shape[0]):
        for col in range(values.shape[1]):
            ax.text(col, row, f"{int(values[row, col])}", ha="center", va="center")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "external_confusion_matrix.png", dpi=180)
    plt.close(fig)


def plot_threshold_curve() -> None:
    path = RESULTS_DIR / "external_threshold_sweep.csv"
    if not path.exists():
        return
    df = pd.read_csv(path)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(df["threshold"], df["f1"], marker="o", label="F1 incorrect")
    ax.plot(df["threshold"], df["precision"], marker=".", label="Precision incorrect")
    ax.plot(df["threshold"], df["recall"], marker=".", label="Recall incorrect")
    ax.set_xlabel("Decision threshold")
    ax.set_ylabel("Score")
    ax.set_title("External Threshold Sweep")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "external_threshold_sweep.png", dpi=180)
    plt.close(fig)


def plot_tpri_distribution() -> None:
    path = RESULTS_DIR / "session_risk_index.csv"
    if not path.exists():
        return
    df = pd.read_csv(path)
    if "temporal_risk_index" not in df.columns or df.empty:
        return
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(df["temporal_risk_index"], bins=np.linspace(0, 100, 11), color="#2563eb", alpha=0.85)
    ax.set_xlabel("Temporal Posture Risk Index")
    ax.set_ylabel("Session count")
    ax.set_title("Session Risk Distribution")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "tpri_distribution.png", dpi=180)
    plt.close(fig)


def write_pipeline_diagram() -> None:
    text = """# System Pipeline Diagram

```mermaid
flowchart LR
    A["Webcam / IP camera / Video file"] --> B["OpenCV frame capture"]
    B --> C["MediaPipe Pose landmarks"]
    C --> D["99 landmark features"]
    D --> E["ANN classifier"]
    C --> F["Rule-based ergonomic indicators"]
    E --> G["Realtime status and alert logic"]
    F --> G
    G --> H["SQLite session and posture logs"]
    H --> I["Dashboard statistics"]
    H --> J["Temporal Posture Risk Index"]
```
"""
    (FIGURES_DIR / "system_pipeline_mermaid.md").write_text(text, encoding="utf-8")


def write_artifact_index() -> None:
    text = f"""# Paper Artifacts

Generated figures:

- `reports/figures/external_confusion_matrix.png`
- `reports/figures/external_threshold_sweep.png`
- `reports/figures/tpri_distribution.png`
- `reports/figures/system_pipeline_mermaid.md`
- `reports/results/roc_curve.png`
- `reports/results/pr_curve.png`
- `reports/results/calibration_curve.png`

Generated table snapshots:

- `reports/tables/algorithm_benchmark_full.csv`
- `reports/tables/ablation_full.csv`
- `reports/tables/video_wise_metrics.csv`
- `reports/tables/external_threshold_sweep.csv`
- `reports/tables/classifier_benchmark_external.csv`
- `reports/tables/feature_ablation.csv`
- `reports/tables/participant_wise_metrics_raw.csv`
- `reports/tables/participant_wise_metrics_combined.csv`
- `reports/tables/runtime_benchmark_summary.csv`
- `reports/tables/video_manifest.csv`

Note: GUI screenshots still require a manual or Playwright-style desktop capture because this is a Tkinter desktop app.
"""
    (BASE_DIR / "reports" / "PAPER_ARTIFACTS.md").write_text(text, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    plot_confusion_matrix()
    plot_threshold_curve()
    plot_tpri_distribution()
    write_pipeline_diagram()
    copy_table("algorithm_benchmark_full.csv", "algorithm_benchmark_full.csv")
    copy_table("ablation_full.csv", "ablation_full.csv")
    copy_table("video_wise_metrics.csv", "video_wise_metrics.csv")
    copy_table("external_threshold_sweep.csv", "external_threshold_sweep.csv")
    copy_table("classifier_benchmark_external.csv", "classifier_benchmark_external.csv")
    copy_table("feature_ablation.csv", "feature_ablation.csv")
    copy_table("participant_wise_metrics_raw.csv", "participant_wise_metrics_raw.csv")
    copy_table("participant_wise_metrics_combined.csv", "participant_wise_metrics_combined.csv")
    copy_table("runtime_benchmark_summary.csv", "runtime_benchmark_summary.csv")
    manifest_path = BASE_DIR / "dataset" / "metadata" / "video_manifest.csv"
    if manifest_path.exists():
        pd.read_csv(manifest_path).to_csv(TABLES_DIR / "video_manifest.csv", index=False, encoding="utf-8-sig")
    write_artifact_index()
    print(f"Generated figures in {FIGURES_DIR}")
    print(f"Generated tables in {TABLES_DIR}")


if __name__ == "__main__":
    main()
