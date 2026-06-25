# Phát hiện lỗi tư thế làm việc qua webcam sử dụng MediaPipe Pose và học máy nhẹ

## Tóm tắt

Làm việc với máy tính trong thời gian dài có thể dẫn đến các tư thế ngồi sai kéo dài, trong khi nhiều hệ thống giám sát tư thế hiện nay cần cảm biến đeo, đệm áp lực, camera chiều sâu hoặc phần cứng chuyên dụng. Báo cáo này trình bày một hệ thống desktop phát hiện lỗi tư thế làm việc qua webcam, sử dụng OpenCV, MediaPipe Pose landmarks, các đặc trưng tư thế được thiết kế, các mô hình học máy nhẹ và cơ chế cảnh báo thời gian thực. MediaPipe Pose được dùng để trích xuất 33 điểm mốc cơ thể từ webcam, IP camera hoặc video MP4. Hệ thống xây dựng đặc trưng landmark thô 99 chiều, đặc trưng landmark chuẩn hóa theo cơ thể và các chỉ báo hình học ergonomic liên quan đến độ lệch vai, độ nghiêng thân, vị trí đầu, rụt cổ và khoảng cách tay-miệng. Bộ dữ liệu tự thu gồm 84 video thô từ 5 người tham gia và 11.022 khung hình được lấy mẫu, gồm 4.438 mẫu Correct posture và 6.584 mẫu Incorrect posture. Tập kiểm thử ngoài sau hiệu chỉnh gồm 10 video và 1.658 khung hình. Ứng dụng desktop hiện tích hợp bộ phân loại ANN/Keras, trong khi quy trình thực nghiệm so sánh rule-based, ANN, Logistic Regression, SVM RBF, Random Forest, MLP và HistGradientBoosting. Trên tập kiểm thử ngoài, ANN đạt Accuracy 90,17% và F1 lớp Incorrect 90,34%, so với Accuracy 67,49% và F1 75,40% của baseline rule-based. Mô hình thực nghiệm tốt nhất, HistGradientBoosting với landmark chuẩn hóa và ngưỡng 0,65, đạt Accuracy 96,50%, F1 96,76% và MCC 92,97%. Đánh giá thời gian chạy đạt khoảng 28 FPS ở các góc nhìn đại diện.

## Từ khóa

Phát hiện tư thế làm việc; MediaPipe Pose; Ước lượng tư thế người; Học máy; Giám sát qua webcam

## 1. Giới thiệu

Tư thế làm việc sai trong quá trình sử dụng máy tính lâu dài là một vấn đề ergonomic phổ biến trong môi trường văn phòng, học tập và làm việc từ xa. Các trạng thái như cúi đầu, lệch vai, nghiêng thân hoặc rụt cổ có thể kéo dài mà người dùng không nhận ra ngay. Vì vậy, một hệ thống giám sát thực tế cần cung cấp phản hồi liên tục mà không yêu cầu thiết bị đeo hoặc phần cứng chuyên dụng gây bất tiện.

Các hệ thống nhận diện tư thế ngồi trước đây đã sử dụng cảm biến áp lực, ghế thông minh, cảm biến chuyển động, camera RGB-D và thị giác máy tính dựa trên camera. Các hệ thống dùng cảm biến và ghế thông minh có thể cho tín hiệu đo tốt, nhưng cần thêm thiết bị và khó áp dụng rộng rãi cho người dùng chỉ có laptop hoặc webcam thông thường (Tsai et al., 2023; Odesola et al., 2024). Các phương pháp dùng camera chiều sâu hoặc RGB-D khai thác được thông tin hình học phong phú hơn, nhưng phần cứng này không phải lúc nào cũng có sẵn trong môi trường làm việc hằng ngày (Kulikajevas et al., 2021). Các framework ước lượng tư thế gần đây như OpenPose và MediaPipe cho phép ước lượng landmark cơ thể từ video RGB thông thường (Cao et al., 2018; Lugaresi et al., 2019; Bazarevsky et al., 2020).

Đối với một ứng dụng desktop giám sát tư thế làm việc, vẫn còn khoảng trống giữa kết quả nhận diện và khả năng triển khai thực tế. Một hệ thống hữu ích cần kết hợp đầu vào webcam chi phí thấp, các chỉ báo tư thế có khả năng giải thích, mô hình học máy, baseline rõ ràng, cảnh báo thời gian thực và lưu lịch sử cục bộ để xem lại. Một số nghiên cứu đã báo cáo phân loại tư thế ngồi hoặc hệ thống phản hồi tư thế, nhưng chưa nhiều công trình trình bày đầy đủ một pipeline desktop gồm dữ liệu webcam/video tự thu, feature ablation, so sánh rule-based, benchmark classifier, đánh giá thời gian chạy và ghi log theo phiên trong cùng một hệ thống (Estrada et al., 2023; Nadeem et al., 2024; Krauter et al., 2024).

Nghiên cứu này đi theo hướng sử dụng mô hình và công cụ có sẵn kết hợp với bộ dữ liệu và đặc trưng tự xây dựng. Đóng góp của đề tài không phải là một mô hình ước lượng tư thế mới hoặc một kiến trúc deep learning mới. Thay vào đó, đóng góp chính là một pipeline ứng dụng có thể tái lập cho bài toán phát hiện lỗi tư thế làm việc qua webcam.

Các đóng góp chính gồm:

