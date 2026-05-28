# 13 Task Chuan Hoa Dataset Metadata Benchmark Ablation

Ngay tao: 2026-05-28

## Trang thai thuc thi 2026-05-28

| Task | Trang thai | Ket qua |
|---|---|---|
| TASK-1300 | Done | Da tao script dry-run/apply rename, da doi `P03-P06` thanh `P02-P05`, report tai `reports/dataset_rename_plan.csv`. |
| TASK-1301 | Done | Da tao `dataset/metadata/video_manifest.csv` va `reports/DATASET_VIDEO_MANIFEST_SUMMARY.md`. |
| TASK-1302 | Done | Da trich xuat lai raw/external CSV co metadata trong `dataset/processed/`. |
| TASK-1303 | Done | Da tao ergonomic va combined feature CSV, report `reports/ERGONOMIC_FEATURES_DESCRIPTION.md`, test `tests/test_ergonomic_features.py`. |
| TASK-1304 | Done | Da chay video-wise evaluation, output trong `reports/results/video_wise_summary.md`. |
| TASK-1305 | Done | Da chay leave-one-participant-out cho raw va combined, output trong `reports/results/participant_wise_*`. |
| TASK-1306 | Done | Da benchmark classifiers external cho raw/ergonomic/combined, output `reports/BENCHMARK_CLASSIFIERS_SUMMARY.md`. |
| TASK-1307 | Done | Da chay ablation feature set, output `reports/FEATURE_ABLATION_SUMMARY.md`. |
| TASK-1308 | Done | Da tao prediction-level error analysis, output `reports/ERROR_ANALYSIS_BY_VIDEO_PERSON_VIEW.md`. |
| TASK-1309 | Done | Da benchmark runtime tren front/side_30/side_90, output `reports/RUNTIME_BENCHMARK.md`. |
| TASK-1310 | Done | Da cap nhat `src/14_generate_paper_artifacts.py` va sinh lai `reports/figures`, `reports/tables`. |
| TASK-1311 | Done | Da cap nhat dataset manifest va tong quan de dung 5 participant. |
| TASK-1312 | Done | Da tao `reports/RESEARCH_SUBMISSION_READINESS_CHECKLIST.md`. |

Muc tieu: hoan thien phan du lieu va thuc nghiem de du an co the viet bai nghien cuu khoa hoc theo huong **mo hinh co san, nhung du lieu + dac trung + quy trinh danh gia ro rang**.

Tinh trang hien tai:

- Dataset raw hien co 84 video:
  - `dataset/raw_videos/correct`: 34 video
  - `dataset/raw_videos/incorrect`: 50 video
- External videos hien co 10 video:
  - `dataset/external_videos/correct`: 5 video
  - `dataset/external_videos/incorrect`: 5 video
- Hien tai chi con **5 nguoi tham gia** vi da xoa nguoi thu hai.
- Ten file local hien dang co cac ma:
  - `P01`
  - `P03`
  - `P04`
  - `P05`
  - `P06`
- Can doi lai thanh 5 nguoi lien tuc:
  - `P01`
  - `P02`
  - `P03`
  - `P04`
  - `P05`

Quy uoc doi ten:

| Ma hien tai | Ma moi |
|---|---|
| `P01` | `P01` |
| `P03` | `P02` |
| `P04` | `P03` |
| `P05` | `P04` |
| `P06` | `P05` |

Khong doi y nghia label:

| Folder | Label |
|---|---:|
| `correct` | `0` |
| `incorrect` | `1` |

## Nguyen tac quan trong

1. Khong sua truc tiep CSV cu de "gia lap" metadata.
2. Phai doi ten video/tao manifest truoc, sau do trich xuat lai CSV co metadata.
3. Khong chia train/test random theo frame de viet paper, vi de gay ro ri du lieu.
4. Bat buoc co `source_video`, `frame_index`, `participant_id`, `view_angle` trong CSV moi.
5. Video raw khong can push GitHub, nhung metadata va CSV landmark nen co the tai lap.
6. Moi buoc phai sinh report trong `reports/` hoac `reports/results/`.

---

## TASK-1300: Backup va lap ke hoach doi ten video

Muc tieu: doi ten ma participant sau khi xoa P02, nhung phai co dry-run va backup truoc.

Can lam:

1. Tao script:

```text
build_scripts/rename_participants_after_p02_removed.ps1
```

2. Script phai co che do dry-run mac dinh.

3. Script quet cac file video trong:

```text
dataset/raw_videos/correct
dataset/raw_videos/incorrect
dataset/external_videos/correct
dataset/external_videos/incorrect
```

4. Script tao report truoc khi doi ten:

```text
reports/dataset_rename_plan.csv
```

Cot report:

```text
old_path,new_path,old_participant_id,new_participant_id,label,view_angle,status
```

5. Script phai check:

- Khong co file dich bi trung.
- Khong con `P02` cu gay conflict.
- Chi rename file co pattern `Pxx_`.
- Neu file nao khong match pattern thi ghi vao report status `skip_unmatched`.

6. Khi chay that moi dung co:

```powershell
powershell -ExecutionPolicy Bypass -File build_scripts/rename_participants_after_p02_removed.ps1 -Apply
```

Acceptance criteria:

- Co report dry-run.
- Khong mat video.
- Sau khi apply, raw video chi con participant `P01` den `P05`.
- Tong so video van la 84 raw va 10 external.

Lenh kiem tra:

```powershell
Get-ChildItem dataset/raw_videos -Recurse -File -Include *.mp4 |
  Select-Object Name |
  Sort-Object Name
```

---

## TASK-1301: Tao video manifest chuan cho toan bo video

Muc tieu: co file metadata chuan de chung minh dataset co 5 nguoi, nhieu goc quay, nhieu label.

Can lam:

1. Tao script:

```text
src/15_build_video_manifest.py
```

2. Script doc video tu:

```text
dataset/raw_videos
dataset/external_videos
```

3. Sinh file:

```text
dataset/metadata/video_manifest.csv
reports/DATASET_VIDEO_MANIFEST_SUMMARY.md
```

4. Cac cot bat buoc trong `video_manifest.csv`:

```text
dataset_split
source_video
file_name
label
label_name
participant_id
view_angle
camera_type
duration_sec
fps
width
height
total_frames
file_size_mb
sha256
notes
```

5. Cach suy luan:

- Folder `raw_videos` -> `dataset_split=raw`
- Folder `external_videos` -> `dataset_split=external`
- Folder `correct` -> `label=0`, `label_name=correct`
- Folder `incorrect` -> `label=1`, `label_name=incorrect`
- Ten file co `front` -> `view_angle=front`
- Ten file co `side_30` -> `view_angle=side_30`
- Ten file co `side_90` -> `view_angle=side_90`
- Khong suy luan duoc -> de `unknown`

Acceptance criteria:

- Manifest co 94 video neu tinh ca raw + external.
- Raw co 84 video.
- External co 10 video.
- Participant raw gom dung `P01` den `P05`.
- Summary report co bang:
  - So video theo label.
  - So video theo participant.
  - So video theo view angle.
  - Tong duration.
  - Tong dung luong.

Lenh chay:

```powershell
python src/15_build_video_manifest.py
```

---

## TASK-1302: Trich xuat lai CSV raw co metadata

Muc tieu: thay the CSV train frame-only bang CSV co metadata de danh gia video-wise/person-wise.

Can lam:

1. Chay lai trich xuat cho raw dataset:

```powershell
python src/2_extract_features.py --input-root dataset/raw_videos --sample-fps 2 --include-metadata --output dataset/processed/posture_data_2fps_with_metadata.csv
```

2. Chay lai trich xuat cho external dataset:

```powershell
python src/2_extract_features.py --input-root dataset/external_videos --sample-fps 2 --include-metadata --output dataset/processed/posture_external_test_2fps_with_metadata.csv
```

3. Cap nhat:

```text
reports/DATASET_MANIFEST.md
```

Thong tin can cap nhat:

- So video raw dung/sai.
- So video external dung/sai.
- So participant.
- So view angle.
- So row cua CSV moi.
- So cot cua CSV moi.
- Label distribution.

Acceptance criteria:

- CSV moi co cac cot:

```text
source_video
frame_index
timestamp_sec
sample_fps
video_fps
participant_id
view_angle
camera_type
label
```

- `participant_id` khong rong voi raw dataset.
- `source_video` khong rong.
- Co the group by `source_video`, `participant_id`, `view_angle`.

Lenh kiem tra nhanh:

```powershell
python - <<'PY'
import pandas as pd
df = pd.read_csv('dataset/processed/posture_data_2fps_with_metadata.csv')
print(df.shape)
print(df['participant_id'].value_counts())
print(df['view_angle'].value_counts())
print(df['label'].value_counts())
print(df['source_video'].nunique())
PY
```

---

