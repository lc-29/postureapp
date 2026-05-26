# Posture Detection App

Đề tài: Xây dựng ứng dụng phát hiện lỗi tư thế làm việc qua webcam sử dụng Computer Vision.

## Pipeline

OpenCV → MediaPipe Pose → Landmark Extraction → Feature Engineering → Dataset CSV → Rule-based Baseline → ANN Training → Model Evaluation → Tkinter GUI → Realtime Warning → SQLite Logging/Statistics
