# NGỮ CẢNH DỰ ÁN CHO CHATGPT WEB

Ngày tạo: 16/06/2026  
Dự án: `D:\posture_detection_app`

File này dùng để copy/paste cho ChatGPT Web hoặc một trợ lý AI khác trước khi hỏi về đề tài. Mục tiêu là giúp AI hiểu đúng phạm vi dự án, tránh trả lời quá mức hoặc suy đoán sai.

---

## 1. Thông tin đề tài

Tên đề tài luận văn:

> Xây dựng ứng dụng phát hiện lỗi tư thế làm việc qua webcam sử dụng Computer Vision, MediaPipe Pose và ANN.

Bản chất đề tài:

- Đây là đề tài nghiên cứu ứng dụng trong lĩnh vực thị giác máy tính và học máy.
- Hệ thống dùng webcam hoặc video MP4 để theo dõi tư thế làm việc.
- Ứng dụng phát hiện tư thế đúng/sai, cảnh báo khi người dùng duy trì tư thế sai và ghi log vào SQLite.
- Hệ thống là công cụ hỗ trợ nhắc nhở tư thế, không phải công cụ chẩn đoán y tế và không phải hệ thống đánh giá ergonomic chính thức.

Mục tiêu chính:

- Trích xuất pose landmarks từ video/webcam bằng MediaPipe Pose.
- Xây dựng các nhóm đặc trưng tư thế từ landmarks.
- Huấn luyện ANN/Keras classifier và so sánh với các mô hình học máy khác.
- Xây dựng baseline rule-based để có mốc so sánh dễ giải thích.
- Tích hợp vào ứng dụng desktop Python có giao diện realtime, cảnh báo và thống kê.

---

## 2. Pipeline tổng quát

Pipeline chính của dự án:

```text
Webcam / Video MP4
-> OpenCV đọc từng frame
-> MediaPipe Pose trích xuất 33 landmarks
-> Feature Extraction tạo vector đặc trưng
-> ANN / HGB / mô hình ML / rule-based baseline phân loại
-> Làm mượt dự đoán theo thời gian
-> Cảnh báo realtime nếu sai tư thế đủ lâu
-> Ghi log vào SQLite
-> Thống kê phiên/ngày trên dashboard
```

Vai trò từng thành phần:

| Thành phần | Vai trò trong dự án |
| --- | --- |
| OpenCV | Đọc webcam/video MP4, lấy frame, xử lý FPS, hiển thị khung hình. |
| MediaPipe Pose | Mô hình có sẵn để trích xuất 33 pose landmarks từ ảnh/video. |
| Feature Extraction | Chuyển landmarks thành vector số cho mô hình học máy. |
| Rule-based Detection | Baseline dựa trên ngưỡng hình học như lệch vai, nghiêng thân, đầu lệch, tay gần miệng. |
| ANN/Keras | Mô hình chính theo tên đề tài, phân loại tư thế từ vector landmarks. |
| Các mô hình ML khác | Logistic Regression, SVM, Random Forest, MLP, HistGradientBoosting dùng để benchmark/so sánh. |
| SQLite | Lưu tài khoản, cấu hình, phiên làm việc, log cảnh báo và dữ liệu thống kê. |
| Tkinter/CustomTkinter | Xây dựng giao diện desktop realtime. |

---

## 3. Những gì là mô hình có sẵn, những gì là đóng góp của sinh viên

Mô hình/công cụ có sẵn:

- MediaPipe Pose là mô hình có sẵn của Google, không phải đóng góp mới.
- OpenCV, TensorFlow/Keras, scikit-learn, SQLite, CustomTkinter là thư viện/công cụ có sẵn.
- ANN, SVM, Random Forest, HistGradientBoosting là thuật toán/mô hình có sẵn, sinh viên sử dụng và huấn luyện trong phạm vi dữ liệu của đề tài.

Đóng góp của sinh viên:

- Xây dựng quy trình end-to-end từ webcam/video đến cảnh báo tư thế.
- Tự quay video, trích xuất landmarks thành CSV và tổ chức dữ liệu thực nghiệm.
- Thiết kế feature schema thống nhất gồm `raw_99`, `normalized_99`, `ergonomic_14` và các bộ đặc trưng kết hợp.
- Xây dựng rule-based baseline có khả năng giải thích bằng hình học.
- Huấn luyện ANN và so sánh với nhiều mô hình học máy khác.
- Đánh giá theo external set, participant-wise, video-wise, benchmark runtime/FPS.
- Tích hợp ứng dụng desktop có realtime detection, cảnh báo âm thanh/giao diện, đăng nhập/đăng ký OTP email, SQLite logging và dashboard thống kê.
- Viết báo cáo luận văn, slide bảo vệ, tài liệu tham khảo, báo cáo khoa học/Springer draft.

