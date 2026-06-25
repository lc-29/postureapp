# Manual Additions TODO for Springer Final Draft

File này liệt kê những hình ảnh và số liệu cần bổ sung thủ công trước khi chuyển `SPRINGER_MANUSCRIPT_FINAL_DRAFT.md` / `SPRINGER_MANUSCRIPT_FINAL_DRAFT_VN.md` sang template Springer chính thức.

## A. Hình ảnh cần thêm hoặc xuất lại

| STT | Hình cần có | Vị trí trong bài | Trạng thái | File đề xuất | Cách bổ sung |
|---:|---|---|---|---|---|
| 1 | System architecture | Section 3, ngay sau pipeline đầu tiên | Chưa export ảnh độc lập | `reports/figures/system_architecture.png` | Export Mermaid diagram trong Section 3 sang PNG/SVG. |
| 2 | MediaPipe landmarks trên frame thật | Section 3.1 hoặc đầu Section 4 | Chưa có | `reports/figures/mediapipe_landmark_sample.png` | Chạy app/video, chụp 1 frame có skeleton overlay từ dữ liệu thật của project. |
| 3 | Feature construction pipeline | Section 3.2 | Chưa export ảnh độc lập | `reports/figures/feature_construction_pipeline.png` | Export Mermaid diagram trong Section 3.2 sang PNG/SVG. |
| 4 | Confusion matrix | Section 6.3 | Đã có | `reports/figures/external_confusion_matrix.png` | Kiểm tra độ phân giải trước khi nộp. |
| 5 | Threshold calibration curve | Section 6.3 | Đã có | `reports/figures/external_threshold_sweep.png` | Kiểm tra caption và độ phân giải. |
| 6 | Temporal smoothing effect | Section 6.6 | Đã có | `reports/figures/temporal_smoothing_effect.png` | Kiểm tra caption và độ phân giải. |
| 7 | Desktop GUI screenshot | Section 7 | Chưa có | `reports/figures/desktop_gui_screenshot.png` | Mở app, chụp màn hình có video/skeleton, prediction status và warning controls. |
| 8 | SQLite/logging/dashboard flow | Section 7 | Chưa có | `reports/figures/sqlite_logging_flow.png` | Vẽ flow: prediction -> warning event -> posture log -> session summary -> daily statistics -> dashboard. |
| 9 | Feature importance top 20 | Section 6.2 hoặc Supplementary | Đã có, chưa dùng trong bài chính | `reports/figures/feature_importance_top20.png` | Có thể thêm nếu cần giải thích vai trò feature; không bắt buộc. |
| 10 | TPRI distribution | Section 6.6 hoặc Supplementary | Đã có, chưa dùng trong bài chính | `reports/figures/tpri_distribution.png` | Chỉ thêm nếu có đoạn giải thích rõ TPRI là gì và liên quan thế nào. |

## B. Số liệu cần bổ sung thủ công

| STT | Số liệu cần bổ sung | Vị trí trong bài | Vì sao cần | Trạng thái hiện tại |
|---:|---|---|---|---|
| 1 | Cấu hình phần cứng chạy runtime: CPU, RAM, GPU nếu có, OS, loại camera | Section 5 Experimental Setup | Runtime FPS cần môi trường đo rõ ràng để tái lập | Chưa thấy trong project artifacts. |
| 2 | Camera setting: resolution, webcam model hoặc laptop camera, input FPS | Section 5 Experimental Setup hoặc Section 4 Dataset | Ảnh hưởng trực tiếp đến MediaPipe và FPS | Chưa thấy mô tả đầy đủ. |
| 3 | Full GUI FPS khi app chạy thật | Section 6.5 Runtime Evaluation hoặc Section 7 Implementation | Hiện chỉ có processing latency, chưa phải full GUI refresh | Chưa đo. |
| 4 | Protocol gán nhãn chi tiết: ai gán nhãn, gán theo video/segment/frame, có kiểm tra lại không | Section 4 Dataset and Feature Extraction | Reviewer sẽ hỏi nhãn Correct/Incorrect được tạo như thế nào | Hiện chỉ biết nhãn theo source posture class khi tạo sample. |
| 5 | Expert ergonomic annotation hoặc RULA/REBA score trên một subset | Section 4 hoặc Section 8 Limitations/Future Work | Tăng độ tin cậy ergonomic | Chưa có. |
| 6 | Inter-rater agreement nếu có nhiều người gán nhãn | Section 4 Dataset | Tăng độ tin cậy annotation | Chưa có. |
| 7 | Demographic tối thiểu: số người, giới tính/độ tuổi/chiều cao nếu được phép công bố | Section 4 Dataset | Tăng mô tả dataset và tính tái lập | Hiện chỉ có 5 participants P01-P05. |
| 8 | Public benchmark result, ví dụ MultiPosture | Section 6 Results hoặc Future Work | Giúp bài mạnh hơn nếu muốn nộp hội thảo quốc tế | Chưa chạy benchmark. |
| 9 | Video-wise error analysis sau khi sửa external video | Section 6.6 Error and Temporal Behavior | Giúp phân tích lỗi cụ thể hơn | Nếu đã có report, nên trích số liệu ngắn; nếu chưa, cần chạy lại. |
| 10 | Kết quả app nếu tích hợp HGB | Section 7 Implementation hoặc Section 6 | Hiện app dùng ANN, HGB là experimental best model | Chưa tích hợp HGB vào app. |

## C. Chỗ nên chèn hình trong manuscript

1. Section 3, sau Mermaid architecture:
   - Thay Mermaid bằng `reports/figures/system_architecture.png` khi nộp Springer.
2. Section 3.1, sau mô tả MediaPipe 33 landmarks:
   - Thêm hình frame thật có skeleton overlay.
3. Section 3.2, sau Mermaid feature pipeline:
   - Thay Mermaid bằng `reports/figures/feature_construction_pipeline.png`.
4. Section 6.3:
   - Giữ confusion matrix và threshold sweep.
5. Section 6.6:
   - Giữ temporal smoothing figure.
6. Section 7:
   - Thêm screenshot app và logging-flow diagram.

## D. Chỗ nên chèn số liệu thủ công trong manuscript

1. Section 5, đoạn đầu Experimental Setup:
   - Thêm phần cứng và OS.
   - Thêm camera resolution và input FPS.
2. Section 4, đoạn labeling protocol:
   - Thêm người gán nhãn, quy tắc gán nhãn, cách kiểm tra lại.
3. Section 6.5:
   - Thêm full GUI FPS nếu đã đo.
4. Section 6.6:
   - Thêm bảng video-wise error analysis nếu có đủ số liệu.
5. Section 6 hoặc Future Work:
   - Thêm public benchmark result nếu đã chạy MultiPosture hoặc dataset tương đương.

## E. Không nên thêm thủ công nếu chưa có bằng chứng

1. Không thêm claim expert ergonomic validation nếu chưa có chuyên gia hoặc rubric rõ ràng.
2. Không thêm claim SOTA.
3. Không ghi app đang dùng HistGradientBoosting nếu chưa tích hợp thật.
4. Không ghi benchmark public nếu chưa chạy thật.
5. Không thêm thông số phần cứng/camera theo phỏng đoán.