1. Một bộ dữ liệu webcam/video tự thu có metadata và nhãn nhị phân project-specific: Correct posture và Incorrect posture.
2. Một biểu diễn đặc trưng thống nhất dựa trên 33 landmark MediaPipe Pose, gồm đặc trưng 99 chiều thô, đặc trưng chuẩn hóa theo cơ thể và các chỉ báo hình học ergonomic.
3. Một quy trình đánh giá gồm baseline rule-based, ANN và các mô hình học máy cổ điển, kiểm thử ngoài sau hiệu chỉnh, đánh giá theo người, đo FPS thời gian chạy và tích hợp vào ứng dụng desktop Python.

## 2. Công trình liên quan

### 2.1 Nhận diện tư thế ngồi bằng cảm biến và camera chiều sâu

Nhận diện tư thế bằng cảm biến đã được nghiên cứu rộng rãi với đệm áp lực, cảm biến lực, thiết bị motion capture và ghế thông minh. Tsai et al. (2023) sử dụng cảm biến áp lực nhúng trong đệm ghế để nhận diện nhiều tư thế ngồi với độ chính xác cao. Luna-Perejon et al. (2021) cũng nghiên cứu phân loại tư thế ngồi bằng cảm biến áp lực và mạng neural nhân tạo. Feradov et al. (2022) phát hiện tư thế ngồi sai bằng cảm biến motion capture, trong khi Odesola et al. (2024) tổng quan các ghế cảm biến thông minh cho phát hiện, phân loại và giám sát tư thế ngồi.

Các hướng tiếp cận này có giá trị tham chiếu vì cho thấy tầm quan trọng của việc giám sát tư thế ngồi liên tục. Tuy nhiên, chúng phụ thuộc vào phần cứng chuyên dụng. Điều này hạn chế khả năng áp dụng trực tiếp cho sinh viên hoặc nhân viên văn phòng chỉ có camera laptop hoặc webcam giá rẻ. Các phương pháp dùng camera chiều sâu giảm nhu cầu đeo cảm biến nhưng vẫn cần thiết bị riêng. Ví dụ, Kulikajevas et al. (2021) sử dụng chuỗi ảnh RGB-D và deep learning để nhận diện tư thế ngồi. Các hệ thống như vậy cung cấp thông tin không gian tốt hơn webcam RGB, nhưng giả định phần cứng khác với ứng dụng desktop chi phí thấp.

### 2.2 Nhận diện tư thế bằng camera RGB

Nhận diện tư thế bằng camera RGB gần hơn với môi trường mục tiêu của nghiên cứu này. Estrada et al. (2023) mô hình hóa tư thế ngồi đúng và sai của người dùng máy tính bằng machine vision trong bối cảnh làm việc tại nhà. Công trình này có liên quan vì sử dụng đầu vào hình ảnh để giám sát tư thế thay vì cảm biến áp lực hoặc cảm biến đeo. Chen (2019) nghiên cứu nhận diện tư thế ngồi dựa trên OpenPose, cho thấy ước lượng tư thế cơ thể có thể được dùng như biểu diễn trung gian cho phân loại tư thế.

Các phương pháp dùng camera giúp giảm chi phí phần cứng, nhưng phải xử lý thay đổi góc camera, ánh sáng, kích thước người và độ ổn định của landmark. Trong dự án này, các vấn đề đó được xử lý bằng MediaPipe Pose landmarks, đặc trưng landmark chuẩn hóa và các chỉ báo hình học ergonomic. Hệ thống không được thiết kế như một bộ phân loại ảnh tổng quát; hệ thống tập trung vào đặc trưng dạng bảng trích xuất từ landmark và phù hợp với các mô hình học máy nhẹ.

### 2.3 Phân tích tư thế dựa trên pose landmark với OpenPose và MediaPipe

OpenPose giới thiệu phương pháp ước lượng tư thế 2D nhiều người thời gian thực bằng part affinity fields (Cao et al., 2018). MediaPipe sau đó cung cấp framework xây dựng perception pipeline và hỗ trợ theo dõi tư thế hiệu quả trên thiết bị (Lugaresi et al., 2019; Bazarevsky et al., 2020). MediaPipe Pose và các phương pháp dựa trên landmark phù hợp cho giám sát tư thế desktop vì cung cấp biểu diễn cơ thể gọn nhẹ mà không cần bộ phân loại ảnh lớn.

Các nghiên cứu gần đây cũng sử dụng pose landmark cho nhận diện và phản hồi tư thế ngồi. Bộ dữ liệu MultiPosture cung cấp keypoints cơ thể trích xuất bằng MediaPipe cho nhận diện tư thế ngồi đa nhiệm (Carneros Prado et al., 2024). Carneros-Prado et al. (2024) so sánh các mô hình neural cho nhận diện tư thế ngồi, trong khi Sahoo et al. (2026) đề xuất framework IoT thời gian thực cho phát hiện tư thế ngồi. Các bài tổng quan của Nadeem et al. (2024), Krauter et al. (2024), và Roggio et al. (2024) cho thấy nhận diện tư thế ngồi vẫn là chủ đề đang phát triển với nhiều loại cảm biến, cơ chế phản hồi và protocol đánh giá khác nhau.

So với các công trình trên, nghiên cứu này nhấn mạnh triển khai desktop end-to-end với đầu vào webcam/video, MediaPipe Pose landmarks, feature engineering có khả năng giải thích, baseline rule-based, benchmark classifier, đánh giá thời gian chạy và ghi log phiên làm việc bằng SQLite. Các kết quả trong literature chỉ được dùng làm bối cảnh so sánh vì dataset, nhãn, cảm biến và protocol đánh giá khác nhau.

