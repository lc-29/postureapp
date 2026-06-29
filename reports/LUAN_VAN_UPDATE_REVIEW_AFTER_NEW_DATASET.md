# Hướng Dẫn Sửa Luận Văn Sau Khi Chốt Dataset Và Thực Nghiệm Mới

File luận văn đã rà soát:

```text
D:\LUẬN VĂN 2026\CA_NHAN\223650_DuongLyCu_BCLV.docx
```

Mục tiêu của file này là chỉ rõ **chương nào, mục nào, bảng nào, hình nào cần sửa**, đồng thời cung cấp **đoạn văn và bảng có thể copy trực tiếp vào Word**.

Lưu ý quan trọng khi sửa luận văn:

- Hãy xem dataset mới là dataset chính thức của đề tài, không viết theo kiểu “sau khi bổ sung thêm dataset”.
- Không dùng lại các số liệu cũ: 84 video, 10 external video, 11.022 mẫu, 1.658 mẫu, external chỉ P01, HGB normalized_99 threshold 0,65 đạt 96,50%.
- Protocol mới phải thống nhất: **P01-P05 là tập phát triển/train**, **P06-P07 là external test người mới**.
- ANN vẫn có trong luận văn nhưng nên trình bày là **baseline mạng nơ-ron/ứng viên so sánh**, không phải mô hình tốt nhất cuối cùng.
- HistGradientBoosting với `ergonomic_v2_with_view` là cấu hình khuyến nghị sau benchmark mới.

---

## 1. Bộ Số Liệu Chuẩn Phải Dùng Trong Toàn Luận Văn

### 1.1. Dataset chuẩn

| Nội dung | Giá trị mới cần dùng |
| --- | --- |
| Tổng số video | 117 video |
| Tổng số người tham gia | 7 người, P01-P07 |
| Tập phát triển/train | 94 video, P01-P05 |
| Video Correct trong tập phát triển | 39 video |
| Video Incorrect trong tập phát triển | 55 video |
| Số mẫu tập phát triển | 12.680 mẫu |
| Correct mẫu tập phát triển | 5.206 mẫu |
| Incorrect mẫu tập phát triển | 7.474 mẫu |
| Tập external test | 23 video, P06-P07 |
| Video Correct trong external | 11 video |
| Video Incorrect trong external | 12 video |
| Số mẫu external | 4.556 mẫu |
| Correct mẫu external | 2.001 mẫu |
| Incorrect mẫu external | 2.555 mẫu |
| Tần suất lấy mẫu | 2 FPS |
| Nhãn | Correct / Incorrect, nhãn project-specific |

### 1.2. Model và kết quả chuẩn

| Nội dung | Giá trị mới cần dùng |
| --- | --- |
| Model được chọn sau benchmark | `hist_gradient_boosting__ergonomic_v2_with_view` |
| Thuật toán | HistGradientBoosting |
| Feature set | `ergonomic_v2_with_view` |
| Số đặc trưng | 31 |
| Threshold | 0,76 |
| Accuracy external P06-P07 | 89,31% |
| Precision Incorrect | 93,48% |
| Recall Incorrect | 87,01% |
| F1 Incorrect | 90,13% |
| MCC | 0,7875 |
| ROC-AUC | 94,91% |
| PR-AUC | 96,21% |
| TN | 1.846 |
| FP | 155 |
| FN | 332 |
| TP | 2.223 |

### 1.3. ANN mới cần trình bày

| Model | Feature set | Threshold | Accuracy | F1 Incorrect | Ghi chú |
| --- | --- | ---: | ---: | ---: | --- |
| `ann_normalized_99_balanced` | `normalized_99` | 0,55 | 79,10% | 79,44% | ANN tốt nhất sau khi train lại local |
| `ann_old_app` | `raw_99` | 0,30 | 59,17% | 65,56% | ANN cũ trong app, chỉ dùng làm mốc đối chiếu |
| `hist_gradient_boosting__ergonomic_v2_with_view` | `ergonomic_v2_with_view` | 0,76 | 89,31% | 90,13% | Model khuyến nghị sau benchmark |

Đoạn giải thích nên dùng khi luận văn vẫn nhắc ANN:

> ANN/Keras được xây dựng như một baseline mạng nơ-ron và là hướng triển khai ban đầu của ứng dụng. Tuy nhiên, khi benchmark trên dữ liệu mở rộng, HistGradientBoosting với nhóm đặc trưng `ergonomic_v2_with_view` đạt kết quả external tốt hơn. Vì vậy, luận văn xem ANN là một mô hình so sánh quan trọng, còn HistGradientBoosting là cấu hình khuyến nghị sau thực nghiệm.

---

## 2. Các Cụm Từ Và Số Liệu Cũ Cần Tìm Trong Word Để Sửa

Trong Word, dùng `Ctrl + H` hoặc `Ctrl + F` để tìm các cụm sau:

| Cần tìm | Sửa thành |
| --- | --- |
| 84 video | 94 video nếu nói tập phát triển; 117 video nếu nói toàn bộ dữ liệu |
| 34 video nhãn Correct | 39 video Correct |
| 50 video nhãn Incorrect | 55 video Incorrect |
| 10 video external | 23 video external |
| 11.022 mẫu | 12.680 mẫu nếu nói tập phát triển |
| 4.438 mẫu Correct | 5.206 mẫu Correct |
| 6.584 mẫu Incorrect | 7.474 mẫu Incorrect |
| 1.658 mẫu | 4.556 mẫu nếu nói external |
| 768 mẫu Correct | 2.001 mẫu Correct |
| 890 mẫu Incorrect | 2.555 mẫu Incorrect |
| external hiện chỉ có P01 | external gồm P06 và P07 |
| corrected external set | external test set P06-P07 hoặc tập external P06-P07 |
| `hist_gradient_boosting__normalized_99` | `hist_gradient_boosting__ergonomic_v2_with_view` nếu nói model tốt nhất mới |
| threshold 0,65 | threshold 0,76 nếu nói model selected mới |
| Accuracy 96,50% | Accuracy 89,31% nếu nói external P06-P07 mới |
| F1 Incorrect 96,76% | F1 Incorrect 90,13% nếu nói external P06-P07 mới |
| P01_incorrect_004.mp4 là video khó | P07_incorrect_side_90_001.mp4 hoặc P07_incorrect_side_30_002.mp4 |

---

## 3. Sửa Phần Tóm Tắt Nếu Có

### Vị trí

Phần đầu luận văn, nếu có mục **TÓM TẮT** hoặc **ABSTRACT**.

### Vấn đề thường gặp

Nếu phần tóm tắt vẫn ghi:

- 84 video.
- 10 external video.
- 11.022 mẫu.
- 1.658 external samples.
- ANN là mô hình chính/tốt nhất.
- HGB normalized_99 đạt 96,50%.

thì cần sửa.

### Đoạn tóm tắt tiếng Việt có thể copy

