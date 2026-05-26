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
| Dataset rows | 1697 |
| Accuracy | 0.793164 |
| Precision (incorrect) | 0.945988 |
| Recall (incorrect) | 0.659849 |
| F1-score (incorrect) | 0.777425 |

Confusion matrix `[[TN, FP], [FN, TP]]`:

```text
[[733  35]
 [316 613]]
```

Best threshold by F1 in sweep: `0.10`, with F1 `0.799031`.

## Baseline comparison

Source: `reports/results/algorithm_comparison.csv`

| Algorithm | Dataset | Accuracy | Precision | Recall | F1 |
|---|---|---:|---:|---:|---:|
| ANN | posture_external_test_2fps.csv | 0.793164 | 0.945988 | 0.659849 | 0.777425 |
| Rule-based | posture_external_test_2fps.csv | 0.566293 | 0.584427 | 0.719053 | 0.644788 |

## Statistical analysis

Source: `reports/results/statistical_analysis.txt`

Accuracy with Wilson 95% confidence interval:

| Algorithm | Accuracy | 95% CI |
|---|---:|---:|
| ANN | 0.793164 | [0.773242, 0.811763] |
| Rule-based | 0.566293 | [0.542591, 0.589697] |

McNemar paired test on sample-level correctness:

```text
[[856 490]
 [105 246]]
```

P-value: `2.19314e-60`.

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

## Pending result tables

- External metrics.
- Threshold sweep.
- Full ablation study with repeat runs.
- Video-wise/person-wise evaluation.
- Runtime benchmark.
