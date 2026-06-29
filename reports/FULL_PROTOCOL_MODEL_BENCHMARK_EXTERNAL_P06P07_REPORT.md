# Full Protocol Model Benchmark on External P06-P07

Updated: 2026-06-25 23:33:12

## 1. Muc tieu

Bao cao nay chay lai benchmark day du tren cung protocol: cac mo hinh hoc may duoc train tren P01-P05 va danh gia tren external P06-P07. Rule-based Baseline khong train, chi danh gia truc tiep tren external.

## 2. Dataset split va leakage check

- Train/development: 12680 frame, 94 video, participants P01, P02, P03, P04, P05.
- External: 4556 frame, 23 video, participants P06, P07.
- Train label counts: {'0': 5206, '1': 7474}.
- External label counts: {'0': 2001, '1': 2555}.
- Source video overlap count: 0.
- Train only P01-P05: True.
- External only P06-P07: True.
- Participant disjoint: True.
- Source video disjoint: True.

## 3. Feature sets va thuat toan

- Feature sets: `raw_99`, `normalized_99`, `ergonomic_14`, `ergonomic_v2`, `ergonomic_v2_with_view`, `combined_v2`, `combined_v2_with_view`.
- ANN/Keras feature sets: `normalized_99`, `ergonomic_v2_with_view`.
- Algorithms: Logistic Regression, SVM RBF, KNN, Decision Tree, Random Forest, MLPClassifier, ANN/Keras, HistGradientBoosting, Rule-based Baseline.
- Threshold mac dinh cho bang chinh: 0.50 voi cac mo hinh co score/probability.
- Threshold sweep la phan tich external-calibrated, khong nen goi la blind external test.

## 4. Bang benchmark chinh theo threshold mac dinh 0.50

