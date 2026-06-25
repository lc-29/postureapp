# Phát hiện lỗi tư thế làm việc qua webcam sử dụng landmark MediaPipe chuẩn hóa và học máy nhẹ

## Tóm tắt

Tư thế ngồi sai khi làm việc với máy tính khó được theo dõi liên tục nếu không có phần cứng bổ sung. Bài báo này trình bày một hệ thống desktop ứng dụng phát hiện lỗi tư thế làm việc qua webcam, sử dụng MediaPipe Pose landmarks, đặc trưng chuẩn hóa theo cơ thể, các chỉ báo hình học ergonomic và các mô hình học máy nhẹ. Hệ thống đọc frame từ webcam, IP camera hoặc video MP4, trích xuất 33 landmarks bằng MediaPipe Pose, xây dựng các nhóm đặc trưng raw, normalized và ergonomic, phân loại tư thế đúng hoặc tư thế sai, làm mượt dự đoán theo thời gian, kích hoạt cảnh báo và lưu log phiên làm việc bằng SQLite. Bộ dữ liệu tự thu gồm 84 video thô từ 5 người tham gia, tạo ra 11.022 frame được lấy mẫu, trong đó có 4.438 mẫu tư thế đúng và 6.584 mẫu tư thế sai. Tập kiểm thử ngoài đã hiệu chỉnh gồm 10 video và 1.658 frame từ P01. Trên tập kiểm thử ngoài này, mô hình ANN/Keras trong ứng dụng tăng F1 của lớp tư thế sai từ 75,40% của baseline dựa trên luật lên 90,34%. Mô hình thực nghiệm được chọn, HistGradientBoosting với landmarks chuẩn hóa và ngưỡng 0,65, đạt Accuracy 96,50%, Precision 96,22%, Recall 97,30%, F1 96,76% cho lớp tư thế sai và MCC 92,97%. Đánh giá thời gian chạy đạt 28,03-29,34 FPS trên các góc nhìn đại diện. Kết quả cho thấy hướng giám sát tư thế chi phí thấp qua webcam là khả thi, nhưng độ đa dạng người tham gia, kiểm thử ngoài độc lập và xác nhận ergonomic bởi chuyên gia vẫn là các hạn chế.

## Từ khóa

Phát hiện tư thế làm việc; MediaPipe Pose; Ước lượng tư thế người; Học máy; Bộ dữ liệu webcam

## 1. Giới thiệu

Làm việc lâu với máy tính có thể dẫn đến các lỗi tư thế như cúi đầu về phía trước, lệch vai, rụt cổ và nghiêng thân trên. Những lỗi này thường xuất hiện dần trong quá trình học tập hoặc làm việc văn phòng, nên người dùng có thể không nhận ra cho đến khi có cảm giác khó chịu. Vì vậy, một hệ thống giám sát thực tế nên hoạt động với phần cứng sẵn có như camera laptop hoặc webcam giá rẻ, đồng thời đưa ra phản hồi mà không cần đệm áp lực, cảm biến đeo, ghế thông minh hoặc camera chiều sâu.

Các nghiên cứu trước về giám sát tư thế đã sử dụng cảm biến áp lực, cảm biến lực, thiết bị motion capture, ghế thông minh, camera RGB-D và hệ thống camera RGB. Hệ thống dựa trên cảm biến có thể đạt độ chính xác cao trong bối cảnh kiểm soát, nhưng cần phần cứng chuyên dụng và kém thuận tiện cho triển khai desktop thông thường (Luna-Perejon et al., 2021; Bourahmoune et al., 2022; Tsai et al., 2023; Odesola et al., 2024). Phương pháp dùng depth camera hoặc RGB-D cung cấp thông tin hình học phong phú hơn, nhưng vẫn giả định thiết bị mà nhiều người dùng không có (Zeng et al., 2017; Kulikajevas et al., 2021). Hệ thống RGB camera và pose estimation giảm rào cản phần cứng, nhưng một pipeline desktop hoàn chỉnh vẫn cần cách xây dựng đặc trưng rõ ràng, baseline minh bạch, so sánh mô hình, đánh giá thời gian chạy, logic cảnh báo và ghi log để phân tích sau.

Bài báo này đi theo hướng Nghiên cứu ứng dụng. Bài báo không đề xuất mô hình pose estimation mới và không khẳng định vượt trội tổng quát so với các nghiên cứu trước. Thay vào đó, nghiên cứu áp dụng mô hình có sẵn là MediaPipe Pose trên bộ dữ liệu webcam của project, đồng thời kiểm tra liệu đặc trưng landmarks chuẩn hóa, đặc trưng hình học ergonomic, phát hiện dựa trên luật và các classifier nhẹ có hỗ trợ được một hệ thống desktop giám sát tư thế hay không.

Các đóng góp chính gồm:

1. Một bộ dữ liệu webcam/video tự thu có metadata và nhãn project-specific gồm tư thế đúng và tư thế sai.
2. Một biểu diễn đặc trưng thống nhất, so sánh MediaPipe Pose landmarks thô, landmarks chuẩn hóa theo cơ thể, các chỉ báo hình học ergonomic và các nhóm đặc trưng kết hợp.
3. Một pipeline đánh giá và triển khai gồm baseline dựa trên luật, mô hình ANN/Keras trong ứng dụng, benchmark các classifier nhẹ, kiểm thử ngoài đã hiệu chỉnh, đánh giá theo người tham gia, hiệu chỉnh ngưỡng, runtime FPS, hành vi cảnh báo và ghi log SQLite.

## 2. Công trình liên quan

**Nhận diện tư thế dựa trên cảm biến và camera chiều sâu.** Các hệ thống tư thế dựa trên cảm biến thường dùng đệm áp lực, cảm biến lực, cảm biến quán tính hoặc ghế thông minh. Luna-Perejon et al. (2021) xây dựng thiết bị IoT phân loại tư thế ngồi bằng cảm biến lực và mạng neural. Bourahmoune et al. (2022) đề xuất hệ thống huấn luyện tư thế thông minh dựa trên đệm IoT cảm biến áp lực. Tsai et al. (2023) báo cáo hệ thống nhận diện tư thế ngồi tự động dùng cảm biến áp lực, còn Wang et al. (2022) nghiên cứu nhận diện tư thế ngồi bằng spiking neural network với dữ liệu áp lực. Các hệ thống này cho thấy cảm biến chuyên dụng có thể tạo tín hiệu tư thế hữu ích, nhưng làm tăng chi phí phần cứng và chưa phù hợp với bối cảnh desktop chỉ dùng webcam.

Các phương pháp dùng depth camera hoặc RGB-D giảm nhu cầu đeo cảm biến nhưng vẫn yêu cầu thiết bị hình ảnh đặc biệt. Zeng et al. (2017) nhận diện tư thế ngồi của người học từ ảnh chiều sâu. Kulikajevas et al. (2021) sử dụng chuỗi RGB-D và mô hình deep recurrent hierarchical cho nhận diện tư thế ngồi. Đây là các tham chiếu quan trọng cho phân tích tư thế bằng thị giác máy tính, nhưng giả định phần cứng khác với ứng dụng chỉ dùng webcam.

**Nhận diện tư thế bằng camera RGB và pose landmarks.** Hệ thống camera RGB gần hơn với bối cảnh laptop và văn phòng thông thường. Estrada et al. (2023) mô hình hóa tư thế ngồi đúng và sai của người dùng máy tính bằng machine vision. Chen (2019) dùng OpenPose cho nhận diện tư thế ngồi, cho thấy pose estimation có thể đóng vai trò biểu diễn trung gian cho phân loại tư thế. Chaikhamwang et al. (2025) nghiên cứu MediaPipe và computer vision cho giảm rủi ro office syndrome. Các nghiên cứu này củng cố hướng dùng visual landmarks thay vì chỉ phân loại ảnh thô.

Các phương pháp pose estimation tạo nền tảng kỹ thuật cho những hệ thống như vậy. OpenPose giới thiệu ước lượng tư thế 2D nhiều người theo thời gian thực bằng part affinity fields (Cao et al., 2019). MediaPipe cung cấp framework dạng graph cho perception pipelines (Lugaresi et al., 2019), trong khi BlazePose hỗ trợ theo dõi tư thế người theo thời gian thực trên thiết bị (Bazarevsky et al., 2020). MediaPipe Pose phù hợp với ứng dụng desktop nhẹ vì trả về tọa độ landmarks gọn, có thể chuyển thành đặc trưng dạng bảng. Tài liệu Google AI Edge chỉ được dùng như nguồn triển khai kỹ thuật cho pose landmarker, không thay thế Related Work học thuật.

**Review, dataset và bối cảnh ergonomic.** Các bài tổng quan gần đây mô tả sự đa dạng về cảm biến, dataset, chiến lược phản hồi và protocol đánh giá trong nhận diện tư thế (Jiang et al., 2023; Nadeem et al., 2024; Krauter et al., 2024; Roggio et al., 2024). Dataset MultiPosture cung cấp keypoints cơ thể trích xuất bằng MediaPipe cho nhận diện tư thế ngồi đa nhiệm (Carneros Prado et al., 2024), và Carneros-Prado et al. (2024) so sánh các mô hình neural cho bài toán này. Các phương pháp ergonomic như RULA và REBA vẫn liên quan cho hướng gán nhãn chuyên gia và diễn giải rủi ro trong tương lai (McAtamney and Corlett, 1993; Hignett and McAtamney, 2000), mặc dù project hiện chưa dùng điểm ergonomic chuyên gia làm nhãn.

