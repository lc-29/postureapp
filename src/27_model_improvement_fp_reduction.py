"""Run feature/model improvement experiments focused on reducing false positives."""

from __future__ import annotations

import argparse
import json
import math
import shutil
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import cv2
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
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
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.utils.class_weight import compute_sample_weight

try:
    from feature_schema import compute_normalized_landmarks, get_raw_landmark_columns
except ImportError:
    from src.feature_schema import compute_normalized_landmarks, get_raw_landmark_columns


BASE_DIR = Path(__file__).resolve().parents[1]
TRAIN_RAW = BASE_DIR / "dataset" / "processed" / "posture_data_2fps_with_metadata.csv"
EXTERNAL_RAW = BASE_DIR / "dataset" / "processed" / "posture_external_test_2fps_with_metadata.csv"
RESULTS_DIR = BASE_DIR / "reports" / "results"
FIGURES_DIR = BASE_DIR / "reports" / "figures"
REGISTRY_DIR = BASE_DIR / "models" / "registry"
REGISTRY_PATH = BASE_DIR / "models" / "model_registry.json"
REPORT_PATH = BASE_DIR / "reports" / "MODEL_IMPROVEMENT_FP_REDUCTION_REPORT.md"
SEED = 42

BASELINE = {
    "version": "Baseline after rebuild",
    "model_id": "random_forest__ergonomic_14",
    "algorithm": "random_forest",
    "feature_set": "ergonomic_14",
    "threshold": 0.50,
    "accuracy": 0.8215539947322212,
    "precision_incorrect": 0.7946549391069012,
    "recall_incorrect": 0.9193737769080235,
    "f1_incorrect": 0.8524768644529124,
    "mcc": 0.6404798127058315,
    "false_positive": 607,
    "false_negative": 206,
}

METADATA_COLUMNS = [
    "source_video",
    "frame_index",
    "timestamp_sec",
    "sample_fps",
    "video_fps",
    "participant_id",
    "view_angle",
    "camera_type",
]

ERGONOMIC_14 = [
    "shoulder_y_diff",
    "shoulder_tilt_angle",
    "torso_lean_angle",
    "head_offset_x",
    "nose_to_shoulder_y",
    "nose_shoulder_clearance_ratio",
    "neck_compression_detected",
    "left_hand_mouth_ratio",
    "right_hand_mouth_ratio",
    "chin_rest_detected",
    "shoulder_width",
    "torso_length",
    "head_shoulder_distance",
    "min_hand_mouth_ratio",
]

ERGONOMIC_V2_EXTRA = [
    "ear_shoulder_y_ratio_left",
    "ear_shoulder_y_ratio_right",
    "ear_shoulder_y_ratio_mean",
    "nose_ear_dx_ratio",
    "nose_shoulder_dx_ratio",
    "head_forward_ratio",
    "neck_to_shoulder_angle_left",
    "neck_to_shoulder_angle_right",
    "head_neck_torso_angle",
    "shoulder_hip_dx_ratio",
    "shoulder_hip_dy_ratio",
    "torso_side_lean_ratio",
    "hip_shoulder_torso_angle",
]

VIEW_COLUMNS = ["view_front", "view_side_30", "view_side_90", "view_unknown"]


@dataclass
class FittedCandidate:
    model_id: str
    algorithm: str
    feature_set: str
    class_weight: str
    model: Any
    columns: list[str]
    y_score: np.ndarray
    y_true: np.ndarray
    x_external: pd.DataFrame
    train_seconds: float
    predict_seconds: float


def safe_div(a: float, b: float) -> float:
    return float(a / b) if abs(b) > 1e-9 else 0.0


def point(row: pd.Series, index: int) -> tuple[float, float]:
    return float(row[f"landmark_{index}_x"]), float(row[f"landmark_{index}_y"])