## 3. Phương pháp đề xuất

Hệ thống giám sát tư thế qua webcam xử lý khung hình từ webcam, IP camera hoặc file video MP4. Mỗi frame được OpenCV đọc và đưa vào MediaPipe Pose để trích xuất landmark. Tọa độ landmark được chuyển thành vector đặc trưng và phân loại thành Correct posture hoặc Incorrect posture. Kết quả sau đó đi qua bước làm mượt thời gian, so sánh ngưỡng, logic cảnh báo và ghi log SQLite.

[Insert Fig. 1 here: System architecture of the proposed webcam-based posture monitoring system]

Fig. 1. Kiến trúc hệ thống giám sát tư thế làm việc qua webcam.

Các module xử lý gồm:

1. OpenCV Frame Capture Module.
2. Landmark Extraction Module.
3. Feature Construction Module.
4. Posture Classification Module.
5. Rule-Based Baseline Module.
6. Warning and Logging Module.
7. Dashboard Statistics Module.

### 3.1 Trích xuất landmark

Với mỗi frame đầu vào, MediaPipe Pose ước lượng 33 pose landmarks. Mỗi landmark gồm tọa độ ảnh chuẩn hóa và giá trị độ sâu tương đối. Biểu diễn landmark thô là:

```text
x_i, y_i, z_i,  i = 0, 1, ..., 32
```

Do đó, vector đặc trưng thô có 99 giá trị:

```latex
\mathbf{x}_{raw} =
[x_0, y_0, z_0, x_1, y_1, z_1, \ldots, x_{32}, y_{32}, z_{32}]
```

trong đó \(x_i\), \(y_i\), và \(z_i\) là tọa độ MediaPipe của landmark \(i\). Nếu không phát hiện được pose landmarks, frame được đánh dấu là không phát hiện người và không được phân loại như một mẫu tư thế bình thường.

### 3.2 Xây dựng đặc trưng

Hệ thống sử dụng ba nhóm đặc trưng chính. Nhóm thứ nhất, `raw_99`, gồm 99 tọa độ MediaPipe landmark thô. Nhóm thứ hai, `normalized_99`, chuẩn hóa landmark theo trung điểm vai và kích thước cơ thể. Nhóm thứ ba, `ergonomic_14`, gồm các chỉ báo hình học có thể giải thích liên quan đến rủi ro tư thế.

Trung điểm vai được định nghĩa như sau:

```latex
\mathbf{s}_{mid} = \frac{\mathbf{s}_{left} + \mathbf{s}_{right}}{2}
```

trong đó \(\mathbf{s}_{left}\) và \(\mathbf{s}_{right}\) là tọa độ landmark vai trái và vai phải trên mặt phẳng ảnh.

Hệ số scale cơ thể được tính bằng:

```latex
\alpha = \max(w_s, l_t, \epsilon)
```

trong đó \(w_s\) là độ rộng vai, \(l_t\) là đại lượng proxy cho chiều dài thân trên và \(\epsilon\) là hằng số nhỏ để tránh chia cho 0.

Tọa độ chuẩn hóa được tính như sau:

```latex
\hat{x}_i = \frac{x_i - s_{mid,x}}{\alpha}, \quad
\hat{y}_i = \frac{y_i - s_{mid,y}}{\alpha}, \quad
\hat{z}_i = \frac{z_i}{\alpha}
```

trong đó \(\hat{x}_i\), \(\hat{y}_i\), và \(\hat{z}_i\) là tọa độ chuẩn hóa của landmark \(i\), còn \(s_{mid,x}\), \(s_{mid,y}\) là tọa độ trung điểm vai.

[Insert Fig. 2 here: MediaPipe Pose landmarks and selected ergonomic indicators]

Fig. 2. MediaPipe Pose landmarks và các chỉ báo ergonomic được chọn để xây dựng đặc trưng tư thế.

### 3.3 Phân loại tư thế

Ứng dụng desktop hiện tại sử dụng bộ phân loại ANN/Keras. Kiến trúc ANN là:

```text
Input -> Dense(128) -> BatchNorm -> Dropout
      -> Dense(64) -> BatchNorm -> Dropout
      -> Dense(32) -> Dropout
      -> Dense(1, sigmoid)
```

Đầu ra là xác suất Incorrect posture. Với xác suất \(p\) và ngưỡng \(\tau\), nhãn dự đoán được tính:

```latex
\hat{y} =
\begin{cases}
1, & p \ge \tau \\
0, & p < \tau
\end{cases}
```

trong đó \(\hat{y}=1\) là Incorrect posture và \(\hat{y}=0\) là Correct posture. Trong ứng dụng hiện tại, mô hình ANN được nạp từ `ann_best.keras` và scaler được nạp từ `scaler.pkl`.

Quy trình thực nghiệm cũng huấn luyện và so sánh Logistic Regression, SVM RBF, Random Forest, MLP và HistGradientBoosting. Mô hình tốt nhất trong protocol hiện tại là `hist_gradient_boosting__normalized_99` với ngưỡng hiệu chỉnh 0,65. Mô hình này được báo cáo như mô hình thực nghiệm tốt nhất, còn ứng dụng desktop hiện tại được mô tả là đang dùng ANN mode nếu registry model chưa được tích hợp.

### 3.4 Baseline rule-based