## TASK-1303: Tao bo dac trung ergonomic/geometric

Muc tieu: bien raw landmark thanh bo dac trung co y nghia tu the, dap ung huong "dac trung moi/ro rang".

Can lam:

1. Tao script:

```text
src/16_build_ergonomic_features.py
```

2. Input mac dinh:

```text
dataset/processed/posture_data_2fps_with_metadata.csv
dataset/processed/posture_external_test_2fps_with_metadata.csv
```

3. Output:

```text
dataset/processed/posture_data_2fps_ergonomic_features.csv
dataset/processed/posture_external_test_2fps_ergonomic_features.csv
dataset/processed/posture_data_2fps_combined_features.csv
dataset/processed/posture_external_test_2fps_combined_features.csv
reports/ERGONOMIC_FEATURES_DESCRIPTION.md
```

4. Dac trung ergonomic can co:

```text
shoulder_y_diff
shoulder_tilt_angle
torso_lean_angle
head_offset_x
nose_to_shoulder_y
nose_shoulder_clearance_ratio
neck_compression_detected
left_hand_mouth_ratio
right_hand_mouth_ratio
chin_rest_detected
visibility_mean
shoulder_width
torso_length
head_shoulder_distance
```

5. Neu khong co visibility trong CSV 99 feature, ghi ro:

```text
visibility_mean = not_available
```

hoac bo cot visibility khoi feature set, nhung phai noi ro trong report.

6. Tao 3 feature set:

| Feature set | Mo ta |
|---|---|
| `raw` | 99 landmark x/y/z |
| `ergonomic` | Cac dac trung hinh hoc/giai thich |
| `combined` | Raw + ergonomic |

Acceptance criteria:

- Khong lam mat metadata.
- Khong lam mat label.
- Co report giai thich cong thuc tung dac trung.
- Co unit test cho ham tinh feature voi landmark gia lap.

---

## TASK-1304: Video-wise evaluation

Muc tieu: danh gia theo tung video de tranh chi bao cao frame-level.

Can lam:

1. Cap nhat hoac mo rong:

```text
src/7_video_wise_evaluation.py
```

2. Input:

```text
dataset/processed/posture_data_2fps_with_metadata.csv
dataset/processed/posture_external_test_2fps_with_metadata.csv
```

3. Output:

```text
reports/results/video_wise_metrics.csv
reports/results/video_wise_source_summary.csv
reports/results/video_wise_summary.md
```

4. Chi so can bao cao theo moi video:

```text
source_video
participant_id
view_angle
label
rows
accuracy
precision_incorrect
recall_incorrect
f1_incorrect
false_positive
false_negative
mean_prob_incorrect
```

5. Summary can co:

- Mean video accuracy.
- Std video accuracy.
- Mean F1 incorrect.
- Worst 5 videos.
- Best 5 videos.
- Ket qua theo `view_angle`.

Acceptance criteria:

- Report khong con status "not runnable".
- Co bang worst videos de phuc vu error analysis.

Lenh chay:

```powershell
python src/7_video_wise_evaluation.py --dataset dataset/processed/posture_external_test_2fps_with_metadata.csv
```

---

## TASK-1305: Participant-wise evaluation

Muc tieu: danh gia kha nang tong quat sang nguoi moi.

Can lam:

1. Tao script:

```text
src/17_participant_wise_evaluation.py
```

2. Input:

```text
dataset/processed/posture_data_2fps_with_metadata.csv
```

3. Protocol:

```text
Leave-One-Participant-Out
```

Voi 5 nguoi:

- Lan 1: test P01, train P02-P05.
- Lan 2: test P02, train P01,P03-P05.
- Lan 3: test P03, train nguoi con lai.
- Lan 4: test P04, train nguoi con lai.
- Lan 5: test P05, train nguoi con lai.

4. Chay cac mo hinh:

```text
Logistic Regression
KNN
SVM RBF
Random Forest
HistGradientBoosting
ANN/MLP neu can
```

5. Output:

```text
reports/results/participant_wise_metrics.csv
reports/results/participant_wise_summary.md
```

6. Chi so:

```text
held_out_participant
algorithm
accuracy
precision_incorrect
recall_incorrect
f1_incorrect
macro_f1
mcc
roc_auc
pr_auc
train_rows
test_rows
```

Acceptance criteria:

- Co ket qua cho ca 5 participant.
- Co trung binh va do lech chuan theo participant.
- Neu ket qua giam manh so voi frame-level, phai ghi ro do la danh gia nghiem ngat hon.

