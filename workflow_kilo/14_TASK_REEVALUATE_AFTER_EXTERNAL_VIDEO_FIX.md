# 14 Task Chạy Lại Đánh Giá Sau Khi Sửa Video External Sai Nhãn

Ngày tạo: 2026-05-28

## Trạng thái thực thi 2026-05-28

| Task | Trạng thái | Kết quả |
|---|---|---|
| TASK-1401 | Done | Video mới `P01_incorrect_004.mp4` đọc được bằng OpenCV, 2794 frames, 29.947 FPS, 1920x1080. |
| TASK-1402 | Done | Đã tạo lại `dataset/metadata/video_manifest.csv`; manifest vẫn có 94 video, external incorrect 5 video. |
| TASK-1403 | Done | Đã trích xuất lại external CSV: 1658 rows, 108 columns, 10 source videos, `P01_incorrect_004` có 200 rows. |
| TASK-1404 | Done | Đã tạo lại external ergonomic/combined features: 1658 rows cho mỗi file. |
| TASK-1405 | Done | ANN external mới: accuracy 90.169%, precision 95.609%, recall 85.618%, F1 90.338%, best threshold 0.10 với F1 91.889%. |
| TASK-1406 | Done | Video-wise mới: mean video accuracy 90.000%, std 11.770%; `P01_incorrect_004` accuracy 77.500%, false negatives 45. |
| TASK-1407 | Done | Benchmark mới: SVM RBF + ergonomic đạt F1 incorrect 95.107%, cao nhất trong benchmark external hiện tại. |
| TASK-1408 | Done | Ablation mới: ergonomic đạt F1 incorrect 95.107%, combined đạt 93.684%, raw đạt 91.580%. |
| TASK-1409 | Done | Error analysis mới: correct 1495, false negatives 128, false positives 35. |
| TASK-1410 | Done | Đã sinh lại paper artifacts trong `reports/figures` và `reports/tables`. |
| TASK-1411 | Done | Đã cập nhật các report/narrative có số liệu cũ liên quan external evaluation. |
| TASK-1412 | Done | `py_compile` pass; `pytest tests -q` đạt 23 passed, 1 skipped. |

## Bối cảnh

Video:

```text
dataset/external_videos/incorrect/P01_incorrect_004.mp4
```

trước đó bị đặt nhầm nội dung: tên file và folder là `incorrect`, nhưng nội dung thực tế lại là tư thế đúng. Hiện tại video này đã được thay bằng video tư thế sai đúng với tên file và folder.

Vì tên file không đổi nhưng nội dung video đã đổi, các file kết quả cũ liên quan đến external test không còn đáng tin cậy. Cần chạy lại toàn bộ các bước phụ thuộc vào external video, đặc biệt là:

- `dataset/metadata/video_manifest.csv`
- `dataset/processed/posture_external_test_2fps_with_metadata.csv`
- `dataset/processed/posture_external_test_2fps_ergonomic_features.csv`
- `dataset/processed/posture_external_test_2fps_combined_features.csv`
- `reports/results/external_*`
- `reports/results/video_wise_metrics.csv`
- `reports/results/classifier_benchmark_external.csv`
- `reports/results/feature_ablation.csv`
- `reports/results/predictions_external.csv`
- `reports/results/error_cases.csv`
- `reports/ERROR_ANALYSIS_BY_VIDEO_PERSON_VIEW.md`
- các bảng/hình trong `reports/tables` và `reports/figures` lấy từ external results.

## Mục tiêu

1. Xóa ảnh hưởng của kết quả cũ được tạo từ video external bị sai nội dung.
2. Tái trích xuất landmark từ video external mới.
3. Chạy lại đánh giá ANN, threshold sweep, confusion matrix, ROC/PR/calibration.
4. Chạy lại video-wise error analysis để kiểm tra `P01_incorrect_004.mp4`.
5. Chạy lại benchmark và ablation dùng external set.
6. Cập nhật lại report/tables/figures phục vụ bài báo.

## Nguyên tắc

