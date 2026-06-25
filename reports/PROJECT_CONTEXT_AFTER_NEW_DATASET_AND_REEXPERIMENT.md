# Project Context After New Dataset and Re-Experiment

File này dùng để cung cấp ngữ cảnh cho ChatGPT Plus hoặc người hỗ trợ khác. Nội dung tóm tắt những thay đổi quan trọng của dự án sau khi bổ sung dataset mới, rebuild CSV, train/evaluate lại model và cập nhật app desktop.

## 1. Thông Tin Đề Tài

Tên đề tài:

> Xây dựng ứng dụng phát hiện lỗi tư thế làm việc qua webcam sử dụng Computer Vision.

Hướng nghiên cứu phù hợp:

> Existing model + new dataset/features.

Không claim mô hình AI hoàn toàn mới. Không claim state-of-the-art. Trọng tâm là ứng dụng MediaPipe Pose, xây dựng dataset/feature, benchmark nhiều mô hình và triển khai desktop app realtime.

## 2. Pipeline Kỹ Thuật Hiện Tại

Pipeline tổng quát:

```text
Webcam/IP camera/video MP4
-> OpenCV frame capture
-> MediaPipe Pose
-> 33 pose landmarks
-> Feature extraction
-> Model inference
-> Temporal smoothing
-> Warning/cooldown
-> SQLite logging
-> Statistics dashboard
```

Thư viện chính:

- Python
- OpenCV
- MediaPipe Pose
- TensorFlow/Keras
- Scikit-learn
- CustomTkinter
- SQLite

App desktop hiện có:

- Mở webcam, IP camera hoặc video MP4.
- Hiển thị skeleton overlay.
- Có ANN mode.
- Có Rule-based Baseline.
- Có 2 mode HistGradientBoosting mới:
  - `HistGradientBoosting (balanced best)`
  - `HistGradientBoosting (high recall demo)`
- Có cảnh báo âm thanh.
- Có smoothing xác suất.
- Có cooldown cảnh báo.
- Có lưu lịch sử SQLite.
- Có dashboard thống kê.
- Có light/dark mode.

## 3. Dataset Sau Khi Bổ Sung Người Mới

Trước đây external có P01, nhưng vì P01 đã xuất hiện trong dataset gốc nên external P01 đã được chuyển vào raw/train. Sau đó bổ sung 23 video mới từ P06 và P07 để làm external test người mới.

Split hiện tại:

| Split | Videos | Participants | Correct videos | Incorrect videos | Mục đích |
|---|---:|---|---:|---:|---|
| Raw/development | 94 | P01-P05 | 39 | 55 | Train/model selection |
| External unseen-participant | 23 | P06-P07 | 11 | 12 | Final external test trên người mới |

CSV đã trích xuất:

| File | Shape | Participants | Label distribution |
|---|---:|---|---|
| `dataset/processed/posture_data_2fps_with_metadata.csv` | 12680 x 108 | P01-P05 | Correct: 5206, Incorrect: 7474 |
| `dataset/processed/posture_external_test_2fps_with_metadata.csv` | 4556 x 108 | P06-P07 | Correct: 2001, Incorrect: 2555 |
| `dataset/posture_data_2fps.csv` | 12680 x 100 | no metadata | Correct: 5206, Incorrect: 7474 |
| `dataset/posture_external_test_2fps.csv` | 4556 x 100 | no metadata | Correct: 2001, Incorrect: 2555 |
| `dataset/processed/posture_data_2fps_ergonomic_features.csv` | 12680 x 23 | P01-P05 | Correct: 5206, Incorrect: 7474 |
| `dataset/processed/posture_external_test_2fps_ergonomic_features.csv` | 4556 x 23 | P06-P07 | Correct: 2001, Incorrect: 2555 |
| `dataset/processed/posture_data_2fps_combined_features.csv` | 12680 x 122 | P01-P05 | Correct: 5206, Incorrect: 7474 |
| `dataset/processed/posture_external_test_2fps_combined_features.csv` | 4556 x 122 | P06-P07 | Correct: 2001, Incorrect: 2555 |
| `dataset/processed/posture_data_2fps_ergonomic_v2_features.csv` | 12680 x 40 | P01-P05 | Correct: 5206, Incorrect: 7474 |
| `dataset/processed/posture_external_test_2fps_ergonomic_v2_features.csv` | 4556 x 40 | P06-P07 | Correct: 2001, Incorrect: 2555 |
| `dataset/processed/posture_data_2fps_combined_v2_features.csv` | 12680 x 139 | P01-P05 | Correct: 5206, Incorrect: 7474 |
| `dataset/processed/posture_external_test_2fps_combined_v2_features.csv` | 4556 x 139 | P06-P07 | Correct: 2001, Incorrect: 2555 |

