# Results Draft

## Local frame-wise ANN result

Source: `models/local_training/metrics.txt`

| Metric | Value |
|---|---:|
| Dataset rows | 11022 |
| Train shape | 7714 x 99 |
| Validation shape | 1654 x 99 |
| Test shape | 1654 x 99 |
| Accuracy | 0.998186 |
| Precision (incorrect) | 0.998987 |
| Recall (incorrect) | 0.997976 |
| F1-score (incorrect) | 0.998481 |

Confusion matrix `[[TN, FP], [FN, TP]]`:

```text
[[665   1]
 [  2 986]]
```

## External result

Source: `reports/results/external_metrics.txt`

| Metric | Value |
|---|---:|
| Dataset rows | 1658 |
| Accuracy | 0.901689 |
| Precision (incorrect) | 0.956085 |
| Recall (incorrect) | 0.856180 |
| F1-score (incorrect) | 0.903379 |

Confusion matrix `[[TN, FP], [FN, TP]]`:

```text
[[733  35]
 [128 762]]
```

Best threshold by F1 in sweep: `0.10`, with F1 `0.918888`.

## Baseline comparison

Source: `reports/results/algorithm_comparison.csv`

| Algorithm | Dataset | Accuracy | Precision | Recall | F1 |
|---|---|---:|---:|---:|---:|
| ANN | posture_external_test_2fps_with_metadata.csv | 0.901689 | 0.956085 | 0.856180 | 0.903379 |
| Rule-based | posture_external_test_2fps_with_metadata.csv | 0.674910 | 0.634896 | 0.928090 | 0.753994 |

## Statistical analysis

Source: `reports/results/statistical_analysis.txt`

Accuracy with Wilson 95% confidence interval:

| Algorithm | Accuracy | 95% CI |
|---|---:|---:|
| ANN | 0.901689 | [0.886415, 0.915105] |
| Rule-based | 0.674910 | [0.651981, 0.697029] |

McNemar paired test on sample-level correctness:

```text
[[1006  489]
 [ 113   50]]
```

P-value: `1.15022e-56`.

This indicates a statistically significant difference between ANN and rule-based correctness on the same external frames. This result is still frame-level and must not be treated as a substitute for video-wise/person-wise validation.

## Temporal Posture Risk Index

Source: local run of `python src/12_temporal_risk_index.py`

The current local SQLite database contains 50 demo sessions. The generated TPRI distribution was:

| Risk level | Session count |
|---|---:|
| LOW | 19 |
| MEDIUM | 25 |
| HIGH | 6 |
| CRITICAL | 0 |

The highest observed session-level score was `61.053` (HIGH). These values summarize local application logs and should be reported separately from model classification metrics. The generated CSV outputs are intentionally not committed because they derive from local session logs.

## Interpretation

The local frame-wise result is very high. This should be reported with caution because adjacent frames from the same source video can be visually similar. A video-wise or person-wise split is needed to estimate generalization more rigorously.

## Literature comparison context

Source: `reports/LITERATURE_METRICS_COMPARISON.md`

The current external ANN result should be framed as a low-cost webcam/MediaPipe baseline with external-set testing, statistical comparison against a rule-based baseline, and Temporal Posture Risk Index support. It should not be framed as state-of-the-art because related studies report higher values under different modalities and protocols, including pressure-sensor systems above 98%, RGB-D hierarchical models around 91.47% for base sitting posture grouping, and MediaPipe/camera studies around 85.18%-92.07% or higher depending on view and protocol.

## Pending result tables

- External metrics.
- Threshold sweep.
- Full ablation study with repeat runs.
- Video-wise/person-wise evaluation.
- Runtime benchmark.
- Literature comparison table.
# Results Draft Update

Ngay cap nhat: 2026-05-28

## Current external result

The current ANN model was evaluated on `dataset/processed/posture_external_test_2fps_with_metadata.csv`, which contains 1658 external frames after replacing the mislabeled-content video `P01_incorrect_004.mp4` with a true incorrect-posture video. At threshold 0.50, the ANN reached 90.169% accuracy, 95.609% precision for the incorrect class, 85.618% recall for the incorrect class, and 90.338% F1 for the incorrect class. The confusion matrix was `[[733, 35], [128, 762]]`.

The best F1 threshold in the sweep was 0.10, reaching 91.375% accuracy and 91.889% F1 for the incorrect class. This suggests that a lower alert threshold may still be useful for an assistive warning system if recall is prioritized.

## Baseline comparison

The ANN outperformed the local rule-based ergonomic baseline on the same corrected external frame-level set. The baseline reached 67.491% accuracy and 75.399% F1 for the incorrect class. McNemar's paired test gave p-value `1.15022e-56`, indicating a statistically significant difference on the paired frame predictions.

## Interpretation

The main remaining weakness is false negatives: at threshold 0.50, 128 incorrect frames were classified as correct. This is important for a posture-warning app because missed incorrect posture can reduce user benefit. The preferred fix is not only lowering threshold, but combining threshold tuning with temporal smoothing and normalized/ergonomic features.

## Claim boundary

These results support the statement that the ANN is better than the local rule-based baseline under the corrected current frame-level protocol. They do not support a state-of-the-art claim against external literature because those studies use different sensors, datasets, labels, and split protocols.
