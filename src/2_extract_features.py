"""
Trich xuat landmark MediaPipe Pose tu video thanh CSV de train ANN.

Input:
- dataset/raw_videos/correct/
- dataset/raw_videos/incorrect/

Output mac dinh:
- dataset/posture_data_2fps.csv

Moi mau CSV gom 99 dac trung:
33 landmark * (x, y, z), kem cot label o cuoi.

Label:
- correct = 0
- incorrect = 1
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any

# Giam bot log tu TensorFlow/MediaPipe tren terminal khi chay trich xuat.
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import cv2
import mediapipe as mp
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_ROOT = BASE_DIR / "dataset" / "raw_videos"
OUTPUT_CSV = BASE_DIR / "dataset" / "posture_data_2fps.csv"

VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".m4v"}
NUM_POSE_LANDMARKS = 33
FEATURES_PER_LANDMARK = 3
NUM_FEATURES = NUM_POSE_LANDMARKS * FEATURES_PER_LANDMARK

mp_pose = mp.solutions.pose


def get_video_files(folder: Path) -> list[Path]:
    """
    Lay danh sach video trong folder va sap xep theo ten file.

    Chi lay cac file co phan mo rong nam trong VIDEO_EXTENSIONS.
    """
    if not folder.exists():
        print(f"CANH BAO: Thu muc khong ton tai: {folder}")
        return []

    if not folder.is_dir():
        print(f"CANH BAO: Duong dan khong phai thu muc: {folder}")
        return []

    video_files = [
        path
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in VIDEO_EXTENSIONS
    ]
    return sorted(video_files, key=lambda path: path.name.lower())


def generate_feature_columns() -> list[str]:
    """
    Tao danh sach cot CSV: 99 feature landmark + cot label.

    Dinh dang:
    landmark_0_x, landmark_0_y, landmark_0_z, ..., landmark_32_z, label
    """
    columns: list[str] = []
    for landmark_index in range(NUM_POSE_LANDMARKS):
        columns.extend(
            [
                f"landmark_{landmark_index}_x",
                f"landmark_{landmark_index}_y",
                f"landmark_{landmark_index}_z",
            ]
        )

    columns.append("label")
    return columns


def extract_landmark_vector(pose_landmarks: Any) -> list[float] | None:
    """
    Chuyen MediaPipe pose_landmarks thanh vector 99 gia tri float.

    Chi lay x, y, z. Khong lay visibility de CSV chinh dung 99 dac trung.
    Neu landmark bi thieu hoac khong du 33 diem thi tra ve None.
    """
    if pose_landmarks is None:
        return None

    landmarks = getattr(pose_landmarks, "landmark", None)
    if landmarks is None or len(landmarks) < NUM_POSE_LANDMARKS:
        return None

    feature_vector: list[float] = []
    for landmark in landmarks[:NUM_POSE_LANDMARKS]:
        feature_vector.extend(
            [
                float(landmark.x),
                float(landmark.y),
                float(landmark.z),
            ]
        )

    if len(feature_vector) != NUM_FEATURES:
        return None

    return feature_vector


def create_empty_stats(label: int, video_path: Path) -> dict[str, int | float | str]:
    """Tao dict thong ke mac dinh cho mot video."""
    return {
        "video": video_path.name,
        "label": label,
        "total_read_frames": 0,
        "sampled_frames": 0,
        "valid_frames": 0,
        "skipped_frames": 0,
        "video_fps": 0.0,
    }


def process_video(
    video_path: Path,
    label: int,
    pose: Any,
    sample_fps: float = 2.0,
) -> tuple[list[list[float]], dict[str, int | float | str]]:
    """
    Xu ly mot video va tra ve cac row CSV cung thong ke.

    Moi video duoc lay mau theo sample_fps. Mac dinh sample_fps=2.0 nghia la
    lay khoang 2 frame moi giay de giam lap du lieu qua nhieu.
    """
    rows: list[list[float]] = []
    stats = create_empty_stats(label, video_path)

    if sample_fps <= 0:
        print("CANH BAO: sample_fps <= 0, tu dong dung 1.0 FPS.")
        sample_fps = 1.0

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"CANH BAO: Khong mo duoc video: {video_path}")
        return rows, stats

    try:
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        if video_fps is None or video_fps <= 0:
            video_fps = 30.0

        frame_interval = max(int(video_fps / sample_fps), 1)
        stats["video_fps"] = float(video_fps)

        print(
            f"Dang xu ly: {video_path.name} | label={label} | "
            f"fps={video_fps:.2f} | lay {sample_fps:g} frame/giay"
        )

        frame_index = 0
        while True:
            success, frame = cap.read()
            if not success or frame is None:
                break

            stats["total_read_frames"] = int(stats["total_read_frames"]) + 1

            if frame_index % frame_interval != 0:
                frame_index += 1
                continue

            stats["sampled_frames"] = int(stats["sampled_frames"]) + 1

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb_frame.flags.writeable = False
            results = pose.process(rgb_frame)
            rgb_frame.flags.writeable = True

            if results.pose_landmarks:
                vector = extract_landmark_vector(results.pose_landmarks)
                if vector is not None:
                    rows.append(vector + [label])
                    stats["valid_frames"] = int(stats["valid_frames"]) + 1
                else:
                    stats["skipped_frames"] = int(stats["skipped_frames"]) + 1
            else:
                stats["skipped_frames"] = int(stats["skipped_frames"]) + 1

            frame_index += 1

    except Exception as exc:
        print(f"CANH BAO: Loi khi xu ly video {video_path.name}: {exc}")
    finally:
        cap.release()

    print(
        "Ket qua: "
        f"sampled={stats['sampled_frames']}, "
        f"valid={stats['valid_frames']}, "
        f"skipped={stats['skipped_frames']}"
    )

    return rows, stats


def add_stats(total: dict[str, int], stats: dict[str, int | float | str]) -> None:
    """Cong don thong ke cua mot video vao thong ke theo nhan."""
    total["total_read_frames"] += int(stats["total_read_frames"])
    total["sampled_frames"] += int(stats["sampled_frames"])
    total["valid_frames"] += int(stats["valid_frames"])
    total["skipped_frames"] += int(stats["skipped_frames"])


def print_final_statistics(
    correct_video_count: int,
    incorrect_video_count: int,
    correct_stats: dict[str, int],
    incorrect_stats: dict[str, int],
    total_rows: int,
    label_counts: dict[int, int],
    output_csv: Path,
) -> None:
    """In thong ke cuoi cung sau khi trich xuat va luu CSV."""
    print("\n================= THONG KE TRICH XUAT =================")
    print(f"Tong video correct: {correct_video_count}")
    print(f"Tong video incorrect: {incorrect_video_count}")

    print(f"\nTong frame da doc correct: {correct_stats['total_read_frames']}")
    print(f"Tong frame da doc incorrect: {incorrect_stats['total_read_frames']}")

    print(f"\nTong frame duoc lay mau correct: {correct_stats['sampled_frames']}")
    print(f"Tong frame duoc lay mau incorrect: {incorrect_stats['sampled_frames']}")

    print(f"\nTong frame hop le correct: {correct_stats['valid_frames']}")
    print(f"Tong frame hop le incorrect: {incorrect_stats['valid_frames']}")

    print(f"\nTong frame bi bo qua correct: {correct_stats['skipped_frames']}")
    print(f"Tong frame bi bo qua incorrect: {incorrect_stats['skipped_frames']}")

    print(f"\nTong mau CSV: {total_rows}")
    print(f"So dac trung moi mau: {NUM_FEATURES}")
    print(f"So cot CSV: {NUM_FEATURES + 1}")
    print("Phan bo label:")
    print(f"  label 0 - correct: {label_counts.get(0, 0)}")
    print(f"  label 1 - incorrect: {label_counts.get(1, 0)}")

    print(f"\nDuong dan file CSV: {output_csv}")
    print("========================================================")


def resolve_input_root(input_root: str | Path | None) -> Path:
    """
    Chuan hoa thu muc goc chua 2 folder correct va incorrect.

    Neu input_root=None thi dung dataset/raw_videos. Neu la duong dan tuong doi
    thi tinh theo BASE_DIR de co the chay script tu bat ky working directory nao.
    """
    if input_root is None:
        return DEFAULT_INPUT_ROOT

    root = Path(input_root)
    if not root.is_absolute():
        root = BASE_DIR / root

    return root


def process_dataset(
    input_root: str | Path | None = None,
    sample_fps: float = 2.0,
    output_csv: Path = OUTPUT_CSV,
) -> None:
    """
    Xu ly toan bo dataset correct/incorrect va luu CSV.

    CSV chinh chi gom 99 feature + label de train ANN don gian. Chua them
    source_video/frame_index trong buoc nay.
    """
    output_csv = Path(output_csv)
    if not output_csv.is_absolute():
        output_csv = BASE_DIR / output_csv

    input_root_path = resolve_input_root(input_root)
    correct_dir = input_root_path / "correct"
    incorrect_dir = input_root_path / "incorrect"

    correct_videos = get_video_files(correct_dir)
    incorrect_videos = get_video_files(incorrect_dir)

    print("========== BAT DAU TRICH XUAT LANDMARK ==========")
    print(f"Input root: {input_root_path}")
    print(f"Correct dir: {correct_dir}")
    print(f"Incorrect dir: {incorrect_dir}")
    print(f"Tim thay video correct: {len(correct_videos)}")
    print(f"Tim thay video incorrect: {len(incorrect_videos)}")
    print(f"Sample FPS: {sample_fps:g}")
    print(f"Output CSV: {output_csv}")
    print("==================================================\n")

    if not correct_videos and not incorrect_videos:
        print("ERROR: Khong tim thay video nao trong correct/incorrect.")
        print(f"Hay kiem tra thu muc {correct_dir} va {incorrect_dir}.")
        return

    all_rows: list[list[float]] = []
    correct_stats = {
        "total_read_frames": 0,
        "sampled_frames": 0,
        "valid_frames": 0,
        "skipped_frames": 0,
    }
    incorrect_stats = {
        "total_read_frames": 0,
        "sampled_frames": 0,
        "valid_frames": 0,
        "skipped_frames": 0,
    }

    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as pose:
        for video_path in correct_videos:
            rows, stats = process_video(video_path, label=0, pose=pose, sample_fps=sample_fps)
            all_rows.extend(rows)
            add_stats(correct_stats, stats)

        for video_path in incorrect_videos:
            rows, stats = process_video(video_path, label=1, pose=pose, sample_fps=sample_fps)
            all_rows.extend(rows)
            add_stats(incorrect_stats, stats)

    if not all_rows:
        print(
            "ERROR: Khong co mau hop le nao duoc trich xuat. "
            "Hay kiem tra video, anh sang, goc quay, MediaPipe Pose."
        )
        return

    columns = generate_feature_columns()
    df = pd.DataFrame(all_rows, columns=columns)

    if len(df.columns) != NUM_FEATURES + 1 or df.columns[-1] != "label":
        print("ERROR: Cau truc CSV khong dung 99 dac trung + label.")
        return

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")

    label_counts = {
        0: int((df["label"] == 0).sum()),
        1: int((df["label"] == 1).sum()),
    }

    print_final_statistics(
        correct_video_count=len(correct_videos),
        incorrect_video_count=len(incorrect_videos),
        correct_stats=correct_stats,
        incorrect_stats=incorrect_stats,
        total_rows=len(df),
        label_counts=label_counts,
        output_csv=output_csv,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Trich xuat 33 landmark MediaPipe Pose tu video thanh CSV "
            "de phuc vu train ANN."
        )
    )
    parser.add_argument(
        "--input-root",
        type=str,
        default=None,
        help=(
            "Thu muc goc chua 2 folder correct va incorrect. "
            "Mac dinh la dataset/raw_videos."
        ),
    )
    parser.add_argument(
        "--sample-fps",
        type=float,
        default=2.0,
        help="So frame lay mau moi giay. Mac dinh 2 FPS.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(OUTPUT_CSV),
        help="Duong dan file CSV dau ra.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        process_dataset(
            input_root=args.input_root,
            sample_fps=args.sample_fps,
            output_csv=Path(args.output),
        )
    except KeyboardInterrupt:
        print("\nDa dung chuong trinh theo yeu cau nguoi dung.")
        sys.exit(130)
    except Exception as exc:
        print(f"ERROR: Loi khong mong muon khi trich xuat du lieu: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
