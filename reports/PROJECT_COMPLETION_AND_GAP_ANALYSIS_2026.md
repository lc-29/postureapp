# Project Completion And Gap Analysis 2026

Ngay cap nhat: 2026-05-27

## Muc tieu

File nay tong ket cac nhiem vu trong `workflow_kilo/10_TASK_SPRINGER_AUDIT_AND_UPGRADE_BACKLOG.md` da duoc thuc thi, nhung ket qua moi, diem manh hien tai, diem con thieu, va cach khac phuc toi uu.

## Nhung viec da lam duoc

| Nhom | Ket qua |
|---|---|
| Model card | Da tao `reports/MODEL_CARD_ANN_CURRENT.md`. |
| Metadata extraction | Da nang cap `src/2_extract_features.py` de xuat `source_video`, `frame_index`, `timestamp_sec`, `participant_id`, `view_angle`, `camera_type`. |
| External metadata CSV | Da tao `dataset/processed/posture_external_test_2fps_with_metadata.csv` voi 1697 rows, 108 columns. |
| Video-wise evaluation | Da tao `reports/results/video_wise_metrics.csv` va `reports/results/video_wise_summary.md`. |
| Full algorithm benchmark | Da tao `reports/results/algorithm_benchmark_full.csv`. |
| Prediction-level export | Da tao `reports/results/external_predictions.csv`. |
| Error analysis | Da tao `reports/ERROR_ANALYSIS.md`. |
| ROC/PR/calibration | Da tao `reports/results/roc_curve.png`, `pr_curve.png`, `calibration_curve.png`. |
| Feature ablation | Da tao `reports/results/ablation_full.csv`. |
| Temporal smoothing app | Da them smoothing window va smoothing threshold vao `src/4_main_desktop_app.py`. |
| Runtime benchmark | Da tao `src/13_runtime_benchmark.py`, `reports/results/runtime_benchmark.csv`, `reports/RUNTIME_BENCHMARK.md`. |
| Paper figures/tables | Da tao `src/14_generate_paper_artifacts.py`, `reports/figures/`, `reports/tables/`, `reports/PAPER_ARTIFACTS.md`. |
| Related work | Da cap nhat `reports/RELATED_WORK_TODO.md`. |
| Data/ethics | Da tao `reports/DATA_ETHICS_STATEMENT.md`. |
| Springer drafts | Da cap nhat method/results/outline drafts. |

## Ket qua thuc nghiem moi

### External ANN metrics

| Metric | Gia tri |
|---|---:|
| Rows | 1697 |
| Accuracy | 79.316% |
| Precision incorrect | 94.599% |
| Recall incorrect | 65.985% |
| F1 incorrect | 77.743% |
| Macro F1 | 79.213% |
| MCC | 62.933% |
| ROC-AUC | 95.046% |
| PR-AUC | 95.747% |
| Brier score | 18.642% |
| Best F1 threshold | 0.10 |
| Best F1 | 79.903% |

### Full algorithm benchmark

| Model | Accuracy | F1 incorrect | Ghi chu |
|---|---:|---:|---|
| Random Forest | 87.036% | 88.372% | Tot nhat theo accuracy/F1 tren external CSV hien tai. |
| SVM RBF | 79.906% | 78.912% | Gan ANN, recall tot hon ANN. |
| HistGradientBoosting | 77.549% | 78.438% | Tot nhung kem RF/SVM. |
| ANN | 79.316% | 77.743% | ROC-AUC/PR-AUC cao nhat, threshold can tune. |
| Logistic Regression | 77.313% | 74.721% | Baseline tuyen tinh kha tot. |
| KNN | 71.656% | 70.327% | Kem hon. |
| Rule-based | 56.747% | 64.610% | Giai thich duoc, nhung metric thap. |

Ket luan moi: **ANN khong con la model tot nhat theo F1/accuracy tren external set hien tai**. Random Forest dang la ung vien tot hon cho classifier tabular landmark. ANN van co ROC-AUC/PR-AUC cao, nen co the cai thien neu calibration/threshold tot hon.

### Video-wise finding

External metadata CSV co 10 videos. Mean video accuracy la 82.482%, nhung std la 28.763%, cho thay performance khong on dinh theo video.

Failure case nghiem trong:

- `dataset\external_videos\incorrect\P01_incorrect_004.mp4`
- Accuracy: 2.929%
- False negatives: 232/239
- Mean probability incorrect: 0.043

Day la bang chung quan trong: model bo sot mot video sai tu the gan nhu hoan toan. Can uu tien error analysis theo video nay.

### Feature ablation

| Feature group | Accuracy | F1 incorrect |
|---|---:|---:|
| normalized_plus_ergonomic | 93.424% | 94.438% |
| normalized_all_33_landmarks | 91.202% | 92.527% |
| raw_all_33_landmarks | 90.567% | 92.031% |
| normalized_head_shoulders_hips_hands | 86.304% | 88.394% |
| raw_head_shoulders_hips_hands | 86.259% | 88.377% |
| ergonomic_indicators | 83.492% | 85.978% |

Luu y: ablation nay la split noi bo frame-level, chua phai external/video-wise. Tuy vay, ket qua ung ho huong them normalized + ergonomic features.

### Runtime benchmark

