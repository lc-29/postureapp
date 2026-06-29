# 27. TASK - Chạy lại runtime benchmark cho HistGradientBoosting được lựa chọn

## 1. Bối cảnh

Trong Chương 4, mô hình được lựa chọn theo kết quả phân loại hiện tại là:

- Model ID: `hist_gradient_boosting__ergonomic_v2_with_view`
- Thuật toán: HistGradientBoosting.
- Feature set: `ergonomic_v2_with_view`.
- Số đặc trưng: 31.
- Threshold: 0,76.

Tuy nhiên, phần runtime benchmark cũ đang đo pipeline ANN:

- MediaPipe Pose.
- Feature vector cho ANN.
- Scaler.
- ANN/Keras classifier.

Nếu luận văn trình bày HistGradientBoosting là cấu hình được lựa chọn nhưng lại dùng Bảng runtime của ANN làm benchmark chính, hội đồng có thể hỏi vì sao model chính là HGB nhưng hiệu năng lại đo bằng ANN. Vì vậy cần chạy lại runtime benchmark cho đúng pipeline HGB được lựa chọn.

## 2. Mục tiêu

Chạy lại benchmark thời gian xử lý cho pipeline:

Input video -> resize 640x360 -> MediaPipe Pose -> tạo feature `ergonomic_v2_with_view` -> HistGradientBoosting -> threshold 0,76.

Kết quả dùng để thay thế hoặc bổ sung cho Bảng 4.9 và Hình 4.6 trong luận văn.

## 3. Ràng buộc

Không được:

- Không sửa giao diện app.
- Không sửa SQLite.
- Không cập nhật model registry.
- Không thay thế model đang dùng trong app.
- Không xóa runtime benchmark ANN cũ.
- Không tự tạo số liệu.
- Không claim đây là full GUI FPS nếu chỉ đo script xử lý.

Được phép:

- Tạo script runtime benchmark mới.
- Đọc model HGB từ registry/artifact hiện có.
- Đọc threshold 0,76 từ `threshold.json`.
- Tạo CSV, hình và report mới.
- Cập nhật ghi chú/caption phục vụ Chương 4.

## 4. Model và feature bắt buộc

Sử dụng đúng:

- Model registry path: `models/registry/hist_gradient_boosting__ergonomic_v2_with_view/model.pkl`
- Feature schema: `models/registry/hist_gradient_boosting__ergonomic_v2_with_view/feature_schema.json`
- Threshold: `models/registry/hist_gradient_boosting__ergonomic_v2_with_view/threshold.json`
- Feature set: `ergonomic_v2_with_view`

Nếu không tìm thấy artifact, dừng task và báo lỗi rõ trong report.

## 5. Video benchmark

Chọn ba video đại diện tương ứng các góc:

- `front`
- `side_30`
- `side_90`

Ưu tiên dùng cùng ba video đã dùng trong runtime benchmark ANN cũ nếu script cũ có lưu đường dẫn. Nếu không tìm được, tự chọn mỗi góc một video từ dataset raw/external, nhưng phải ghi rõ đường dẫn video trong report.

Mỗi video:

- Resize frame về 640 x 360.
- Giới hạn tối đa 120 frame đã xử lý để so sánh với benchmark cũ.
- Ghi số frame thực tế đã xử lý.
- Ghi tỷ lệ frame MediaPipe phát hiện được pose.

## 6. Script cần tạo

Tạo script mới:

`src/36_runtime_benchmark_hgb_selected.py`

Script cần thực hiện:

1. Load model HGB selected.
2. Load feature schema và threshold.
3. Mở từng video benchmark.
4. Resize frame về 640 x 360.
5. Đo thời gian:
   - `capture_resize_ms`: đọc frame + resize.
   - `mediapipe_ms`: chạy MediaPipe Pose.
   - `feature_ms`: tạo DataFrame landmark + `build_feature_matrix()`.
   - `model_ms`: `predict_proba()` hoặc score của HGB.
   - `total_ms`: tổng pipeline xử lý.
6. Tính `estimated_fps = 1000 / mean_total_ms`.
7. Ghi frame-level CSV.
8. Ghi summary CSV.
9. Tạo report Markdown.
10. Tạo Hình 4.6.

## 7. Output bắt buộc

Xuất các file:

- `reports/results/runtime_benchmark_hgb_selected.csv`
- `reports/results/runtime_benchmark_hgb_selected_summary.csv`
- `reports/RUNTIME_BENCHMARK_HGB_SELECTED.md`
- `reports/figures/figure_4_6_hgb_runtime_latency_fps.png`
- `reports/figures/figure_4_6_hgb_runtime_latency_fps.svg`

Không ghi đè:

- `reports/results/runtime_benchmark.csv`
- `reports/results/runtime_benchmark_summary.csv`
- `reports/RUNTIME_BENCHMARK.md`

## 8. Bảng 4.9 đề xuất

Tạo bảng summary có các cột:

- Góc quan sát.
- Video benchmark.
- Số frame xử lý.
- Tỷ lệ phát hiện pose.
- Độ trễ MediaPipe trung bình.
- Độ trễ tạo feature trung bình.
- Độ trễ HGB trung bình.
- Độ trễ toàn pipeline trung bình.
- p50 total latency.
- p95 total latency.
- FPS ước lượng.

Định dạng trong report:

- Latency: ms, 3 chữ số thập phân.
- FPS: 3 chữ số thập phân.
- Tỷ lệ pose detected: phần trăm, 2 chữ số thập phân.

## 9. Hình 4.6 đề xuất

Tạo Hình 4.6 gồm hai phần hoặc một biểu đồ kết hợp:

- Cột: `mean_total_latency_ms`.
- Đường hoặc nhãn phụ: `mean_estimated_fps`.
- Nhóm theo `view_angle`: front, side_30, side_90.

Caption đề xuất:

> Hình 4.6. So sánh độ trễ toàn pipeline và FPS ước lượng của pipeline HistGradientBoosting được lựa chọn theo góc quan sát.

Ghi chú dưới hình:

> Kết quả đo ở mức processing benchmark, gồm đọc/resize frame, MediaPipe Pose, tạo đặc trưng ergonomic_v2_with_view và suy luận HistGradientBoosting. Kết quả chưa bao gồm toàn bộ chi phí cập nhật giao diện CustomTkinter, phát âm thanh và ghi SQLite.

## 10. Nội dung cần ghi trong report

Report `RUNTIME_BENCHMARK_HGB_SELECTED.md` cần có:

1. Mục tiêu benchmark.
2. Model và feature set đang đo.
3. Đường dẫn artifact model/threshold/schema.
4. Video được dùng cho từng góc.
5. Bảng frame-level summary.
6. So sánh ngắn với runtime ANN cũ nếu có:
   - ANN runtime cũ chỉ là tham khảo.
   - HGB runtime mới mới là benchmark phù hợp với model được lựa chọn.
7. Hạn chế:
   - Chưa phải full GUI FPS.
   - Webcam/IP camera realtime có thể dùng `view_unknown`.
   - FPS phụ thuộc phần cứng, camera, ánh sáng, số người trong khung hình và tải hệ thống.
8. Đoạn văn có thể copy vào Chương 4.

## 11. Đoạn văn đề xuất cho Chương 4 sau khi có kết quả

Sau khi chạy xong, report cần tạo đoạn văn theo mẫu:

> Sau khi lựa chọn HistGradientBoosting với nhóm đặc trưng `ergonomic_v2_with_view`, đề tài tiến hành đo lại thời gian xử lý của pipeline sử dụng đúng cấu hình này. Kết quả trong Bảng 4.9 cho thấy độ trễ trung bình của pipeline dao động từ ... ms đến ... ms, tương ứng khoảng ... FPS đến ... FPS trên ba video đại diện. Phần lớn thời gian xử lý vẫn nằm ở bước MediaPipe Pose, trong khi bước tạo đặc trưng và suy luận HistGradientBoosting chiếm tỷ lệ nhỏ hơn. Kết quả này cho thấy pipeline HGB có khả năng xử lý gần thời gian thực ở mức processing benchmark, tuy nhiên chưa đại diện cho full GUI FPS của ứng dụng.

Không điền dấu `...` thủ công nếu chưa có số liệu; script phải tự sinh đoạn văn có số thật sau khi benchmark xong.

## 12. Kiểm tra cuối

Task hoàn thành khi:

- [ ] Đã tạo script `src/36_runtime_benchmark_hgb_selected.py`.
- [ ] Đã load đúng HGB selected model.
- [ ] Đã load đúng feature set `ergonomic_v2_with_view`.
- [ ] Đã load đúng threshold 0,76.
- [ ] Đã chạy benchmark trên front, side_30, side_90.
- [ ] Đã xuất frame-level CSV.
- [ ] Đã xuất summary CSV.
- [ ] Đã tạo Hình 4.6.
- [ ] Đã tạo report Markdown.
- [ ] Report ghi rõ đây là processing benchmark, không phải full GUI FPS.
- [ ] Không sửa app, SQLite hoặc model registry.

## 13. Lệnh chạy dự kiến

```powershell
cd D:\posture_detection_app
.\.venv\Scripts\activate
python src\36_runtime_benchmark_hgb_selected.py
```