> Luận văn trình bày quá trình xây dựng ứng dụng phát hiện lỗi tư thế làm việc qua webcam sử dụng Computer Vision. Hệ thống sử dụng OpenCV để đọc webcam, camera IP hoặc video, MediaPipe Pose để trích xuất 33 điểm mốc cơ thể, sau đó xây dựng các nhóm đặc trưng gồm landmark thô, landmark chuẩn hóa và đặc trưng hình học công thái học. Trên cơ sở các đặc trưng này, luận văn khảo sát Rule-based Baseline, ANN/Keras và các mô hình học máy dạng bảng như Logistic Regression, SVM, Random Forest và HistGradientBoosting.
>
> Dữ liệu của đề tài gồm 117 video tự thu thập từ 7 người tham gia. Tập phát triển gồm 94 video của P01-P05, tạo ra 12.680 mẫu ở 2 FPS; tập external gồm 23 video của P06-P07, tạo ra 4.556 mẫu dùng để đánh giá trên người mới. Kết quả thực nghiệm cho thấy ANN/Keras là baseline mạng nơ-ron quan trọng nhưng không phải mô hình tốt nhất sau benchmark. Cấu hình HistGradientBoosting với nhóm đặc trưng `ergonomic_v2_with_view` và threshold 0,76 đạt Accuracy 89,31%, Precision Incorrect 93,48%, Recall Incorrect 87,01%, F1 Incorrect 90,13% và MCC 0,7875 trên external P06-P07. Ứng dụng desktop đã tích hợp nhận diện realtime, skeleton overlay, cảnh báo âm thanh, làm mượt xác suất, cooldown cảnh báo, lưu lịch sử SQLite và dashboard thống kê.

---

## 4. Sửa Chương 1 - Giới Thiệu

### 4.1. Mục cần sửa

Trong Chương 1, cần rà các mục:

- Lý do chọn đề tài.
- Mục tiêu đề tài.
- Đối tượng và phạm vi nghiên cứu.
- Dữ liệu của đề tài.
- Đóng góp của đề tài.
- Cấu trúc luận văn.

### 4.2. Đoạn mô tả dữ liệu cần sửa

#### Vị trí

Chương 1, đoạn đang mô tả dataset. Trong bản Word hiện tại đã có đoạn nhắc:

- Tập phát triển gồm 94 video P01-P05.
- Tập external gồm 23 video P06-P07.

Đoạn này tương đối đúng nhưng cần bỏ cách viết kiểu “sau khi bổ sung dữ liệu”.

#### Đoạn thay thế có thể copy

> Dữ liệu của đề tài là dữ liệu tự thu thập, gồm các video mô phỏng tư thế làm việc đúng và sai trong bối cảnh sử dụng máy tính. Dữ liệu được tổ chức thành hai phần: tập phát triển và tập external. Tập phát triển gồm 94 video của năm người tham gia P01-P05, trong đó có 39 video Correct và 55 video Incorrect. Các video được lấy mẫu ở 2 FPS và xử lý bằng MediaPipe Pose, tạo ra 12.680 mẫu hợp lệ gồm 5.206 mẫu Correct và 7.474 mẫu Incorrect. Tập external gồm 23 video của hai người tham gia P06-P07, trong đó có 11 video Correct và 12 video Incorrect, tạo ra 4.556 mẫu hợp lệ gồm 2.001 mẫu Correct và 2.555 mẫu Incorrect. P06 và P07 không xuất hiện trong tập phát triển, nhờ đó tập external được dùng để đánh giá khả năng hoạt động của mô hình trên người tham gia mới.

### 4.3. Đoạn phạm vi nghiên cứu cần sửa

#### Vị trí

Chương 1, mục **Phạm vi nghiên cứu** hoặc đoạn nói hệ thống không phải đánh giá y khoa.

#### Đoạn thay thế có thể copy

> Phạm vi của đề tài là phát hiện nhị phân hai trạng thái Correct posture và Incorrect posture trong bối cảnh làm việc hoặc học tập trước máy tính. Các nhãn trong dataset là nhãn project-specific phục vụ mục tiêu xây dựng và kiểm thử hệ thống cảnh báo tư thế, chưa phải nhãn được xác nhận bởi chuyên gia công thái học, vật lý trị liệu hoặc y tế lao động. Do đó, kết quả của hệ thống không được diễn giải như chẩn đoán bệnh, đánh giá lâm sàng hoặc tiêu chuẩn công thái học chính thức.

### 4.4. Đoạn đóng góp cần sửa

#### Vị trí

Cuối Chương 1, mục **Đóng góp của đề tài** hoặc đoạn liệt kê đóng góp.

#### Đoạn thay thế có thể copy

> Các đóng góp chính của luận văn gồm:
>
> 1. Xây dựng bộ dữ liệu webcam/video tự thu thập cho bài toán phát hiện lỗi tư thế làm việc, gồm 117 video từ 7 người tham gia, được tổ chức thành tập phát triển P01-P05 và tập external P06-P07.
> 2. Thiết kế các nhóm đặc trưng từ MediaPipe Pose landmarks, bao gồm `raw_99`, `normalized_99`, `ergonomic_14`, `ergonomic_v2`, `ergonomic_v2_with_view` và các nhóm đặc trưng kết hợp.
> 3. Đánh giá nhiều phương pháp phân loại trên cùng protocol, gồm Rule-based Baseline, ANN/Keras, Logistic Regression, SVM, Random Forest, MLPClassifier và HistGradientBoosting.
> 4. Tích hợp pipeline nhận diện vào ứng dụng desktop Python có giao diện realtime, skeleton overlay, cảnh báo âm thanh, smoothing, cooldown, SQLite logging và dashboard thống kê.
> 5. Phân tích kết quả external theo frame-level, participant-wise, video-wise, threshold calibration và runtime benchmark để chỉ ra ưu điểm, hạn chế và hướng cải thiện của hệ thống.

### 4.5. Sửa câu “ANN là mô hình chính”

Nếu trong Chương 1 có câu kiểu:

> Đề tài sử dụng ANN làm mô hình chính để phân loại tư thế.

Nên sửa thành:

> Đề tài xây dựng ANN/Keras như một baseline mạng nơ-ron và so sánh với nhiều mô hình học máy khác. Kết quả benchmark trên dữ liệu mở rộng cho thấy HistGradientBoosting với đặc trưng `ergonomic_v2_with_view` là cấu hình khuyến nghị trong protocol hiện tại.

---

## 5. Sửa Chương 2 - Cơ Sở Lý Thuyết

### 5.1. Mục “Phân loại bằng ANN và các thuật toán học máy”

#### Vị trí

Chương 2, mục **Phân loại bằng ANN và các thuật toán học máy**.

#### Cần sửa

Phần này đang ổn về lý thuyết, nhưng nên bổ sung để tránh bị hỏi “vì sao không chọn ANN cuối cùng”.

#### Đoạn bổ sung có thể copy

> Trong phạm vi đề tài, ANN/Keras được sử dụng như một baseline mạng nơ-ron để học quan hệ phi tuyến giữa các đặc trưng landmark và nhãn tư thế. Tuy nhiên, dữ liệu đầu vào sau khi trích xuất bằng MediaPipe Pose là dữ liệu dạng bảng, gồm tọa độ, góc, khoảng cách và tỷ lệ hình học. Với dạng dữ liệu này, các mô hình học máy dạng bảng như Random Forest hoặc HistGradientBoosting cũng là lựa chọn phù hợp vì có thể học quan hệ phi tuyến, ít yêu cầu dữ liệu lớn hơn CNN end-to-end và có chi phí suy luận thấp. Do đó, luận văn không chọn mô hình cuối cùng theo giả định ban đầu mà dựa trên kết quả benchmark trên cùng tập dữ liệu và cùng giao thức đánh giá.

### 5.2. Mục “HistGradientBoosting”

#### Vị trí

Chương 2, đoạn đang giải thích HistGradientBoosting.

#### Đoạn bổ sung có thể copy