| model_id | algorithm_family | feature_set | class_weight | threshold | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | macro_f1 | mcc | roc_auc | pr_auc | false_positive | false_negative | train_seconds | predict_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hist_gradient_boosting_balanced_sample_weight__ergonomic_v2_with_view | HistGradientBoosting | ergonomic_v2_with_view | balanced_sample_weight | 0.50 | 87.34% | 86.71% | 91.43% | 89.01% | 87.04% | 0.7424 | 94.70% | 95.73% | 358 | 219 | 0.5250 | 0.0180 |
| hist_gradient_boosting_none__ergonomic_v2_with_view | HistGradientBoosting | ergonomic_v2_with_view | none | 0.50 | 86.46% | 85.89% | 90.76% | 88.26% | 86.13% | 0.7244 | 94.91% | 96.21% | 381 | 236 | 0.7212 | 0.0234 |
| hist_gradient_boosting_balanced_sample_weight__ergonomic_v2 | HistGradientBoosting | ergonomic_v2 | balanced_sample_weight | 0.50 | 85.25% | 84.10% | 90.88% | 87.36% | 84.83% | 0.7002 | 93.24% | 95.39% | 439 | 233 | 0.5123 | 0.0174 |
| hist_gradient_boosting_none__ergonomic_v2 | HistGradientBoosting | ergonomic_v2 | none | 0.50 | 84.66% | 82.75% | 91.78% | 87.03% | 84.13% | 0.6893 | 93.04% | 95.26% | 489 | 210 | 0.5780 | 0.0167 |
| logistic_regression_none__ergonomic_14 | Logistic Regression | ergonomic_14 | none | 0.50 | 86.24% | 94.10% | 80.51% | 86.77% | 86.22% | 0.7357 | 92.28% | 93.39% | 129 | 498 | 0.0268 | 0.0019 |
| random_forest_balanced__ergonomic_v2_with_view | Random Forest | ergonomic_v2_with_view | balanced | 0.50 | 83.87% | 84.89% | 86.65% | 85.76% | 83.58% | 0.6718 | 91.72% | 94.22% | 394 | 341 | 1.9714 | 0.0814 |
| random_forest_balanced__combined_v2 | Random Forest | combined_v2 | balanced | 0.50 | 83.65% | 85.21% | 85.71% | 85.46% | 83.39% | 0.6678 | 91.81% | 94.06% | 380 | 365 | 5.7803 | 0.0820 |
| random_forest_none__ergonomic_v2_with_view | Random Forest | ergonomic_v2_with_view | none | 0.50 | 82.51% | 83.99% | 85.01% | 84.50% | 82.21% | 0.6443 | 90.34% | 93.09% | 414 | 383 | 1.8935 | 0.0817 |
| random_forest_balanced__ergonomic_v2 | Random Forest | ergonomic_v2 | balanced | 0.50 | 82.44% | 86.40% | 81.53% | 83.89% | 82.30% | 0.6476 | 91.10% | 93.61% | 328 | 472 | 2.2389 | 0.0708 |
| logistic_regression_balanced__ergonomic_14 | Logistic Regression | ergonomic_14 | balanced | 0.50 | 83.54% | 94.74% | 74.79% | 83.60% | 83.54% | 0.6944 | 92.26% | 93.35% | 106 | 644 | 0.0320 | 0.0019 |
| random_forest_balanced__ergonomic_14 | Random Forest | ergonomic_14 | balanced | 0.50 | 79.46% | 76.99% | 90.37% | 83.15% | 78.42% | 0.5848 | 81.53% | 84.84% | 690 | 246 | 1.3252 | 0.0690 |
| hist_gradient_boosting_balanced_sample_weight__combined_v2 | HistGradientBoosting | combined_v2 | balanced_sample_weight | 0.50 | 78.27% | 75.88% | 89.78% | 82.25% | 77.12% | 0.5604 | 87.36% | 90.61% | 729 | 261 | 1.5931 | 0.0195 |
| hist_gradient_boosting_none__combined_v2 | HistGradientBoosting | combined_v2 | none | 0.50 | 77.30% | 74.10% | 91.51% | 81.89% | 75.75% | 0.5450 | 86.92% | 89.80% | 817 | 217 | 1.5953 | 0.0194 |
| hist_gradient_boosting_balanced_sample_weight__combined_v2_with_view | HistGradientBoosting | combined_v2_with_view | balanced_sample_weight | 0.50 | 77.66% | 76.06% | 87.79% | 81.50% | 76.64% | 0.5454 | 87.51% | 90.47% | 706 | 312 | 1.6232 | 0.0210 |
| random_forest_none__ergonomic_14 | Random Forest | ergonomic_14 | none | 0.50 | 77.90% | 76.89% | 86.61% | 81.47% | 77.05% | 0.5492 | 81.00% | 84.63% | 665 | 342 | 1.2852 | 0.0701 |
| hist_gradient_boosting_balanced_sample_weight__ergonomic_14 | HistGradientBoosting | ergonomic_14 | balanced_sample_weight | 0.50 | 78.71% | 82.23% | 79.14% | 80.65% | 78.49% | 0.5706 | 84.05% | 85.92% | 437 | 533 | 0.5746 | 0.0207 |
| hist_gradient_boosting_none__combined_v2_with_view | HistGradientBoosting | combined_v2_with_view | none | 0.50 | 75.00% | 72.39% | 89.59% | 80.08% | 73.26% | 0.4950 | 84.14% | 86.50% | 873 | 266 | 1.5364 | 0.0208 |
| random_forest_balanced__combined_v2_with_view | Random Forest | combined_v2_with_view | balanced | 0.50 | 76.47% | 77.58% | 81.64% | 79.56% | 75.92% | 0.5198 | 88.15% | 91.70% | 603 | 469 | 5.8311 | 0.0919 |
| random_forest_none__ergonomic_v2 | Random Forest | ergonomic_v2 | none | 0.50 | 78.23% | 84.23% | 75.26% | 79.50% | 78.14% | 0.5685 | 88.34% | 91.36% | 360 | 632 | 2.1025 | 0.0700 |
| random_forest_none__combined_v2 | Random Forest | combined_v2 | none | 0.50 | 77.35% | 81.88% | 76.56% | 79.13% | 77.18% | 0.5457 | 87.32% | 89.72% | 433 | 599 | 5.3768 | 0.0823 |
| random_forest_none__combined_v2_with_view | Random Forest | combined_v2_with_view | none | 0.50 | 76.03% | 78.52% | 78.83% | 78.67% | 75.66% | 0.5132 | 86.21% | 89.16% | 551 | 541 | 6.0188 | 0.0936 |
| random_forest_none__raw_99 | Random Forest | raw_99 | none | 0.50 | 69.71% | 65.15% | 98.86% | 78.54% | 63.53% | 0.4369 | 73.90% | 76.01% | 1351 | 29 | 4.5382 | 0.0617 |
| random_forest_balanced__raw_99 | Random Forest | raw_99 | balanced | 0.50 | 69.47% | 65.04% | 98.51% | 78.35% | 63.29% | 0.4288 | 76.47% | 77.69% | 1353 | 38 | 4.6832 | 0.0710 |
| svm_rbf_balanced__normalized_99 | SVM RBF | normalized_99 | balanced | 0.50 | 68.09% | 63.98% | 98.63% | 77.61% | 61.04% | 0.4020 | 79.15% | 83.61% | 1419 | 35 | 0.8934 | 0.4003 |
| svm_rbf_none__normalized_99 | SVM RBF | normalized_99 | none | 0.50 | 67.19% | 63.24% | 99.06% | 77.20% | 59.34% | 0.3879 | 79.21% | 83.74% | 1471 | 24 | 0.8144 | 0.3980 |