---

## 4. Dữ liệu của dự án

Tóm tắt dữ liệu theo `reports/DATASET_MANIFEST.md`:

| Hạng mục | Giá trị |
| --- | ---: |
| Raw videos đúng tư thế | 34 |
| Raw videos sai tư thế | 50 |
| Raw videos tổng | 84 |
| External videos đúng tư thế | 5 |
| External videos sai tư thế | 5 |
| External videos tổng | 10 |
| Tổng số video | 94 |
| Số người trong raw dataset | 5 người, mã `P01`-`P05` |
| Góc quay raw | `front`, `side_30`, `side_90` |
| Tổng thời lượng video | 5991.480 giây |
| Tổng dung lượng video | 33142.051 MB |

CSV đã trích xuất:

| Dataset | File | Số dòng | Số cột |
| --- | --- | ---: | ---: |
| Raw metadata | `dataset/processed/posture_data_2fps_with_metadata.csv` | 11022 | 108 |
| External metadata | `dataset/processed/posture_external_test_2fps_with_metadata.csv` | 1658 | 108 |
| Raw ergonomic | `dataset/processed/posture_data_2fps_ergonomic_features.csv` | 11022 | 23 |
| External ergonomic | `dataset/processed/posture_external_test_2fps_ergonomic_features.csv` | 1658 | 23 |
| Raw combined | `dataset/processed/posture_data_2fps_combined_features.csv` | 11022 | 122 |
| External combined | `dataset/processed/posture_external_test_2fps_combined_features.csv` | 1658 | 122 |

Phân bố nhãn:

| Dataset | Correct `0` | Incorrect `1` |
| --- | ---: | ---: |
| Raw metadata CSV | 4438 | 6584 |
| External metadata CSV | 768 | 890 |

Lưu ý quan trọng về dữ liệu:

- Raw videos không nên công khai nếu chưa có consent vì có thể chứa mặt, dáng người, trang phục hoặc không gian cá nhân.
- External set hiện tại chỉ có `P01`, nên chưa chứng minh tổng quát mạnh cho người hoàn toàn mới.
- Participant-wise evaluation đã có nhưng dataset chỉ có 5 người, cần trình bày là đánh giá sơ bộ.
- Dữ liệu gắn nhãn ở mức đúng/sai, chưa phải chấm điểm ergonomic chính thức như RULA/REBA.

---

## 5. Feature schema của dự án

File chính:

- `src/feature_schema.py`
- `models/feature_schema_final.json`
- `reports/FEATURE_SCHEMA_FINAL.md`

Các nhóm đặc trưng:

| Feature set | Số feature | Ý nghĩa |
| --- | ---: | --- |
| `raw_99` | 99 | 33 MediaPipe landmarks, mỗi điểm gồm `(x, y, z)`. |
| `normalized_99` | 99 | Landmarks được chuẩn hóa theo trung điểm vai và scale cơ thể. |
| `ergonomic_14` | 14 | Đặc trưng hình học dễ giải thích về vai, thân, đầu/cổ, tay/cằm. |
| `combined_raw_ergonomic` | 113 | Kết hợp landmarks thô và ergonomic indicators. |
| `combined_normalized_ergonomic` | 113 | Kết hợp landmarks chuẩn hóa và ergonomic indicators. |

Các ergonomic indicators chính:

- `shoulder_y_diff`: lệch dọc giữa hai vai.
- `shoulder_tilt_angle`: độ nghiêng đường vai.
- `torso_lean_angle`: độ nghiêng thân trên.
- `head_offset_x`: độ lệch ngang của mũi so với trung điểm vai.
- `nose_to_shoulder_y`: vị trí mũi so với vai, hỗ trợ phát hiện cúi/rụt cổ.
- `nose_shoulder_clearance_ratio`: khoảng cách mũi-vai chuẩn hóa.
- `neck_compression_detected`: cờ rụt cổ.
- `left_hand_mouth_ratio`, `right_hand_mouth_ratio`: khoảng cách tay đến vùng miệng/cằm.
- `chin_rest_detected`: cờ tay gần cằm/miệng.
- `shoulder_width`, `torso_length`, `head_shoulder_distance`, `min_hand_mouth_ratio`.