Khoảng trống mà bài báo xử lý là một pipeline desktop chỉ dùng webcam, kết hợp MediaPipe Pose landmarks, các nhóm đặc trưng normalized và ergonomic, baseline dựa trên luật có khả năng giải thích, nhiều classifier nhẹ, đánh giá external có hiệu chỉnh, đo thời gian chạy, cảnh báo và ghi log cục bộ. Đóng góp nằm ở hệ thống ứng dụng và protocol đánh giá, không nằm ở bản thân MediaPipe.

## 3. Hệ thống giám sát tư thế qua webcam được đề xuất

Hệ thống xử lý đầu vào từ webcam, IP camera hoặc video MP4 theo một pipeline tuần tự. Trước hết, OpenCV Frame Capture Module đọc frame từ nguồn được chọn. Landmark Extraction Module sau đó áp dụng MediaPipe Pose để phát hiện 33 landmark cơ thể. Feature Construction Module chuyển các landmark này thành nhóm đặc trưng raw, normalized và ergonomic. Posture Classification Module ước lượng xác suất tư thế đúng hoặc tư thế sai. Temporal Smoothing Module giảm dao động ngắn hạn ở mức frame trước khi Warning and Logging Module kích hoạt cảnh báo khi điều kiện thời lượng và cooldown được thỏa mãn. Cuối cùng, SQLite Session Logs and Dashboard Statistics lưu thông tin tư thế theo phiên để phân tích sau. Fig. 1 tóm tắt luồng xử lý này.

Fig. 1. Kiến trúc hệ thống giám sát tư thế làm việc qua webcam.

**Trích xuất landmarks.** Với mỗi frame đầu vào, MediaPipe Pose ước lượng 33 landmarks cơ thể. Mỗi landmark gồm tọa độ ảnh chuẩn hóa và giá trị độ sâu tương đối. Vector landmark thô là:

```latex
\mathbf{x}_{raw} =
[x_0, y_0, z_0, x_1, y_1, z_1, \ldots, x_{32}, y_{32}, z_{32}]
```

Trong đó \(x_i\), \(y_i\), và \(z_i\) là tọa độ MediaPipe của landmark \(i\). Vector này có 99 giá trị. Nếu không phát hiện được landmarks, frame được xem là không phát hiện người thay vì là một mẫu phân loại tư thế bình thường.

**Xây dựng đặc trưng.** Hệ thống dùng ba nhóm đặc trưng chính. Nhóm `raw_99` chứa 33 landmarks với tọa độ \(x\), \(y\), và \(z\). Nhóm `normalized_99` đưa landmarks về gốc tại trung điểm vai và scale theo proxy kích thước cơ thể. Nhóm `ergonomic_14` gồm các chỉ báo hình học có khả năng giải thích liên quan đến đầu, cổ, vai, thân trên và quan hệ tay-miệng.

Trung điểm vai được tính như sau:

```latex
\mathbf{s}_{mid} = \frac{\mathbf{s}_{left} + \mathbf{s}_{right}}{2}
```

Trong đó \(\mathbf{s}_{left}\) và \(\mathbf{s}_{right}\) là điểm vai trái và vai phải trên mặt phẳng ảnh.

Hệ số scale cơ thể là:

```latex
\alpha = \max(w_s, l_t, \epsilon)
```

Trong đó \(w_s\) là độ rộng vai, \(l_t\) là proxy độ dài thân trên và \(\epsilon\) tránh chia cho 0.

Tọa độ landmark chuẩn hóa là:

```latex
\hat{x}_i = \frac{x_i - s_{mid,x}}{\alpha}, \quad
\hat{y}_i = \frac{y_i - s_{mid,y}}{\alpha}, \quad
\hat{z}_i = \frac{z_i}{\alpha}
```

Trong đó \(\hat{x}_i\), \(\hat{y}_i\), và \(\hat{z}_i\) là tọa độ chuẩn hóa của landmark \(i\). Các đặc trưng ergonomic gồm `shoulder_y_diff`, `shoulder_tilt_angle`, `torso_lean_angle`, `head_offset_x`, `nose_to_shoulder_y`, `nose_shoulder_clearance_ratio`, `neck_compression_detected`, các tỷ lệ tay-miệng, `chin_rest_detected`, `shoulder_width`, `torso_length`, `head_shoulder_distance`, và `min_hand_mouth_ratio`.

Fig. 2. Xây dựng đặc trưng từ MediaPipe Pose landmarks sang các nhóm raw, normalized, ergonomic và combined.

**Phân loại tư thế.** Mô hình ANN/Keras dùng trong ứng dụng là một mạng feed-forward gồm ba hidden layer. Hidden layer thứ nhất có 128 neuron, theo sau là Batch Normalization và Dropout. Hidden layer thứ hai có 64 neuron, cũng dùng Batch Normalization và Dropout. Hidden layer thứ ba có 32 neuron và Dropout. Output layer gồm một neuron sigmoid để ước lượng xác suất tư thế sai.

