# TASK 28 - Cập nhật bài báo Springer Overleaf theo dữ liệu mới, tối đa 13 trang

## 1. Mục tiêu

Cập nhật hoàn chỉnh bài báo khoa học Springer từ phiên bản thực nghiệm cũ sang protocol mới:

- Tập phát triển gồm P01-P05.
- Tập external gồm hai người chưa xuất hiện trong huấn luyện: P06-P07.
- Benchmark lại vai trò của Rule-based, ANN/Keras và các mô hình machine learning.
- HistGradientBoosting với `ergonomic_v2_with_view` là mô hình thực nghiệm được lựa chọn.
- Runtime phải dùng benchmark HGB mới, không dùng runtime ANN cũ.
- Build lại project Springer Overleaf thành PDF tiếng Anh hoàn chỉnh.
- Tổng số trang cuối cùng phải **nhỏ hơn 14 trang**, tức **không quá 13 trang**, tính cả tài liệu tham khảo.

Không sửa code ứng dụng, không train lại mô hình và không thay đổi dataset trong task này. Chỉ tổng hợp từ artifact thực nghiệm hiện có, cập nhật LaTeX, hình/bảng và build PDF.

## 2. Tài liệu đầu vào bắt buộc

### 2.1. Bài báo cũ dùng để đối chiếu

- `D:\LUẬN VĂN 2026\CA_NHAN\BAOCAOKHOAHOC\CHINH\chinhcuoicung\DuongLyCu_223650_DH22TIN01_GVHD_VOVANPHUC.docm`
- `D:\LUẬN VĂN 2026\CA_NHAN\BAOCAOKHOAHOC\CHINH\chinhcuoicung\DuongLyCu_223650_DH22TIN01_GVHD_VOVANPHUC.pdf`
- `reports/springer_overleaf/main_applied_research_final_formatfix.tex`
- `reports/springer_overleaf/references.bib`

Bản PDF cũ có 13 trang và chỉ được dùng làm mốc bố cục. Không được giữ lại số liệu cũ.

### 2.2. Nguồn sự thật của thực nghiệm mới

Đọc đầy đủ trước khi sửa bài:

- `reports/PROJECT_CONTEXT_AFTER_NEW_DATASET_AND_REEXPERIMENT.md`
- `reports/REBUILD_DATASET_P01_TRAIN_P06P07_EXTERNAL_REPORT.md`
- `reports/EXPERIMENT_PROTOCOL_FINAL.md`
- `reports/FEATURE_SCHEMA_FINAL.md`
- `reports/FULL_PROTOCOL_MODEL_BENCHMARK_EXTERNAL_P06P07_REPORT.md`
- `reports/FULL_PROTOCOL_BENCHMARK_FINAL_REVIEW.md`
- `reports/ANN_LOCAL_REBUILD_REPORT.md`
- `reports/MODEL_SELECTION_REPORT.md`
- `reports/MODEL_IMPROVEMENT_FP_REDUCTION_REPORT.md`
- `reports/RUNTIME_BENCHMARK_HGB_SELECTED.md`
- `reports/APP_HGB_MODE_UPDATE_REPORT.md`
- `reports/ERROR_ANALYSIS_BY_VIDEO_PERSON_VIEW.md`
- `reports/results/full_protocol_best_by_algorithm_default_threshold.csv`
- `reports/results/selected_hgb_external_calibrated_metrics.csv`
- `reports/results/full_protocol_repeatability_mean_std.csv`
- `reports/results/runtime_benchmark_hgb_selected_summary.csv`
- `reports/tables/figure_4_5_participant_metric_comparison.csv`
- `dataset/processed/posture_data_2fps_with_metadata.csv`
- `dataset/processed/posture_external_test_2fps_with_metadata.csv`
- `dataset/processed/video_manifest.csv`

Nếu các báo cáo cũ mâu thuẫn với CSV kết quả mới, ưu tiên CSV mới và ghi lại mâu thuẫn trong báo cáo thực thi.

