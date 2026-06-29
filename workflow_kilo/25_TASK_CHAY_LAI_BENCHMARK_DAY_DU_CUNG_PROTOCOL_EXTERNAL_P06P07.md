# 25. TASK - Chạy lại benchmark đầy đủ trên cùng protocol external P06-P07

## 1. Bối cảnh

Sau khi cập nhật dataset mới, dự án hiện có:

- Tập phát triển/training: 94 video, người tham gia P01-P05.
- Tập external mới: 23 video, người tham gia P06-P07.
- Các kết quả gần đây mới tập trung vào một số cấu hình đại diện như HistGradientBoosting, Random Forest, ANN/Keras và một số cấu hình threshold.

Để bài luận văn và bài báo khoa học có tính kiểm chứng tốt hơn, cần chạy lại benchmark đầy đủ các thuật toán đã liệt kê trên cùng một giao thức thực nghiệm.

## 2. Mục tiêu

Chạy lại, so sánh và báo cáo đầy đủ các nhóm thuật toán sau trên cùng một tập external P06-P07:

1. Logistic Regression.
2. SVM.
3. KNN.
4. Decision Tree.
5. Random Forest.
6. MLPClassifier.
7. ANN/Keras.
8. HistGradientBoosting.
9. Rule-based Baseline.

Nguyên tắc chính:

- Các mô hình học máy phải được train trên tập phát triển P01-P05.
- Tập external P06-P07 chỉ dùng để đánh giá cuối cùng.
- Rule-based Baseline không train, chỉ chạy trực tiếp trên cùng tập external để so sánh.
- Không dùng dữ liệu P06-P07 để huấn luyện hoặc chọn mô hình nếu đang báo cáo theo nghĩa external test độc lập.

## 3. Câu trả lời phương pháp luận cần thống nhất

Nếu được hỏi "có cần train trước rồi mới test external không?", câu trả lời là:

> Có. Với các thuật toán học máy như Logistic Regression, SVM, KNN, Decision Tree, Random Forest, MLPClassifier, ANN/Keras và HistGradientBoosting, mô hình cần được huấn luyện trên tập phát triển P01-P05 trước. Sau đó mô hình đã huấn luyện mới được chạy đánh giá trên tập external P06-P07 để kiểm tra khả năng tổng quát trên người mới. Riêng rule-based baseline không cần train vì nó là bộ luật thủ công, nên chỉ cần chạy trực tiếp trên tập external.

## 4. File dữ liệu đầu vào

Ưu tiên dùng các file hiện có sau:

- `dataset/processed/posture_data_2fps_with_metadata.csv`
- `dataset/processed/posture_external_test_2fps_with_metadata.csv`
- `dataset/processed/posture_data_2fps_with_metadata_ergonomic_v2_features.csv` nếu có.
- `dataset/processed/posture_external_test_2fps_with_metadata_ergonomic_v2_features.csv` nếu có.
- `dataset/processed/posture_data_2fps_with_metadata_combined_v2_features.csv` nếu có.
- `dataset/processed/posture_external_test_2fps_with_metadata_combined_v2_features.csv` nếu có.

Nếu file đặc trưng v2 chưa có hoặc không khớp số dòng với CSV gốc, phải trích xuất/tạo lại đặc trưng trước khi benchmark.

## 5. Kiểm tra chống rò rỉ dữ liệu

Trước khi train, phải kiểm tra:

- Tập train/development chỉ có `participant_id` thuộc P01-P05.
- Tập external chỉ có `participant_id` thuộc P06-P07.
- Không có `source_video` trùng giữa train và external.
- Không có video external bị đưa nhầm vào tập train.
- Không shuffle gộp train và external rồi chia frame-level ngẫu nhiên.

Xuất kết quả kiểm tra vào báo cáo.

## 6. Nhóm đặc trưng cần benchmark

Chạy ít nhất các nhóm đặc trưng sau:

1. `raw_99`: 33 MediaPipe Pose landmarks x 3 tọa độ.
2. `normalized_99`: 99 đặc trưng landmark đã chuẩn hóa theo cơ thể.
3. `ergonomic_14`: nhóm đặc trưng hình học/ergonomic cũ.
4. `ergonomic_v2`: nhóm đặc trưng ergonomic cải tiến.
5. `ergonomic_v2_with_view`: ergonomic v2 có thêm thông tin góc nhìn/camera nếu đã có trong project.

Nếu thời gian cho phép, chạy thêm:

6. `combined_v2`: normalized landmarks + ergonomic v2.
7. `combined_v2_with_view`: normalized landmarks + ergonomic v2 + thông tin góc nhìn/camera.

## 7. Quy tắc tiền xử lý

Áp dụng nhất quán:

- Logistic Regression, SVM, KNN, MLPClassifier và ANN/Keras phải dùng scaler.
- Decision Tree, Random Forest và HistGradientBoosting không bắt buộc dùng scaler.
- Thiếu landmark hoặc giá trị NaN phải được xử lý giống nhau giữa train và external.
- Label phải thống nhất:
  - Correct posture = 0.
  - Incorrect posture = 1.
- Với các mô hình có xác suất, xác suất cần hiểu là xác suất thuộc lớp Incorrect posture.

## 8. Thuật toán cần train và đánh giá

### 8.1. Logistic Regression

- Train trên từng nhóm đặc trưng.
- Dùng `class_weight="balanced"` nếu dữ liệu lệch lớp.
- Báo cáo threshold mặc định 0.50.
- Nếu sweep threshold, ghi rõ là kết quả sau hiệu chỉnh ngưỡng.

### 8.2. SVM

- Dùng SVM RBF là cấu hình chính.
- Nếu chạy thêm Linear SVM thì ghi là phụ.
- Cần scaling.
- Nếu dùng `probability=True`, ghi nhận thời gian train có thể lâu hơn.

### 8.3. KNN

- Chạy ít nhất `n_neighbors` trong một cấu hình hợp lý, ví dụ 3, 5, 7.
- Cần scaling.
- Chọn cấu hình tốt nhất theo validation nội bộ nếu có, không chọn trực tiếp theo external nếu muốn báo cáo external độc lập.

### 8.4. Decision Tree

- Chạy baseline cây đơn.
- Có thể giới hạn `max_depth` để tránh overfit.
- Báo cáo cả default và cấu hình hạn chế độ sâu nếu cần.

### 8.5. Random Forest

- Chạy lại trên cùng protocol mới.
- Ghi rõ số cây, random state, class weight nếu dùng.

### 8.6. MLPClassifier

- Đây là MLP của scikit-learn, khác với ANN/Keras.
- Cần scaling.
- Ghi rõ kiến trúc hidden layers, max_iter, random_state.

### 8.7. ANN/Keras

- Train lại local trên dataset mới P01-P05.
- Không dùng lại model ANN cũ nếu model đó train trên dataset cũ.
- Kiến trúc ưu tiên giữ theo luận văn:
  - Dense 128
  - BatchNorm
  - Dropout
  - Dense 64
  - BatchNorm
  - Dropout
  - Dense 32
  - Dropout
  - Dense 1 sigmoid
- Lưu model, scaler, threshold và metrics riêng để truy vết.

### 8.8. HistGradientBoosting

- Chạy lại trên cùng protocol.
- Chạy ít nhất cấu hình `ergonomic_v2_with_view`.
- Báo cáo threshold mặc định 0.50 và threshold cân bằng nếu có hiệu chỉnh.

### 8.9. Rule-based Baseline

- Không train.
- Chạy trực tiếp trên tập external P06-P07.
- Dùng cùng logic rule-based đang có trong app hoặc script thực nghiệm.
- Báo cáo cùng metric với các mô hình học máy.

## 9. Protocol đánh giá

Chạy theo hai lớp báo cáo:

### 9.1. External test mặc định

Đây là bảng chính nên đưa vào luận văn.

- Train: P01-P05.
- Test: P06-P07.
- Threshold:
  - 0.50 cho các mô hình xác suất nếu chưa hiệu chỉnh.
  - Rule-based dùng logic ngưỡng nội tại của rule.

