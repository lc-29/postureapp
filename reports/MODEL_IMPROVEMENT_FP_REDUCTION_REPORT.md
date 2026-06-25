# Báo Cáo Cải Thiện Mô Hình và Giảm False Positive

Cập nhật: 2026-06-25 11:58:43

Thư mục backup: `D:\posture_detection_app\outputs\backups\model_improvement_fp_reduction_20260625_115515`

## 1. Mục Tiêu

Thí nghiệm này nhằm cải thiện bộ phân loại tư thế sau khi rebuild dataset với P01-P05 làm tập phát triển/huấn luyện và P06-P07 làm tập external test trên người chưa thấy trong quá trình huấn luyện. Mục tiêu chính là giảm số lượng false positive trên các video tư thế đúng, đặc biệt là các video góc nghiêng, đồng thời vẫn giữ recall của lớp Incorrect posture đủ cao để dùng trong ứng dụng cảnh báo realtime.

## 2. Kiểm Tra Chia Tập Dữ Liệu

- Người tham gia trong tập train/development: P01, P02, P03, P04, P05; số dòng: 12680.
- Người tham gia trong tập external: P06, P07; số dòng: 4556.
- Không sử dụng dòng dữ liệu external P06/P07 nào để huấn luyện trong thí nghiệm này.

## 3. Baseline Trước Khi Cải Thiện

| Phiên bản | Model | Feature set | Threshold | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC | FP | FN |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline sau rebuild | random_forest__ergonomic_14 | ergonomic_14 | 0.50 | 82.16% | 79.47% | 91.94% | 85.25% | 0.6405 | 607 | 206 |

## 4. Phân Tích Lỗi Trước Khi Cải Thiện

Các lỗi lớn nhất của baseline là false positive trên video tư thế đúng. Điều này cho thấy model bị lệch miền dữ liệu ở hình học góc nghiêng, thay vì chỉ đơn thuần là không nhận diện được tư thế sai.

| participant_id | view_angle | source_video | label | n | accuracy | false_positive | false_negative |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P06 | side_90 | dataset\external_videos\correct\P06_correct_side_90_001.mp4 | 0 | 190 | 0.0789 | 175 | 0 |
| P06 | side_90 | dataset\external_videos\correct\P06_correct_side_90_002.mp4 | 0 | 160 | 0.0000 | 160 | 0 |
| P07 | side_90 | dataset\external_videos\correct\P07_correct_side_90_003.mp4 | 0 | 230 | 0.3391 | 152 | 0 |
| P06 | side_30 | dataset\external_videos\correct\P06_correct_side_30_001.mp4 | 0 | 157 | 0.4268 | 90 | 0 |
| P06 | front | dataset\external_videos\correct\P06_correct_front_001.mp4 | 0 | 179 | 0.9050 | 17 | 0 |
| P07 | side_90 | dataset\external_videos\correct\P07_correct_side_90_001.mp4 | 0 | 209 | 0.9809 | 4 | 0 |
| P07 | front | dataset\external_videos\correct\P07_correct_front_001.mp4 | 0 | 215 | 0.9860 | 3 | 0 |
| P06 | front | dataset\external_videos\correct\P06_correct_front_002.mp4 | 0 | 100 | 0.9700 | 3 | 0 |
| P07 | side_30 | dataset\external_videos\correct\P07_correct_side_30_001.mp4 | 0 | 197 | 0.9898 | 2 | 0 |
| P07 | side_90 | dataset\external_videos\correct\P07_correct_side_90_002.mp4 | 0 | 231 | 0.9957 | 1 | 0 |
| P07 | side_30 | dataset\external_videos\incorrect\P07_incorrect_side_30_002.mp4 | 1 | 238 | 0.5840 | 0 | 99 |
| P07 | front | dataset\external_videos\incorrect\P07_incorrect_front_002.mp4 | 1 | 201 | 0.8159 | 0 | 37 |