Baseline rule-based được dùng để tạo mốc so sánh có khả năng giải thích. Baseline này dùng các chỉ báo hình học như độ lệch chiều cao vai, góc nghiêng vai, góc nghiêng thân, độ lệch ngang của đầu, vị trí dọc mũi so với vai, rụt cổ và khoảng cách tay-miệng. Nếu một hoặc nhiều chỉ báo vượt ngưỡng định trước, frame được phân loại là Incorrect posture.

Baseline rule-based không nhằm thay thế classifier. Nó là mốc tham chiếu minh bạch để cho thấy mô hình học máy cải thiện như thế nào so với các ngưỡng thủ công trên cùng tập kiểm thử ngoài.

### 3.5 Cảnh báo thời gian thực và ghi log

Xác suất dự đoán được làm mượt trên một cửa sổ frame ngắn. Cảnh báo chỉ được kích hoạt khi xác suất sau làm mượt vượt ngưỡng cấu hình trong một khoảng thời gian tối thiểu. Cơ chế cooldown ngăn cảnh báo âm thanh lặp lại quá dày. Hệ thống ghi thông tin phiên làm việc, thay đổi trạng thái tư thế, sự kiện cảnh báo, số frame, độ tin cậy và thống kê vào SQLite.

Tốc độ xử lý xấp xỉ được tính bằng:

```latex
FPS = \frac{N}{T}
```

trong đó \(N\) là số frame đã xử lý và \(T\) là thời gian xử lý tính bằng giây.

## 4. Dataset và trích xuất đặc trưng

Dataset trong nghiên cứu này là dataset project-specific, được thu cho bài toán phát hiện lỗi tư thế làm việc. Nhãn là nhị phân: Correct posture và Incorrect posture. Các nhãn này là nhãn project-specific và chưa được xác nhận độc lập bởi chuyên gia ergonomic.

Tập dữ liệu raw training gồm 84 video từ 5 người tham gia, P01 đến P05. File CSV lấy mẫu 2 FPS cho training gồm 11.022 mẫu frame-level, trong đó có 4.438 mẫu Correct posture và 6.584 mẫu Incorrect posture. Tập kiểm thử ngoài sau hiệu chỉnh gồm 10 video và 1.658 mẫu. Tập ngoài hữu ích cho kiểm chứng sơ bộ, nhưng hiện chỉ chứa P01.

Table 1. Phân bố dataset dùng trong thực nghiệm.

| Dataset file | Videos | Participants | Samples | Correct | Incorrect |
|---|---:|---:|---:|---:|---:|
| `posture_data.csv` | This information should be completed before submission | This information should be completed before submission | 5.377 | 2.169 (40,34%) | 3.208 (59,66%) |
| `posture_data_2fps.csv` | 84 | 5 | 11.022 | 4.438 (40,26%) | 6.584 (59,74%) |
| `posture_data_2fps_with_metadata.csv` | 84 | 5 | 11.022 | 4.438 (40,26%) | 6.584 (59,74%) |
| `posture_external_test_2fps_with_metadata.csv` | 10 | 1 | 1.658 | 768 (46,32%) | 890 (53,68%) |
| `video_manifest.csv` | 94 | 5 | This information should be completed before submission | 39 videos (41,49%) | 55 videos (58,51%) |

Các cột metadata gồm `source_video`, `frame_index`, `timestamp_sec`, `sample_fps`, `video_fps`, `participant_id`, `view_angle`, và `camera_type`. Các trường này hỗ trợ đánh giá theo video, phân tích theo người và kiểm tra lỗi.

Table 2. Các nhóm đặc trưng dùng trong thực nghiệm.

| Feature group | Số đặc trưng | Mô tả |
|---|---:|---|
| `raw_99` | 99 | 33 MediaPipe Pose landmarks, mỗi điểm gồm tọa độ \(x\), \(y\), và \(z\). |
| `normalized_99` | 99 | Landmark thô được chuẩn hóa theo trung điểm vai và kích thước cơ thể. |
| `ergonomic_14` | 14 | Các chỉ báo tư thế có thể giải thích, suy ra từ vai, thân, đầu, cổ và hình học tay-miệng. |
| `combined_raw_ergonomic` | 113 | 99 landmark thô kết hợp với chỉ báo ergonomic. |
| `combined_normalized_ergonomic` | 113 | 99 landmark chuẩn hóa kết hợp với chỉ báo ergonomic. |

Các chỉ báo ergonomic gồm `shoulder_y_diff`, `shoulder_tilt_angle`, `torso_lean_angle`, `head_offset_x`, `nose_to_shoulder_y`, `nose_shoulder_clearance_ratio`, `neck_compression_detected`, left and right hand-mouth ratios, `chin_rest_detected`, `shoulder_width`, `torso_length`, `head_shoulder_distance`, và `min_hand_mouth_ratio`.

[Insert Fig. 3 here: Feature construction pipeline from MediaPipe landmarks to raw, normalized, and ergonomic features]

Fig. 3. Pipeline xây dựng đặc trưng từ MediaPipe landmarks sang raw, normalized và ergonomic features.

## 5. Thiết lập thực nghiệm

Quy trình thực nghiệm đánh giá cả mô hình đang tích hợp trong ứng dụng và các classifier học máy bổ sung. Ứng dụng desktop hiện tại sử dụng mô hình ANN/Keras và scaler đã lưu. Quy trình nghiên cứu rộng hơn so sánh các mô hình:

1. Rule-based baseline.
2. ANN/Keras classifier.
3. Logistic Regression.
4. SVM RBF.
5. Random Forest.
6. MLP sklearn.
7. HistGradientBoosting.