### 9.2. Threshold sweep/threshold calibration

Đây là phân tích bổ sung.

- Chạy sweep threshold từ 0.05 đến 0.95 hoặc khoảng phù hợp.
- Báo cáo:
  - threshold tối ưu cân bằng F1/MCC.
  - threshold ưu tiên Recall Incorrect.
  - threshold giảm False Positive.
- Nếu threshold được chọn bằng external set, phải ghi rõ là "external-calibrated analysis", không gọi là blind external test.
- Nếu có thể, chọn threshold bằng validation nội bộ từ P01-P05 rồi chỉ test một lần trên P06-P07.

## 10. Metric cần xuất

Với từng model + feature set + threshold, cần có:

- Accuracy.
- Precision cho lớp Incorrect posture.
- Recall cho lớp Incorrect posture.
- F1-score cho lớp Incorrect posture.
- Macro-F1.
- MCC.
- ROC-AUC nếu mô hình có score/probability.
- PR-AUC nếu mô hình có score/probability.
- TN.
- FP.
- FN.
- TP.
- Train time nếu đo được.
- Predict time nếu đo được.
- Số mẫu test.

## 11. Phân tích theo video và theo người

Ngoài frame-level metrics, cần xuất thêm:

- Video-wise report:
  - source_video.
  - participant_id.
  - label thật của video.
  - số frame.
  - số frame dự đoán Correct.
  - số frame dự đoán Incorrect.
  - tỷ lệ Incorrect trung bình.
  - nhãn majority vote theo video.
  - đúng/sai ở mức video.

- Participant-wise report:
  - P06.
  - P07.
  - Accuracy.
  - Precision Incorrect.
  - Recall Incorrect.
  - F1 Incorrect.
  - FP.
  - FN.

## 12. File script đề nghị tạo hoặc cập nhật

Tạo script mới nếu chưa có:

- `src/30_full_protocol_external_benchmark.py`

Script nên làm các việc:

1. Load train CSV và external CSV.
2. Kiểm tra split P01-P05/P06-P07.
3. Build/load feature groups.
4. Train từng thuật toán trên từng feature group.
5. Evaluate trên external.
6. Chạy rule-based baseline trên external.
7. Chạy threshold sweep cho mô hình có probability/score.
8. Xuất CSV kết quả.
9. Xuất hình so sánh.
10. Xuất báo cáo Markdown.

## 13. File kết quả cần tạo

Tạo thư mục nếu chưa có:

- `reports/results/`
- `reports/figures/`
- `models/full_protocol_benchmark/`

Xuất các file:

- `reports/results/full_protocol_model_benchmark_external_p06p07.csv`
- `reports/results/full_protocol_threshold_sweep_external_p06p07.csv`
- `reports/results/full_protocol_predictions_external_p06p07.csv`
- `reports/results/full_protocol_rule_based_external_p06p07.csv`
- `reports/results/full_protocol_video_wise_external_p06p07.csv`
- `reports/results/full_protocol_participant_wise_external_p06p07.csv`
- `reports/figures/full_protocol_model_comparison_bar.png`
- `reports/figures/full_protocol_confusion_matrix_best.png`
- `reports/figures/full_protocol_threshold_sweep_best.png`
- `reports/FULL_PROTOCOL_MODEL_BENCHMARK_EXTERNAL_P06P07_REPORT.md`

Nếu có lưu model:

- `models/full_protocol_benchmark/<model_id>/model.pkl`
- `models/full_protocol_benchmark/<model_id>/scaler.pkl` nếu có.
- `models/full_protocol_benchmark/<model_id>/metrics.json`
- `models/full_protocol_benchmark/<model_id>/feature_schema.json`
- `models/full_protocol_benchmark/<model_id>/threshold.json`

## 14. Nội dung báo cáo Markdown cần có

File `reports/FULL_PROTOCOL_MODEL_BENCHMARK_EXTERNAL_P06P07_REPORT.md` phải gồm:

1. Mục tiêu benchmark.
2. Dataset split.
3. Kiểm tra chống data leakage.
4. Danh sách thuật toán và feature groups.
5. Protocol train/test.
6. Bảng benchmark đầy đủ.
7. Bảng top model theo F1 Incorrect.
8. Bảng top model theo MCC.
9. Bảng top model giảm False Positive.
10. Bảng top model giảm False Negative.
11. Kết quả Rule-based Baseline.
12. Kết quả ANN/Keras.
13. Kết quả HistGradientBoosting.
14. Phân tích theo video.
15. Phân tích theo người P06/P07.
16. Nhận xét chọn model cho demo app.
17. Nhận xét chọn model cho luận văn/bài báo.
18. Những hạn chế còn lại.
19. Cách cập nhật lại bảng/hình trong luận văn.

## 15. Hình và bảng cần phục vụ luận văn

Sau khi chạy xong, đề xuất cập nhật luận văn:

- Bảng benchmark đầy đủ:
  - Logistic Regression.
  - SVM.
  - KNN.
  - Decision Tree.
  - Random Forest.
  - MLPClassifier.
  - ANN/Keras.
  - HistGradientBoosting.
  - Rule-based Baseline.

- Hình so sánh metric:
  - Accuracy.
  - Precision Incorrect.
  - Recall Incorrect.
  - F1 Incorrect.

- Nếu bảng quá rộng, luận văn nên dùng:
  - Bảng chính: top cấu hình đại diện của từng thuật toán.
  - Phụ lục: toàn bộ model + feature set + threshold.

## 16. Cách diễn giải nếu chỉ số thấp hơn kỳ vọng

Không được nói số liệu là "ảo" hoặc né tránh. Cách diễn giải nên dùng:

> Kết quả trên external P06-P07 thấp hơn một số kết quả nội bộ vì đây là tập người mới, chưa xuất hiện trong huấn luyện. Ngoài ra, nhãn của video là nhãn cấp video, trong khi người tham gia có thể thay đổi tư thế nhẹ trong từng frame. Vì vậy một số frame có thể không hoàn toàn khớp với nhãn tổng của video, làm tăng FP hoặc FN. Đây là hạn chế thực nghiệm thực tế và cũng cho thấy cần bổ sung annotation chi tiết hơn ở mức frame hoặc đoạn thời gian trong nghiên cứu tiếp theo.

## 17. Tiêu chí hoàn thành

Task được xem là hoàn thành khi:

- Đã train lại đầy đủ các thuật toán học máy trên P01-P05.
- Đã đánh giá tất cả trên external P06-P07.
- Rule-based Baseline đã được đánh giá trên cùng tập external.
- Có CSV benchmark đầy đủ.
- Có báo cáo Markdown tổng hợp.
- Có ít nhất một hình so sánh metric.
- Có confusion matrix của model tốt nhất.
- Có phân tích video-wise và participant-wise.
- Có kết luận rõ model nào phù hợp cho:
  - báo cáo khoa học;
  - luận văn;
  - demo realtime trong app.

## 18. Lệnh chạy dự kiến

Sau khi script được tạo:

```powershell
cd D:\posture_detection_app
.\.venv\Scripts\activate
python src\30_full_protocol_external_benchmark.py
```

Nếu thiếu package, ghi rõ package cần cài và không tự ý thay đổi môi trường nếu chưa cần.

## 19. Lưu ý khi đưa vào luận văn

Không nên chỉ đưa một hình 4 cấu hình nếu mục tiêu là chứng minh đã so sánh nhiều thuật toán. Nên trình bày:

- Một bảng đầy đủ các thuật toán chính.
- Một hình chỉ chọn các cấu hình đại diện để dễ nhìn.
- Một đoạn giải thích vì sao chọn HistGradientBoosting hoặc model tốt nhất.
- Một đoạn giải thích ANN/Keras vẫn có vai trò trong app/luận văn nếu app đang tích hợp ANN, nhưng benchmark cho thấy mô hình khác có thể phù hợp hơn trên external P06-P07.