---

## TASK-1306: Benchmark nhieu mo hinh tren cung split

Muc tieu: so sanh mo hinh co san mot cach cong bang.

Can lam:

1. Cap nhat:

```text
src/8_compare_algorithms.py
```

hoac tao moi:

```text
src/18_benchmark_classifiers.py
```

2. Mo hinh can benchmark:

```text
Rule-based baseline
Logistic Regression
KNN
SVM RBF
Random Forest
HistGradientBoosting
ANN hien tai
```

3. Feature set can benchmark:

```text
raw
ergonomic
combined
```

4. Split can benchmark:

```text
external test
video-wise
participant-wise
```

5. Output:

```text
reports/results/classifier_benchmark_external.csv
reports/results/classifier_benchmark_video_wise.csv
reports/results/classifier_benchmark_participant_wise.csv
reports/BENCHMARK_CLASSIFIERS_SUMMARY.md
```

Chi so bat buoc:

```text
accuracy
precision
recall
f1
macro_f1
mcc
roc_auc
pr_auc
train_seconds
predict_seconds
```

Acceptance criteria:

- Tat ca mo hinh dung cung input/split.
- Co bang xep hang theo F1 incorrect va PR-AUC.
- Khong claim "tot nhat literature", chi claim "tot nhat trong thuc nghiem noi bo".

---

## TASK-1307: Ablation study cho dac trung

Muc tieu: chung minh dac trung ergonomic co giup ich hay khong.

Can lam:

1. Tao script:

```text
src/19_ablation_feature_sets.py
```

2. So sanh:

| Feature set | Mo ta |
|---|---|
| `raw` | 99 MediaPipe landmarks |
| `ergonomic` | Dac trung hinh hoc |
| `combined` | Raw + ergonomic |
| `combined_without_neck` | Bo nhom rut co |
| `combined_without_hand` | Bo nhom tay gan mieng/chong cam |

3. Output:

```text
reports/results/feature_ablation.csv
reports/FEATURE_ABLATION_SUMMARY.md
```

4. Can co nhan xet:

- Dac trung nao cai thien recall sai tu the?
- Dac trung nao giup view side/front?
- Dac trung nao khong co ich?
- Feature combined co tot hon raw khong?

Acceptance criteria:

- Co bang ket qua ro rang.
- Co phan ket luan trung thuc neu ergonomic features khong cai thien metric.

---

## TASK-1308: Error analysis theo video/nguoi/goc quay

Muc tieu: giai thich khi nao mo hinh sai.

Can lam:

1. Tao script:

```text
src/20_error_analysis.py
```

2. Input:

```text
dataset/processed/posture_external_test_2fps_with_metadata.csv
reports/results/predictions_external.csv
```

3. Output:

```text
reports/results/error_cases.csv
reports/ERROR_ANALYSIS_BY_VIDEO_PERSON_VIEW.md
```

4. Gom nhom loi:

- False positive: tu the dung nhung model bao sai.
- False negative: tu the sai nhung model bao dung.
- Loi theo participant.
- Loi theo view angle.
- Loi theo source video.

5. Neu co the, export frame anh loi:

```text
reports/figures/error_cases/
```

Acceptance criteria:

- Co top video co false negative cao.
- Co top video co false positive cao.
- Co nhan xet nguyen nhan kha nang:
  - goc quay
  - anh sang
  - nguoi ra khoi khung
  - landmark MediaPipe khong on dinh
  - tu the trung gian

---

## TASK-1309: Runtime benchmark cho ung dung realtime

Muc tieu: chung minh app co kha nang chay realtime.

Can lam:

1. Cap nhat hoac tao:

```text
src/13_runtime_benchmark.py
```

2. Do:

```text
mean_fps
p50_latency_ms
p95_latency_ms
model_load_seconds
mediapipe_time_ms
ann_predict_time_ms
cpu_percent
ram_mb
```

3. Test tren:

- Webcam neu co.
- 3 video mau:
  - front
  - side_30
  - side_90

4. Output:

```text
reports/results/runtime_benchmark.csv
reports/RUNTIME_BENCHMARK.md
```

Acceptance criteria:

- Bao cao cau hinh may test.
- Co FPS trung binh.
- Co latency trung binh/p95.
- Co ket luan app co realtime duoc hay khong.

---

## TASK-1310: Cap nhat paper artifacts

Muc tieu: tao bang/hinh san sang dua vao bao cao/bai bao.

