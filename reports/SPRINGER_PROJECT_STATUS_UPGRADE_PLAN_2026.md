# Phân Tích Hiện Trạng Và Lộ Trình Nâng Cấp Theo Hướng Springer

Ngày cập nhật: 2026-05-28

## Cap nhat sau khi sua external video

Ngay 2026-05-28, video
`dataset/external_videos/incorrect/P01_incorrect_004.mp4` da duoc thay bang
video sai tu the dung. Truoc do file nay co ten/folder `incorrect` nhung noi
dung bi nhap nham la video dung tu the. Toan bo external evaluation, video-wise
analysis, benchmark, ablation, error analysis, statistical analysis va paper
artifacts da duoc chay lai tren external dataset da sua.

Ket qua external ANN moi tai threshold 0.50:

| Metric | Gia tri |
|---|---:|
| External rows | 1658 |
| Accuracy | 90.169% |
| Precision incorrect | 95.609% |
| Recall incorrect | 85.618% |
| F1 incorrect | 90.338% |
| Macro-F1 | 90.166% |
| MCC | 80.901% |
| ROC-AUC | 98.226% |
| PR-AUC | 98.505% |

Ket qua benchmark external moi:

- SVM RBF + ergonomic features: F1 incorrect 95.107%, accuracy 94.873%.
- SVM RBF + raw features: F1 incorrect 91.580%, accuracy 91.194%.
- ANN + raw features: F1 incorrect 90.338%, accuracy 90.169%.
- Rule-based baseline: F1 incorrect 75.399%, accuracy 67.491%.

Video-wise error analysis moi:

- `P01_incorrect_005.mp4`: accuracy 67.485%, false negatives 53.
- `P01_correct_004.mp4`: accuracy 73.771%, false positives 32.
- `P01_incorrect_004.mp4`: accuracy 77.500%, false negatives 45.

Ket luan cu rang `P01_incorrect_004.mp4` la failure case cuc doan voi accuracy
2.929% khong con dung, vi ket qua do sinh ra tu video external bi nhap nham noi
dung. Sau khi sua, video nay van la hard case nhung khong con la loi gan nhu
toan bo.

## 1. Mục tiêu tài liệu

Tài liệu này tổng hợp dự án phát hiện lỗi tư thế làm việc qua webcam theo hướng có thể viết bài báo nghiên cứu khoa học hoặc báo cáo hội thảo quốc tế theo phong cách Springer.

Trọng tâm phân tích:

- Dự án hiện đã làm được những gì.
- Dự án đang thiếu những gì nếu muốn nâng cấp thành nghiên cứu mạnh hơn.
- Điểm mới nào có thể trình bày với thầy/hội đồng.
- Điểm nào chưa nên claim quá mạnh để tránh phản biện.
- Lộ trình nâng cấp tuần tự để đi từ demo sản phẩm đến bài báo có kiểm chứng.

## 2. Căn cứ đánh giá theo hướng Springer

Springer Nature khuyến nghị cấu trúc nghiên cứu phổ biến theo IMRaD: Introduction, Materials and Methods, Results, Discussion and Conclusions. Bài nghiên cứu cần trình bày đủ phương pháp, kết quả, thảo luận và khả năng tái lập. Tham khảo: https://www.springernature.com/gp/authors/campaigns/writing-a-manuscript/structuring-your-manuscript

Với loại bài Research Article, cấu trúc thường là Introduction, Methods, Results, Discussion và Conclusions. Với Method Article, cần mô tả phương pháp mới và có kết quả kiểm chứng phương pháp. Tham khảo: https://support.springernature.com/en/support/solutions/articles/6000271850-what-article-types-do-you-accept-

Nếu nghiên cứu có người tham gia, dữ liệu người tham gia hoặc hình ảnh/video người thật, phần đạo đức nghiên cứu, đồng ý tham gia, dữ liệu/code availability cần được chuẩn bị rõ. Tham khảo guideline ví dụ của Springer Nature Link: https://link.springer.com/journal/12553/submission-guidelines

## 3. Kết luận nhanh