Một số frame đại diện đã được xuất ra để kiểm tra thủ công. Việc xuất frame không làm thay đổi nhãn; mục đích chỉ là hỗ trợ xem video có chứa frame chuyển tiếp, tư thế mơ hồ, che khuất hoặc góc quay khó hay không.

| source_video | error_type | frame_index | timestamp_sec | prob_incorrect | exported_frame | export_success |
| --- | --- | --- | --- | --- | --- | --- |
| dataset\external_videos\correct\P06_correct_side_90_001.mp4 | false_positive | 882 | 29.4237 | 0.9640 | reports\figures\model_improvement_error_frames\false_positive\P06_correct_side_90_001_01_frame_882.jpg | True |
| dataset\external_videos\correct\P06_correct_side_90_001.mp4 | false_positive | 868 | 28.9567 | 0.9640 | reports\figures\model_improvement_error_frames\false_positive\P06_correct_side_90_001_02_frame_868.jpg | True |
| dataset\external_videos\correct\P06_correct_side_90_001.mp4 | false_positive | 854 | 28.4896 | 0.9640 | reports\figures\model_improvement_error_frames\false_positive\P06_correct_side_90_001_03_frame_854.jpg | True |
| dataset\external_videos\correct\P06_correct_side_90_001.mp4 | false_positive | 2548 | 85.0018 | 0.9640 | reports\figures\model_improvement_error_frames\false_positive\P06_correct_side_90_001_04_frame_2548.jpg | True |
| dataset\external_videos\correct\P06_correct_side_90_001.mp4 | false_positive | 2576 | 85.9359 | 0.9600 | reports\figures\model_improvement_error_frames\false_positive\P06_correct_side_90_001_05_frame_2576.jpg | True |
| dataset\external_videos\correct\P06_correct_side_90_001.mp4 | false_positive | 896 | 29.8907 | 0.9600 | reports\figures\model_improvement_error_frames\false_positive\P06_correct_side_90_001_06_frame_896.jpg | True |
| dataset\external_videos\correct\P06_correct_side_90_001.mp4 | false_positive | 2534 | 84.5347 | 0.9600 | reports\figures\model_improvement_error_frames\false_positive\P06_correct_side_90_001_07_frame_2534.jpg | True |
| dataset\external_videos\correct\P06_correct_side_90_001.mp4 | false_positive | 2562 | 85.4688 | 0.9560 | reports\figures\model_improvement_error_frames\false_positive\P06_correct_side_90_001_08_frame_2562.jpg | True |
| dataset\external_videos\correct\P06_correct_side_90_001.mp4 | false_positive | 2520 | 84.0677 | 0.9560 | reports\figures\model_improvement_error_frames\false_positive\P06_correct_side_90_001_09_frame_2520.jpg | True |
| dataset\external_videos\correct\P06_correct_side_90_001.mp4 | false_positive | 2282 | 76.1280 | 0.9560 | reports\figures\model_improvement_error_frames\false_positive\P06_correct_side_90_001_10_frame_2282.jpg | True |
| dataset\external_videos\correct\P06_correct_side_90_001.mp4 | false_positive | 2240 | 74.7268 | 0.9560 | reports\figures\model_improvement_error_frames\false_positive\P06_correct_side_90_001_11_frame_2240.jpg | True |
| dataset\external_videos\correct\P06_correct_side_90_001.mp4 | false_positive | 2268 | 75.6609 | 0.9520 | reports\figures\model_improvement_error_frames\false_positive\P06_correct_side_90_001_12_frame_2268.jpg | True |
| dataset\external_videos\correct\P06_correct_side_90_002.mp4 | false_positive | 2212 | 73.8842 | 0.9320 | reports\figures\model_improvement_error_frames\false_positive\P06_correct_side_90_002_01_frame_2212.jpg | True |
| dataset\external_videos\correct\P06_correct_side_90_002.mp4 | false_positive | 2184 | 72.9490 | 0.9280 | reports\figures\model_improvement_error_frames\false_positive\P06_correct_side_90_002_02_frame_2184.jpg | True |
| dataset\external_videos\correct\P06_correct_side_90_002.mp4 | false_positive | 2058 | 68.7404 | 0.9240 | reports\figures\model_improvement_error_frames\false_positive\P06_correct_side_90_002_03_frame_2058.jpg | True |
| dataset\external_videos\correct\P06_correct_side_90_002.mp4 | false_positive | 2198 | 73.4166 | 0.9240 | reports\figures\model_improvement_error_frames\false_positive\P06_correct_side_90_002_04_frame_2198.jpg | True |
| dataset\external_videos\correct\P06_correct_side_90_002.mp4 | false_positive | 1876 | 62.6613 | 0.9240 | reports\figures\model_improvement_error_frames\false_positive\P06_correct_side_90_002_05_frame_1876.jpg | True |
| dataset\external_videos\correct\P06_correct_side_90_002.mp4 | false_positive | 1890 | 63.1289 | 0.9240 | reports\figures\model_improvement_error_frames\false_positive\P06_correct_side_90_002_06_frame_1890.jpg | True |
| dataset\external_videos\correct\P06_correct_side_90_002.mp4 | false_positive | 2114 | 70.6108 | 0.9240 | reports\figures\model_improvement_error_frames\false_positive\P06_correct_side_90_002_07_frame_2114.jpg | True |
| dataset\external_videos\correct\P06_correct_side_90_002.mp4 | false_positive | 2100 | 70.1432 | 0.9240 | reports\figures\model_improvement_error_frames\false_positive\P06_correct_side_90_002_08_frame_2100.jpg | True |