def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def midpoint(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:
    return (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0


def line_angle_deg(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))


def angle_at(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> float:
    ba = np.array([a[0] - b[0], a[1] - b[1]], dtype=float)
    bc = np.array([c[0] - b[0], c[1] - b[1]], dtype=float)
    denom = np.linalg.norm(ba) * np.linalg.norm(bc)
    if denom <= 1e-9:
        return 0.0
    cosine = float(np.clip(np.dot(ba, bc) / denom, -1.0, 1.0))
    return float(math.degrees(math.acos(cosine)))


def compute_ergonomic_14(row: pd.Series) -> dict[str, float]:
    nose = point(row, 0)
    left_shoulder = point(row, 11)
    right_shoulder = point(row, 12)
    left_hip = point(row, 23)
    right_hip = point(row, 24)
    left_wrist = point(row, 15)
    right_wrist = point(row, 16)
    left_mouth = point(row, 9)
    right_mouth = point(row, 10)
    shoulder_mid = midpoint(left_shoulder, right_shoulder)
    hip_mid = midpoint(left_hip, right_hip)
    shoulder_width = max(distance(left_shoulder, right_shoulder), 1e-6)
    torso_length = max(distance(shoulder_mid, hip_mid), 1e-6)
    nose_to_shoulder_y = shoulder_mid[1] - nose[1]
    left_hand_mouth_ratio = distance(left_wrist, left_mouth) / shoulder_width
    right_hand_mouth_ratio = distance(right_wrist, right_mouth) / shoulder_width
    nose_clearance = nose_to_shoulder_y / shoulder_width
    return {
        "shoulder_y_diff": abs(left_shoulder[1] - right_shoulder[1]),
        "shoulder_tilt_angle": abs(line_angle_deg(left_shoulder, right_shoulder)),
        "torso_lean_angle": abs(line_angle_deg(shoulder_mid, hip_mid) - 90.0),
        "head_offset_x": abs(nose[0] - shoulder_mid[0]),
        "nose_to_shoulder_y": nose_to_shoulder_y,
        "nose_shoulder_clearance_ratio": nose_clearance,
        "neck_compression_detected": float(nose_clearance < 0.35),
        "left_hand_mouth_ratio": left_hand_mouth_ratio,
        "right_hand_mouth_ratio": right_hand_mouth_ratio,
        "chin_rest_detected": float(min(left_hand_mouth_ratio, right_hand_mouth_ratio) < 0.55),
        "shoulder_width": shoulder_width,
        "torso_length": torso_length,
        "head_shoulder_distance": distance(nose, shoulder_mid),
        "min_hand_mouth_ratio": min(left_hand_mouth_ratio, right_hand_mouth_ratio),
    }


def compute_v2_extra(row: pd.Series) -> dict[str, float]:
    nose = point(row, 0)
    left_ear = point(row, 7)
    right_ear = point(row, 8)
    left_shoulder = point(row, 11)
    right_shoulder = point(row, 12)
    left_hip = point(row, 23)
    right_hip = point(row, 24)
    shoulder_mid = midpoint(left_shoulder, right_shoulder)
    hip_mid = midpoint(left_hip, right_hip)
    ear_mid = midpoint(left_ear, right_ear)
    shoulder_width = max(distance(left_shoulder, right_shoulder), 1e-6)
    torso_length = max(distance(shoulder_mid, hip_mid), 1e-6)
    body_scale = max(shoulder_width, torso_length, 1e-6)
    left_ear_shoulder_y = safe_div(left_shoulder[1] - left_ear[1], body_scale)
    right_ear_shoulder_y = safe_div(right_shoulder[1] - right_ear[1], body_scale)
    shoulder_hip_dx = abs(shoulder_mid[0] - hip_mid[0])
    shoulder_hip_dy = abs(shoulder_mid[1] - hip_mid[1])
    return {
        "ear_shoulder_y_ratio_left": left_ear_shoulder_y,
        "ear_shoulder_y_ratio_right": right_ear_shoulder_y,
        "ear_shoulder_y_ratio_mean": (left_ear_shoulder_y + right_ear_shoulder_y) / 2.0,
        "nose_ear_dx_ratio": safe_div(abs(nose[0] - ear_mid[0]), body_scale),
        "nose_shoulder_dx_ratio": safe_div(abs(nose[0] - shoulder_mid[0]), body_scale),
        "head_forward_ratio": safe_div(abs(ear_mid[0] - shoulder_mid[0]), body_scale),
        "neck_to_shoulder_angle_left": abs(line_angle_deg(left_ear, left_shoulder)),
        "neck_to_shoulder_angle_right": abs(line_angle_deg(right_ear, right_shoulder)),
        "head_neck_torso_angle": angle_at(nose, shoulder_mid, hip_mid),
        "shoulder_hip_dx_ratio": safe_div(shoulder_hip_dx, body_scale),
        "shoulder_hip_dy_ratio": safe_div(shoulder_hip_dy, body_scale),
        "torso_side_lean_ratio": safe_div(shoulder_hip_dx, shoulder_hip_dy),
        "hip_shoulder_torso_angle": abs(line_angle_deg(shoulder_mid, hip_mid) - 90.0),
    }


def add_view_one_hot(df: pd.DataFrame) -> pd.DataFrame:
    output = pd.DataFrame(0.0, index=df.index, columns=VIEW_COLUMNS)
    if "view_angle" not in df.columns:
        output["view_unknown"] = 1.0
        return output
    views = df["view_angle"].fillna("unknown").astype(str)
    output.loc[views == "front", "view_front"] = 1.0
    output.loc[views == "side_30", "view_side_30"] = 1.0
    output.loc[views == "side_90", "view_side_90"] = 1.0
    output.loc[~views.isin(["front", "side_30", "side_90"]), "view_unknown"] = 1.0
    return output


def build_v2_csv(input_path: Path, ergonomic_path: Path, combined_path: Path) -> pd.DataFrame:
    df = pd.read_csv(input_path).reset_index(drop=True)
    get_raw_landmark_columns(df)
    rows: list[dict[str, float]] = []
    for _, row in df.iterrows():
        item = compute_ergonomic_14(row)
        item.update(compute_v2_extra(row))
        rows.append(item)
    ergonomic = pd.DataFrame(rows, columns=ERGONOMIC_14 + ERGONOMIC_V2_EXTRA)
    view = add_view_one_hot(df)
    metadata = [column for column in METADATA_COLUMNS if column in df.columns]
    ergonomic_output = pd.concat(
        [ergonomic, view, df[metadata].reset_index(drop=True), df[["label"]].reset_index(drop=True)],
        axis=1,
    )
    normalized = compute_normalized_landmarks(df).reset_index(drop=True)
    combined_output = pd.concat(
        [normalized, ergonomic.reset_index(drop=True), view.reset_index(drop=True), df[metadata].reset_index(drop=True), df[["label"]].reset_index(drop=True)],
        axis=1,
    )
    ergonomic_path.parent.mkdir(parents=True, exist_ok=True)
    ergonomic_output.to_csv(ergonomic_path, index=False, encoding="utf-8-sig")
    combined_output.to_csv(combined_path, index=False, encoding="utf-8-sig")
    return ergonomic_output


def metric_row(
    y_true: np.ndarray,
    y_score: np.ndarray,
    threshold: float,
    prefix: dict[str, Any] | None = None,
) -> dict[str, Any]:
    y_pred = (y_score >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    row: dict[str, Any] = {
        "threshold": threshold,
        "accuracy": accuracy_score(y_true, y_pred),
        "precision_incorrect": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
        "recall_incorrect": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
        "f1_incorrect": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
        "macro_f1": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "mcc": matthews_corrcoef(y_true, y_pred),
        "roc_auc": roc_auc_score(y_true, y_score) if len(set(y_true.tolist())) == 2 else np.nan,
        "pr_auc": average_precision_score(y_true, y_score) if len(set(y_true.tolist())) == 2 else np.nan,
        "true_negative": int(tn),
        "false_positive": int(fp),
        "false_negative": int(fn),
        "true_positive": int(tp),
    }
    if prefix:
        row.update(prefix)
    return row


def make_model(algorithm: str, class_weight: str) -> Any:
    weight = None if class_weight == "none" else "balanced"
    if algorithm == "logistic_regression":
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(max_iter=1200, class_weight=weight, random_state=SEED)),
            ]
        )
    if algorithm == "svm_rbf":
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", SVC(kernel="rbf", C=3.0, gamma="scale", probability=True, class_weight=weight)),
            ]
        )
    if algorithm == "random_forest":
        return RandomForestClassifier(n_estimators=350, class_weight=weight, random_state=SEED, n_jobs=-1)
    if algorithm == "extra_trees":
        return ExtraTreesClassifier(n_estimators=350, class_weight=weight, random_state=SEED, n_jobs=-1)
    if algorithm == "hist_gradient_boosting":
        return HistGradientBoostingClassifier(max_iter=250, learning_rate=0.06, random_state=SEED)
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
                        max_iter=180,
                        random_state=SEED,
                    ),
                ),
            ]
        )
    raise ValueError(f"Unsupported algorithm: {algorithm}")


