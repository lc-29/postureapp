import argparse
import os
import sys

import cv2


def _resolve_source(source):
    if source is None:
        return 0, "Webcam (0)"

    if isinstance(source, int):
        return source, f"Webcam ({source})"

    source_str = str(source).strip()

    if source_str.isdigit():
        idx = int(source_str)
        return idx, f"Webcam ({idx})"

    lower = source_str.lower()
    if lower.startswith(("rtsp://", "http://", "https://")):
        return source_str, "IP Camera"

    if os.path.isfile(source_str):
        return source_str, "Video File"

    if "://" in source_str:
        return source_str, "IP Camera"

    return source_str, "Video File"


def test_camera(source=0):
    source_value, source_label = _resolve_source(source)
    cap = cv2.VideoCapture(source_value)

    if not cap.isOpened():
        print("Không mở được nguồn video.")
        return False

    print(f"Mở nguồn video thành công: {source_label}. Nhấn Q để thoát.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Không đọc được frame.")
            break

        cv2.imshow(f"Test {source_label}", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Test webcam (0), IP camera (rtsp/http), hoặc file video."
    )
    parser.add_argument(
        "--source",
        "-s",
        default="0",
        help="0 cho webcam, URL cho IP camera, hoặc duong dan file video.",
    )
    args = parser.parse_args()

    ok = test_camera(args.source)
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()