Lý do dùng landmarks thay vì ảnh RGB:

- Ảnh RGB có số chiều rất lớn, chứa nhiều thông tin nền/ánh sáng/quần áo không trực tiếp phục vụ tư thế.
- Landmarks giữ lại hình học cơ thể, phù hợp với bài toán tư thế.
- Vector landmarks nhẹ hơn, huấn luyện nhanh hơn, phù hợp realtime.
- Đặc trưng hình học dễ giải thích khi trả lời hội đồng.
- CNN trên ảnh có thể mạnh hơn nếu có dataset lớn, nhưng không phù hợp nhất với phạm vi dữ liệu hiện tại.

---

## 6. Mô hình và kết quả hiện tại

ANN/Keras:

- Có mô hình ANN đã train trong `models/local_training/ann_best.keras`.
- Có `scaler.pkl` đi kèm.
- ANN là mô hình chính theo tên đề tài và được dùng để chứng minh hướng tiếp cận ANN trên vector landmarks.

Model registry:

- Dự án đã huấn luyện/benchmark thêm nhiều mô hình trong `models/registry/`.
- File registry chính: `models/model_registry.json`.
- Mô hình được chọn theo báo cáo hiện tại: `hist_gradient_boosting__normalized_99`.
- Tiêu chí chọn: F1 của lớp sai tư thế, sau đó recall, sau đó MCC.

Kết quả chọn model theo `reports/MODEL_SELECTION_REPORT.md`:

| Model | Feature set | Accuracy | Precision incorrect | Recall incorrect | F1 incorrect | MCC |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| HistGradientBoosting | `normalized_99` | 0.959590 | 0.950712 | 0.975281 | 0.962840 | 0.918932 |
| Random Forest | `normalized_99` | 0.958987 | 0.946739 | 0.978652 | 0.962431 | 0.917917 |
| SVM RBF | `ergonomic_14` | 0.953559 | 0.968858 | 0.943820 | 0.956175 | 0.907154 |

Kết quả final external sau calibration theo `reports/FINAL_EVALUATION_REPORT.md`:

| Model | Feature set | Threshold | n | Accuracy | Precision incorrect | Recall incorrect | F1 incorrect | MCC |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| HistGradientBoosting | `normalized_99` | 0.65 | 1658 | 0.965018 | 0.962222 | 0.973034 | 0.967598 | 0.929661 |

Participant-wise raw dataset:

- Accuracy trung bình: `0.886801`.
- F1 incorrect trung bình: `0.906748`.
- MCC trung bình: `0.773545`.
- Kết quả này cho thấy mô hình có khả năng tổng quát sơ bộ theo người, nhưng chưa đủ để claim mạnh vì chỉ có 5 người.

Runtime benchmark:

| Góc quay | Mean latency | Estimated FPS | MediaPipe latency | ANN latency |
| --- | ---: | ---: | ---: | ---: |
| front | 35.315 ms | 28.317 FPS | 24.713 ms | 8.712 ms |
| side_30 | 35.671 ms | 28.034 FPS | 25.184 ms | 8.496 ms |
| side_90 | 34.085 ms | 29.339 FPS | 23.981 ms | 8.247 ms |

Lưu ý khi trả lời:

- Có thể nói HGB đang là mô hình tốt nhất trong protocol cục bộ.
- Không được nói đây là state-of-the-art.
- Không được nói HGB là ANN.
- Nếu hỏi “Tên đề tài ANN còn đúng không nếu HGB tốt hơn?”, trả lời: tên đề tài vẫn đúng vì đề tài có xây dựng ANN, nhưng phần thực nghiệm trung thực cho thấy HGB là mô hình so sánh/ứng viên triển khai tốt hơn trong protocol hiện tại.

---

## 7. Ứng dụng desktop hiện tại

File chính:

- `src/4_main_desktop_app.py`

Chức năng đã có:

- Giao diện desktop bằng CustomTkinter.
- Đăng nhập, đăng ký tài khoản.
- Xác thực OTP email qua cấu hình SMTP/Gmail.
- Chọn nguồn vào: webcam, camera IP hoặc file video MP4.
- Chế độ dự đoán:
  - `ANN`
  - `HistGradientBoosting (best)`
  - `Rule-based Baseline`
