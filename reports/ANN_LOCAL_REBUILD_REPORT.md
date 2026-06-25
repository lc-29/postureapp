# Báo Cáo Train ANN Local Trên CSV Mới

Cập nhật: 2026-06-25 14:01:32

Backup ANN cũ: `D:\posture_detection_app\outputs\backups\ann_before_local_rebuild_20260625_135916`

## 1. Mục Tiêu

Train lại ANN/Keras trên máy local bằng CSV mới sau khi rebuild dataset. Tập train/development chỉ gồm P01-P05; tập external P06-P07 chỉ dùng để đánh giá người mới, không đưa vào train.

## 2. Dataset

- Train/development: `dataset/processed/posture_data_2fps_with_metadata.csv`, 12680 mẫu, P01-P05.
- External: `dataset/processed/posture_external_test_2fps_with_metadata.csv`, 4556 mẫu, P06-P07.
- Feature v2: dùng thêm `posture_data_2fps_combined_v2_features.csv` và `posture_external_test_2fps_combined_v2_features.csv`.

## 3. Cấu Hình ANN

Kiến trúc: Dense 128 + BatchNorm + Dropout 0.30, Dense 64 + BatchNorm + Dropout 0.25, Dense 32 + Dropout 0.20, Dense 1 sigmoid. Loss là binary crossentropy, optimizer Adam, EarlyStopping theo validation loss.

## 4. Kết Quả External P06/P07

| model_id | feature_set | class_weight | threshold | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | mcc | false_positive | false_negative |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ann_normalized_99_balanced | normalized_99 | balanced | 0.5500 | 0.7910 | 0.8863 | 0.7198 | 0.7944 | 0.5997 | 236 | 716 |
| ann_raw_99_balanced | raw_99 | balanced | 0.7500 | 0.6499 | 0.6513 | 0.8086 | 0.7215 | 0.2761 | 1106 | 489 |
| ann_raw_99_none | raw_99 | none | 0.7100 | 0.6238 | 0.6271 | 0.8121 | 0.7077 | 0.2175 | 1234 | 480 |
| ann_ergonomic_v2_with_view_balanced | ergonomic_v2_with_view | balanced | 0.3500 | 0.6343 | 0.6590 | 0.7209 | 0.6886 | 0.2494 | 953 | 713 |
| ann_normalized_99_none | normalized_99 | none | 0.3100 | 0.6383 | 0.7027 | 0.6153 | 0.6561 | 0.2809 | 665 | 983 |
| ann_old_app | raw_99 | old_unknown | 0.3000 | 0.5917 | 0.6221 | 0.6928 | 0.6556 | 0.1594 | 1075 | 785 |
| ann_ergonomic_v2_with_view_none | ergonomic_v2_with_view | none | 0.3000 | 0.5386 | 0.6002 | 0.5311 | 0.5635 | 0.0788 | 904 | 1198 |

## 5. So Sánh Với HGB Tốt Nhất Hiện Tại

| model_id | feature_set | threshold | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | mcc | false_positive | false_negative |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ann_normalized_99_balanced | normalized_99 | 0.5500 | 0.7910 | 0.8863 | 0.7198 | 0.7944 | 0.5997 | 236 | 716 |
| hist_gradient_boosting__ergonomic_v2_with_view | ergonomic_v2_with_view | 0.7600 | 0.8931 | 0.9348 | 0.8701 | 0.9013 | 0.7875 | 155 | 332 |

## 6. Model ANN Tốt Nhất

- Model ANN tốt nhất: `ann_normalized_99_balanced`.
- Accuracy: 79.10%.
- F1 Incorrect: 79.44%.
- MCC: 0.5997.
- FP: 236; FN: 716.

Kết luận cập nhật app: Không nên thay HGB làm model chính. ANN mới có thể dùng làm model đối chiếu/neural baseline.

## 7. ANN Cũ Trong App

ANN cũ được evaluate lại trên external P06/P07 để làm mốc đối chiếu. Ngưỡng trong bảng là ngưỡng tốt nhất khi sweep trên external, không nhất thiết là ngưỡng app đang dùng realtime.

| model_id | feature_set | class_weight | threshold | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | mcc | false_positive | false_negative |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ann_old_app | raw_99 | old_unknown | 0.3000 | 0.5917 | 0.6221 | 0.6928 | 0.6556 | 0.1594 | 1075 | 785 |