Dự án hiện đã vượt mức một demo đơn giản. Dự án đã có một hệ thống ứng dụng desktop hoàn chỉnh, pipeline Computer Vision, mô hình học máy, baseline có giải thích, log phiên làm việc, dashboard thống kê, benchmark, ablation, đánh giá theo video/người, runtime benchmark và tài liệu phục vụ viết bài.

Tuy nhiên, nếu viết theo chuẩn Springer, dự án vẫn chưa nên claim là "state-of-the-art" hoặc "mô hình mới tốt hơn các nghiên cứu khác". Hướng phù hợp nhất hiện tại là:

> Một hệ thống AI ứng dụng hoàn chỉnh cho giám sát tư thế làm việc bằng webcam, kết hợp MediaPipe Pose, đặc trưng ergonomic có giải thích, phân loại học máy, cảnh báo thời gian thực, thống kê theo phiên và đánh giá thực nghiệm sơ bộ trên tập video tự thu.

Hướng paper phù hợp nhất:

- Applied AI system paper.
- Computer vision based ergonomic monitoring.
- Webcam-based posture monitoring with interpretable features and temporal risk scoring.

Không nên định vị là:

- Mô hình deep learning mới.
- Dataset benchmark chuẩn công khai.
- Phương pháp vượt state-of-the-art.
- Hệ thống y tế/clinical diagnosis.

## 4. Dự án hiện đã làm được gì

### 4.1. Sản phẩm desktop app

| Hạng mục | Trạng thái | Ý nghĩa |
|---|---|---|
| App desktop Tkinter/CustomTkinter | Đã có | Có thể demo trực tiếp bằng webcam/video. |
| Nguồn đầu vào camera/video/IP camera | Đã có | Phù hợp demo thực tế và test lại video. |
| Nhận diện pose bằng MediaPipe | Đã có | Trích xuất 33 landmarks cơ thể. |
| Mô hình ANN local | Đã có | Phân loại đúng/sai tư thế theo frame. |
| Rule-based ergonomic baseline | Đã có | Giải thích lỗi đầu, vai, thân, rụt cổ. |
| Cảnh báo realtime | Đã có | Có thời gian cảnh báo, cooldown, âm thanh. |
| Làm mượt xác suất | Đã có | Giảm nhấp nháy dự đoán theo frame. |
| Light/Dark mode | Đã có | Giao diện phù hợp demo sản phẩm hơn. |
| Dashboard thống kê | Đã có | Có thống kê phiên, risk, biểu đồ. |
| SQLite logging | Đã có | Có dữ liệu lịch sử để phân tích phiên làm việc. |
| Đóng gói sản phẩm | Đã có script | Có `build_scripts`, `release_docs`, hướng build app. |

Đây là điểm mạnh theo hướng sản phẩm: không chỉ có mô hình, mà có app chạy được, có cảnh báo, có log và có thống kê.

### 4.2. Dataset và metadata

Theo `dataset/metadata/video_manifest.csv`:

| Thành phần | Số lượng |
|---|---:|
| Tổng video | 94 |
| Video raw tự thu | 84 |
| Video external test | 10 |
| Video tư thế đúng trong raw | 34 |
| Video tư thế sai trong raw | 50 |
| Video đúng trong external | 5 |
| Video sai trong external | 5 |
| Tổng thời lượng | Khoảng 100.16 phút |
| Người tham gia raw | 5 người, P01-P05 |
| Góc quay raw | front, side_30, side_90 |

Phân bố người tham gia trong raw dataset:

| Người tham gia | Số video |
|---|---:|
| P01 | 19 |
| P02 | 11 |
| P03 | 18 |
| P04 | 16 |
| P05 | 20 |

Điểm đã tốt:

- Đã có manifest video.
- Đã có `participant_id`, label, split, view angle.
- Đã có SHA256 để kiểm tra toàn vẹn video local.
- Raw video không cần push GitHub vì nặng, nhưng metadata vẫn theo dõi được.

Điểm còn yếu:

