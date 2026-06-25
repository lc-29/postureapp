# Phát hiện lỗi tư thế làm việc qua webcam sử dụng MediaPipe landmarks chuẩn hóa và học máy nhẹ

**Tác giả:** Ly-Cu Duong, Van-Phuc Vo  
**Đơn vị:** Nam Can Tho University, Can Tho, Vietnam

> Bản tiếng Việt này được viết để đối chiếu nội dung với `reports/springer_overleaf/main_revised.pdf`. Đây là bản dịch/diễn giải học thuật, không phải file nộp Springer chính thức. File nộp chính vẫn là bản tiếng Anh `main_revised.tex` hoặc `main_revised.pdf`.

## Tóm tắt

Tư thế ngồi sai khi làm việc với máy tính khó được theo dõi liên tục, trong khi nhiều hệ thống giám sát tư thế cần cảm biến áp lực, thiết bị đeo, ghế thông minh hoặc camera chiều sâu. Vì vậy, một hướng tiếp cận chi phí thấp dựa trên webcam có ý nghĩa khi mục tiêu là phản hồi trong môi trường desktop thông thường. Bài báo này trình bày một pipeline giám sát tư thế kết hợp OpenCV để đọc frame, MediaPipe Pose landmarks, đặc trưng landmark chuẩn hóa theo cơ thể, các chỉ báo hình học ergonomic và các mô hình học máy nhẹ.

Bộ dữ liệu tự thu gồm 84 video thô từ 5 người tham gia, tạo ra 11.022 frame được lấy mẫu với 4.438 mẫu Correct posture và 6.584 mẫu Incorrect posture; tập corrected external gồm 10 video và 1.658 frame. Trên tập corrected external, mô hình ANN/Keras đang dùng trong ứng dụng tăng F1 của lớp Incorrect từ 75,40% của rule-based baseline lên 90,34%, và tăng accuracy từ 67,49% lên 90,17%. Mô hình thực nghiệm được chọn, HistGradientBoosting với landmarks chuẩn hóa và ngưỡng 0,65, đạt accuracy 96,50%, F1 lớp Incorrect 96,76% và MCC 92,97%; kiểm thử runtime đạt 28,03-29,34 FPS.

Kết quả cho thấy giám sát tư thế qua webcam với cảnh báo và ghi log cục bộ là khả thi, nhưng độ đa dạng người tham gia, xác nhận ergonomic bởi chuyên gia và đánh giá public benchmark vẫn cần bổ sung.

**Từ khóa:** Working posture detection; MediaPipe Pose; Normalized landmarks; Lightweight machine learning; Webcam dataset

## 1. Giới thiệu

Làm việc lâu với máy tính có thể dẫn đến các lỗi tư thế kéo dài như đầu đưa về phía trước, lệch vai, rụt cổ và nghiêng thân trên. Các lỗi này thường xuất hiện không liên tục và người dùng không phải lúc nào cũng nhận ra trong quá trình học tập hoặc làm việc văn phòng. Các bài tổng quan gần đây về nhận diện tư thế ngồi và hệ thống phản hồi cũng cho thấy phương thức cảm biến, thiết kế phản hồi và protocol đánh giá ảnh hưởng mạnh đến tính hữu dụng thực tế. Vì vậy, một hệ thống giám sát thực tế nên cung cấp phản hồi bằng phần cứng sẵn có, chẳng hạn camera laptop hoặc webcam giá thấp.

Các nghiên cứu trước về nhận diện tư thế ngồi đã sử dụng đệm áp lực, ghế thông minh, cảm biến đeo hoặc cảm biến chuyển động, camera RGB-D và hệ thống camera RGB. Hệ thống dựa trên cảm biến có thể tạo phép đo tư thế chính xác, nhưng cần phần cứng chuyên dụng và ít phù hợp với triển khai desktop thông thường. Hệ thống RGB-D và depth camera cung cấp thông tin hình học phong phú hơn, nhưng vẫn giả định thiết bị mà nhiều người dùng không có. Các bài khảo sát cũng cho thấy các nghiên cứu nhận diện tư thế khác nhau đáng kể về nguồn dữ liệu, nhãn và protocol đánh giá. Hệ thống camera RGB và pose estimation giảm rào cản phần cứng, nhưng một pipeline desktop hoàn chỉnh vẫn cần xây dựng đặc trưng rõ ràng, baseline, so sánh mô hình, đánh giá runtime và ghi log để phân tích sau.

Bài báo này giải quyết khoảng trống đó bằng một hệ thống giám sát tư thế qua webcam. Hệ thống dùng OpenCV để đọc frame, MediaPipe Pose để trích xuất 33 body landmarks, đặc trưng landmark chuẩn hóa, các chỉ báo ergonomic có khả năng giải thích, rule-based baseline và các classifier học máy nhẹ. Phần triển khai cũng có cảnh báo thời gian thực và ghi log phiên làm việc bằng SQLite. Nghiên cứu đi theo hướng existing-model-plus-new-dataset/features. Bài báo không đề xuất pose estimation model mới và không đưa ra claim vượt trội tổng quát so với các nghiên cứu trước.