Bang tren la so sanh cong bang theo threshold mac dinh. Neu dua vao luan van, co the rut gon thanh top cau hinh dai dien cua tung thuat toan va dua bang day du vao phu luc.

## 5. Cau hinh tot nhat cua tung nhom thuat toan

| model_id | algorithm_family | feature_set | class_weight | threshold | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | macro_f1 | mcc | roc_auc | pr_auc | false_positive | false_negative | train_seconds | predict_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hist_gradient_boosting_balanced_sample_weight__ergonomic_v2_with_view | HistGradientBoosting | ergonomic_v2_with_view | balanced_sample_weight | 0.50 | 87.34% | 86.71% | 91.43% | 89.01% | 87.04% | 0.7424 | 94.70% | 95.73% | 358 | 219 | 0.5250 | 0.0180 |
| logistic_regression_none__ergonomic_14 | Logistic Regression | ergonomic_14 | none | 0.50 | 86.24% | 94.10% | 80.51% | 86.77% | 86.22% | 0.7357 | 92.28% | 93.39% | 129 | 498 | 0.0268 | 0.0019 |
| random_forest_balanced__ergonomic_v2_with_view | Random Forest | ergonomic_v2_with_view | balanced | 0.50 | 83.87% | 84.89% | 86.65% | 85.76% | 83.58% | 0.6718 | 91.72% | 94.22% | 394 | 341 | 1.9714 | 0.0814 |
| svm_rbf_balanced__normalized_99 | SVM RBF | normalized_99 | balanced | 0.50 | 68.09% | 63.98% | 98.63% | 77.61% | 61.04% | 0.4020 | 79.15% | 83.61% | 1419 | 35 | 0.8934 | 0.4003 |
| decision_tree_none__combined_v2_with_view | Decision Tree | combined_v2_with_view | none | 0.50 | 68.11% | 65.08% | 93.07% | 76.60% | 63.27% | 0.3650 | 68.43% | 72.01% | 1276 | 177 | 1.0403 | 0.0020 |
| knn_none__ergonomic_14 | KNN | ergonomic_14 | none | 0.50 | 73.64% | 79.67% | 71.15% | 75.17% | 73.54% | 0.4761 | 80.96% | 82.55% | 464 | 737 | 0.0191 | 0.1033 |
| ann_keras_balanced__normalized_99 | ANN/Keras | normalized_99 | balanced | 0.50 | 68.72% | 68.37% | 82.31% | 74.69% | 66.88% | 0.3570 | 79.17% | 84.72% | 973 | 452 | 33.3327 | 0.2623 |
| mlp_sklearn_none__raw_99 | MLPClassifier | raw_99 | none | 0.50 | 58.38% | 57.40% | 100.00% | 72.94% | 41.45% | 0.1736 | 57.39% | 60.44% | 1896 | 0 | 1.4273 | 0.0056 |
| rule_based_baseline | Rule-based Baseline | manual_ergonomic_rules | none | 0.50 | 56.08% | 56.08% | 100.00% | 71.86% | 35.93% | 0.0000 | 50.00% | 56.08% | 2001 | 0 | 0.0000 | 0.8607 |

Day la bang nen dua vao muc thuc nghiem cua luan van vi moi nhom thuat toan chi lay cau hinh tot nhat tren protocol hien tai.

## 6. Threshold sweep va ket qua hieu chinh nguong