- External set hiện chỉ có P01, chưa đại diện cho người mới.
- Chưa có thông tin điều kiện quay đầy đủ như khoảng cách camera, ánh sáng, webcam/laptop, độ cao camera.
- Chưa có consent form hoặc mô tả đồng ý tham gia nếu dùng để nộp bài nghiêm túc.
- Dataset vẫn nhỏ nếu muốn claim mạnh về generalization.

### 4.3. Pipeline nghiên cứu và đánh giá

Các thành phần đã có:

| Nhóm | File/Artifact tiêu biểu |
|---|---|
| Trích xuất đặc trưng | `src/2_extract_features.py`, `src/16_build_ergonomic_features.py` |
| Train ANN | `src/5_train_ann_local.py` |
| External evaluation | `src/6_evaluate_external.py` |
| Video-wise evaluation | `src/7_video_wise_evaluation.py` |
| Benchmark thuật toán | `src/8_compare_algorithms.py`, `src/18_benchmark_classifiers.py` |
| Ablation study | `src/9_ablation_study.py`, `src/19_ablation_feature_sets.py` |
| Statistical analysis | `src/11_statistical_analysis.py` |
| Temporal risk index | `src/12_temporal_risk_index.py` |
| Runtime benchmark | `src/13_runtime_benchmark.py` |
| Paper artifacts | `src/14_generate_paper_artifacts.py` |
| Error analysis | `src/20_error_analysis.py` |

Đây là điểm rất quan trọng cho bài báo: dự án không chỉ dừng ở app demo, mà đã có pipeline thực nghiệm có thể tái chạy.

## 5. Kết quả hiện tại có thể báo cáo

### 5.1. Benchmark trên external frame-level set

Theo `reports/results/classifier_benchmark_external.csv`, top model theo F1 lớp sai tư thế:

| Xếp hạng | Mô hình | Feature set | Accuracy | F1 sai tư thế | Macro-F1 | MCC |
|---:|---|---|---:|---:|---:|---:|
| 1 | SVM RBF | ergonomic | 94.87% | 95.11% | 94.86% | 89.85% |
| 2 | SVM RBF | combined | 93.49% | 93.68% | 93.48% | 87.29% |
| 3 | HistGradientBoosting | combined | 91.31% | 92.28% | 91.18% | 82.86% |
| 4 | Random Forest | combined | 91.01% | 92.06% | 90.85% | 82.35% |
| 5 | Logistic Regression | ergonomic | 90.89% | 91.66% | 90.81% | 81.69% |

Nhận xét:

- ANN hiện chạy tốt hơn nhiều sau khi sửa video external, nhưng không phải mô hình tốt nhất trong benchmark mở rộng theo feature set.
- SVM RBF với ergonomic features đang là ứng viên mạnh nhất nếu ưu tiên F1/accuracy trên external benchmark hiện tại.
- ANN vẫn có giá trị trong app hiện tại, nhưng nên benchmark lại với feature schema mới trước khi claim.

### 5.2. Kết quả ANN hiện tại

Theo `reports/results/algorithm_benchmark_full.csv`:

| Mô hình | Accuracy | Precision sai | Recall sai | F1 sai | ROC-AUC | PR-AUC |
|---|---:|---:|---:|---:|---:|---:|
| ANN | 90.17% | 95.61% | 85.62% | 90.34% | 98.23% | 98.51% |

Diễn giải:

- Precision cao nghĩa là khi app báo sai tư thế thì thường đúng.
- Recall thấp hơn nghĩa là vẫn có nhiều frame sai tư thế bị bỏ sót.
- ROC-AUC/PR-AUC cao cho thấy xác suất của ANN còn có tiềm năng nếu tune threshold/calibration tốt hơn.

### 5.3. Threshold sweep

Theo `reports/results/external_threshold_sweep.csv`, threshold 0.10 cho F1 cao nhất:

| Threshold | Accuracy | Precision | Recall | F1 | MCC |
|---:|---:|---:|---:|---:|---:|
| 0.10 | 91.38% | 92.78% | 91.01% | 91.89% | 82.95% |
| 0.20 | 91.25% | 94.08% | 89.33% | 91.64% | 82.61% |
| 0.15 | 90.89% | 93.85% | 88.88% | 91.30% | 81.88% |