## 3. Những số liệu cũ bắt buộc phải loại bỏ

Rà toàn bộ LaTeX, caption, hình, bảng, abstract, conclusion và xóa hoặc thay thế các thông tin sau:

- 84 development videos.
- 11,022 sampled frames.
- 4,438 Correct và 6,584 Incorrect.
- External 10 videos, 1,658 frames, chỉ P01.
- `hist_gradient_boosting__normalized_99`.
- Threshold 0.65.
- Accuracy 96.50%, Precision 96.22%, Recall 97.30%, F1 96.76%, MCC 92.97%.
- Confusion matrix TN=734, FP=34, FN=24, TP=866.
- Runtime 28.03-29.34 FPS của pipeline ANN cũ.
- Mọi câu nói external chỉ gồm P01.
- Mọi câu nói ANN là mô hình tốt nhất hoặc mô hình chính duy nhất.

Dùng `rg` để kiểm tra không còn các chuỗi/số liệu cũ trong file `.tex` cuối cùng.

## 4. Số liệu mới được phép sử dụng

### 4.1. Dataset split

| Split | Videos | Participants | Frames | Correct | Incorrect |
|---|---:|---|---:|---:|---:|
| Development | 94 | P01-P05 | 12,680 | 5,206 (41.06%) | 7,474 (58.94%) |
| External unseen-participant | 23 | P06-P07 | 4,556 | 2,001 (43.92%) | 2,555 (56.08%) |

Tổng cộng có 117 video, nhưng không được gộp hai split để tạo một chỉ số accuracy chung.

Phải nêu rõ:

- Không trùng participant giữa development và external.
- Không trùng `source_video`.
- P06 và P07 không được dùng để train.
- Nhãn Correct/Incorrect là nhãn theo quy ước của dự án, chưa được chuyên gia ergonomic xác nhận.

### 4.2. Benchmark chung tại threshold mặc định 0.50

Trong bảng so sánh công bằng giữa các họ thuật toán, lấy đúng một cấu hình đại diện cho mỗi họ từ:

`reports/results/full_protocol_best_by_algorithm_default_threshold.csv`

Phải có đủ chín phương pháp:

1. Logistic Regression.
2. SVM RBF.
3. KNN.
4. Decision Tree.
5. Random Forest.
6. MLPClassifier.
7. ANN/Keras.
8. HistGradientBoosting.
9. Rule-based Baseline.

Không trộn kết quả threshold đã hiệu chỉnh 0.76 vào bảng threshold mặc định 0.50.

Cấu hình HGB tốt nhất tại threshold mặc định:

- Model: `hist_gradient_boosting_balanced_sample_weight__ergonomic_v2_with_view`.
- Accuracy: 87.34%.
- Precision Incorrect: 86.71%.
- Recall Incorrect: 91.43%.
- F1 Incorrect: 89.01%.
- MCC: 0.7424.
- FP: 358.
- FN: 219.

Rule-based có Recall 100% nhưng MCC 0 và FP=2,001 vì dự đoán toàn bộ external thành Incorrect. Phải giải thích rõ, không được gọi đây là mô hình tốt.

### 4.3. Cấu hình HGB được lựa chọn sau hiệu chỉnh

- Model: `hist_gradient_boosting_none__ergonomic_v2_with_view`.
- Feature set: `ergonomic_v2_with_view`.
- Số đặc trưng: 31.
- Threshold: 0.76.
- Accuracy: 89.31%.
- Precision Incorrect: 93.48%.
- Recall Incorrect: 87.01%.
- F1 Incorrect: 90.13%.
- Macro F1: 89.24%.
- MCC: 0.7875.
- ROC-AUC: 94.91%.
- PR-AUC: 96.21%.
- TN=1,846, FP=155, FN=332, TP=2,223.

Phải ghi trung thực:

> Threshold 0.76 was selected using a sweep on P06-P07; therefore, this result is calibrated external performance and not a fully blind independent test estimate.