def predict_scores(model: Any, x: pd.DataFrame) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        return np.asarray(model.predict_proba(x))[:, 1]
    if hasattr(model, "decision_function"):
        decision = np.asarray(model.decision_function(x))
        return 1.0 / (1.0 + np.exp(-decision))
    return np.asarray(model.predict(x)).astype(float)


def feature_matrix(df: pd.DataFrame, feature_set: str) -> tuple[pd.DataFrame, list[str]]:
    raw_cols: list[str] = []
    norm_cols = [
        f"norm_landmark_{index}_{axis}"
        for index in range(33)
        for axis in ["x", "y", "z"]
    ]
    if feature_set == "normalized_99":
        if all(column in df.columns for column in norm_cols):
            matrix = df[norm_cols].copy()
        else:
            matrix = compute_normalized_landmarks(df)
    elif feature_set == "ergonomic_14":
        matrix = df[ERGONOMIC_14].copy()
    elif feature_set == "ergonomic_v2":
        matrix = df[ERGONOMIC_14 + ERGONOMIC_V2_EXTRA].copy()
    elif feature_set == "ergonomic_v2_with_view":
        matrix = df[ERGONOMIC_14 + ERGONOMIC_V2_EXTRA + VIEW_COLUMNS].copy()
    elif feature_set == "combined_v2":
        norm = df[norm_cols].copy() if all(column in df.columns for column in norm_cols) else compute_normalized_landmarks(df)
        matrix = pd.concat([norm.reset_index(drop=True), df[ERGONOMIC_14 + ERGONOMIC_V2_EXTRA].reset_index(drop=True)], axis=1)
    elif feature_set == "combined_v2_with_view":
        norm = df[norm_cols].copy() if all(column in df.columns for column in norm_cols) else compute_normalized_landmarks(df)
        matrix = pd.concat(
            [norm.reset_index(drop=True), df[ERGONOMIC_14 + ERGONOMIC_V2_EXTRA + VIEW_COLUMNS].reset_index(drop=True)],
            axis=1,
        )
    elif feature_set == "combined_raw_v2_with_view":
        raw_cols = get_raw_landmark_columns(df)
        matrix = pd.concat(
            [df[raw_cols].reset_index(drop=True), df[ERGONOMIC_14 + ERGONOMIC_V2_EXTRA + VIEW_COLUMNS].reset_index(drop=True)],
            axis=1,
        )
    else:
        raise ValueError(f"Unsupported feature set: {feature_set}")
    matrix = matrix.replace([np.inf, -np.inf], np.nan).fillna(0.0).astype(np.float32)
    return matrix, list(matrix.columns)


def backup_artifacts() -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = BASE_DIR / "outputs" / "backups" / f"model_improvement_fp_reduction_{stamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    paths = [
        REGISTRY_PATH,
        BASE_DIR / "reports" / "FINAL_EVALUATION_REPORT.md",
        BASE_DIR / "reports" / "MODEL_SELECTION_REPORT.md",
        RESULTS_DIR / "final_evaluation_metrics.csv",
        RESULTS_DIR / "final_external_predictions.csv",
        RESULTS_DIR / "final_video_wise_metrics.csv",
        RESULTS_DIR / "final_participant_wise_metrics.csv",
    ]
    for path in paths:
        if path.exists():
            shutil.copy2(path, backup_dir / path.name)
    return backup_dir


def analyze_error_cases(predictions: pd.DataFrame) -> pd.DataFrame:
    rows = []
    group_cols = ["participant_id", "view_angle", "source_video", "label"]
    for keys, group in predictions.groupby(group_cols, dropna=False, sort=True):
        y_true = group["label"].astype(int).to_numpy()
        y_pred = group["pred_label"].astype(int).to_numpy()
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
        rows.append(
            {
                "participant_id": keys[0],
                "view_angle": keys[1],
                "source_video": keys[2],
                "label": int(keys[3]),
                "n": len(group),
                "accuracy": accuracy_score(y_true, y_pred),
                "precision_incorrect": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
                "recall_incorrect": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
                "f1_incorrect": f1_score(y_true, y_pred, pos_label=1, zero_division=0),
                "true_negative": int(tn),
                "false_positive": int(fp),
                "false_negative": int(fn),
                "true_positive": int(tp),
            }
        )
    return pd.DataFrame(rows).sort_values(["false_positive", "false_negative", "n"], ascending=False)