Đầu ra là xác suất tư thế sai. Với xác suất \(p\) và ngưỡng \(\tau\), nhãn dự đoán là:

```latex
\hat{y} =
\begin{cases}
1, & p \ge \tau \\
0, & p < \tau
\end{cases}
```

Trong đó \(\hat{y}=1\) là tư thế sai và \(\hat{y}=0\) là tư thế đúng. Ứng dụng nạp `ann_best.keras` và `scaler.pkl`. Bản demo desktop cũng đã có lựa chọn mô hình HistGradientBoosting tốt nhất, nhưng bài báo vẫn phân biệt rõ giữa mô hình ANN/Keras ban đầu trong app và mô hình thực nghiệm được chọn.

**Baseline dựa trên luật.** Baseline rule-based dùng các ngưỡng hình học thủ công. Nó kiểm tra lệch vai, nghiêng vai, nghiêng thân, lệch đầu, quan hệ mũi-vai, rụt cổ và khoảng cách tay-miệng. Một frame được gán tư thế sai khi một hoặc nhiều luật cho thấy rủi ro. Baseline này được giữ lại vì có khả năng giải thích và không cần huấn luyện.

**Làm mượt, cảnh báo và ghi log.** Xác suất tư thế sai được làm mượt trên một cửa sổ frame ngắn. Sự kiện cảnh báo chỉ được kích hoạt nếu xác suất sau làm mượt vượt ngưỡng trong thời lượng yêu cầu. Khoảng cooldown giảm cảnh báo lặp lại. SQLite lưu thông tin phiên, tư thế, cảnh báo, độ tin cậy, frame và thời gian. Database hiện tại có 64 phiên làm việc, 989 dòng log tư thế và 10 bản ghi thống kê ngày.

Vì vậy, luồng xử lý thời gian thực được mô tả ở mức module thay vì trình bày như mã triển khai: mỗi frame được đọc vào, landmarks được trích xuất, đặc trưng được xây dựng, classifier ước lượng xác suất tư thế sai, logic làm mượt và ngưỡng quyết định có kích hoạt cảnh báo hay không, sau đó trạng thái được lưu vào SQLite để phân tích theo phiên.
## 4. Quy trình thực nghiệm

Project đi theo protocol existing-model-plus-new-dataset/features. MediaPipe Pose được dùng như bộ trích xuất landmarks có sẵn, còn thực nghiệm so sánh các nhóm đặc trưng và classifier nhẹ trên dataset của project.

Table 1. Các split dữ liệu dùng trong thực nghiệm.

| Split | Video | Người tham gia | Số mẫu | Tư thế đúng | Tư thế sai |
|---|---:|---:|---:|---:|---:|
| Development/training set | 84 | 5 | 11.022 | 4.438 (40,26%) | 6.584 (59,74%) |
| Corrected external set | 10 | 1 | 1.658 | 768 (46,32%) | 890 (53,68%) |

Video manifest đầy đủ gồm 94 video, trong đó có 84 video raw và 10 video external. Table 1 trình bày theo split thay vì theo tên file. Development set dùng cho huấn luyện, so sánh classifier và đánh giá theo người tham gia. Corrected external set dùng cho kết quả external chính, nhưng còn hạn chế vì chỉ gồm P01. Metadata gồm `source_video`, `frame_index`, `timestamp_sec`, `sample_fps`, `video_fps`, `participant_id`, `view_angle`, và `camera_type`. Nhãn tư thế đúng và tư thế sai là nhãn project-specific, chưa được chuyên gia ergonomic xác nhận.

Table 2. Các nhóm đặc trưng dùng trong thực nghiệm.

| Nhóm đặc trưng | Số đặc trưng | Mô tả | Vai trò |
|---|---:|---|---|
| `raw_99` | 99 | 33 MediaPipe Pose landmarks với \(x\), \(y\), \(z\). | Biểu diễn landmark cơ bản. |
| `normalized_99` | 99 | Landmarks được đưa về trung điểm vai và scale theo kích thước cơ thể. | Giảm ảnh hưởng kích thước cơ thể và khoảng cách camera. |
| `ergonomic_14` | 14 | Chỉ báo vai, thân, đầu, cổ và tay-miệng. | Dấu hiệu tư thế có thể giải thích. |
| `combined_raw_ergonomic` | 113 | Landmark thô cộng chỉ báo ergonomic. | Kiểm tra landmark thô với cue tư thế rõ ràng. |
| `combined_normalized_ergonomic` | 113 | Landmark chuẩn hóa cộng chỉ báo ergonomic. | Kiểm tra landmark chuẩn hóa với cue tư thế rõ ràng. |

