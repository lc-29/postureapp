# 26. TASK - Chuẩn hóa bảng, hình và báo cáo benchmark cho Chương 4 luận văn

## 1. Bối cảnh

Sau khi đã chạy lại benchmark đầy đủ theo protocol P01-P05 -> P06-P07, dự án đã có báo cáo:

- `reports/FULL_PROTOCOL_MODEL_BENCHMARK_EXTERNAL_P06P07_REPORT.md`
- `reports/results/full_protocol_model_benchmark_external_p06p07.csv`
- `reports/results/full_protocol_threshold_sweep_external_p06p07.csv`
- `reports/results/full_protocol_predictions_external_p06p07.csv`
- `reports/results/full_protocol_video_wise_external_p06p07.csv`
- `reports/results/full_protocol_participant_wise_external_p06p07.csv`

Tuy nhiên, để đưa vào Chương 4 của luận văn, cần chuẩn hóa lại cách trình bày:

- Bảng 4.5 và Hình 4.2 chỉ dùng kết quả so sánh công bằng tại `threshold = 0.50`.
- Không trộn HGB ngưỡng 0.76 vào bảng/hình so sánh mặc định.
- HGB ngưỡng 0.76 phải được phân tích riêng như phần hiệu chỉnh ngưỡng.
- Các thuật toán có Recall 100% như MLPClassifier và Rule-based Baseline cần được giải thích cẩn thận, không xem Recall 100% là vượt trội.

## 2. Ràng buộc bắt buộc

Không được làm các việc sau:

- Không chỉnh sửa cấu trúc SQLite.
- Không thay đổi giao diện desktop app.
- Không cập nhật `models/model_registry.json`.
- Không thay thế model đang được app sử dụng.
- Không xóa model artifact, CSV hoặc báo cáo hiện có.
- Không tự bịa số liệu.
- Không nhập tay số liệu nếu có thể đọc trực tiếp từ CSV.
- Không làm lỗi tiếng Việt có dấu hoặc mojibake.

Chỉ được bổ sung/chỉnh:

- Script benchmark/report.
- Script tạo bảng/hình.
- CSV tổng hợp phục vụ Chương 4.
- Hình minh họa phục vụ Chương 4.
- Báo cáo Markdown tổng hợp.

## 3. Dữ liệu và protocol cần xác nhận lại

Trước khi tạo bảng/hình, kiểm tra lại:

- Train/development:
  - 12.680 mẫu.
  - 94 video.
  - Participants: P01-P05.
- External:
  - 4.556 mẫu.
  - 23 video.
  - Participants: P06-P07.
  - Correct: 2.001 mẫu.
  - Incorrect: 2.555 mẫu.
- Không trùng `participant_id` giữa train và external.
- Không trùng `source_video` giữa train và external.
- Lớp dương là `Incorrect`.

Nếu sai bất kỳ điều nào, dừng task và báo lỗi trong report.

## 4. Chuẩn hóa tên feature set

Trong toàn bộ bảng, hình, caption và báo cáo, dùng đúng tên:

- `raw_99`
- `normalized_99`
- `ergonomic_14`
- `ergonomic_v2`
- `ergonomic_v2_with_view`
- `combined_v2`
- `combined_v2_with_view`

Không dùng tên rút gọn sai:

- `ergonomic_v2_view`
- `combined_v2_view`

Nếu hình cần rút gọn để dễ đọc, có thể dùng nhãn ngắn nhưng phải ghi rõ trong ghi chú, ví dụ:

- `ergonomic_v2_with_view` có thể xuống dòng, không đổi thành tên schema khác.

## 5. Bảng 4.5 - So sánh công bằng tại threshold 0.50

Tạo bảng đại diện cho từng nhóm thuật toán tại ngưỡng mặc định:

`threshold = 0.50`

Áp dụng cho các mô hình có xác suất hoặc decision score.

Không đưa `hist_gradient_boosting_none__ergonomic_v2_with_view` tại ngưỡng 0.76 vào Bảng 4.5.

### 5.1. Thuật toán phải có trong Bảng 4.5

Mỗi nhóm thuật toán lấy 1 cấu hình đại diện tốt nhất:

1. Logistic Regression.
2. SVM RBF.
3. KNN.
4. Decision Tree.
5. Random Forest.
6. MLPClassifier.
7. ANN/Keras.
8. HistGradientBoosting.
9. Rule-based Baseline.

### 5.2. Quy tắc chọn cấu hình đại diện

Với mỗi nhóm thuật toán, chọn cấu hình theo thứ tự:

1. F1-score lớp `Incorrect` cao nhất tại threshold 0.50.
2. Nếu bằng nhau, chọn MCC cao hơn.
3. Nếu vẫn bằng nhau, chọn Accuracy cao hơn.
4. Nếu vẫn bằng nhau, chọn False Positive thấp hơn.

Rule-based Baseline là dòng riêng, không dùng threshold xác suất.

### 5.3. Cột cần xuất

