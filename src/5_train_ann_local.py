"""
Train ANN posture classifier locally from a landmark CSV.

Default input:
- dataset/posture_data_2fps.csv

Default output:
- models/local_training/ann_best.keras
- models/local_training/scaler.pkl
- models/local_training/metrics.txt
- models/local_training/classification_report.txt
- models/local_training/confusion_matrix.csv
- models/local_training/training_curves.png

After checking the metrics, copy ann_best.keras and scaler.pkl to models/ if you
want the desktop app to use the new model.
"""

from __future__ import annotations

import argparse
import io
import os
from pathlib import Path

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
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.layers import BatchNormalization, Dense, Dropout, Input
from tensorflow.keras.models import Sequential


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATASET_PATH = BASE_DIR / "dataset" / "posture_data_2fps.csv"
DEFAULT_OUTPUT_DIR = BASE_DIR / "models" / "local_training"
NUM_FEATURES = 99
SEED = 42


def load_and_validate_dataset(csv_path: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    if not csv_path.exists():
        raise FileNotFoundError(f"Khong tim thay CSV: {csv_path}")

    df = pd.read_csv(csv_path)
    if "label" not in df.columns:
        raise ValueError("CSV phai co cot 'label'.")

    feature_columns = [
        column
        for column in df.columns
        if column.startswith("landmark_") and column.rsplit("_", 1)[-1] in {"x", "y", "z"}
    ]
    if len(feature_columns) != NUM_FEATURES:
        raise ValueError(
            f"CSV phai co {NUM_FEATURES} landmark feature, nhung dang co {len(feature_columns)}."
        )

    missing_count = int(df.isnull().sum().sum())
    if missing_count > 0:
        print(f"Phat hien {missing_count} missing values, dang loai bo cac dong bi thieu.")
        df = df.dropna().reset_index(drop=True)

    unique_labels = set(df["label"].astype(int).unique().tolist())
    if unique_labels != {0, 1}:
        raise ValueError(f"Label chi duoc gom 0 va 1. Hien co: {sorted(unique_labels)}")

    X = df[feature_columns].astype(np.float32)
    y = df["label"].astype(int)
    return df, X, y


def split_dataset(
    X: pd.DataFrame,
    y: pd.Series,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series]:
    X_train_temp, X_test, y_train_temp, y_test = train_test_split(
        X,
        y,
        test_size=0.15,
        random_state=SEED,
        stratify=y,
    )

    validation_size = 0.15 / 0.85
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_temp,
        y_train_temp,
        test_size=validation_size,
        random_state=SEED,
        stratify=y_train_temp,
    )

    return X_train, X_val, X_test, y_train, y_val, y_test


def build_model(input_dim: int) -> Sequential:
    model = Sequential(
        [
            Input(shape=(input_dim,)),
            Dense(128, activation="relu"),
            BatchNormalization(),
            Dropout(0.3),
            Dense(64, activation="relu"),
            BatchNormalization(),
            Dropout(0.25),
            Dense(32, activation="relu"),
            Dropout(0.2),
            Dense(1, activation="sigmoid"),
        ]
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )
    return model