Mô hình tốt nhất được chọn theo F1-score của lớp Incorrect, với recall của lớp Incorrect và MCC làm tiêu chí phụ khi cần. Mô hình được chọn trong protocol hiện tại là `hist_gradient_boosting__normalized_99`, với ngưỡng quyết định \(\tau = 0.65\).

Các độ đo gồm Accuracy, Precision, Recall, F1-score, MCC, confusion matrix, video-wise metrics, participant-wise metrics và runtime FPS. Với phân loại nhị phân, TP, TN, FP và FN lần lượt là true positives, true negatives, false positives và false negatives. Trong nghiên cứu này, lớp dương là Incorrect posture.

```latex
Accuracy = \frac{TP + TN}{TP + TN + FP + FN}
```

Accuracy đo tỷ lệ mẫu được phân loại đúng trên toàn bộ mẫu.

```latex
Precision = \frac{TP}{TP + FP}
```

Precision đo trong các mẫu được dự đoán là Incorrect posture, có bao nhiêu mẫu thật sự Incorrect.

```latex
Recall = \frac{TP}{TP + FN}
```

Recall đo trong các mẫu Incorrect posture thật, hệ thống phát hiện được bao nhiêu mẫu.

```latex
F1 = \frac{2 \times Precision \times Recall}{Precision + Recall}
```

F1-score cân bằng Precision và Recall cho lớp Incorrect posture.

Kết quả split frame-level nội bộ của ANN có thể lạc quan vì các frame liền kề trong cùng video thường có mẫu pose tương tự nhau. Vì vậy, tập kiểm thử ngoài sau hiệu chỉnh, phân tích theo video, đánh giá theo người và runtime evaluation quan trọng hơn khi báo cáo độ tin cậy của project.

## 6. Kết quả và thảo luận

### 6.1 Baseline rule-based và ANN classifier

Table 3 so sánh baseline rule-based và ANN/Keras classifier trên tập kiểm thử ngoài sau hiệu chỉnh. ANN cải thiện rõ Accuracy và F1-score so với baseline rule-based. Rule-based có recall cao vì các ngưỡng rộng phát hiện được nhiều mẫu Incorrect, nhưng cũng tạo nhiều cảnh báo sai, làm giảm precision và overall accuracy.

Table 3. Baseline rule-based và ANN classifier trên tập kiểm thử ngoài sau hiệu chỉnh.

| Method | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC |
|---|---:|---:|---:|---:|---:|
| Rule-based baseline | 67,49% | 63,49% | 92,81% | 75,40% | 37,56% |
| ANN/Keras classifier | 90,17% | 95,61% | 85,62% | 90,34% | 80,90% |

### 6.2 So sánh classifier và feature

Model registry so sánh nhiều classifier và nhiều nhóm đặc trưng. Table 4 trình bày 5 mô hình đứng đầu trước khi hiệu chỉnh ngưỡng cuối. Biểu diễn landmark chuẩn hóa đạt kết quả mạnh, cho thấy việc chuẩn hóa theo kích thước cơ thể giúp giảm bias do kích thước người và khoảng cách camera.

Table 4. Các tổ hợp classifier và feature đứng đầu trong model registry.

| Rank | Model | Feature group | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | HistGradientBoosting | `normalized_99` | 95,96% | 95,07% | 97,53% | 96,28% | 91,89% |
| 2 | Random Forest | `normalized_99` | 95,90% | 94,67% | 97,87% | 96,24% | 91,79% |
| 3 | SVM RBF | `ergonomic_14` | 95,36% | 96,89% | 94,38% | 95,62% | 90,72% |
| 4 | SVM RBF | `normalized_99` | 94,51% | 92,82% | 97,30% | 95,01% | 89,04% |
| 5 | Random Forest | `combined_normalized_ergonomic` | 94,27% | 91,89% | 97,98% | 94,83% | 88,65% |

Nhóm `ergonomic_14` đạt hiệu quả cạnh tranh khi dùng SVM RBF, dù chỉ có 14 chỉ báo có thể giải thích. Điều này hữu ích cho việc giải thích lỗi tư thế, trong khi landmark chuẩn hóa vẫn mạnh hơn cho mô hình cuối được chọn.

### 6.3 Mô hình cuối trên tập kiểm thử ngoài

Sau khi hiệu chỉnh ngưỡng, mô hình được chọn là HistGradientBoosting với `normalized_99` và ngưỡng 0,65. Table 5 trình bày kết quả frame-level trên tập kiểm thử ngoài sau hiệu chỉnh.

Table 5. Hiệu năng của mô hình cuối trên tập kiểm thử ngoài sau hiệu chỉnh.

| Model | Feature group | Threshold | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC | FP | FN |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| HistGradientBoosting | `normalized_99` | 0,65 | 96,50% | 96,22% | 97,30% | 96,76% | 92,97% | 34 | 24 |

[Insert Fig. 4 here: Confusion matrix of the final selected model on the corrected external set]

Fig. 4. Confusion matrix của mô hình cuối trên tập kiểm thử ngoài sau hiệu chỉnh.

Confusion matrix có 34 false positives và 24 false negatives. False positives là các frame Correct nhưng bị phân loại thành Incorrect posture. Trong ứng dụng thực tế, lỗi này có thể gây cảnh báo không cần thiết. False negatives là các frame Incorrect bị bỏ sót và quan trọng hơn đối với hệ thống phản hồi tư thế. Ngưỡng hiệu chỉnh được chọn để cân bằng hai loại lỗi này trong khi vẫn giữ recall cao cho lớp Incorrect.

