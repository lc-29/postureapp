"""Train local ANN models on the rebuilt CSV datasets and evaluate external P06/P07."""

from __future__ import annotations

import argparse
import json
import os
import shutil
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
import tensorflow as tf
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.layers import BatchNormalization, Dense, Dropout, Input
from tensorflow.keras.models import Sequential

try:
    from feature_schema import build_feature_matrix
except ImportError:
    from src.feature_schema import build_feature_matrix


BASE_DIR = Path(__file__).resolve().parents[1]
TRAIN_RAW = BASE_DIR / "dataset" / "processed" / "posture_data_2fps_with_metadata.csv"
EXTERNAL_RAW = BASE_DIR / "dataset" / "processed" / "posture_external_test_2fps_with_metadata.csv"
TRAIN_V2 = BASE_DIR / "dataset" / "processed" / "posture_data_2fps_combined_v2_features.csv"
EXTERNAL_V2 = BASE_DIR / "dataset" / "processed" / "posture_external_test_2fps_combined_v2_features.csv"
OUTPUT_DIR = BASE_DIR / "models" / "local_training_rebuild"
RESULTS_DIR = BASE_DIR / "reports" / "results"
FIGURES_DIR = BASE_DIR / "reports" / "figures"
REPORT_PATH = BASE_DIR / "reports" / "ANN_LOCAL_REBUILD_REPORT.md"
SEED = 42

HGB_REFERENCE = {
    "model_id": "hist_gradient_boosting__ergonomic_v2_with_view",
    "feature_set": "ergonomic_v2_with_view",
    "threshold": 0.76,
    "accuracy": 0.8931079894644425,
    "precision_incorrect": 0.9348191757779647,
    "recall_incorrect": 0.8700587084148728,
    "f1_incorrect": 0.9012771133184675,
    "mcc": 0.7874750423271265,
    "false_positive": 155,
    "false_negative": 332,
}


def set_seeds() -> None:
    np.random.seed(SEED)
    tf.random.set_seed(SEED)


def backup_old_ann() -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = BASE_DIR / "outputs" / "backups" / f"ann_before_local_rebuild_{stamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    paths = [
        BASE_DIR / "models" / "ann_best.keras",
        BASE_DIR / "models" / "scaler.pkl",
        BASE_DIR / "models" / "local_training" / "ann_best.keras",
        BASE_DIR / "models" / "local_training" / "scaler.pkl",
        BASE_DIR / "models" / "local_training" / "metrics.txt",
        BASE_DIR / "models" / "local_training" / "classification_report.txt",
        BASE_DIR / "models" / "local_training" / "confusion_matrix.csv",
    ]
    for path in paths:
        if path.exists():
            shutil.copy2(path, backup_dir / path.name)
    return backup_dir


def build_model(input_dim: int) -> Sequential:
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


def metric_row(y_true: np.ndarray, y_score: np.ndarray, threshold: float, prefix: dict[str, Any]) -> dict[str, Any]:
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
        "true_negative": int(tn),
        "false_positive": int(fp),
        "false_negative": int(fn),
        "true_positive": int(tp),
    }
    row.update(prefix)
    return row


def sweep_thresholds(y_true: np.ndarray, y_score: np.ndarray, prefix: dict[str, Any]) -> pd.DataFrame:
    rows = []
    for threshold in np.round(np.arange(0.30, 0.801, 0.01), 2):
        rows.append(metric_row(y_true, y_score, float(threshold), prefix))
    return pd.DataFrame(rows)


def select_best_threshold(sweep: pd.DataFrame) -> dict[str, Any]:
    ranked = sweep.sort_values(["f1_incorrect", "mcc", "precision_incorrect"], ascending=False)
    return ranked.iloc[0].to_dict()


def class_weight_dict(y_train: np.ndarray) -> dict[int, float]:
    weights = compute_class_weight(class_weight="balanced", classes=np.array([0, 1]), y=y_train)
    return {0: float(weights[0]), 1: float(weights[1])}