Các đóng góp chính gồm:

1. Một bộ dữ liệu webcam/video tự thu có metadata và nhãn project-specific Correct posture và Incorrect posture.
2. Một biểu diễn đặc trưng thống nhất để so sánh raw MediaPipe Pose landmarks, body-normalized landmarks, ergonomic geometric indicators và các nhóm đặc trưng kết hợp.
3. Một protocol đánh giá gồm rule-based baseline, ANN baseline, benchmark classifier, corrected external testing, participant-wise evaluation, threshold calibration, runtime FPS và tích hợp vào ứng dụng desktop.

## 2. Công trình liên quan

### 2.1 Nhận diện tư thế ngồi dựa trên cảm biến và camera chiều sâu

Các hệ thống dựa trên cảm biến thường dùng đệm áp lực, cảm biến lực, cảm biến quán tính hoặc ghế thông minh để suy luận tư thế ngồi. Tsai et al. báo cáo hiệu năng cao khi dùng cảm biến áp lực nhúng trong đệm ghế. Luna-Perejon et al. và Bourahmoune et al. cũng sử dụng cảm biến cùng mô hình neural hoặc machine learning cho phân loại tư thế ngồi. Feradov et al. nghiên cứu phát hiện tư thế ngồi sai bằng motion capture sensors. Các nghiên cứu này cho thấy cảm biến chuyên dụng có thể cung cấp tín hiệu tư thế hữu ích, nhưng chúng cần thiết bị bổ sung và không có sẵn với người dùng laptop thông thường.

Các phương pháp depth camera và RGB-D giảm nhu cầu đeo cảm biến nhưng vẫn dựa vào phần cứng hình ảnh đặc biệt. Kulikajevas et al. sử dụng chuỗi video RGB-D và deep learning cho nhận diện tư thế ngồi. Zeng et al. cũng nghiên cứu nhận diện tư thế ngồi từ ảnh chiều sâu. Các hệ thống này là baseline có giá trị cho phân tích tư thế, nhưng giả định phần cứng khác với bối cảnh giám sát chỉ bằng webcam. Khoảng trống của bài báo này là môi trường desktop chi phí thấp, nơi đầu vào chỉ là RGB webcam/video.

### 2.2 Nhận diện tư thế bằng camera RGB

Hệ thống camera RGB gần hơn với bối cảnh triển khai dự kiến. Estrada et al. dùng machine vision để mô hình hóa tư thế ngồi đúng và sai của người dùng máy tính. Chen sử dụng OpenPose cho nhận diện tư thế ngồi, cho thấy pose estimation có thể đóng vai trò biểu diễn trung gian cho phân loại tư thế. Các công trình này ủng hộ việc dùng đặc trưng pose thay vì chỉ phân loại ảnh thô.

Thách thức còn lại không chỉ là phát hiện tư thế từ frame RGB. Một hệ thống desktop có thể triển khai cần quản lý đọc frame, xây dựng đặc trưng, làm mượt dự đoán, cảnh báo và ghi log theo phiên. Hệ thống cũng cần baseline để diễn giải hiệu năng của mô hình so với các luật tư thế minh bạch. Bài báo này tập trung vào hướng end-to-end đó và giữ họ mô hình ở mức nhẹ.

### 2.3 Phân tích tư thế dựa trên pose landmark với OpenPose và MediaPipe

OpenPose giới thiệu phương pháp ước lượng tư thế 2D nhiều người thời gian thực bằng part affinity fields. MediaPipe cung cấp framework cho perception pipelines và hỗ trợ pose tracking hiệu quả trên thiết bị. MediaPipe Pose cũng đã được nghiên cứu như một biểu diễn human-pose thực tế trong phân tích chuyển động. MediaPipe Pose phù hợp với giám sát tư thế desktop vì trả về tập landmark gọn, có thể chuyển thành đặc trưng dạng bảng.

Các nghiên cứu và dataset gần đây tiếp tục hỗ trợ phân tích tư thế dựa trên landmarks. MultiPosture cung cấp body keypoints trích xuất bằng MediaPipe cho nhận diện tư thế ngồi. Carneros-Prado et al. so sánh các mô hình neural cho tác vụ nhận diện tư thế, trong khi Sahoo et al. báo cáo một framework IoT thời gian thực cho phát hiện tư thế ngồi. Các bài tổng quan của Nadeem et al., Krauter et al. và Roggio et al. mô tả sự đa dạng của sensing modalities, feedback mechanisms và validation protocols trong lĩnh vực này.

