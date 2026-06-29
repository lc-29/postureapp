# Full Protocol Benchmark Final Review cho Chương 4

Thời điểm tạo: 2026-06-26 01:33:29

## 1. Dataset split và kiểm tra leakage

- Tập phát triển: 12680 mẫu, 94 video, participants P01, P02, P03, P04, P05.
- Tập external: 4556 mẫu, 23 video, participants P06, P07.
- Train label counts: {'0': 5206, '1': 7474}.
- External label counts: {'0': 2001, '1': 2555}.
- Source video overlap: 0.
- Participant disjoint: True.
- Source video disjoint: True.
- Split check passed: True.

## 2. Feature set và thuật toán

- Feature sets: `raw_99`, `normalized_99`, `ergonomic_14`, `ergonomic_v2`, `ergonomic_v2_with_view`, `combined_v2`, `combined_v2_with_view`.
- Thuật toán: Logistic Regression, SVM RBF, KNN, Decision Tree, Random Forest, MLPClassifier, ANN/Keras, HistGradientBoosting, Rule-based Baseline.
- Lớp dương: `Incorrect`.
- Bảng 4.5 và Hình 4.2 chỉ dùng threshold mặc định 0,50.

## 3. Top cấu hình trong toàn bộ benchmark mặc định

| algorithm_family | model_id | feature_set | threshold | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | mcc | false_positive | false_negative |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | hist_gradient_boosting_balanced_sample_weight__ergonomic_v2_with_view | ergonomic_v2_with_view | 0.50 | 87,34% | 86,71% | 91,43% | 89,01% | 0,7424 | 358 | 219 |
| HistGradientBoosting | hist_gradient_boosting_none__ergonomic_v2_with_view | ergonomic_v2_with_view | 0.50 | 86,46% | 85,89% | 90,76% | 88,26% | 0,7244 | 381 | 236 |
| HistGradientBoosting | hist_gradient_boosting_balanced_sample_weight__ergonomic_v2 | ergonomic_v2 | 0.50 | 85,25% | 84,10% | 90,88% | 87,36% | 0,7002 | 439 | 233 |
| HistGradientBoosting | hist_gradient_boosting_none__ergonomic_v2 | ergonomic_v2 | 0.50 | 84,66% | 82,75% | 91,78% | 87,03% | 0,6893 | 489 | 210 |
| Logistic Regression | logistic_regression_none__ergonomic_14 | ergonomic_14 | 0.50 | 86,24% | 94,10% | 80,51% | 86,77% | 0,7357 | 129 | 498 |
| Random Forest | random_forest_balanced__ergonomic_v2_with_view | ergonomic_v2_with_view | 0.50 | 83,87% | 84,89% | 86,65% | 85,76% | 0,6718 | 394 | 341 |
| Random Forest | random_forest_balanced__combined_v2 | combined_v2 | 0.50 | 83,65% | 85,21% | 85,71% | 85,46% | 0,6678 | 380 | 365 |
| Random Forest | random_forest_none__ergonomic_v2_with_view | ergonomic_v2_with_view | 0.50 | 82,51% | 83,99% | 85,01% | 84,50% | 0,6443 | 414 | 383 |
| Random Forest | random_forest_balanced__ergonomic_v2 | ergonomic_v2 | 0.50 | 82,44% | 86,40% | 81,53% | 83,89% | 0,6476 | 328 | 472 |
| Logistic Regression | logistic_regression_balanced__ergonomic_14 | ergonomic_14 | 0.50 | 83,54% | 94,74% | 74,79% | 83,60% | 0,6944 | 106 | 644 |
| Random Forest | random_forest_balanced__ergonomic_14 | ergonomic_14 | 0.50 | 79,46% | 76,99% | 90,37% | 83,15% | 0,5848 | 690 | 246 |
| HistGradientBoosting | hist_gradient_boosting_balanced_sample_weight__combined_v2 | combined_v2 | 0.50 | 78,27% | 75,88% | 89,78% | 82,25% | 0,5604 | 729 | 261 |
| HistGradientBoosting | hist_gradient_boosting_none__combined_v2 | combined_v2 | 0.50 | 77,30% | 74,10% | 91,51% | 81,89% | 0,5450 | 817 | 217 |
| HistGradientBoosting | hist_gradient_boosting_balanced_sample_weight__combined_v2_with_view | combined_v2_with_view | 0.50 | 77,66% | 76,06% | 87,79% | 81,50% | 0,5454 | 706 | 312 |
| Random Forest | random_forest_none__ergonomic_14 | ergonomic_14 | 0.50 | 77,90% | 76,89% | 86,61% | 81,47% | 0,5492 | 665 | 342 |
| HistGradientBoosting | hist_gradient_boosting_balanced_sample_weight__ergonomic_14 | ergonomic_14 | 0.50 | 78,71% | 82,23% | 79,14% | 80,65% | 0,5706 | 437 | 533 |
| HistGradientBoosting | hist_gradient_boosting_none__combined_v2_with_view | combined_v2_with_view | 0.50 | 75,00% | 72,39% | 89,59% | 80,08% | 0,4950 | 873 | 266 |
| Random Forest | random_forest_balanced__combined_v2_with_view | combined_v2_with_view | 0.50 | 76,47% | 77,58% | 81,64% | 79,56% | 0,5198 | 603 | 469 |
| Random Forest | random_forest_none__ergonomic_v2 | ergonomic_v2 | 0.50 | 78,23% | 84,23% | 75,26% | 79,50% | 0,5685 | 360 | 632 |
| Random Forest | random_forest_none__combined_v2 | combined_v2 | 0.50 | 77,35% | 81,88% | 76,56% | 79,13% | 0,5457 | 433 | 599 |

