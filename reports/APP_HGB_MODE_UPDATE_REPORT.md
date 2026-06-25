# Báo Cáo Cập Nhật Chế Độ HistGradientBoosting Trong App

Cập nhật: 2026-06-25

## 1. Hiện Trạng Trước Khi Sửa

Trước task này, app chỉ có một chế độ `HistGradientBoosting (best)` nhưng thực tế đang hard-code model:

- Model ID: `hist_gradient_boosting__normalized_99`
- Feature set: `normalized_99`
- Threshold: `0.50`

Điều này gây nhầm lẫn vì sau task cải thiện model, model có kết quả tổng thể tốt nhất trên external P06/P07 là:

- Model ID: `hist_gradient_boosting__ergonomic_v2_with_view`
- Feature set: `ergonomic_v2_with_view`
- Threshold: `0.76`

## 2. Lý Do Không Chỉ Dùng Một HGB Mode

Hai model HGB có mục tiêu khác nhau:

| Model | Feature set | Threshold | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC | FP | FN |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| HGB high recall cũ | `normalized_99` | 0.50 | 67.38% | 63.62% | 97.69% | 77.06% | 0.3785 | 1427 | 59 |
| HGB balanced mới | `ergonomic_v2_with_view` | 0.76 | 89.31% | 93.48% | 87.01% | 90.13% | 0.7875 | 155 | 332 |

Model balanced mới tốt hơn về kết quả tổng thể, giảm false positive rất mạnh và phù hợp để báo cáo khoa học. Model high recall cũ có recall Incorrect cao hơn, phù hợp cho demo realtime khi muốn hạn chế bỏ sót tư thế sai.

## 3. Mode Mới Trong App

App hiện có các mode:

- `ANN`
- `HistGradientBoosting (balanced best)`
- `HistGradientBoosting (high recall demo)`
- `Rule-based Baseline`

Mode cũ `HistGradientBoosting (best)` được map về `HistGradientBoosting (balanced best)` nếu còn xuất hiện trong cấu hình cũ.

## 4. Cấu Hình Model Theo Mode

| App mode | Model ID | Feature set | Threshold | Mục tiêu |
|---|---|---|---:|---|
| `HistGradientBoosting (balanced best)` | `hist_gradient_boosting__ergonomic_v2_with_view` | `ergonomic_v2_with_view` | 0.76 | Kết quả khoa học cân bằng FP/FN |
| `HistGradientBoosting (high recall demo)` | `hist_gradient_boosting__normalized_99` | `normalized_99` | 0.50 | Demo realtime ưu tiên ít bỏ sót tư thế sai |

## 5. Thay Đổi Kỹ Thuật

Đã cập nhật `src/4_main_desktop_app.py`:

- Thêm cấu hình `HGB_MODE_CONFIGS`.
- Thêm hai mode HGB trong combobox.
- `is_hgb_mode()` nhận diện mọi mode nằm trong `HGB_MODE_CONFIGS`.
- `load_ai_components()` load model theo mode đang chọn.
- Lưu lại `self.hgb_model_id`, `self.hgb_feature_set`, `self.hgb_threshold`.
- HGB mode đọc threshold từ `models/registry/<model_id>/threshold.json`.
- `predict_frame_hgb()` không còn chỉ tạo `normalized_99` thủ công.
- `predict_frame_hgb()` tạo DataFrame landmark 1 dòng và gọi `build_feature_matrix(frame_df, self.hgb_feature_set)`.
- HGB mode dùng threshold model, không dùng nhầm `smoothingThreshold` làm ngưỡng quyết định.

## 6. Suy Ra `view_angle`

App thêm logic suy ra góc quay:

- Tên video chứa `side_90` => `side_90`
- Tên video chứa `side_30` => `side_30`
- Tên video chứa `front` => `front`
- Không nhận diện được hoặc webcam/IP camera => `unknown`

Lưu ý: với webcam realtime, balanced model sẽ dùng `view_unknown` nếu chưa có UI chọn góc quay. Nếu cần dùng balanced model cho webcam ổn định hơn, nên thêm combobox chọn góc quay ở task sau.

## 7. Kiểm Tra Service

Đã kiểm tra cả hai model bằng một dòng external CSV:

| Model ID | Feature set | Threshold | Số feature | Kết quả |
|---|---|---:|---:|---|
| `hist_gradient_boosting__normalized_99` | `normalized_99` | 0.50 | 99 | Predict được |
| `hist_gradient_boosting__ergonomic_v2_with_view` | `ergonomic_v2_with_view` | 0.76 | 31 | Predict được |

Đã chạy:

```powershell
.venv\Scripts\python.exe -m pytest tests\test_feature_schema.py tests\test_model_registry_service.py
```

Kết quả:

```text
4 passed
```

## 8. Khuyến Nghị Demo

- Demo realtime trước hội đồng: chọn `HistGradientBoosting (high recall demo)`.
- Báo cáo khoa học/luận văn: trình bày `HistGradientBoosting (balanced best)` là model có kết quả tổng thể tốt hơn trên external P06/P07.
- ANN nên trình bày là baseline neural network hoặc mô hình tích hợp ban đầu, không nên dùng làm model demo chính khi kết quả external còn thấp.

## 9. Giới Hạn Còn Lại

- Chưa thêm UI chọn góc quay cho webcam realtime.
- `HistGradientBoosting (balanced best)` dùng `view_unknown` khi chạy webcam/IP camera.
- Chưa test thủ công bằng cửa sổ GUI trong report này; cần mở app và thử webcam/video trước buổi demo.
- Dòng hướng dẫn phụ trong sidebar chưa được thiết kế lại toàn bộ; task này tập trung sửa logic model.

## 10. Checklist

- [x] App có mode `HistGradientBoosting (balanced best)`.
- [x] App có mode `HistGradientBoosting (high recall demo)`.
- [x] App vẫn giữ mode `ANN`.
- [x] App vẫn giữ mode `Rule-based Baseline`.
- [x] Balanced mode load model `hist_gradient_boosting__ergonomic_v2_with_view`.
- [x] Balanced mode dùng feature set `ergonomic_v2_with_view`.
- [x] Balanced mode dùng threshold `0.76`.
- [x] High recall mode load model `hist_gradient_boosting__normalized_99`.
- [x] High recall mode dùng feature set `normalized_99`.
- [x] High recall mode dùng threshold `0.50`.
- [x] Video file suy ra được `view_angle` từ tên file.
- [x] Webcam/IP camera có fallback `view_unknown`.
- [x] `predict_frame_hgb()` dùng `build_feature_matrix()`.
- [x] HGB mode không dùng nhầm `smoothingThreshold` làm threshold model.
- [x] Test feature/model registry pass.
- [x] Đã tạo report `APP_HGB_MODE_UPDATE_REPORT.md`.