Khoảng trống được xử lý ở đây là cụ thể: các nghiên cứu trước chưa bao phủ đầy đủ một pipeline desktop chỉ dùng webcam, kết hợp MediaPipe Pose landmarks, các nhóm đặc trưng normalized và ergonomic, rule-based baseline có khả năng giải thích, nhiều classifier nhẹ, calibrated external evaluation, runtime measurement và local logging. Bài báo này giải quyết khoảng trống đó mà không xem bản thân MediaPipe là đóng góp mới.

## 3. Phương pháp đề xuất

Đề xuất của bài báo là một hệ thống giám sát tư thế qua webcam có thể khả thi trong thực tế khi kết hợp normalized MediaPipe Pose landmarks, interpretable ergonomic features, so sánh classifier cục bộ, temporal smoothing và session logging trong một pipeline có thể tái lập. Hệ thống xử lý frame từ webcam, IP camera hoặc video MP4.

Luồng xử lý chính:

```text
Webcam/IP camera/MP4 video
-> OpenCV Frame Capture Module
-> Landmark Extraction Module: MediaPipe Pose
-> Feature Construction Module
-> Posture Classification Module
-> Temporal Smoothing Module
-> Warning and Logging Module
-> SQLite Session Logs
-> Dashboard Statistics Module
```

Các tên module này được dùng nhất quán trong mô tả phương pháp và Algorithm 1. Hệ thống đọc frame, trích xuất MediaPipe Pose landmarks, xây dựng đặc trưng tư thế, dự đoán nhãn tư thế, làm mượt điểm dự đoán, kích hoạt cảnh báo khi cần và lưu log.

### 3.1 Landmark Extraction Module

Với mỗi frame đầu vào, MediaPipe Pose ước lượng 33 body landmarks. Mỗi landmark cung cấp tọa độ ảnh chuẩn hóa và giá trị độ sâu tương đối. Vector landmark thô là:

```latex
\mathbf{x}_{raw} =
[x_0, y_0, z_0, x_1, y_1, z_1, \ldots, x_{32}, y_{32}, z_{32}]
```

Trong đó \(x_i\), \(y_i\) và \(z_i\) là tọa độ MediaPipe của landmark \(i\). Vector có 99 giá trị. Nếu không phát hiện được landmarks, frame được đánh dấu là không phát hiện người và không được xem là mẫu phân loại tư thế bình thường.

### 3.2 Feature Construction Module

Hệ thống dùng raw landmarks, normalized landmarks và ergonomic geometric indicators. Biểu diễn chuẩn hóa căn giữa cơ thể theo trung điểm vai và scale theo một đại lượng xấp xỉ kích thước cơ thể:

```latex
\mathbf{s}_{mid} = \frac{\mathbf{s}_{left} + \mathbf{s}_{right}}{2}
```

Trong đó \(\mathbf{s}_{left}\) và \(\mathbf{s}_{right}\) là điểm vai trái và vai phải trên mặt phẳng ảnh, còn \(\mathbf{s}_{mid}\) là trung điểm vai.

```latex
\alpha = \max(w_s, l_t, \epsilon)
```

Trong đó \(w_s\) là độ rộng vai, \(l_t\) là proxy cho độ dài thân trên và \(\epsilon\) giúp tránh chia cho 0.

```latex
\hat{x}_i = \frac{x_i - s_{mid,x}}{\alpha}, \quad
\hat{y}_i = \frac{y_i - s_{mid,y}}{\alpha}, \quad
\hat{z}_i = \frac{z_i}{\alpha}
```

Trong đó \(\hat{x}_i\), \(\hat{y}_i\) và \(\hat{z}_i\) là tọa độ chuẩn hóa của landmark \(i\), còn \(s_{mid,x}\) và \(s_{mid,y}\) là tọa độ trung điểm vai.

Các ergonomic features gồm shoulder vertical difference, shoulder tilt, torso lean, head horizontal offset, nose-to-shoulder vertical relation, neck compression, hand-to-mouth ratios, chin-rest indicator, shoulder width, torso length, head-to-shoulder distance và minimum hand-mouth ratio.

### 3.3 Posture Classification Module

Ứng dụng desktop hiện tại dùng ANN/Keras classifier với kiến trúc:

```text
Input -> Dense(128) -> BatchNorm -> Dropout
      -> Dense(64) -> BatchNorm -> Dropout
      -> Dense(32) -> Dropout
      -> Dense(1, sigmoid)
```

Đầu ra là xác suất Incorrect posture. Với xác suất \(p\) và ngưỡng \(\tau\), nhãn dự đoán là:

```latex
\hat{y} =
\begin{cases}
1, & p \ge \tau \\
0, & p < \tau
\end{cases}
```

Trong đó \(\hat{y}=1\) là Incorrect posture và \(\hat{y}=0\) là Correct posture. Ứng dụng nạp ANN từ `ann_best.keras` và scaler từ `scaler.pkl`.

