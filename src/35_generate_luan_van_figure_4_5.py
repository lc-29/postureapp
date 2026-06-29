"""Generate thesis Figure 4.5: selected model metrics by participant."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "reports" / "results"
FIGURES_DIR = BASE_DIR / "reports" / "figures"
TABLES_DIR = BASE_DIR / "reports" / "tables"


def percent_label(value: float) -> str:
    return f"{value:.2f}%".replace(".", ",")


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    source_path = RESULTS_DIR / "full_protocol_participant_wise_external_p06p07.csv"
    df = pd.read_csv(source_path).sort_values("participant_id").reset_index(drop=True)
    required = {"P06", "P07"}
    participants = set(df["participant_id"].astype(str))
    if participants != required:
        raise ValueError(f"Expected participants {required}, found {participants}")

    metric_columns = ["accuracy", "precision_incorrect", "recall_incorrect", "f1_incorrect"]
    metric_labels = ["Accuracy", "Precision", "Recall", "F1-score"]

    table = df[
        [
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
    ].copy()
    for column in metric_columns:
        table[f"{column}_percent"] = (table[column] * 100).round(2)
    table.to_csv(TABLES_DIR / "figure_4_5_participant_metric_comparison.csv", index=False, encoding="utf-8-sig")

    values = df[metric_columns].to_numpy(dtype=float) * 100.0
    x = np.arange(len(metric_labels))
    width = 0.34
    colors = ["#2563eb", "#f97316"]

    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False
    fig, ax = plt.subplots(figsize=(9.4, 5.6))

    for i, participant in enumerate(df["participant_id"].astype(str)):
        offset = (i - 0.5) * width
        bars = ax.bar(
            x + offset,
            values[i],
            width=width,
            label=participant,
            color=colors[i],
            edgecolor="white",
            linewidth=0.9,
        )
        for bar, value in zip(bars, values[i]):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 1.0,
                percent_label(value),
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold",
                color="#1f2937",
            )

    ax.set_title(
        "So sánh kết quả của cấu hình được lựa chọn trên P06 và P07",
        fontsize=14,
        fontweight="bold",
        pad=14,
    )
    ax.set_ylabel("Giá trị (%)")
    ax.set_ylim(0, 108)
    ax.set_xticks(x, metric_labels, fontsize=11, fontweight="bold")
    ax.grid(axis="y", alpha=0.25)
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        title="Người tham gia",
        ncol=2,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.075),
        frameon=True,
    )

    fig.text(
        0.01,
        0.012,
        (
            "Ghi chú: Precision, Recall và F1-score được tính cho lớp Incorrect. "
            "Cấu hình: HistGradientBoosting + ergonomic_v2_with_view, threshold = 0,76."
        ),
        ha="left",
        fontsize=8.8,
        color="#374151",
    )
    fig.subplots_adjust(left=0.09, right=0.98, top=0.86, bottom=0.25)

    for name in ["figure_4_5_participant_metric_comparison"]:
        fig.savefig(FIGURES_DIR / f"{name}.png", dpi=320)
        fig.savefig(FIGURES_DIR / f"{name}.svg")
    plt.close(fig)

    print(FIGURES_DIR / "figure_4_5_participant_metric_comparison.png")
    print(TABLES_DIR / "figure_4_5_participant_metric_comparison.csv")


if __name__ == "__main__":
    main()
