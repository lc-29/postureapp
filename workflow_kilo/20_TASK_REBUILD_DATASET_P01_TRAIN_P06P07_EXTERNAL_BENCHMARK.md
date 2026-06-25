# 20_TASK_REBUILD_DATASET_P01_TRAIN_P06P07_EXTERNAL_BENCHMARK

## Muc tieu

Lam lai toan bo pipeline du lieu va thuc nghiem sau khi thay doi split dataset:

```text
Raw/train/development:
- P01-P05
- Bao gom them 10 video P01 truoc day nam trong external, nay da chuyen vao raw_videos

External unseen-participant test:
- P06-P07
- Tong 23 video moi
```

Muc tieu khoa hoc la bien external test thanh bo kiem thu nguoi moi that su, khong con external P01 nhu protocol cu. Sau khi hoan thanh, tat ca CSV, manifest, model registry, benchmark, threshold calibration, final evaluation, error analysis va bao cao lien quan phai khop voi split moi.

---

## Nguyen tac bat buoc

- Khong xoa video goc.
- Khong doi label thu muc neu chua xem video va xac nhan nhan dung/sai.
- Khong dung ket qua cu cua external P01 lam ket qua final moi.
- Khong claim state-of-the-art.
- Khong bia so lieu. Moi so lieu phai lay tu CSV/report moi sinh ra.
- Neu script bi loi, dung lai va ghi ro loi; khong tiep tuc train/evaluate tren CSV cu.
- Truoc khi ghi de artifact quan trong, tao backup hoac it nhat ghi lai timestamp/file cu.
- External moi phai chi gom P06-P07. Neu external con P01 thi protocol chua dat.
- Raw/train moi chi gom P01-P05. Neu raw co P06/P07 thi da lam ro ri du lieu external vao train.

---

## Trang thai dau vao hien tai can xac nhan

Kiem tra thu muc video:

```powershell
Get-ChildItem dataset/raw_videos -Recurse -File -Include *.mp4 | Measure-Object
Get-ChildItem dataset/external_videos -Recurse -File -Include *.mp4 | Measure-Object
```

Ket qua mong doi sau khi nguoi dung da di chuyen video:

```text
dataset/raw_videos:
- 94 video
- participant: P01, P02, P03, P04, P05

dataset/external_videos:
- 23 video
- participant: P06, P07
- correct: 11 video
- incorrect: 12 video
- view_angle: front, side_30, side_90
```

Kiem tra khong con loi `font`:

```powershell
Get-ChildItem dataset/external_videos -Recurse -File | Where-Object { $_.Name -like '*font*' }
```

Neu con file `font`, doi thanh `front` truoc khi chay pipeline.

---

## File/thu muc can backup truoc

Tao thu muc backup co timestamp, vi cac lenh sau se ghi de CSV/report/model:

```text
outputs/backups/rebuild_dataset_p06_p07_YYYYMMDD_HHMMSS/
```

Backup toi thieu:

```text
dataset/metadata/video_manifest.csv
dataset/processed/posture_data_2fps_with_metadata.csv
dataset/processed/posture_external_test_2fps_with_metadata.csv
dataset/processed/posture_data_2fps_ergonomic_features.csv
dataset/processed/posture_external_test_2fps_ergonomic_features.csv
dataset/processed/posture_data_2fps_combined_features.csv
dataset/processed/posture_external_test_2fps_combined_features.csv
models/model_registry.json
models/registry/
reports/results/
reports/DATASET_MANIFEST.md
reports/DATASET_VIDEO_MANIFEST_SUMMARY.md
reports/MODEL_SELECTION_REPORT.md
reports/FINAL_EVALUATION_REPORT.md
reports/THRESHOLD_CALIBRATION_REPORT.md
reports/BENCHMARK_CLASSIFIERS_SUMMARY.md
```

Khong can backup video neu video goc da co ban sao rieng, nhung khong duoc xoa/chuyen tiep video trong task nay.

---

## Buoc 1 - Kiem tra video split moi

Chay script kiem tra nhanh bang Python hoac PowerShell de bao cao:

- Tong video raw/external.
- So video correct/incorrect theo split.
- Participant trong raw/external.
- View angle trong raw/external.
- File sai pattern.
- File co label trong ten khac thu muc.
- File trung ten.
- File dung luong 0 byte.

Tieu chi dat:

```text
Raw:
- chi co P01-P05
- khong co P06/P07

External:
- chi co P06/P07
- khong co P01-P05
- khong co view_angle unknown do sai ten
- khong co file sai pattern
```

Pattern ten file nen dung:

```text
P06_correct_front_001.mp4
P06_correct_side_30_001.mp4
P06_correct_side_90_001.mp4
P06_incorrect_front_001.mp4
P06_incorrect_side_30_001.mp4
P06_incorrect_side_90_001.mp4
```

---

## Buoc 2 - Build lai video manifest

Chay:

```powershell
python src/15_build_video_manifest.py
```

File dau ra:

```text
dataset/metadata/video_manifest.csv
reports/DATASET_VIDEO_MANIFEST_SUMMARY.md
```

Kiem tra bat buoc:

```powershell
python - <<'PY'
import pandas as pd
df = pd.read_csv('dataset/metadata/video_manifest.csv')
print(df.shape)
print(df.groupby(['dataset_split', 'label_name']).size())
print(df.groupby(['dataset_split', 'participant_id']).size())
print(df.groupby(['dataset_split', 'view_angle']).size())
print(df['source_video'].map(lambda p: __import__('pathlib').Path(p).exists()).value_counts())
PY
```

Tieu chi dat:

```text
Total videos: 117
Raw videos: 94
External videos: 23
Raw participants: P01-P05
External participants: P06-P07
External view_angle khong co unknown
Tat ca source_video ton tai tren disk
```

Neu manifest van co `dataset/external_videos/...P01...`, dung lai vi CSV/report cu chua duoc rebuild dung.

---

## Buoc 3 - Trich xuat lai landmark CSV raw/train

Chay:

```powershell
python src/2_extract_features.py `
  --input-root dataset/raw_videos `
  --sample-fps 2 `
  --include-metadata `
  --output dataset/processed/posture_data_2fps_with_metadata.csv
```

Neu muon giu ban CSV legacy khong metadata cho ANN cu:

```powershell
python src/2_extract_features.py `
  --input-root dataset/raw_videos `
  --sample-fps 2 `
  --output dataset/posture_data_2fps.csv
```

Kiem tra:

```powershell
python - <<'PY'
import pandas as pd
df = pd.read_csv('dataset/processed/posture_data_2fps_with_metadata.csv')
print(df.shape)
print(df['label'].value_counts().sort_index())
print(df['participant_id'].value_counts().sort_index())
print(df['view_angle'].value_counts().sort_index())
print(df['source_video'].nunique())
PY
```

Tieu chi dat:

```text
participant_id chi gom P01-P05
source_video unique phai bang 94 hoac bang so video co frame hop le neu MediaPipe bo het mot video
khong co P06/P07 trong train CSV
```

---

## Buoc 4 - Trich xuat lai landmark CSV external P06-P07

Chay:

```powershell
python src/2_extract_features.py `
  --input-root dataset/external_videos `
  --sample-fps 2 `
  --include-metadata `
  --output dataset/processed/posture_external_test_2fps_with_metadata.csv
```

Neu muon giu ban CSV legacy khong metadata:

```powershell
python src/2_extract_features.py `
  --input-root dataset/external_videos `
  --sample-fps 2 `
  --output dataset/posture_external_test_2fps.csv
```

Kiem tra:

```powershell
python - <<'PY'
import pandas as pd
df = pd.read_csv('dataset/processed/posture_external_test_2fps_with_metadata.csv')
print(df.shape)
print(df['label'].value_counts().sort_index())
print(df['participant_id'].value_counts().sort_index())
print(df['view_angle'].value_counts().sort_index())
print(df['source_video'].nunique())
PY
```

Tieu chi dat:

```text
participant_id chi gom P06 va P07
source_video unique phai bang 23 hoac bang so video co frame hop le neu MediaPipe bo het mot video
khong co P01-P05 trong external CSV
view_angle gom front, side_30, side_90
```

---

## Buoc 5 - Build lai ergonomic va combined features

Chay:

```powershell
python src/16_build_ergonomic_features.py
```

File dau ra:

```text
dataset/processed/posture_data_2fps_ergonomic_features.csv
dataset/processed/posture_data_2fps_combined_features.csv
dataset/processed/posture_external_test_2fps_ergonomic_features.csv
dataset/processed/posture_external_test_2fps_combined_features.csv
reports/ERGONOMIC_FEATURES_DESCRIPTION.md
```

Kiem tra:

```powershell
python - <<'PY'
import pandas as pd
files = [
 'dataset/processed/posture_data_2fps_ergonomic_features.csv',
 'dataset/processed/posture_data_2fps_combined_features.csv',
 'dataset/processed/posture_external_test_2fps_ergonomic_features.csv',
 'dataset/processed/posture_external_test_2fps_combined_features.csv',
]
for f in files:
    df = pd.read_csv(f)
    print(f, df.shape, df['participant_id'].value_counts().sort_index().to_dict())
PY
```