> HistGradientBoosting phù hợp với dữ liệu dạng bảng có số lượng đặc trưng vừa phải. Trong đề tài này, mô hình không học trực tiếp từ ảnh RGB mà học từ các đặc trưng đã được rút gọn từ MediaPipe Pose landmarks. Vì vậy, HistGradientBoosting có thể tận dụng các đặc trưng hình học như độ lệch vai, góc nghiêng thân, khoảng cách đầu-vai và thông tin góc nhìn mà không cần huấn luyện một mạng CNN lớn trên ảnh thô.

### 5.3. Mục “Đặc trưng hình học”

#### Vị trí

Chương 2, mục nói về trích xuất đặc trưng từ landmarks hoặc bảng nhóm đặc trưng.

#### Đoạn bổ sung có thể copy

> Bên cạnh tọa độ landmark thô và landmark chuẩn hóa, đề tài sử dụng thêm các đặc trưng hình học mở rộng nhằm mô tả rõ hơn quan hệ đầu-cổ-vai-thân. Nhóm `ergonomic_v2_with_view` bổ sung các tỷ lệ và góc liên quan đến vùng đầu, tai, vai, hông và góc quan sát. Mục tiêu của nhóm đặc trưng này là giảm phụ thuộc vào tọa độ tuyệt đối và giúp mô hình học được các dấu hiệu tư thế có ý nghĩa hơn đối với bài toán cảnh báo.

---

## 6. Sửa Chương 3 - Phân Tích, Thiết Kế Và Triển Khai Hệ Thống

### 6.1. Mục kiến trúc pipeline

#### Vị trí

Chương 3, đoạn mô tả pipeline:

```text
OpenCV -> MediaPipe Pose -> Feature extraction -> Model -> Warning -> SQLite
```

#### Đoạn thay thế có thể copy

> Quy trình xử lý của hệ thống bắt đầu từ nguồn đầu vào là webcam, camera IP hoặc video MP4. OpenCV đọc từng khung hình và chuyển sang MediaPipe Pose để trích xuất 33 landmarks cơ thể. Từ các landmarks này, hệ thống xây dựng các nhóm đặc trưng gồm `raw_99`, `normalized_99`, đặc trưng hình học và đặc trưng có thông tin góc nhìn. Kết quả đặc trưng được đưa vào một trong các phương pháp nhận diện gồm ANN/Keras, HistGradientBoosting hoặc Rule-based Baseline. Xác suất dự đoán được làm mượt theo cửa sổ thời gian, sau đó so sánh với threshold để xác định trạng thái Correct hoặc Incorrect. Nếu trạng thái Incorrect kéo dài quá thời gian cấu hình, hệ thống phát cảnh báo âm thanh và ghi nhận thông tin phiên làm việc vào SQLite.

### 6.2. Mục model trong app

#### Vị trí

Chương 3, đoạn mô tả ANN/HGB/Rule-based hoặc bảng công nghệ hệ thống.

#### Đoạn thay thế có thể copy

> Ứng dụng hỗ trợ nhiều chế độ nhận diện. Chế độ ANN sử dụng mô hình Keras và scaler tương ứng để dự đoán xác suất Incorrect từ vector đặc trưng. Chế độ Rule-based Baseline sử dụng các ngưỡng hình học để đưa ra quyết định có khả năng giải thích. Chế độ HistGradientBoosting gồm hai cấu hình: `HistGradientBoosting (balanced best)` dùng model `hist_gradient_boosting__ergonomic_v2_with_view` với threshold 0,76 cho kết quả khoa học cân bằng giữa FP và FN; `HistGradientBoosting (high recall demo)` dùng cấu hình ưu tiên giảm bỏ sót khi demo realtime. Việc tách nhiều chế độ giúp hệ thống vừa có khả năng so sánh thực nghiệm, vừa linh hoạt khi trình diễn ứng dụng.

### 6.3. Bảng nhóm đặc trưng trong Chương 3

#### Vị trí

Chương 3, bảng mô tả feature groups. Trong bản Word hiện tại có bảng gần nội dung:

```text
raw_99, normalized_99, ergonomic_14, combined...
```

#### Bảng thay thế có thể copy

| Nhóm đặc trưng | Số thành phần | Nội dung | Mục đích |
| --- | ---: | --- | --- |
| `raw_99` | 99 | Tọa độ `(x, y, z)` của 33 MediaPipe Pose landmarks | Giữ trực tiếp thông tin điểm mốc cơ thể |
| `normalized_99` | 99 | Landmarks chuẩn hóa theo trung điểm vai và tỷ lệ cơ thể | Giảm ảnh hưởng của vị trí người trong khung hình và khoảng cách camera |
| `ergonomic_14` | 14 | Các chỉ báo hình học ban đầu về vai, thân, đầu-cổ và tay-mặt | Tạo đặc trưng gọn và dễ diễn giải |
| `ergonomic_v2` | 27 | Đặc trưng hình học mở rộng vùng đầu, tai, vai, cổ, thân và hông | Mô tả rõ hơn các lỗi như rụt cổ, cúi đầu, nghiêng thân và lệch vai |
| `ergonomic_v2_with_view` | 31 | `ergonomic_v2` kết hợp one-hot view angle | Bổ sung thông tin góc nhìn để hỗ trợ mô hình khi dữ liệu có front, side_30 và side_90 |
| `combined_v2` | 135 | Kết hợp `raw_99`, `normalized_99` và `ergonomic_v2` | Khảo sát hiệu quả khi dùng nhiều nhóm đặc trưng cùng lúc |
| `combined_v2_with_view` | 139 | `combined_v2` kết hợp one-hot view angle | Khảo sát đặc trưng kết hợp có thông tin góc nhìn |

### 6.4. Mục database/SQLite

#### Vị trí

Chương 3, mục cơ sở dữ liệu hoặc bảng các bảng SQLite.

#### Đoạn bổ sung có thể copy

> Dữ liệu phiên làm việc, cấu hình và thống kê được ràng buộc với người dùng đang đăng nhập thông qua khóa người dùng trong SQLite. Cách tổ chức này giúp mỗi tài khoản có dữ liệu riêng, tránh tình trạng người dùng mới nhìn thấy lịch sử phiên hoặc cấu hình của người dùng trước. Đây là yêu cầu quan trọng khi ứng dụng được sử dụng như một sản phẩm desktop có nhiều tài khoản cục bộ.

---

## 7. Sửa Chương 4 - Thực Nghiệm Và Đánh Giá Hệ Thống

Đây là chương cần sửa nhiều nhất.

### 7.1. Mục “Môi trường thực nghiệm”

#### Vị trí

Chương 4, mục đầu tiên, hiện có đoạn nói ANN train bằng Kaggle Notebook.

#### Cần sửa

Vì ANN đã train lại local trên CSV mới, không nên viết ANN chỉ train trên Kaggle. Có thể nói Kaggle từng dùng ở giai đoạn đầu, nhưng protocol mới đã chạy local.

#### Đoạn thay thế có thể copy

> Quá trình thực nghiệm được thực hiện chủ yếu trên máy Windows cục bộ của đề tài, bao gồm trích xuất dữ liệu, xây dựng đặc trưng, benchmark mô hình học máy, hiệu chỉnh threshold, đánh giá external và kiểm thử ứng dụng desktop. ANN/Keras từng được huấn luyện trong môi trường notebook ở giai đoạn đầu, sau đó được train lại local trên CSV mới để đảm bảo kết quả phù hợp với dataset P01-P05 và external P06-P07. Các mô hình học máy dạng bảng như Random Forest và HistGradientBoosting được huấn luyện, lưu artifact và đánh giá bằng scikit-learn/joblib.