Không được gọi kết quả 0.76 là blind external validation.

### 4.4. ANN mới

ANN/Keras là neural baseline và là mô hình tích hợp ban đầu, không phải mô hình tốt nhất sau thực nghiệm mới.

Kết quả ANN local tốt nhất sau hiệu chỉnh:

- `ann_normalized_99_balanced`.
- Threshold 0.55.
- Accuracy 79.10%.
- Precision Incorrect 88.63%.
- Recall Incorrect 71.98%.
- F1 Incorrect 79.44%.
- MCC 0.5997.
- FP=236, FN=716.

Trong bảng so sánh chín thuật toán tại threshold 0.50 phải dùng đúng dòng ANN từ CSV benchmark mặc định, không thay bằng kết quả threshold 0.55.

### 4.5. Participant-wise của HGB được lựa chọn

| Participant | Frames | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC | FP | FN |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| P06 | 1,838 | 92.87% | 92.52% | 95.25% | 93.86% | 0.8542 | 81 | 50 |
| P07 | 2,718 | 86.90% | 94.29% | 81.24% | 87.28% | 0.7481 | 74 | 282 |

Phân tích P07 có Recall thấp hơn và nhiều FN hơn P06; không kết luận nguyên nhân nếu chưa có kiểm chứng.

### 4.6. Runtime HGB mới

| View | Mean latency | P95 latency | Estimated FPS |
|---|---:|---:|---:|
| front | 39.010 ms | 45.677 ms | 25.635 |
| side_30 | 38.764 ms | 45.695 ms | 25.797 |
| side_90 | 39.567 ms | 47.288 ms | 25.274 |

Phải gọi đây là **processing benchmark**, không phải full GUI FPS. Benchmark chưa bao gồm toàn bộ chi phí vẽ GUI, Tkinter scheduling, âm thanh và SQLite.

## 5. Hướng bài báo và giới hạn claim

Bài báo thuộc hướng:

> Applied Research: existing pose-estimation model + self-collected dataset + view-aware ergonomic features + comparative evaluation + desktop implementation.

Được phép claim:

- Xây dựng dataset video tự thu có metadata.
- External split P06-P07 là unseen-participant so với development P01-P05.
- Đề xuất/triển khai biểu diễn đặc trưng `ergonomic_v2_with_view`.
- Benchmark chín phương pháp dưới cùng protocol.
- HGB cho kết quả tốt nhất trong protocol của dự án.
- Pipeline xử lý đạt khoảng 25.27-25.80 FPS trong processing benchmark.

Không được claim:

- State-of-the-art.
- Mô hình pose estimation mới.
- Mô hình machine learning hoàn toàn mới.
- Tổng quát cho mọi người dùng/môi trường.
- External hoàn toàn độc lập sau khi đã dùng P06-P07 để hiệu chỉnh threshold.
- Kết quả tốt hơn nghiên cứu khác nếu khác dataset/protocol.

## 6. Cấu trúc bài báo cần giữ gọn

Dùng cấu trúc Applied Research với sáu mục lớn:

1. `Introduction`
2. `Related Work`
3. `Proposed Webcam-Based Posture Monitoring System`
4. `Experimental Protocol`
5. `Evaluation and Discussion`
6. `Conclusion and Future Work`

Không tạo quá nhiều `\subsection`. Dùng `\paragraph{...}` ngắn khi thật sự cần.

### 6.1. Title và tác giả

Tiêu đề đề nghị:

> Webcam-Based Working Posture Error Detection Using View-Aware Ergonomic Features and Lightweight Machine Learning

Thông tin tác giả giữ chính xác:

- `Ly-Cu DUONG`
- `Van-Phuc VO`
- Nam Can Tho University, Can Tho, Vietnam.

Không tự sửa tên, thứ tự tác giả, email hoặc ORCID nếu không có bằng chứng trong nguồn.

### 6.2. Abstract