| model_id | algorithm_family | feature_set | class_weight | threshold | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | macro_f1 | mcc | roc_auc | pr_auc | false_positive | false_negative | train_seconds | predict_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hist_gradient_boosting_none__ergonomic_v2_with_view | HistGradientBoosting | ergonomic_v2_with_view | none | 0.76 | 89.31% | 93.48% | 87.01% | 90.13% | 89.24% | 0.7875 | 94.91% | 96.21% | 155 | 332 | 0.7212 | 0.0234 |
| hist_gradient_boosting_balanced_sample_weight__ergonomic_v2_with_view | HistGradientBoosting | ergonomic_v2_with_view | balanced_sample_weight | 0.39 | 87.40% | 85.44% | 93.46% | 89.27% | 87.01% | 0.7453 | 94.70% | 95.73% | 407 | 167 | 0.5250 | 0.0180 |
| logistic_regression_none__ergonomic_14 | Logistic Regression | ergonomic_14 | none | 0.24 | 87.66% | 87.93% | 90.41% | 89.15% | 87.43% | 0.7490 | 92.28% | 93.39% | 317 | 245 | 0.0268 | 0.0019 |
| logistic_regression_balanced__ergonomic_14 | Logistic Regression | ergonomic_14 | balanced | 0.19 | 87.71% | 88.62% | 89.59% | 89.10% | 87.50% | 0.7502 | 92.26% | 93.35% | 294 | 266 | 0.0320 | 0.0019 |
| hist_gradient_boosting_none__ergonomic_v2 | HistGradientBoosting | ergonomic_v2 | none | 0.78 | 88.08% | 92.48% | 85.71% | 88.97% | 88.00% | 0.7631 | 93.04% | 95.26% | 178 | 365 | 0.5780 | 0.0167 |
| hist_gradient_boosting_balanced_sample_weight__ergonomic_v2 | HistGradientBoosting | ergonomic_v2 | balanced_sample_weight | 0.84 | 88.06% | 94.00% | 84.07% | 88.76% | 88.01% | 0.7665 | 93.24% | 95.39% | 137 | 407 | 0.5123 | 0.0174 |
| random_forest_balanced__ergonomic_v2 | Random Forest | ergonomic_v2 | balanced | 0.45 | 85.51% | 84.02% | 91.59% | 87.64% | 85.07% | 0.7060 | 91.10% | 93.61% | 445 | 215 | 2.2389 | 0.0708 |
| random_forest_balanced__ergonomic_v2_with_view | Random Forest | ergonomic_v2_with_view | balanced | 0.47 | 84.77% | 82.25% | 92.88% | 87.24% | 84.17% | 0.6930 | 91.72% | 94.22% | 512 | 182 | 1.9714 | 0.0814 |
| hist_gradient_boosting_balanced_sample_weight__ergonomic_14 | HistGradientBoosting | ergonomic_14 | balanced_sample_weight | 0.11 | 82.97% | 79.86% | 93.11% | 85.98% | 82.14% | 0.6585 | 84.05% | 85.92% | 600 | 176 | 0.5746 | 0.0207 |
| random_forest_balanced__combined_v2 | Random Forest | combined_v2 | balanced | 0.48 | 83.23% | 81.86% | 90.06% | 85.76% | 82.68% | 0.6592 | 91.81% | 94.06% | 510 | 254 | 5.7803 | 0.0820 |
| random_forest_none__ergonomic_v2_with_view | Random Forest | ergonomic_v2_with_view | none | 0.45 | 82.37% | 79.82% | 91.78% | 85.38% | 81.60% | 0.6445 | 90.34% | 93.09% | 593 | 210 | 1.8935 | 0.0817 |
| random_forest_none__ergonomic_14 | Random Forest | ergonomic_14 | none | 0.45 | 80.68% | 76.85% | 93.82% | 84.49% | 79.45% | 0.6166 | 81.00% | 84.63% | 722 | 158 | 1.2852 | 0.0701 |
| random_forest_balanced__ergonomic_14 | Random Forest | ergonomic_14 | balanced | 0.47 | 80.11% | 76.28% | 93.66% | 84.08% | 78.80% | 0.6053 | 81.53% | 84.84% | 744 | 162 | 1.3252 | 0.0690 |
| hist_gradient_boosting_none__ergonomic_14 | HistGradientBoosting | ergonomic_14 | none | 0.07 | 80.51% | 77.61% | 91.70% | 84.07% | 79.48% | 0.6080 | 83.54% | 85.46% | 676 | 212 | 0.4907 | 0.0213 |
| random_forest_none__combined_v2 | Random Forest | combined_v2 | none | 0.43 | 79.68% | 75.75% | 93.78% | 83.81% | 78.26% | 0.5973 | 87.32% | 89.72% | 767 | 159 | 5.3768 | 0.0823 |
| hist_gradient_boosting_balanced_sample_weight__combined_v2 | HistGradientBoosting | combined_v2 | balanced_sample_weight | 0.62 | 80.42% | 79.92% | 86.93% | 83.28% | 79.83% | 0.6007 | 87.36% | 90.61% | 558 | 334 | 1.5931 | 0.0195 |
| random_forest_none__normalized_99 | Random Forest | normalized_99 | none | 0.46 | 78.75% | 75.87% | 91.08% | 82.78% | 77.52% | 0.5724 | 84.33% | 86.91% | 740 | 228 | 4.4481 | 0.0609 |
| random_forest_balanced__combined_v2_with_view | Random Forest | combined_v2_with_view | balanced | 0.45 | 77.90% | 73.73% | 94.13% | 82.69% | 76.06% | 0.5646 | 88.15% | 91.70% | 857 | 150 | 5.8311 | 0.0919 |
| random_forest_none__ergonomic_v2 | Random Forest | ergonomic_v2 | none | 0.44 | 79.83% | 80.61% | 84.31% | 82.42% | 79.38% | 0.5887 | 88.34% | 91.36% | 518 | 401 | 2.1025 | 0.0700 |
| hist_gradient_boosting_none__combined_v2 | HistGradientBoosting | combined_v2 | none | 0.47 | 77.19% | 73.70% | 92.25% | 81.94% | 75.50% | 0.5449 | 86.92% | 89.80% | 841 | 198 | 1.5953 | 0.0194 |
| hist_gradient_boosting_balanced_sample_weight__combined_v2_with_view | HistGradientBoosting | combined_v2_with_view | balanced_sample_weight | 0.78 | 80.16% | 83.85% | 80.04% | 81.90% | 79.97% | 0.6005 | 87.51% | 90.47% | 394 | 510 | 1.6232 | 0.0210 |
| decision_tree_none__ergonomic_v2_with_view | Decision Tree | ergonomic_v2_with_view | none | 0.80 | 80.99% | 87.99% | 76.56% | 81.88% | 80.95% | 0.6276 | 81.00% | 83.88% | 267 | 599 | 0.2505 | 0.0012 |
| random_forest_none__combined_v2_with_view | Random Forest | combined_v2_with_view | none | 0.43 | 76.51% | 72.47% | 93.74% | 81.74% | 74.42% | 0.5367 | 86.21% | 89.16% | 910 | 160 | 6.0188 | 0.0936 |
| hist_gradient_boosting_none__combined_v2_with_view | HistGradientBoosting | combined_v2_with_view | none | 0.43 | 76.16% | 72.33% | 93.11% | 81.42% | 74.09% | 0.5276 | 84.14% | 86.50% | 910 | 176 | 1.5364 | 0.0208 |
| decision_tree_balanced__ergonomic_v2 | Decision Tree | ergonomic_v2 | balanced | 0.65 | 79.85% | 84.70% | 78.20% | 81.32% | 79.73% | 0.5975 | 82.70% | 85.01% | 361 | 557 | 0.2204 | 0.0011 |