def save_training_curves(history: tf.keras.callbacks.History, output_path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    axes[0].plot(history.history["loss"], label="Training Loss")
    axes[0].plot(history.history["val_loss"], label="Validation Loss")
    axes[0].set_title("Loss")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    axes[1].plot(history.history["accuracy"], label="Training Accuracy")
    axes[1].plot(history.history["val_accuracy"], label="Validation Accuracy")
    axes[1].set_title("Accuracy")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Accuracy")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def train(args: argparse.Namespace) -> None:
    np.random.seed(SEED)
    tf.random.set_seed(SEED)

    csv_path = Path(args.dataset)
    if not csv_path.is_absolute():
        csv_path = BASE_DIR / csv_path

    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = BASE_DIR / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    best_model_path = output_dir / "ann_best.keras"
    scaler_path = output_dir / "scaler.pkl"
    metrics_path = output_dir / "metrics.txt"
    report_path = output_dir / "classification_report.txt"
    cm_path = output_dir / "confusion_matrix.csv"
    curves_path = output_dir / "training_curves.png"

    print("TensorFlow:", tf.__version__)
    print("Dataset:", csv_path)
    print("Output dir:", output_dir)

    df, X, y = load_and_validate_dataset(csv_path)

    if args.max_rows is not None:
        if args.max_rows < 20:
            raise ValueError("--max-rows phai >= 20 de co du mau train/validation/test.")
        sample_size = min(args.max_rows, len(df))
        if sample_size < len(df):
            df, _ = train_test_split(
                df,
                train_size=sample_size,
                random_state=SEED,
                stratify=df["label"],
            )
            df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)
        feature_columns = [
            column
            for column in df.columns
            if column.startswith("landmark_") and column.rsplit("_", 1)[-1] in {"x", "y", "z"}
        ]
        X = df[feature_columns].astype(np.float32)
        y = df["label"].astype(int)
        print(f"Smoke/subset mode: using {len(df)} rows.")

    print("Dataset shape:", df.shape)
    print("Label distribution:")
    print(y.value_counts().sort_index().to_string())

    X_train, X_val, X_test, y_train, y_val, y_test = split_dataset(X, y)
    print("Train shape:", X_train.shape)
    print("Validation shape:", X_val.shape)
    print("Test shape:", X_test.shape)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)

    classes = np.array([0, 1])
    class_weights = compute_class_weight(
        class_weight="balanced",
        classes=classes,
        y=y_train,
    )
    class_weight_dict = {
        int(label): float(weight)
        for label, weight in zip(classes, class_weights)
    }
    print("Class weight:", class_weight_dict)

    model = build_model(X_train_scaled.shape[1])
    model.summary()

    callbacks = [
        EarlyStopping(
            monitor="val_loss",
            patience=args.patience,
            restore_best_weights=True,
        ),
        ModelCheckpoint(
            filepath=best_model_path,
            monitor="val_loss",
            save_best_only=True,
            mode="min",
            verbose=1,
        ),
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=max(2, args.patience // 3),
            min_lr=1e-6,
            verbose=1,
        ),
    ]

    history = model.fit(
        X_train_scaled,
        y_train,
        validation_data=(X_val_scaled, y_val),
        epochs=args.epochs,
        batch_size=args.batch_size,
        callbacks=callbacks,
        class_weight=class_weight_dict,
        verbose=1,
    )

    if best_model_path.exists():
        model = tf.keras.models.load_model(best_model_path)
    else:
        model.save(best_model_path)

    y_prob = model.predict(X_test_scaled, verbose=0)
    y_pred = (y_prob >= args.threshold).astype(int).ravel()

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, pos_label=1, zero_division=0)
    recall = recall_score(y_test, y_pred, pos_label=1, zero_division=0)
    f1 = f1_score(y_test, y_pred, pos_label=1, zero_division=0)
    cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
    report = classification_report(
        y_test,
        y_pred,
        labels=[0, 1],
        target_names=["0 - Correct", "1 - Incorrect"],
        zero_division=0,
    )

    joblib.dump(scaler, scaler_path)
    pd.DataFrame(
        cm,
        index=["true_0_correct", "true_1_incorrect"],
        columns=["pred_0_correct", "pred_1_incorrect"],
    ).to_csv(cm_path)
    report_path.write_text(report, encoding="utf-8")
    save_training_curves(history, curves_path)

    summary_buffer = io.StringIO()
    model.summary(print_fn=lambda line: summary_buffer.write(line + "\n"))

    metrics_text = f"""Posture Detection ANN Metrics
=============================

Dataset path: {csv_path}
Dataset shape: {df.shape}

Train shape: {X_train.shape}
Validation shape: {X_val.shape}
Test shape: {X_test.shape}

Class distribution:
{y.value_counts().sort_index().to_string()}

Class weight:
{class_weight_dict}

Decision threshold: {args.threshold:.4f}

Test Accuracy: {accuracy:.6f}
Test Precision: {precision:.6f}
Test Recall: {recall:.6f}
Test F1-score: {f1:.6f}

Confusion matrix [[TN, FP], [FN, TP]]:
{cm}

Classification report:
{report}

Model architecture summary:
{summary_buffer.getvalue()}
"""
    metrics_path.write_text(metrics_text, encoding="utf-8")

    print("\n========== KET QUA TEST ==========")
    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1-score : {f1:.4f}")
    print("Confusion matrix [[TN, FP], [FN, TP]]:")
    print(cm)
    print("\nDa luu:")
    print(f"- {best_model_path}")
    print(f"- {scaler_path}")
    print(f"- {metrics_path}")
    print(f"- {report_path}")
    print(f"- {cm_path}")
    print(f"- {curves_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train ANN posture classifier locally from a landmark CSV."
    )
    parser.add_argument(
        "--dataset",
        default=str(DEFAULT_DATASET_PATH),
        help="Duong dan CSV train. Mac dinh: dataset/posture_data_2fps.csv",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Thu muc luu model, scaler va metrics.",
    )
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--patience", type=int, default=15)
    parser.add_argument(
        "--max-rows",
        type=int,
        default=None,
        help="Lay toi da N dong de smoke test pipeline train nhanh.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Nguong sigmoid de doi xac suat thanh label. Mac dinh 0.5.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    train(args)


if __name__ == "__main__":
    main()