| Metric | Gia tri |
|---|---:|
| Processed frames | 110 |
| Pose detection rate | 1.000 |
| Mean total latency | 27.908 ms |
| P95 total latency | 30.026 ms |
| Estimated processing FPS | 35.831 |
| Mean MediaPipe latency | 19.564 ms |
| Mean ANN latency | 6.516 ms |

Ket luan: pipeline MediaPipe + ANN co kha nang realtime tren video test. GUI FPS thuc te co the thap hon do Tkinter, ve overlay, camera buffer, logging va audio.

## Diem moi cua do an hien tai

1. End-to-end webcam posture monitoring: camera/video/IP camera -> MediaPipe -> classifier/rules -> warning -> SQLite -> dashboard.
2. Hybrid model: ANN/RF benchmark cho performance, rule-based ergonomic indicators cho giai thich.
3. Neck-compression/rut co rule: phat hien truong hop mui gan ngang vai do rut co sau.
4. Temporal Posture Risk Index: bien log theo phien thanh risk score 0-100.
5. Statistical workflow: external evaluation, threshold sweep, Wilson CI, McNemar, ROC/PR/calibration.
6. Product workflow: CustomTkinter app co light/dark mode, dashboard, theme toggle, smoothing setting.

## Diem con thieu va cach khac phuc toi uu

### 1. Train metadata CSV chua co

Van de: external CSV da co metadata, nhung train CSV chinh van la frame-only. Chua the train/evaluate video-wise/person-wise that cho full dataset.

Cach khac phuc:

```powershell
python src/2_extract_features.py --input-root dataset/raw_videos --sample-fps 2 --include-metadata --output dataset/processed/posture_data_2fps_with_metadata.csv
```

Sau do cap nhat train/evaluate script de split theo `source_video` va `participant_id`.

### 2. Person-wise validation chua du manh

Van de: filename co participant ID, nhung external videos hien chi la `P01`; train co P01/P03/P04/P05/P06. Chua co protocol giu lai nguoi chua tung xuat hien trong train.

Cach khac phuc toi uu:

- Tao `dataset/metadata/participants.csv`.
- Dam bao moi participant co ca correct/incorrect va nhieu view angles.
- Chay leave-one-participant-out cross-validation.

### 3. ANN khong phai model tot nhat theo benchmark moi

Van de: Random Forest dat F1 external 88.372%, cao hon ANN 77.743%.

Cach khac phuc:

- Dong goi Random Forest thanh model ung vien cho app.
- Them model selector trong app: ANN / Random Forest / Rule-based.
- So sanh RF voi ANN tren video-wise/person-wise truoc khi thay default.
- Neu muon giu ANN, can retrain voi normalized + ergonomic features va threshold calibration.

### 4. Failure case `P01_incorrect_004` rat nghiem trong

Van de: model gan nhu nhan sai toan bo video incorrect nay thanh correct.

Cach khac phuc:

- Trich frame minh hoa false negative tu video nay.
- Kiem tra goc quay, anh sang, pose landmarks, label consistency.
- Them feature ergonomic/normalized.
- Them video nay vao hard-case analysis trong paper.

### 5. Feature schema cho app chua dung normalized + ergonomic

Van de: ablation cho thay normalized + ergonomic tot hon, nhung model app hien van dung raw 99 landmarks.

Cach khac phuc:

- Tao `src/15_feature_schema.py` gom raw/normalized/ergonomic feature functions.
- Re-train RF/ANN tren schema moi.
- Luu `models/feature_schema.json`.
- App load model theo schema thay vi hardcode 99 features.

### 6. GUI screenshots chua tu dong hoa

Van de: `reports/PAPER_ARTIFACTS.md` da co figure/table, nhung GUI screenshot light/dark van can chup manual.

Cach khac phuc:

- Chay app o light/dark mode.
- Chup man hinh dashboard va main app.
- Luu vao `reports/figures/gui_light.png`, `gui_dark.png`.

### 7. Data ethics/consent chua day du

Van de: da co statement, nhung chua co consent/participant metadata thuc.

Cach khac phuc:

- Tao form consent noi bo neu can bao cao nghiem tuc.
- Tao metadata CSV khong nhay cam.
- Neu chia se dataset, uu tien landmark CSV thay vi raw video.

## Huong phat trien toi uu tiep theo

Thu tu nen lam tiep:

1. Re-extract full train metadata CSV.
2. Implement video/person-wise train-test split.
3. Dong goi Random Forest va normalized+ergonomic feature schema.
4. So sanh ANN vs RF vs SVM tren video/person-wise protocol.
5. Trich frame/error examples cho `P01_incorrect_004`.
6. Cap nhat app de chon model RF/ANN va dung feature schema moi.
7. Chup GUI screenshots va hoan thien figures.
8. Viet final Springer-style report voi claim an toan.

## Claim hien tai nen dung

> The project implements a complete webcam-based posture monitoring system with realtime alerts, interpretable ergonomic indicators, session logging, temporal risk scoring, and statistical evaluation. On the current external frame-level set, Random Forest achieved the best F1 among tested tabular models, while the ANN provided high ROC-AUC/PR-AUC but lower recall at the default threshold. Further metadata-rich video/person-wise validation is required before claiming robust generalization.
