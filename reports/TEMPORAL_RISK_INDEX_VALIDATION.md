# Temporal Risk Index Validation

Input predictions: `D:\posture_detection_app\reports\results\final_external_predictions.csv`

Window seconds: `5`

## Frame vs Temporal Smoothing

| method | accuracy | false_positive | false_negative |
| --- | --- | --- | --- |
| frame_level | 0.821554 | 607 | 206 |
| temporal_5s_mean | 0.831212 | 624 | 145 |

## Interpretation

Temporal smoothing is useful when the application should avoid flickering warnings. It can reduce isolated false alerts, but it may delay detection if the window is too long. Use this result as session-level risk support, not as medical validation.
