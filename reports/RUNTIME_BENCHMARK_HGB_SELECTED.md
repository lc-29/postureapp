# Runtime Benchmark HGB Selected

## 1. Mục tiêu

Benchmark này đo lại thời gian xử lý của pipeline sử dụng đúng cấu hình HistGradientBoosting được lựa chọn trong thực nghiệm. Kết quả dùng để thay thế runtime benchmark ANN cũ trong phần đánh giá hiệu năng của Chương 4.

## 2. Cấu hình đo

- Model ID: `hist_gradient_boosting__ergonomic_v2_with_view`.
- Thuật toán: HistGradientBoosting.
- Feature set: `ergonomic_v2_with_view`.
- Số đặc trưng: 31.
- Threshold: 0.76.
- Model artifact: `models\registry\hist_gradient_boosting__ergonomic_v2_with_view\model.pkl`.
- Feature schema: `models\registry\hist_gradient_boosting__ergonomic_v2_with_view\feature_schema.json`.
- Threshold artifact: `models\registry\hist_gradient_boosting__ergonomic_v2_with_view\threshold.json`.
- Resolution: 640x360.
- Max processed frames per video: 120.
- Warm-up frames excluded from summary: 5 per video.
- Frame stride: 15.
- MediaPipe model complexity: 1.

## 3. Bảng 4.9 đề xuất

| view_angle | video_path | processed_frames | warmup_excluded_frames | pose_detection_rate | mean_mediapipe_latency_ms | mean_feature_latency_ms | mean_hgb_latency_ms | mean_total_latency_ms | p50_total_latency_ms | p95_total_latency_ms | mean_estimated_fps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| front | dataset\external_videos\correct\P06_correct_front_001.mp4 | 115 | 5 | 100,00% | 22.909 | 3.870 | 2.893 | 39.010 | 37.790 | 45.677 | 25.635 |
| side_30 | dataset\external_videos\correct\P06_correct_side_30_001.mp4 | 115 | 5 | 100,00% | 22.385 | 3.931 | 2.951 | 38.764 | 37.992 | 45.695 | 25.797 |
| side_90 | dataset\external_videos\correct\P06_correct_side_90_001.mp4 | 115 | 5 | 100,00% | 23.004 | 4.078 | 2.987 | 39.567 | 38.252 | 47.288 | 25.274 |

## 4. Hình 4.6

- `reports/figures/figure_4_6_hgb_runtime_latency_fps.png`
- `reports/figures/figure_4_6_hgb_runtime_latency_fps.svg`

**Caption đề xuất:** Hình 4.6. So sánh độ trễ toàn pipeline và FPS ước lượng của pipeline HistGradientBoosting được lựa chọn theo góc quan sát.

## 5. Diễn giải kết quả

Sau khi lựa chọn HistGradientBoosting với nhóm đặc trưng `ergonomic_v2_with_view`, đề tài tiến hành đo lại thời gian xử lý của pipeline sử dụng đúng cấu hình này. Kết quả cho thấy độ trễ trung bình của pipeline dao động từ 38.764 ms đến 39.567 ms, tương ứng khoảng 25.274 FPS đến 25.797 FPS trên ba video đại diện. Thời gian MediaPipe Pose trung bình khoảng 22.766 ms/frame, trong khi bước tạo đặc trưng trung bình khoảng 3.960 ms/frame và suy luận HistGradientBoosting khoảng 2.944 ms/frame. Kết quả này cho thấy pipeline HGB có khả năng xử lý gần thời gian thực ở mức processing benchmark, tuy nhiên chưa đại diện cho full GUI FPS của ứng dụng.

## 6. So sánh với benchmark ANN cũ

Benchmark ANN cũ chỉ nên dùng như kết quả tham khảo lịch sử của pipeline MediaPipe + ANN. Vì mô hình được lựa chọn hiện tại là HistGradientBoosting, benchmark HGB trong báo cáo này mới là kết quả phù hợp hơn để đưa vào Bảng 4.9 và Hình 4.6 của luận văn.

## 7. Hạn chế

- Đây là processing benchmark, chưa phải full GUI FPS.
- Chưa bao gồm chi phí cập nhật giao diện CustomTkinter, vẽ skeleton lên GUI, phát âm thanh, ghi SQLite và xử lý sự kiện người dùng.
- Webcam/IP camera realtime có thể dùng `view_unknown` nếu không có metadata góc nhìn.
- FPS phụ thuộc phần cứng, camera, ánh sáng, số người trong khung hình và tải hệ thống.

## 8. File đã xuất

- `reports/results/runtime_benchmark_hgb_selected.csv`
- `reports/results/runtime_benchmark_hgb_selected_summary.csv`
- `reports/figures/figure_4_6_hgb_runtime_latency_fps.png`
- `reports/figures/figure_4_6_hgb_runtime_latency_fps.svg`

## 9. Checklist

- [x] Đã load đúng HGB selected model.
- [x] Đã load đúng feature set `ergonomic_v2_with_view`.
- [x] Đã load đúng threshold 0,76.
- [x] Đã benchmark front, side_30 và side_90.
- [x] Đã loại 5 frame warm-up đầu mỗi video khỏi bảng tổng hợp.
- [x] Không sửa app, SQLite hoặc model registry.
