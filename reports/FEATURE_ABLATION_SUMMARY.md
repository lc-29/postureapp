# Feature Ablation Summary

Train: `D:\posture_detection_app\dataset\processed\posture_data_2fps_combined_features.csv`

External: `D:\posture_detection_app\dataset\processed\posture_external_test_2fps_combined_features.csv`

Model: `SVM RBF`

| feature_subset | algorithm | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | macro_f1 | mcc | roc_auc | pr_auc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| combined_without_hand | SVM RBF | 0.834414 | 0.972303 | 0.717976 | 0.826006 | 0.834026 | 0.703125 | 0.900281 | 0.933708 |
| ergonomic | SVM RBF | 0.826753 | 0.968981 | 0.706136 | 0.816936 | 0.826253 | 0.689971 | 0.871545 | 0.918690 |
| combined | SVM RBF | 0.823807 | 0.971557 | 0.698601 | 0.812774 | 0.823193 | 0.686535 | 0.896830 | 0.930726 |
| combined_without_neck | SVM RBF | 0.823217 | 0.970105 | 0.698601 | 0.812265 | 0.822614 | 0.685029 | 0.900785 | 0.932521 |
| raw | SVM RBF | 0.799057 | 0.927326 | 0.686760 | 0.789116 | 0.798610 | 0.630229 | 0.919625 | 0.938245 |

## Interpretation Guide

- If `combined` is better than `raw`, ergonomic features improve the model.
- If `combined_without_neck` drops, neck-compression features are useful.
- If `combined_without_hand` drops, hand/chin-rest features are useful.