### 6.4 Đánh giá theo người

Đánh giá theo người trên raw dataset được thực hiện bằng cách giữ từng participant làm tập kiểm thử. Table 6 trình bày kết quả theo participant. F1-score trung bình cho lớp Incorrect là 90,67%, nhưng hiệu năng thay đổi giữa các participant. P02 là participant khó nhất trong dataset hiện tại.

Table 6. Đánh giá leave-one-participant-out trên raw dataset.

| Held-out participant | Samples | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC |
|---|---:|---:|---:|---:|---:|---:|
| P01 | 3.524 | 90,81% | 98,28% | 84,88% | 91,09% | 82,64% |
| P02 | 1.225 | 79,35% | 77,87% | 91,55% | 84,16% | 56,55% |
| P03 | 2.208 | 93,03% | 99,85% | 90,05% | 94,70% | 85,55% |
| P04 | 1.815 | 86,67% | 79,37% | 100,00% | 88,50% | 75,92% |
| P05 | 2.250 | 93,56% | 95,63% | 94,24% | 94,93% | 86,11% |
| Mean | - | 88,68% | - | - | 90,67% | 77,35% |

Kết quả này hỗ trợ tính tổng quát sơ bộ trong raw dataset tự thu. Tuy nhiên, nó không thay thế được đánh giá ngoài độc lập với nhiều participant hơn, vì tập external corrected hiện chỉ chứa P01.

### 6.5 Đánh giá thời gian chạy

Table 7 trình bày hiệu năng thời gian chạy trên các video đại diện ở góc front, side_30 và side_90. Tốc độ xử lý đo được xấp xỉ 28 FPS, đủ gần realtime cho demo desktop. Benchmark này chỉ đo processing latency; FPS toàn bộ GUI có thể thấp hơn do vẽ giao diện, lịch Tkinter, buffer camera, âm thanh và ghi database.

Table 7. Runtime benchmark trên các video đại diện.

| View angle | Processed frames | Pose detection rate | Mean total latency | p95 latency | Estimated FPS |
|---|---:|---:|---:|---:|---:|
| front | 52 | 100,00% | 35,31 ms | 38,80 ms | 28,32 |
| side_30 | 120 | 100,00% | 35,67 ms | 43,08 ms | 28,03 |
| side_90 | 120 | 100,00% | 34,08 ms | 38,95 ms | 29,34 |

### 6.6 Thảo luận

Kết quả cho thấy các classifier học được hiệu quả hơn các ngưỡng tư thế thủ công trên tập kiểm thử ngoài sau hiệu chỉnh. Baseline rule-based vẫn có giá trị vì có khả năng giải thích và có thể chỉ ra các vấn đề hình học cụ thể như nghiêng vai, nghiêng thân, lệch đầu và rụt cổ. Tuy nhiên, các ngưỡng thủ công khó thích nghi với vị trí camera, tỷ lệ cơ thể và biến thiên tư thế tự nhiên.

ANN đang tích hợp trong ứng dụng hiện tại là một classifier realtime thực tế và vượt baseline rule-based. Quy trình thực nghiệm rộng hơn cho thấy mô hình HistGradientBoosting với landmark chuẩn hóa đạt kết quả tốt hơn trong evaluation hiện tại. Sự phân biệt này rất quan trọng: ứng dụng hiện dùng ANN mode, trong khi HistGradientBoosting là mô hình thực nghiệm tốt nhất và cần được tích hợp vào ứng dụng trước khi mô tả sản phẩm triển khai là đang dùng mô hình cuối.

Kết quả split frame-level nội bộ rất cao cần được diễn giải thận trọng vì random split theo frame có thể đánh giá quá lạc quan khi các frame liền kề giống nhau. Tập kiểm thử ngoài sau hiệu chỉnh, đánh giá theo người và phân tích lỗi theo video cung cấp bằng chứng hữu ích hơn cho báo cáo khoa học. Các kết quả trong literature không được xem là leaderboard vì các nghiên cứu liên quan dùng cảm biến, dataset, nhãn và protocol đánh giá khác nhau.

## 7. Triển khai ứng dụng desktop

Hệ thống được triển khai dưới dạng ứng dụng desktop Python. OpenCV được dùng để đọc webcam, IP camera và video MP4. MediaPipe Pose ước lượng landmarks, sau đó ứng dụng vẽ skeleton overlay lên frame hiển thị. Người dùng có thể chọn ANN mode hoặc rule-based mode, cấu hình thời gian cảnh báo, cooldown, smoothing window và decision threshold.

[Insert Fig. 5 here: Desktop application interface]

Fig. 5. Giao diện ứng dụng desktop với video preview, trạng thái dự đoán, control và truy cập thống kê.

Ứng dụng hiển thị trạng thái tư thế dự đoán, độ tin cậy, thời gian sai tư thế liên tục và số lần cảnh báo. Nếu Incorrect posture kéo dài quá thời gian cảnh báo cấu hình, hệ thống phát âm thanh cảnh báo `.wav`. Thiết lập cooldown ngăn một lỗi tư thế kích hoạt cảnh báo âm thanh quá nhiều lần.

SQLite được dùng để ghi log cục bộ. Database gồm các bảng `NguoiDung`, `CaiDat`, `PhienLamViec`, `NhatKyTuThe`, `ThongKeNgay`, và `ThongTinModel`. Database hiện có 64 phiên làm việc, 989 dòng nhật ký tư thế và 10 dòng thống kê ngày. Dashboard tổng hợp thời lượng phiên, phân bố trạng thái tư thế, số lần cảnh báo và xu hướng theo ngày. Ứng dụng cũng hỗ trợ light mode và dark mode.