Can lam:

1. Cap nhat hoac tao:

```text
src/14_generate_paper_artifacts.py
```

2. Sinh:

```text
reports/tables/dataset_summary.md
reports/tables/model_comparison.md
reports/tables/video_wise_summary.md
reports/tables/participant_wise_summary.md
reports/tables/feature_ablation.md
reports/figures/confusion_matrix.png
reports/figures/roc_curve.png
reports/figures/pr_curve.png
reports/figures/tpri_distribution.png
reports/figures/system_pipeline_mermaid.md
```

Acceptance criteria:

- Moi bang/hinh co nguon du lieu ro.
- Khong co so lieu hard-code sai voi CSV moi.
- Co the dua truc tiep vao paper/report.

---

## TASK-1311: Cap nhat narrative paper theo huong dung

Muc tieu: dinh vi bai bao dung va khong thoi phong.

Can cap nhat cac file:

```text
reports/springer_method_draft.md
reports/springer_results_draft.md
reports/springer_paper_outline.md
reports/NOVELTY_AND_CONTRIBUTION_ANALYSIS_SPRINGER.md
reports/TONGQUANDUAN.md
```

Noi dung can sua:

1. So participant = 5.
2. Dataset raw = 84 video.
3. Correct = 34, incorrect = 50.
4. Goc quay: front, side_30, side_90.
5. Co metadata source_video/frame_index/participant_id.
6. Neu da co participant-wise result thi dua vao.
7. Dong gop nen viet:

```text
metadata-rich project-specific webcam dataset
interpretable ergonomic geometric features
video-wise and participant-wise evaluation
desktop realtime posture monitoring application
Temporal Posture Risk Index
```

8. Khong viet:

```text
state-of-the-art
new deep learning architecture
new benchmark dataset
medical diagnosis
```

Acceptance criteria:

- Tat ca report khong con noi 6 nguoi.
- Claim khoa hoc nhat quan voi ket qua thuc nghiem.
- Co phan limitations ro rang.

---

## TASK-1312: Checklist truoc khi nop/demo nghien cuu

Muc tieu: co checklist de biet du an da san sang viet bai hay chua.

Tao file:

```text
reports/RESEARCH_SUBMISSION_READINESS_CHECKLIST.md
```

Checklist:

| Hang muc | Trang thai | Ghi chu |
|---|---|---|
| Video renamed P01-P05 |  |  |
| `video_manifest.csv` created |  |  |
| Raw metadata CSV extracted |  |  |
| External metadata CSV extracted |  |  |
| Ergonomic features generated |  |  |
| Video-wise evaluation done |  |  |
| Participant-wise evaluation done |  |  |
| Benchmark classifiers done |  |  |
| Ablation study done |  |  |
| Error analysis done |  |  |
| Runtime benchmark done |  |  |
| Paper tables generated |  |  |
| Paper figures generated |  |  |
| Dataset statement written |  |  |
| Limitations written |  |  |

---

## Thu tu thuc thi de nhanh nhat

Lam theo dung thu tu:

1. TASK-1300: Backup/dry-run/apply doi ten video.
2. TASK-1301: Tao video manifest.
3. TASK-1302: Trich xuat lai CSV co metadata.
4. TASK-1303: Tao ergonomic/combined features.
5. TASK-1304: Video-wise evaluation.
6. TASK-1305: Participant-wise evaluation.
7. TASK-1306: Benchmark classifiers.
8. TASK-1307: Ablation study.
9. TASK-1308: Error analysis.
10. TASK-1309: Runtime benchmark.
11. TASK-1310: Tao paper artifacts.
12. TASK-1311: Cap nhat narrative paper.
13. TASK-1312: Checklist san sang nop/demo.

## Ket qua mong doi sau khi hoan thanh

Sau khi xong task nay, du an se co:

- Dataset metadata ro rang voi 5 participant.
- CSV co `source_video`, `frame_index`, `participant_id`, `view_angle`.
- Dac trung ergonomic giai thich duoc.
- Danh gia theo video.
- Danh gia theo nguoi.
- Benchmark nhieu mo hinh co san.
- Ablation de chung minh vai tro cua dac trung.
- Error analysis.
- Runtime benchmark.
- Bang/hinh san sang dua vao bai bao.

Day la nen tang tot de viet bai theo huong:

> A metadata-rich webcam-based working posture monitoring system using MediaPipe landmarks, interpretable ergonomic features, machine-learning classifiers, and session-level temporal risk analysis.