## 8. Phân Tích Video P07_incorrect_side_90_001.mp4

| threshold | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | macro_f1 | mcc | true_negative | false_positive | false_negative | true_positive | source_video |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.5500 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0 | 0 | 234 | 0 | dataset\external_videos\incorrect\P07_incorrect_side_90_001.mp4 |

## 9. Video-Wise Evaluation Của ANN Tốt Nhất

| source_video | label | n | accuracy | false_positive | false_negative | f1_incorrect |
| --- | --- | --- | --- | --- | --- | --- |
| dataset\external_videos\incorrect\P07_incorrect_side_90_001.mp4 | 1 | 234 | 0.0000 | 0 | 234 | 0.0000 |
| dataset\external_videos\incorrect\P06_incorrect_side_90_002.mp4 | 1 | 228 | 0.0219 | 0 | 223 | 0.0429 |
| dataset\external_videos\incorrect\P07_incorrect_side_30_002.mp4 | 1 | 238 | 0.3025 | 0 | 166 | 0.4645 |
| dataset\external_videos\correct\P07_correct_side_90_003.mp4 | 0 | 230 | 0.4043 | 137 | 0 | 0.0000 |
| dataset\external_videos\incorrect\P06_incorrect_side_30_002.mp4 | 1 | 192 | 0.6615 | 0 | 65 | 0.7962 |
| dataset\external_videos\correct\P07_correct_side_90_001.mp4 | 0 | 209 | 0.8278 | 36 | 0 | 0.0000 |
| dataset\external_videos\correct\P06_correct_side_30_001.mp4 | 0 | 157 | 0.8471 | 24 | 0 | 0.0000 |
| dataset\external_videos\correct\P07_correct_side_30_002.mp4 | 0 | 133 | 0.9098 | 12 | 0 | 0.0000 |
| dataset\external_videos\incorrect\P07_incorrect_front_003.mp4 | 1 | 206 | 0.9417 | 0 | 12 | 0.9700 |
| dataset\external_videos\correct\P07_correct_front_001.mp4 | 0 | 215 | 0.9488 | 11 | 0 | 0.0000 |
| dataset\external_videos\correct\P06_correct_side_90_001.mp4 | 0 | 190 | 0.9579 | 8 | 0 | 0.0000 |
| dataset\external_videos\correct\P06_correct_front_001.mp4 | 0 | 179 | 0.9609 | 7 | 0 | 0.0000 |
| dataset\external_videos\incorrect\P07_incorrect_side_90_002.mp4 | 1 | 246 | 0.9675 | 0 | 8 | 0.9835 |
| dataset\external_videos\incorrect\P06_incorrect_side_30_001.mp4 | 1 | 218 | 0.9725 | 0 | 6 | 0.9860 |
| dataset\external_videos\incorrect\P07_incorrect_front_001.mp4 | 1 | 168 | 0.9940 | 0 | 1 | 0.9970 |

## 10. Participant-Wise Evaluation Của ANN Tốt Nhất

| participant_id | n | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | mcc | false_positive | false_negative |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P06 | 1838 | 0.8183 | 0.9510 | 0.7196 | 0.8193 | 0.6689 | 39 | 295 |
| P07 | 2718 | 0.7726 | 0.8460 | 0.7199 | 0.7779 | 0.5556 | 197 | 421 |

## 11. Kết Luận

ANN đã được train local trên CSV mới và đánh giá trên external P06/P07. Nếu ANN tốt nhất vẫn thấp hơn HGB hiện tại, nên giữ HGB làm model chính cho demo và dùng ANN như baseline học sâu nhẹ. Nếu muốn dùng ANN v2 trong app, cần bảo đảm app tính đúng feature set tương ứng ở realtime.

## 12. Checklist

- [x] Đã backup ANN cũ.
- [x] Đã train ANN raw_99.
- [x] Đã train ANN normalized_99.
- [x] Đã train ANN ergonomic_v2_with_view.
- [x] Đã evaluate external P06/P07.
- [x] Đã sweep threshold.
- [x] Đã tạo confusion matrix.
- [x] Đã tạo video-wise evaluation.
- [x] Đã tạo participant-wise evaluation.
- [x] Đã so sánh với HGB mới.
- [x] Không có leakage P06/P07 vào train.