- Tối đa 250 từ.
- Nêu vấn đề, phương pháp, dataset split, benchmark, HGB selected result và runtime.
- Không đưa toàn bộ chín kết quả model vào Abstract.
- Không citation.
- Không dùng “state-of-the-art”, “novel framework”, “groundbreaking”.
- Phải thay toàn bộ số liệu cũ.

### 6.3. Introduction và Related Work

- Giữ research gap rõ: webcam-only, pose landmarks, view-aware ergonomic features, benchmark, external unseen participants, realtime desktop warning/logging.
- Không biến Related Work thành danh sách bài báo.
- Không thêm reference hoặc DOI không kiểm chứng.
- Giữ khoảng 20-25 nguồn chất lượng nhất; chỉ giữ citation có liên quan trực tiếp.
- Official documentation chỉ dùng cho implementation.

### 6.4. Proposed System

Pipeline thống nhất:

```text
Webcam/IP camera/MP4
-> OpenCV Frame Capture
-> MediaPipe Pose Landmark Extraction
-> View-Aware Feature Construction
-> Posture Classification
-> Temporal Smoothing and Warning
-> SQLite Logging
```

Mô tả ngắn:

- `raw_99`.
- `normalized_99`.
- `ergonomic_14`.
- `ergonomic_v2`.
- `ergonomic_v2_with_view` gồm 31 đặc trưng và là nhóm được chọn.
- ANN là neural baseline/application model ban đầu.
- HGB là selected experimental/application recommendation sau benchmark.
- Rule-based là interpretable baseline.

Không đưa pseudocode dài. Nếu còn Algorithm 1 từ bản cũ thì xóa.

### 6.5. Experimental Protocol

Phải mô tả:

- 94 development videos P01-P05.
- 23 external videos P06-P07.
- Sampling 2 FPS.
- Participant-disjoint và video-disjoint.
- Chín phương pháp benchmark.
- Positive class là Incorrect.
- Metrics: Accuracy, Precision, Recall, F1, MCC, FP/FN; ROC-AUC/PR-AUC chỉ dùng nơi có xác suất hợp lệ.
- Benchmark mặc định threshold 0.50 và calibrated HGB threshold 0.76 là hai phân tích riêng.
- Repeatability nhiều seed chỉ trình bày ngắn nếu đủ chỗ; không dùng để chọn lại model.

### 6.6. Evaluation and Discussion

Ưu tiên bốn nội dung:

1. So sánh chín họ thuật toán tại threshold 0.50.
2. Kết quả HGB được lựa chọn tại threshold 0.76 và confusion matrix.
3. Participant-wise P06/P07 và phân tích FP/FN.
4. Runtime HGB theo ba góc nhìn.

Phải giải thích:

- HGB tốt nhất trong protocol của dự án.
- Logistic Regression có Precision cao nhưng Recall thấp hơn HGB mặc định.
- SVM/MLP/Rule-based có Recall cao nhưng FP lớn.
- ANN mới cải thiện so với ANN cũ nhưng thấp hơn HGB.
- P07 khó hơn P06, chủ yếu thể hiện qua Recall và FN.
- Ngưỡng 0.76 giảm FP nhưng làm tăng FN so với cấu hình ưu tiên Recall.

## 7. Hình và bảng tối đa để bảo đảm không vượt quá 13 trang

Không bê toàn bộ hình/bảng của luận văn vào bài báo.

### Hình bắt buộc hoặc ưu tiên

Chỉ dùng tối đa 4 figure environment:

1. System architecture.
2. Feature construction, cập nhật rõ `ergonomic_v2_with_view`.
3. HGB threshold/confusion matrix, có thể ghép hai subfigure.
4. Participant-wise/runtime, có thể ghép hai subfigure nếu vẫn đọc rõ.

Nguồn hình mới:

- `reports/figures/figure_4_2_algorithm_family_default_threshold_heatmap.png`
- `reports/figures/figure_4_3_selected_hgb_threshold_sweep.png`
- `reports/figures/figure_4_4_selected_hgb_confusion_matrix.png`
- `reports/figures/figure_4_5_participant_metric_comparison.png`
- `reports/figures/figure_4_6_hgb_runtime_latency_fps.png`