[Insert Fig. 6 here: Statistics dashboard and SQLite logging flow]

Fig. 6. Dashboard thống kê và luồng ghi log SQLite của ứng dụng desktop.

## 8. Hạn chế

Dataset hiện tại vẫn còn hạn chế. Raw training set có 5 người tham gia, và tập kiểm thử ngoài sau hiệu chỉnh hiện chỉ chứa P01. Do đó, kết quả báo cáo chưa thể tổng quát cho mọi người dùng, môi trường làm việc, điều kiện ánh sáng, vị trí camera hoặc dáng người.

Nhãn Correct posture và Incorrect posture là nhãn project-specific. Các nhãn này chưa được xác nhận bởi chuyên gia ergonomic. Vì vậy, hệ thống hiện nên được xem như prototype cảnh báo tư thế, không phải công cụ đánh giá lâm sàng hoặc ergonomic chính thức.

Ứng dụng desktop hiện sử dụng ANN mode, trong khi protocol thực nghiệm chọn HistGradientBoosting với landmark chuẩn hóa là mô hình tốt nhất. Mô hình được chọn cần được tích hợp vào ứng dụng trước khi mô tả hành vi sản phẩm là đang dùng mô hình thực nghiệm cuối.

Project chưa được đánh giá trên public benchmark như MultiPosture. Public dataset có thể giúp đánh giá khả năng tổng quát hóa, nhưng cần kiểm tra license và mapping nhãn trước khi dùng. Báo cáo này không đưa ra claim state-of-the-art.

Runtime benchmark hiện đo processing latency trên các video đại diện. FPS end-to-end của GUI có thể thấp hơn do rendering, lịch Tkinter, buffer camera, phát âm thanh và ghi log database.

## 9. Kết luận và hướng phát triển

Báo cáo này trình bày một hệ thống desktop phát hiện lỗi tư thế làm việc qua webcam, sử dụng OpenCV, MediaPipe Pose landmarks, các đặc trưng tư thế được thiết kế, các mô hình học máy nhẹ và cơ chế cảnh báo thời gian thực. Nghiên cứu đi theo hướng existing-model-plus-new-dataset/features. MediaPipe Pose cung cấp 33 landmarks cơ thể, và protocol feature của dự án so sánh landmark thô, landmark chuẩn hóa, các chỉ báo hình học ergonomic và các nhóm feature kết hợp.

Bộ dữ liệu tự thu gồm 84 video thô từ 5 người tham gia và 11.022 frame được lấy mẫu. Tập kiểm thử ngoài sau hiệu chỉnh gồm 10 video và 1.658 mẫu. Trên tập kiểm thử ngoài, mô hình ANN/Keras đang dùng trong ứng dụng đạt Accuracy 90,17% và F1-score lớp Incorrect 90,34%, vượt baseline rule-based trên cùng tập đánh giá. Mô hình thực nghiệm tốt nhất, HistGradientBoosting với normalized landmark features và ngưỡng 0,65, đạt Accuracy 96,50%, F1-score lớp Incorrect 96,76% và MCC 92,97%. Đánh giá thời gian chạy đạt khoảng 28 FPS trên các video đại diện ở góc front và side-view.

Kết quả cho thấy MediaPipe Pose landmarks và các mô hình học máy nhẹ có thể hỗ trợ một ứng dụng desktop cảnh báo tư thế thực tế. Baseline rule-based đem lại khả năng giải thích, trong khi classifier học máy cải thiện độ ổn định so với ngưỡng thủ công. Việc ghi log SQLite và dashboard thống kê cũng giúp hệ thống có khả năng xem lại hành vi tư thế theo phiên làm việc.

Hướng phát triển tiếp theo là mở rộng dataset với nhiều người tham gia hơn, nhiều vị trí camera, điều kiện ánh sáng và môi trường làm việc hơn. Nếu hệ thống cần diễn giải ergonomic mạnh hơn, cần bổ sung annotation từ chuyên gia hoặc nhãn theo hướng RULA/REBA. Public benchmark như MultiPosture nên được đánh giá sau khi kiểm tra license, định dạng feature và mapping nhãn. Mô hình thực nghiệm tốt nhất cần được tích hợp vào ứng dụng desktop để hành vi triển khai khớp với protocol nghiên cứu. Cuối cùng, nhãn nhị phân nên được mở rộng thành nhãn đa lớp khi có đủ dữ liệu, ví dụ forward head posture, shoulder imbalance, neck compression, torso leaning và chin-resting behavior.

## Tài liệu tham khảo

Aziz, M. H., & Mahmood, H. A. (2023). Automated body postures assessment from still images using Mediapipe. *Journal of Optimization and Decision Making, 2*(2), 240-246. https://izlik.org/JA28RM33TT

Bagga, E., & Yang, A. (2024). *Real-time posture monitoring and risk assessment for manual lifting tasks using MediaPipe and LSTM*. arXiv. https://arxiv.org/abs/2408.12796

Bazarevsky, V., Grishchenko, I., Raveendran, K., Zhu, T., Zhang, F., & Grundmann, M. (2020). *BlazePose: On-device real-time body pose tracking*. arXiv. https://doi.org/10.48550/arXiv.2006.10204

