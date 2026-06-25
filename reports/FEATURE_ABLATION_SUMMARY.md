# Feature Ablation Summary

Train: `D:\posture_detection_app\dataset\processed\posture_data_2fps_combined_features.csv`

External: `D:\posture_detection_app\dataset\processed\posture_external_test_2fps_combined_features.csv`

Model: `SVM RBF`

| feature_subset | algorithm | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | macro_f1 | mcc | roc_auc | pr_auc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ergonomic | SVM RBF | 0.948733 | 0.975207 | 0.928090 | 0.951065 | 0.948617 | 0.898516 | 0.977150 | 0.983259 |
| combined_without_hand | SVM RBF | 0.945115 | 0.977300 | 0.919101 | 0.947307 | 0.945019 | 0.891979 | 0.981094 | 0.986610 |
| combined_without_neck | SVM RBF | 0.936068 | 0.975728 | 0.903371 | 0.938156 | 0.935995 | 0.874967 | 0.982396 | 0.986665 |
| combined | SVM RBF | 0.934861 | 0.976829 | 0.900000 | 0.936842 | 0.934797 | 0.872939 | 0.980941 | 0.985898 |
| raw | SVM RBF | 0.911942 | 0.940758 | 0.892135 | 0.915802 | 0.911757 | 0.824924 | 0.974585 | 0.979465 |

## Interpretation Guide

- If `combined` is better than `raw`, ergonomic features improve the model.
- If `combined_without_neck` drops, neck-compression features are useful.
- If `combined_without_hand` drops, hand/chin-rest features are useful.