Protocol thực nghiệm cũng đánh giá Logistic Regression, SVM RBF, Random Forest, MLP sklearn và HistGradientBoosting. Trong protocol hiện tại, `hist_gradient_boosting__normalized_99` với threshold 0,65 là selected experimental model. Mô hình này không được mô tả là model đang triển khai trong ứng dụng nếu chưa được tích hợp sau này.

### 3.4 Rule-Based Baseline Module

Rule-based baseline dùng các ngưỡng hình học được định nghĩa thủ công. Baseline kiểm tra shoulder imbalance, shoulder tilt, torso lean, head offset, nose-to-shoulder relation, neck compression và hand-to-mouth proximity. Một frame được gán Incorrect posture khi một hoặc nhiều luật cho thấy rủi ro.

Baseline được dùng để so sánh vì có khả năng giải thích và không cần training. Nó cũng giúp cho thấy learned classifiers cải thiện như thế nào so với các geometric thresholds minh bạch.

**Table 1. Các rule và threshold của rule-based baseline**

| Rule indicator | Điều kiện | Threshold | Ý nghĩa |
|---|---|---:|---|
| Visibility gate | mean visibility < threshold | 0,50 | Pose có độ tin cậy thấp không được phân loại |
| Shoulder vertical difference | `shoulder_y_diff` > threshold | 0,06 | Dấu hiệu lệch vai |
| Shoulder tilt | `shoulder_tilt_angle` > threshold | 10,0 độ | Đường vai bị nghiêng |
| Torso lean | `torso_lean_angle` > threshold | 12,0 độ | Thân trên nghiêng lệch |
| Head offset | `head_offset_x` > threshold | 0,10 | Mũi lệch khỏi trung điểm vai |
| Neck compression | `nose_shoulder_clearance_ratio` < threshold | 0,12 | Mũi gần ngang vai, rụt cổ sâu |
| Hand-mouth ratio | hand-mouth ratio < threshold | 0,45 | Tay gần miệng/cằm |
| Hand-mouth distance | hand-mouth distance < threshold | 0,13 | Khoảng cách tuyệt đối tay-miệng nhỏ |
| Hand visibility gate | hand landmark visibility < threshold | 0,35 | Bỏ qua hand landmarks có độ tin cậy thấp |

Các threshold này là giá trị heuristic dùng cho baseline so sánh, không phải tiêu chuẩn ergonomic lâm sàng.

### 3.5 Temporal Smoothing and Logging

Xác suất Incorrect được làm mượt trên một cửa sổ frame ngắn. Warning event chỉ được kích hoạt nếu giá trị sau làm mượt vượt ngưỡng trong thời lượng yêu cầu. Cooldown interval giảm cảnh báo lặp lại cho cùng một posture episode. Log entries được lưu trong SQLite với thông tin session, posture, warning, frame, confidence và FPS.

**Algorithm 1. Phát hiện lỗi tư thế làm việc thời gian thực**

1. Khởi tạo video capture, MediaPipe Pose, probability buffer và SQLite session.
2. Với mỗi frame, phát hiện MediaPipe Pose landmarks.
3. Nếu không có landmarks, gán trạng thái no-person và lưu log.
4. Xây dựng raw, normalized hoặc ergonomic features.
5. Áp dụng scaler nếu classifier yêu cầu.
6. Dự đoán \(p_{incorrect}\), thêm vào smoothing buffer và tính smoothed probability.
7. Gán Incorrect posture nếu smoothed probability vượt decision threshold; ngược lại gán Correct posture.
8. Kích hoạt cảnh báo nếu incorrect-duration và cooldown thỏa điều kiện.
9. Vẽ landmarks/trạng thái lên frame, sau đó lưu log vào SQLite.
10. Đóng capture và kết thúc session khi dừng xử lý.

Runtime được báo cáo bằng FPS:

```latex
FPS = \frac{N}{T}
```

Trong đó \(N\) là số frame đã xử lý và \(T\) là thời gian xử lý tính bằng giây.

## 4. Dataset and Feature Extraction

Dữ liệu được thu cho tác vụ phát hiện lỗi tư thế làm việc nhị phân của project. Nhãn là project-specific và gồm hai lớp: Correct posture và Incorrect posture. Trong các artifact hiện có của project, nhãn được gán ở giai đoạn tạo video/sample theo posture class của nguồn video. Artifact không cung cấp protocol annotation độc lập bởi chuyên gia, inter-rater agreement hoặc ergonomic scoring theo RULA/REBA. Vì vậy, nhãn được xem là nhãn nhị phân project-specific, không phải expert ergonomic ground truth.

Development set gồm 84 raw videos từ 5 người tham gia, P01-P05. Frame được lấy mẫu ở 2 FPS, tạo ra 11.022 samples. Corrected external set gồm 10 videos từ P01 và 1.658 samples. Tập external này hữu ích cho đánh giá corrected đầu tiên, nhưng bị giới hạn vì chỉ gồm một người tham gia.