1. Không cần đổi tên file vì tên `P01_incorrect_004.mp4` hiện đã đúng.
2. Không cần chạy lại raw train CSV nếu raw dataset không thay đổi.
3. Không cần chạy lại participant-wise evaluation nếu chỉ thay external video.
4. Bắt buộc chạy lại external CSV vì nội dung frame/landmark đã thay đổi.
5. Bắt buộc chạy lại manifest vì SHA256, duration, frame count và size của video có thể đã đổi.
6. Không sửa số liệu thủ công trong report. Mọi report phải sinh từ script.

---

## TASK-1401: Kiểm tra video external mới

Mục tiêu: xác nhận file `P01_incorrect_004.mp4` tồn tại, đọc được, nằm đúng folder và có metadata video hợp lệ.

Lệnh kiểm tra:

```powershell
Get-Item dataset/external_videos/incorrect/P01_incorrect_004.mp4 |
  Select-Object FullName,Length,LastWriteTime
```

Kiểm tra bằng OpenCV:

```powershell
@'
import cv2
from pathlib import Path

path = Path("dataset/external_videos/incorrect/P01_incorrect_004.mp4")
cap = cv2.VideoCapture(str(path))
print("exists:", path.exists())
print("opened:", cap.isOpened())
print("frames:", int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0))
print("fps:", float(cap.get(cv2.CAP_PROP_FPS) or 0))
print("width:", int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0))
print("height:", int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0))
cap.release()
'@ | .\.venv\Scripts\python.exe -
```

Acceptance criteria:

- File tồn tại.
- OpenCV mở được video.
- `frames > 0`.
- `fps > 0`.
- Video nằm trong folder `dataset/external_videos/incorrect`.

---

## TASK-1402: Tạo lại video manifest

Mục tiêu: cập nhật lại SHA256, dung lượng, duration và số frame của video external mới.

Lệnh chạy:

```powershell
.\.venv\Scripts\python.exe src/15_build_video_manifest.py
```

Output cần cập nhật:

```text
dataset/metadata/video_manifest.csv
reports/DATASET_VIDEO_MANIFEST_SUMMARY.md
```

Kiểm tra riêng video vừa thay:

```powershell
@'
import pandas as pd
df = pd.read_csv("dataset/metadata/video_manifest.csv")
row = df[df["source_video"].str.contains("P01_incorrect_004.mp4", regex=False)]
print(row.T)
'@ | .\.venv\Scripts\python.exe -
```

Acceptance criteria:

- Manifest vẫn có 94 video.
- External vẫn có 10 video.
- External incorrect vẫn có 5 video.
- `P01_incorrect_004.mp4` có `label=1`, `label_name=incorrect`.
- SHA256 mới phản ánh file đã thay.

---

## TASK-1403: Trích xuất lại external CSV có metadata

Mục tiêu: tái tạo landmark CSV cho external set từ video mới.

Lệnh chạy:

```powershell
.\.venv\Scripts\python.exe src/2_extract_features.py `
  --input-root dataset/external_videos `
  --sample-fps 2 `
  --include-metadata `
  --output dataset/processed/posture_external_test_2fps_with_metadata.csv
```

Output:

```text
dataset/processed/posture_external_test_2fps_with_metadata.csv
```

Kiểm tra:

```powershell
@'
import pandas as pd
df = pd.read_csv("dataset/processed/posture_external_test_2fps_with_metadata.csv")
print("shape:", df.shape)
print("labels:")
print(df["label"].value_counts().sort_index())
print("videos:", df["source_video"].nunique())
print(df[df["source_video"].str.contains("P01_incorrect_004.mp4", regex=False)][["source_video","label","participant_id","view_angle"]].head())
print("rows P01_incorrect_004:", df["source_video"].str.contains("P01_incorrect_004.mp4", regex=False).sum())
'@ | .\.venv\Scripts\python.exe -
```

Acceptance criteria:

- CSV có đủ 99 landmark columns.
- Có metadata: `source_video`, `frame_index`, `timestamp_sec`, `participant_id`, `view_angle`, `camera_type`.
- Có 10 `source_video`.
- `P01_incorrect_004.mp4` có `label=1`.
- Số row của `P01_incorrect_004.mp4` lớn hơn 0.

---

## TASK-1404: Tạo lại ergonomic và combined features cho external