Xuất CSV:

`reports/results/full_protocol_best_by_algorithm_default_threshold.csv`

Cột bắt buộc:

- `algorithm_family`
- `model_id`
- `feature_set`
- `class_weight`
- `threshold`
- `accuracy`
- `precision_incorrect`
- `recall_incorrect`
- `f1_incorrect`
- `macro_f1`
- `mcc`
- `roc_auc`
- `pr_auc`
- `false_positive`
- `false_negative`
- `train_seconds`
- `predict_seconds`

### 5.4. Bảng Markdown cho luận văn

Trong report cuối, tạo thêm bảng Markdown có thể copy vào luận văn, hiển thị số theo dạng:

- Accuracy, Precision, Recall, F1-score, Macro-F1, ROC-AUC, PR-AUC: phần trăm, 2 chữ số thập phân.
- MCC: 4 chữ số thập phân.
- FP/FN: số nguyên.
- Threshold: `0.50` hoặc `rule`.

## 6. Tạo lại Hình 4.2

Tạo heatmap so sánh 4 chỉ số:

- Accuracy.
- Precision lớp Incorrect.
- Recall lớp Incorrect.
- F1-score lớp Incorrect.

Dữ liệu lấy từ:

`reports/results/full_protocol_best_by_algorithm_default_threshold.csv`

### 6.1. Yêu cầu nội dung

- Mỗi dòng là cấu hình đại diện tốt nhất của một nhóm thuật toán tại threshold 0.50.
- Sắp xếp dòng theo F1-score giảm dần.
- Không dùng HGB threshold 0.76.
- Không có dòng chữ `Model được chọn`.
- Không dùng viền đỏ để đánh dấu HGB.
- Không dùng thang màu 55-100 vì dễ phóng đại chênh lệch.
- Thang màu phải từ 0 đến 100.
- Nhãn phần trăm dùng dấu phẩy thập phân, ví dụ `87,34%`.
- Nền trắng.
- Xuất ít nhất 300 DPI.
- Font rõ, không chồng chữ.

### 6.2. File hình cần xuất

Xuất:

- `reports/figures/figure_4_2_algorithm_family_default_threshold_heatmap.png`
- `reports/figures/figure_4_2_algorithm_family_default_threshold_heatmap.svg`

Có thể đồng thời cập nhật file thuận tiện hiện tại:

- `reports/figures/figure_4_2_model_metric_comparison.png`
- `reports/figures/figure_4_2_model_metric_comparison.svg`

Nhưng nội dung phải đúng quy tắc threshold 0.50.

### 6.3. Caption đề xuất

> Hình 4.2. So sánh Accuracy, Precision, Recall và F1-score của cấu hình đại diện thuộc từng nhóm thuật toán trên tập external P06-P07 tại ngưỡng mặc định 0,50.

### 6.4. Ghi chú dưới hình

> Mỗi dòng là cấu hình có F1-score lớp Incorrect cao nhất của một nhóm thuật toán tại ngưỡng mặc định 0,50 trên tập external P06-P07. Precision, Recall và F1-score được tính cho lớp Incorrect. Rule-based Baseline không sử dụng ngưỡng xác suất.

## 7. Phân tích riêng HGB ngưỡng 0.76

Tách riêng phần model được chọn:

- Algorithm: HistGradientBoosting.
- Feature set: `ergonomic_v2_with_view`.
- Class weight: `none`.
- Threshold: 0.76.

Không trộn phần này vào Bảng 4.5 hoặc Hình 4.2.

### 7.1. File cần xuất

Xuất:

- `reports/results/selected_hgb_external_calibrated_metrics.csv`
- `reports/figures/figure_4_3_selected_hgb_threshold_sweep.png`
- `reports/figures/figure_4_3_selected_hgb_threshold_sweep.svg`
- `reports/figures/figure_4_4_selected_hgb_confusion_matrix.png`
- `reports/figures/figure_4_4_selected_hgb_confusion_matrix.svg`

### 7.2. Metric cần có

- Accuracy.
- Precision Incorrect.
- Recall Incorrect.
- F1 Incorrect.
- Macro-F1.
- MCC.
- ROC-AUC.
- PR-AUC.
- TN.
- FP.
- FN.
- TP.

### 7.3. Câu bắt buộc ghi trong report

> Ngưỡng 0,76 được hiệu chỉnh dựa trên external P06-P07. Vì external đã được sử dụng để phân tích lỗi và chọn ngưỡng, kết quả này không được xem là blind external test hoàn toàn độc lập.

## 8. Phân tích Recall 100%

Kiểm tra riêng:

- MLPClassifier.
- Rule-based Baseline.

Trong report phải nêu:

- Recall 100% không đồng nghĩa với mô hình tốt.
- Nếu mô hình dự đoán gần như toàn bộ mẫu thành `Incorrect`, Precision sẽ thấp và FP tăng cao.
- Cần báo cáo FP, FN, MCC và confusion matrix.
- Không được diễn giải Recall 100% như hiệu quả vượt trội.