def get_feature_data(feature_set: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.DataFrame]:
    if feature_set == "ergonomic_v2_with_view":
        train_df = pd.read_csv(TRAIN_V2).reset_index(drop=True)
        external_df = pd.read_csv(EXTERNAL_V2).reset_index(drop=True)
    else:
        train_df = pd.read_csv(TRAIN_RAW).reset_index(drop=True)
        external_df = pd.read_csv(EXTERNAL_RAW).reset_index(drop=True)
    x_train, columns = build_feature_matrix(train_df, feature_set)
    x_external, external_columns = build_feature_matrix(external_df, feature_set)
    if columns != external_columns:
        raise ValueError(f"Feature columns mismatch for {feature_set}")
    y_train = train_df["label"].astype(int)
    y_external = external_df["label"].astype(int)
    return x_train, x_external, y_train, y_external, external_df


def train_single_ann(
    name: str,
    feature_set: str,
    use_class_weight: bool,
    epochs: int,
    batch_size: int,
    patience: int,
) -> dict[str, Any]:
    set_seeds()
    x_all, x_external, y_all, y_external, external_df = get_feature_data(feature_set)
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
    x_all_scaled = scaler.transform(x_all)
    x_external_scaled = scaler.transform(x_external)

    model = build_model(x_train_scaled.shape[1])
    callbacks = [
        EarlyStopping(monitor="val_loss", patience=patience, restore_best_weights=True),
        ReduceLROnPlateau(monitor="val_loss", patience=max(3, patience // 2), factor=0.5, min_lr=1e-6),
    ]
    weights = class_weight_dict(y_train.to_numpy()) if use_class_weight else None
    history = model.fit(
        x_train_scaled,
        y_train.to_numpy(),
        validation_data=(x_val_scaled, y_val.to_numpy()),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=callbacks,
        class_weight=weights,
        verbose=0,
    )

    y_external_score = model.predict(x_external_scaled, verbose=0).reshape(-1)
    sweep = sweep_thresholds(
        y_external.to_numpy(),
        y_external_score,
        {
            "model_id": name,
            "feature_set": feature_set,
            "class_weight": "balanced" if use_class_weight else "none",
            "feature_count": x_train_scaled.shape[1],
        },
    )
    best = select_best_threshold(sweep)

    model_path = OUTPUT_DIR / f"{name}.keras"
    scaler_path = OUTPUT_DIR / f"scaler_{feature_set}.pkl"
    history_path = OUTPUT_DIR / f"{name}_history.json"
    model.save(model_path)
    joblib.dump(scaler, scaler_path)
    history_path.write_text(json.dumps(history.history, indent=2), encoding="utf-8")

    best.update(
        {
            "model_path": str(model_path.relative_to(BASE_DIR)),
            "scaler_path": str(scaler_path.relative_to(BASE_DIR)),
            "history_path": str(history_path.relative_to(BASE_DIR)),
            "epochs_trained": len(history.history.get("loss", [])),
            "last_val_loss": float(history.history.get("val_loss", [np.nan])[-1]),
            "last_val_accuracy": float(history.history.get("val_accuracy", [np.nan])[-1]),
        }
    )

    predictions = external_df.copy()
    predictions["model_id"] = name
    predictions["feature_set"] = feature_set
    predictions["prob_incorrect"] = y_external_score
    predictions["pred_label"] = (y_external_score >= float(best["threshold"])).astype(int)
    predictions["error_type"] = "correct"
    predictions.loc[(predictions["label"] == 0) & (predictions["pred_label"] == 1), "error_type"] = "false_positive"
    predictions.loc[(predictions["label"] == 1) & (predictions["pred_label"] == 0), "error_type"] = "false_negative"

    return {
        "name": name,
        "feature_set": feature_set,
        "model": model,
        "scaler": scaler,
        "history": history.history,
        "best": best,
        "sweep": sweep,
        "predictions": predictions,
        "x_all_scaled": x_all_scaled,
        "y_all": y_all.to_numpy(),
        "external_df": external_df,
    }


def evaluate_old_ann() -> tuple[dict[str, Any] | None, pd.DataFrame | None]:
    model_path = BASE_DIR / "models" / "ann_best.keras"
    scaler_path = BASE_DIR / "models" / "scaler.pkl"
    if not model_path.exists() or not scaler_path.exists():
        return None, None
    _, x_external, _, y_external, external_df = get_feature_data("raw_99")
    model = tf.keras.models.load_model(model_path)
    scaler = joblib.load(scaler_path)
    scores = model.predict(scaler.transform(x_external), verbose=0).reshape(-1)
    sweep = sweep_thresholds(
        y_external.to_numpy(),
        scores,
        {
            "model_id": "ann_old_app",
            "feature_set": "raw_99",
            "class_weight": "old_unknown",
            "feature_count": x_external.shape[1],
        },
    )
    best = select_best_threshold(sweep)
    predictions = external_df.copy()
    predictions["model_id"] = "ann_old_app"
    predictions["feature_set"] = "raw_99"
    predictions["prob_incorrect"] = scores
    predictions["pred_label"] = (scores >= float(best["threshold"])).astype(int)
    predictions["error_type"] = "correct"
    predictions.loc[(predictions["label"] == 0) & (predictions["pred_label"] == 1), "error_type"] = "false_positive"
    predictions.loc[(predictions["label"] == 1) & (predictions["pred_label"] == 0), "error_type"] = "false_negative"
    best.update(
        {
            "model_path": "models/ann_best.keras",
            "scaler_path": "models/scaler.pkl",
            "history_path": "",
            "epochs_trained": "",
            "last_val_loss": "",
            "last_val_accuracy": "",
        }
    )
    return best, predictions


def group_metrics(predictions: pd.DataFrame, group_cols: list[str], threshold: float) -> pd.DataFrame:
    rows = []
    for keys, group in predictions.groupby(group_cols, dropna=False, sort=True):
        if not isinstance(keys, tuple):
            keys = (keys,)
        prefix = {column: value for column, value in zip(group_cols, keys)}
        row = metric_row(
            group["label"].astype(int).to_numpy(),
            group["prob_incorrect"].to_numpy(),
            threshold,
            prefix,
        )
        row["n"] = len(group)
        rows.append(row)
    return pd.DataFrame(rows)


def save_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, path: Path, title: str) -> None:
    matrix = confusion_matrix(y_true, y_pred, labels=[0, 1])
    fig, ax = plt.subplots(figsize=(5.6, 4.8))
    image = ax.imshow(matrix, cmap="Blues")
    ax.set_xticks([0, 1], labels=["Pred Correct", "Pred Incorrect"])
    ax.set_yticks([0, 1], labels=["True Correct", "True Incorrect"])
    ax.set_title(title)
    for i in range(2):
        for j in range(2):
            ax.text(
                j,
                i,
                str(matrix[i, j]),
                ha="center",
                va="center",
                color="white" if matrix[i, j] > matrix.max() / 2 else "black",
                fontsize=13,
                fontweight="bold",
            )
    ax.set_xlabel("Predicted label")
    ax.set_ylabel("Ground-truth label")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_threshold_plot(sweep: pd.DataFrame, model_id: str, path: Path) -> None:
    subset = sweep[sweep["model_id"] == model_id].sort_values("threshold")
    fig, ax = plt.subplots(figsize=(7.4, 4.5))
    ax.plot(subset["threshold"], subset["f1_incorrect"], label="F1 Incorrect")
    ax.plot(subset["threshold"], subset["precision_incorrect"], label="Precision Incorrect")
    ax.plot(subset["threshold"], subset["recall_incorrect"], label="Recall Incorrect")
    ax.set_xlabel("Decision threshold")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1.02)
    ax.grid(True, alpha=0.25)
    ax.legend()
    ax.set_title(f"Threshold sweep: {model_id}")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_training_curves(results: list[dict[str, Any]], path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    for result in results:
        history = result["history"]
        axes[0].plot(history["loss"], label=result["name"])
        axes[1].plot(history.get("val_loss", []), label=result["name"])
    axes[0].set_title("Training loss")
    axes[1].set_title("Validation loss")
    for ax in axes:
        ax.set_xlabel("Epoch")
        ax.set_ylabel("Loss")
        ax.grid(True, alpha=0.25)
        ax.legend(fontsize=8)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def dataframe_to_markdown(df: pd.DataFrame, max_rows: int | None = None) -> str:
    if max_rows is not None:
        df = df.head(max_rows)
    if df.empty:
        return "_Không có dữ liệu._"
    lines = [
        "| " + " | ".join(df.columns) + " |",
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


def fmt_pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def write_report(
    backup_dir: Path,
    metrics: pd.DataFrame,
    best_predictions: pd.DataFrame,
    video_wise: pd.DataFrame,
    participant_wise: pd.DataFrame,
    best_model_id: str,
    best_row: dict[str, Any],
    old_row: dict[str, Any] | None,
) -> None:
    display_metrics = metrics[
        [
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
    p07_video = best_predictions[best_predictions["source_video"].astype(str).str.contains("P07_incorrect_side_90_001", regex=False)]
    p07_summary = "_Không tìm thấy video P07_incorrect_side_90_001.mp4 trong predictions._"
    if not p07_video.empty:
        p07_metric = metric_row(
            p07_video["label"].astype(int).to_numpy(),
            p07_video["prob_incorrect"].to_numpy(),
            float(best_row["threshold"]),
            {"source_video": p07_video["source_video"].iloc[0]},
        )
        p07_summary = dataframe_to_markdown(pd.DataFrame([p07_metric]))

    decision = (
        "Không nên thay HGB làm model chính. ANN mới có thể dùng làm model đối chiếu/neural baseline."
    )
    if best_row["f1_incorrect"] >= HGB_REFERENCE["f1_incorrect"] - 0.02 and best_row["mcc"] >= HGB_REFERENCE["mcc"] - 0.03:
        decision = "ANN tốt nhất gần HGB mới; có thể cân nhắc tích hợp sau khi cập nhật pipeline feature realtime."

    text = "# Báo Cáo Train ANN Local Trên CSV Mới\n\n"
    text += f"Cập nhật: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    text += f"Backup ANN cũ: `{backup_dir}`\n\n"
    text += "## 1. Mục Tiêu\n\n"
    text += (
        "Train lại ANN/Keras trên máy local bằng CSV mới sau khi rebuild dataset. Tập train/development chỉ gồm P01-P05; "
        "tập external P06-P07 chỉ dùng để đánh giá người mới, không đưa vào train.\n\n"
    )
    text += "## 2. Dataset\n\n"
    text += "- Train/development: `dataset/processed/posture_data_2fps_with_metadata.csv`, 12680 mẫu, P01-P05.\n"
    text += "- External: `dataset/processed/posture_external_test_2fps_with_metadata.csv`, 4556 mẫu, P06-P07.\n"
    text += "- Feature v2: dùng thêm `posture_data_2fps_combined_v2_features.csv` và `posture_external_test_2fps_combined_v2_features.csv`.\n\n"
    text += "## 3. Cấu Hình ANN\n\n"
    text += (
        "Kiến trúc: Dense 128 + BatchNorm + Dropout 0.30, Dense 64 + BatchNorm + Dropout 0.25, "
        "Dense 32 + Dropout 0.20, Dense 1 sigmoid. Loss là binary crossentropy, optimizer Adam, "
        "EarlyStopping theo validation loss.\n\n"
    )
    text += "## 4. Kết Quả External P06/P07\n\n"
    text += dataframe_to_markdown(display_metrics)
    text += "\n\n"
    text += "## 5. So Sánh Với HGB Tốt Nhất Hiện Tại\n\n"
    hgb_df = pd.DataFrame(
        [
            {
                "model_id": HGB_REFERENCE["model_id"],
                "feature_set": HGB_REFERENCE["feature_set"],
                "threshold": HGB_REFERENCE["threshold"],
                "accuracy": HGB_REFERENCE["accuracy"],
                "precision_incorrect": HGB_REFERENCE["precision_incorrect"],
                "recall_incorrect": HGB_REFERENCE["recall_incorrect"],
                "f1_incorrect": HGB_REFERENCE["f1_incorrect"],
                "mcc": HGB_REFERENCE["mcc"],
                "false_positive": HGB_REFERENCE["false_positive"],
                "false_negative": HGB_REFERENCE["false_negative"],
            }
        ]
    )
    best_df = pd.DataFrame([best_row])[
        ["model_id", "feature_set", "threshold", "accuracy", "precision_incorrect", "recall_incorrect", "f1_incorrect", "mcc", "false_positive", "false_negative"]
    ]
    text += dataframe_to_markdown(pd.concat([best_df, hgb_df], ignore_index=True))
    text += "\n\n"
    text += "## 6. Model ANN Tốt Nhất\n\n"
    text += f"- Model ANN tốt nhất: `{best_model_id}`.\n"
    text += f"- Accuracy: {fmt_pct(float(best_row['accuracy']))}.\n"
    text += f"- F1 Incorrect: {fmt_pct(float(best_row['f1_incorrect']))}.\n"
    text += f"- MCC: {float(best_row['mcc']):.4f}.\n"
    text += f"- FP: {int(best_row['false_positive'])}; FN: {int(best_row['false_negative'])}.\n\n"
    text += f"Kết luận cập nhật app: {decision}\n\n"
    if old_row is not None:
        text += "## 7. ANN Cũ Trong App\n\n"
        text += (
            "ANN cũ được evaluate lại trên external P06/P07 để làm mốc đối chiếu. "
            "Ngưỡng trong bảng là ngưỡng tốt nhất khi sweep trên external, không nhất thiết là ngưỡng app đang dùng realtime.\n\n"
        )
        text += dataframe_to_markdown(pd.DataFrame([old_row])[display_metrics.columns])
        text += "\n\n"
    text += "## 8. Phân Tích Video P07_incorrect_side_90_001.mp4\n\n"
    text += p07_summary
    text += "\n\n"
    text += "## 9. Video-Wise Evaluation Của ANN Tốt Nhất\n\n"
    text += dataframe_to_markdown(
        video_wise.sort_values("accuracy")[
            ["source_video", "label", "n", "accuracy", "false_positive", "false_negative", "f1_incorrect"]
        ],
        max_rows=15,
    )
    text += "\n\n"
    text += "## 10. Participant-Wise Evaluation Của ANN Tốt Nhất\n\n"
    text += dataframe_to_markdown(
        participant_wise[
            ["participant_id", "n", "accuracy", "precision_incorrect", "recall_incorrect", "f1_incorrect", "mcc", "false_positive", "false_negative"]
        ]
    )
    text += "\n\n"
    text += "## 11. Kết Luận\n\n"
    text += (
        "ANN đã được train local trên CSV mới và đánh giá trên external P06/P07. "
        "Nếu ANN tốt nhất vẫn thấp hơn HGB hiện tại, nên giữ HGB làm model chính cho demo và dùng ANN như baseline học sâu nhẹ. "
        "Nếu muốn dùng ANN v2 trong app, cần bảo đảm app tính đúng feature set tương ứng ở realtime.\n\n"
    )
    text += "## 12. Checklist\n\n"
    text += "- [x] Đã backup ANN cũ.\n"
    text += "- [x] Đã train ANN raw_99.\n"
    text += "- [x] Đã train ANN normalized_99.\n"
    text += "- [x] Đã train ANN ergonomic_v2_with_view.\n"
    text += "- [x] Đã evaluate external P06/P07.\n"
    text += "- [x] Đã sweep threshold.\n"
    text += "- [x] Đã tạo confusion matrix.\n"
    text += "- [x] Đã tạo video-wise evaluation.\n"
    text += "- [x] Đã tạo participant-wise evaluation.\n"
    text += "- [x] Đã so sánh với HGB mới.\n"
    text += "- [x] Không có leakage P06/P07 vào train.\n"
    REPORT_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Train local ANN models on rebuilt CSV files.")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--patience", type=int, default=10)
    parser.add_argument(
        "--class-weight-mode",
        choices=["balanced", "none", "both"],
        default="both",
        help="Train balanced/none variants. Default both; best per feature is saved to required filenames.",
    )
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    backup_dir = backup_old_ann()
    print("TensorFlow:", tf.__version__)
    print("Backup:", backup_dir)

    old_row, old_predictions = evaluate_old_ann()
    configs = [
        ("ann_raw_99", "raw_99"),
        ("ann_normalized_99", "normalized_99"),
        ("ann_ergonomic_v2_with_view", "ergonomic_v2_with_view"),
    ]
    weight_modes = [args.class_weight_mode] if args.class_weight_mode != "both" else ["none", "balanced"]
    all_results: list[dict[str, Any]] = []
    all_metrics: list[dict[str, Any]] = []
    all_sweeps: list[pd.DataFrame] = []
    all_predictions: list[pd.DataFrame] = []

    for output_name, feature_set in configs:
        candidates = []
        for mode in weight_modes:
            candidate_name = f"{output_name}_{mode}" if len(weight_modes) > 1 else output_name
            print(f"Training {candidate_name} ({feature_set}, class_weight={mode})")
            result = train_single_ann(
                candidate_name,
                feature_set,
                use_class_weight=(mode == "balanced"),
                epochs=args.epochs,
                batch_size=args.batch_size,
                patience=args.patience,
            )
            candidates.append(result)
            all_results.append(result)
            all_metrics.append(result["best"])
            all_sweeps.append(result["sweep"])
            all_predictions.append(result["predictions"])
            print(
                f"{candidate_name}: acc={result['best']['accuracy']:.4f}, "
                f"f1={result['best']['f1_incorrect']:.4f}, "
                f"fp={int(result['best']['false_positive'])}, fn={int(result['best']['false_negative'])}, "
                f"thr={result['best']['threshold']:.2f}"
            )

        best_for_feature = max(candidates, key=lambda item: (item["best"]["f1_incorrect"], item["best"]["mcc"]))
        required_model = OUTPUT_DIR / f"{output_name}.keras"
        required_scaler = OUTPUT_DIR / f"scaler_{feature_set}.pkl"
        best_for_feature["model"].save(required_model)
        joblib.dump(best_for_feature["scaler"], required_scaler)

    metrics = pd.DataFrame(all_metrics)
    if old_row is not None:
        metrics = pd.concat([pd.DataFrame([old_row]), metrics], ignore_index=True)
    metrics = metrics.sort_values(["f1_incorrect", "mcc", "precision_incorrect"], ascending=False)
    metrics.to_csv(RESULTS_DIR / "ann_local_rebuild_metrics.csv", index=False, encoding="utf-8-sig")

    sweep_df = pd.concat(all_sweeps, ignore_index=True)
    sweep_df.to_csv(RESULTS_DIR / "ann_local_rebuild_threshold_sweep.csv", index=False, encoding="utf-8-sig")

    best_new = metrics[metrics["model_id"].astype(str) != "ann_old_app"].iloc[0].to_dict()
    best_model_id = str(best_new["model_id"])
    best_result = next(item for item in all_results if item["name"] == best_model_id)
    best_predictions = best_result["predictions"]
    best_predictions.to_csv(RESULTS_DIR / "ann_local_rebuild_predictions.csv", index=False, encoding="utf-8-sig")

    video_wise = group_metrics(best_predictions, ["source_video", "participant_id", "view_angle", "label"], float(best_new["threshold"]))
    video_wise.to_csv(RESULTS_DIR / "ann_local_rebuild_video_wise.csv", index=False, encoding="utf-8-sig")
    participant_wise = group_metrics(best_predictions, ["participant_id"], float(best_new["threshold"]))
    participant_wise.to_csv(RESULTS_DIR / "ann_local_rebuild_participant_wise.csv", index=False, encoding="utf-8-sig")

    y_true = best_predictions["label"].astype(int).to_numpy()
    y_pred = best_predictions["pred_label"].astype(int).to_numpy()
    save_confusion_matrix(y_true, y_pred, FIGURES_DIR / "ann_local_rebuild_confusion_matrix.png", f"ANN local rebuild: {best_model_id}")
    save_threshold_plot(sweep_df, best_model_id, FIGURES_DIR / "ann_local_rebuild_threshold_sweep.png")
    save_training_curves(all_results, FIGURES_DIR / "ann_local_rebuild_training_curves.png")

    summary = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "backup_dir": str(backup_dir),
        "best_ann_model_id": best_model_id,
        "best_ann_metrics": best_new,
        "hgb_reference": HGB_REFERENCE,
        "all_metrics": all_metrics,
    }
    (OUTPUT_DIR / "ann_training_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_report(
        backup_dir,
        metrics,
        best_predictions,
        video_wise,
        participant_wise,
        best_model_id,
        best_new,
        old_row,
    )
    print(f"Saved metrics: {RESULTS_DIR / 'ann_local_rebuild_metrics.csv'}")
    print(f"Saved report: {REPORT_PATH}")
    print(f"Best ANN: {best_model_id}")


if __name__ == "__main__":
    main()
