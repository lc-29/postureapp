"""Generate thesis Figure 4.2 from the full external benchmark results."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "reports" / "results"
FIGURES_DIR = BASE_DIR / "reports" / "figures"
TABLES_DIR = BASE_DIR / "reports" / "tables"


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    default = pd.read_csv(RESULTS_DIR / "full_protocol_model_benchmark_external_p06p07.csv")
    sweep = pd.read_csv(RESULTS_DIR / "full_protocol_threshold_sweep_external_p06p07.csv")

    hgb_calibrated = (
        sweep[sweep["model_id"].eq("hist_gradient_boosting_none__ergonomic_v2_with_view")]
        .sort_values(["f1_incorrect", "mcc"], ascending=False)
        .iloc[[0]]
        .copy()
    )
    family_best = (
        default.sort_values(
            ["algorithm_family", "f1_incorrect", "mcc", "precision_incorrect"],
            ascending=[True, False, False, False],
        )
        .groupby("algorithm_family")
        .head(1)
        .copy()
    )
    family_best = family_best[family_best["algorithm_family"] != "HistGradientBoosting"]
    selected = pd.concat([hgb_calibrated, family_best], ignore_index=True)

    order = [
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
    selected["order"] = selected["algorithm_family"].map({name: i for i, name in enumerate(order)})
    selected = selected.sort_values("order").reset_index(drop=True)

    label_map = {
        "HistGradientBoosting": "HistGradientBoosting\nergonomic_v2_view, ngưỡng 0,76",
        "Logistic Regression": "Logistic Regression\nergonomic_14, ngưỡng 0,50",
        "Random Forest": "Random Forest\nergonomic_v2_view, ngưỡng 0,50",
        "SVM RBF": "SVM RBF\nnormalized_99, ngưỡng 0,50",
        "Decision Tree": "Decision Tree\ncombined_v2_view, ngưỡng 0,50",
        "KNN": "KNN\nergonomic_14, ngưỡng 0,50",
        "ANN/Keras": "ANN/Keras\nnormalized_99, ngưỡng 0,50",
        "MLPClassifier": "MLPClassifier\nraw_99, ngưỡng 0,50",
        "Rule-based Baseline": "Rule-based Baseline\nmanual rules",
    }
    metric_cols = ["accuracy", "precision_incorrect", "recall_incorrect", "f1_incorrect"]
    metric_labels = ["Accuracy", "Precision", "Recall", "F1-score"]
    values = selected[metric_cols].to_numpy() * 100.0
    row_labels = [label_map[name] for name in selected["algorithm_family"]]

    source_table = selected[
        [
            "model_id",
            "algorithm_family",
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
        source_table[f"{column}_percent"] = (source_table[column] * 100).round(2)
    source_table.to_csv(
        TABLES_DIR / "figure_4_2_full_algorithm_metric_comparison.csv",
        index=False,
        encoding="utf-8-sig",
    )

    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False
    fig, ax = plt.subplots(figsize=(11.8, 6.4))
    image = ax.imshow(values, cmap="YlGnBu", vmin=55, vmax=100, aspect="auto")

    ax.set_xticks(np.arange(len(metric_labels)), labels=metric_labels, fontsize=11, fontweight="bold")
    ax.set_yticks(np.arange(len(row_labels)), labels=row_labels, fontsize=9.5)
    ax.set_title(
        "So sánh các chỉ số của cấu hình đại diện theo nhóm thuật toán",
        fontsize=14,
        fontweight="bold",
        pad=18,
    )

    ax.set_xticks(np.arange(-0.5, len(metric_labels), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(row_labels), 1), minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=1.4)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.tick_params(axis="x", top=True, bottom=False, labeltop=True, labelbottom=False)

    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            value = values[i, j]
            color = "white" if value >= 82 else "#1f2933"
            ax.text(
                j,
                i,
                f"{value:.2f}%",
                ha="center",
                va="center",
                fontsize=9.6,
                fontweight="bold",
                color=color,
            )

    ax.add_patch(
        plt.Rectangle(
            (-0.5, -0.5),
            len(metric_labels),
            1,
            fill=False,
            edgecolor="#d62828",
            linewidth=2.2,
        )
    )
    ax.text(
        len(metric_labels) - 0.02,
        -0.64,
        "Model được chọn",
        ha="right",
        va="bottom",
        color="#d62828",
        fontsize=9.5,
        fontweight="bold",
    )

    colorbar = fig.colorbar(image, ax=ax, fraction=0.035, pad=0.025)
    colorbar.set_label("Giá trị (%)", rotation=90)

    fig.text(
        0.01,
        0.012,
        (
            "Ghi chú: mỗi dòng là cấu hình đại diện/tốt nhất của một nhóm thuật toán "
            "trên external P06-P07; Precision/Recall/F1 tính cho lớp Incorrect posture."
        ),
        ha="left",
        fontsize=9,
        color="#374151",
    )
    fig.subplots_adjust(left=0.30, right=0.93, top=0.82, bottom=0.12)

    for name in [
        "figure_4_2_model_metric_comparison",
        "figure_4_2_full_algorithm_metric_heatmap",
    ]:
        fig.savefig(FIGURES_DIR / f"{name}.png", dpi=220)
        fig.savefig(FIGURES_DIR / f"{name}.svg")
    plt.close(fig)

    print(FIGURES_DIR / "figure_4_2_model_metric_comparison.png")
    print(TABLES_DIR / "figure_4_2_full_algorithm_metric_comparison.csv")


if __name__ == "__main__":
    main()