Xuất bảng nhỏ trong report gồm:

- Algorithm.
- Model ID.
- Accuracy.
- Precision Incorrect.
- Recall Incorrect.
- F1 Incorrect.
- MCC.
- FP.
- FN.
- Tỷ lệ frame dự đoán Incorrect.
- Nhận xét ngắn.

## 9. Kiểm tra độ lặp lại với nhiều seed

Chạy lại với seed:

`[42, 43, 44, 45, 46]`

Áp dụng cho các mô hình có yếu tố ngẫu nhiên:

- Random Forest.
- MLPClassifier.
- ANN/Keras.
- HistGradientBoosting nếu cấu hình có seed/random_state.
- Decision Tree nếu có random_state.

Không cần chạy lặp lại:

- Logistic Regression nếu deterministic.
- SVM nếu deterministic.
- KNN.
- Rule-based Baseline.

Giữ nguyên:

- Train P01-P05.
- External P06-P07.
- Feature set theo cấu hình đại diện của từng thuật toán.
- Threshold 0.50.

Xuất:

`reports/results/full_protocol_repeatability_mean_std.csv`

Metric cần tính trung bình và độ lệch chuẩn:

- Accuracy.
- Precision Incorrect.
- Recall Incorrect.
- F1 Incorrect.
- MCC.
- FP.
- FN.

Không dùng kết quả trung bình nhiều seed để chọn lại model hoặc chọn lại threshold trên external.

## 10. Script đề nghị tạo hoặc cập nhật

Tạo script mới:

`src/32_prepare_chapter4_benchmark_artifacts.py`

Script này nên:

1. Đọc `full_protocol_model_benchmark_external_p06p07.csv`.
2. Đọc `full_protocol_threshold_sweep_external_p06p07.csv`.
3. Kiểm tra dataset split từ CSV gốc.
4. Tạo `full_protocol_best_by_algorithm_default_threshold.csv`.
5. Tạo Hình 4.2 đúng threshold 0.50.
6. Tạo metric riêng HGB threshold 0.76.
7. Tạo Hình 4.3 threshold sweep cho HGB.
8. Tạo Hình 4.4 confusion matrix cho HGB.
9. Phân tích MLPClassifier và Rule-based Baseline Recall 100%.
10. Chạy hoặc đọc kết quả repeatability nhiều seed.
11. Tạo report tổng hợp.

Nếu repeatability nhiều seed mất thời gian, có thể tách script phụ:

`src/33_repeatability_benchmark_seeds.py`

Nhưng report cuối vẫn phải gom kết quả.

## 11. Report tổng hợp cần tạo

Tạo:

`reports/FULL_PROTOCOL_BENCHMARK_FINAL_REVIEW.md`

Report gồm:

1. Dataset split và leakage check.
2. Danh sách feature set và thuật toán.
3. Bảng đầy đủ tất cả cấu hình.
4. Bảng cấu hình đại diện tại threshold 0.50.
5. Kết quả trung bình ± độ lệch chuẩn của các mô hình ngẫu nhiên.
6. Phân tích HGB sau hiệu chỉnh ngưỡng 0.76.
7. Phân tích MLPClassifier và Rule-based Baseline có Recall 100%.
8. Danh sách file CSV và hình đã xuất.
9. Caption và đoạn mô tả có thể đưa trực tiếp vào luận văn.
10. Xác nhận không thay đổi app registry, SQLite hoặc giao diện.

## 12. Kiểm tra cuối

Trước khi báo hoàn thành, kiểm tra:

- [ ] `full_protocol_best_by_algorithm_default_threshold.csv` có đủ 9 dòng thuật toán.
- [ ] Hình 4.2 không chứa HGB threshold 0.76.
- [ ] Hình 4.2 không có chữ `Model được chọn`.
- [ ] Hình 4.2 không có viền đỏ.
- [ ] Hình 4.2 dùng thang màu 0-100.
- [ ] Các số trong Hình 4.2 khớp CSV nguồn.
- [ ] HGB threshold 0.76 nằm ở phần riêng.
- [ ] Có cảnh báo học thuật về threshold 0.76 không phải blind external test hoàn toàn.
- [ ] Có phân tích Recall 100% của MLPClassifier và Rule-based.
- [ ] Có repeatability mean ± std hoặc ghi rõ nếu chưa chạy được.
- [ ] Không cập nhật app registry.
- [ ] Không sửa SQLite.
- [ ] Không sửa giao diện app.
- [ ] Không có mojibake trong report/hình.

## 13. Lệnh chạy dự kiến

```powershell
cd D:\posture_detection_app
.\.venv\Scripts\activate
python src\32_prepare_chapter4_benchmark_artifacts.py
```

Nếu tách repeatability:

```powershell
python src\33_repeatability_benchmark_seeds.py
python src\32_prepare_chapter4_benchmark_artifacts.py
```

