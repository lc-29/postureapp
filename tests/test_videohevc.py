from pathlib import Path

import cv2
import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VIDEO_PATH = PROJECT_ROOT / "dataset" / "raw_videos" / "20260514_202203.mp4"


def check_hevc_video(video_path=VIDEO_PATH):
    video_path = Path(video_path)

    if not video_path.is_file():
        print(f"Khong tim thay video: {video_path}")
        return False

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        print("Khong mo duoc video HEVC. Nen convert sang H.264.")
        cap.release()
        return False

    print("Mo video thanh cong.")
    print("Video:", video_path)
    print("FPS:", cap.get(cv2.CAP_PROP_FPS))
    print("Width:", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    print("Height:", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("Frame count:", cap.get(cv2.CAP_PROP_FRAME_COUNT))

    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        print("Mo duoc video nhung khong tach/decode duoc frame. Nen convert sang H.264.")
        return False

    print("Tach frame bang OpenCV thanh cong.")
    print("First frame shape:", frame.shape)
    return True


def test_video_hevc_can_be_decoded_by_opencv():
    if not VIDEO_PATH.is_file():
        pytest.skip(f"Manual HEVC sample does not exist: {VIDEO_PATH}")

    assert check_hevc_video()


if __name__ == "__main__":
    raise SystemExit(0 if check_hevc_video() else 1)