Table 2 tách biệt biểu diễn pose thô và các chỉ báo ergonomic có thể giải thích. Mô hình thực nghiệm được chọn dùng `normalized_99`, còn đặc trưng ergonomic vẫn hữu ích cho baseline rule-based và giải thích lỗi tư thế.

Các mô hình ứng viên gồm baseline rule-based, ANN/Keras, Logistic Regression, SVM RBF, Random Forest, MLP sklearn và HistGradientBoosting. Tiêu chí chọn model là F1 của lớp tư thế sai, với Recall của lớp tư thế sai và MCC làm tiêu chí phụ. Mô hình thực nghiệm được chọn là `hist_gradient_boosting__normalized_99`. Hiệu chỉnh ngưỡng chọn 0,65 trong protocol cuối. Vì artifact của project cho thấy việc calibration gắn với corrected external protocol, kết quả cuối nên được hiểu là calibrated corrected-external performance, không phải kết quả hold-out độc lập hoàn toàn.

Thực nghiệm chạy với Python 3.11.9. Các thư viện chính được ghi nhận gồm OpenCV 4.11.0, MediaPipe 0.10.21, NumPy 1.26.4, scikit-learn 1.6.1, TensorFlow 2.16.2, matplotlib, CustomTkinter, Pillow, joblib, pytest và statsmodels 0.14.6. Runtime benchmark dùng input 640 x 360, MediaPipe complexity 1 và tối đa 120 frame lấy mẫu mỗi video. Thông tin phần cứng chưa được ghi trong artifact của project.

Trong đánh giá, TP, TN, FP và FN lần lượt là true positives, true negatives, false positives và false negatives. Lớp dương là tư thế sai.

```latex
Accuracy = \frac{TP + TN}{TP + TN + FP + FN}
```

Accuracy đo tỷ lệ mẫu được phân loại đúng.

```latex
Precision = \frac{TP}{TP + FP}
```

Precision đo tỷ lệ mẫu dự đoán là tư thế sai mà thật sự là tư thế sai.

```latex
Recall = \frac{TP}{TP + FN}
```

Recall đo tỷ lệ mẫu tư thế sai thật sự được mô hình phát hiện.

```latex
F1 = \frac{2 \times Precision \times Recall}{Precision + Recall}
```

F1-score cân bằng Precision và Recall cho lớp tư thế sai. MCC cũng được báo cáo vì hữu ích khi cần xem xét cả hai lớp và hai loại lỗi.

Tốc độ xử lý được báo cáo bằng:

```latex
FPS = \frac{N}{T}
```

Trong đó \(N\) là số frame đã xử lý và \(T\) là thời gian xử lý tính bằng giây.

## 5. Đánh giá và thảo luận

Table 3 trình bày so sánh corrected external giữa baseline rule-based và mô hình ANN/Keras trong ứng dụng.

Table 3. So sánh corrected external giữa baseline rule-based và mô hình ANN/Keras.

| Phương pháp | Accuracy | Precision tư thế sai | Recall tư thế sai | F1 tư thế sai | MCC |
|---|---:|---:|---:|---:|---:|
| Baseline rule-based | 67,49% | 63,49% | 92,81% | 75,40% | 37,56% |
| ANN/Keras trong ứng dụng | 90,17% | 95,61% | 85,62% | 90,34% | 80,90% |

ANN tăng F1 của lớp tư thế sai từ 75,40% lên 90,34%. Baseline rule-based có Recall cao hơn, nhưng Precision thấp hơn nhiều, cho thấy có nhiều cảnh báo sai trên frame tư thế đúng. Trade-off này quan trọng với hệ thống cảnh báo vì bỏ sót tư thế sai và cảnh báo không cần thiết ảnh hưởng khác nhau đến người dùng.

Table 4 liệt kê 5 tổ hợp model-feature đứng đầu trong model registry trước khi hiệu chỉnh ngưỡng cuối.

Table 4. Các tổ hợp classifier và feature đứng đầu trong model registry.

| Rank | Model | Nhóm đặc trưng | Accuracy | Precision tư thế sai | Recall tư thế sai | F1 tư thế sai | MCC |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | HistGradientBoosting | `normalized_99` | 95,96% | 95,07% | 97,53% | 96,28% | 91,89% |
| 2 | Random Forest | `normalized_99` | 95,90% | 94,67% | 97,87% | 96,24% | 91,79% |
| 3 | SVM RBF | `ergonomic_14` | 95,36% | 96,89% | 94,38% | 95,62% | 90,72% |
| 4 | SVM RBF | `normalized_99` | 94,51% | 92,82% | 97,30% | 95,01% | 89,04% |
| 5 | Random Forest | `combined_normalized_ergonomic` | 94,27% | 91,89% | 97,98% | 94,83% | 88,65% |