Mục tiêu: cập nhật feature set external sau khi trích xuất lại landmark.

Lệnh chạy:

```powershell
.\.venv\Scripts\python.exe src/16_build_ergonomic_features.py
```

Output liên quan:

```text
dataset/processed/posture_external_test_2fps_ergonomic_features.csv
dataset/processed/posture_external_test_2fps_combined_features.csv
reports/ERGONOMIC_FEATURES_DESCRIPTION.md
```

Kiểm tra:

```powershell
@'
import pandas as pd
for path in [
    "dataset/processed/posture_external_test_2fps_ergonomic_features.csv",
    "dataset/processed/posture_external_test_2fps_combined_features.csv",
]:
    df = pd.read_csv(path)
    print(path, df.shape, "videos:", df["source_video"].nunique())
    print("P01_incorrect_004 rows:", df["source_video"].str.contains("P01_incorrect_004.mp4", regex=False).sum())
'@ | .\.venv\Scripts\python.exe -
```

Acceptance criteria:

- Ergonomic và combined CSV có 10 video external.
- Row count của combined external khớp với external metadata CSV.
- Metadata và label không bị mất.

---

## TASK-1405: Chạy lại ANN external evaluation

Mục tiêu: cập nhật metric ANN, confusion matrix, threshold sweep, prediction CSV và curve sau khi video mới được thay.

Lệnh chạy:

```powershell
.\.venv\Scripts\python.exe src/6_evaluate_external.py `
  --dataset dataset/processed/posture_external_test_2fps_with_metadata.csv `
  --threshold 0.5
```

Output:

```text
reports/results/external_metrics.txt
reports/results/external_confusion_matrix.csv
reports/results/external_threshold_sweep.csv
reports/results/external_predictions.csv
reports/results/external_error_by_video.csv
reports/results/roc_curve.png
reports/results/pr_curve.png
reports/results/calibration_curve.png
```

Kiểm tra nhanh:

```powershell
Get-Content reports/results/external_metrics.txt
```

Acceptance criteria:

- Metric external mới được sinh lại.
- Confusion matrix không còn phản ánh video cũ.
- Threshold sweep mới có best threshold mới.
- Nếu recall lớp incorrect tăng so với trước thì ghi nhận trong report.

---

## TASK-1406: Chạy lại video-wise evaluation

Mục tiêu: cập nhật bảng đánh giá theo từng video, đặc biệt là `P01_incorrect_004.mp4`.

Lệnh chạy:

```powershell
.\.venv\Scripts\python.exe src/7_video_wise_evaluation.py `
  --dataset dataset/processed/posture_external_test_2fps_with_metadata.csv `
  --threshold 0.5
```

Output:

```text
reports/results/video_wise_metrics.csv
reports/results/video_wise_summary.md
```

Kiểm tra riêng video vừa sửa:

```powershell
@'
import pandas as pd
df = pd.read_csv("reports/results/video_wise_metrics.csv")
row = df[df["source_video"].str.contains("P01_incorrect_004.mp4", regex=False)]
print(row.T)
'@ | .\.venv\Scripts\python.exe -
```

Acceptance criteria:

- `P01_incorrect_004.mp4` vẫn xuất hiện trong video-wise metrics.
- Label của video là incorrect.
- `false_negative`, `accuracy`, `mean_prob_incorrect` được tính lại từ video mới.
- Nếu video vẫn là worst case thì kết luận là model thật sự yếu ở kiểu sai tư thế đó, không còn do nhầm nhãn.
- Nếu video không còn là worst case thì cập nhật phần thảo luận lỗi trước đó.

---

## TASK-1407: Chạy lại benchmark classifiers trên external set

Mục tiêu: cập nhật so sánh Random Forest, SVM, Logistic Regression, KNN, HistGradientBoosting trên external set mới.

Lệnh chạy:

```powershell
.\.venv\Scripts\python.exe src/18_benchmark_classifiers.py
```

Output:

```text
reports/results/classifier_benchmark_external.csv
reports/BENCHMARK_CLASSIFIERS_SUMMARY.md
```

Kiểm tra:

```powershell
Get-Content reports/BENCHMARK_CLASSIFIERS_SUMMARY.md
```

Acceptance criteria:

- Bảng benchmark được sắp xếp lại theo F1 incorrect.
- Model tốt nhất có thể thay đổi so với kết quả cũ.
- Không còn dùng metric sinh từ video external bị nhầm nội dung.

---

## TASK-1408: Chạy lại feature ablation

Mục tiêu: cập nhật ảnh hưởng của feature set vì external set đã thay đổi.

Lệnh chạy:

```powershell
.\.venv\Scripts\python.exe src/19_ablation_feature_sets.py
```

Output:

```text
reports/results/feature_ablation.csv
reports/FEATURE_ABLATION_SUMMARY.md
```

Acceptance criteria:

- Kết quả ablation mới được sinh từ external combined CSV mới.
- Kết luận `raw`, `ergonomic`, `combined`, `without_neck`, `without_hand` được cập nhật.
- Nếu neck/hand features thay đổi vai trò, ghi nhận trong phần discussion.

---

## TASK-1409: Chạy lại error analysis theo video/người/góc quay

Mục tiêu: cập nhật report lỗi sau khi video nhầm nhãn đã được thay đúng.

Lệnh chạy:

```powershell
.\.venv\Scripts\python.exe src/20_error_analysis.py `
  --dataset dataset/processed/posture_external_test_2fps_with_metadata.csv `
  --threshold 0.5
```

Output:

```text
reports/results/predictions_external.csv
reports/results/error_cases.csv
reports/ERROR_ANALYSIS_BY_VIDEO_PERSON_VIEW.md
```

Kiểm tra:

```powershell
Get-Content reports/ERROR_ANALYSIS_BY_VIDEO_PERSON_VIEW.md
```

Acceptance criteria:

- Error counts được cập nhật.
- Worst videos được cập nhật.
- `P01_incorrect_004.mp4` không còn bị diễn giải là lỗi do dataset nhầm nhãn.
- Nếu `P01_incorrect_004.mp4` vẫn nhiều false negative, ghi rõ: "video này là hard case thật sau khi đã sửa dữ liệu".

---

## TASK-1410: Cập nhật paper artifacts

Mục tiêu: đồng bộ lại bảng/hình paper từ kết quả external mới.

Lệnh chạy:

```powershell
.\.venv\Scripts\python.exe src/14_generate_paper_artifacts.py
```

Output bị ảnh hưởng:

```text
reports/tables/video_manifest.csv
reports/tables/video_wise_metrics.csv
reports/tables/external_threshold_sweep.csv
reports/tables/classifier_benchmark_external.csv
reports/tables/feature_ablation.csv
reports/figures/external_confusion_matrix.png
reports/figures/external_threshold_sweep.png
reports/PAPER_ARTIFACTS.md
```

Acceptance criteria:

- `reports/tables` khớp với `reports/results`.
- Hình confusion matrix và threshold sweep là bản mới.
- Không còn artifact lấy từ video external cũ.

---

## TASK-1411: Cập nhật narrative trong report nghiên cứu

Mục tiêu: sửa lại phần thảo luận trước đây từng ghi `P01_incorrect_004.mp4` là failure case nghiêm trọng do mô hình.

Các file cần kiểm tra/cập nhật:

```text
reports/ERROR_ANALYSIS_BY_VIDEO_PERSON_VIEW.md
reports/SPRINGER_PROJECT_STATUS_UPGRADE_PLAN_2026.md
reports/PROJECT_COMPLETION_AND_GAP_ANALYSIS_2026.md
reports/springer_results_draft.md
reports/TONGQUANDUAN.md
reports/NOVELTY_AND_CONTRIBUTION_ANALYSIS_SPRINGER.md
```

Nội dung cần chỉnh:

1. Ghi chú rõ video `P01_incorrect_004.mp4` trước đây từng bị sai nội dung và đã được thay bằng video sai tư thế đúng.
2. Xóa/điều chỉnh các kết luận cũ nếu chúng dựa trên video bị nhầm.
3. Cập nhật lại:
   - external accuracy
   - F1 incorrect
   - recall incorrect
   - worst videos
   - threshold tốt nhất
   - model benchmark tốt nhất
