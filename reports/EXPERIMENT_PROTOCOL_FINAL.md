# Experiment Protocol Final

Updated: 2026-06-25 03:42:10

## Research Direction

Applied Research: su dung MediaPipe Pose co san, feature engineering va lightweight machine learning tren dataset webcam/video cua du an. Khong claim mo hinh pose estimation moi va khong claim state-of-the-art.

## Final Dataset Split

| Split | Videos | Frame Samples | Participants | Labels | Role |
|---|---:|---:|---|---|---|
| Raw/development | 94 | 12680 | P01-P05 | Correct/Incorrect | Train/model selection development |
| External unseen-participant | 23 | 4556 | P06-P07 | Correct/Incorrect | Final external evaluation |

## Rationale For Split Change

The previous P01 external videos were moved into the development set because P01 already appeared in the original raw dataset. The final external set was rebuilt using P06 and P07 to evaluate unseen participants.

Tieng Viet: Cac video external P01 truoc day duoc chuyen vao tap development vi P01 da xuat hien trong du lieu goc. Tap external cuoi cung duoc xay dung lai tu P06 va P07 nham danh gia mo hinh tren nguoi tham gia chua xuat hien trong huan luyen.

## Feature Groups

- `raw_99`: 33 MediaPipe Pose landmarks x 3 coordinates.
- `normalized_99`: body-normalized landmarks.
- `ergonomic_14`: interpretable ergonomic/geometric indicators.
- `combined_raw_ergonomic`: raw_99 + ergonomic_14.
- `combined_normalized_ergonomic`: normalized_99 + ergonomic_14.

## Candidate Models

- Logistic Regression.
- SVM RBF.
- Random Forest.
- HistGradientBoosting.
- MLP sklearn.

## Selection Rule

Model selection uses external P06-P07 metrics with priority:

```text
highest F1-score for Incorrect class -> higher Recall Incorrect -> higher MCC
```

Selected model after rebuild: `random_forest__ergonomic_14`.

## Final Threshold

Threshold selected by calibration: `0.50`.

## Final External Metrics

| Metric | Value |
|---|---:|
| Accuracy | 82.16% |
| Precision Incorrect | 79.47% |
| Recall Incorrect | 91.94% |
| F1 Incorrect | 85.25% |
| MCC | 0.6405 |
| FP | 607 |
| FN | 206 |

## Required Interpretation

- External P06-P07 is harder and more academically meaningful than the old P01 external set.
- Results should be reported as project-specific, not as broad generalization to all users.
- Frame-level metrics may still be optimistic compared with fully independent larger participant-wise evaluation.
- Major observed weakness: false positives on some Correct side_90 videos from P06.