Cac dong trong muc nay duoc chon tu threshold sweep tren external P06-P07. Neu dung de viet bai, can ghi ro day la phan tich hieu chinh nguong tren external, khong phai ket qua blind test hoan toan.

## 7. Model tot nhat theo default va theo calibrated threshold

Default threshold best:

| model_id | algorithm_family | feature_set | class_weight | threshold | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | macro_f1 | mcc | roc_auc | pr_auc | false_positive | false_negative | train_seconds | predict_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hist_gradient_boosting_balanced_sample_weight__ergonomic_v2_with_view | HistGradientBoosting | ergonomic_v2_with_view | balanced_sample_weight | 0.50 | 87.34% | 86.71% | 91.43% | 89.01% | 87.04% | 0.7424 | 94.70% | 95.73% | 358 | 219 | 0.5250 | 0.0180 |

External-calibrated best:

| model_id | algorithm_family | feature_set | class_weight | threshold | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | macro_f1 | mcc | roc_auc | pr_auc | false_positive | false_negative | train_seconds | predict_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hist_gradient_boosting_none__ergonomic_v2_with_view | HistGradientBoosting | ergonomic_v2_with_view | none | 0.76 | 89.31% | 93.48% | 87.01% | 90.13% | 89.24% | 0.7875 | 94.91% | 96.21% | 155 | 332 | 0.7212 | 0.0234 |

## 8. Rule-based Baseline

