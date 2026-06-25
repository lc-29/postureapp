# 16 TASK - Hoàn thiện báo cáo luận văn Word theo file mẫu

Ngày tạo: 2026-05-28

## Mục tiêu

Dùng file mẫu:

```text
D:\LUẬN VĂN 2026\LVTN_TranThaoVan_B2203485maucoTrinhCTU.pdf
```

để tham chiếu cấu trúc báo cáo luận văn và biên soạn bản Word cho đề tài:

```text
Xây dựng ứng dụng phát hiện lỗi tư thế làm việc qua webcam sử dụng Computer Vision
```

## Cấu trúc rút ra từ file mẫu

File mẫu có cấu trúc chính:

1. Trang bìa.
2. Trang bìa phụ có người hướng dẫn.
3. Lời cảm ơn.
4. Tóm tắt.
5. Mục lục.
6. Danh mục hình.
7. Danh mục bảng.
8. Danh mục từ chuyên ngành.
9. Chương 1 - Giới thiệu.
10. Chương 2 - Tổng quan tài liệu.
11. Chương 3 - Nội dung và phương pháp nghiên cứu.
12. Chương 4 - Kết quả và thảo luận.
13. Chương 5 - Kết luận và hướng phát triển.
14. Tài liệu tham khảo.

## Quy trình thực hiện

| Task | Trạng thái | Kết quả |
|---|---|---|
| TASK-1601 | Done | Đã đọc PDF mẫu và trích cấu trúc chương/mục. |
| TASK-1602 | Done | Đã ánh xạ cấu trúc mẫu sang đề tài phát hiện tư thế. |
| TASK-1603 | Done | Đã đưa số liệu dự án vào báo cáo: dataset, benchmark, ablation, participant-wise, temporal smoothing, model final. |
| TASK-1604 | Done | Đã tạo file Word nháp trong `reports/`. |
| TASK-1605 | Done | Đã copy một bản sang thư mục `D:\LUẬN VĂN 2026\`. |

## File đầu ra

```text
D:\posture_detection_app\reports\LUAN_VAN_PHAT_HIEN_TU_THE_WEBCAM_DRAFT.docx
D:\LUẬN VĂN 2026\LUAN_VAN_PHAT_HIEN_TU_THE_WEBCAM_DRAFT.docx
```

## Nội dung đã đưa vào bản Word

- Trang bìa theo phong cách file mẫu.
- Trang bìa phụ có phần cán bộ hướng dẫn.
- Lời cảm ơn.
- Tóm tắt tiếng Việt.
- Mục lục tự động dạng field của Microsoft Word.
- Danh mục từ viết tắt và thuật ngữ.
- Chương 1: Giới thiệu, mục tiêu, phạm vi, phương pháp, cấu trúc luận văn.
- Chương 2: Tổng quan Computer Vision, MediaPipe Pose, đặc trưng tư thế, mô hình ML, metrics.
- Chương 3: Dataset, metadata, pipeline, feature schema, model registry, threshold calibration, cảnh báo thời gian thực.
- Chương 4: Kết quả corrected external, mô hình cuối, participant-wise, ablation, temporal smoothing, ứng dụng desktop.
- Chương 5: Kết luận, đóng góp, hạn chế, hướng phát triển.
- Tài liệu tham khảo gợi ý.

## Việc cần bổ sung thủ công trước khi nộp

1. Điền họ tên sinh viên, mã số sinh viên, khóa, ngành học, tên giảng viên hướng dẫn.
2. Mở file bằng Microsoft Word và chọn `References > Update Table` để cập nhật mục lục/số trang.
3. Bổ sung ảnh chụp màn hình app desktop: màn hình chính, light mode, dark mode, tab thống kê, cảnh báo thực tế.
4. Xuất sơ đồ Mermaid `reports/figures/system_pipeline_mermaid.md` sang PNG nếu muốn chèn hình pipeline đẹp hơn.
5. Bổ sung thêm tài liệu tham khảo khoa học theo chuẩn trích dẫn mà khoa/hội đồng yêu cầu.
6. Kiểm tra lại quy định font, căn lề, đánh số trang, biểu mẫu nhận xét và chữ ký theo mẫu chính thức của trường.

## Hướng nâng cấp tiếp theo

1. Viết bản luận văn đầy đủ hơn theo từng chương, tăng độ dài phần tổng quan tài liệu và cơ sở lý thuyết.
2. Bổ sung bảng so sánh với các nghiên cứu liên quan.
3. Bổ sung ảnh minh họa pipeline, confusion matrix, feature importance và giao diện app.
4. Chuẩn hóa tài liệu tham khảo bằng BibTeX/Zotero/Mendeley.
5. Tạo bản PDF cuối từ Word sau khi đã cập nhật mục lục và hình ảnh.
