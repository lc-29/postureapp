# Method Draft

The proposed system detects workplace posture from a live webcam, IP camera, or video file. Each frame is processed with OpenCV and MediaPipe Pose. When a pose is detected, the system extracts 33 body landmarks. For machine-learning inference, each landmark contributes normalized `x`, `y`, and `z` values, forming a 99-dimensional feature vector.

The ANN classifier is a binary model that predicts whether a frame represents a correct or incorrect posture. The current architecture uses dense layers with batch normalization and dropout, followed by a sigmoid output. A `StandardScaler` fitted on the training set is applied before inference. The desktop application loads `models/ann_best.keras` and `models/scaler.pkl`.

A rule-based baseline is also implemented for interpretability. It estimates geometric posture indicators such as shoulder height difference, shoulder tilt, torso lean, horizontal head offset, head lowering, and hand-to-mouth proximity. Thresholds are empirical and intended as a comparison baseline rather than a medical standard.

The real-time application maintains posture state over time. If incorrect posture persists beyond a configured duration, the app can trigger an audio warning. Sessions, frame counts, warning counts, and daily summaries are stored in SQLite. This logging layer supports later export for reports and demonstration.

To summarize session-level ergonomic behavior, the system computes a Temporal Posture Risk Index (TPRI). TPRI combines four normalized temporal components: incorrect posture duration ratio, long continuous incorrect-posture ratio, warning-rate ratio, and no-person/low-confidence ratio. The default score is:

```text
TPRI = 100 * (
  0.40 * incorrect_time_ratio
  + 0.25 * long_bad_posture_ratio
  + 0.20 * warning_rate_norm
  + 0.15 * no_person_or_low_confidence_ratio
)
```

The score is interpreted as LOW, MEDIUM, HIGH, or CRITICAL using fixed ranges. It is intended for comparing sessions inside this application and for reporting temporal behavior, not for clinical diagnosis.

The system is an assistive ergonomic reminder. It is not intended for medical diagnosis or clinical decision-making.

## Evaluation Protocol Update

The experimental workflow now includes:

- Frame-level external evaluation using `dataset/posture_external_test_2fps.csv`.
- Prediction-level export for false-positive/false-negative analysis.
- ROC, precision-recall, and calibration curves for threshold inspection.
- Video-level grouping when a metadata CSV contains `source_video` and `frame_index`.
- Classical machine-learning benchmark models trained on the same landmark CSV and evaluated on the same external CSV.
- Runtime benchmarking on raw video to estimate MediaPipe + ANN latency.

The strongest current claim remains limited to external frame-level validation. Video-wise and person-wise validation are treated as required future work unless the metadata-rich extraction and held-out split protocol are completed for the full training set.