**Table 2. Các split dữ liệu dùng trong thực nghiệm**

| Split | Videos | Participants | Samples | Correct | Incorrect |
|---|---:|---:|---:|---:|---:|
| Development/training set | 84 | 5 | 11.022 | 4.438 (40,26%) | 6.584 (59,74%) |
| Corrected external set | 10 | 1 | 1.658 | 768 (46,32%) | 890 (53,68%) |

Bảng trên được trình bày theo split thay vì theo tên file. Development set hỗ trợ training, classifier comparison và participant-wise evaluation. Corrected external set hỗ trợ kết quả frame-level external chính. Full video manifest gồm 94 videos, trong đó có 84 development videos và 10 corrected external videos. Ở mức video, 39 videos được gán Correct và 55 videos được gán Incorrect.

Các metadata fields gồm `source_video`, `frame_index`, `timestamp_sec`, `sample_fps`, `video_fps`, `participant_id`, `view_angle` và `camera_type`. Những trường này hỗ trợ video-wise analysis và participant-wise validation.

**Table 3. Các nhóm feature dùng trong protocol thực nghiệm**

| Feature group | Số feature | Mô tả | Vai trò |
|---|---:|---|---|
| `raw_99` | 99 | 33 MediaPipe Pose landmarks với \(x\), \(y\), \(z\) | Biểu diễn landmark cơ bản |
| `normalized_99` | 99 | Raw landmarks được căn theo trung điểm vai và scale theo kích thước cơ thể | Giảm bias do kích thước cơ thể và khoảng cách camera |
| `ergonomic_14` | 14 | Các chỉ báo hình học liên quan vai, thân, đầu, cổ và tay-miệng | Posture cues có khả năng giải thích |
| `combined_raw_ergonomic` | 113 | Raw landmarks kết hợp ergonomic indicators | Kiểm tra raw landmarks cùng explicit posture cues |
| `combined_normalized_ergonomic` | 113 | Normalized landmarks kết hợp ergonomic indicators | Kiểm tra normalized landmarks cùng explicit posture cues |

**Table 4. Định nghĩa ergonomic/geometric features**

| Feature | Định nghĩa | Landmarks chính | Mục đích |
|---|---|---|---|
| `shoulder_width` | Khoảng cách 2D giữa hai vai | left/right shoulders | Proxy kích thước cơ thể |
| `torso_length` | Khoảng cách từ trung điểm vai đến trung điểm hông | shoulders, hips | Proxy chiều dài thân |
| `shoulder_y_diff` | Độ lệch dọc tuyệt đối giữa hai vai | left/right shoulders | Phát hiện lệch vai |
| `shoulder_tilt_angle` | Góc đường vai so với phương ngang | left/right shoulders | Phát hiện nghiêng vai |
| `torso_lean_angle` | Góc giữa trục vai-hông và phương dọc | shoulders, hips | Phát hiện nghiêng thân trên |
| `head_offset_x` | Độ lệch ngang của mũi so với trung điểm vai | nose, shoulders | Phát hiện lệch đầu |
| `nose_to_shoulder_y` | Vị trí dọc của mũi so với trung điểm vai | nose, shoulders | Quan hệ đầu/cổ |
| `nose_shoulder_clearance_ratio` | Khoảng cách mũi-vai chia cho chiều cao thân | nose, shoulders, hips | Dấu hiệu rụt cổ |
| `neck_compression_detected` | Cờ nhị phân khi clearance ratio < 0,12 | nose, shoulders, hips | Rụt cổ sâu |
| `left/right_hand_mouth_ratio` | Khoảng cách tay-miệng chia cho độ rộng vai | wrists/fingers, mouth, shoulders | Tay gần miệng/cằm |
| `chin_rest_detected` | Cờ nhị phân từ hand-mouth proximity | wrists/fingers, mouth | Chống cằm/tay đỡ mặt |
| `head_shoulder_distance` | Khoảng cách 2D từ mũi đến trung điểm vai | nose, shoulders | Quan hệ đầu-thân |
| `min_hand_mouth_ratio` | Giá trị nhỏ nhất của left/right hand-mouth ratios | wrists/fingers, mouth, shoulders | Tay gần miệng nhất |

Các định nghĩa này dựa trên feature schema và code feature extraction hiện tại. MediaPipe visibility không nằm trong final tabular schema vì CSV 99 feature chỉ lưu \(x\), \(y\), \(z\).

## 5. Experimental Setup

Thực nghiệm được chạy bằng Python 3.11.9. Các thư viện chính được ghi nhận trong project gồm OpenCV 4.11.0, MediaPipe 0.10.21, NumPy 1.26.4, scikit-learn 1.6.1, TensorFlow 2.16.2, matplotlib, CustomTkinter, Pillow, joblib, pytest và statsmodels 0.14.6. Runtime scripts dùng input frames 640x360, MediaPipe model complexity 1 và tối đa 120 sampled frames cho mỗi video đại diện. Chi tiết phần cứng không được ghi trong artifact của project. Vì vậy, runtime được báo cáo như phép đo xử lý ở mức project, không phải hardware-normalized benchmark.