Hai cấu hình đứng đầu dùng `normalized_99`, cho thấy chuẩn hóa theo cơ thể hữu ích trong protocol hiện tại. SVM RBF chỉ dùng `ergonomic_14` cũng đạt kết quả mạnh, cho thấy các chỉ báo hình học có thể giải thích chứa thông tin tư thế đáng kể. Các kết quả này chỉ có ý nghĩa trong dataset và protocol của project, không phải leaderboard so với nghiên cứu khác.

Table 5 trình bày kết quả corrected external đã hiệu chỉnh ngưỡng của mô hình thực nghiệm được chọn.

Table 5. Mô hình thực nghiệm được chọn trên corrected external set.

| Model | Nhóm đặc trưng | Ngưỡng | Accuracy | Precision tư thế sai | Recall tư thế sai | F1 tư thế sai | MCC | FP | FN |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| HistGradientBoosting | `normalized_99` | 0,65 | 96,50% | 96,22% | 97,30% | 96,76% | 92,97% | 34 | 24 |

Mô hình được chọn tạo ra 34 false positives và 24 false negatives. False positives có thể tạo cảnh báo không cần thiết, trong khi false negatives là các frame tư thế sai bị bỏ sót. Với hệ thống cảnh báo sức khỏe, Recall cho lớp tư thế sai là quan trọng, nhưng quá nhiều cảnh báo sai có thể làm giảm niềm tin của người dùng. Ngưỡng được chọn cân bằng các yếu tố này trong protocol calibrated hiện tại.

Fig. 3. Confusion matrix của mô hình thực nghiệm được chọn trên corrected external set.

Fig. 4. Hiệu chỉnh ngưỡng trên corrected external set.

Table 6 trình bày đánh giá leave-one-participant-out trên raw development dataset.

Table 6. Đánh giá leave-one-participant-out trên raw dataset.

| Người được giữ lại để test | Số mẫu | Accuracy | Precision tư thế sai | Recall tư thế sai | F1 tư thế sai | MCC |
|---|---:|---:|---:|---:|---:|---:|
| P01 | 3.524 | 90,81% | 98,28% | 84,88% | 91,09% | 82,64% |
| P02 | 1.225 | 79,35% | 77,87% | 91,55% | 84,16% | 56,55% |
| P03 | 2.208 | 93,03% | 99,85% | 90,05% | 94,70% | 85,55% |
| P04 | 1.815 | 86,67% | 79,37% | 100,00% | 88,50% | 75,92% |
| P05 | 2.250 | 93,56% | 95,63% | 94,24% | 94,93% | 86,11% |
| Mean | - | 88,68% | - | - | 90,67% | 77,35% |

Kết quả theo người tham gia mạnh hơn random internal frame split vì người được giữ lại không được dùng để train trong từng fold. Tuy nhiên, kết quả này vẫn dùng cùng quy trình thu thập dữ liệu của project. Kết quả thấp hơn ở P02 cho thấy dáng người, vị trí camera hoặc kiểu tư thế có thể ảnh hưởng đến hiệu năng.

Table 7 trình bày processing latency trên các video đại diện.

Table 7. Runtime benchmark trên các video đại diện.

| Góc nhìn | Frame xử lý | Tỷ lệ phát hiện pose | Mean total latency | p95 latency | FPS ước lượng |
|---|---:|---:|---:|---:|---:|
| front | 52 | 100,00% | 35,31 ms | 38,80 ms | 28,32 |
| side_30 | 120 | 100,00% | 35,67 ms | 43,08 ms | 28,03 |
| side_90 | 120 | 100,00% | 34,08 ms | 38,95 ms | 29,34 |

Mức 28,03-29,34 FPS hỗ trợ tính khả thi realtime của core processing pipeline. Benchmark này chỉ đo processing latency. Full GUI FPS có thể thấp hơn vì vẽ giao diện, lịch Tkinter, camera buffering, phát âm thanh và ghi SQLite tạo thêm overhead.

Fig. 5. Ví dụ temporal smoothing thể hiện xác suất frame thô, giá trị trung bình theo thời gian và ngưỡng quyết định trên corrected external predictions.

Fig. 6. Luồng ghi log SQLite được ứng dụng desktop dùng cho phân tích tư thế theo phiên.

So sánh với literature chỉ nên xem là so sánh theo ngữ cảnh. Các nghiên cứu dùng cảm biến, RGB-D, camera RGB và pose landmarks có thiết bị, nhãn, người tham gia và protocol chia dữ liệu khác nhau. Vì vậy, bài báo chỉ so sánh model trong cùng protocol của project, còn literature dùng để định vị hướng nghiên cứu, không dùng để claim vượt trội.