| model_id | algorithm_family | feature_set | class_weight | threshold | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | macro_f1 | mcc | roc_auc | pr_auc | false_positive | false_negative | train_seconds | predict_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rule_based_baseline | Rule-based Baseline | manual_ergonomic_rules | none | 0.50 | 56.08% | 56.08% | 100.00% | 71.86% | 35.93% | 0.0000 | 50.00% | 56.08% | 2001 | 0 | 0.0000 | 0.8607 |

Rule-based khong hoc tu du lieu. Day la baseline giai thich duoc nhung thuong kem linh hoat voi goc camera va khac biet co the nguoi dung.

## 9. ANN/Keras

| model_id | algorithm_family | feature_set | class_weight | threshold | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | macro_f1 | mcc | roc_auc | pr_auc | false_positive | false_negative | train_seconds | predict_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ann_keras_balanced__normalized_99 | ANN/Keras | normalized_99 | balanced | 0.50 | 68.72% | 68.37% | 82.31% | 74.69% | 66.88% | 0.3570 | 79.17% | 84.72% | 973 | 452 | 33.3327 | 0.2623 |
| ann_keras_balanced__ergonomic_v2_with_view | ANN/Keras | ergonomic_v2_with_view | balanced | 0.50 | 59.26% | 72.36% | 44.27% | 54.93% | 58.88% | 0.2371 | 69.18% | 73.51% | 432 | 1424 | 20.2135 | 0.2595 |

ANN/Keras duoc train lai tren dataset moi, nhung neu ket qua thap hon HGB thi nen trinh bay ANN la neural baseline hoac model tich hop ban dau.

## 10. HistGradientBoosting

| model_id | algorithm_family | feature_set | class_weight | threshold | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | macro_f1 | mcc | roc_auc | pr_auc | false_positive | false_negative | train_seconds | predict_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hist_gradient_boosting_balanced_sample_weight__ergonomic_v2_with_view | HistGradientBoosting | ergonomic_v2_with_view | balanced_sample_weight | 0.50 | 87.34% | 86.71% | 91.43% | 89.01% | 87.04% | 0.7424 | 94.70% | 95.73% | 358 | 219 | 0.5250 | 0.0180 |
| hist_gradient_boosting_none__ergonomic_v2_with_view | HistGradientBoosting | ergonomic_v2_with_view | none | 0.50 | 86.46% | 85.89% | 90.76% | 88.26% | 86.13% | 0.7244 | 94.91% | 96.21% | 381 | 236 | 0.7212 | 0.0234 |
| hist_gradient_boosting_balanced_sample_weight__ergonomic_v2 | HistGradientBoosting | ergonomic_v2 | balanced_sample_weight | 0.50 | 85.25% | 84.10% | 90.88% | 87.36% | 84.83% | 0.7002 | 93.24% | 95.39% | 439 | 233 | 0.5123 | 0.0174 |
| hist_gradient_boosting_none__ergonomic_v2 | HistGradientBoosting | ergonomic_v2 | none | 0.50 | 84.66% | 82.75% | 91.78% | 87.03% | 84.13% | 0.6893 | 93.04% | 95.26% | 489 | 210 | 0.5780 | 0.0167 |
| hist_gradient_boosting_balanced_sample_weight__combined_v2 | HistGradientBoosting | combined_v2 | balanced_sample_weight | 0.50 | 78.27% | 75.88% | 89.78% | 82.25% | 77.12% | 0.5604 | 87.36% | 90.61% | 729 | 261 | 1.5931 | 0.0195 |
| hist_gradient_boosting_none__combined_v2 | HistGradientBoosting | combined_v2 | none | 0.50 | 77.30% | 74.10% | 91.51% | 81.89% | 75.75% | 0.5450 | 86.92% | 89.80% | 817 | 217 | 1.5953 | 0.0194 |
| hist_gradient_boosting_balanced_sample_weight__combined_v2_with_view | HistGradientBoosting | combined_v2_with_view | balanced_sample_weight | 0.50 | 77.66% | 76.06% | 87.79% | 81.50% | 76.64% | 0.5454 | 87.51% | 90.47% | 706 | 312 | 1.6232 | 0.0210 |
| hist_gradient_boosting_balanced_sample_weight__ergonomic_14 | HistGradientBoosting | ergonomic_14 | balanced_sample_weight | 0.50 | 78.71% | 82.23% | 79.14% | 80.65% | 78.49% | 0.5706 | 84.05% | 85.92% | 437 | 533 | 0.5746 | 0.0207 |
| hist_gradient_boosting_none__combined_v2_with_view | HistGradientBoosting | combined_v2_with_view | none | 0.50 | 75.00% | 72.39% | 89.59% | 80.08% | 73.26% | 0.4950 | 84.14% | 86.50% | 873 | 266 | 1.5364 | 0.0208 |
| hist_gradient_boosting_none__normalized_99 | HistGradientBoosting | normalized_99 | none | 0.50 | 67.67% | 64.28% | 95.30% | 76.78% | 61.79% | 0.3670 | 69.58% | 76.15% | 1353 | 120 | 1.2365 | 0.0195 |
| hist_gradient_boosting_none__raw_99 | HistGradientBoosting | raw_99 | none | 0.50 | 65.67% | 62.06% | 99.77% | 76.52% | 56.34% | 0.3647 | 53.42% | 59.04% | 1558 | 6 | 1.3330 | 0.0176 |
| hist_gradient_boosting_balanced_sample_weight__raw_99 | HistGradientBoosting | raw_99 | balanced_sample_weight | 0.50 | 65.63% | 62.03% | 99.77% | 76.50% | 56.27% | 0.3638 | 55.23% | 59.63% | 1560 | 6 | 1.1357 | 0.0171 |