### 5.1 Evaluation Protocol

Các mô hình ứng viên gồm rule-based baseline, ANN/Keras, Logistic Regression, SVM RBF, Random Forest, MLP sklearn và HistGradientBoosting. ANN là model đang được tích hợp trong desktop app. HistGradientBoosting là selected experimental model tốt nhất theo registry protocol hiện tại.

Development set được dùng cho training và model registry comparison. Corrected external set không dùng để fit model. Tuy nhiên, script threshold calibration của project quét threshold trên corrected external set và chọn threshold 0,65 cho báo cáo cuối. Vì vậy, kết quả final selected model nên được hiểu là calibrated external performance, không phải strictly independent hold-out test. Participant-wise evaluation giữ lại từng người tham gia làm held-out participant. Frame-level random splits chỉ được xem là kết quả tham khảo vì các frame liền kề từ cùng video có thể giống nhau và làm kết quả optimistic.

Model selection dùng Incorrect-class F1 làm tiêu chí chính. Incorrect-class recall và MCC được dùng làm tie-breakers. Threshold calibration quét các decision thresholds và chọn threshold dùng trong final protocol. Selected experimental model là `hist_gradient_boosting__normalized_99` với threshold 0,65.

### 5.2 Evaluation Metrics

Trong định nghĩa metric, TP, TN, FP và FN lần lượt là true positives, true negatives, false positives và false negatives. Positive class là Incorrect posture.

```latex
Accuracy = \frac{TP + TN}{TP + TN + FP + FN}
```

Accuracy là tỷ lệ mẫu được phân loại đúng trên toàn bộ mẫu.

```latex
Precision = \frac{TP}{TP + FP}
```

Precision là tỷ lệ mẫu được dự đoán Incorrect và thực sự là Incorrect.

```latex
Recall = \frac{TP}{TP + FN}
```

Recall là tỷ lệ mẫu Incorrect thực sự được mô hình phát hiện.

```latex
F1 = \frac{2 \times Precision \times Recall}{Precision + Recall}
```

F1-score cân bằng Precision và Recall cho lớp Incorrect.

MCC cũng được báo cáo vì chỉ số này hữu ích hơn accuracy khi cân bằng lớp và loại lỗi có ý nghĩa. Corrected external set, participant-wise evaluation và video-wise analysis được xem là bằng chứng mạnh hơn random frame-level internal split.

## 6. Results and Discussion

### 6.1 Rule-Based Baseline and ANN Application Model

**Table 5. So sánh corrected external giữa rule-based baseline và ANN/Keras application model**

| Method | Accuracy | Precision Inc. | Recall Inc. | F1 Inc. | MCC |
|---|---:|---:|---:|---:|---:|
| Rule-based baseline | 67,49% | 63,49% | 92,81% | 75,40% | 37,56% |
| ANN/Keras application model | 90,17% | 95,61% | 85,62% | 90,34% | 80,90% |

ANN tăng Incorrect-class F1 từ 75,40% lên 90,34%. Accuracy tăng từ 67,49% lên 90,17%. Rule-based baseline có recall cao hơn, 92,81%, nhưng precision chỉ 63,49%, cho thấy có nhiều false warnings trên các frame Correct posture.

Baseline hữu ích như một tham chiếu có khả năng giải thích, nhưng các ngưỡng cố định khó thích nghi với góc camera, body scale và biến thiên tư thế tự nhiên. ANN giảm false warnings, nhưng recall lớp Incorrect thấp hơn rule-based baseline. Trade-off này quan trọng với hệ thống cảnh báo: recall cao giảm bỏ sót lỗi tư thế, còn precision cao giảm cảnh báo không cần thiết.

### 6.2 Classifier and Feature Comparison

**Table 6. Các tổ hợp classifier và feature đứng đầu trong model registry**

| Rank | Model | Feature group | Accuracy | Recall Inc. | F1 Inc. | MCC |
|---:|---|---|---:|---:|---:|---:|
| 1 | HistGradientBoosting | `normalized_99` | 95,96% | 97,53% | 96,28% | 91,89% |
| 2 | Random Forest | `normalized_99` | 95,90% | 97,87% | 96,24% | 91,79% |
| 3 | SVM RBF | `ergonomic_14` | 95,36% | 94,38% | 95,62% | 90,72% |
| 4 | SVM RBF | `normalized_99` | 94,51% | 97,30% | 95,01% | 89,04% |
| 5 | Random Forest | `combined_normalized_ergonomic` | 94,27% | 97,98% | 94,83% | 88,65% |