### 7.2. Mục “Dữ liệu và giao thức thực nghiệm”

#### Vị trí

Chương 4, đoạn ngay sau tiêu đề **Dữ liệu và giao thức thực nghiệm**.

Trong bản Word hiện tại, đoạn này vẫn ghi:

- Tập phát triển gồm 84 video.
- Tập external gồm 10 video.
- External chỉ P01.
- 11.022 mẫu và 1.658 mẫu.

#### Đoạn thay thế có thể copy

> Dữ liệu của đề tài được xây dựng từ các video tư thế làm việc trước máy tính. Tập phát triển gồm 94 video của năm người tham gia P01-P05, trong đó có 39 video nhãn Correct và 55 video nhãn Incorrect. Các video được lấy mẫu ở mức 2 FPS, sau đó từng khung hình được đưa qua MediaPipe Pose để trích xuất 33 điểm mốc cơ thể. Sau khi loại bỏ các mẫu không hợp lệ theo pipeline trích xuất, tập phát triển có 12.680 mẫu, gồm 5.206 mẫu Correct và 7.474 mẫu Incorrect.
>
> Ngoài tập phát triển, đề tài sử dụng tập external gồm 23 video của hai người tham gia P06 và P07. Tập này có 11 video Correct và 12 video Incorrect. Sau khi trích xuất ở mức 2 FPS, tập external có 4.556 mẫu hợp lệ, gồm 2.001 mẫu Correct và 2.555 mẫu Incorrect. P06 và P07 không xuất hiện trong tập phát triển, nhờ đó tập external cho phép đánh giá mô hình trên người tham gia mới. Tuy nhiên, do tập external vẫn chỉ gồm hai người và đã được dùng trong phân tích lỗi, kết quả này chưa được xem là kiểm thử mù hoàn toàn độc lập.

### 7.3. Đoạn mô tả file CSV

#### Vị trí

Chương 4, sau đoạn mô tả trích xuất dữ liệu. Trong bản Word hiện tại có đoạn nói:

```text
posture_data_2fps.csv có 11.022 mẫu...
posture_external_test_2fps_with_metadata.csv có 1.658 mẫu...
```

#### Đoạn thay thế có thể copy

> Dữ liệu sau trích xuất được lưu thành nhiều phiên bản CSV. Tập `posture_data_2fps.csv` có 12.680 mẫu và 100 cột, gồm 99 cột landmark và một cột nhãn. Phiên bản `posture_data_2fps_with_metadata.csv` có 12.680 mẫu và 108 cột, bổ sung metadata như `source_video`, `frame_index`, `timestamp_sec`, `participant_id`, `view_angle` và `camera_type`. Đối với tập external, file `posture_external_test_2fps_with_metadata.csv` có 4.556 mẫu và 108 cột. Các file `combined_v2_features` bổ sung thêm đặc trưng hình học mở rộng và thông tin góc nhìn để phục vụ benchmark mô hình.

### 7.4. Bảng 4.2 - Thống kê dữ liệu thực nghiệm sau trích xuất

#### Vị trí

Chương 4, ngay sau dòng:

```text
Bảng 4.2. Thống kê dữ liệu thực nghiệm sau trích xuất
```

#### Cần làm

Xóa bảng cũ đang có 11.022 và 1.658 mẫu. Thay bằng bảng sau.

#### Bảng copy vào Word

| Tập dữ liệu | Số video | Người tham gia | Số mẫu | Số cột | Correct | Incorrect | Ghi chú |
| --- | ---: | --- | ---: | ---: | ---: | ---: | --- |
| Development metadata | 94 | P01-P05 | 12.680 | 108 | 5.206 | 7.474 | Dữ liệu phát triển có metadata |
| Development raw landmark | 94 | P01-P05 | 12.680 | 100 | 5.206 | 7.474 | 99 landmark features + label |
| Development combined v2 | 94 | P01-P05 | 12.680 | 139 | 5.206 | 7.474 | Metadata, landmarks và ergonomic v2 |
| External metadata | 23 | P06-P07 | 4.556 | 108 | 2.001 | 2.555 | Dữ liệu external trên người mới |
| External combined v2 | 23 | P06-P07 | 4.556 | 139 | 2.001 | 2.555 | Dữ liệu external phục vụ benchmark v2 |

#### Đoạn giải thích sau bảng

> Bảng 4.2 cho thấy dữ liệu có xu hướng lệch về lớp Incorrect. Điều này phù hợp với mục tiêu ứng dụng vì hệ thống cần phát hiện các trạng thái sai tư thế, nhưng cũng làm cho Accuracy chưa đủ để đánh giá toàn diện. Vì vậy, luận văn sử dụng thêm Precision, Recall, F1-score của lớp Incorrect, MCC, FP và FN. Tập external P06-P07 được tách theo người tham gia, không đưa vào huấn luyện, nên có giá trị hơn phép chia ngẫu nhiên ở mức frame.

### 7.5. Hình 4.1 - Quy trình kiểm thử và đánh giá mô hình

#### Vị trí

Chương 4, hình hiện đang có caption:

```text
Hình 4.1. Quy trình kiểm thử và đánh giá mô hình
```

#### Cần kiểm tra

Nếu hình vẫn ghi dataset cũ hoặc không có P06-P07, cần sửa hình.

#### Nội dung hình nên có

Hình nên thể hiện luồng:

```text
Raw videos P01-P05
        -> 2 FPS sampling
        -> MediaPipe Pose
        -> feature extraction
        -> train/benchmark models
        -> model selection

External videos P06-P07
        -> 2 FPS sampling
        -> MediaPipe Pose
        -> feature extraction
        -> external evaluation
        -> threshold calibration / error analysis
```

#### Caption nên dùng

> Hình 4.1. Quy trình xây dựng dữ liệu, huấn luyện và đánh giá mô hình với tập phát triển P01-P05 và tập external P06-P07.

### 7.6. Mục “Kịch bản kiểm thử”

#### Vị trí

Chương 4, đoạn trước Bảng 4.4.

#### Đoạn thay thế có thể copy

> Quá trình đánh giá được tổ chức thành nhiều kịch bản nhằm xem xét hệ thống ở cả chất lượng phân loại và khả năng vận hành ứng dụng. Các thí nghiệm chính gồm benchmark nhóm đặc trưng và mô hình, đánh giá ANN/Keras, đánh giá model selected, khảo sát threshold, phân tích theo người tham gia, phân tích theo video, đánh giá smoothing theo thời gian và đo runtime. Lớp Incorrect được quy ước là lớp dương vì đây là trạng thái có khả năng kích hoạt cảnh báo.

### 7.7. Bảng 4.4 - Các kịch bản và mục tiêu đánh giá

#### Vị trí

Chương 4, bảng có caption:

```text
Bảng 4.4. Các kịch bản và mục tiêu đánh giá
```

#### Cần sửa

Dòng external không được ghi external P01 nữa. Thay bảng bằng bản sau nếu muốn đồng nhất.

#### Bảng copy vào Word