Các hạn chế chính cần nêu rõ. Development set chỉ gồm 5 người tham gia, và corrected external set chỉ gồm P01. Nhãn là project-specific, chưa được chuyên gia ergonomic hoặc RULA/REBA xác nhận. Kết quả mô hình được chọn là calibrated corrected-external performance, chưa phải hold-out độc lập hoàn toàn. Project chưa đánh giá public benchmark như MultiPosture. Full GUI FPS cũng chưa được đo.

## 6. Kết luận và hướng phát triển

Bài báo đã trình bày một hệ thống phát hiện lỗi tư thế làm việc qua webcam sử dụng MediaPipe Pose landmarks, các nhóm đặc trưng normalized và ergonomic, baseline dựa trên luật, các classifier học máy nhẹ và triển khai desktop Python. Nghiên cứu đi theo hướng Nghiên cứu ứng dụng: kết hợp pose estimation có sẵn với dataset project-specific, feature engineering, so sánh classifier, cảnh báo và ghi log cục bộ.

Dataset project gồm 84 video thô từ 5 người tham gia và 11.022 frame được lấy mẫu. Corrected external set gồm 10 video và 1.658 frame. Trên external set này, mô hình ANN/Keras trong ứng dụng tăng F1 lớp tư thế sai từ 75,40% của baseline rule-based lên 90,34%. Mô hình thực nghiệm được chọn, HistGradientBoosting với `normalized_99` và ngưỡng 0,65, đạt Accuracy 96,50%, F1 lớp tư thế sai 96,76% và MCC 92,97%. Runtime testing đạt 28,03-29,34 FPS trên các video đại diện.

Kết quả cho thấy MediaPipe Pose landmarks và classifier dạng bảng nhẹ có thể hỗ trợ một pipeline cảnh báo tư thế desktop chi phí thấp. Baseline dựa trên luật vẫn hữu ích vì giải thích được posture cues, trong khi classifier học máy cải thiện phân loại trong protocol dữ liệu hiện tại. SQLite logging và dashboard statistics bổ sung bằng chứng theo phiên cho phân tích sau.

Hướng phát triển tiếp theo là mở rộng dataset với nhiều người tham gia, vị trí camera, điều kiện ánh sáng và môi trường làm việc hơn. Nếu cần diễn giải ergonomic mạnh hơn, cần bổ sung annotation từ chuyên gia hoặc nhãn theo RULA/REBA. Public benchmark như MultiPosture nên được đánh giá sau khi kiểm tra license và mapping nhãn. Mô hình HistGradientBoosting được chọn cần tiếp tục được giữ nhất quán với hành vi của desktop app. Cuối cùng, nhãn nhị phân nên được mở rộng thành các loại tư thế cụ thể khi có đủ dữ liệu gán nhãn.

## Tài liệu tham khảo