Bourahmoune, K., Ishac, K., & Amagasa, T. (2022). Intelligent posture training: Machine-learning-powered human sitting posture recognition based on a pressure-sensing IoT cushion. *Sensors, 22*(14), 5337. https://doi.org/10.3390/s22145337

Cao, Z., Hidalgo, G., Simon, T., Wei, S.-E., & Sheikh, Y. (2018). *OpenPose: Realtime multi-person 2D pose estimation using part affinity fields*. arXiv. https://doi.org/10.48550/arXiv.1812.08008

Carneros-Prado, D., Cabanero-Gomez, L., Johnson, E., Gonzalez, I., Fontecha, J., & Hervas, R. (2024). A comparison between multilayer perceptrons and Kolmogorov-Arnold networks for multi-task classification in sitting posture recognition. *IEEE Access, 12*, 180198-180209. https://doi.org/10.1109/ACCESS.2024.3510034

Carneros Prado, D., Cabanero Gomez, L., Fontecha, J., Hervas, R., Gonzalez Diaz, I., & Johnson, E. (2024). *MultiPosture: A dataset of body joints keypoints extracted using MediaPipe for multi-task sitting posture recognition with upper and lower body labels* (Version v1) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.14230872

Chen, K. (2019). Sitting posture recognition based on OpenPose. *IOP Conference Series: Materials Science and Engineering, 677*(3), 032057. https://doi.org/10.1088/1757-899X/677/3/032057

Estrada, J. E., Vea, L. A., & Devaraj, M. (2023). Modelling proper and improper sitting posture of computer users using machine vision for a human-computer intelligent interactive system during COVID-19. *Applied Sciences, 13*(9), 5402. https://doi.org/10.3390/app13095402

Feradov, F., Markova, V., & Ganchev, T. (2022). Automated detection of improper sitting postures in computer users based on motion capture sensors. *Computers, 11*(7), 116. https://doi.org/10.3390/computers11070116

Google AI Edge. (2026). *Pose landmark detection guide*. MediaPipe Solutions. https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker

Jiang, X., Hu, Z., Wang, S., & Zhang, Y. (2023). A survey on artificial intelligence in posture recognition. *Computer Modeling in Engineering & Sciences, 137*(1), 35-82. https://doi.org/10.32604/cmes.2023.027676

Kim, J.-W., Choi, J.-Y., Ha, E. J., & Choi, J.-H. (2023). Human pose estimation using MediaPipe Pose and optimization method based on a humanoid model. *Applied Sciences, 13*(4), 2700. https://doi.org/10.3390/app13042700

Krauter, C., Angerbauer, K., Sousa Calepso, A., Achberger, A., Mayer, S., & Sedlmair, M. (2024). Sitting posture recognition and feedback: A literature review. In *Proceedings of the CHI Conference on Human Factors in Computing Systems*. Association for Computing Machinery. https://doi.org/10.1145/3613904.3642657

Kulikajevas, A., Maskeliunas, R., & Damasevicius, R. (2021). Detection of sitting posture using hierarchical image composition and deep learning. *PeerJ Computer Science, 7*, e442. https://doi.org/10.7717/peerj-cs.442

Lugaresi, C., Tang, J., Nash, H., McClanahan, C., Uboweja, E., Hays, M., Zhang, F., Chang, C.-L., Yong, M. G., Lee, J., Chang, W.-T., Hua, W., Georg, M., & Grundmann, M. (2019). *MediaPipe: A framework for building perception pipelines*. arXiv. https://arxiv.org/abs/1906.08172

Nadeem, M., Elbasi, E., Zreikat, A. I., & Sharsheer, M. (2024). Sitting posture recognition systems: Comprehensive literature review and analysis. *Applied Sciences, 14*(18), 8557. https://doi.org/10.3390/app14188557

Odesola, D. F., Kulon, J., Verghese, S., Partlow, A., & Gibson, C. (2024). Smart sensing chairs for sitting posture detection, classification, and monitoring: A comprehensive review. *Sensors, 24*(9), 2940. https://doi.org/10.3390/s24092940

Roggio, F., Trovato, B., Sortino, M., & Musumeci, G. (2024). A comprehensive analysis of the machine learning pose estimation models used in human movement and posture analyses: A narrative review. *Heliyon, 10*(21), e39977. https://doi.org/10.1016/j.heliyon.2024.e39977

Sahoo, K. K., Patel, T., Swain, D., Gerogiannis, V. C., Kanavos, A., Singh, D. P., Kumar, M., & Acharya, B. (2026). ALIGN: An AI-driven IoT framework for real-time sitting posture detection. *Algorithms, 19*(1), 48. https://doi.org/10.3390/a19010048

Tsai, M.-C., Chu, E. T.-H., & Lee, C.-R. (2023). An automated sitting posture recognition system utilizing pressure sensors. *Sensors, 23*(13), 5894. https://doi.org/10.3390/s23135894

Wang, S., Tavares, A., Lima, C., Gomes, T., Zhang, Y., Zhao, J., & Liang, Y. (2025). LAViTSPose: A lightweight cascaded framework for robust sitting posture recognition via detection-segmentation-classification. *Entropy, 27*(12), 1196. https://doi.org/10.3390/e27121196

Zeng, X., Sun, B., Wang, E., Luo, W., & Liu, T. (2017). A method of learner's sitting posture recognition based on depth image. In *Proceedings of the 2017 2nd International Conference on Control, Automation and Artificial Intelligence (CAAI 2017)* (pp. 558-563). Atlantis Press. https://doi.org/10.2991/caai-17.2017.125
