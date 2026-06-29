# Báo cáo cập nhật bài báo Springer theo dataset và thực nghiệm mới

## 1. Kết quả đầu ra

- LaTeX: `reports/springer_overleaf/main_new_dataset_final.tex`
- PDF: `reports/springer_overleaf/main_new_dataset_final.pdf`
- Script xuất hình từ CSV: `reports/springer_overleaf/generate_new_dataset_figures.py`
- Tổng số trang PDF: **11 trang**, tính cả References.
- Template: Springer LNCS (`llncs.cls`), chế độ citation author-year.
- Tác giả: **Ly-Cu DUONG** và **Van-Phuc VO**.

Bản cũ không bị xóa hoặc ghi đè.

## 2. Dữ liệu đã xác minh trực tiếp

Đọc bằng `pandas` từ CSV:

| Split | Shape CSV | Video | Participant | Correct | Incorrect |
|---|---:|---:|---|---:|---:|
| Development | 12,680 x 108 | 94 | P01-P05 | 5,206 | 7,474 |
| External | 4,556 x 108 | 23 | P06-P07 | 2,001 | 2,555 |

Kết quả kiểm tra:

- Participant overlap: rỗng.
- Source-video overlap: rỗng.
- Manifest thật nằm tại `dataset/metadata/video_manifest.csv`.
- Manifest có 117 video: 94 raw/development và 23 external.

## 3. Các thông tin cũ đã thay thế

| Nội dung cũ | Nội dung mới |
|---|---|
| 84 development videos | 94 development videos |
| 11,022 development frames | 12,680 development frames |
| 4,438 Correct / 6,584 Incorrect | 5,206 Correct / 7,474 Incorrect |
| External 10 videos, 1,658 frames, P01 | External 23 videos, 4,556 frames, P06-P07 |
| HGB `normalized_99` | HGB `ergonomic_v2_with_view` |
| Threshold 0.65 | Calibrated threshold 0.76 |
| Accuracy 96.50%, F1 96.76%, MCC 92.97% | Accuracy 89.31%, F1 90.13%, MCC 0.7875 |
| Confusion matrix 734/34/24/866 | TN=1,846, FP=155, FN=332, TP=2,223 |
| ANN runtime 28.03-29.34 FPS | HGB processing benchmark 25.27-25.80 FPS |
| ANN được nhấn mạnh như model chính | ANN là neural baseline; HGB là model được chọn sau benchmark |

Tìm kiếm tự động không còn các số liệu và placeholder cũ trong LaTeX cuối.

## 4. Cấu trúc bài báo

Bài báo được rút gọn còn sáu mục lớn:

1. Introduction.
2. Related Work.
3. Proposed Webcam-Based Posture Monitoring System.
4. Experimental Protocol.
5. Evaluation and Discussion.
6. Conclusion and Future Work.

Abstract có 199 từ. Keywords có 5 từ khóa.

## 5. Benchmark được trình bày

Bảng so sánh mặc định dùng cùng threshold 0.50 và đủ chín phương pháp:

1. HistGradientBoosting.
2. Logistic Regression.
3. Random Forest.
4. SVM RBF.
5. Decision Tree.
6. KNN.
7. ANN/Keras.
8. MLPClassifier.
9. Rule-based Baseline.

HGB tại threshold mặc định:

- Accuracy 87.34%.
- Precision Incorrect 86.71%.
- Recall Incorrect 91.43%.
- F1 Incorrect 89.01%.
- MCC 0.7424.

HGB sau threshold sweep:

- Feature set: `ergonomic_v2_with_view`, 31 đặc trưng.
- Threshold 0.76.
- Accuracy 89.31%.
- Precision Incorrect 93.48%.
- Recall Incorrect 87.01%.
- F1 Incorrect 90.13%.
- MCC 0.7875.
- TN=1,846, FP=155, FN=332, TP=2,223.

Bài báo ghi rõ threshold 0.76 được chọn trên P06-P07 nên đây là calibrated external performance, không phải blind independent test.

## 6. Hình và bảng

### Hình

1. Kiến trúc pipeline webcam đến warning/logging.
2. Heatmap benchmark chín họ thuật toán tại threshold 0.50.
3. Confusion matrix và threshold sweep của HGB.
4. Participant-wise metrics và runtime HGB.

Các hình mới được xuất bằng tiếng Anh trực tiếp từ CSV:

- `newdata_fig1_system_architecture`
- `newdata_fig2_algorithm_benchmark`
- `newdata_fig3a_hgb_confusion_matrix`
- `newdata_fig3b_hgb_threshold_sweep`
- `newdata_fig4a_participant_metrics`
- `newdata_fig4b_runtime_metrics`

Mỗi hình có cả bản PNG và PDF vector trong `reports/springer_overleaf/figures`.

### Bảng

1. Feature groups.
2. Dataset split.
3. Benchmark chín phương pháp.
4. HGB overall và participant-wise.
5. Runtime benchmark.

Không đưa toàn bộ 87 cấu hình vào bài chính.

## 7. Kiểm tra PDF

PDF được build bằng:

```powershell
cd reports\springer_overleaf
..\..\.tools\tectonic\tectonic.exe -r 2 --keep-logs --keep-intermediates main_new_dataset_final.tex
```

Đã render toàn bộ 11 trang bằng Poppler và kiểm tra trực quan:

- Không có bảng hoặc hình bị cắt.
- Không có chữ tràn lề.
- Không có placeholder.
- Không có trang thứ 14.
- Hình và bảng được dẫn giải trong văn bản.
- References hiển thị đầy đủ trên hai trang cuối.

LaTeX không có lỗi build hoặc overfull box. Còn một số `Underfull \hbox` trong bảng chứa tên feature dài và một `Underfull \vbox` do phân bố float; các cảnh báo này không làm mất nội dung hoặc tràn lề.

## 8. Rủi ro học thuật còn lại

- Development chỉ có năm người và external chỉ có hai người.
- Nhãn là project-specific, chưa có chuyên gia ergonomic hoặc RULA/REBA xác nhận.
- Threshold 0.76 đã được hiệu chỉnh trên P06-P07.
- Chưa có untouched external set sau threshold calibration.
- Chưa đánh giá trên MultiPosture hoặc public benchmark tương thích.
- Runtime hiện là processing benchmark, chưa phải full GUI FPS.
- Chưa có formal ethics approval trong artifact hiện tại.
- Các video chứa người nhận diện được nên không thể công bố thô nếu chưa có consent phù hợp.

## 9. Kết luận

Bài báo đã được chuyển hoàn toàn sang protocol dữ liệu mới, phân biệt rõ benchmark threshold 0.50 và calibrated HGB threshold 0.76, thay runtime ANN bằng HGB, cập nhật vai trò ANN/HGB và giữ giới hạn claim phù hợp hướng Applied Research.