| Kịch bản đánh giá | Dữ liệu hoặc thành phần sử dụng | Mục tiêu đánh giá | Kết quả cần ghi nhận |
| --- | --- | --- | --- |
| Benchmark nhóm đặc trưng và mô hình | Tập phát triển P01-P05 và external P06-P07; các nhóm `raw_99`, `normalized_99`, `ergonomic_14`, `ergonomic_v2`, `ergonomic_v2_with_view`, `combined_v2` | So sánh ảnh hưởng của đặc trưng và thuật toán phân loại | Accuracy, Precision, Recall, F1 Incorrect, MCC, FP, FN |
| Đánh giá ANN/Keras | ANN train lại trên CSV mới | Kiểm tra hiệu quả baseline mạng nơ-ron | Accuracy, F1 Incorrect, FP, FN và so sánh với HGB |
| Đánh giá model selected | HGB `ergonomic_v2_with_view`, threshold 0,76 | Xác định cấu hình khuyến nghị sau benchmark | External metrics, confusion matrix, threshold calibration |
| Đánh giá trên external P06-P07 | 23 video của P06-P07 không nằm trong train | Kiểm tra khả năng hoạt động trên người mới | Frame-level metrics, participant-wise, video-wise |
| Đánh giá theo người tham gia | P06 và P07 trong external | Quan sát chênh lệch hiệu quả giữa từng người | Chỉ số theo participant, FP, FN |
| Đánh giá theo video | Từng video external | Xác định video khó, góc nhìn khó, lỗi FP/FN nổi bật | Accuracy theo video, FP, FN, nhận xét lỗi |
| Khảo sát threshold | Xác suất Incorrect trên external | Cân bằng giữa cảnh báo nhầm và bỏ sót | Metrics tại từng threshold |
| Đánh giá runtime | Các video đại diện theo góc nhìn | Kiểm tra khả năng gần realtime | Độ trễ, FPS, tỷ lệ phát hiện landmark |

### 7.8. Bảng benchmark mô hình

#### Vị trí

Chương 4, bảng hiện có các dòng như:

```text
SVM RBF ergonomic_14 94,87%
HistGradientBoosting combined_raw_ergonomic 91,32%
ANN/Keras 90,17%
Rule-based 67,49%
```

Bảng này là kết quả cũ, cần thay.

#### Bảng copy vào Word

| Phương pháp | Feature set | Threshold | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC | FP | FN |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| HGB selected | `ergonomic_v2_with_view` | 0,76 | 89,31% | 93,48% | 87,01% | 90,13% | 0,7875 | 155 | 332 |
| HGB uncalibrated | `ergonomic_v2_with_view` | 0,50 | 86,46% | 85,89% | 90,76% | 88,26% | 0,7244 | 381 | 236 |
| Random Forest baseline | `ergonomic_14` | 0,50 | 82,16% | 79,47% | 91,94% | 85,25% | 0,6405 | 607 | 206 |
| ANN/Keras rebuilt | `normalized_99` | 0,55 | 79,10% | 88,63% | 71,98% | 79,44% | 0,5997 | 236 | 716 |
| ANN app old | `raw_99` | 0,30 | 59,17% | 62,21% | 69,28% | 65,56% | 0,1594 | 1.075 | 785 |

#### Đoạn giải thích sau bảng

> Kết quả benchmark cho thấy ANN/Keras vẫn là baseline mạng nơ-ron quan trọng, nhưng không phải cấu hình tốt nhất trên external P06-P07. Cấu hình HGB selected với đặc trưng `ergonomic_v2_with_view` đạt F1 Incorrect 90,13%, cao hơn ANN/Keras rebuilt 79,44%. So với Random Forest baseline, HGB selected tăng Accuracy từ 82,16% lên 89,31% và giảm FP từ 607 xuống 155. Đổi lại, FN tăng từ 206 lên 332, cho thấy mô hình mới thận trọng hơn khi cảnh báo sai tư thế.

### 7.9. Bảng final selected model

#### Vị trí

Chương 4, bảng hiện có:

```text
Model ID: hist_gradient_boosting__normalized_99
Threshold: 0,65
Accuracy: 96,50%
F1 Incorrect: 96,76%
```

Bảng này phải thay hoàn toàn.

#### Bảng copy vào Word

| Chỉ số | Giá trị |
| --- | --- |
| Model ID | `hist_gradient_boosting__ergonomic_v2_with_view` |
| Thuật toán | HistGradientBoosting |
| Nhóm đặc trưng | `ergonomic_v2_with_view` |
| Số đặc trưng đầu vào | 31 |
| Ngưỡng quyết định | 0,76 |
| Số mẫu đánh giá | 4.556 |
| Số mẫu Correct | 2.001 |
| Số mẫu Incorrect | 2.555 |
| Accuracy | 89,31% |
| Precision lớp Incorrect | 93,48% |
| Recall lớp Incorrect | 87,01% |
| F1-score lớp Incorrect | 90,13% |
| Macro-F1 | 89,24% |
| MCC | 0,7875 |
| ROC-AUC | 94,91% |
| PR-AUC | 96,21% |
| True Negative | 1.846 |
| False Positive | 155 |
| False Negative | 332 |
| True Positive | 2.223 |

#### Đoạn giải thích sau bảng

> Cấu hình được chọn là HistGradientBoosting với nhóm đặc trưng `ergonomic_v2_with_view` và threshold 0,76. Kết quả trên external P06-P07 đạt Accuracy 89,31% và F1-score lớp Incorrect 90,13%. Precision Incorrect đạt 93,48%, cho thấy khi hệ thống cảnh báo sai tư thế thì phần lớn cảnh báo là đúng. Recall Incorrect đạt 87,01%, nghĩa là vẫn còn một số frame sai tư thế bị bỏ sót. Đây là điểm cần tiếp tục cải thiện bằng cách mở rộng dữ liệu và xử lý tốt hơn các video góc nghiêng.

### 7.10. Hình confusion matrix

#### Vị trí

Chương 4, hình ma trận nhầm lẫn của model cuối.

#### Cần sửa

Nếu hình hiện tại có số:

```text
734 / 34 / 24 / 866
```

thì đó là hình cũ. Cần thay bằng số mới:

```text
TN = 1.846
FP = 155
FN = 332
TP = 2.223
```

#### Caption nên dùng

> Hình 4.x. Ma trận nhầm lẫn của HistGradientBoosting `ergonomic_v2_with_view` trên tập external P06-P07.

#### Đoạn giải thích sau hình

> Ma trận nhầm lẫn cho thấy mô hình dự đoán đúng 1.846 mẫu Correct và 2.223 mẫu Incorrect. Số False Positive là 155, thấp hơn đáng kể so với baseline sau rebuild, cho thấy cấu hình mới giảm cảnh báo nhầm trên tư thế đúng. Tuy nhiên, số False Negative là 332, phản ánh vẫn còn các frame sai tư thế bị bỏ sót, chủ yếu ở một số video góc nghiêng hoặc tư thế không ổn định.

### 7.11. Bảng threshold calibration

#### Vị trí

Chương 4, bảng threshold hiện có các dòng 0,50; 0,60; 0,65; 0,75; 0,95 với kết quả 96%.

Bảng này là cũ, cần thay.

#### Bảng copy vào Word

| Threshold | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC | FP | FN |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0,70 | 87,91% | 90,11% | 88,10% | 89,10% | 0,7555 | 247 | 304 |
| 0,72 | 88,63% | 91,59% | 87,79% | 89,65% | 0,7714 | 206 | 312 |
| 0,74 | 88,94% | 92,43% | 87,44% | 89,86% | 0,7786 | 183 | 321 |
| 0,76 | 89,31% | 93,48% | 87,01% | 90,13% | 0,7875 | 155 | 332 |
| 0,78 | 89,29% | 93,81% | 86,61% | 90,07% | 0,7878 | 146 | 342 |
| 0,80 | 89,14% | 94,09% | 86,03% | 89,88% | 0,7857 | 138 | 357 |

