# REFERENCES_25_SELECTION_AUDIT

Ngày tạo: 2026-06-03

Mục tiêu: chọn lọc khoảng 25 tài liệu phù hợp nhất cho bài báo theo hướng **Applied Research / Existing model + new dataset/features** của hệ thống phát hiện lỗi tư thế làm việc qua webcam.

Nguyên tắc kiểm tra:

- Không bịa DOI.
- Không dùng blog/tutorial làm nguồn học thuật chính.
- Official documentation chỉ dùng cho phần Methodology/Implementation.
- Literature metrics chỉ dùng để định vị ngữ cảnh, không dùng làm leaderboard vì khác dataset, cảm biến, nhãn và protocol.
- Các nguồn chưa đủ chắc chắn được đưa vào nhóm loại/cần kiểm tra, không đưa vào references chính.

## Bảng chọn lọc references

| STT | Tên tài liệu | Tác giả/năm | Link/DOI/URL | Loại nguồn | Phần dùng trong bài | Giữ/Loại | Lý do |
|---:|---|---|---|---|---|---|---|
| 1 | BlazePose: On-device real-time body pose tracking | Bazarevsky et al., 2020 | https://doi.org/10.48550/arXiv.2006.10204 | arXiv/preprint | Related Work, Proposed System | Giữ | Nguồn nền tảng cho BlazePose/MediaPipe Pose, phù hợp với webcam và realtime pose tracking. |
| 2 | MediaPipe: A framework for building perception pipelines | Lugaresi et al., 2019 | https://arxiv.org/abs/1906.08172 | arXiv/preprint | Related Work, Methodology | Giữ | Nguồn nền tảng mô tả MediaPipe framework. |
| 3 | OpenPose: Realtime multi-person 2D pose estimation using part affinity fields | Cao et al., 2019 | https://doi.org/10.1109/TPAMI.2019.2929257 | Journal paper | Related Work | Giữ | Nguồn kinh điển về pose estimation, giúp so sánh OpenPose/MediaPipe trong Related Work. |
| 4 | Pose landmark detection guide | Google AI Edge, 2026 | https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker | Official documentation | Methodology/Implementation | Giữ có giới hạn | Chỉ dùng để mô tả implementation MediaPipe Pose, không dùng thay paper học thuật. |
| 5 | Human pose estimation using MediaPipe Pose and optimization method based on a humanoid model | Kim et al., 2023 | https://doi.org/10.3390/app13042700 | Journal paper | Related Work | Giữ | Liên quan trực tiếp đến MediaPipe Pose và human pose estimation. |
| 6 | Sitting posture recognition based on OpenPose | Chen, 2019 | https://doi.org/10.1088/1757-899X/677/3/032057 | Conference/proceedings paper | Related Work | Giữ | Gần với bài toán nhận diện tư thế ngồi từ pose landmarks. |
| 7 | Modelling proper and improper sitting posture of computer users using machine vision | Estrada et al., 2023 | https://doi.org/10.3390/app13095402 | Journal paper | Related Work, Discussion | Giữ | Rất gần đề tài vì nhận diện tư thế đúng/sai của người dùng máy tính bằng machine vision. |
| 8 | Detection of sitting posture using hierarchical image composition and deep learning | Kulikajevas et al., 2021 | https://doi.org/10.7717/peerj-cs.442 | Journal paper | Related Work, Discussion | Giữ | Nguồn RGB-D/deep learning quan trọng để so sánh phần cứng và protocol. |
| 9 | MultiPosture dataset | Carneros Prado et al., 2024 | https://doi.org/10.5281/zenodo.14230872 | Dataset | Dataset, Future Work | Giữ | Dataset MediaPipe keypoints cho sitting posture, phù hợp để benchmark tương lai. |
| 10 | MLP vs Kolmogorov-Arnold Networks for sitting posture recognition | Carneros-Prado et al., 2024 | https://doi.org/10.1109/ACCESS.2024.3510034 | Journal paper | Related Work, Dataset/Benchmark | Giữ | Paper đi kèm hướng sitting posture recognition và MultiPosture. |
| 11 | Sitting posture recognition systems: Comprehensive literature review and analysis | Nadeem et al., 2024 | https://doi.org/10.3390/app14188557 | Review paper | Introduction, Related Work | Giữ | Review mạnh cho bối cảnh sitting posture recognition. |
| 12 | Sitting posture recognition and feedback: A literature review | Krauter et al., 2024 | https://doi.org/10.1145/3613904.3642657 | Conference paper / review | Related Work, Discussion | Giữ | Review CHI về posture recognition và feedback, phù hợp với hệ thống cảnh báo. |
| 13 | Machine learning pose estimation models in human movement and posture analyses | Roggio et al., 2024 | https://doi.org/10.1016/j.heliyon.2024.e39977 | Review paper | Related Work | Giữ | Review về pose estimation trong phân tích chuyển động/tư thế người. |
| 14 | A survey on artificial intelligence in posture recognition | Jiang et al., 2023 | https://doi.org/10.32604/cmes.2023.027676 | Review paper | Introduction, Related Work | Giữ | Tổng quan AI trong posture recognition, hỗ trợ bối cảnh. |
| 15 | RULA: A survey method for work-related upper limb disorders | McAtamney & Corlett, 1993 | https://doi.org/10.1016/0003-6870(93)90080-S | Journal paper | Discussion, Future Work | Giữ | Nguồn ergonomic nền tảng; dùng để nói hướng expert/RULA annotation tương lai. |
| 16 | Rapid Entire Body Assessment (REBA) | Hignett & McAtamney, 2000 | https://doi.org/10.1016/S0003-6870(99)00039-3 | Journal paper | Discussion, Future Work | Giữ | Nguồn ergonomic nền tảng; dùng cho hướng REBA annotation tương lai. |
| 17 | An automated sitting posture recognition system utilizing pressure sensors | Tsai et al., 2023 | https://doi.org/10.3390/s23135894 | Journal paper | Related Work | Giữ | Sensor baseline mạnh, giúp nêu hạn chế cần phần cứng riêng. |
| 18 | Intelligent posture training using pressure-sensing IoT cushion | Bourahmoune et al., 2022 | https://doi.org/10.3390/s22145337 | Journal paper | Related Work | Giữ | Sensor/IoT cushion, phù hợp nhóm sensor-based posture recognition. |
| 19 | IoT device for sitting posture classification using artificial neural networks | Luna-Perejon et al., 2021 | https://doi.org/10.3390/electronics10151825 | Journal paper | Related Work | Giữ | ANN + sensor-based sitting posture classification, phù hợp để so sánh với ANN app model. |
| 20 | Automated detection of improper sitting postures in computer users based on motion capture sensors | Feradov et al., 2022 | https://doi.org/10.3390/computers11070116 | Journal paper | Related Work | Giữ | Gần chủ đề computer users và improper posture, nhưng dùng motion capture sensors. |
| 21 | Smart sensing chairs for sitting posture detection, classification, and monitoring | Odesola et al., 2024 | https://doi.org/10.3390/s24092940 | Review paper | Introduction, Related Work | Giữ | Review về smart chair/sensor posture monitoring, giúp nêu hạn chế phần cứng. |
| 22 | Machine learning algorithms application for sitting posture monitoring system | Tlili et al., 2022 | https://doi.org/10.1016/j.procs.2022.07.031 | Conference/proceedings paper | Related Work, Experiment context | Giữ | Phù hợp nhóm ML cho sitting posture monitoring. |
| 23 | Sitting posture recognition using a spiking neural network | Wang et al., 2022 | https://doi.org/10.48550/arXiv.2212.12908 | arXiv/preprint | Related Work | Giữ | Sensor/pressure + SNN, dùng làm nền so sánh ngữ cảnh, không phải nguồn chính mạnh nhất. |
| 24 | A method of learner's sitting posture recognition based on depth image | Zeng et al., 2017 | https://doi.org/10.2991/caai-17.2017.125 | Conference paper | Related Work | Giữ | Đại diện cho hướng depth image, khác với webcam-only. |
| 25 | An intelligent platform for behavior modification and office syndrome risk reduction using MediaPipe and computer vision | Chaikhamwang et al., 2025 | https://doi.org/10.14569/IJACSA.2025.0161038 | Journal/conference-style journal paper | Related Work, Discussion | Giữ | Gần hướng MediaPipe + office syndrome + cảnh báo ứng dụng; cần xem lại full paper trước nộp chính thức. |
| 26 | On-device, real-time body pose tracking with MediaPipe BlazePose | Bazarevsky & Grishchenko, 2020 | Google Research Blog URL | Blog/technical article | References phụ nếu cần | Loại khỏi references chính | Không phải nguồn học thuật chính; paper arXiv BlazePose đã đủ. |
| 27 | LearnOpenCV body posture detection tutorial | Kukil, 2022 | https://learnopencv.com/building-a-body-posture-analysis-system-using-mediapipe/ | Blog/tutorial | Tham khảo kỹ thuật | Loại khỏi references chính | Không phải nguồn học thuật chính, chỉ dùng tham khảo kỹ thuật nếu cần. |
| 28 | Roboflow Sitting Posture Detection dataset | Roboflow | Roboflow Universe URLs | Dataset/web dataset | Dataset tham khảo | Loại khỏi references chính | Chưa đủ mạnh cho references chính; cần kiểm tra license, nhãn, chất lượng và nguồn gốc. |
| 29 | Hugging Face KandenAiHackathonPosture2 | SeiyaCM | Hugging Face dataset URL | Dataset/web dataset | Dataset tham khảo | Loại khỏi references chính | Chưa kiểm chứng học thuật; chỉ dùng nếu có kế hoạch benchmark rõ. |
| 30 | LSP-YOLO sitting posture recognition | Li et al., 2025 | arXiv DOI trong project | arXiv/preprint | So sánh ngoài phạm vi | Loại khỏi references chính | Dùng YOLO, lệch hướng yêu cầu không chuyển sang YOLO/CNN. |
| 31 | SitLLM pressure sensor posture health understanding | Gao et al., 2025 | arXiv DOI trong project | arXiv/preprint | Tham khảo xu hướng | Loại khỏi references chính | LLM + pressure sensor, xa trọng tâm bài Applied Research hiện tại. |

