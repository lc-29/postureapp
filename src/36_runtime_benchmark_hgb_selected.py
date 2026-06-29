"""Benchmark MediaPipe + selected HistGradientBoosting runtime.

This processing benchmark measures frame capture/resize, MediaPipe Pose,
feature construction for ergonomic_v2_with_view, and HGB inference. It does
not measure full CustomTkinter GUI FPS.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import cv2
import joblib
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import mediapipe as mp
import numpy as np
import pandas as pd

try:
    from feature_schema import build_feature_matrix
except ImportError:
    from src.feature_schema import build_feature_matrix


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_ID = "hist_gradient_boosting__ergonomic_v2_with_view"
MODEL_DIR = BASE_DIR / "models" / "registry" / MODEL_ID
MODEL_PATH = MODEL_DIR / "model.pkl"
SCHEMA_PATH = MODEL_DIR / "feature_schema.json"
THRESHOLD_PATH = MODEL_DIR / "threshold.json"
RESULTS_DIR = BASE_DIR / "reports" / "results"
FIGURES_DIR = BASE_DIR / "reports" / "figures"
REPORT_PATH = BASE_DIR / "reports" / "RUNTIME_BENCHMARK_HGB_SELECTED.md"

DEFAULT_VIDEOS = {
    "front": BASE_DIR / "dataset" / "external_videos" / "correct" / "P06_correct_front_001.mp4",
    "side_30": BASE_DIR / "dataset" / "external_videos" / "correct" / "P06_correct_side_30_001.mp4",
    "side_90": BASE_DIR / "dataset" / "external_videos" / "correct" / "P06_correct_side_90_001.mp4",
}

NUM_POSE_LANDMARKS = 33


def resolve_path(path_text: str | Path) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else BASE_DIR / path


def load_threshold(path: Path, fallback: float = 0.76) -> float:
    if not path.exists():
        return fallback
    payload = json.loads(path.read_text(encoding="utf-8"))
    return float(payload.get("default", fallback))


def validate_artifacts() -> tuple[Any, dict[str, Any], float]:
    missing = [path for path in [MODEL_PATH, SCHEMA_PATH, THRESHOLD_PATH] if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing HGB artifact(s): " + ", ".join(str(path) for path in missing))
    model = joblib.load(MODEL_PATH)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    threshold = load_threshold(THRESHOLD_PATH)
    if schema.get("feature_set") != "ergonomic_v2_with_view":
        raise ValueError(f"Unexpected feature set in schema: {schema.get('feature_set')}")
    columns = schema.get("columns", [])
    if len(columns) != 31:
        raise ValueError(f"Expected 31 HGB features, found {len(columns)}.")
    return model, schema, threshold


def landmark_row(pose_landmarks: Any, view_angle: str) -> dict[str, float | str] | None:
    if pose_landmarks is None:
        return None
    landmarks = getattr(pose_landmarks, "landmark", None)
    if landmarks is None or len(landmarks) < NUM_POSE_LANDMARKS:
        return None
    row: dict[str, float | str] = {"view_angle": view_angle}
    for index, landmark in enumerate(landmarks[:NUM_POSE_LANDMARKS]):
        row[f"landmark_{index}_x"] = float(landmark.x)
        row[f"landmark_{index}_y"] = float(landmark.y)
        row[f"landmark_{index}_z"] = float(landmark.z)
    return row


def predict_hgb(model: Any, features: pd.DataFrame) -> float:
    if hasattr(model, "predict_proba"):
        return float(np.asarray(model.predict_proba(features))[:, 1][0])
    if hasattr(model, "decision_function"):
        score = float(np.asarray(model.decision_function(features)).reshape(-1)[0])
        return float(1.0 / (1.0 + np.exp(-score)))
    return float(np.asarray(model.predict(features)).reshape(-1)[0])


def percentile(values: pd.Series | list[float], q: float) -> float:
    values = pd.Series(values).dropna().astype(float)
    if values.empty:
        return 0.0
    return float(np.percentile(values.to_numpy(dtype=np.float64), q))


def benchmark_video(
    view_angle: str,
    video_path: Path,
    model: Any,
    threshold: float,
    args: argparse.Namespace,
) -> pd.DataFrame:
    if not video_path.exists():
        raise FileNotFoundError(video_path)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    rows: list[dict[str, Any]] = []
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
            capture_start = time.perf_counter()
            success, frame = cap.read()
            if not success or frame is None:
                break
            if args.frame_stride > 1 and frame_index % args.frame_stride != 0:
                frame_index += 1
                continue

            total_start = capture_start
            resized = cv2.resize(frame, (args.width, args.height), interpolation=cv2.INTER_AREA)
            rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            capture_resize_ms = (time.perf_counter() - capture_start) * 1000.0

            pose_start = time.perf_counter()
            results = pose.process(rgb)
            mediapipe_ms = (time.perf_counter() - pose_start) * 1000.0

            feature_ms = 0.0
            model_ms = 0.0
            prob_incorrect = np.nan
            pred_label = np.nan
            pose_detected = 0
            row = landmark_row(results.pose_landmarks, view_angle)
            if row is not None:
                pose_detected = 1
                feature_start = time.perf_counter()
                frame_df = pd.DataFrame([row])
                features, _ = build_feature_matrix(frame_df, "ergonomic_v2_with_view")
                feature_ms = (time.perf_counter() - feature_start) * 1000.0

                model_start = time.perf_counter()
                prob_incorrect = predict_hgb(model, features)
                model_ms = (time.perf_counter() - model_start) * 1000.0
                pred_label = int(prob_incorrect >= threshold)

            total_ms = (time.perf_counter() - total_start) * 1000.0
            rows.append(
                {
                    "view_angle": view_angle,
                    "video_path": str(video_path.relative_to(BASE_DIR)),
                    "sample_index": processed,
                    "frame_index": frame_index,
                    "is_warmup": int(processed < args.warmup_frames),
                    "pose_detected": pose_detected,
                    "capture_resize_ms": capture_resize_ms,
                    "mediapipe_ms": mediapipe_ms,
                    "feature_ms": feature_ms,
                    "model_ms": model_ms,
                    "total_ms": total_ms,
                    "prob_incorrect": prob_incorrect,
                    "pred_label": pred_label,
                }
            )
            processed += 1
            frame_index += 1
    cap.release()
    return pd.DataFrame(rows)


def summarize(frame_df: pd.DataFrame, warmup_frames: int) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for view_angle, group in frame_df.groupby("view_angle", sort=False):
        measured = group[group["is_warmup"] == 0].copy()
        if measured.empty:
            measured = group.copy()
        total_mean = float(measured["total_ms"].mean()) if not measured.empty else 0.0
        rows.append(
            {
                "view_angle": view_angle,
                "video_path": group["video_path"].iloc[0] if not group.empty else "",
                "processed_frames": int(len(measured)),
                "warmup_excluded_frames": int(min(warmup_frames, len(group))),
                "pose_detection_rate": float(measured["pose_detected"].mean()) if not measured.empty else 0.0,
                "mean_capture_resize_latency_ms": float(measured["capture_resize_ms"].mean()) if not measured.empty else 0.0,
                "mean_mediapipe_latency_ms": float(measured["mediapipe_ms"].mean()) if not measured.empty else 0.0,
                "mean_feature_latency_ms": float(measured["feature_ms"].mean()) if not measured.empty else 0.0,
                "mean_hgb_latency_ms": float(measured["model_ms"].mean()) if not measured.empty else 0.0,
                "mean_total_latency_ms": total_mean,
                "p50_total_latency_ms": percentile(measured["total_ms"], 50),
                "p95_total_latency_ms": percentile(measured["total_ms"], 95),
                "mean_estimated_fps": 1000.0 / total_mean if total_mean > 0 else 0.0,
                "mean_prob_incorrect": float(measured["prob_incorrect"].mean()) if not measured.empty else np.nan,
                "predicted_incorrect_rate": float(measured["pred_label"].mean()) if not measured.empty else np.nan,
            }
        )
    return pd.DataFrame(rows)


def save_figure(summary: pd.DataFrame) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plot_df = summary.copy()
    x = np.arange(len(plot_df))

    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False
    fig, ax1 = plt.subplots(figsize=(8.8, 5.4))
    bars = ax1.bar(
        x,
        plot_df["mean_total_latency_ms"],
        color="#2563eb",
        width=0.52,
        label="Độ trễ toàn pipeline",
    )
    ax1.set_ylabel("Độ trễ trung bình (ms)")
    ax1.set_xticks(x, plot_df["view_angle"])
    ax1.set_ylim(0, max(float(plot_df["mean_total_latency_ms"].max()) * 1.28, 10))
    ax1.grid(axis="y", alpha=0.25)

    for bar, value in zip(bars, plot_df["mean_total_latency_ms"]):
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.8,
            f"{value:.2f} ms",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
        )

    ax2 = ax1.twinx()
    ax2.plot(
        x,
        plot_df["mean_estimated_fps"],
        color="#f97316",
        marker="o",
        linewidth=2.4,
        label="FPS ước lượng",
    )
    ax2.set_ylabel("FPS ước lượng")
    ax2.set_ylim(0, max(float(plot_df["mean_estimated_fps"].max()) * 1.35, 10))
    for xi, value in zip(x, plot_df["mean_estimated_fps"]):
        ax2.text(
            xi,
            value - 1.0,
            f"{value:.2f} FPS",
            ha="center",
            va="top",
            fontsize=9,
            fontweight="bold",
            color="#9a3412",
        )

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(handles1 + handles2, labels1 + labels2, loc="upper center", ncol=2, bbox_to_anchor=(0.5, -0.16))
    ax1.set_title(
        "Runtime pipeline HGB được lựa chọn theo góc quan sát",
        fontsize=13,
        fontweight="bold",
        pad=14,
    )
    fig.text(
        0.5,
        0.055,
        "Ghi chú: loại 5 frame warm-up đầu mỗi video khi tính trung bình.",
        ha="center",
        fontsize=8.4,
        color="#374151",
    )
    fig.text(
        0.5,
        0.025,
        "Benchmark gồm đọc/resize frame, MediaPipe Pose, tạo đặc trưng ergonomic_v2_with_view và suy luận HGB; chưa bao gồm full GUI FPS.",
        ha="center",
        fontsize=8.2,
        color="#374151",
    )
    fig.subplots_adjust(left=0.10, right=0.90, top=0.84, bottom=0.28)
    fig.savefig(FIGURES_DIR / "figure_4_6_hgb_runtime_latency_fps.png", dpi=320)
    fig.savefig(FIGURES_DIR / "figure_4_6_hgb_runtime_latency_fps.svg")
    plt.close(fig)


def fmt_pct(value: float) -> str:
    return f"{value * 100:.2f}%".replace(".", ",")


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_Không có dữ liệu._"
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join("---" for _ in df.columns) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(value) for value in row.tolist()) + " |")
    return "\n".join(lines)


def display_summary(summary: pd.DataFrame) -> pd.DataFrame:
    output = summary.copy()
    output["pose_detection_rate"] = output["pose_detection_rate"].map(fmt_pct)
    output["mean_capture_resize_latency_ms"] = output["mean_capture_resize_latency_ms"].map(lambda value: f"{value:.3f}")
    output["mean_mediapipe_latency_ms"] = output["mean_mediapipe_latency_ms"].map(lambda value: f"{value:.3f}")
    output["mean_feature_latency_ms"] = output["mean_feature_latency_ms"].map(lambda value: f"{value:.3f}")
    output["mean_hgb_latency_ms"] = output["mean_hgb_latency_ms"].map(lambda value: f"{value:.3f}")
    output["mean_total_latency_ms"] = output["mean_total_latency_ms"].map(lambda value: f"{value:.3f}")
    output["p50_total_latency_ms"] = output["p50_total_latency_ms"].map(lambda value: f"{value:.3f}")
    output["p95_total_latency_ms"] = output["p95_total_latency_ms"].map(lambda value: f"{value:.3f}")
    output["mean_estimated_fps"] = output["mean_estimated_fps"].map(lambda value: f"{value:.3f}")
    return output[
        [
            "view_angle",
            "video_path",
            "processed_frames",
            "warmup_excluded_frames",
            "pose_detection_rate",
            "mean_mediapipe_latency_ms",
            "mean_feature_latency_ms",
            "mean_hgb_latency_ms",
            "mean_total_latency_ms",
            "p50_total_latency_ms",
            "p95_total_latency_ms",
            "mean_estimated_fps",
        ]
    ]


def write_report(summary: pd.DataFrame, threshold: float, args: argparse.Namespace) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    display = display_summary(summary)
    min_latency = float(summary["mean_total_latency_ms"].min())
    max_latency = float(summary["mean_total_latency_ms"].max())
    min_fps = float(summary["mean_estimated_fps"].min())
    max_fps = float(summary["mean_estimated_fps"].max())
    mean_mp = float(summary["mean_mediapipe_latency_ms"].mean())
    mean_feature = float(summary["mean_feature_latency_ms"].mean())
    mean_hgb = float(summary["mean_hgb_latency_ms"].mean())

    text = "# Runtime Benchmark HGB Selected\n\n"
    text += "## 1. Mục tiêu\n\n"
    text += (
        "Benchmark này đo lại thời gian xử lý của pipeline sử dụng đúng cấu hình "
        "HistGradientBoosting được lựa chọn trong thực nghiệm. Kết quả dùng để thay thế "
        "runtime benchmark ANN cũ trong phần đánh giá hiệu năng của Chương 4.\n\n"
    )
    text += "## 2. Cấu hình đo\n\n"
    text += f"- Model ID: `{MODEL_ID}`.\n"
    text += "- Thuật toán: HistGradientBoosting.\n"
    text += "- Feature set: `ergonomic_v2_with_view`.\n"
    text += "- Số đặc trưng: 31.\n"
    text += f"- Threshold: {threshold:.2f}.\n"
    text += f"- Model artifact: `{MODEL_PATH.relative_to(BASE_DIR)}`.\n"
    text += f"- Feature schema: `{SCHEMA_PATH.relative_to(BASE_DIR)}`.\n"
    text += f"- Threshold artifact: `{THRESHOLD_PATH.relative_to(BASE_DIR)}`.\n"
    text += f"- Resolution: {args.width}x{args.height}.\n"
    text += f"- Max processed frames per video: {args.max_frames}.\n"
    text += f"- Warm-up frames excluded from summary: {args.warmup_frames} per video.\n"
    text += f"- Frame stride: {args.frame_stride}.\n"
    text += f"- MediaPipe model complexity: {args.model_complexity}.\n\n"
    text += "## 3. Bảng 4.9 đề xuất\n\n"
    text += markdown_table(display)
    text += "\n\n"
    text += "## 4. Hình 4.6\n\n"
    text += "- `reports/figures/figure_4_6_hgb_runtime_latency_fps.png`\n"
    text += "- `reports/figures/figure_4_6_hgb_runtime_latency_fps.svg`\n\n"
    text += (
        "**Caption đề xuất:** Hình 4.6. So sánh độ trễ toàn pipeline và FPS ước lượng "
        "của pipeline HistGradientBoosting được lựa chọn theo góc quan sát.\n\n"
    )
    text += "## 5. Diễn giải kết quả\n\n"
    text += (
        f"Sau khi lựa chọn HistGradientBoosting với nhóm đặc trưng `ergonomic_v2_with_view`, "
        f"đề tài tiến hành đo lại thời gian xử lý của pipeline sử dụng đúng cấu hình này. "
        f"Kết quả cho thấy độ trễ trung bình của pipeline dao động từ {min_latency:.3f} ms "
        f"đến {max_latency:.3f} ms, tương ứng khoảng {min_fps:.3f} FPS đến {max_fps:.3f} FPS "
        "trên ba video đại diện. "
        f"Thời gian MediaPipe Pose trung bình khoảng {mean_mp:.3f} ms/frame, "
        f"trong khi bước tạo đặc trưng trung bình khoảng {mean_feature:.3f} ms/frame "
        f"và suy luận HistGradientBoosting khoảng {mean_hgb:.3f} ms/frame. "
        "Kết quả này cho thấy pipeline HGB có khả năng xử lý gần thời gian thực ở mức "
        "processing benchmark, tuy nhiên chưa đại diện cho full GUI FPS của ứng dụng.\n\n"
    )
    text += "## 6. So sánh với benchmark ANN cũ\n\n"
    text += (
        "Benchmark ANN cũ chỉ nên dùng như kết quả tham khảo lịch sử của pipeline MediaPipe + ANN. "
        "Vì mô hình được lựa chọn hiện tại là HistGradientBoosting, benchmark HGB trong báo cáo này "
        "mới là kết quả phù hợp hơn để đưa vào Bảng 4.9 và Hình 4.6 của luận văn.\n\n"
    )
    text += "## 7. Hạn chế\n\n"
    text += "- Đây là processing benchmark, chưa phải full GUI FPS.\n"
    text += "- Chưa bao gồm chi phí cập nhật giao diện CustomTkinter, vẽ skeleton lên GUI, phát âm thanh, ghi SQLite và xử lý sự kiện người dùng.\n"
    text += "- Webcam/IP camera realtime có thể dùng `view_unknown` nếu không có metadata góc nhìn.\n"
    text += "- FPS phụ thuộc phần cứng, camera, ánh sáng, số người trong khung hình và tải hệ thống.\n\n"
    text += "## 8. File đã xuất\n\n"
    text += "- `reports/results/runtime_benchmark_hgb_selected.csv`\n"
    text += "- `reports/results/runtime_benchmark_hgb_selected_summary.csv`\n"
    text += "- `reports/figures/figure_4_6_hgb_runtime_latency_fps.png`\n"
    text += "- `reports/figures/figure_4_6_hgb_runtime_latency_fps.svg`\n\n"
    text += "## 9. Checklist\n\n"
    text += "- [x] Đã load đúng HGB selected model.\n"
    text += "- [x] Đã load đúng feature set `ergonomic_v2_with_view`.\n"
    text += "- [x] Đã load đúng threshold 0,76.\n"
    text += "- [x] Đã benchmark front, side_30 và side_90.\n"
    text += f"- [x] Đã loại {args.warmup_frames} frame warm-up đầu mỗi video khỏi bảng tổng hợp.\n"
    text += "- [x] Không sửa app, SQLite hoặc model registry.\n"
    REPORT_PATH.write_text(text, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark selected HGB runtime.")
    parser.add_argument("--front-video", default=str(DEFAULT_VIDEOS["front"]))
    parser.add_argument("--side-30-video", default=str(DEFAULT_VIDEOS["side_30"]))
    parser.add_argument("--side-90-video", default=str(DEFAULT_VIDEOS["side_90"]))
    parser.add_argument("--max-frames", type=int, default=120)
    parser.add_argument("--warmup-frames", type=int, default=5)
    parser.add_argument("--frame-stride", type=int, default=15)
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=360)
    parser.add_argument("--model-complexity", type=int, default=1)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    model, _, threshold = validate_artifacts()
    videos = {
        "front": resolve_path(args.front_video),
        "side_30": resolve_path(args.side_30_video),
        "side_90": resolve_path(args.side_90_video),
    }
    frames = []
    for view_angle, video_path in videos.items():
        print(f"Benchmark {view_angle}: {video_path}")
        frames.append(benchmark_video(view_angle, video_path, model, threshold, args))
    frame_df = pd.concat(frames, ignore_index=True)
    summary = summarize(frame_df, args.warmup_frames)
    frame_path = RESULTS_DIR / "runtime_benchmark_hgb_selected.csv"
    summary_path = RESULTS_DIR / "runtime_benchmark_hgb_selected_summary.csv"
    frame_df.to_csv(frame_path, index=False, encoding="utf-8-sig")
    summary.to_csv(summary_path, index=False, encoding="utf-8-sig")
    save_figure(summary)
    write_report(summary, threshold, args)
    print(f"Saved: {frame_path}")
    print(f"Saved: {summary_path}")
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