Hai mô hình đầu dùng `normalized_99`, cho thấy body normalization cải thiện external protocol hiện tại. SVM RBF chỉ dùng `ergonomic_14` cũng đạt F1 lớp Incorrect 95,62%, cho thấy các geometric indicators có khả năng giải thích vẫn mang thông tin tư thế hữu ích.

Kết quả này không hàm ý HistGradientBoosting tốt hơn các mô hình trong nghiên cứu khác. Nó chỉ cho thấy, dưới dataset và protocol hiện tại của project, normalized landmarks với HistGradientBoosting đứng đầu trong các cấu hình local đã kiểm thử.

### 6.3 Final Selected Model

Sau threshold calibration trên corrected external set, selected experimental model dùng threshold 0,65. Vì threshold được chọn trên cùng corrected external set, kết quả này được báo cáo là calibrated external performance, không phải strictly independent hold-out estimate.

**Table 7. Selected experimental model trên corrected external set**

| Model | Feature group | Threshold | Accuracy | Precision Inc. | Recall Inc. | F1 Inc. | MCC | FP | FN |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| HistGradientBoosting | `normalized_99` | 0,65 | 96,50% | 96,22% | 97,30% | 96,76% | 92,97% | 34 | 24 |

False positives là các frame Correct posture bị phân loại thành Incorrect posture. Chúng có thể gây cảnh báo không cần thiết. False negatives là các frame Incorrect posture bị phân loại thành Correct posture. Chúng quan trọng hơn với hệ thống cảnh báo sức khỏe vì là các lỗi tư thế bị bỏ sót. Threshold được chọn giữ Incorrect-class recall trên 97,00% trong khi vẫn duy trì precision cao.

### 6.4 Participant-Wise Evaluation

**Table 8. Leave-one-participant-out evaluation trên raw dataset**

| Held-out participant | Samples | Accuracy | Precision Inc. | Recall Inc. | F1 Inc. | MCC |
|---|---:|---:|---:|---:|---:|---:|
| P01 | 3.524 | 90,81% | 98,28% | 84,88% | 91,09% | 82,64% |
| P02 | 1.225 | 79,35% | 77,87% | 91,55% | 84,16% | 56,55% |
| P03 | 2.208 | 93,03% | 99,85% | 90,05% | 94,70% | 85,55% |
| P04 | 1.815 | 86,67% | 79,37% | 100,00% | 88,50% | 75,92% |
| P05 | 2.250 | 93,56% | 95,63% | 94,24% | 94,93% | 86,11% |
| Mean | - | 88,68% | - | - | 90,67% | 77,35% |

Kết quả participant-wise mạnh hơn random internal frame split, nhưng vẫn dùng cùng project dataset. Corrected external set nhỏ hơn và chỉ chứa P01. Cần thêm external data độc lập với nhiều người tham gia hơn trước khi đưa ra claim tổng quát.

### 6.5 Runtime Evaluation

**Table 9. Runtime benchmark trên các video đại diện**

| View angle | Processed frames | Pose detection rate | Mean total latency | p95 latency | Estimated FPS |
|---|---:|---:|---:|---:|---:|
| front | 52 | 100,00% | 35,31 ms | 38,80 ms | 28,32 |
| side_30 | 120 | 100,00% | 35,67 ms | 43,08 ms | 28,03 |
| side_90 | 120 | 100,00% | 34,08 ms | 38,95 ms | 29,34 |

FPS đo được hỗ trợ tính khả thi real-time của core pipeline. Ứng dụng đầy đủ có thể chậm hơn vì drawing, Tkinter scheduling, camera buffering, audio playback và database logging tạo thêm overhead. Full GUI FPS nên được đo trong thí nghiệm tiếp theo.

### 6.6 Error and Temporal Behavior

Selected experimental model có 34 false positives và 24 false negatives trên corrected external set. Các exported error cases trong project artifact cho thấy hai nhóm lặp lại: label-boundary hoặc camera-angle cases, và ambiguous hoặc unseen posture types. Các trường hợp này phù hợp với external set nhỏ và nhãn nhị phân.

Temporal smoothing được dùng để ổn định cảnh báo, không phải để claim classifier mới. Hình temporal smoothing trong bản PDF thể hiện frame probability, temporal mean và decision threshold trên corrected external predictions. Nó giảm dao động dự đoán ngắn hạn và giúp tránh cảnh báo do frame đơn lẻ. Điều này phù hợp với ứng dụng desktop vì người dùng phản hồi với cảnh báo kéo dài, không phải nhãn của từng frame riêng lẻ.

### 6.7 Contextual Comparison with Literature

Literature gồm sensor-based systems, RGB-D systems, RGB camera systems và pose-landmark systems. Các metric được báo cáo trong literature không thể so sánh trực tiếp với project này vì khác input devices, participants, labels, datasets và split protocols. So sánh đúng trong bài là so sánh local: rule-based baseline với ANN trên cùng corrected external set, và các machine learning classifiers dưới cùng registry protocol. Literature values chỉ dùng để định vị phương pháp trong lĩnh vực posture recognition.