- Hiển thị video realtime, trạng thái tư thế và độ tin cậy.
- Cảnh báo khi tư thế sai kéo dài đủ thời gian.
- Có thời gian cảnh báo mặc định khoảng 5 giây và cooldown khoảng 15 giây.
- Ghi log SQLite cho chế độ ANN; rule-based baseline chủ yếu để đối chiếu nhanh, không lưu như chế độ chính.
- Dashboard thống kê phiên/ngày, cảnh báo, thời lượng, risk index và export CSV.

Database:

- File mặc định: `database/posture_app.db`.
- Script tạo database: `src/3_database_setup.py`.
- SQLite dùng để lưu tài khoản, phiên làm việc, cấu hình, cảnh báo và thống kê.

Quyền riêng tư:

- App không cần lưu video người dùng vào SQLite.
- App lưu log cảnh báo/thống kê, không phải raw video.
- Nếu chia sẻ raw video ra ngoài cần consent và xử lý riêng tư.

---

## 8. Cấu trúc thư mục quan trọng

| Đường dẫn | Vai trò |
| --- | --- |
| `src/1_rule_based_baseline.py` | Baseline rule-based chạy độc lập. |
| `src/2_extract_features.py` | Trích xuất landmark features từ video sang CSV. |
| `src/3_database_setup.py` | Tạo SQLite schema. |
| `src/4_main_desktop_app.py` | Ứng dụng desktop realtime. |
| `src/5_train_ann_local.py` | Huấn luyện ANN local. |
| `src/6_evaluate_external.py` | Đánh giá external set. |
| `src/13_runtime_benchmark.py` | Benchmark runtime/FPS. |
| `src/17_participant_wise_evaluation.py` | Đánh giá theo người tham gia. |
| `src/18_benchmark_classifiers.py` | Benchmark nhiều thuật toán. |
| `src/21_train_model_registry.py` | Train model registry nhiều mô hình/feature set. |
| `src/feature_schema.py` | Chuẩn hóa feature schema. |
| `src/posture_baseline.py` | Rule-based logic và ergonomic features. |
| `dataset/` | CSV đã trích xuất và metadata. |
| `models/` | ANN, scaler, model registry và các model `.pkl`. |
| `reports/` | Báo cáo, kết quả, bảng, hình, checklist. |
| `reports/baocaoluanvan/` | Các chương luận văn và slide bảo vệ. |
| `release_docs/` | Hướng dẫn chạy/nộp source. |

---

## 9. Báo cáo luận văn hiện có

Thư mục:

```text
reports/baocaoluanvan/
```

Các file chính:

- `HOANCHINHC1.md`: Chương 1 hoàn chỉnh.
- `HOANCHINHC2.md`: Chương 2 cơ sở lý thuyết, đã viết lại theo cấu trúc bài mẫu và dùng trích dẫn số `[n]`.
- `HOANCHINHC3.md`: Chương 3.
- `HOANCHINHC4.md`: Chương 4.
- `HOANCHINHC5.md`: Chương 5.
- `QUYEN_BAOCAO_LUANVAN_DAYDU.md`: Bản gom báo cáo luận văn.
- `BAOCAO_BAOVE_TUTHE_WEBCAM.pptx`: Slide bảo vệ.
- `BAOCAO_BAOVE_TUTHE_WEBCAM.pdf`: PDF slide bảo vệ.

Hình Chương 2 đã tạo:

- `reports/baocaoluanvan/hinhanh/hinh_2_1_tong_quan_bai_toan.png`
- `reports/baocaoluanvan/hinhanh/hinh_2_2_landmarks_va_vector_dac_trung.png`
- `reports/baocaoluanvan/hinhanh/hinh_2_3_xu_ly_thoi_gian_thuc_va_luu_tru.png`

---

## 10. Những claim nên dùng

Nên nói:

- Đề tài xây dựng hệ thống phát hiện lỗi tư thế làm việc qua webcam theo hướng end-to-end.
- Hệ thống kết hợp MediaPipe Pose landmarks, feature extraction, ANN, các mô hình học máy so sánh, rule-based baseline, cảnh báo realtime và SQLite logging.
- MediaPipe Pose là mô hình có sẵn; đóng góp nằm ở pipeline ứng dụng, dữ liệu, feature schema, so sánh mô hình và tích hợp phần mềm.
- Landmarks được chọn vì nhẹ, phù hợp realtime, dễ giải thích hơn ảnh RGB trong phạm vi dữ liệu hiện tại.
- HGB normalized landmarks đạt kết quả tốt nhất trong protocol cục bộ sau khi benchmark, nhưng không claim state-of-the-art.
- Hệ thống là prototype nghiên cứu ứng dụng, hỗ trợ nhắc nhở tư thế.

