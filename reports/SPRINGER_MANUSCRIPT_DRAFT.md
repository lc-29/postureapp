# Springer Manuscript Draft

Ngay cap nhat: 2026-05-28

## Proposed title

A Webcam-Based Desktop System for Real-Time Working Posture Monitoring Using
Normalized Pose Landmarks, Interpretable Ergonomic Features, and Temporal Risk
Scoring

## Abstract draft

Prolonged computer work can lead to poor sitting posture, but many posture
monitoring systems require wearable sensors, pressure chairs, or controlled
hardware. This study presents a real-time desktop posture monitoring system
using webcam/video input, MediaPipe pose landmarks, calibrated machine-learning
classifiers, interpretable ergonomic indicators, and session-level temporal
risk analysis. A project-specific dataset containing 84 raw videos from five
participants and 10 corrected external videos was used for model development
and evaluation. A unified feature schema was implemented to compare raw
landmarks, body-normalized landmarks, ergonomic geometric indicators, and
combined feature sets. In the corrected external evaluation, the selected
HistGradientBoosting model using normalized landmarks achieved 96.50% accuracy
and 96.76% F1 for the incorrect-posture class at the calibrated threshold.
Leave-one-participant-out evaluation on the raw dataset achieved a mean
incorrect-class F1 of 90.67%. Temporal smoothing reduced false negatives from
24 to 8 on the corrected external set. The results indicate that normalized
pose landmarks and calibrated tabular classifiers can support a practical
webcam-based posture warning application. However, broader participant-
independent external validation and expert ergonomic annotation are still
needed before claiming robust real-world or clinical validity.

## Contributions

1. An end-to-end desktop application for real-time working posture monitoring
   using webcam/video input.
2. A unified feature schema comparing raw landmarks, normalized landmarks,
   ergonomic geometric indicators, and combined feature sets.
3. A calibrated model registry that selects the final model based on
   incorrect-class F1, recall, and MCC.
4. A final evaluation protocol including corrected external evaluation,
   video-wise analysis, participant-wise validation, threshold calibration,
   error taxonomy, feature importance, and temporal smoothing.
5. A session-level temporal risk direction for converting frame-level
   predictions into more stable warning behavior.

## Methods summary

The system captures frames from webcam, IP camera, or video files using OpenCV.
MediaPipe Pose extracts 33 body landmarks. The proposed feature schema generates
raw 99-dimensional landmarks, body-normalized 99-dimensional landmarks, 14
ergonomic geometric indicators, and combined feature sets. Candidate models
include Logistic Regression, SVM RBF, Random Forest, HistGradientBoosting, and
MLP. Models are trained on the raw training set and evaluated on the corrected
external set. Threshold calibration is performed by sweeping thresholds from
0.05 to 0.95. Temporal smoothing is evaluated using a five-second rolling
probability mean.

## Main results

| Result | Value |
|---|---:|
| Selected model | HistGradientBoosting + normalized_99 |
| Corrected external accuracy | 96.50% |
| Corrected external F1 incorrect | 96.76% |
| Corrected external recall incorrect | 97.30% |
| Corrected external MCC | 92.97% |
| Participant-wise mean F1 incorrect | 90.67% |
| Temporal smoothing false negatives | 8, down from 24 |

## Discussion points

- Normalized landmarks outperformed raw landmarks in the final registry,
  suggesting that body-scale normalization reduces camera/person-size bias.
- Ergonomic features remain valuable for interpretability and achieved strong
  performance with SVM RBF.
- The current app still needs integration with the model registry before the
  product behavior fully matches the best research model.
- The corrected external set is useful for preliminary validation but currently
  has limited participant diversity.

## Limitations

- External validation currently contains only P01.
- Dataset is project-specific and not a public benchmark.
- Labels are binary correct/incorrect and do not yet encode posture subtypes.
- No clinical or expert ergonomic validation has been performed.
- Final model integration into the Tkinter app is still a follow-up engineering
  task.

## Conclusion draft

This study demonstrates a practical webcam-based desktop posture monitoring
pipeline with calibrated machine-learning classification, interpretable
posture indicators, and temporal warning stabilization. The corrected external
and participant-wise results support the feasibility of the approach for a
desktop feedback application. Future work should expand participant-independent
external validation, add multi-class posture taxonomy, integrate the selected
model registry into the app, and compare system outputs with expert ergonomic
assessment.