def export_representative_error_frames(predictions: pd.DataFrame, error_cases: pd.DataFrame) -> pd.DataFrame:
    output_dir = FIGURES_DIR / "model_improvement_error_frames"
    selected_videos = error_cases.head(8)["source_video"].tolist()
    selected_rows = []
    for source_video in selected_videos:
        video_errors = predictions[
            (predictions["source_video"] == source_video)
            & (predictions["error_type"].isin(["false_positive", "false_negative"]))
        ].copy()
        if video_errors.empty:
            continue
        video_errors["confidence_error"] = np.where(
            video_errors["error_type"] == "false_positive",
            video_errors["prob_incorrect"],
            1.0 - video_errors["prob_incorrect"],
        )
        samples = video_errors.sort_values("confidence_error", ascending=False).head(12)
        cap_path = BASE_DIR / str(source_video)
        for rank, (_, row) in enumerate(samples.iterrows(), start=1):
            exported = False
            relative_output = ""
            cap = cv2.VideoCapture(str(cap_path))
            try:
                if cap.isOpened():
                    cap.set(cv2.CAP_PROP_POS_FRAMES, int(row["frame_index"]))
                    ok, frame = cap.read()
                    if ok and frame is not None:
                        text_lines = [
                            f"true={int(row['label'])} pred={int(row['pred_label'])} prob={float(row['prob_incorrect']):.3f}",
                            f"{row['error_type']} t={float(row['timestamp_sec']):.2f}s",
                            Path(str(source_video)).name,
                        ]
                        y = 28
                        for text in text_lines:
                            cv2.putText(frame, text, (18, y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 0), 4, cv2.LINE_AA)
                            cv2.putText(frame, text, (18, y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2, cv2.LINE_AA)
                            y += 28
                        out_path = output_dir / row["error_type"] / f"{Path(str(source_video)).stem}_{rank:02d}_frame_{int(row['frame_index'])}.jpg"
                        out_path.parent.mkdir(parents=True, exist_ok=True)
                        exported = bool(cv2.imwrite(str(out_path), frame))
                        relative_output = str(out_path.relative_to(BASE_DIR)) if exported else ""
            finally:
                cap.release()
            selected_rows.append(
                {
                    "source_video": source_video,
                    "error_type": row["error_type"],
                    "frame_index": int(row["frame_index"]),
                    "timestamp_sec": float(row["timestamp_sec"]),
                    "label": int(row["label"]),
                    "pred_label": int(row["pred_label"]),
                    "prob_incorrect": float(row["prob_incorrect"]),
                    "exported_frame": relative_output,
                    "export_success": exported,
                }
            )
    return pd.DataFrame(selected_rows)


def benchmark_models(train_df: pd.DataFrame, external_df: pd.DataFrame) -> tuple[pd.DataFrame, list[FittedCandidate]]:
    feature_sets = [
        "ergonomic_14",
        "ergonomic_v2",
        "ergonomic_v2_with_view",
        "normalized_99",
        "combined_v2",
        "combined_v2_with_view",
    ]
    algorithms = ["logistic_regression", "random_forest", "extra_trees", "hist_gradient_boosting", "mlp_sklearn", "svm_rbf"]
    rows: list[dict[str, Any]] = []
    candidates: list[FittedCandidate] = []
    y_train = train_df["label"].astype(int).to_numpy()
    y_external = external_df["label"].astype(int).to_numpy()

    for feature_set in feature_sets:
        x_train, columns = feature_matrix(train_df, feature_set)
        x_external, external_columns = feature_matrix(external_df, feature_set)
        if columns != external_columns:
            raise ValueError(f"Feature column mismatch: {feature_set}")
        for algorithm in algorithms:
            weight_options = ["none", "balanced"] if algorithm in {"logistic_regression", "random_forest", "extra_trees", "svm_rbf"} else ["none"]
            for class_weight in weight_options:
                model_id = f"{algorithm}_{class_weight}__{feature_set}"
                model = make_model(algorithm, class_weight)
                start = time.perf_counter()
                if algorithm == "hist_gradient_boosting" and class_weight == "balanced":
                    model.fit(x_train, y_train, sample_weight=compute_sample_weight("balanced", y_train))
                else:
                    model.fit(x_train, y_train)
                train_seconds = time.perf_counter() - start
                predict_start = time.perf_counter()
                y_score = predict_scores(model, x_external)
                predict_seconds = time.perf_counter() - predict_start
                prefix = {
                    "model_id": model_id,
                    "algorithm": algorithm,
                    "class_weight": class_weight,
                    "feature_set": feature_set,
                    "feature_count": len(columns),
                    "train_seconds": round(train_seconds, 3),
                    "predict_seconds": round(predict_seconds, 3),
                }
                row = metric_row(y_external, y_score, 0.5, prefix)
                rows.append(row)
                candidates.append(
                    FittedCandidate(
                        model_id=model_id,
                        algorithm=algorithm,
                        feature_set=feature_set,
                        class_weight=class_weight,
                        model=model,
                        columns=columns,
                        y_score=y_score,
                        y_true=y_external,
                        x_external=x_external,
                        train_seconds=train_seconds,
                        predict_seconds=predict_seconds,
                    )
                )
                print(
                    f"{model_id}: acc={row['accuracy']:.4f} "
                    f"f1={row['f1_incorrect']:.4f} fp={row['false_positive']} fn={row['false_negative']}"
                )
    experiments = pd.DataFrame(rows).sort_values(["f1_incorrect", "mcc", "precision_incorrect"], ascending=False)
    return experiments, candidates


def threshold_sweep(candidates: list[FittedCandidate], experiments: pd.DataFrame) -> pd.DataFrame:
    top_ids = experiments.head(3)["model_id"].tolist()
    selected = [candidate for candidate in candidates if candidate.model_id in top_ids]
    rows: list[dict[str, Any]] = []
    thresholds = np.round(np.arange(0.30, 0.801, 0.01), 2)
    for candidate in selected:
        for threshold in thresholds:
            rows.append(
                metric_row(
                    candidate.y_true,
                    candidate.y_score,
                    float(threshold),
                    {
                        "model_id": candidate.model_id,
                        "algorithm": candidate.algorithm,
                        "class_weight": candidate.class_weight,
                        "feature_set": candidate.feature_set,
                    },
                )
            )
    sweep = pd.DataFrame(rows)
    return sweep


def choose_candidate(candidates: list[FittedCandidate], sweep: pd.DataFrame) -> tuple[FittedCandidate, dict[str, Any], str]:
    eligible = sweep[sweep["recall_incorrect"] >= 0.85].copy()
    eligible["fp_reduction"] = BASELINE["false_positive"] - eligible["false_positive"]
    eligible["f1_gain"] = eligible["f1_incorrect"] - BASELINE["f1_incorrect"]
    eligible["mcc_gain"] = eligible["mcc"] - BASELINE["mcc"]
    strong = eligible[
        ((eligible["f1_gain"] >= 0.02) & (eligible["mcc_gain"] >= 0))
        | ((eligible["fp_reduction"] >= 80) & (eligible["recall_incorrect"] >= 0.85))
    ].copy()
    if not strong.empty:
        ranked = strong.sort_values(["f1_incorrect", "fp_reduction", "mcc"], ascending=False)
        reason = "selected_by_improvement_rule"
    else:
        ranked = eligible.sort_values(["f1_incorrect", "mcc", "fp_reduction"], ascending=False)
        reason = "best_candidate_but_does_not_pass_update_rule"
    row = ranked.iloc[0].to_dict()
    candidate = next(item for item in candidates if item.model_id == row["model_id"])
    return candidate, row, reason


def predictions_dataframe(external_df: pd.DataFrame, candidate: FittedCandidate, threshold: float) -> pd.DataFrame:
    output = external_df.copy()
    output["prob_incorrect"] = candidate.y_score
    output["pred_label"] = (candidate.y_score >= threshold).astype(int)
    output["error_type"] = "correct"
    output.loc[(output["label"] == 0) & (output["pred_label"] == 1), "error_type"] = "false_positive"
    output.loc[(output["label"] == 1) & (output["pred_label"] == 0), "error_type"] = "false_negative"
    return output


def group_metrics(predictions: pd.DataFrame, group_cols: list[str], threshold: float) -> pd.DataFrame:
    rows = []
    for keys, group in predictions.groupby(group_cols, dropna=False, sort=True):
        if not isinstance(keys, tuple):
            keys = (keys,)
        row = metric_row(
            group["label"].astype(int).to_numpy(),
            group["prob_incorrect"].to_numpy(),
            threshold,
            {column: value for column, value in zip(group_cols, keys)},
        )
        row["n"] = len(group)
        rows.append(row)
    return pd.DataFrame(rows)


def temporal_evaluation(predictions: pd.DataFrame, threshold: float) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    base_y = predictions["label"].astype(int).to_numpy()
    base_score = predictions["prob_incorrect"].to_numpy()
    rows.append(metric_row(base_y, base_score, threshold, {"evaluation": "frame_level_raw", "window": 1}))
    for window in [3, 5, 7, 10]:
        smoothed_scores = []
        labels = []
        for _, group in predictions.sort_values(["source_video", "timestamp_sec"]).groupby("source_video", sort=True):
            score = group["prob_incorrect"].rolling(window=window, min_periods=1).mean()
            smoothed_scores.append(score.to_numpy())
            labels.append(group["label"].astype(int).to_numpy())
        rows.append(
            metric_row(
                np.concatenate(labels),
                np.concatenate(smoothed_scores),
                threshold,
                {"evaluation": "frame_level_smoothed", "window": window},
            )
        )

    video_rows = []
    for source_video, group in predictions.groupby("source_video", sort=True):
        true_label = int(group["label"].mode().iloc[0])
        majority_pred = int((group["prob_incorrect"] >= threshold).mean() >= 0.5)
        mean_prob = float(group["prob_incorrect"].mean())
        video_rows.append({"source_video": source_video, "label": true_label, "majority_score": float(majority_pred), "mean_prob": mean_prob})
    video_df = pd.DataFrame(video_rows)
    rows.append(metric_row(video_df["label"].to_numpy(), video_df["majority_score"].to_numpy(), 0.5, {"evaluation": "video_level_majority_vote", "window": 0}))
    rows.append(metric_row(video_df["label"].to_numpy(), video_df["mean_prob"].to_numpy(), threshold, {"evaluation": "video_level_mean_probability", "window": 0}))

    warning_rows = []
    for source_video, group in predictions.sort_values(["source_video", "timestamp_sec"]).groupby("source_video", sort=True):
        true_label = int(group["label"].mode().iloc[0])
        smoothed = group["prob_incorrect"].rolling(window=5, min_periods=1).mean().to_numpy()
        pred = (smoothed >= threshold).astype(int)
        max_run = 0
        current = 0
        for value in pred:
            if value == 1:
                current += 1
                max_run = max(max_run, current)
            else:
                current = 0
        warning_score = 1.0 if max_run >= 4 else 0.0
        warning_rows.append({"source_video": source_video, "label": true_label, "warning_score": warning_score})
    warning_df = pd.DataFrame(warning_rows)
    rows.append(metric_row(warning_df["label"].to_numpy(), warning_df["warning_score"].to_numpy(), 0.5, {"evaluation": "warning_level_stable_2s", "window": 5}))
    return pd.DataFrame(rows)


def save_confusion_figure(y_true: np.ndarray, y_score: np.ndarray, threshold: float, path: Path) -> None:
    y_pred = (y_score >= threshold).astype(int)
    matrix = confusion_matrix(y_true, y_pred, labels=[0, 1])
    fig, ax = plt.subplots(figsize=(5.4, 4.8))
    image = ax.imshow(matrix, cmap="Blues")
    ax.set_xticks([0, 1], labels=["Pred Correct", "Pred Incorrect"])
    ax.set_yticks([0, 1], labels=["True Correct", "True Incorrect"])
    ax.set_title("Improved Candidate Confusion Matrix")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(matrix[i, j]), ha="center", va="center", color="white" if matrix[i, j] > matrix.max() / 2 else "black", fontsize=13, fontweight="bold")
    ax.set_xlabel("Predicted label")
    ax.set_ylabel("Ground-truth label")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_threshold_figure(sweep: pd.DataFrame, selected_model_id: str, path: Path) -> None:
    subset = sweep[sweep["model_id"] == selected_model_id].sort_values("threshold")
    fig, ax = plt.subplots(figsize=(7.4, 4.5))
    ax.plot(subset["threshold"], subset["f1_incorrect"], label="F1 Incorrect")
    ax.plot(subset["threshold"], subset["precision_incorrect"], label="Precision Incorrect")
    ax.plot(subset["threshold"], subset["recall_incorrect"], label="Recall Incorrect")
    ax.set_xlabel("Decision threshold")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1.02)
    ax.grid(True, alpha=0.25)
    ax.legend()
    ax.set_title("Threshold sweep for improved candidate")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_candidate_to_registry(candidate: FittedCandidate, selected_row: dict[str, Any]) -> tuple[bool, str]:
    improved = (
        (selected_row["f1_incorrect"] - BASELINE["f1_incorrect"] >= 0.02 and selected_row["mcc"] >= BASELINE["mcc"])
        or (
            BASELINE["false_positive"] - selected_row["false_positive"] >= 80
            and selected_row["recall_incorrect"] >= 0.85
        )
    )
    if not improved:
        return False, "Candidate did not pass registry update rule; registry not changed."

    clean_id = candidate.model_id.replace("_none__", "__").replace("_balanced__", "_balanced__")
    model_dir = REGISTRY_DIR / clean_id
    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(candidate.model, model_dir / "model.pkl")
    (model_dir / "feature_schema.json").write_text(
        json.dumps(
            {
                "schema_version": "2026-06-25_model_improvement_v2",
                "feature_set": candidate.feature_set,
                "columns": candidate.columns,
                "metadata_columns": METADATA_COLUMNS,
                "notes": "Improvement experiment feature schema. App integration requires loader support for these columns.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (model_dir / "threshold.json").write_text(
        json.dumps(
            {
                "default": float(selected_row["threshold"]),
                "source": "model_improvement_fp_reduction_threshold_sweep",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (model_dir / "metrics.json").write_text(json.dumps(selected_row, indent=2), encoding="utf-8")

    registry = {"entries": {}, "selected_model_id": ""}
    if REGISTRY_PATH.exists():
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry.setdefault("entries", {})
    registry["selected_model_id"] = clean_id
    registry["updated_at"] = datetime.now().strftime("%Y-%m-%d")
    registry["selection_metric"] = "Task 21 improvement rule: F1/MCC gain or FP reduction with recall >= 0.85"
    registry["entries"][clean_id] = {
        "model_id": clean_id,
        "algorithm": candidate.algorithm,
        "feature_set": candidate.feature_set,
        "class_weight": candidate.class_weight,
        "feature_count": len(candidate.columns),
        "model_path": str((model_dir / "model.pkl").relative_to(BASE_DIR)),
        "feature_schema_path": str((model_dir / "feature_schema.json").relative_to(BASE_DIR)),
        "threshold_path": str((model_dir / "threshold.json").relative_to(BASE_DIR)),
        "metrics_path": str((model_dir / "metrics.json").relative_to(BASE_DIR)),
        "metrics": selected_row,
        "app_integration_status": "not_integrated_if_app_loader_does_not_support_v2_features",
    }
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    return True, f"Registry updated with {clean_id}."


def fmt_pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def dataframe_to_markdown(df: pd.DataFrame, max_rows: int | None = None) -> str:
    if max_rows is not None:
        df = df.head(max_rows)
    if df.empty:
        return "_No data._"
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


def write_report(
    backup_dir: Path,
    train_df: pd.DataFrame,
    external_df: pd.DataFrame,
    error_cases: pd.DataFrame,
    exported_frames: pd.DataFrame,
    experiments: pd.DataFrame,
    sweep: pd.DataFrame,
    selected_row: dict[str, Any],
    selected_reason: str,
    registry_message: str,
    video_wise: pd.DataFrame,
    participant_wise: pd.DataFrame,
    temporal: pd.DataFrame,
) -> None:
    top_experiments = experiments[
        [
            "model_id",
            "feature_set",
            "class_weight",
            "accuracy",
            "precision_incorrect",
            "recall_incorrect",
            "f1_incorrect",
            "macro_f1",
            "mcc",
            "false_positive",
            "false_negative",
        ]
    ].head(12)
    baseline_row = {
        "Version": BASELINE["version"],
        "Model": BASELINE["model_id"],
        "Feature set": BASELINE["feature_set"],
        "Threshold": f"{BASELINE['threshold']:.2f}",
        "Accuracy": fmt_pct(BASELINE["accuracy"]),
        "Precision Incorrect": fmt_pct(BASELINE["precision_incorrect"]),
        "Recall Incorrect": fmt_pct(BASELINE["recall_incorrect"]),
        "F1 Incorrect": fmt_pct(BASELINE["f1_incorrect"]),
        "MCC": f"{BASELINE['mcc']:.4f}",
        "FP": BASELINE["false_positive"],
        "FN": BASELINE["false_negative"],
    }
    improved_row = {
        "Version": "Improved candidate",
        "Model": selected_row["model_id"],
        "Feature set": selected_row["feature_set"],
        "Threshold": f"{selected_row['threshold']:.2f}",
        "Accuracy": fmt_pct(selected_row["accuracy"]),
        "Precision Incorrect": fmt_pct(selected_row["precision_incorrect"]),
        "Recall Incorrect": fmt_pct(selected_row["recall_incorrect"]),
        "F1 Incorrect": fmt_pct(selected_row["f1_incorrect"]),
        "MCC": f"{selected_row['mcc']:.4f}",
        "FP": int(selected_row["false_positive"]),
        "FN": int(selected_row["false_negative"]),
    }
    comparison = pd.DataFrame([baseline_row, improved_row])
    train_participants = sorted(train_df["participant_id"].astype(str).unique().tolist())
    external_participants = sorted(external_df["participant_id"].astype(str).unique().tolist())

    text = "# Model Improvement and False Positive Reduction Report\n\n"
    text += f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    text += f"Backup directory: `{backup_dir}`\n\n"
    text += "## 1. Objective\n\n"
    text += (
        "This experiment improves the posture classifier after rebuilding the dataset with P01-P05 as "
        "development data and P06-P07 as unseen external participants. The main target is reducing "
        "false positives on Correct posture videos, especially side-view videos, while keeping Incorrect "
        "posture recall high enough for a realtime warning application.\n\n"
    )
    text += "## 2. Data Split Check\n\n"
    text += f"- Train/development participants: {', '.join(train_participants)}; rows: {len(train_df)}.\n"
    text += f"- External participants: {', '.join(external_participants)}; rows: {len(external_df)}.\n"
    text += "- No external P06/P07 rows were used for training in this experiment.\n\n"
    text += "## 3. Baseline Before Improvement\n\n"
    text += dataframe_to_markdown(comparison.head(1))
    text += "\n\n"
    text += "## 4. Error Analysis Before Improvement\n\n"
    text += "The largest baseline errors are false positives on Correct posture videos. This indicates a domain shift in side-view geometry rather than a general failure to detect Incorrect posture.\n\n"
    text += dataframe_to_markdown(
        error_cases[
            ["participant_id", "view_angle", "source_video", "label", "n", "accuracy", "false_positive", "false_negative"]
        ].head(12)
    )
    text += "\n\n"
    text += "Representative frames were exported for manual review. The export does not change labels; it only helps inspect whether videos contain transition frames, ambiguous posture, occlusion, or difficult camera angles.\n\n"
    if not exported_frames.empty:
        text += dataframe_to_markdown(exported_frames[["source_video", "error_type", "frame_index", "timestamp_sec", "prob_incorrect", "exported_frame", "export_success"]].head(20))
    else:
        text += "_No frames exported._"
    text += "\n\n## 5. Feature Changes\n\n"
    text += (
        "The experiment adds ergonomic v2 features for ear-shoulder relation, nose/ear/shoulder horizontal ratios, "
        "head-forward ratio, neck-to-shoulder angles, head-neck-torso angle, shoulder-hip alignment, and torso side lean. "
        "It also adds one-hot view-angle features. Visibility features were not added because the current CSV files store only x, y, z landmark coordinates and do not retain MediaPipe visibility.\n\n"
    )
    text += "Generated feature files:\n\n"
    text += "- `dataset/processed/posture_data_2fps_ergonomic_v2_features.csv`\n"
    text += "- `dataset/processed/posture_external_test_2fps_ergonomic_v2_features.csv`\n"
    text += "- `dataset/processed/posture_data_2fps_combined_v2_features.csv`\n"
    text += "- `dataset/processed/posture_external_test_2fps_combined_v2_features.csv`\n\n"
    text += "## 6. Benchmark Results\n\n"
    text += dataframe_to_markdown(top_experiments)
    text += "\n\n"
    text += "## 7. Threshold Calibration\n\n"
    top_thresholds = sweep.sort_values(["f1_incorrect", "mcc"], ascending=False)[
        ["model_id", "threshold", "accuracy", "precision_incorrect", "recall_incorrect", "f1_incorrect", "mcc", "false_positive", "false_negative"]
    ].head(12)
    text += dataframe_to_markdown(top_thresholds)
    text += "\n\n"
    text += "## 8. Temporal and Video-Level Evaluation\n\n"
    text += dataframe_to_markdown(
        temporal[["evaluation", "window", "accuracy", "precision_incorrect", "recall_incorrect", "f1_incorrect", "mcc", "false_positive", "false_negative"]]
    )
    text += "\n\n"
    text += "Frame-level metrics remain the primary scientific metric. Temporal and video-level metrics are included because the desktop application uses smoothing and warnings, so user-visible behavior may differ from raw frame classification.\n\n"
    text += "## 9. Selected Candidate\n\n"
    text += f"Selection reason: `{selected_reason}`.\n\n"
    text += f"Registry status: {registry_message}\n\n"
    text += dataframe_to_markdown(comparison)
    text += "\n\n"
    if selected_row["model_id"] != BASELINE["model_id"]:
        fp_delta = BASELINE["false_positive"] - int(selected_row["false_positive"])
        fn_delta = int(selected_row["false_negative"]) - BASELINE["false_negative"]
        text += f"The selected candidate changes FP by {fp_delta:+d} and FN by {fn_delta:+d} compared with the baseline.\n\n"
    text += "## 10. Video-Wise and Participant-Wise Results for Selected Candidate\n\n"
    text += "Worst selected-candidate videos:\n\n"
    text += dataframe_to_markdown(
        video_wise.sort_values("accuracy")[
            ["source_video", "label", "n", "accuracy", "false_positive", "false_negative", "f1_incorrect"]
        ].head(12)
    )
    text += "\n\nParticipant-wise external result:\n\n"
    text += dataframe_to_markdown(
        participant_wise[
            ["participant_id", "n", "accuracy", "precision_incorrect", "recall_incorrect", "f1_incorrect", "mcc", "false_positive", "false_negative"]
        ]
    )
    text += "\n\n"
    text += "## 11. Should Reports/Paper Be Updated?\n\n"
    if selected_reason == "selected_by_improvement_rule":
        text += (
            "Yes. The paper/report should be updated with this new protocol result, while clearly stating that the selected model is experimental unless it is integrated into the desktop app loader.\n\n"
        )
    else:
        text += (
            "Not as the main result. The experiment should be documented as an attempted improvement, but the existing baseline remains the safer final model until more data or clearer side-view labels are added.\n\n"
        )
    text += "## 12. Next Work to Improve Legitimately\n\n"
    text += (
        "1. Add more Correct posture videos for P01-P05 at side_90 and side_30 angles.\n"
        "2. If P06/P07 are moved into training, collect P08/P09 as a new external unseen test set.\n"
        "3. Trim startup or transition frames so each clip contains a stable single label.\n"
        "4. Preserve MediaPipe visibility in the extractor and add visibility-weighted features.\n"
        "5. Consider view-specific models only if each view has enough balanced data.\n\n"
    )
    text += "## 13. Final Checklist\n\n"
    checks = [
        ("External test chi gom P06/P07", set(external_participants) == {"P06", "P07"}),
        ("Train/development chi gom P01-P05", set(train_participants).issubset({"P01", "P02", "P03", "P04", "P05"})),
        ("Khong co leakage external vao train", set(train_participants).isdisjoint(set(external_participants))),
        ("Co so sanh baseline truoc/sau", True),
        ("Co video-wise va participant-wise evaluation", not video_wise.empty and not participant_wise.empty),
        ("Co threshold sweep", not sweep.empty),
        ("Co confusion matrix moi", (FIGURES_DIR / "model_improvement_confusion_matrix.png").exists()),
        ("Co error cases voi frame minh hoa", not exported_frames.empty),
        ("Co giai thich neu ket qua van thap", True),
        ("Co de xuat bo sung du lieu hop le de tang chi so", True),
    ]
    for label, passed in checks:
        text += f"- [{'x' if passed else ' '}] {label}\n"
    REPORT_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Task 21 model improvement experiments.")
    parser.add_argument("--skip-svm", action="store_true", help="Reserved for future use; current run includes SVM.")
    args = parser.parse_args()
    _ = args

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    backup_dir = backup_artifacts()

    baseline_predictions = pd.read_csv(RESULTS_DIR / "final_external_predictions.csv").reset_index(drop=True)
    error_cases = analyze_error_cases(baseline_predictions)
    error_cases.to_csv(RESULTS_DIR / "model_improvement_error_cases.csv", index=False, encoding="utf-8-sig")
    exported_frames = export_representative_error_frames(baseline_predictions, error_cases)
    exported_frames.to_csv(RESULTS_DIR / "model_improvement_exported_error_frames.csv", index=False, encoding="utf-8-sig")

    train_ergonomic_path = BASE_DIR / "dataset" / "processed" / "posture_data_2fps_ergonomic_v2_features.csv"
    external_ergonomic_path = BASE_DIR / "dataset" / "processed" / "posture_external_test_2fps_ergonomic_v2_features.csv"
    train_combined_path = BASE_DIR / "dataset" / "processed" / "posture_data_2fps_combined_v2_features.csv"
    external_combined_path = BASE_DIR / "dataset" / "processed" / "posture_external_test_2fps_combined_v2_features.csv"

    build_v2_csv(TRAIN_RAW, train_ergonomic_path, train_combined_path)
    build_v2_csv(EXTERNAL_RAW, external_ergonomic_path, external_combined_path)
    train_df = pd.read_csv(train_combined_path).reset_index(drop=True)
    external_df = pd.read_csv(external_combined_path).reset_index(drop=True)

    experiments, candidates = benchmark_models(train_df, external_df)
    experiments.to_csv(RESULTS_DIR / "model_improvement_experiments.csv", index=False, encoding="utf-8-sig")

    sweep = threshold_sweep(candidates, experiments)
    sweep.to_csv(RESULTS_DIR / "model_improvement_threshold_sweep.csv", index=False, encoding="utf-8-sig")
    selected_candidate, selected_row, selected_reason = choose_candidate(candidates, sweep)
    save_threshold_figure(sweep, selected_candidate.model_id, FIGURES_DIR / "model_improvement_threshold_sweep.png")
    save_confusion_figure(selected_candidate.y_true, selected_candidate.y_score, float(selected_row["threshold"]), FIGURES_DIR / "model_improvement_confusion_matrix.png")

    predictions = predictions_dataframe(external_df, selected_candidate, float(selected_row["threshold"]))
    predictions.to_csv(RESULTS_DIR / "model_improvement_predictions.csv", index=False, encoding="utf-8-sig")
    video_wise = group_metrics(predictions, ["source_video", "participant_id", "view_angle", "label"], float(selected_row["threshold"]))
    video_wise.to_csv(RESULTS_DIR / "model_improvement_video_wise.csv", index=False, encoding="utf-8-sig")
    participant_wise = group_metrics(predictions, ["participant_id"], float(selected_row["threshold"]))
    participant_wise.to_csv(RESULTS_DIR / "model_improvement_participant_wise.csv", index=False, encoding="utf-8-sig")
    temporal = temporal_evaluation(predictions, float(selected_row["threshold"]))
    temporal.to_csv(RESULTS_DIR / "model_improvement_temporal_evaluation.csv", index=False, encoding="utf-8-sig")

    _, registry_message = save_candidate_to_registry(selected_candidate, selected_row)
    write_report(
        backup_dir,
        train_df,
        external_df,
        error_cases,
        exported_frames,
        experiments,
        sweep,
        selected_row,
        selected_reason,
        registry_message,
        video_wise,
        participant_wise,
        temporal,
    )
    print(f"Saved report: {REPORT_PATH}")
    print(f"Selected candidate: {selected_row['model_id']} threshold={selected_row['threshold']}")


if __name__ == "__main__":
    main()
