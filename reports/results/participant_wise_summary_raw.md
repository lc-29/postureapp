# Participant-wise Evaluation

Dataset: `D:\posture_detection_app\dataset\processed\posture_data_2fps_with_metadata.csv`

Feature set: `raw`

Participants: P01, P02, P03, P04, P05

## Summary By Algorithm

| algorithm | feature_set | mean_accuracy | std_accuracy | mean_f1_incorrect | std_f1_incorrect | mean_pr_auc |
| --- | --- | --- | --- | --- | --- | --- |
| SVM RBF | raw | 0.803447 | 0.070829 | 0.844110 | 0.039870 | 0.868951 |
| Random Forest | raw | 0.711508 | 0.044856 | 0.788309 | 0.023458 | 0.808299 |
| HistGradientBoosting | raw | 0.714011 | 0.052590 | 0.784560 | 0.037793 | 0.801074 |
| KNN | raw | 0.737902 | 0.106610 | 0.768842 | 0.094145 | 0.806793 |
| Logistic Regression | raw | 0.710063 | 0.061608 | 0.733457 | 0.113411 | 0.826789 |

## Notes

This is a stricter protocol than frame-wise random evaluation because each fold tests on a participant unseen during training.