## 11. Video-wise external analysis cho selected calibrated model

| source_video | participant_id | view_angle | label | n | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | false_positive | false_negative | majority_pred_label | mean_prob_incorrect |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dataset\external_videos\incorrect\P07_incorrect_side_90_001.mp4 | P07 | side_90 | 1 | 234 | 29.91% | 100.00% | 29.91% | 46.05% | 0 | 164 | 0 | 0.5177 |
| dataset\external_videos\incorrect\P07_incorrect_side_30_002.mp4 | P07 | side_30 | 1 | 238 | 62.18% | 100.00% | 62.18% | 76.68% | 0 | 90 | 1 | 0.6924 |
| dataset\external_videos\correct\P06_correct_side_30_001.mp4 | P06 | side_30 | 0 | 157 | 68.15% | 0.00% | 0.00% | 0.00% | 50 | 0 | 0 | 0.7152 |
| dataset\external_videos\correct\P07_correct_side_90_003.mp4 | P07 | side_90 | 0 | 230 | 70.43% | 0.00% | 0.00% | 0.00% | 68 | 0 | 0 | 0.3856 |
| dataset\external_videos\incorrect\P06_incorrect_side_90_002.mp4 | P06 | side_90 | 1 | 228 | 82.89% | 100.00% | 82.89% | 90.65% | 0 | 39 | 1 | 0.8611 |
| dataset\external_videos\correct\P06_correct_front_001.mp4 | P06 | front | 0 | 179 | 90.50% | 0.00% | 0.00% | 0.00% | 17 | 0 | 0 | 0.1914 |
| dataset\external_videos\correct\P06_correct_side_90_001.mp4 | P06 | side_90 | 0 | 190 | 94.74% | 0.00% | 0.00% | 0.00% | 10 | 0 | 0 | 0.2452 |
| dataset\external_videos\incorrect\P07_incorrect_front_003.mp4 | P07 | front | 1 | 206 | 95.15% | 100.00% | 95.15% | 97.51% | 0 | 10 | 1 | 0.9509 |
| dataset\external_videos\incorrect\P07_incorrect_side_90_002.mp4 | P07 | side_90 | 1 | 246 | 95.53% | 100.00% | 95.53% | 97.71% | 0 | 11 | 1 | 0.9575 |
| dataset\external_videos\incorrect\P07_incorrect_front_001.mp4 | P07 | front | 1 | 168 | 97.02% | 100.00% | 97.02% | 98.49% | 0 | 5 | 1 | 0.9303 |
| dataset\external_videos\correct\P06_correct_side_90_002.mp4 | P06 | side_90 | 0 | 160 | 97.50% | 0.00% | 0.00% | 0.00% | 4 | 0 | 0 | 0.3532 |
| dataset\external_videos\correct\P07_correct_side_90_001.mp4 | P07 | side_90 | 0 | 209 | 97.61% | 0.00% | 0.00% | 0.00% | 5 | 0 | 0 | 0.0539 |
| dataset\external_videos\incorrect\P06_incorrect_side_30_001.mp4 | P06 | side_30 | 1 | 218 | 97.71% | 100.00% | 97.71% | 98.84% | 0 | 5 | 1 | 0.9743 |
| dataset\external_videos\incorrect\P06_incorrect_side_30_002.mp4 | P06 | side_30 | 1 | 192 | 98.44% | 100.00% | 98.44% | 99.21% | 0 | 3 | 1 | 0.9865 |
| dataset\external_videos\incorrect\P06_incorrect_front_001.mp4 | P06 | front | 1 | 233 | 98.71% | 100.00% | 98.71% | 99.35% | 0 | 3 | 1 | 0.9638 |
| dataset\external_videos\incorrect\P07_incorrect_front_002.mp4 | P07 | front | 1 | 201 | 99.00% | 100.00% | 99.00% | 99.50% | 0 | 2 | 1 | 0.9513 |
| dataset\external_videos\correct\P07_correct_side_30_001.mp4 | P07 | side_30 | 0 | 197 | 99.49% | 0.00% | 0.00% | 0.00% | 1 | 0 | 0 | 0.0485 |
| dataset\external_videos\correct\P06_correct_front_002.mp4 | P06 | front | 0 | 100 | 100.00% | 0.00% | 0.00% | 0.00% | 0 | 0 | 0 | 0.0324 |
| dataset\external_videos\correct\P07_correct_front_001.mp4 | P07 | front | 0 | 215 | 100.00% | 0.00% | 0.00% | 0.00% | 0 | 0 | 0 | 0.0080 |
| dataset\external_videos\correct\P07_correct_side_30_002.mp4 | P07 | side_30 | 0 | 133 | 100.00% | 0.00% | 0.00% | 0.00% | 0 | 0 | 0 | 0.1781 |
| dataset\external_videos\correct\P07_correct_side_90_002.mp4 | P07 | side_90 | 0 | 231 | 100.00% | 0.00% | 0.00% | 0.00% | 0 | 0 | 0 | 0.0210 |
| dataset\external_videos\incorrect\P06_incorrect_side_90_001.mp4 | P06 | side_90 | 1 | 181 | 100.00% | 100.00% | 100.00% | 100.00% | 0 | 0 | 1 | 0.9991 |
| dataset\external_videos\incorrect\P07_incorrect_side_30_001.mp4 | P07 | side_30 | 1 | 210 | 100.00% | 100.00% | 100.00% | 100.00% | 0 | 0 | 1 | 0.9989 |