Không dùng confusion matrix cũ TN=734, FP=34, FN=24, TP=866.

### Bảng

Chỉ dùng tối đa 5 bảng chính:

1. Dataset split.
2. Feature groups.
3. Đại diện chín thuật toán tại threshold 0.50.
4. Selected HGB + participant-wise result, có thể trình bày gọn trong cùng bảng.
5. Runtime HGB.

Không đưa bảng 87 cấu hình đầy đủ vào bài chính.

Mỗi hình/bảng phải:

- Được nhắc và phân tích trong văn bản.
- Có caption sạch.
- Không có placeholder kiểu `[Insert Fig...]`.
- Không tràn lề, không chữ quá nhỏ.
- Không nhập tay số liệu nếu có thể tạo/đọc từ CSV.

## 8. Chiến lược giới hạn tối đa 13 trang

Giới hạn tính cả References. Bài báo được phép có đủ 13 trang nhưng tuyệt đối không được phát sinh trang thứ 14.

Page budget đề nghị:

| Nội dung | Ngân sách |
|---|---:|
| Title, Abstract, Introduction | 1.5 trang |
| Related Work | 1.0 trang |
| Proposed System | 2.0 trang |
| Experimental Protocol | 2.0 trang |
| Evaluation and Discussion | 3.5 trang |
| Conclusion, limitations, references | 2.0 trang |
| Khoảng dự phòng bố cục | 1.0 trang |

Nếu PDF vượt 13 trang, rút theo thứ tự:

1. Xóa lặp giữa Abstract, Introduction và Conclusion.
2. Rút Related Work nhưng giữ research gap.
3. Rút mô tả GUI và SQLite xuống một đoạn.
4. Gộp bảng/hình liên quan.
5. Chỉ giữ một cấu hình đại diện cho mỗi thuật toán.
6. Đưa chi tiết repeatability/video-wise ra khỏi bài chính.
7. Rút References ít liên quan nhưng không được xóa nguồn đang được trích dẫn.

Không được:

- Giảm font dưới chuẩn LNCS.
- Sửa margin của `llncs.cls`.
- Dùng `\vspace` âm dày đặc để ép trang.
- Scale bảng/hình đến mức không đọc được.

## 9. File đầu ra

Không xóa hoặc ghi đè bản cũ. Tạo:

- `reports/springer_overleaf/main_new_dataset_final.tex`
- `reports/springer_overleaf/main_new_dataset_final.pdf`
- `reports/springer_overleaf/main_new_dataset_final.bib` nếu cần tách bibliography; nếu dùng bibliography inline thì không bắt buộc.
- `reports/SPRINGER_NEW_DATASET_REVISION_REPORT.md`
- `reports/SPRINGER_NEW_DATASET_FINAL_CHECKLIST.md`

Báo cáo revision phải liệt kê:

- Các số liệu cũ đã thay.
- Các bảng/hình đã thay.
- Các claim đã giới hạn.
- Số trang PDF cuối.
- Các warning LaTeX còn lại.
- Những rủi ro học thuật chưa giải quyết.

## 10. Quy trình thực thi tuần tự

### Bước 1 - Audit bản cũ

- Đọc DOCM/PDF và LaTeX cũ.
- Ghi nhận số trang, cấu trúc, bảng, hình, citation.
- Lập danh sách mọi vị trí chứa số liệu cũ.

### Bước 2 - Xác minh dữ liệu mới

- Đọc CSV bằng parser, không đếm bằng mắt.
- Xác minh số video, participant, frame, label.
- Xác minh không overlap P01-P05 với P06-P07.
- Xác minh từng metric được dùng có nguồn CSV/report.

### Bước 3 - Tạo LaTeX mới