Quan trọng:

- P06/P07 không được đưa vào train nếu vẫn dùng P06/P07 làm external unseen test.
- External hiện tại có ý nghĩa học thuật tốt hơn external cũ vì là người mới chưa xuất hiện trong train.

## 4. Các Nhóm Đặc Trưng Hiện Có

### 4.1 Raw 99

33 MediaPipe landmarks x 3 tọa độ:

```text
landmark_0_x, landmark_0_y, landmark_0_z, ..., landmark_32_x, landmark_32_y, landmark_32_z
```

### 4.2 Normalized 99

Landmark được chuẩn hóa theo shoulder midpoint và body scale. Mục tiêu là giảm ảnh hưởng vị trí/người/camera.

### 4.3 Ergonomic 14

Các đặc trưng hình học/ergonomic ban đầu:

- `shoulder_y_diff`
- `shoulder_tilt_angle`
- `torso_lean_angle`
- `head_offset_x`
- `nose_to_shoulder_y`
- `nose_shoulder_clearance_ratio`
- `neck_compression_detected`
- `left_hand_mouth_ratio`
- `right_hand_mouth_ratio`
- `chin_rest_detected`
- `shoulder_width`
- `torso_length`
- `head_shoulder_distance`
- `min_hand_mouth_ratio`

### 4.4 Ergonomic v2 with view

Bổ sung các feature mới:

- quan hệ tai-vai;
- tỷ lệ ngang mũi/tai/vai;
- head-forward ratio;
- góc cổ-vai;
- góc đầu-cổ-thân;
- độ thẳng hàng vai-hông;
- độ nghiêng thân theo góc nhìn bên;
- one-hot view angle: `view_front`, `view_side_30`, `view_side_90`, `view_unknown`.

Feature set quan trọng hiện tại:

```text
ergonomic_v2_with_view
```

## 5. Rebuild Dataset Và Benchmark Sau Khi Thêm P06/P07

Task đã thực hiện:

- `20_TASK_REBUILD_DATASET_P01_TRAIN_P06P07_EXTERNAL_BENCHMARK.md`
- `21_TASK_CAI_THIEN_MODEL_GIAM_FALSE_POSITIVE_TANG_DO_CHINH_XAC.md`
- `22_TASK_TRAIN_ANN_LOCAL_TREN_CSV_MOI.md`
- `23_TASK_CAP_NHAT_APP_HGB_BEST_DUNG_MODEL_MOI.md`

Backup quan trọng:

- `outputs/backups/rebuild_dataset_p06_p07_20260625_024450`
- `outputs/backups/model_improvement_fp_reduction_20260625_115515`
- `outputs/backups/ann_before_local_rebuild_20260625_135916`

## 6. Kết Quả Model Sau Rebuild Dataset

### 6.1 Model HGB ban đầu sau rebuild

Sau khi rebuild dataset P01-P05 train và P06/P07 external, model tốt nhất ban đầu là:

```text
random_forest__ergonomic_14
```

External P06/P07:

| Model | Feature set | Threshold | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC | FP | FN |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| random_forest__ergonomic_14 | ergonomic_14 | 0.50 | 82.16% | 79.47% | 91.94% | 85.25% | 0.6405 | 607 | 206 |

Vấn đề chính:

- FP cao, đặc biệt trên các video Correct ở góc `side_90` và `side_30`.

### 6.2 Model cải thiện sau task 21

Sau khi bổ sung feature ergonomic v2 và view-aware feature, model tốt nhất tổng thể là:

```text
hist_gradient_boosting__ergonomic_v2_with_view
```

External P06/P07:

| Model | Feature set | Threshold | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC | FP | FN |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| hist_gradient_boosting__ergonomic_v2_with_view | ergonomic_v2_with_view | 0.76 | 89.31% | 93.48% | 87.01% | 90.13% | 0.7875 | 155 | 332 |

So với baseline sau rebuild:

- Accuracy tăng từ 82.16% lên 89.31%.
- F1 Incorrect tăng từ 85.25% lên 90.13%.
- MCC tăng từ 0.6405 lên 0.7875.
- FP giảm từ 607 xuống 155.
- FN tăng từ 206 lên 332.