## 12. Participant-wise external analysis cho selected calibrated model

| participant_id | n | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | mcc | false_positive | false_negative |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P06 | 1838 | 92.87% | 92.52% | 95.25% | 93.86% | 0.8542 | 81 | 50 |
| P07 | 2718 | 86.90% | 94.29% | 81.24% | 87.28% | 0.7481 | 74 | 282 |

## 13. File da xuat

- `reports\results\full_protocol_model_benchmark_external_p06p07.csv`
- `reports\results\full_protocol_threshold_sweep_external_p06p07.csv`
- `reports\results\full_protocol_predictions_external_p06p07.csv`
- `reports\results\full_protocol_rule_based_external_p06p07.csv`
- `reports\results\full_protocol_video_wise_external_p06p07.csv`
- `reports\results\full_protocol_participant_wise_external_p06p07.csv`
- `reports\figures\full_protocol_model_comparison_bar.png`
- `reports\figures\full_protocol_confusion_matrix_best.png`
- `reports\figures\full_protocol_threshold_sweep_best.png`

## 14. Ket luan su dung cho luan van

Ket qua benchmark day du nen thay the bang so sanh 4 cau hinh dai dien neu muc 4.4 dang can minh chung tat ca thuat toan da duoc chay lai. Trong than luan van, nen dua bang tom tat top cau hinh cua tung algorithm family; bieu do chi nen minh hoa Accuracy, Precision, Recall va F1 de tranh qua tai thong tin.

Neu model tot nhat khac ANN/Keras, co the trinh bay ANN la neural baseline/model tich hop ban dau, con model co ket qua external tot hon la model duoc de xuat cho phien ban ung dung cap nhat.

## 15. Checklist

- [x] Da train Logistic Regression
- [x] Da train SVM
- [x] Da train KNN
- [x] Da train Decision Tree
- [x] Da train Random Forest
- [x] Da train MLPClassifier
- [x] Da train ANN/Keras
- [x] Da train HistGradientBoosting
- [x] Da danh gia Rule-based Baseline
- [x] Train/external khong trung participant
- [x] Train/external khong trung source_video
- [x] Co video-wise report
- [x] Co participant-wise report
- [x] Co threshold sweep
- [x] Khong cap nhat app registry
