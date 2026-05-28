"""Benchmark MediaPipe + ANN inference latency on a video source."""

from __future__ import annotations

import argparse
import os
import time
from pathlib import Path
from typing import Any

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import cv2
import joblib
import mediapipe as mp
import numpy as np
import pandas as pd
import tensorflow as tf


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_VIDEO = BASE_DIR / "dataset" / "external_videos" / "correct" / "P01_correct_001.mp4"
DEFAULT_MODEL = BASE_DIR / "models" / "ann_best.keras"
DEFAULT_SCALER = BASE_DIR / "models" / "scaler.pkl"
DEFAULT_OUTPUT_DIR = BASE_DIR / "reports" / "results"
NUM_POSE_LANDMARKS = 33
NUM_FEATURES = 99


def resolve_path(path_text: str | Path) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else BASE_DIR / path


def landmark_vector(pose_landmarks: Any) -> list[float] | None:
    if pose_landmarks is None:
        return None
    landmarks = getattr(pose_landmarks, "landmark", None)
    if landmarks is None or len(landmarks) < NUM_POSE_LANDMARKS:
        return None
    vector: list[float] = []
    for landmark in landmarks[:NUM_POSE_LANDMARKS]:
        vector.extend([float(landmark.x), float(landmark.y), float(landmark.z)])
    return vector if len(vector) == NUM_FEATURES else None


def percentile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    return float(np.percentile(np.asarray(values, dtype=np.float64), q))


def run_benchmark(args: argparse.Namespace) -> None:
    video_path = resolve_path(args.video)
    model_path = resolve_path(args.model)
    scaler_path = resolve_path(args.scaler)
    output_dir = resolve_path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not video_path.exists():
        raise FileNotFoundError(f"Video not found: {video_path}")

    model = tf.keras.models.load_model(model_path)
    scaler = joblib.load(scaler_path)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    rows: list[dict[str, float | int | str]] = []
    with mp.solutions.pose.Pose(
        static_image_mode=False,
        model_complexity=args.model_complexity,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as pose:
        frame_index = 0
        processed = 0
        while processed < args.max_frames:
            success, frame = cap.read()
            if not success or frame is None:
                break
            if args.frame_stride > 1 and frame_index % args.frame_stride != 0:
                frame_index += 1
                continue

            total_start = time.perf_counter()
            resized = cv2.resize(frame, (args.width, args.height), interpolation=cv2.INTER_AREA)
            rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

            pose_start = time.perf_counter()
            results = pose.process(rgb)
            pose_ms = (time.perf_counter() - pose_start) * 1000.0

            vector = landmark_vector(results.pose_landmarks)
            model_ms = 0.0
            prob_incorrect = np.nan
            detected = 0
            if vector is not None:
                detected = 1
                model_start = time.perf_counter()
                X = scaler.transform(np.array([vector], dtype=np.float32))
                prob_incorrect = float(np.asarray(model(X, training=False)).reshape(-1)[0])
                model_ms = (time.perf_counter() - model_start) * 1000.0

            total_ms = (time.perf_counter() - total_start) * 1000.0
            rows.append(
                {
                    "frame_index": frame_index,
                    "pose_detected": detected,
                    "pose_ms": pose_ms,
                    "model_ms": model_ms,
                    "total_ms": total_ms,
                    "prob_incorrect": prob_incorrect,
                }
            )
            processed += 1
            frame_index += 1

    cap.release()

    df = pd.DataFrame(rows)
    csv_path = output_dir / "runtime_benchmark.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    total_values = df["total_ms"].astype(float).tolist() if not df.empty else []
    pose_values = df["pose_ms"].astype(float).tolist() if not df.empty else []
    model_values = df["model_ms"].astype(float).tolist() if not df.empty else []
    mean_total = float(np.mean(total_values)) if total_values else 0.0
    mean_fps = 1000.0 / mean_total if mean_total > 0 else 0.0
    detection_rate = float(df["pose_detected"].mean()) if not df.empty else 0.0

    report = f"""# Runtime Benchmark

Video: `{video_path}`
Model: `{model_path}`
Scaler: `{scaler_path}`
Resolution: {args.width}x{args.height}
Max frames: {args.max_frames}
Frame stride: {args.frame_stride}
MediaPipe model complexity: {args.model_complexity}

| Metric | Value |
|---|---:|
| Processed frames | {len(df)} |
| Pose detection rate | {detection_rate:.3f} |
| Mean total latency ms | {mean_total:.3f} |
| P50 total latency ms | {percentile(total_values, 50):.3f} |
| P95 total latency ms | {percentile(total_values, 95):.3f} |
| Mean estimated FPS | {mean_fps:.3f} |
| Mean MediaPipe latency ms | {float(np.mean(pose_values)) if pose_values else 0.0:.3f} |
| Mean ANN latency ms | {float(np.mean(model_values)) if model_values else 0.0:.3f} |

CSV details: `reports/results/runtime_benchmark.csv`

Interpretation: this benchmark measures processing latency only. Full GUI FPS can
be lower because of drawing, Tkinter scheduling, camera buffering, and audio/logging.
"""
    report_path = BASE_DIR / "reports" / "RUNTIME_BENCHMARK.md"
    report_path.write_text(report, encoding="utf-8")

    print(report)
    print(f"Saved: {csv_path}")
    print(f"Saved: {report_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark MediaPipe + ANN runtime.")
    parser.add_argument("--video", default=str(DEFAULT_VIDEO))
    parser.add_argument("--model", default=str(DEFAULT_MODEL))
    parser.add_argument("--scaler", default=str(DEFAULT_SCALER))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--max-frames", type=int, default=120)
    parser.add_argument("--frame-stride", type=int, default=15)
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=360)
    parser.add_argument("--model-complexity", type=int, default=1)
    return parser.parse_args()


if __name__ == "__main__":
    run_benchmark(parse_args())