4. Nếu kết quả cải thiện, ghi rõ nguyên nhân là do sửa dữ liệu external.
5. Nếu kết quả giảm hoặc lỗi vẫn còn, ghi rõ đây là giới hạn thật của model với hard-case video.

Acceptance criteria:

- Không còn câu kết luận nào dựa trên video external bị nhầm nội dung.
- Số liệu trong report khớp với CSV mới.
- Discussion trung thực: dữ liệu đã được sửa, evaluation đã chạy lại.

---

## TASK-1412: Kiểm thử nhanh sau khi chạy lại

Mục tiêu: đảm bảo script và test chính không hỏng sau khi tái sinh kết quả.

Lệnh chạy:

```powershell
.\.venv\Scripts\python.exe -m py_compile `
  src/2_extract_features.py `
  src/6_evaluate_external.py `
  src/7_video_wise_evaluation.py `
  src/14_generate_paper_artifacts.py `
  src/15_build_video_manifest.py `
  src/16_build_ergonomic_features.py `
  src/18_benchmark_classifiers.py `
  src/19_ablation_feature_sets.py `
  src/20_error_analysis.py
```

Nếu có thời gian, chạy thêm:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
```

Acceptance criteria:

- `py_compile` pass.
- Nếu chạy pytest, không có test fail mới.
- Nếu có fail do môi trường/camera/video codec, phải ghi rõ trong report.

---

## Thứ tự thực thi nhanh nhất

Chạy theo đúng thứ tự:

1. TASK-1401: Kiểm tra video mới.
2. TASK-1402: Tạo lại manifest.
3. TASK-1403: Trích xuất lại external CSV.
4. TASK-1404: Tạo lại ergonomic/combined features.
5. TASK-1405: Chạy lại ANN external evaluation.
6. TASK-1406: Chạy lại video-wise evaluation.
7. TASK-1407: Chạy lại benchmark classifiers.
8. TASK-1408: Chạy lại feature ablation.
9. TASK-1409: Chạy lại error analysis.
10. TASK-1410: Cập nhật paper artifacts.
11. TASK-1411: Cập nhật narrative report.
12. TASK-1412: Kiểm thử nhanh.

## Lệnh chạy gộp đề xuất

Nếu muốn chạy liên tục sau khi đã kiểm tra video:

```powershell
.\.venv\Scripts\python.exe src/15_build_video_manifest.py

.\.venv\Scripts\python.exe src/2_extract_features.py `
  --input-root dataset/external_videos `
  --sample-fps 2 `
  --include-metadata `
  --output dataset/processed/posture_external_test_2fps_with_metadata.csv

.\.venv\Scripts\python.exe src/16_build_ergonomic_features.py

.\.venv\Scripts\python.exe src/6_evaluate_external.py `
  --dataset dataset/processed/posture_external_test_2fps_with_metadata.csv `
  --threshold 0.5

.\.venv\Scripts\python.exe src/7_video_wise_evaluation.py `
  --dataset dataset/processed/posture_external_test_2fps_with_metadata.csv `
  --threshold 0.5

.\.venv\Scripts\python.exe src/18_benchmark_classifiers.py

.\.venv\Scripts\python.exe src/19_ablation_feature_sets.py

.\.venv\Scripts\python.exe src/20_error_analysis.py `
  --dataset dataset/processed/posture_external_test_2fps_with_metadata.csv `
  --threshold 0.5

.\.venv\Scripts\python.exe src/14_generate_paper_artifacts.py
```

## Kết quả mong đợi sau khi hoàn thành

Sau khi hoàn thành task này, dự án sẽ có:

- External CSV mới phản ánh đúng video `P01_incorrect_004.mp4`.
- Manifest mới với SHA/duration/frame count đúng.
- External metrics mới.
- Video-wise error analysis mới.
- Benchmark và ablation mới.
- Paper artifacts mới.
- Report nghiên cứu không còn dựa trên dữ liệu external bị nhầm nội dung.

Kết luận cần ghi sau khi chạy xong:

```text
External evaluation was regenerated after replacing the mislabeled-content video P01_incorrect_004.mp4 with a true incorrect-posture video. All reported external metrics, video-wise analysis, benchmark results, ablation results, and error analysis are based on the corrected external dataset.
```