## 7. Desktop Application Implementation

Phần triển khai chứng minh pipeline có thể chạy như một ứng dụng desktop thay vì chỉ là offline script. Ứng dụng đọc webcam, IP camera hoặc MP4 input, hiển thị MediaPipe Pose landmarks chồng lên video frame, hiển thị trạng thái dự đoán, áp dụng smoothing và cooldown logic, phát warning sound khi điều kiện cấu hình được thỏa, và lưu session logs.

SQLite được dùng để lưu cục bộ. Database gồm user settings, working sessions, posture logs, daily statistics và model information. Trong database hiện tại của project có 64 sessions, 989 posture log entries và 10 daily statistics records. Các log này hỗ trợ session-level analysis và dashboard statistics.

Ứng dụng được dùng để kiểm chứng triển khai thời gian thực của pipeline đề xuất và không được đánh giá như một sản phẩm thương mại. Phần implementation này được đưa vào để thể hiện system feasibility và reproducibility. Các chi tiết giao diện như theme switching không được xem là đóng góp khoa học.

## 8. Limitations

Development dataset gồm 5 người tham gia, và corrected external set hiện chỉ gồm P01. Vì vậy, kết quả chưa thể tổng quát hóa cho mọi người dùng, camera positions, lighting conditions hoặc workplace environments.

Nhãn Correct posture và Incorrect posture là project-specific. Nhãn chưa được xác nhận bằng expert ergonomic annotation hoặc đánh giá theo RULA/REBA.

Desktop app hiện dùng ANN/Keras mode. Best experimental model là HistGradientBoosting với normalized landmarks. Selected model cần được tích hợp vào app trước khi mô tả deployed application là đang dùng model đó.

Project chưa được đánh giá trên public benchmark như MultiPosture. Public benchmark evaluation cần kiểm tra license, label mapping và protocol có thể so sánh.

Runtime evaluation hiện đo processing latency. Full GUI FPS, bao gồm display updates, audio, camera buffering và SQLite logging, chưa được đo.

## Data, Code, and Ethics Note

Raw videos không được dự kiến công bố công khai vì có thể chứa người tham gia có thể nhận diện. Extracted landmark features có thể được chia sẻ sau khi ẩn danh nếu venue yêu cầu và nếu sự đồng ý của người tham gia cho phép. Dữ liệu thu thập chỉ được dùng cho đánh giá học thuật trong project này.

## 9. Kết luận và hướng phát triển

Bài báo này trình bày một hệ thống phát hiện lỗi tư thế làm việc qua webcam sử dụng MediaPipe Pose landmarks, normalized và ergonomic feature groups, rule-based comparison, lightweight machine learning classifiers và triển khai Python desktop. Nghiên cứu đi theo hướng existing-model-plus-new-dataset/features. Bài báo không đề xuất pose estimator mới hoặc deep learning architecture mới.

Project dataset gồm 84 raw videos từ 5 người tham gia và 11.022 sampled frames. Corrected external set gồm 10 videos và 1.658 frames. Trên external set này, ANN tăng Incorrect-class F1 từ 75,40% của rule-based baseline lên 90,34%. Selected experimental model, HistGradientBoosting với `normalized_99` và threshold 0,65, đạt accuracy 96,50%, Incorrect-class F1 96,76% và MCC 92,97%. Runtime testing đạt 28,03-29,34 FPS trên các video đại diện.

Các kết quả này cho thấy MediaPipe Pose landmarks và lightweight tabular classifiers có thể hỗ trợ một desktop posture warning pipeline chi phí thấp. Rule-based baseline vẫn hữu ích vì giải thích được posture cues, trong khi learned classifiers cải thiện phân loại dưới data protocol hiện tại. SQLite logging và dashboard statistics bổ sung bằng chứng theo phiên cho phân tích sau.

Future work nên mở rộng dataset với nhiều participants, camera positions, lighting conditions và working environments hơn. Expert ergonomic annotation hoặc RULA/REBA-inspired labeling nên được bổ sung nếu hệ thống được dùng cho diễn giải ergonomic mạnh hơn. MultiPosture dataset hoặc public benchmarks tương tự nên được đánh giá sau khi kiểm tra license và label mapping. Selected HistGradientBoosting model nên được tích hợp vào desktop app để behavior của ứng dụng khớp với experimental protocol. Cuối cùng, binary labels nên được mở rộng thành multi-class posture types khi có đủ dữ liệu gán nhãn.

## Tài liệu tham khảo

Bản tiếng Việt này giữ nội dung tham khảo theo bản tiếng Anh trong `main_revised.pdf`. Khi đối chiếu citation, dùng danh sách BibTeX chính tại:

- `reports/springer_overleaf/references.bib`

