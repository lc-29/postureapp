# Claim Boundary And Limitations

Ngay cap nhat: 2026-05-28

## Claim nen dung

> This study presents a real-time webcam-based working posture monitoring system
> that combines MediaPipe pose landmarks, body-normalized landmark features,
> interpretable ergonomic indicators, calibrated machine-learning classifiers,
> and session-level temporal risk analysis.

> In the corrected project-specific external evaluation, the selected
> HistGradientBoosting model using normalized landmarks achieved 96.50% accuracy
> and 96.76% F1 for the incorrect-posture class at the calibrated threshold.

> Temporal smoothing reduced missed incorrect-posture frames in the corrected
> external set, supporting the use of session-level risk aggregation for a
> warning-oriented desktop application.

## Claim khong nen dung

```text
State-of-the-art posture recognition.
Clinically validated system.
Medical diagnosis.
New deep learning architecture.
New public benchmark dataset.
Guaranteed ergonomic correctness.
```

## Ly do khong nen claim qua muc

| Issue | Why it matters |
|---|---|
| External set currently has only P01 | Generalization to new participants is not fully proven. |
| Dataset is project-specific | Cannot compare directly as leaderboard against literature. |
| Labels are binary correct/incorrect | Does not yet separate posture error taxonomy. |
| No expert ergonomic validation | Cannot claim RULA/REBA-grade assessment. |
| Final model not yet integrated into app | Current app behavior may still use older ANN path. |

## Best positioning

Huong viet manh va an toan:

```text
Applied Research / Implementation-supported Applied AI System
```

Dong gop nen nhan manh:

1. End-to-end webcam desktop posture monitoring.
2. Unified feature schema comparing raw, normalized, ergonomic and combined features.
3. Calibrated model selection instead of using a default ANN blindly.
4. Video-wise, participant-wise and hard-case analysis.
5. Temporal/session-level risk support for a real warning application.

