# Participant-wise Evaluation

Dataset: `D:\posture_detection_app\dataset\processed\posture_data_2fps_combined_features.csv`

Feature set: `combined`

Participants: P01, P02, P03, P04, P05

## Summary By Algorithm

| algorithm | feature_set | mean_accuracy | std_accuracy | mean_f1_incorrect | std_f1_incorrect | mean_pr_auc |
| --- | --- | --- | --- | --- | --- | --- |
| SVM RBF | combined | 0.862564 | 0.013634 | 0.883745 | 0.006408 | 0.934909 |
| Logistic Regression | combined | 0.847676 | 0.057139 | 0.867606 | 0.054827 | 0.886020 |
| HistGradientBoosting | combined | 0.784661 | 0.065257 | 0.833556 | 0.041700 | 0.862499 |
| Random Forest | combined | 0.778581 | 0.035648 | 0.832089 | 0.033147 | 0.828992 |
| KNN | combined | 0.802897 | 0.056980 | 0.828242 | 0.055412 | 0.846391 |

## Notes

This is a stricter protocol than frame-wise random evaluation because each fold tests on a participant unseen during training.