#### Đoạn giải thích sau bảng

> Khi threshold tăng, mô hình thận trọng hơn trước khi dự đoán Incorrect. Điều này giúp giảm FP nhưng làm FN tăng. Threshold 0,76 được chọn vì cho F1 Incorrect cao nhất trong nhóm khảo sát, đồng thời giữ FP ở mức thấp hơn đáng kể so với baseline. Nếu ưu tiên giảm báo nhầm, có thể tăng threshold lên 0,78 hoặc 0,80; nếu ưu tiên phát hiện nhiều tư thế sai hơn, có thể giảm threshold, nhưng khi đó số cảnh báo nhầm sẽ tăng.

### 7.12. Bảng internal test vs external test

#### Vị trí

Chương 4, bảng hiện có:

```text
Gradient Boosting 99,44% internal, 88,11% external...
```

#### Khuyến nghị

Nếu chưa chạy lại internal split đồng nhất với protocol mới, nên **bỏ bảng này** hoặc chuyển thành đoạn văn thay vì bảng định lượng.

#### Đoạn thay thế có thể copy

> Kết quả internal thường cao hơn external do dữ liệu cùng miền với tập phát triển và có thể tồn tại tương đồng giữa các frame được lấy từ cùng người hoặc cùng điều kiện quay. Vì vậy, luận văn không dùng internal frame-level split làm bằng chứng chính về khả năng tổng quát. Thay vào đó, kết quả external P06-P07, participant-wise và video-wise được ưu tiên vì phản ánh tốt hơn khả năng hoạt động trên người mới.

### 7.13. Bảng participant-wise

#### Vị trí

Chương 4, bảng participant-wise hiện có P01-P05.

#### Cần sửa

Nếu bảng đang nhằm đánh giá external mới thì thay bằng P06/P07. Nếu muốn giữ P01-P05 leave-one-participant, cần chạy lại riêng. Trong bản sửa nhanh, nên dùng bảng external P06/P07.

#### Bảng copy vào Word

| Người tham gia | Số mẫu | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC | FP | FN |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| P06 | 1.838 | 92,87% | 92,52% | 95,25% | 93,86% | 0,8542 | 81 | 50 |
| P07 | 2.718 | 86,90% | 94,29% | 81,24% | 87,28% | 0,7481 | 74 | 282 |

#### Đoạn giải thích sau bảng

> Kết quả theo người tham gia cho thấy mô hình hoạt động tốt hơn trên P06 so với P07. Với P06, F1 Incorrect đạt 93,86% và FN chỉ 50 frame. Với P07, F1 Incorrect giảm còn 87,28% và FN tăng lên 282 frame. Điều này cho thấy sự khác biệt về dáng ngồi, góc quay và chất lượng landmark giữa từng người vẫn ảnh hưởng đáng kể đến mô hình.

### 7.14. Bảng video-wise / error analysis

#### Vị trí

Chương 4, bảng hiện có các video:

```text
P01_correct_003.mp4
P01_incorrect_004.mp4
P01_correct_001.mp4
P01_incorrect_002.mp4
```

Đây là external cũ, cần thay bằng P06/P07.

#### Bảng copy vào Word

| Nhóm trường hợp | Video đại diện | Nhãn thật | Số mẫu | Accuracy | Sai số chính | Nhận xét |
| --- | --- | --- | ---: | ---: | --- | --- |
| Video Incorrect khó nhất | `P07_incorrect_side_90_001.mp4` | Incorrect | 234 | 29,91% | FN = 164 | Model bỏ sót nhiều frame sai ở góc side_90 |
| Video Incorrect khó | `P07_incorrect_side_30_002.mp4` | Incorrect | 238 | 62,18% | FN = 90 | Góc nghiêng và tư thế mơ hồ làm recall giảm |
| Video Correct nhiều FP | `P07_correct_side_90_003.mp4` | Correct | 230 | 70,43% | FP = 68 | Góc side_90 dễ gây báo nhầm |
| Video Correct nhiều FP | `P06_correct_side_30_001.mp4` | Correct | 157 | 68,15% | FP = 50 | Dáng ngồi/góc quay gần ranh giới Incorrect |
| Video Correct ổn định | `P06_correct_front_002.mp4` | Correct | 100 | 100,00% | FP = 0 | Chính diện, landmark ổn định |
| Video Incorrect ổn định | `P07_incorrect_front_001.mp4` | Incorrect | 168 | 97,02% | FN = 5 | Front view dễ nhận diện hơn side view |

#### Đoạn giải thích sau bảng

> Phân tích theo video cho thấy các lỗi lớn tập trung ở một số video góc nghiêng. Video `P07_incorrect_side_90_001.mp4` có nhiều FN nhất, nghĩa là nhiều frame sai tư thế bị dự đoán thành Correct. Ngược lại, một số video Correct ở góc side_90 hoặc side_30 tạo nhiều FP, cho thấy mô hình còn nhạy với góc quay và hình học cơ thể gần ranh giới giữa hai lớp. Kết quả này giải thích vì sao cần tiếp tục mở rộng dữ liệu theo góc nhìn và người tham gia.

### 7.15. Bảng runtime

#### Vị trí

Chương 4, bảng runtime hiện có front, side_30, side_90.

#### Có thể giữ bảng hiện tại

Các số sau vẫn có thể dùng nếu bảng đang nói về core processing benchmark:

| Góc quan sát | FPS xử lý ước lượng |
| --- | ---: |
| front | 28,317 |
| side_30 | 28,034 |
| side_90 | 29,339 |

#### Đoạn cần thêm sau bảng

> Kết quả runtime cho thấy pipeline xử lý lõi đạt khoảng 28-29 FPS trên các video đại diện, đủ gần realtime cho mục tiêu demo desktop. Tuy nhiên, đây là benchmark xử lý lõi, chưa phải FPS đầy đủ của toàn bộ GUI vì chưa tính toàn bộ chi phí vẽ giao diện CustomTkinter, phát âm thanh, ghi SQLite, scheduling giao diện và đọc camera trực tiếp trong thời gian dài.

### 7.16. Bảng kiểm thử chức năng app

#### Vị trí

Chương 4, bảng kiểm thử chức năng ứng dụng desktop.

#### Dòng cần sửa

Dòng HistGradientBoosting hiện có thể đang ghi model cũ `hist_gradient_boosting__normalized_99`.

#### Nội dung thay thế cho dòng đó

| Chức năng hoặc trường hợp kiểm thử | Kết quả mong đợi | Kết quả ghi nhận | Trạng thái |
| --- | --- | --- | --- |
| Phân loại bằng HistGradientBoosting balanced best | Tải model HGB tốt nhất theo protocol mới và dùng đúng feature schema/threshold | App hỗ trợ mode `HistGradientBoosting (balanced best)` với model `hist_gradient_boosting__ergonomic_v2_with_view`, feature set `ergonomic_v2_with_view`, threshold 0,76 | Đã tích hợp trong app |
| Phân loại bằng HistGradientBoosting high recall demo | Có chế độ demo realtime ưu tiên giảm bỏ sót tư thế sai | App hỗ trợ mode `HistGradientBoosting (high recall demo)` dùng cấu hình HGB normalized_99 cũ để đối chiếu/demo khi cần recall cao | Đã tích hợp trong app |

---

## 8. Sửa Chương 5 - Kết Luận Và Hướng Phát Triển

### 8.1. Mục “Kết quả đạt được”

#### Vị trí