- Copy bản LaTeX cũ sang tên mới.
- Sửa có kiểm soát, không viết lại toàn bộ nếu không cần.
- Cập nhật title, abstract, method, experiment, evaluation, limitations và conclusion.
- Giữ định dạng LNCS và author-year hiện tại trừ khi template hội thảo yêu cầu khác.

### Bước 4 - Cập nhật hình/bảng

- Chỉ dùng artifact mới.
- Cập nhật sơ đồ feature nếu hình cũ chưa có view-aware features.
- Kiểm tra caption và lời dẫn.

### Bước 5 - Build Overleaf/LaTeX

Chạy build đủ số vòng cần thiết để citation và cross-reference ổn định. Có thể dùng `pdflatex`/`bibtex` hoặc công cụ LaTeX hiện có trong project.

### Bước 6 - Kiểm tra PDF trực quan

- Dùng `pdfinfo` hoặc `pypdf` xác nhận `pages <= 13`.
- Render toàn bộ trang PDF sang PNG.
- Kiểm tra từng trang: tràn lề, bảng bị cắt, hình mờ, caption tách trang, ký tự lỗi, khoảng trắng bất thường.
- Sửa và build lại cho đến khi không còn lỗi trình bày đáng kể.

### Bước 7 - Kiểm tra nội dung tự động

Chạy tìm kiếm trong file `.tex` cuối:

```text
84
11,022
1,658
P01 only
normalized_99 and threshold 0.65
96.50
96.76
28.03
29.34
734
866
[Insert Fig
This information should be completed before submission
state-of-the-art
```

Các chuỗi chỉ được tồn tại nếu nằm trong câu giải thích lịch sử cần thiết; mặc định phải bằng 0 kết quả.

### Bước 8 - Báo cáo cuối

Ghi rõ:

- File PDF cuối.
- Tổng số trang.
- Model và threshold được trình bày.
- Dataset split.
- Các metric chính.
- Việc nào chưa đủ bằng chứng.

## 11. Acceptance criteria

- [ ] PDF dùng đúng template Springer LNCS.
- [ ] Tác giả là Ly-Cu DUONG và Van-Phuc VO.
- [ ] PDF không quá 13 trang, kể cả References; tuyệt đối không có trang thứ 14.
- [ ] Không còn số liệu dataset/external cũ.
- [ ] Development là P01-P05; external là P06-P07.
- [ ] Dataset mới là 94 + 23 video và 12,680 + 4,556 frame.
- [ ] Có đủ chín phương pháp trong benchmark mặc định.
- [ ] Không trộn threshold 0.50 với threshold 0.76.
- [ ] HGB selected dùng `ergonomic_v2_with_view`, 31 features.
- [ ] Confusion matrix selected là TN=1,846, FP=155, FN=332, TP=2,223.
- [ ] ANN được mô tả là neural baseline/application model ban đầu.
- [ ] Runtime là HGB processing benchmark khoảng 25.27-25.80 FPS.
- [ ] Có cảnh báo threshold 0.76 đã hiệu chỉnh trên P06-P07.
- [ ] Không claim blind independent external test.
- [ ] Không claim state-of-the-art hoặc mô hình mới.
- [ ] Không có placeholder hình/nội dung.
- [ ] Không có citation hoặc cross-reference lỗi.
- [ ] Không có bảng/hình tràn lề hoặc chữ không đọc được.
- [ ] Abstract không quá 250 từ.
- [ ] Keywords từ 3 đến 5.
- [ ] Conclusion không thêm kết quả mới và không có citation.
- [ ] Có revision report và final checklist.

## 12. Điều cấm

- Không sửa code trong `src/`.
- Không train model.
- Không thay model artifact.
- Không sửa database.
- Không thay dataset.
- Không bịa số liệu, DOI, reference, phần cứng hoặc cấu hình môi trường.
- Không dùng metric từ protocol cũ để lấp chỗ trống.
- Không tối ưu threshold thêm trên P06-P07.
- Không đưa P06/P07 vào train.
- Không ghi kết quả calibrated external như kết quả blind hold-out.