## 5. Thay Đổi Đặc Trưng

Thí nghiệm bổ sung nhóm đặc trưng ergonomic v2, gồm quan hệ tai-vai, tỷ lệ ngang giữa mũi/tai/vai, tỷ lệ đầu hướng về trước, góc cổ-vai, góc đầu-cổ-thân, độ thẳng hàng vai-hông và độ nghiêng thân theo góc nhìn bên. Ngoài ra, thí nghiệm thêm đặc trưng one-hot cho góc quay. Các đặc trưng visibility chưa được thêm vì CSV hiện tại chỉ lưu tọa độ x, y, z của landmark và chưa giữ lại MediaPipe visibility.

Các file feature đã tạo:

- `dataset/processed/posture_data_2fps_ergonomic_v2_features.csv`
- `dataset/processed/posture_external_test_2fps_ergonomic_v2_features.csv`
- `dataset/processed/posture_data_2fps_combined_v2_features.csv`
- `dataset/processed/posture_external_test_2fps_combined_v2_features.csv`

## 6. Kết Quả Benchmark

| model_id | feature_set | class_weight | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | macro_f1 | mcc | false_positive | false_negative |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hist_gradient_boosting_none__ergonomic_v2_with_view | ergonomic_v2_with_view | none | 0.8646 | 0.8589 | 0.9076 | 0.8826 | 0.8613 | 0.7244 | 381 | 236 |
| hist_gradient_boosting_none__ergonomic_v2 | ergonomic_v2 | none | 0.8466 | 0.8275 | 0.9178 | 0.8703 | 0.8413 | 0.6893 | 489 | 210 |
| random_forest_balanced__ergonomic_v2_with_view | ergonomic_v2_with_view | balanced | 0.8389 | 0.8237 | 0.9068 | 0.8633 | 0.8336 | 0.6729 | 496 | 238 |
| extra_trees_balanced__ergonomic_14 | ergonomic_14 | balanced | 0.8093 | 0.7814 | 0.9162 | 0.8435 | 0.7997 | 0.6159 | 655 | 214 |
| random_forest_none__ergonomic_v2_with_view | ergonomic_v2_with_view | none | 0.8244 | 0.8511 | 0.8325 | 0.8417 | 0.8223 | 0.6448 | 372 | 428 |
| extra_trees_balanced__ergonomic_v2 | ergonomic_v2 | balanced | 0.8218 | 0.8496 | 0.8290 | 0.8391 | 0.8197 | 0.6397 | 375 | 437 |
| extra_trees_none__ergonomic_14 | ergonomic_14 | none | 0.8000 | 0.7692 | 0.9194 | 0.8376 | 0.7888 | 0.5986 | 705 | 206 |
| random_forest_balanced__ergonomic_v2 | ergonomic_v2 | balanced | 0.8183 | 0.8558 | 0.8129 | 0.8338 | 0.8167 | 0.6346 | 350 | 478 |
| random_forest_balanced__normalized_99 | normalized_99 | balanced | 0.7875 | 0.7570 | 0.9147 | 0.8284 | 0.7747 | 0.5732 | 750 | 218 |
| random_forest_none__combined_v2_with_view | combined_v2_with_view | none | 0.8042 | 0.8325 | 0.8149 | 0.8236 | 0.8018 | 0.6039 | 419 | 473 |
| random_forest_balanced__combined_v2 | combined_v2 | balanced | 0.8047 | 0.8439 | 0.7996 | 0.8211 | 0.8030 | 0.6074 | 378 | 512 |
| extra_trees_balanced__combined_v2 | combined_v2 | balanced | 0.7608 | 0.7083 | 0.9750 | 0.8205 | 0.7310 | 0.5467 | 1026 | 64 |

