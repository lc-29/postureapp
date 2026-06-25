# APPLIED_RESEARCH_FINAL_FIX_REPORT

Ngày tạo: 2026-06-04

Nguồn chỉnh chính:

- `reports/SPRINGER_MANUSCRIPT_APPLIED_RESEARCH_RESTRUCTURED.md`
- `reports/springer_overleaf/main_applied_research_final.tex`
- `reports/springer_overleaf/main_applied_research_final.pdf`

Không sửa code nguồn. Các ngưỡng rule-based được đọc từ `src/posture_baseline.py`.

## Bảng xử lý yêu cầu

| Issue | Fixed? | Location | What changed | Remaining risk |
| ----- | ------ | -------- | ------------ | -------------- |
| Title normalized landmarks | Yes | Title, PDF first page | Đổi title thành `Webcam-Based Working Posture Error Detection Using Normalized MediaPipe Landmarks and Lightweight Machine Learning`. | Không có. |
| Table 1 full video manifest | Yes | Section 4, Table 3 | Bảng dataset chỉ còn `Development/training set` và `Corrected external set`; dòng full manifest được chuyển thành câu mô tả riêng. | Không có. |
| Labeling protocol | Yes | Section 4 | Bổ sung đoạn mô tả nhãn video/segment-level, Correct/Incorrect project-specific, frame kế thừa nhãn, chưa có expert annotation/inter-rater agreement. | Nhãn vẫn là project-specific, cần chuyên gia ergonomic nếu nộp bài mạnh hơn. |
| Rule-based threshold table | Yes | Section 3, Table 2 | Thêm bảng ngưỡng thật: visibility 0.50, shoulder_y_diff 0.06, shoulder_tilt 10.0°, torso_lean 12.0°, head_offset 0.10, neck compression ratio 0.12, hand-mouth ratio 0.45, hand-mouth distance 0.13, hand visibility 0.35. | Bảng là baseline kỹ thuật, không phải chuẩn ergonomic lâm sàng. |
| Ergonomic feature definition table | Yes | Section 3, Table 1 | Thêm bảng 8 feature chính: shoulder_width, shoulder_tilt_angle, torso_lean_angle, head_offset_x, nose_shoulder_clearance_ratio, neck_compression_detected, min_hand_mouth_ratio, chin_rest_detected. | Chưa trình bày công thức chi tiết cho từng feature để giữ bài gọn. |
| Algorithm 1 | Yes | Section 3 | Thêm lại Algorithm 1 dạng 10 bước ngắn, không dùng code block dài. | Là mô tả thuật toán mức pipeline, không phải implementation listing. |
| Metric formula formatting | Yes | Section 4 | Sửa các công thức thành `\\mathrm{Accuracy}`, `\\mathrm{Precision}`, `\\mathrm{Recall}`, `\\mathrm{F1}`, `\\mathrm{FPS}`. | Không có. |
| Data/Code/Ethics note | Yes | Cuối Section 5 | Thêm note: raw videos không dự kiến public vì có thể định danh người tham gia; landmark features có thể chia sẻ sau ẩn danh nếu consent/venue cho phép; không claim formal ethics approval. | Cần bổ sung consent/ethics document nếu venue yêu cầu. |
| Google AI Edge reference | Yes | References | Đổi `Google AI Edge. (2026)` thành `Google AI Edge. (n.d.)` vì không chắc năm xuất bản. | Không có retrieved date vì project không có ngày truy cập. |
| GUI screenshot | No | Report only | Không tìm thấy screenshot GUI thật trong project, nên không thêm hình giả. | GUI screenshot should be added before submission. |

## Kiểm tra build

| Item | Result |
|---|---|
| Final TeX | `reports/springer_overleaf/main_applied_research_final.tex` |
| Final PDF | `reports/springer_overleaf/main_applied_research_final.pdf` |
| Build engine | Tectonic/LaTeX with `llncs.cls` |
| Authors in PDF | `Ly-Cu DUONG` and `Van-Phuc VO` |
| Affiliation | `Nam Can Tho University, Can Tho, Vietnam` |
| PDF pages before this prompt | 13 |
| PDF pages after fixes | 15 |
| References before | 25 |
| References after | 25 |

## Kiểm tra rủi ro cuối

| Check | Status |
|---|---|
| Có còn citation/DOI chưa chắc không? | Có một rủi ro nhẹ: một số nguồn gần đây như Chaikhamwang et al. (2025) nên đọc full paper trước khi nộp chính thức. Không thêm DOI mới chưa xác minh. |
| Có còn placeholder hình không? | Không có placeholder kiểu `[Insert Fig.]`. |
| Có còn hình giả không? | Không. GUI screenshot chưa thêm vì không tìm thấy ảnh thật. |
| Có còn claim quá mức không? | Không thấy claim vượt trội tổng quát hoặc claim mô hình mới. |
| Có còn `Not frame-level` trong manuscript/PDF không? | Không. |
| Có giữ threshold calibration note không? | Có. Bài vẫn ghi kết quả 0.65 là calibrated corrected-external performance, không phải strictly independent hold-out. |
| Có giữ limitations không? | Có. Vẫn nêu 5 participants, external set only P01, project-specific labels, no expert ergonomic annotation, no public benchmark, no full GUI FPS. |

## Ghi chú tiếp theo

Trước khi nộp hội thảo, nên bổ sung:

1. Screenshot GUI thật của app desktop.
2. Thông tin phần cứng chạy thực nghiệm: CPU, RAM, GPU nếu có, webcam.
3. Consent/ethics note chính thức nếu hội thảo yêu cầu.
4. Kiểm tra lại full text các references gần đây trước khi final submission.
