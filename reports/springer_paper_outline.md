# Springer Paper Outline

## Title

Real-Time Workplace Posture Monitoring Using MediaPipe Pose Landmarks and an ANN Classifier

## Abstract

Placeholder: problem, method, dataset, main local/external metrics, real-time desktop application, limitations.

## Keywords

Posture detection; MediaPipe Pose; computer vision; artificial neural network; ergonomic feedback; real-time monitoring.

## 1. Introduction

- Motivation: prolonged poor sitting posture and ergonomic risk.
- Gap: accessible webcam-based posture feedback.
- Contribution: end-to-end desktop app, ANN classifier, rule-based baseline, SQLite logging.

## 2. Related Work

- Pose estimation methods.
- Ergonomic posture assessment.
- Machine learning for posture classification.
- Real-time feedback systems.

## 3. Materials and Methods

- Data acquisition.
- Feature extraction.
- ANN classifier.
- Rule-based baseline.
- Realtime warning and logging.

## 4. Experiments

- Frame-wise split.
- External test.
- Threshold sweep.
- Planned video-wise/person-wise split.

## 5. Results

- Local metrics.
- External metrics.
- Confusion matrices.
- Baseline vs ANN.

## 6. Discussion

- Practical usability.
- Model behavior and threshold tradeoffs.
- Data leakage risk and generalization.

## 7. Limitations

- Dataset size and diversity.
- Frame-wise split.
- No clinical/medical claim.
- Lighting, camera angle, occlusion.

## 8. Conclusion

Placeholder.

## Declarations

- Funding: placeholder.
- Conflicts of interest: placeholder.
- Ethics approval/consent: placeholder.
- Data availability: raw videos not stored in Git; availability placeholder.

## References

Use `reports/RELATED_WORK_TODO.md` to collect real citations. Do not invent citations.
# Springer Paper Outline Update

Ngay cap nhat: 2026-05-27

## Recommended contribution statement

This work presents a webcam-based posture monitoring system that combines MediaPipe pose landmarks, frame-level ANN classification, interpretable ergonomic rule indicators, realtime warning logic, SQLite session logging, and a Temporal Posture Risk Index for session-level posture risk summarization.

## Recommended paper flow

1. Introduction: workplace posture problem, low-cost webcam motivation, limitations of sensor-heavy systems.
2. Related Work: camera/MediaPipe, RGB-D, pressure sensors, wearable sensors, ergonomic rules such as RULA.
3. Materials and Methods: dataset, feature extraction, ANN, rule-based baseline, TPRI, app workflow.
4. Experimental Protocol: train/external split, metrics, threshold sweep, statistical tests, benchmark models.
5. Results: external metrics, baseline comparison, threshold behavior, error analysis, runtime.
6. Discussion: why the system is practical, why it is not state-of-the-art yet, how TPRI adds session-level value.
7. Limitations: small dataset, frame-level validation, missing public benchmark, no clinical/ergonomic certification.
8. Conclusion and Future Work: video/person-wise validation, richer features, temporal models, user study.

## Strong but safe claim

The project contributes an integrated applied AI posture-monitoring pipeline with interpretable alerts and session-level risk reporting. The ANN significantly improves over the local rule-based baseline on the current external frame-level set, but further metadata-rich video/person-wise validation is required before broader generalization claims.