Không nên nói:

- Không nói đây là hệ thống chẩn đoán bệnh.
- Không nói đây là hệ thống đánh giá ergonomic chính thức.
- Không nói đây là state-of-the-art posture recognition.
- Không nói MediaPipe là đóng góp mới của sinh viên.
- Không nói dataset là public benchmark.
- Không nói kết quả tổng quát cho mọi người/mọi môi trường.
- Không nói ngưỡng rule-based là chuẩn y khoa; chỉ là baseline dựa trên đặc trưng hình học và nguyên tắc công thái học.

---

## 11. Cách trả lời các câu hỏi phản biện thường gặp

### Căn cứ nào để nói tư thế này đúng?

Trả lời ngắn:

> Em không tự kết luận theo cảm tính. Trong phạm vi đề tài, tư thế đúng được quy ước là tư thế gần trung tính khi làm việc trước máy tính: đầu gần trục vai, vai cân bằng, thân không nghiêng rõ, không cúi/rụt cổ và không chống cằm. Cơ sở là các hướng dẫn công thái học như OSHA, ISO 11226 và các phương pháp đánh giá tư thế như RULA/REBA. Tuy nhiên hệ thống chỉ hỗ trợ nhắc nhở, không thay thế đánh giá ergonomic chính thức.

### Vì sao không dùng ảnh gốc mà dùng landmarks?

> Ảnh RGB có số chiều rất lớn và chứa nhiều nhiễu như nền, ánh sáng, màu áo. Bài toán tư thế chủ yếu cần thông tin hình học cơ thể, nên dùng 33 pose landmarks giúp giảm số chiều, tăng tốc huấn luyện/suy luận, phù hợp realtime và dễ giải thích bằng các đặc trưng như lệch vai, nghiêng thân, đầu lệch.

### MediaPipe có phải đóng góp của em không?

> Không. MediaPipe Pose là mô hình có sẵn của Google. Đóng góp của em là dùng MediaPipe để xây dựng pipeline phát hiện tư thế hoàn chỉnh, tạo dữ liệu, trích xuất và chuẩn hóa đặc trưng, huấn luyện/so sánh mô hình, xây dựng baseline và tích hợp vào ứng dụng desktop realtime.

### Vì sao chọn ANN?

> ANN phù hợp với vector landmarks có kích thước cố định, có thể học quan hệ phi tuyến giữa các điểm cơ thể và đủ nhẹ để chạy trong ứng dụng realtime. Đồng thời ANN phù hợp với tên đề tài và mục tiêu chứng minh hướng tiếp cận học máy trên pose landmarks.

### Vì sao không dùng CNN?

> CNN trên ảnh gốc cần dữ liệu lớn hơn, tài nguyên huấn luyện cao hơn và khó giải thích hơn. Với phạm vi đề tài, landmarks đã giữ lại thông tin hình học quan trọng cho tư thế, nên ANN/ML trên landmarks là hướng nhẹ và phù hợp hơn. CNN có thể là hướng phát triển khi có dataset ảnh/video lớn hơn.

### Nếu HGB tốt hơn ANN thì tên đề tài ANN có còn đúng không?

> Có. Đề tài vẫn xây dựng ANN và đánh giá ANN theo đúng mục tiêu ban đầu. Việc benchmark thêm HGB, SVM, Random Forest giúp so sánh khách quan. Nếu HGB tốt hơn, em trình bày trung thực rằng ANN là mô hình chính theo đề tài, còn HGB là mô hình so sánh đạt kết quả tốt hơn trong protocol hiện tại.

### Dữ liệu tự gắn nhãn có đáng tin không?

> Dữ liệu tự gắn nhãn có thể dùng cho luận văn ứng dụng nếu quy ước nhãn rõ ràng, dựa trên nguyên tắc công thái học và được mô tả nhất quán. Tuy nhiên đây vẫn là hạn chế vì chưa có chuyên gia ergonomic xác nhận. Do đó em chỉ claim mức prototype hỗ trợ nhắc nhở, không claim chuẩn y khoa hoặc ergonomic chính thức.

### Ngưỡng rule-based lấy từ đâu?

> Ngưỡng rule-based là baseline kỹ thuật dựa trên các đặc trưng hình học như lệch vai, nghiêng thân, lệch đầu, tay gần miệng/cằm và được hiệu chỉnh theo dữ liệu thực nghiệm. Nó dùng để đối chiếu và giải thích, không được xem là ngưỡng y khoa hay tiêu chuẩn ergonomic chính thức.