## 4. Bảng 4.5 đề xuất - cấu hình đại diện tại threshold 0,50

| algorithm_family | model_id | feature_set | class_weight | threshold | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | macro_f1 | mcc | roc_auc | pr_auc | false_positive | false_negative |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | hist_gradient_boosting_balanced_sample_weight__ergonomic_v2_with_view | ergonomic_v2_with_view | balanced_sample_weight | 0.50 | 87,34% | 86,71% | 91,43% | 89,01% | 87,04% | 0,7424 | 94,70% | 95,73% | 358 | 219 |
| Logistic Regression | logistic_regression_none__ergonomic_14 | ergonomic_14 | none | 0.50 | 86,24% | 94,10% | 80,51% | 86,77% | 86,22% | 0,7357 | 92,28% | 93,39% | 129 | 498 |
| Random Forest | random_forest_balanced__ergonomic_v2_with_view | ergonomic_v2_with_view | balanced | 0.50 | 83,87% | 84,89% | 86,65% | 85,76% | 83,58% | 0,6718 | 91,72% | 94,22% | 394 | 341 |
| SVM RBF | svm_rbf_balanced__normalized_99 | normalized_99 | balanced | 0.50 | 68,09% | 63,98% | 98,63% | 77,61% | 61,04% | 0,4020 | 79,15% | 83,61% | 1419 | 35 |
| Decision Tree | decision_tree_none__combined_v2_with_view | combined_v2_with_view | none | 0.50 | 68,11% | 65,08% | 93,07% | 76,60% | 63,27% | 0,3650 | 68,43% | 72,01% | 1276 | 177 |
| KNN | knn_none__ergonomic_14 | ergonomic_14 | none | 0.50 | 73,64% | 79,67% | 71,15% | 75,17% | 73,54% | 0,4761 | 80,96% | 82,55% | 464 | 737 |
| ANN/Keras | ann_keras_balanced__normalized_99 | normalized_99 | balanced | 0.50 | 68,72% | 68,37% | 82,31% | 74,69% | 66,88% | 0,3570 | 79,17% | 84,72% | 973 | 452 |
| MLPClassifier | mlp_sklearn_none__raw_99 | raw_99 | none | 0.50 | 58,38% | 57,40% | 100,00% | 72,94% | 41,45% | 0,1736 | 57,39% | 60,44% | 1896 | 0 |
| Rule-based Baseline | rule_based_baseline | manual_ergonomic_rules | none | rule | 56,08% | 56,08% | 100,00% | 71,86% | 35,93% | 0,0000 | 50,00% | 56,08% | 2001 | 0 |