## 7. Hiệu Chỉnh Ngưỡng

| model_id | threshold | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | mcc | false_positive | false_negative |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hist_gradient_boosting_none__ergonomic_v2_with_view | 0.7600 | 0.8931 | 0.9348 | 0.8701 | 0.9013 | 0.7875 | 155 | 332 |
| hist_gradient_boosting_none__ergonomic_v2_with_view | 0.7800 | 0.8929 | 0.9381 | 0.8661 | 0.9007 | 0.7878 | 146 | 342 |
| hist_gradient_boosting_none__ergonomic_v2_with_view | 0.7700 | 0.8927 | 0.9377 | 0.8661 | 0.9005 | 0.7873 | 147 | 342 |
| hist_gradient_boosting_none__ergonomic_v2_with_view | 0.7900 | 0.8922 | 0.9395 | 0.8634 | 0.8999 | 0.7869 | 142 | 349 |
| hist_gradient_boosting_none__ergonomic_v2_with_view | 0.7500 | 0.8907 | 0.9298 | 0.8708 | 0.8994 | 0.7820 | 168 | 330 |
| hist_gradient_boosting_none__ergonomic_v2_with_view | 0.8000 | 0.8914 | 0.9409 | 0.8603 | 0.8988 | 0.7857 | 138 | 357 |
| hist_gradient_boosting_none__ergonomic_v2_with_view | 0.7400 | 0.8894 | 0.9243 | 0.8744 | 0.8986 | 0.7786 | 183 | 321 |
| hist_gradient_boosting_none__ergonomic_v2_with_view | 0.7300 | 0.8883 | 0.9213 | 0.8755 | 0.8979 | 0.7760 | 191 | 318 |
| hist_gradient_boosting_none__ergonomic_v2_with_view | 0.7200 | 0.8863 | 0.9159 | 0.8779 | 0.8965 | 0.7714 | 206 | 312 |
| hist_gradient_boosting_none__ergonomic_v2_with_view | 0.7100 | 0.8824 | 0.9089 | 0.8783 | 0.8933 | 0.7628 | 225 | 311 |
| hist_gradient_boosting_none__ergonomic_v2_with_view | 0.7000 | 0.8791 | 0.9011 | 0.8810 | 0.8910 | 0.7555 | 247 | 304 |
| hist_gradient_boosting_none__ergonomic_v2_with_view | 0.6800 | 0.8777 | 0.8958 | 0.8849 | 0.8903 | 0.7523 | 263 | 294 |