1. Bazarevsky, V., Grishchenko, I., Raveendran, K., Zhu, T., Zhang, F., & Grundmann, M. (2020). *BlazePose: On-device real-time body pose tracking*. arXiv. https://doi.org/10.48550/arXiv.2006.10204
2. Bourahmoune, K., Ishac, K., & Amagasa, T. (2022). Intelligent posture training: Machine-learning-powered human sitting posture recognition based on a pressure-sensing IoT cushion. *Sensors, 22*(14), 5337. https://doi.org/10.3390/s22145337
3. Cao, Z., Hidalgo, G., Simon, T., Wei, S.-E., & Sheikh, Y. (2019). OpenPose: Realtime multi-person 2D pose estimation using part affinity fields. *IEEE Transactions on Pattern Analysis and Machine Intelligence, 43*(1), 172-186. https://doi.org/10.1109/TPAMI.2019.2929257
4. Carneros Prado, D., Cabanero Gomez, L., Fontecha, J., Hervas, R., Gonzalez Diaz, I., & Johnson, E. (2024). *MultiPosture: A dataset of body joints keypoints extracted using MediaPipe for multi-task sitting posture recognition with upper and lower body labels* (Version v1) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.14230872
5. Carneros-Prado, D., Cabanero-Gomez, L., Johnson, E., Gonzalez, I., Fontecha, J., & Hervas, R. (2024). A comparison between multilayer perceptrons and Kolmogorov-Arnold networks for multi-task classification in sitting posture recognition. *IEEE Access, 12*, 180198-180209. https://doi.org/10.1109/ACCESS.2024.3510034
6. Chaikhamwang, S., Montri, W., Janthajirakowit, C., & Fongmanee, S. (2025). An intelligent platform for behavior modification and office syndrome risk reduction using MediaPipe and computer vision. *International Journal of Advanced Computer Science and Applications, 16*(10). https://doi.org/10.14569/IJACSA.2025.0161038
7. Chen, K. (2019). Sitting posture recognition based on OpenPose. *IOP Conference Series: Materials Science and Engineering, 677*(3), 032057. https://doi.org/10.1088/1757-899X/677/3/032057
8. Estrada, J. E., Vea, L. A., & Devaraj, M. (2023). Modelling proper and improper sitting posture of computer users using machine vision for a human-computer intelligent interactive system during COVID-19. *Applied Sciences, 13*(9), 5402. https://doi.org/10.3390/app13095402
9. Feradov, F., Markova, V., & Ganchev, T. (2022). Automated detection of improper sitting postures in computer users based on motion capture sensors. *Computers, 11*(7), 116. https://doi.org/10.3390/computers11070116
10. Google AI Edge. (n.d.). *Pose landmark detection guide*. MediaPipe Solutions. https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker
11. Hignett, S., & McAtamney, L. (2000). Rapid entire body assessment (REBA). *Applied Ergonomics, 31*(2), 201-205. https://doi.org/10.1016/S0003-6870(99)00039-3
12. Jiang, X., Hu, Z., Wang, S., & Zhang, Y. (2023). A survey on artificial intelligence in posture recognition. *Computer Modeling in Engineering & Sciences, 137*(1), 35-82. https://doi.org/10.32604/cmes.2023.027676
13. Kim, J.-W., Choi, J.-Y., Ha, E. J., & Choi, J.-H. (2023). Human pose estimation using MediaPipe Pose and optimization method based on a humanoid model. *Applied Sciences, 13*(4), 2700. https://doi.org/10.3390/app13042700
14. Krauter, C., Angerbauer, K., Sousa Calepso, A., Achberger, A., Mayer, S., & Sedlmair, M. (2024). Sitting posture recognition and feedback: A literature review. In *Proceedings of the CHI Conference on Human Factors in Computing Systems*. Association for Computing Machinery. https://doi.org/10.1145/3613904.3642657
15. Kulikajevas, A., Maskeliunas, R., & Damasevicius, R. (2021). Detection of sitting posture using hierarchical image composition and deep learning. *PeerJ Computer Science, 7*, e442. https://doi.org/10.7717/peerj-cs.442
16. Lugaresi, C., Tang, J., Nash, H., McClanahan, C., Uboweja, E., Hays, M., Zhang, F., Chang, C.-L., Yong, M. G., Lee, J., Chang, W.-T., Hua, W., Georg, M., & Grundmann, M. (2019). *MediaPipe: A framework for building perception pipelines*. arXiv. https://arxiv.org/abs/1906.08172
17. Luna-Perejon, F., Montes-Sanchez, J. M., Duran-Lopez, L., Vazquez-Baeza, A., Beasley-Bohorquez, I., & Sevillano-Ramos, J. L. (2021). IoT device for sitting posture classification using artificial neural networks. *Electronics, 10*(15), 1825. https://doi.org/10.3390/electronics10151825
18. McAtamney, L., & Corlett, E. N. (1993). RULA: A survey method for the investigation of work-related upper limb disorders. *Applied Ergonomics, 24*(2), 91-99. https://doi.org/10.1016/0003-6870(93)90080-S
19. Nadeem, M., Elbasi, E., Zreikat, A. I., & Sharsheer, M. (2024). Sitting posture recognition systems: Comprehensive literature review and analysis. *Applied Sciences, 14*(18), 8557. https://doi.org/10.3390/app14188557
20. Odesola, D. F., Kulon, J., Verghese, S., Partlow, A., & Gibson, C. (2024). Smart sensing chairs for sitting posture detection, classification, and monitoring: A comprehensive review. *Sensors, 24*(9), 2940. https://doi.org/10.3390/s24092940
21. Roggio, F., Trovato, B., Sortino, M., & Musumeci, G. (2024). A comprehensive analysis of the machine learning pose estimation models used in human movement and posture analyses: A narrative review. *Heliyon, 10*(21), e39977. https://doi.org/10.1016/j.heliyon.2024.e39977
22. Tlili, F., Haddad, R., Bouallegue, R., & Shubair, R. (2022). Machine learning algorithms application for the proposed sitting posture monitoring system. *Procedia Computer Science, 203*, 239-246. https://doi.org/10.1016/j.procs.2022.07.031
23. Tsai, M.-C., Chu, E. T.-H., & Lee, C.-R. (2023). An automated sitting posture recognition system utilizing pressure sensors. *Sensors, 23*(13), 5894. https://doi.org/10.3390/s23135894
24. Wang, J., Hafidh, B., Dong, H., & El Saddik, A. (2022). *Sitting posture recognition using a spiking neural network*. arXiv. https://doi.org/10.48550/arXiv.2212.12908
25. Zeng, X., Sun, B., Wang, E., Luo, W., & Liu, T. (2017). A method of learner's sitting posture recognition based on depth image. In *Proceedings of the 2017 2nd International Conference on Control, Automation and Artificial Intelligence (CAAI 2017)* (pp. 558-563). Atlantis Press. https://doi.org/10.2991/caai-17.2017.125