Chương 5, bảng hoặc đoạn đang ghi:

```text
Dữ liệu từ 84 video huấn luyện và 10 video external...
Gradient Boosting đạt Accuracy 0.8686 và F1-score 0.8811...
```

Cần thay hoàn toàn.

#### Bảng copy vào Word

| Nội dung | Kết quả đạt được |
| --- | --- |
| Pipeline xử lý | Hoàn thành luồng webcam/video, MediaPipe Pose, feature extraction, ANN/HGB/Rule-based, cảnh báo và SQLite logging |
| Dataset | Xây dựng dữ liệu từ 117 video tự thu thập, gồm 94 video development P01-P05 và 23 video external P06-P07 |
| Mẫu trích xuất | 12.680 mẫu development và 4.556 mẫu external ở 2 FPS |
| Đặc trưng | Xây dựng `raw_99`, `normalized_99`, `ergonomic_14`, `ergonomic_v2`, `ergonomic_v2_with_view`, `combined_v2` |
| ANN/Keras | Train lại ANN trên CSV mới; ANN tốt nhất đạt Accuracy 79,10% và F1 Incorrect 79,44% trên external P06-P07 |
| Model selected | HGB `ergonomic_v2_with_view`, threshold 0,76 đạt Accuracy 89,31% và F1 Incorrect 90,13% trên external P06-P07 |
| Ứng dụng desktop | Có đăng nhập/đăng ký/OTP, webcam/video/IP camera, skeleton overlay, light/dark mode, smoothing, cooldown, audio warning, SQLite logging và dashboard |
| Giá trị ứng dụng | Chứng minh khả năng xây dựng pipeline desktop chi phí thấp để hỗ trợ nhận biết tư thế làm việc đúng/sai qua webcam |

### 8.2. Đoạn kết luận tổng hợp

#### Đoạn thay thế có thể copy

> Luận văn đã xây dựng được một hệ thống phát hiện lỗi tư thế làm việc qua webcam dựa trên OpenCV, MediaPipe Pose và các mô hình học máy. Hệ thống không xử lý trực tiếp ảnh RGB bằng CNN mà chuyển khung hình thành 33 landmarks cơ thể, sau đó xây dựng các nhóm đặc trưng landmark thô, landmark chuẩn hóa và đặc trưng hình học công thái học. Cách tiếp cận này giúp giảm số chiều dữ liệu, phù hợp với quy mô dataset tự thu thập và cho phép triển khai realtime trên ứng dụng desktop.
>
> Về dữ liệu, đề tài đã xây dựng bộ dữ liệu gồm 117 video từ 7 người tham gia. Tập phát triển gồm 94 video của P01-P05, tạo ra 12.680 mẫu hợp lệ; tập external gồm 23 video của P06-P07, tạo ra 4.556 mẫu dùng để đánh giá trên người mới. Kết quả thực nghiệm cho thấy ANN/Keras là baseline mạng nơ-ron quan trọng, nhưng HistGradientBoosting với đặc trưng `ergonomic_v2_with_view` đạt kết quả tốt hơn trên external P06-P07. Cấu hình selected đạt Accuracy 89,31%, F1 Incorrect 90,13% và MCC 0,7875.
>
> Tuy nhiên, hệ thống vẫn còn hạn chế. Dataset tuy đã mở rộng nhưng vẫn còn nhỏ, external chỉ gồm hai người, nhãn Correct/Incorrect là nhãn project-specific và chưa có chuyên gia công thái học xác nhận. Một số video có frame chuyển tiếp hoặc tư thế mơ hồ, làm FP/FN tăng. Ngoài ra, runtime hiện tại mới là benchmark xử lý lõi, chưa phải FPS đầy đủ của toàn bộ giao diện khi chạy dài hạn.

### 8.3. Mục hạn chế

#### Đoạn copy vào Word

> Hạn chế thứ nhất là quy mô và độ đa dạng của dataset vẫn còn hạn chế. Tập phát triển có năm người và tập external có hai người, chưa đủ để khẳng định hệ thống tổng quát tốt cho mọi vóc dáng, trang phục, điều kiện ánh sáng và góc camera.
>
> Hạn chế thứ hai là nhãn Correct/Incorrect trong dataset là nhãn project-specific phục vụ mục tiêu xây dựng hệ thống cảnh báo, chưa được xác nhận bởi chuyên gia công thái học hoặc y tế lao động. Do đó, kết quả của hệ thống không nên được diễn giải như đánh giá y khoa hoặc chuẩn ergonomic chính thức.
>
> Hạn chế thứ ba là quá trình đánh giá được thực hiện ở mức frame trong khi nhãn được gán theo video. Trong một video có thể tồn tại một số frame chuyển tiếp, frame người dùng điều chỉnh tư thế hoặc frame mơ hồ. Điều này có thể làm tăng FP hoặc FN và cần được xử lý bằng quy trình cắt lọc frame hoặc gán nhãn chi tiết hơn trong tương lai.
>
> Hạn chế thứ tư là tập external P06-P07 đã được dùng trong quá trình phân tích lỗi và hiệu chỉnh threshold, nên chưa phải kiểm thử mù hoàn toàn độc lập. Để đánh giá khách quan hơn, cần thu thêm P08, P09 hoặc nhiều người mới khác làm tập external mới sau khi đã chốt mô hình.

### 8.4. Mục hướng phát triển

#### Đoạn copy vào Word

> Hướng phát triển tiếp theo là mở rộng dataset với nhiều người tham gia hơn, nhiều góc camera hơn, nhiều điều kiện ánh sáng và nhiều thiết bị webcam khác nhau. Đặc biệt, sau khi chốt mô hình, cần thu thêm một tập external mới gồm những người chưa từng xuất hiện trong quá trình train, phân tích lỗi hoặc hiệu chỉnh threshold để đánh giá khách quan hơn.
>
> Hướng phát triển thứ hai là chuẩn hóa quy trình gán nhãn. Các video nên được gán nhãn bởi ít nhất hai người độc lập, sau đó đối chiếu các trường hợp mâu thuẫn. Nếu có điều kiện, nên có sự tham vấn của chuyên gia công thái học, vật lý trị liệu hoặc y tế lao động để tăng độ tin cậy của nhãn.
>
> Hướng phát triển thứ ba là mở rộng bài toán từ phân loại nhị phân sang phân loại đa lớp hoặc đa nhãn, chẳng hạn cúi đầu, rụt cổ, nghiêng vai, nghiêng thân, gù lưng hoặc chống cằm. Khi đó, ứng dụng không chỉ cảnh báo sai tư thế mà còn đưa ra phản hồi cụ thể hơn cho người dùng.
>
> Hướng phát triển thứ tư là cải thiện module kiểm soát chất lượng đầu vào. Hệ thống cần phát hiện các trường hợp nhiều người xuất hiện trong khung hình, người ngồi quá gần camera, mất landmarks quan trọng hoặc cơ thể bị cắt khỏi khung hình. Những trường hợp này nên được cảnh báo là dữ liệu đầu vào không hợp lệ thay vì cố gắng phân loại.

---

## 9. Hình Cần Sửa Hoặc Thêm

### Hình 1 - Sơ đồ pipeline hệ thống

#### Vị trí nên đặt

Chương 3, sau đoạn mô tả kiến trúc tổng thể.

#### Nội dung cần có