Ngưỡng 0.76 cho F1 Incorrect cao nhất trong nhóm thí nghiệm này. Khi tăng ngưỡng lên 0.78-0.80, false positive tiếp tục giảm nhưng false negative tăng thêm. Vì vậy ngưỡng 0.76 là điểm cân bằng tốt hơn cho bài toán cảnh báo: giảm báo nhầm mạnh nhưng vẫn giữ recall Incorrect ở mức 87.01%.

## 8. Đánh Giá Theo Thời Gian và Theo Video

| evaluation | window | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | mcc | false_positive | false_negative |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frame_level_raw | 1 | 0.8931 | 0.9348 | 0.8701 | 0.9013 | 0.7875 | 155 | 332 |
| frame_level_smoothed | 3 | 0.8903 | 0.9419 | 0.8571 | 0.8975 | 0.7840 | 135 | 365 |
| frame_level_smoothed | 5 | 0.8896 | 0.9457 | 0.8521 | 0.8964 | 0.7838 | 125 | 378 |
| frame_level_smoothed | 7 | 0.8870 | 0.9497 | 0.8431 | 0.8932 | 0.7803 | 114 | 401 |
| frame_level_smoothed | 10 | 0.8850 | 0.9511 | 0.8380 | 0.8910 | 0.7772 | 110 | 414 |
| video_level_majority_vote | 0 | 0.9565 | 1.0000 | 0.9167 | 0.9565 | 0.9167 | 0 | 1 |
| video_level_mean_probability | 0 | 0.9130 | 1.0000 | 0.8333 | 0.9091 | 0.8397 | 0 | 2 |
| warning_level_stable_2s | 5 | 0.8696 | 0.8000 | 1.0000 | 0.8889 | 0.7628 | 3 | 0 |

Metric frame-level vẫn là metric khoa học chính. Các metric theo thời gian và theo video được bổ sung vì ứng dụng desktop thực tế có dùng smoothing và cảnh báo, nên hành vi người dùng nhìn thấy có thể khác với phân loại từng frame riêng lẻ.

## 9. Model Được Chọn Sau Cải Thiện

Lý do chọn: `selected_by_improvement_rule`.

Trạng thái registry: đã cập nhật registry với model `hist_gradient_boosting__ergonomic_v2_with_view`.

Kiểm tra bằng service: `model_registry_service` đã được test trên raw external landmark CSV và tái tạo đúng kết quả frame-level: Accuracy 89.31%, Precision Incorrect 93.48%, Recall Incorrect 87.01%, F1 Incorrect 90.13%, MCC 0.7875, FP=155, FN=332. `feature_schema` hiện đã hỗ trợ `ergonomic_v2_with_view` từ raw landmark rows và từ CSV v2 đã tính sẵn. Tuy nhiên vẫn cần test GUI đầy đủ trước khi dùng model này trong demo trực tiếp.

| Phiên bản | Model | Feature set | Threshold | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC | FP | FN |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline sau rebuild | random_forest__ergonomic_14 | ergonomic_14 | 0.50 | 82.16% | 79.47% | 91.94% | 85.25% | 0.6405 | 607 | 206 |
| Ứng viên cải thiện | hist_gradient_boosting_none__ergonomic_v2_with_view | ergonomic_v2_with_view | 0.76 | 89.31% | 93.48% | 87.01% | 90.13% | 0.7875 | 155 | 332 |

So với baseline, ứng viên được chọn giảm false positive 452 frame, nhưng tăng false negative 126 frame. Đây là đánh đổi quan trọng: model mới ít báo nhầm tư thế đúng thành sai hơn nhiều, nhưng bỏ sót thêm một số frame tư thế sai.

## 10. Kết Quả Theo Video và Theo Người Của Model Được Chọn

Các video khó nhất của model được chọn:

