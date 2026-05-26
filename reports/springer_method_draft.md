# Method Draft

The proposed system detects workplace posture from a live webcam, IP camera, or video file. Each frame is processed with OpenCV and MediaPipe Pose. When a pose is detected, the system extracts 33 body landmarks. For machine-learning inference, each landmark contributes normalized `x`, `y`, and `z` values, forming a 99-dimensional feature vector.

The ANN classifier is a binary model that predicts whether a frame represents a correct or incorrect posture. The current architecture uses dense layers with batch normalization and dropout, followed by a sigmoid output. A `StandardScaler` fitted on the training set is applied before inference. The desktop application loads `models/ann_best.keras` and `models/scaler.pkl`.

A rule-based baseline is also implemented for interpretability. It estimates geometric posture indicators such as shoulder height difference, shoulder tilt, torso lean, horizontal head offset, head lowering, and hand-to-mouth proximity. Thresholds are empirical and intended as a comparison baseline rather than a medical standard.

The real-time application maintains posture state over time. If incorrect posture persists beyond a configured duration, the app can trigger an audio warning. Sessions, frame counts, warning counts, and daily summaries are stored in SQLite. This logging layer supports later export for reports and demonstration.

The system is an assistive ergonomic reminder. It is not intended for medical diagnosis or clinical decision-making.