Cách hiểu:

- Model mới tốt hơn tổng thể.
- Model mới giảm báo nhầm tư thế đúng thành sai.
- Đánh đổi là bỏ sót thêm một số frame tư thế sai.

## 7. HGB Cũ Và HGB Mới Khác Nhau Như Thế Nào?

App trước đây hard-code model HGB cũ:

```text
hist_gradient_boosting__normalized_99
```

So sánh trên external P06/P07:

| Model | Feature set | Threshold | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC | FP | FN |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| HGB cũ high recall | normalized_99 | 0.50 | 67.38% | 63.62% | 97.69% | 77.06% | 0.3785 | 1427 | 59 |
| HGB mới balanced best | ergonomic_v2_with_view | 0.76 | 89.31% | 93.48% | 87.01% | 90.13% | 0.7875 | 155 | 332 |

Kết luận:

- HGB mới tốt hơn để báo cáo khoa học vì cân bằng hơn và tổng thể tốt hơn.
- HGB cũ có Recall Incorrect cao hơn, nên ít bỏ sót tư thế sai hơn khi demo realtime.
- Vì vậy app đã tách thành 2 mode HGB:
  - `HistGradientBoosting (balanced best)`
  - `HistGradientBoosting (high recall demo)`

## 8. Kết Quả Train Lại ANN Local

Task 22 đã train ANN local trên CSV mới bằng máy local, không dùng Kaggle.

Các ANN đã train:

- `ann_raw_99`
- `ann_normalized_99`
- `ann_ergonomic_v2_with_view`

ANN cũ trong app:

- `models/ann_best.keras`
- `models/scaler.pkl`
- Đây là model cũ, chưa phù hợp dataset mới.

ANN tốt nhất sau khi train lại:

```text
ann_normalized_99_balanced
```

External P06/P07:

| Model | Feature set | Threshold | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC | FP | FN |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ANN cũ app | raw_99 | 0.30 | 59.17% | 62.21% | 69.28% | 65.56% | 0.1594 | 1075 | 785 |
| ANN mới tốt nhất | normalized_99 | 0.55 | 79.10% | 88.63% | 71.98% | 79.44% | 0.5997 | 236 | 716 |
| HGB balanced best | ergonomic_v2_with_view | 0.76 | 89.31% | 93.48% | 87.01% | 90.13% | 0.7875 | 155 | 332 |

Kết luận:

- ANN mới cải thiện so với ANN cũ.
- ANN vẫn kém HGB balanced best.
- Không nên dùng ANN làm model chính trong demo.
- ANN nên được trình bày là baseline neural network hoặc mô hình tích hợp ban đầu.

## 9. Vấn Đề Với Luận Văn Đang Viết ANN Là Mô Hình Chính

Luận văn ban đầu đề cập ANN là mô hình chính. Sau khi thực nghiệm mới, nên sửa cách diễn đạt:

Không nên viết:

> ANN là mô hình tốt nhất/chính duy nhất của hệ thống.

Nên viết:

> ANN/Keras là mô hình học máy tích hợp ban đầu trong ứng dụng desktop và được sử dụng như baseline neural network. Sau khi mở rộng dataset và đánh giá trên external P06/P07, luận văn benchmark thêm nhiều mô hình học máy. Kết quả cho thấy HistGradientBoosting với đặc trưng ergonomic_v2_with_view đạt hiệu quả tổng thể tốt hơn ANN. Vì vậy HGB được chọn làm mô hình khuyến nghị cho phiên bản cải thiện, còn ANN giữ vai trò baseline neural network.

Cách nói khi hội đồng hỏi:

> Ban đầu em dùng ANN làm mô hình chính vì kiến trúc đơn giản và dễ tích hợp. Sau khi bổ sung dữ liệu mới và đánh giá nghiêm ngặt hơn trên người chưa thấy, em nhận thấy ANN chưa tổng quát tốt bằng HistGradientBoosting. Vì vậy em mở rộng thực nghiệm, benchmark nhiều mô hình và chọn HGB làm mô hình triển khai khuyến nghị. Đây là một phần kết quả nghiên cứu của đề tài.

## 10. Cập Nhật App Sau Task 23

File đã sửa:

- `src/4_main_desktop_app.py`

Mode hiện tại trong app:

| Mode | Vai trò |
|---|---|
| `ANN` | Baseline neural network/tích hợp ban đầu |
| `HistGradientBoosting (balanced best)` | Model tốt nhất tổng thể, dùng cho kết quả khoa học |
| `HistGradientBoosting (high recall demo)` | Model ưu tiên phát hiện sai tư thế, dùng cho demo realtime |
| `Rule-based Baseline` | Baseline giải thích được |

Logic HGB hiện tại:

- App load model theo mode.
- App đọc threshold từ `threshold.json`.
- App dùng `build_feature_matrix()` thay vì chỉ tạo `normalized_99` thủ công.
- HGB mode không dùng nhầm ô `Ngưỡng sai sau làm mượt` làm threshold model.
- Video file suy ra `view_angle` từ tên file:
  - `front`
  - `side_30`
  - `side_90`
  - nếu không có thì `unknown`
- Webcam/IP camera tạm dùng `view_unknown`.

Threshold thật:

| Mode | Threshold dùng thật |
|---|---:|
| `HistGradientBoosting (balanced best)` | 0.76 |
| `HistGradientBoosting (high recall demo)` | 0.50 |
| `ANN` | dùng ô `Ngưỡng sai sau làm mượt` |

Ô `Ngưỡng sai sau làm mượt` trong GUI:

- Không còn quyết định đúng/sai cho HGB.
- Vẫn có tác dụng với ANN.
- Với HGB, quyết định đúng/sai dùng threshold riêng của model.

## 11. Khuyến Nghị Demo Hội Đồng

Nếu demo realtime bằng webcam:

- Nên chọn `HistGradientBoosting (high recall demo)`.
- Lý do: ưu tiên không bỏ sót tư thế sai khi người demo cố tình sai tư thế.

Nếu trình bày kết quả khoa học:

- Nên dùng `HistGradientBoosting (balanced best)`.
- Lý do: metric tổng thể tốt hơn, FP thấp hơn nhiều, phù hợp external evaluation.

Cách giải thích:

> Trong demo realtime, em chọn chế độ high recall để hệ thống nhạy với tư thế sai và hạn chế bỏ sót cảnh báo. Trong đánh giá khoa học, em sử dụng chế độ balanced best vì mô hình này cân bằng tốt hơn giữa phát hiện sai tư thế và tránh báo nhầm tư thế đúng.

## 12. Các Trường Hợp Hội Đồng Có Thể Hỏi

### 12.1 Nếu có nhiều người trong khung hình thì sao?

Trả lời:

> Phiên bản hiện tại tập trung vào một người dùng ngồi trước webcam. MediaPipe Pose đang dùng ở chế độ single-person, nên khi có nhiều người trong khung hình, hệ thống chỉ nhận một pose nổi bật nhất, thường là người rõ nhất hoặc gần trung tâm hơn. Vì vậy ứng dụng khuyến nghị chỉ có một người trong vùng camera khi sử dụng. Hướng phát triển là dùng multi-person pose estimation hoặc phát hiện người trước, sau đó chọn người có bounding box lớn nhất/gần trung tâm nhất.

### 12.2 Nếu mặt/đầu quá sát camera thì sao?

Trả lời:

> Hệ thống cần thấy rõ tối thiểu đầu, vai và một phần thân trên để tính đặc trưng tư thế. Nếu người dùng đưa mặt quá sát camera khiến vai hoặc thân bị cắt khỏi khung hình, đây là điều kiện đầu vào không đạt yêu cầu. Phiên bản hiện tại có thể không phát hiện đủ pose hoặc dự đoán không ổn định. Hướng phát triển là thêm module kiểm tra chất lượng frame, ví dụ phát hiện vai quá lớn, cơ thể bị cắt khung hoặc landmark thiếu, rồi cảnh báo người dùng lùi ra xa camera.

### 12.3 Vì sao không dùng ANN làm model chính nữa?

Trả lời:

> ANN là mô hình tích hợp ban đầu và được giữ làm baseline neural network. Tuy nhiên, khi đánh giá trên external P06/P07, ANN mới tốt nhất chỉ đạt F1 Incorrect 79.44%, trong khi HGB balanced đạt 90.13%. Vì vậy luận văn chọn HGB làm mô hình khuyến nghị sau benchmark. Đây là kết quả thực nghiệm, không phải thay đổi tùy ý.

### 12.4 Vì sao có 2 chế độ HGB?

Trả lời:

> Hai chế độ phục vụ hai mục tiêu khác nhau. Balanced best dùng cho báo cáo khoa học vì kết quả tổng thể tốt hơn và giảm báo nhầm. High recall demo dùng khi trình diễn realtime vì ưu tiên phát hiện sai tư thế, giảm bỏ sót cảnh báo.