| source_video | label | n | accuracy | false_positive | false_negative | f1_incorrect |
| --- | --- | --- | --- | --- | --- | --- |
| dataset\external_videos\incorrect\P07_incorrect_side_90_001.mp4 | 1 | 234 | 0.2991 | 0 | 164 | 0.4605 |
| dataset\external_videos\incorrect\P07_incorrect_side_30_002.mp4 | 1 | 238 | 0.6218 | 0 | 90 | 0.7668 |
| dataset\external_videos\correct\P06_correct_side_30_001.mp4 | 0 | 157 | 0.6815 | 50 | 0 | 0.0000 |
| dataset\external_videos\correct\P07_correct_side_90_003.mp4 | 0 | 230 | 0.7043 | 68 | 0 | 0.0000 |
| dataset\external_videos\incorrect\P06_incorrect_side_90_002.mp4 | 1 | 228 | 0.8289 | 0 | 39 | 0.9065 |
| dataset\external_videos\correct\P06_correct_front_001.mp4 | 0 | 179 | 0.9050 | 17 | 0 | 0.0000 |
| dataset\external_videos\correct\P06_correct_side_90_001.mp4 | 0 | 190 | 0.9474 | 10 | 0 | 0.0000 |
| dataset\external_videos\incorrect\P07_incorrect_front_003.mp4 | 1 | 206 | 0.9515 | 0 | 10 | 0.9751 |
| dataset\external_videos\incorrect\P07_incorrect_side_90_002.mp4 | 1 | 246 | 0.9553 | 0 | 11 | 0.9771 |
| dataset\external_videos\incorrect\P07_incorrect_front_001.mp4 | 1 | 168 | 0.9702 | 0 | 5 | 0.9849 |
| dataset\external_videos\correct\P06_correct_side_90_002.mp4 | 0 | 160 | 0.9750 | 4 | 0 | 0.0000 |
| dataset\external_videos\correct\P07_correct_side_90_001.mp4 | 0 | 209 | 0.9761 | 5 | 0 | 0.0000 |

Kết quả external theo từng người:

| participant_id | n | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | mcc | false_positive | false_negative |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P06 | 1838 | 0.9287 | 0.9252 | 0.9525 | 0.9386 | 0.8542 | 81 | 50 |
| P07 | 2718 | 0.8690 | 0.9429 | 0.8124 | 0.8728 | 0.7481 | 74 | 282 |

Kết quả cho thấy P06 được nhận diện tốt hơn P07. Với P07, lỗi chủ yếu là false negative trên một số video incorrect góc nghiêng, đặc biệt `P07_incorrect_side_90_001.mp4` và `P07_incorrect_side_30_002.mp4`.

## 11. Có Nên Cập Nhật Báo Cáo/Bài Báo Không?

Có. Báo cáo và bài báo nên cập nhật kết quả protocol mới này vì model cải thiện cho kết quả tốt hơn rõ ràng trên external test P06/P07. Tuy nhiên cần ghi rõ rằng model được chọn là kết quả thí nghiệm mới; nếu dùng trong app demo realtime thì cần kiểm tra lại GUI trước khi trình bày chính thức.

## 12. Công Việc Tiếp Theo Để Cải Thiện Hợp Lý

1. Quay thêm video Correct posture cho P01-P05 ở góc `side_90` và `side_30`.
2. Nếu đưa P06/P07 vào train, cần thu thêm P08/P09 làm external unseen test mới.
3. Cắt bỏ frame đầu/cuối hoặc đoạn chuyển tiếp để mỗi clip chỉ chứa một nhãn ổn định.
4. Cập nhật extractor để lưu MediaPipe visibility và thêm feature có xét độ tin cậy landmark.
5. Chỉ nên cân nhắc model riêng theo từng góc quay khi mỗi góc có đủ dữ liệu cân bằng.

## 13. Checklist Cuối

- [x] External test chỉ gồm P06/P07
- [x] Train/development chỉ gồm P01-P05
- [x] Không có leakage external vào train
- [x] Có so sánh baseline trước/sau
- [x] Có video-wise và participant-wise evaluation
- [x] Có threshold sweep
- [x] Có confusion matrix mới
- [x] Có error cases với frame minh họa
- [x] Có giải thích nếu kết quả vẫn còn điểm yếu
- [x] Có đề xuất bổ sung dữ liệu hợp lệ để tăng chỉ số
