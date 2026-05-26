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

## Interpretation

The local frame-wise result is very high. This should be reported with caution because adjacent frames from the same source video can be visually similar. A video-wise or person-wise split is needed to estimate generalization more rigorously.

## Pending result tables

- External metrics.
- Threshold sweep.
- Full ablation study with repeat runs.