Ý nghĩa:

- Ngưỡng 0.50 trong app có thể hơi bảo thủ, dễ bỏ sót tư thế sai.
- Nên coi threshold là tham số cần hiệu chỉnh, không nên cố định 0.50 cho mọi người/góc quay.

### 5.4. Đánh giá theo người tham gia

Theo `reports/results/participant_wise_metrics_combined.csv`, kết quả trung bình theo leave-one-participant-out:

| Mô hình | Feature set | Accuracy trung bình | F1 sai trung bình | Macro-F1 | MCC |
|---|---|---:|---:|---:|---:|
| SVM RBF | combined | 86.26% | 88.37% | 85.57% | 72.29% |
| Logistic Regression | combined | 84.77% | 86.76% | 84.10% | 71.36% |
| HistGradientBoosting | combined | 78.47% | 83.36% | 75.83% | 55.70% |
| Random Forest | combined | 77.86% | 83.21% | 74.97% | 53.99% |
| KNN | combined | 80.29% | 82.82% | 79.59% | 59.68% |

Nhận xét:

- Kết quả theo người tham gia là bước nâng cấp rất quan trọng so với chỉ split frame ngẫu nhiên.
- Combined features giúp kết quả ổn định hơn raw features.
- SVM RBF + combined hiện là ứng viên mạnh cho claim generalization theo người trong dataset nhỏ.

### 5.5. Ablation feature

Theo `reports/results/ablation_full.csv`:

| Feature group | Số feature | Accuracy | F1 sai tư thế |
|---|---:|---:|---:|
| normalized_plus_ergonomic | 45 | 93.42% | 94.44% |
| normalized_all_33_landmarks | 99 | 91.20% | 92.53% |
| raw_all_33_landmarks | 99 | 90.57% | 92.03% |
| normalized_head_shoulders_hips_hands | 33 | 86.30% | 88.39% |
| raw_head_shoulders_hips_hands | 33 | 86.26% | 88.38% |
| ergonomic_indicators | 12 | 83.49% | 85.98% |

Nhận xét:

- Đặc trưng normalized + ergonomic đang là hướng mạnh nhất.
- Đây là điểm có thể đưa vào contribution: không chỉ dùng raw landmark, mà kết hợp đặc trưng hình học/ergonomic dễ giải thích.
- Tuy nhiên cần nói rõ ablation này là theo protocol hiện tại; muốn mạnh hơn cần chạy lại dưới video-wise/person-wise split.

### 5.6. Video-wise error analysis

Theo `reports/results/video_wise_metrics.csv` và `reports/ERROR_ANALYSIS_BY_VIDEO_PERSON_VIEW.md`:

| Video lỗi nặng | Accuracy | False negative | Mean prob incorrect |
|---|---:|---:|---:|
| `P01_incorrect_005.mp4` | 67.48% | 53 | 0.683 |
| `P01_incorrect_004.mp4` | 77.50% | 45 | 0.769 |
| `P01_correct_004.mp4` | 73.77% | 0 false negative, 32 false positive | 0.274 |

Nhận xét:

- Đây là bằng chứng tốt cho phần Discussion/Limitation.
- Sau khi sửa video external, `P01_incorrect_004.mp4` không còn là failure case cực đoan; video này vẫn còn 45 false negatives nên vẫn là hard case thật.
- Cần phân tích nguyên nhân: góc quay, ánh sáng, độ cao camera, người bị che, nhãn chưa nhất quán, hoặc kiểu sai tư thế chưa có trong train.

### 5.7. Runtime benchmark

Theo `reports/results/runtime_benchmark_summary.csv`:

| Góc quay | Pose detection rate | Mean latency | P95 latency | Estimated FPS |
|---|---:|---:|---:|---:|
| front | 100% | 35.31 ms | 38.80 ms | 28.32 FPS |
| side_30 | 100% | 35.67 ms | 43.08 ms | 28.03 FPS |
| side_90 | 100% | 34.08 ms | 38.95 ms | 29.34 FPS |

Nhận xét:

- Pipeline MediaPipe + ANN đủ realtime ở mức xử lý video.
- Khi chạy GUI thực tế, FPS có thể thấp hơn do Tkinter drawing, camera buffer, logging và âm thanh.
- Đây là kết quả nên đưa vào paper vì chứng minh tính ứng dụng thực tế.

## 6. Điểm mới có thể trình bày trong bài báo

### 6.1. Điểm mới nên claim

| Điểm mới | Mức độ | Cách viết an toàn |
|---|---|---|
| End-to-end desktop app | Mạnh theo hướng ứng dụng | Hệ thống giám sát tư thế làm việc realtime bằng webcam. |
| Hybrid ML + ergonomic rules | Khá mạnh | Kết hợp phân loại học máy với chỉ báo ergonomic có giải thích. |
| Neck-compression/rụt cổ | Vừa | Bổ sung rule phát hiện trường hợp mũi gần ngang vai do rụt cổ sâu. |
| Temporal Posture Risk Index | Khá mạnh | Chuyển dự đoán frame-level thành risk score theo phiên. |
| Metadata-rich video manifest | Vừa | Chuẩn hóa dataset tự thu theo video, người, nhãn, góc quay. |
| Person-wise/video-wise evaluation | Mạnh nếu tiếp tục hoàn thiện | Đánh giá giảm rò rỉ dữ liệu so với frame-level random split. |
| Runtime benchmark | Vừa | Chứng minh khả năng realtime cho desktop app. |
| Ablation normalized + ergonomic | Mạnh nếu validate lại | Chứng minh giá trị của đặc trưng ergonomic/normalized. |

### 6.2. Điểm không nên claim là mới

| Nội dung | Lý do |
|---|---|
| Dùng MediaPipe Pose | Đây là framework phổ biến, không phải đóng góp mới. |
| Dùng 33 landmarks x/y/z | Raw landmarks không phải đặc trưng mới. |
| Binary label đúng/sai | Nhãn hai lớp còn rộng, chưa phải taxonomy mới. |
| ANN dense cơ bản | Chưa phải kiến trúc mô hình mới. |
| So sánh accuracy với paper khác | Không cùng dataset/protocol nên dễ bị phản biện. |

### 6.3. Claim nên dùng trong paper

Có thể viết:

> We propose a webcam-based posture monitoring system that integrates pose landmark extraction, machine-learning classification, interpretable ergonomic indicators, realtime alerts, local session logging, and temporal risk scoring for office posture assessment.

Nên tránh:

> The proposed model achieves state-of-the-art posture recognition performance.

Lý do: hiện chưa có benchmark công bằng trên dataset công khai hoặc cùng protocol với các nghiên cứu khác.

## 7. Những phần còn thiếu để dự án mạnh hơn

### 7.1. Thiếu về dataset

| Thiếu | Tác động | Cách khắc phục |
|---|---|---|
| Số người còn ít | Khó chứng minh generalization | Tăng lên 10-20 người nếu còn thời gian. |
| External set chỉ có P01 | External chưa thật sự độc lập | Quay thêm external từ người khác, camera khác. |
| Metadata điều kiện quay chưa đủ | Khó phân tích lỗi | Thêm camera_distance, camera_height, lighting, device, background. |
| Chưa có consent/ethics rõ | Yếu khi nộp hội thảo nghiêm túc | Tạo consent form, anonymize dữ liệu, mô tả data availability. |
| Chưa có taxonomy lỗi tư thế | Nhãn đúng/sai quá rộng | Tách sai thành forward_head, slouching, shoulder_imbalance, neck_compression, hand_chin_rest. |

### 7.2. Thiếu về thuật toán

| Thiếu | Tác động | Cách khắc phục |
|---|---|---|
| App hiện vẫn thiên về ANN/raw features | Chưa tận dụng kết quả ablation tốt nhất | Đưa normalized + ergonomic schema vào app. |
| Chưa đóng gói RF/SVM tốt nhất vào app | Model app chưa chắc là tốt nhất | Thêm model selector hoặc chọn model tốt nhất theo protocol. |
| Threshold chưa calibration theo người/góc quay | Có thể bỏ sót tư thế sai | Calibrate threshold bằng validation set và lưu vào model config. |
| Chưa có temporal model | Frame độc lập dễ nhiễu | Thử HMM, LSTM/GRU nhỏ, hoặc temporal feature window. |
| Chưa có uncertainty/confidence handling | Landmark kém vẫn dự đoán mạnh | Dùng visibility/pose confidence để giảm cảnh báo sai. |