### 12.5 Dataset có đủ lớn chưa?

Trả lời:

> Dataset hiện tại đủ để xây dựng prototype và đánh giá bước đầu: 94 video train/development từ P01-P05 và 23 video external từ P06-P07. Tuy nhiên, để khái quát tốt hơn cần mở rộng thêm người tham gia, môi trường, góc quay, điều kiện ánh sáng và benchmark thêm public dataset.

## 13. Những File Báo Cáo Quan Trọng Hiện Có

- `reports/REBUILD_DATASET_P01_TRAIN_P06P07_EXTERNAL_REPORT.md`
- `reports/MODEL_IMPROVEMENT_FP_REDUCTION_REPORT.md`
- `reports/ANN_LOCAL_REBUILD_REPORT.md`
- `reports/APP_HGB_MODE_UPDATE_REPORT.md`
- `reports/FINAL_EVALUATION_REPORT.md`
- `reports/MODEL_SELECTION_REPORT.md`
- `reports/FEATURE_SCHEMA_FINAL.md`
- `reports/EXPERIMENT_PROTOCOL_FINAL.md`

## 14. Những File Code Quan Trọng

- `src/4_main_desktop_app.py`
- `src/2_extract_features.py`
- `src/16_build_ergonomic_features.py`
- `src/21_train_model_registry.py`
- `src/22_calibrate_threshold.py`
- `src/23_final_evaluation_protocol.py`
- `src/27_model_improvement_fp_reduction.py`
- `src/28_train_ann_local_rebuild.py`
- `src/feature_schema.py`
- `src/model_registry_service.py`

## 15. Những Model Quan Trọng

ANN cũ:

- `models/ann_best.keras`
- `models/scaler.pkl`

ANN train lại local:

- `models/local_training_rebuild/ann_raw_99.keras`
- `models/local_training_rebuild/ann_normalized_99.keras`
- `models/local_training_rebuild/ann_ergonomic_v2_with_view.keras`

HGB high recall demo:

- `models/registry/hist_gradient_boosting__normalized_99/model.pkl`
- `models/registry/hist_gradient_boosting__normalized_99/threshold.json`

HGB balanced best:

- `models/registry/hist_gradient_boosting__ergonomic_v2_with_view/model.pkl`
- `models/registry/hist_gradient_boosting__ergonomic_v2_with_view/threshold.json`

## 16. Cách Viết Lại Luận Văn Sau Thay Đổi

Không nên xóa ANN, mà đổi vai trò:

- ANN: mô hình tích hợp ban đầu, baseline neural network.
- HGB: mô hình được chọn sau benchmark vì kết quả tốt hơn trên external test.
- Rule-based: baseline giải thích được.

Chương 4 nên là chương sửa nhiều nhất:

1. Mô tả dataset mới.
2. Mô tả protocol train P01-P05, test P06-P07.
3. So sánh ANN cũ, ANN mới, HGB cũ, HGB mới.
4. Phân tích FP/FN, video-wise, participant-wise.
5. Giải thích vì sao chọn HGB balanced cho báo cáo và HGB high recall cho demo.

Một đoạn nên dùng:

> Ban đầu hệ thống sử dụng ANN/Keras làm mô hình phân loại chính do kiến trúc đơn giản và dễ tích hợp vào ứng dụng desktop. Tuy nhiên, sau khi mở rộng dataset và bổ sung tập kiểm thử external trên người chưa xuất hiện trong tập huấn luyện, luận văn tiến hành benchmark thêm nhiều mô hình học máy nhẹ. Kết quả cho thấy HistGradientBoosting với nhóm đặc trưng ergonomic_v2_with_view đạt hiệu quả tổng thể tốt hơn ANN trên tập external. Vì vậy, ANN được giữ như một baseline neural network, còn HistGradientBoosting được đề xuất là mô hình triển khai tốt hơn cho phiên bản cải thiện của hệ thống.

## 17. Tóm Tắt Một Câu

Sau khi thêm dataset P06/P07 và thực nghiệm lại, dự án đã chuyển từ app chỉ nhấn mạnh ANN sang một hệ thống có benchmark rõ ràng: ANN là baseline neural network, còn HistGradientBoosting với feature ergonomic_v2_with_view là model tốt nhất tổng thể cho báo cáo, đồng thời app có thêm mode HGB high recall để demo realtime ít bỏ sót tư thế sai.