## A. Nguồn bắt buộc nên giữ

1. Estrada et al. (2023) - machine vision cho tư thế đúng/sai của người dùng máy tính.
2. Chen (2019) - sitting posture recognition dựa trên OpenPose.
3. Bazarevsky et al. (2020) - BlazePose.
4. Lugaresi et al. (2019) - MediaPipe framework.
5. Carneros Prado et al. (2024) - MultiPosture dataset.
6. Nadeem et al. (2024) - review sitting posture recognition.
7. Krauter et al. (2024) - review sitting posture recognition and feedback.
8. Tsai et al. (2023) - pressure-sensor baseline.

## B. Nguồn nên giữ cho MediaPipe/OpenPose/Human Pose Estimation

1. Cao et al. (2019) - OpenPose.
2. Lugaresi et al. (2019) - MediaPipe.
3. Bazarevsky et al. (2020) - BlazePose.
4. Kim et al. (2023) - MediaPipe Pose trong human pose estimation.
5. Google AI Edge (2026) - documentation triển khai pose landmarker.

## C. Nguồn nên giữ cho posture recognition/ergonomics

1. Estrada et al. (2023).
2. Chen (2019).
3. Kulikajevas et al. (2021).
4. Nadeem et al. (2024).
5. Krauter et al. (2024).
6. Roggio et al. (2024).
7. McAtamney & Corlett (1993) - RULA.
8. Hignett & McAtamney (2000) - REBA.