### 7.3. Thiếu về đánh giá thực nghiệm

| Thiếu | Tác động | Cách khắc phục |
|---|---|---|
| Chưa có protocol cuối cùng duy nhất | Kết quả rời rạc khó viết paper | Chốt 3 protocol: external, video-wise, leave-one-participant-out. |
| Chưa có confidence interval theo video/person | Frame-level CI dễ lạc quan | Báo cáo mean/std theo video và người. |
| Chưa có statistical comparison đầy đủ giữa model | Khó chứng minh model nào tốt hơn | McNemar/paired bootstrap theo video-level predictions. |
| Chưa có error taxonomy | Discussion chưa sâu | Gán nhóm lỗi: false negative do angle, lighting, occlusion, ambiguous posture. |
| Chưa có robustness test | Khó thuyết phục reviewer | Test theo view angle, distance, lighting, device. |

### 7.4. Thiếu về paper artifacts

| Thiếu | Cách khắc phục |
|---|---|
| Hình pipeline chất lượng cao | Vẽ camera -> MediaPipe -> features -> model/rules -> alert/log/dashboard. |
| Screenshot GUI light/dark | Chụp màn hình app và dashboard. |
| Hình confusion matrix theo model tốt nhất | Xuất từ external/person-wise protocol cuối. |
| Hình ablation bar chart | Tạo biểu đồ F1/accuracy theo feature group. |
| Bảng dataset statistics final | Dùng manifest đã chuẩn hóa. |
| Bảng limitations | Viết rõ dataset nhỏ, chưa clinical, môi trường quay hạn chế. |

## 8. Lộ trình nâng cấp tuần tự

### Giai đoạn 1: Chốt trạng thái nghiên cứu hiện tại

Mục tiêu: làm cho kết quả hiện tại rõ ràng, không mâu thuẫn.

1. Chốt file dataset manifest final.
2. Chốt train/test CSV dùng cho paper.
3. Chốt protocol đánh giá chính: external, video-wise, leave-one-participant-out.
4. Chốt model chính để báo cáo: ANN hiện tại hay SVM/RF theo kết quả mới.
5. Ghi rõ model nào dùng trong app, model nào là benchmark nghiên cứu.

Kết quả đầu ra:

- `reports/EXPERIMENT_PROTOCOL_FINAL.md`
- `reports/tables/dataset_statistics_final.csv`
- `reports/tables/model_comparison_final.csv`

### Giai đoạn 2: Nâng cấp feature schema

Mục tiêu: biến kết quả ablation thành đóng góp kỹ thuật rõ ràng.

1. Chuẩn hóa landmark theo shoulder width hoặc torso length.
2. Thêm ergonomic features:
   - head forward offset
   - nose-to-shoulder vertical compression
   - shoulder slope
   - torso lean angle
   - neck angle proxy
   - hand-near-face/chin indicator
3. Tạo `models/feature_schema.json`.
4. Re-train model với normalized + ergonomic.
5. Đánh giá lại cùng protocol.

Kết quả đầu ra:

- `src/feature_schema.py`
- `models/posture_model_best.pkl` hoặc model tương đương
- `reports/FEATURE_SCHEMA_FINAL.md`
- `reports/results/feature_schema_ablation_final.csv`

### Giai đoạn 3: Chọn model tốt nhất cho app

Mục tiêu: app dùng mô hình có bằng chứng tốt nhất, không chỉ dùng ANN vì đã có sẵn.

1. So sánh ANN, RF, SVM RBF, Logistic Regression, HistGradientBoosting trên cùng feature schema.
2. Chọn tiêu chí chính: F1 sai tư thế hoặc recall sai tư thế.
3. Calibrate threshold để giảm false negative.
4. Lưu model kèm scaler/schema/threshold.
5. Cập nhật app load model theo config.