Bảng này nên dùng làm Bảng 4.5 trong luận văn. Mỗi nhóm thuật toán chỉ giữ một cấu hình đại diện tốt nhất tại ngưỡng mặc định 0,50 để tránh đưa toàn bộ 87 cấu hình vào nội dung chính.

## 5. Hình 4.2

- File PNG: `reports/figures/figure_4_2_algorithm_family_default_threshold_heatmap.png`.
- File SVG: `reports/figures/figure_4_2_algorithm_family_default_threshold_heatmap.svg`.

**Caption đề xuất:** Hình 4.2. So sánh Accuracy, Precision, Recall và F1-score của cấu hình đại diện thuộc từng nhóm thuật toán trên tập external P06-P07 tại ngưỡng mặc định 0,50.

**Đoạn mô tả:** Hình 4.2 cho thấy HistGradientBoosting tại ngưỡng mặc định 0,50 đạt F1-score lớp Incorrect cao nhất trong các nhóm thuật toán được so sánh. Logistic Regression có Precision cao nhưng Recall thấp hơn, trong khi SVM RBF, MLPClassifier và Rule-based Baseline có Recall rất cao nhưng Precision thấp do tạo nhiều False Positive. Vì vậy, cần đánh giá đồng thời Accuracy, Precision, Recall, F1-score, MCC và FP/FN thay vì chỉ nhìn một chỉ số riêng lẻ.

## 6. Phân tích riêng HGB threshold 0,76

| model_id | feature_set | class_weight | threshold | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | macro_f1 | mcc | roc_auc | pr_auc | true_negative | false_positive | false_negative | true_positive |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hist_gradient_boosting_none__ergonomic_v2_with_view | ergonomic_v2_with_view | none | 0.76 | 89,31% | 93,48% | 87,01% | 90,13% | 89,24% | 0,7875 | 94,91% | 96,21% | 1846 | 155 | 332 | 2223 |

Ngưỡng 0,76 được hiệu chỉnh dựa trên external P06-P07. Vì external đã được sử dụng để phân tích lỗi và chọn ngưỡng, kết quả này không được xem là blind external test hoàn toàn độc lập.

- Hình 4.3: `reports/figures/figure_4_3_selected_hgb_threshold_sweep.png`.
- Hình 4.4: `reports/figures/figure_4_4_selected_hgb_confusion_matrix.png`.

## 7. Phân tích Recall 100%

| algorithm_family | model_id | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | mcc | false_positive | false_negative | predicted_incorrect_rate | analysis_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MLPClassifier | mlp_sklearn_none__raw_99 | 58,38% | 57,40% | 100,00% | 72,94% | 0,1736 | 1896 | 0 | 97,70% | Recall 100% do mô hình dự đoán gần như/toàn bộ frame là Incorrect; FP cao nên không thể xem là vượt trội. |
| Rule-based Baseline | rule_based_baseline | 56,08% | 56,08% | 100,00% | 71,86% | 0,0000 | 2001 | 0 | 100,00% | Recall 100% do mô hình dự đoán gần như/toàn bộ frame là Incorrect; FP cao nên không thể xem là vượt trội. |

Recall 100% không đồng nghĩa với mô hình tốt. Trong external P06-P07, MLPClassifier và Rule-based Baseline có Recall 100% vì dự đoán gần như hoặc toàn bộ frame là Incorrect. Điều này làm False Positive tăng cao, Precision thấp và MCC kém. Do đó các mô hình này không nên được diễn giải là vượt trội dù không bỏ sót frame Incorrect.

## 8. Repeatability nhiều seed