### Hệ thống có chẩn đoán bệnh không?

> Không. Hệ thống không chẩn đoán bệnh, không kết luận sức khỏe, không thay thế bác sĩ hoặc chuyên gia ergonomic. Hệ thống chỉ nhắc nhở khi phát hiện tư thế lệch khỏi quy ước đúng/sai trong phạm vi đề tài.

### Kết quả có tổng quát cho người khác không?

> Chưa thể khẳng định mạnh. Dự án đã có participant-wise evaluation trên 5 người và external test, nhưng external set hiện còn hạn chế về số người. Vì vậy chỉ có thể nói kết quả cho thấy khả năng tổng quát sơ bộ trong dữ liệu của đề tài; cần thêm người tham gia, góc quay và môi trường khác để kết luận rộng hơn.

### App có lưu video người dùng không?

> Không cần lưu video. App xử lý frame realtime để trích xuất landmarks và lưu log cảnh báo/thống kê vào SQLite. Raw video chỉ dùng trong giai đoạn xây dựng dataset/thực nghiệm.

### Điểm mới so với app posture có sẵn là gì?

> Điểm mới trong phạm vi luận văn là xây dựng đầy đủ pipeline nghiên cứu ứng dụng: tự tổ chức dữ liệu video, trích xuất MediaPipe landmarks, thiết kế nhiều nhóm đặc trưng, so sánh ANN với các mô hình ML, có rule-based baseline, đánh giá external/participant-wise/video-wise/runtime và tích hợp vào app desktop có cảnh báo, log SQLite và dashboard thống kê. Không claim là app thương mại tốt hơn mọi sản phẩm có sẵn.

---

## 12. Prompt gợi ý khi đưa file này cho ChatGPT Web

Có thể copy đoạn sau rồi đính kèm/copy toàn bộ nội dung file này:

```text
Bạn là trợ lý hỗ trợ tôi hoàn thiện luận văn CNTT. Hãy đọc ngữ cảnh dự án dưới đây trước khi trả lời. Khi trả lời, không được claim quá mức. Đề tài của tôi là ứng dụng phát hiện lỗi tư thế làm việc qua webcam dùng Computer Vision, MediaPipe Pose và ANN. Hãy trả lời theo hướng học thuật, đúng phạm vi nghiên cứu ứng dụng, có phân biệt rõ phần công cụ có sẵn và phần đóng góp của sinh viên. Nếu có câu hỏi phản biện, hãy trả lời ngắn gọn, đúng trọng tâm, không nói hệ thống là chẩn đoán y tế hoặc ergonomic chính thức.
```

---

## 13. Các file nên tham khảo thêm nếu cần chi tiết

| Nhu cầu | File nên xem |
| --- | --- |
| Tổng quan dữ liệu | `reports/DATASET_MANIFEST.md` |
| Đạo đức dữ liệu và quyền riêng tư | `reports/DATA_ETHICS_STATEMENT.md` |
| Ranh giới claim/hạn chế | `reports/CLAIM_BOUNDARY_AND_LIMITATIONS.md` |
| Feature schema | `reports/FEATURE_SCHEMA_FINAL.md` |
| Benchmark mô hình | `reports/MODEL_SELECTION_REPORT.md`, `reports/BENCHMARK_CLASSIFIERS_SUMMARY.md` |
| Kết quả cuối | `reports/FINAL_EVALUATION_REPORT.md` |
| Runtime/FPS | `reports/RUNTIME_BENCHMARK.md` |
| Luận văn | `reports/baocaoluanvan/HOANCHINHC1.md` đến `HOANCHINHC5.md` |
| App desktop | `src/4_main_desktop_app.py` |
| Feature extraction | `src/2_extract_features.py`, `src/feature_schema.py` |
| Rule-based baseline | `src/posture_baseline.py`, `src/1_rule_based_baseline.py` |

---

## 14. Tóm tắt một câu

Đây là một hệ thống nghiên cứu ứng dụng phát hiện lỗi tư thế làm việc qua webcam, dùng MediaPipe Pose để trích xuất landmarks, xây dựng các vector đặc trưng tư thế, huấn luyện ANN và so sánh nhiều mô hình học máy, sau đó tích hợp vào ứng dụng desktop có cảnh báo realtime, SQLite logging và dashboard thống kê; hệ thống chỉ hỗ trợ nhắc nhở tư thế, không phải công cụ chẩn đoán hoặc đánh giá ergonomic chính thức.