Kết quả đầu ra:

- `models/model_registry.json`
- `reports/MODEL_SELECTION_REPORT.md`
- App có thể chọn hoặc dùng model best mặc định.

### Giai đoạn 4: Làm mạnh đánh giá theo video và người

Mục tiêu: giảm phản biện "frame-level data leakage".

1. Leave-one-participant-out validation cho tất cả model chính.
2. Leave-one-video-out hoặc group split theo `source_video`.
3. Báo cáo mean/std theo người và theo video.
4. Tạo bảng worst-case videos.
5. Phân tích lỗi cho `P01_incorrect_005.mp4`, `P01_correct_004.mp4`, và `P01_incorrect_004.mp4`.

Kết quả đầu ra:

- `reports/PERSON_WISE_EVALUATION_FINAL.md`
- `reports/VIDEO_WISE_EVALUATION_FINAL.md`
- `reports/ERROR_TAXONOMY.md`

### Giai đoạn 5: Hoàn thiện đóng góp Temporal Posture Risk Index

Mục tiêu: biến app từ frame classifier thành hệ thống theo dõi phiên làm việc.

1. Định nghĩa công thức TPRI rõ ràng.
2. Tách thành phần:
   - tỷ lệ frame sai
   - thời lượng sai liên tục
   - số lần cảnh báo
   - độ tin cậy pose
   - mất người khỏi khung hình
3. Tạo ví dụ phiên làm việc.
4. Vẽ histogram hoặc line chart risk theo thời gian.
5. Liên hệ TPRI với ý nghĩa ergonomic, nhưng không claim y tế.

Kết quả đầu ra:

- `reports/TEMPORAL_RISK_INDEX_FINAL.md`
- `reports/figures/tpri_session_example.png`
- `reports/tables/tpri_session_summary.csv`

### Giai đoạn 6: Hoàn thiện paper theo Springer

Mục tiêu: có bản thảo nộp hội thảo.

1. Viết Introduction: vấn đề sai tư thế khi làm việc máy tính/webcam.
2. Viết Related Work: camera-based, sensor-based, ergonomic assessment.
3. Viết Materials and Methods:
   - dataset
   - pose extraction
   - feature schema
   - model training
   - temporal risk
   - app architecture
4. Viết Results:
   - benchmark
   - ablation
   - person-wise/video-wise
   - runtime
   - error analysis
5. Viết Discussion:
   - điểm mạnh
   - vì sao RF/SVM có thể tốt hơn ANN trên dataset nhỏ
   - hard cases sau khi sửa external video
   - giới hạn dataset
6. Viết Conclusion and Future Work.
7. Thêm Declarations:
   - ethics/consent
   - data availability
   - code availability
   - competing interests

Kết quả đầu ra:

- `reports/SPRINGER_MANUSCRIPT_DRAFT.md`
- `reports/SPRINGER_COVER_LETTER_DRAFT.md`
- `reports/SPRINGER_SUBMISSION_CHECKLIST_FINAL.md`

## 9. Cấu trúc bài báo đề xuất

Tên bài đề xuất:

> A Webcam-Based Desktop System for Real-Time Working Posture Monitoring Using Pose Landmarks, Interpretable Ergonomic Features, and Temporal Risk Scoring

### Abstract

Nêu vấn đề, mục tiêu, phương pháp, dataset, kết quả chính và giới hạn. Không claim quá mạnh.

### 1. Introduction

- Sai tư thế khi làm việc máy tính là vấn đề phổ biến.
- Webcam là giải pháp rẻ, không cần wearable/sensor.
- Thách thức: nhiễu camera, góc quay, khác biệt người dùng, cảnh báo realtime.
- Đóng góp của paper.

### 2. Related Work

- Vision-based posture monitoring.
- MediaPipe/pose landmark based recognition.
- Sensor/chair/IMU based posture systems.
- Ergonomic risk assessment.
- Khoảng trống: nhiều nghiên cứu chỉ dừng ở classifier, ít có desktop app + log + temporal risk.

