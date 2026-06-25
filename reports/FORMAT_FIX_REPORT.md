# FORMAT_FIX_REPORT

Ngày tạo: 2026-06-04

Mục tiêu: chỉnh phần trình bày trong bài báo LaTeX/PDF để tránh lỗi format do pipeline và ANN architecture được viết bằng mũi tên `->` trong code block/monospace.

## File đầu ra

| File | Vai trò |
|---|---|
| `reports/springer_overleaf/main_applied_research_final_formatfix.tex` | Source LaTeX đã sửa format. |
| `reports/springer_overleaf/main_applied_research_final_formatfix.pdf` | PDF mới đã build. |
| `reports/SPRINGER_MANUSCRIPT_APPLIED_RESEARCH_RESTRUCTURED.md` | Manuscript Markdown nguồn đã cập nhật cùng nội dung. |

## Các đoạn đã sửa

| Vị trí | Trước khi sửa | Sau khi sửa |
|---|---|---|
| Section 3, đầu Proposed System | Pipeline dạng code block với các dòng `Webcam/IP camera/MP4 video -> OpenCV -> MediaPipe -> ...` | Thay bằng một đoạn văn học thuật mô tả tuần tự các module: OpenCV Frame Capture, Landmark Extraction, Feature Construction, Posture Classification, Temporal Smoothing, Warning and Logging, SQLite logs/statistics. |
| Section 3, Fig. 1 | Pipeline text lặp lại trước hình | Giữ Fig. 1 và thêm câu `Fig. 1 summarizes this processing flow.` trong đoạn văn. |
| Section 3, Classification | ANN architecture dạng code block `Input -> Dense(128) -> BatchNorm -> Dropout ...` | Thay bằng đoạn văn mô tả feed-forward neural network, 3 hidden layers 128/64/32 neurons, BatchNorm/Dropout, output sigmoid neuron. |
| LaTeX source | Có thể sinh `verbatim` do code block | Không còn `verbatim` block và đã bỏ `\\usepackage{verbatim}` khỏi source sinh ra. |

## Kiểm tra theo yêu cầu

| Check | Kết quả |
|---|---|
| Đã thay pipeline bằng đoạn văn hay bảng? | Đã thay bằng đoạn văn học thuật. |
| Đã thay ANN architecture bằng đoạn văn hay bảng? | Đã thay bằng đoạn văn học thuật, không thêm bảng để tránh lặp ý. |
| Có còn `->` trong Markdown/LaTeX final không? | Không. Đã kiểm tra bằng `rg`. |
| Có còn `Input ->` trong Markdown/LaTeX final không? | Không. |
| Có còn code block/verbatim không cần thiết không? | Không. Các công thức LaTeX vẫn được giữ vì cần thiết cho bài báo. |
| PDF mới có còn bị tách pipeline/architecture giữa hai trang không? | Không còn pipeline/architecture dạng block để bị tách trang. |
| Section 3 còn mạch lạc không? | Có. Fig. 1 vẫn được nhắc ngay sau đoạn mô tả pipeline. |
| ANN architecture còn đủ thông tin không? | Có. Vẫn nêu input feature vector, hidden layers 128/64/32, BatchNorm, Dropout và output sigmoid. |
| Có thay đổi nội dung kỹ thuật hoặc số liệu không? | No technical results were changed. |
| Có sửa code ứng dụng không? | Không. |

## Kiểm tra build PDF

| Item | Result |
|---|---|
| Build engine | Tectonic/LaTeX with `llncs.cls` |
| Output PDF | `reports/springer_overleaf/main_applied_research_final_formatfix.pdf` |
| Output TeX | `reports/springer_overleaf/main_applied_research_final_formatfix.tex` |
| Số trang | 15 |
| Tác giả | `Ly-Cu DUONG` và `Van-Phuc VO` |
| Title | `Webcam-Based Working Posture Error Detection Using Normalized MediaPipe Landmarks and Lightweight Machine Learning` |

## Ghi chú

LaTeX còn cảnh báo `Underfull \\hbox` nhẹ tại đoạn có nhiều tên feature dài trong bảng/đoạn mô tả. Đây là warning dàn dòng của LaTeX, không phải lỗi compile và không liên quan đến pipeline/ANN arrow blocks đã được xử lý.