| algorithm_family | model_id | feature_set | class_weight | accuracy_mean | accuracy_std | precision_incorrect_mean | precision_incorrect_std | recall_incorrect_mean | recall_incorrect_std | f1_incorrect_mean | f1_incorrect_std | mcc_mean | mcc_std | false_positive_mean | false_positive_std | false_negative_mean | false_negative_std |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HistGradientBoosting | hist_gradient_boosting_balanced_sample_weight__ergonomic_v2_with_view | ergonomic_v2_with_view | balanced_sample_weight | 86,02% | 0,93% | 87,08% | 0,46% | 88,16% | 2,40% | 87,60% | 1,02% | 0,7163 | 0,0181 | 334,40 | 21,38 | 302,40 | 61,33 |
| Random Forest | random_forest_balanced__ergonomic_v2_with_view | ergonomic_v2_with_view | balanced | 83,51% | 0,88% | 84,78% | 1,37% | 86,11% | 2,73% | 85,40% | 1,00% | 0,6654 | 0,0170 | 396,20 | 50,27 | 355,00 | 69,83 |
| Decision Tree | decision_tree_none__combined_v2_with_view | combined_v2_with_view | none | 68,11% | 0,00% | 65,08% | 0,00% | 93,07% | 0,00% | 76,60% | 0,00% | 0,3650 | 0,0000 | 1276,00 | 0,00 | 177,00 | 0,00 |
| ANN/Keras | ann_keras_balanced__normalized_99 | normalized_99 | balanced | 64,86% | 6,16% | 76,85% | 8,78% | 53,87% | 6,86% | 63,16% | 6,80% | 0,3342 | 0,1300 | 422,60 | 185,36 | 1178,60 | 175,37 |
| MLPClassifier | mlp_sklearn_none__raw_99 | raw_99 | none | 53,92% | 4,22% | 55,30% | 2,09% | 92,10% | 6,92% | 69,09% | 3,58% | -0,0238 | 0,1553 | 1897,40 | 24,16 | 201,80 | 176,91 |

Kết quả repeatability dùng để đánh giá độ ổn định giữa các lần train với seed khác nhau. Không dùng trung bình nhiều seed để chọn lại model hoặc hiệu chỉnh threshold trên external.

## 9. File đã xuất

- `reports\results\full_protocol_best_by_algorithm_default_threshold.csv`
- `reports\results\selected_hgb_external_calibrated_metrics.csv`
- `reports\results\full_protocol_repeatability_by_seed.csv`
- `reports\results\full_protocol_repeatability_mean_std.csv`
- `reports\figures\figure_4_2_algorithm_family_default_threshold_heatmap.png`
- `reports\figures\figure_4_2_algorithm_family_default_threshold_heatmap.svg`
- `reports\figures\figure_4_3_selected_hgb_threshold_sweep.png`
- `reports\figures\figure_4_3_selected_hgb_threshold_sweep.svg`
- `reports\figures\figure_4_4_selected_hgb_confusion_matrix.png`
- `reports\figures\figure_4_4_selected_hgb_confusion_matrix.svg`

## 10. Xác nhận phạm vi thay đổi

- Không cập nhật app registry.
- Không sửa SQLite.
- Không sửa giao diện app.
- Không thay thế model đang dùng trong app.
- Các số liệu trong hình được đọc từ CSV benchmark, không nhập tay.

## 11. Checklist

- [x] full_protocol_best_by_algorithm_default_threshold.csv có đủ 9 dòng
- [x] Hình 4.2 dùng threshold 0,50
- [x] Hình 4.2 không chứa HGB threshold 0,76
- [x] Hình 4.2 không có chữ Model được chọn
- [x] Hình 4.2 không có viền đỏ
- [x] Hình 4.2 dùng thang màu 0-100
- [x] HGB threshold 0,76 nằm ở phần riêng
- [x] Có cảnh báo threshold 0,76 không phải blind external test hoàn toàn
- [x] Có phân tích Recall 100% của MLPClassifier và Rule-based
- [x] Có repeatability mean ± std
- [x] Không cập nhật app registry
- [x] Không sửa SQLite
- [x] Không sửa giao diện app