## D. Nguồn dataset/benchmark

1. MultiPosture dataset - giữ, phù hợp nhất để benchmark tương lai.
2. MultiPosture IEEE Access comparison paper - giữ.
3. Roboflow Sitting Posture datasets - chưa đưa vào references chính, chỉ cân nhắc nếu kiểm tra license và protocol.
4. Hugging Face posture dataset - chưa đưa vào references chính, chỉ cân nhắc nếu kiểm tra license và nhãn.

## E. Nguồn nên loại hoặc chỉ tham khảo kỹ thuật

1. Google Research Blog về BlazePose - loại khỏi references chính vì đã có arXiv.
2. LearnOpenCV tutorial - không phải nguồn học thuật chính.
3. Roboflow datasets - chưa đủ kiểm chứng học thuật cho references chính.
4. Hugging Face dataset - chưa đủ kiểm chứng học thuật cho references chính.
5. LSP-YOLO - lệch hướng vì bài không chuyển sang YOLO.
6. SitLLM - xa trọng tâm vì dùng pressure sensor và LLM.

## Kết luận chọn lọc

Danh sách references chính hiện chọn **25 nguồn**. Trong đó có:

- 4 nguồn human pose estimation/MediaPipe/OpenPose.
- 8 nguồn posture recognition bằng RGB, RGB-D, pose landmarks hoặc MediaPipe.
- 6 nguồn sensor/pressure/depth-camera baseline.
- 4 nguồn review/tổng quan.
- 2 nguồn ergonomic nền tảng RULA/REBA.
- 1 nguồn official documentation chỉ dùng cho phần triển khai.

Danh sách này đủ mạnh hơn bản cũ vì đã bổ sung RULA, REBA, Luna-Perejon et al., Chaikhamwang et al., Tlili et al. và chuẩn hóa vai trò của nguồn official/blog/dataset.
