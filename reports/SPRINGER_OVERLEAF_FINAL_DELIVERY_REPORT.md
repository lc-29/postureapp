# Báo cáo bàn giao gói Springer Overleaf

## Mục tiêu đã xử lý

Mục tiêu là tạo báo cáo nghiên cứu khoa học theo định dạng Springer, có thể đưa lên Overleaf để biên dịch PDF, dựa trên toàn bộ nội dung và kết quả hiện có của dự án phát hiện lỗi tư thế làm việc qua webcam.

## Gói bàn giao chính

| Hạng mục | Đường dẫn | Trạng thái |
|---|---|---|
| Thư mục gói Overleaf | `reports/springer_overleaf/` | Đã tạo |
| File nén upload Overleaf | `reports/springer_overleaf_package.zip` | Đã tạo |
| File LaTeX chính | `reports/springer_overleaf/main.tex` | Đã tạo |
| File PDF compile thử | `reports/springer_overleaf/main.pdf` | Đã compile thành công |
| BibTeX references | `reports/springer_overleaf/references.bib` | Đã tạo |
| Springer LNCS class | `reports/springer_overleaf/llncs.cls` | Đã kèm trong gói |
| Springer bibliography style | `reports/springer_overleaf/splncs04.bst` | Đã kèm trong gói |
| Hướng dẫn Overleaf | `reports/springer_overleaf/README_OVERLEAF.md` | Đã tạo |
| Checklist gói Overleaf | `reports/springer_overleaf/OVERLEAF_PACKAGE_CHECKLIST.md` | Đã tạo |

## Công cụ đã cài vào D:\Tools Springer

| Công cụ | Đường dẫn | Vai trò |
|---|---|---|
| Springer LNCS template | `D:\Tools Springer\lncs\llncs.cls` | Class file Springer LNCS |
| Springer BibTeX style | `D:\Tools Springer\lncs\splncs04.bst` | Style tài liệu tham khảo |
| Tectonic portable | `D:\Tools Springer\tectonic\tectonic.exe` | Biên dịch LaTeX local để kiểm tra trước Overleaf |

## Nội dung khoa học đã có trong main.tex

1. Title theo hướng Springer:
   - `Webcam-Based Working Posture Error Detection Using Normalized MediaPipe Landmarks and Lightweight Machine Learning`
2. Abstract dưới 250 từ.
3. Keywords đúng định dạng LNCS.
4. Introduction có background, urgency, research gap và contributions.
5. Related Work theo 3 nhóm:
   - sensor/depth-camera methods;
   - RGB-camera posture recognition;
   - OpenPose/MediaPipe landmark-based posture analysis.
6. Proposed Method có:
   - system architecture bằng TikZ;
   - landmark extraction;
   - feature construction;
   - ANN/Keras application model;
   - rule-based baseline;
   - temporal smoothing and logging;
   - Algorithm 1 dạng text.
7. Dataset and Feature Extraction có:
   - 84 raw videos;
   - 5 participants P01-P05;
   - 11,022 sampled frames;
   - 4,438 Correct và 6,584 Incorrect;
   - corrected external set 10 videos, 1,658 frames;
   - project-specific label limitation.
8. Experimental Setup có:
   - Python/library versions;
   - model families;
   - evaluation protocol;
   - metric formulas.
9. Results and Discussion có:
   - rule-based vs ANN;
   - classifier/feature comparison;
   - final selected HGB model;
   - participant-wise evaluation;
   - runtime benchmark;
   - error and temporal behavior.
10. Desktop Application Implementation có:
   - realtime deployment role;
   - SQLite logging;
   - dashboard/logging flow bằng TikZ.
11. Limitations trung thực.
12. Conclusion and Future Work.
13. References theo BibTeX numeric style `splncs04`.

## Hình và bảng đã có

### Hình

| Hình | Nguồn | Trạng thái |
|---|---|---|
| System architecture | TikZ trong `main.tex` | Có |
| Feature construction pipeline | TikZ trong `main.tex` | Có |
| Confusion matrix | `figures/external_confusion_matrix.png` | Có |
| Threshold calibration | `figures/external_threshold_sweep.png` | Có |
| Temporal smoothing effect | `figures/temporal_smoothing_effect.png` | Có |
| SQLite logging flow | TikZ trong `main.tex` | Có |

### Bảng

| Bảng | Nội dung | Trạng thái |
|---|---|---|
| Table 1 | Dataset splits | Có |
| Table 2 | Feature groups | Có |
| Table 3 | Rule-based vs ANN | Có |
| Table 4 | Top classifier/feature combinations | Có |
| Table 5 | Final selected model | Có |
| Table 6 | Participant-wise evaluation | Có |
| Table 7 | Runtime benchmark | Có |

## Kiểm tra kỹ thuật đã thực hiện

Lệnh kiểm tra local:

```powershell
cd D:\posture_detection_app\reports\springer_overleaf
& "D:\Tools Springer\tectonic\tectonic.exe" -X compile main.tex
```

Kết quả:

- `main.pdf` được tạo thành công.
- Không có lỗi LaTeX fatal.
- Citation keys trong `main.tex` đều tồn tại trong `references.bib`.
- Các file ảnh được gọi bằng `\includegraphics` đều tồn tại.
- Còn một số cảnh báo `Underfull \hbox` từ bảng/reference; đây là cảnh báo dàn trang thường gặp, không chặn compile.

## Cách dùng trên Overleaf

1. Upload file `reports/springer_overleaf_package.zip` lên Overleaf.
2. Chọn `main.tex` làm main file.
3. Recompile.
4. Nếu tài liệu tham khảo chưa hiện ngay, recompile thêm một lần.
5. Nếu hội thảo yêu cầu anonymized submission, sửa phần `\author{}` và `\institute{}` trong `main.tex`.

## Những điểm chưa nên claim quá mức

Các điểm sau đã được ghi là limitation hoặc future work, không được viết thành claim kết quả:

1. Dataset hiện có 5 participants.
2. Corrected external set chỉ có P01.
3. Nhãn Correct/Incorrect là project-specific.
4. Chưa có expert ergonomic annotation hoặc RULA/REBA.
5. Chưa chạy public benchmark như MultiPosture.
6. App hiện dùng ANN/Keras, trong khi HGB là selected experimental model.
7. Runtime hiện là processing latency, chưa phải full GUI FPS.

## Kết luận bàn giao

Gói Springer Overleaf đã sẵn sàng để upload và biên dịch. Về mặt kỹ thuật, package có đầy đủ `main.tex`, class/style Springer, bibliography, figures, README, checklist và PDF compile thử. Về mặt học thuật, bài đã phản ánh đúng dữ liệu và kết quả hiện có của dự án, đồng thời ghi rõ các giới hạn chưa có bằng chứng để tránh claim quá mức.