Tieu chi dat:

```text
Raw combined chi co P01-P05
External combined chi co P06-P07
Cot metadata van con day du: source_video, frame_index, timestamp_sec, sample_fps, video_fps, participant_id, view_angle, camera_type
```

---

## Buoc 6 - Benchmark classifier tren external P06-P07

Chay benchmark bo classifier:

```powershell
python src/18_benchmark_classifiers.py
```

File dau ra:

```text
reports/results/classifier_benchmark_external.csv
reports/BENCHMARK_CLASSIFIERS_SUMMARY.md
```

Kiem tra:

```powershell
python - <<'PY'
import pandas as pd
df = pd.read_csv('reports/results/classifier_benchmark_external.csv')
print(df.sort_values('f1_incorrect', ascending=False).head(10))
PY
```

Can ghi nhan:

- Model nao tot nhat tren external P06-P07.
- Feature group nao tot nhat.
- Ket qua co giam so voi external P01 cu hay khong.
- Neu ket qua giam, day la ket qua co gia tri vi external moi la nguoi chua tung thay.

---

## Buoc 7 - Train lai model registry

Chay:

```powershell
python src/21_train_model_registry.py
```

File dau ra:

```text
models/model_registry.json
models/registry/
reports/MODEL_SELECTION_REPORT.md
reports/results/model_registry_metrics.csv
```

Kiem tra:

```powershell
python - <<'PY'
import json, pandas as pd
reg = json.load(open('models/model_registry.json', encoding='utf-8'))
print('selected_model_id:', reg.get('selected_model_id'))
df = pd.read_csv('reports/results/model_registry_metrics.csv')
print(df.sort_values('f1_incorrect', ascending=False).head(10))
PY
```

Tieu chi dat:

```text
Registry duoc tao lai sau khi CSV moi da duoc tao
selected_model_id phai dua tren external P06-P07, khong phai external P01 cu
```

---

## Buoc 8 - Calibrate threshold tren external P06-P07

Chay:

```powershell
python src/22_calibrate_threshold.py
```

File dau ra:

```text
reports/results/threshold_calibration_final.csv
reports/THRESHOLD_CALIBRATION_REPORT.md
models/registry/<selected_model_id>/threshold.json
```

Kiem tra:

```powershell
python - <<'PY'
import pandas as pd
df = pd.read_csv('reports/results/threshold_calibration_final.csv')
print(df.sort_values('f1_incorrect', ascending=False).head(10))
PY
```

Can ghi ro trong report:

- threshold duoc chon theo balanced_f1 hay theo uu tien recall.
- neu demo app uu tien it bo sot sai tu the, co the chon threshold recall-friendly, nhung paper/luan van nen bao cao balanced_f1.

---

## Buoc 9 - Chay final evaluation protocol moi

Chay:

```powershell
python src/23_final_evaluation_protocol.py
```

File dau ra:

```text
reports/FINAL_EVALUATION_REPORT.md
reports/results/final_evaluation_metrics.csv
reports/results/final_external_predictions.csv
reports/results/final_video_wise_metrics.csv
reports/results/final_participant_wise_metrics.csv
```

Kiem tra:

```powershell
python - <<'PY'
import pandas as pd
metrics = pd.read_csv('reports/results/final_evaluation_metrics.csv')
video = pd.read_csv('reports/results/final_video_wise_metrics.csv')
pred = pd.read_csv('reports/results/final_external_predictions.csv')
print(metrics.T)
print(pred['participant_id'].value_counts().sort_index())
print(video[['source_video','participant_id','label','n','accuracy','f1_incorrect','false_positive','false_negative']])
PY
```

Tieu chi dat:

```text
final_external_predictions chi gom P06/P07
final_video_wise_metrics co toi da 23 video
final_participant_wise_metrics cho raw/train van chi gom P01-P05
```

---

## Buoc 10 - Error analysis va xuat frame loi moi

Chay error analysis theo final predictions moi:

```powershell
python src/24_export_error_frames.py
python src/25_temporal_feature_windows.py
python src/26_model_explainability.py
```

Neu van can error analysis ANN cu:

```powershell
python src/20_error_analysis.py
```

File dau ra quan trong:

```text
reports/ERROR_TAXONOMY_REPORT.md
reports/results/error_taxonomy.csv
reports/figures/error_cases/
reports/TEMPORAL_RISK_INDEX_VALIDATION.md
reports/results/temporal_window_features.csv
reports/figures/temporal_smoothing_effect.png
reports/FEATURE_IMPORTANCE_REPORT.md
reports/results/feature_importance.csv
reports/figures/feature_importance_top20.png
```

Kiem tra:

```text
Error frames phai doc duoc video P06/P07 trong dataset/external_videos.
Khong con error report nao noi external la P01 neu dang bao cao protocol moi.
```

---

## Buoc 11 - Cap nhat report tong hop dataset va ket qua

Tao/cap nhat cac file report sau:

```text
reports/DATASET_MANIFEST.md
reports/EXPERIMENT_PROTOCOL_FINAL.md
reports/FINAL_EVALUATION_REPORT.md
reports/MODEL_SELECTION_REPORT.md
reports/BENCHMARK_CLASSIFIERS_SUMMARY.md
reports/FEATURE_SCHEMA_FINAL.md
reports/PROJECT_COMPLETION_AND_GAP_ANALYSIS_2026.md
reports/DUANHIENTAI_version1.md
```

Noi dung can cap nhat:

- Dataset split moi:
  - raw/train: P01-P05, 94 video
  - external unseen-participant: P06-P07, 23 video
- So frame moi sau trich xuat 2 FPS.
- Label distribution moi.
- View angle distribution moi.
- Model tot nhat moi.
- Threshold moi.
- Final external metrics moi.
- Video-wise metrics moi.
- Participant-wise metrics moi.
- Runtime neu co chay lai.
- Ghi ro ket qua cu external P01 khong con la protocol final.

---

## Buoc 12 - Cap nhat paper/luan van sau khi co ket qua moi

Chi cap nhat paper/luan van sau khi Buoc 2-11 da thanh cong.

Can cap nhat cac noi dung:

```text
Dataset:
- raw/development set: P01-P05
- external unseen-participant set: P06-P07

Method:
- khong doi huong, van MediaPipe Pose + feature engineering + lightweight ML

Experiment:
- protocol moi co external unseen participants

Results:
- thay toan bo bang/so lieu final cu bang ket qua moi
```

Can ghi cau giai thich:

```text
The previous P01 external videos were moved into the development set because P01 already appeared in the original raw dataset. The final external set was rebuilt using P06 and P07 to evaluate unseen participants.
```

Tieng Viet:

```text
Các video external P01 trước đây được chuyển vào tập development vì P01 đã xuất hiện trong dữ liệu gốc. Tập external cuối cùng được xây dựng lại từ P06 và P07 nhằm đánh giá mô hình trên người tham gia chưa xuất hiện trong huấn luyện.
```

---

## Checklist ket qua cuoi cung

Sau khi thuc thi xong, phai tra loi duoc cac cau sau:

- [ ] `dataset/metadata/video_manifest.csv` co 117 video hay khong?
- [ ] Raw split co dung 94 video P01-P05 hay khong?
- [ ] External split co dung 23 video P06-P07 hay khong?
- [ ] External co con P01 khong?
- [ ] Raw co bi lan P06/P07 khong?
- [ ] Co con file `font` khong?
- [ ] CSV raw metadata moi co bao nhieu row/cot?
- [ ] CSV external metadata moi co bao nhieu row/cot?
- [ ] Combined feature CSV moi co bao nhieu row/cot?
- [ ] Model nao tot nhat sau benchmark moi?
- [ ] Threshold moi la bao nhieu?
- [ ] Accuracy/Precision/Recall/F1/MCC tren external P06-P07 la bao nhieu?
- [ ] Ket qua theo P06 va P07 rieng ra sao?
- [ ] Video nao loi nhieu nhat?
- [ ] Error cases co anh minh hoa moi khong?
- [ ] Bao cao da ghi ro protocol moi chua?

---

## Bao cao sau khi thuc thi task

Khi hoan thanh, tao file tong hop:

```text
reports/REBUILD_DATASET_P01_TRAIN_P06P07_EXTERNAL_REPORT.md
```

File nay bat buoc gom:

1. Tom tat thay doi split.
2. Bang dataset moi.
3. Bang CSV shape moi.
4. Bang label distribution moi.
5. Bang participant distribution moi.
6. Bang model benchmark moi.
7. Model duoc chon moi va ly do.
8. Threshold moi.
9. Final external metrics moi.
10. Video-wise/person-wise error summary.
11. Cac report/artifact da cap nhat.
12. Cac loi/phat hien bat thuong.
13. Cac buoc tiep theo de dua ket qua vao luan van/bai bao.

---

## Ket luan mong doi

Neu task nay hoan thanh dung, du an se co protocol manh hon:

```text
Train/development: P01-P05
External unseen-participant test: P06-P07
```

Day la cach trinh bay thuyet phuc hon cho luan van va bai bao khoa hoc, vi ket qua external luc nay phan anh kha nang tong quat sang nguoi moi thay vi chi test tren P01 da xuat hien trong du lieu goc.