```text
Webcam/IP camera/MP4
    -> OpenCV frame capture
    -> MediaPipe Pose landmarks
    -> Feature construction
        -> raw_99
        -> normalized_99
        -> ergonomic_v2_with_view
    -> Classifier
        -> ANN
        -> HGB balanced best
        -> HGB high recall demo
        -> Rule-based
    -> Temporal smoothing + threshold
    -> Warning
    -> SQLite logging + dashboard
```

#### Caption

> Hình 3.x. Kiến trúc xử lý của hệ thống phát hiện lỗi tư thế làm việc qua webcam.

### Hình 2 - Sơ đồ chia dataset

#### Vị trí nên đặt

Chương 4, mục Dữ liệu và giao thức thực nghiệm.

#### Nội dung cần có

```text
117 videos
    -> Development set: 94 videos, P01-P05, 12.680 samples
    -> External set: 23 videos, P06-P07, 4.556 samples
```

#### Caption

> Hình 4.x. Cách tổ chức tập phát triển và tập external trong thực nghiệm.

### Hình 3 - Confusion matrix mới

#### Vị trí nên đặt

Chương 4, sau bảng final selected model.

#### Số liệu phải dùng

```text
TN = 1.846
FP = 155
FN = 332
TP = 2.223
```

#### Caption

> Hình 4.x. Ma trận nhầm lẫn của HistGradientBoosting `ergonomic_v2_with_view` trên external P06-P07.

### Hình 4 - Threshold calibration mới

#### Vị trí nên đặt

Chương 4, sau bảng threshold calibration.

#### Nội dung cần có

- Trục x: threshold.
- Trục y: F1 Incorrect hoặc Precision/Recall/F1.
- Đánh dấu threshold 0,76.

#### Caption

> Hình 4.x. Khảo sát threshold của model selected trên external P06-P07.

### Hình 5 - Screenshot app có model selector mới

#### Vị trí nên đặt

Chương 3 hoặc Chương 4 phần kiểm thử chức năng app.

#### Nội dung screenshot nên có

Combobox model nên hiện được các lựa chọn:

- ANN.
- HistGradientBoosting (balanced best).
- HistGradientBoosting (high recall demo).
- Rule-based Baseline.

#### Caption

> Hình 4.x. Giao diện ứng dụng desktop với các chế độ nhận diện tư thế.

---

## 10. Bảng Cần Sửa Hoặc Thêm

| Bảng | Vị trí | Trạng thái hiện tại | Việc cần làm |
| --- | --- | --- | --- |
| Bảng 4.1 Môi trường thực nghiệm | Chương 4 | Có thể giữ phần lớn | Sửa câu ANN train Kaggle thành ANN đã train lại local trên CSV mới |
| Bảng 4.2 Thống kê dữ liệu | Chương 4 | Đang dùng 11.022 và 1.658 mẫu cũ | Thay bằng bảng 94/23 video, 12.680/4.556 mẫu |
| Bảng 4.4 Kịch bản đánh giá | Chương 4 | Còn cách gọi corrected external/P01 | Sửa thành external P06-P07 |
| Bảng benchmark model | Chương 4 | Đang dùng kết quả cũ 90-96% | Thay bằng bảng HGB selected 89,31%, ANN 79,10% |
| Bảng final selected model | Chương 4 | Đang ghi HGB normalized_99 threshold 0,65 | Thay bằng HGB ergonomic_v2_with_view threshold 0,76 |
| Bảng threshold | Chương 4 | Đang dùng threshold cũ | Thay bằng threshold 0,70-0,80 |
| Bảng internal vs external | Chương 4 | Không còn đồng nhất | Nên bỏ hoặc thay bằng đoạn giải thích |
| Bảng participant-wise | Chương 4 | Đang dùng P01-P05 cũ | Thay bằng P06/P07 external hoặc chạy lại leave-one P01-P05 |
| Bảng video-wise | Chương 4 | Đang dùng P01 external cũ | Thay bằng P06/P07 video khó |
| Bảng runtime | Chương 4 | Có thể giữ | Thêm chú thích đây là core processing FPS |
| Bảng kiểm thử app | Chương 4 | Cần cập nhật HGB mode | Thêm 2 mode HGB mới |
| Bảng kết quả đạt được | Chương 5 | Đang dùng 84/10 video và kết quả cũ | Thay bằng bảng 117 video, HGB 89,31%, ANN 79,10% |

---

## 11. Thứ Tự Sửa Word Để Không Bị Rối

1. Sửa toàn bộ Chương 4 trước, vì đây là nơi chứa nhiều số liệu cũ nhất.
2. Thay Bảng 4.2 dataset.
3. Thay bảng benchmark model.
4. Thay bảng final selected model.
5. Thay bảng threshold calibration.
6. Thay hình confusion matrix và hình threshold nếu đang dùng hình cũ.
7. Thay bảng participant-wise và video-wise.
8. Sửa Chương 5 kết luận và hướng phát triển.
9. Quay lại Chương 1 sửa các câu có tính “sau khi bổ sung dữ liệu”.
10. Sửa Chương 3 phần model/app để khớp app hiện tại.
11. Cập nhật danh mục bảng và danh mục hình trong Word.
12. Đọc lại toàn bộ luận văn để đảm bảo không còn số cũ: 84, 10 external, 11.022, 1.658, P01-only, 96,50%.

---

## 12. Đoạn Trả Lời Khi Thầy Hỏi Vì Sao Số Mới Thấp Hơn Số Cũ

> Dạ, số mới thấp hơn vì protocol mới chặt hơn. Trước đây external set nhỏ hơn và chưa thật sự đại diện cho người mới. Sau khi tổ chức lại dữ liệu, em dùng P01-P05 làm tập phát triển và P06-P07 làm external test, tức là người trong external không xuất hiện trong train. Vì vậy kết quả 89,31% Accuracy và 90,13% F1 lớp sai phản ánh thực tế hơn khả năng tổng quát trên người mới. Em không giữ số 96,50% cũ vì số đó thuộc protocol cũ, không còn phù hợp với dataset và giao thức đánh giá hiện tại.

## 13. Đoạn Trả Lời Khi Thầy Hỏi Vì Sao Không Chọn ANN

> Dạ, ban đầu em có xây dựng ANN/Keras vì ANN có khả năng học quan hệ phi tuyến giữa các đặc trưng landmark. Tuy nhiên, sau khi mở rộng dataset và đánh giá lại trên external P06-P07, ANN tốt nhất chỉ đạt Accuracy 79,10% và F1 lớp sai 79,44%, thấp hơn HistGradientBoosting với Accuracy 89,31% và F1 lớp sai 90,13%. Vì vậy, em vẫn giữ ANN như baseline mạng nơ-ron để so sánh, còn mô hình khuyến nghị cuối cùng được chọn dựa trên kết quả thực nghiệm là HistGradientBoosting.

## 14. Đoạn Trả Lời Khi Thầy Hỏi Vì Sao Không Dùng CNN

> Dạ, em không dùng CNN trực tiếp trên ảnh vì hướng của đề tài là sử dụng MediaPipe Pose để trích xuất landmark cơ thể. Sau bước này, dữ liệu không còn là ảnh thô mà là dữ liệu dạng bảng gồm tọa độ, góc, khoảng cách và tỷ lệ hình học. Với dạng dữ liệu này, HistGradientBoosting phù hợp hơn CNN vì nhẹ hơn, train nhanh hơn, ít cần dữ liệu lớn hơn và dễ chạy realtime trên desktop. CNN end-to-end thường cần dataset ảnh lớn và đa dạng hơn để tránh overfitting, trong khi dataset của em hiện vẫn là dataset tự thu ở quy mô luận văn.

