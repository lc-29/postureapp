"""Manual MediaPipe Pose webcam test.

File nay khong mo webcam khi pytest import. Chay thu cong:

    python tests/test_mediapipe_pose.py
"""

import cv2
import mediapipe as mp


def manual_mediapipe_pose_check(source=0):
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("Khong mo duoc webcam/video.")
        return False

    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as pose:
        print("MediaPipe Pose da san sang. Nhan Q de thoat.")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Khong doc duoc frame.")
                break

            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                )

            cv2.imshow("Test MediaPipe Pose", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()
    return True


if __name__ == "__main__":
    raise SystemExit(0 if manual_mediapipe_pose_check() else 1)