### 3. Materials and Methods

- Dataset tự thu: 94 video, 5 người raw, 10 external video.
- Preprocessing và frame sampling.
- MediaPipe Pose landmarks.
- Raw, normalized và ergonomic feature groups.
- ANN/RF/SVM/benchmark model.
- Rule-based baseline.
- Temporal Posture Risk Index.
- Desktop system design.

### 4. Experimental Protocol

- External frame-level evaluation.
- Video-wise evaluation.
- Leave-one-participant-out evaluation.
- Ablation study.
- Runtime benchmark.
- Metrics: accuracy, precision, recall, F1, macro-F1, MCC, ROC-AUC, PR-AUC.

### 5. Results

- Bảng model comparison.
- Bảng ablation.
- Bảng person-wise.
- Bảng runtime.
- Confusion matrix/ROC/PR.
- Error analysis.

### 6. Discussion

- Hệ thống chạy realtime.
- Combined normalized + ergonomic features có lợi.
- ANN chưa tối ưu bằng RF/SVM trong một số protocol.
- False negative ở video hard case cần xử lý.
- Dataset còn nhỏ, cần mở rộng.

### 7. Limitations

- Dataset nhỏ, 5 người raw.
- External set hiện chỉ P01.
- Nhãn đúng/sai chưa tách loại lỗi.
- Chưa có đánh giá lâm sàng/ergonomic expert.
- Chưa kiểm thử nhiều webcam/môi trường.

### 8. Conclusion

Tóm tắt đóng góp thực tế: hệ thống app hoàn chỉnh, đặc trưng ergonomic có giải thích, đánh giá thực nghiệm, runtime realtime và hướng nâng cấp.

## 10. Những gì cần làm ngay nếu muốn nâng cấp nhanh nhất

Ưu tiên trong 1-2 ngày:

1. Chạy lại benchmark final với normalized + ergonomic features.
2. Chọn model final theo F1 sai tư thế và recall sai tư thế.
3. Tạo confusion matrix, ROC, PR cho model final.
4. Chụp screenshot app light mode, dark mode và dashboard.
5. Viết `EXPERIMENT_PROTOCOL_FINAL.md`.
6. Viết `SPRINGER_MANUSCRIPT_DRAFT.md` dựa trên số liệu đã chốt.

Ưu tiên trong 1 tuần:

1. Quay thêm external video từ ít nhất 3 người khác.
2. Tách nhãn lỗi tư thế thành nhiều nhóm.
3. Thêm consent/ethics documentation.
4. Tích hợp model tốt nhất vào app.
5. Hoàn thiện paper figures/tables.

Ưu tiên nếu muốn bài báo mạnh hơn:

1. Tăng dataset lên 10-20 người.
2. Chuẩn hóa multi-camera/multi-lighting protocol.
3. Thêm temporal model hoặc temporal features.
4. So sánh với ergonomic rule/RULA-inspired indicators.
5. Public code + metadata + landmark CSV để tăng reproducibility.

## 11. Verdict cuối cùng

Dự án hiện đủ tốt để demo tổng quan, làm đồ án tốt nghiệp và phát triển thành bài applied research. Điểm mạnh nhất là hệ thống đầy đủ từ webcam đến app, cảnh báo, logging, dashboard, benchmark và phân tích theo hướng nghiên cứu.

Để lên mức Springer workshop/conference tốt hơn, phần cần nâng cấp nhất không phải giao diện nữa, mà là:

1. Chốt protocol đánh giá chống data leakage.
2. Dùng feature schema normalized + ergonomic làm đóng góp kỹ thuật.
3. Chọn model final dựa trên benchmark, không mặc định ANN.
4. Mở rộng external/person-wise evaluation.
5. Viết rõ limitations, data availability và ethics.

Claim an toàn nhất:

> The project presents a practical, real-time webcam-based posture monitoring system with interpretable ergonomic features, temporal session-level risk scoring, and preliminary validation on a project-specific video dataset. The results indicate feasibility for desktop posture feedback, while larger participant-independent validation is required before claiming robust real-world generalization.
