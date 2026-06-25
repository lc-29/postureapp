# 15 Task Nang Cap Do Chinh Xac, Thuat Toan, Tinh Moi Cho Luan Van Va Bai Bao

Ngay tao: 2026-05-28

## Trang thai thuc thi 2026-05-28

| Task | Trang thai | Ket qua |
|---|---|---|
| TASK-1501 | Done | Da tao `src/feature_schema.py`, `models/feature_schema_final.json`, `reports/FEATURE_SCHEMA_FINAL.md`, va `tests/test_feature_schema.py`. |
| TASK-1502 | Done | Da tao `src/21_train_model_registry.py`, train 25 to hop model/feature, sinh `models/model_registry.json` va `reports/MODEL_SELECTION_REPORT.md`. Model final: `hist_gradient_boosting__normalized_99`. |
| TASK-1503 | Done | Da tao `src/22_calibrate_threshold.py`, sinh `reports/THRESHOLD_CALIBRATION_REPORT.md`; threshold final balanced F1 la `0.65`. |
| TASK-1504 | Partial | Da tao `src/model_registry_service.py` va test load registry. Chua tich hop truc tiep vao `src/4_main_desktop_app.py` de tranh pha app khi chua QA GUI. |
| TASK-1505 | Blocked | Can quay them external video tu nguoi/camera moi; hien chua co du lieu moi de mo rong external validation. |
| TASK-1506 | Done | Da tao `src/23_final_evaluation_protocol.py`, sinh `reports/FINAL_EVALUATION_REPORT.md` va cac CSV final evaluation. |
| TASK-1507 | Done | Da tao `src/24_export_error_frames.py`, xuat frame loi va sinh `reports/ERROR_TAXONOMY_REPORT.md`. |
| TASK-1508 | Done | Da tao `src/25_temporal_feature_windows.py`, sinh `reports/TEMPORAL_RISK_INDEX_VALIDATION.md`; temporal 5s giam false negatives tu 24 xuong 8. |
| TASK-1509 | Done | Da tao `src/26_model_explainability.py`, sinh `reports/FEATURE_IMPORTANCE_REPORT.md` va `reports/figures/feature_importance_top20.png`. |
| TASK-1510 | Done | Da tao final paper package: `EXPERIMENT_PROTOCOL_FINAL.md`, `FINAL_RESULTS_TABLES.md`, `FINAL_FIGURE_LIST.md`, `SPRINGER_MANUSCRIPT_DRAFT.md`, `THESIS_CHAPTER_OUTLINE.md`, `CLAIM_BOUNDARY_AND_LIMITATIONS.md`. |

## Ket qua nang cap chinh

| Hang muc | Ket qua |
|---|---:|
| Model final | `hist_gradient_boosting__normalized_99` |
| Threshold final | 0.65 |
| Corrected external accuracy | 96.502% |
| Corrected external F1 incorrect | 96.760% |
| Corrected external recall incorrect | 97.303% |
| Corrected external MCC | 92.966% |
| Participant-wise mean F1 incorrect | 90.675% |
| Temporal 5s false negatives | 8, giam tu 24 |

## Muc tieu

Task nay lap ke hoach nang cap du an tu muc **demo/app + benchmark noi bo** len muc **luan van va bai bao khoa hoc co tinh thuyet phuc**.

Trong tam nang cap:

1. Tang do chinh xac va giam bo sot sai tu the.
2. Chot model va feature schema tot nhat, khong chi dung ANN/raw landmarks.
3. Lam ro diem moi: ergonomic features, temporal risk, hard-case analysis, metadata-rich dataset.
4. Tang do tin cay khoa hoc: video-wise, person-wise, external validation, statistical tests.
5. Tao artifact san sang viet paper: bang, hinh, model card, protocol, limitations.

## Trang thai hien tai sau Task 14

### Ket qua external ANN sau khi sua video external

| Metric | Gia tri |
|---|---:|
| External rows | 1658 |
| Accuracy | 90.169% |
| Precision incorrect | 95.609% |
| Recall incorrect | 85.618% |
| F1 incorrect | 90.338% |
| Macro-F1 | 90.166% |
| MCC | 80.901% |
| ROC-AUC | 98.226% |
| PR-AUC | 98.505% |
| Best threshold | 0.10 |
| Best F1 incorrect | 91.889% |

### Benchmark external hien tai

| Rank | Model | Feature set | Accuracy | F1 incorrect |
|---:|---|---|---:|---:|
| 1 | SVM RBF | ergonomic | 94.873% | 95.107% |
| 2 | SVM RBF | combined | 93.486% | 93.684% |
| 3 | HistGradientBoosting | combined | 91.315% | 92.283% |
| 4 | Random Forest | combined | 91.013% | 92.062% |
| 5 | Logistic Regression | ergonomic | 90.893% | 91.662% |
| 6 | ANN | raw | 90.169% | 90.338% |

### Hard cases hien tai

| Video | Van de |
|---|---|
| `P01_incorrect_005.mp4` | Accuracy 67.485%, false negatives 53. |
| `P01_correct_004.mp4` | Accuracy 73.771%, false positives 32. |
| `P01_incorrect_004.mp4` | Accuracy 77.500%, false negatives 45. |

## Ket luan chan doan

Du an da co ket qua tot hon truoc, nhung de thuyet phuc hon cho luan van/bai bao, viec can lam tiep khong phai chi tang giao dien. Can nang cap theo 5 truc:

1. **Data**: external set hien chi co P01, can them nguoi/camera/goc quay de chung minh generalization.
2. **Feature**: ergonomic features dang rat manh, can chot thanh feature schema khoa hoc va dua vao app.
3. **Model**: ANN khong phai model tot nhat; can dong goi SVM/RF/ANN theo model registry.
4. **Evaluation**: can final protocol chong data leakage, CI theo video/person, hard-case taxonomy.
5. **Novelty**: can dinh vi dong gop la hybrid interpretable ergonomic + temporal risk + product pipeline, khong claim model deep learning moi.

---

## TASK-1501: Chot feature schema final co tinh moi

Muc tieu: bien ergonomic features thanh dong gop khoa hoc ro rang, co cong thuc, co code dung chung cho train/evaluate/app.

Can lam:

1. Tao module dung chung:

```text
src/feature_schema.py
```

2. Module phai co cac ham:

```text
get_raw_landmark_columns(df)
compute_normalized_landmarks(df)
compute_ergonomic_features(df)
build_feature_matrix(df, feature_set)
load_feature_schema(path)
save_feature_schema(path)
```

3. Feature sets can ho tro:

| Feature set | Mo ta |
|---|---|
| `raw_99` | 33 landmarks x/y/z. |
| `normalized_99` | Landmarks normalize theo shoulder width/torso length. |
| `ergonomic_14` | Shoulder, torso, head/neck, hand/chin-rest indicators. |
| `combined_raw_ergonomic` | Raw + ergonomic. |
| `combined_normalized_ergonomic` | Normalized + ergonomic. |
| `temporal_window` | Rolling mean/std/ratio theo cua so 3-5 giay. |

4. Luu schema:

```text
models/feature_schema_final.json
```

5. Report:

```text
reports/FEATURE_SCHEMA_FINAL.md
```

Noi dung report:

- Cong thuc tung feature.
- Vi sao feature do lien quan ergonomic.
- Feature nao la moi trong pham vi do an.
- Feature nao khong moi, chi la baseline.

Acceptance criteria:

- Cung mot schema duoc dung cho train, benchmark va app.
- Khong con tinh feature duplicate o nhieu file.
- Co unit test:

```text
tests/test_feature_schema.py
```

## TASK-1502: Train va dong goi model final

Muc tieu: app va paper co model final duoc chon bang bang chung, khong chi dung ANN cu.

Can lam:

1. Tao script:

```text
src/21_train_model_registry.py
```

2. Train cac model tren feature schema final:

| Model | Ly do |
|---|---|
| ANN/MLP | Model app hien tai, can baseline. |
| SVM RBF | Tot nhat tren ergonomic external benchmark hien tai. |
| Random Forest | Robust, co feature importance. |
| HistGradientBoosting | Manh voi tabular features. |
| Logistic Regression | Baseline giai thich tot. |

3. Moi model can luu:

```text
models/registry/<model_id>/model.pkl hoac model.keras
models/registry/<model_id>/scaler.pkl
models/registry/<model_id>/feature_schema.json
models/registry/<model_id>/threshold.json
models/registry/<model_id>/metrics.json
```

4. Tao registry:

```text
models/model_registry.json
```

5. Chon model final theo tieu chi:

Primary metric:

```text
F1 incorrect
```

Secondary metrics:

```text
recall incorrect
MCC
PR-AUC
video-wise stability
runtime latency
```

6. Report:

```text
reports/MODEL_SELECTION_REPORT.md
```

Acceptance criteria:

- Co model final ro rang.
- Co ly do tai sao chon model do.
- Neu SVM ergonomic tot hon ANN, report phai noi ro app hien tai can cap nhat.
- Khong claim tot hon literature, chi claim tot nhat trong protocol noi bo.

## TASK-1503: Calibrate threshold va giam false negatives

Muc tieu: giam bo sot sai tu the, vi app can canh bao dung luc hon la chi accuracy cao.

Can lam:

1. Tao script:

```text
src/22_calibrate_threshold.py
```

2. Thu threshold tu 0.05 den 0.95.

3. Toi uu theo 3 che do:

| Mode | Muc tieu |
|---|---|
| `balanced_f1` | F1 incorrect cao nhat. |
| `safety_recall` | Recall incorrect >= 90%, precision cao nhat co the. |
| `quiet_precision` | Precision incorrect >= 95%, recall cao nhat co the. |

4. Output:

```text
reports/results/threshold_calibration_final.csv
reports/THRESHOLD_CALIBRATION_REPORT.md
models/registry/<model_id>/threshold.json
```

5. Cap nhat app de co preset:

```text
Nhan bang
Canh bao nhay
Canh bao chat
```

Acceptance criteria:

- Co threshold final cho model app.
- Report noi ro tradeoff precision/recall.
- False negatives cua hard cases duoc so sanh truoc/sau threshold.

## TASK-1504: Tich hop model final vao app desktop

Muc tieu: app dung duoc model tot nhat, khong chi benchmark tren report.

Can lam:

1. Cap nhat:

```text
src/4_main_desktop_app.py
```

2. Them model loader dung registry:

```text
models/model_registry.json
```

3. Them UI chon model:

```text
ANN raw
SVM ergonomic
Random Forest combined
Rule-based only
Hybrid final
```

4. Them inference pipeline:

```text
MediaPipe landmarks -> feature_schema -> scaler -> model -> probability/label
```

5. Hybrid final nen co logic:

```text
model_probability + ergonomic_rule_flags + temporal_smoothing
```

6. Cap nhat dashboard luu:

```text
model_id
feature_set
threshold
probability
rule_flags
```

Acceptance criteria:

- App chay duoc voi model final.
- App van chay duoc voi ANN cu neu can.
- SQLite log biet phien nao dung model nao.
- Co smoke test import/init app.

## TASK-1505: Mo rong external validation de thuyet phuc hon

Muc tieu: diem yeu lon nhat hien tai la external set chi co P01. Can them nguoi moi de paper thuyet phuc.

Can lam neu con thoi gian quay video:

1. Quay them external videos tu it nhat 3 nguoi moi:

```text
P02_external
P03_external
P04_external
```

2. Moi nguoi nen co:

| Loai | So video toi thieu |
|---|---:|
| correct | 3 |
| incorrect | 3 |

3. Nen co nhieu dieu kien:

| Metadata | Gia tri goi y |
|---|---|
| view_angle | front, side_30, side_90 |
| lighting | bright, normal, low |
| camera_distance | near, medium, far |
| device | laptop_webcam, phone_camera, external_webcam |

4. Tao metadata:

```text
dataset/metadata/participants.csv
dataset/metadata/recording_conditions.csv
```

5. Cap nhat manifest va trich xuat lai external CSV.

Acceptance criteria:

- External set co it nhat 4 participants.
- Co bang ket qua theo participant external.
- Paper co the noi "participant-independent external evaluation" neu train khong dung cac nguoi external.

Neu khong kip quay them:

- Phai ghi ro trong limitations: external set chi P01, chi la preliminary external video evaluation.

## TASK-1506: Chay final evaluation protocol chong data leakage

Muc tieu: ket qua paper phai khong bi phan bien la chia frame lam ro ri du lieu.

Can lam:

1. Tao script:

```text
src/23_final_evaluation_protocol.py
```

2. Protocol bat buoc:

| Protocol | Muc dich |
|---|---|
| External frame-level | So sanh voi ket qua hien tai. |
| External video-wise | Xem video nao loi. |
| Leave-one-participant-out | Danh gia generalization sang nguoi moi trong raw dataset. |
| Leave-one-video-out | Danh gia generalization sang video moi. |
| View-angle subgroup | Xem front/side_30/side_90 anh huong the nao. |

3. Metrics:

```text
accuracy
precision_incorrect
recall_incorrect
f1_incorrect
macro_f1
mcc
roc_auc
pr_auc
brier_score
latency_ms
```

4. CI/statistics:

```text
Wilson CI cho accuracy
Bootstrap CI cho F1 incorrect
McNemar pairwise ANN vs final model
Paired bootstrap theo video neu co the
```

5. Output:

```text
reports/results/final_evaluation_metrics.csv
reports/results/final_video_wise_metrics.csv
reports/results/final_participant_wise_metrics.csv
reports/FINAL_EVALUATION_REPORT.md
```

Acceptance criteria:

- Co mot bang final duy nhat de dua vao paper.
- Khong con nhieu bang mau thuan nhau.
- Report noi ro protocol nao la primary.

## TASK-1507: Hard-case mining va error taxonomy

Muc tieu: bien loi cua model thanh insight khoa hoc, tang tinh thuyet phuc cua Discussion.

Can lam:

1. Tao script:

```text
src/24_export_error_frames.py
```

2. Export frame loi tu:

```text
P01_incorrect_005.mp4
P01_correct_004.mp4
P01_incorrect_004.mp4
```

3. Output:

```text
reports/figures/error_cases/false_negative/
reports/figures/error_cases/false_positive/
reports/results/error_taxonomy.csv
reports/ERROR_TAXONOMY_REPORT.md
```

4. Taxonomy goi y:

| Error category | Mo ta |
|---|---|
| ambiguous_posture | Tu the trung gian, nguoi xem cung kho gan nhan. |
| camera_angle | Goc quay lam landmark kho phan biet. |
| partial_occlusion | Tay/ghe/ban che landmark. |
| lighting_or_blur | Anh sang/motion blur anh huong MediaPipe. |
| label_boundary | Ranh gioi correct/incorrect chua ro. |
| unseen_posture_type | Kieu sai tu the it co trong train. |

Acceptance criteria:

- Co hinh minh hoa loi trong report.
- Co bang dem loi theo category.
- Co de xuat cach sua tung category.

## TASK-1508: Nang cap novelty bang temporal features va TPRI validation

Muc tieu: diem moi manh hon khong nam o frame classifier, ma o session-level risk.

Can lam:

1. Tao temporal feature extractor:

```text
src/25_temporal_feature_windows.py
```

2. Them features theo cua so 3s, 5s, 10s:

```text
bad_posture_ratio
mean_prob_incorrect
std_prob_incorrect
max_consecutive_bad_seconds
transition_count
rule_flag_ratio
missing_pose_ratio
```

3. So sanh:

| Model | Input |
|---|---|
| Frame-level final model | Single frame. |
| Temporal feature model | Window features. |
| Temporal smoothing only | EMA/majority vote. |

4. TPRI validation:

```text
reports/results/tpri_validation.csv
reports/TEMPORAL_RISK_INDEX_VALIDATION.md
```

5. Tao figure:

```text
reports/figures/tpri_session_timeline.png
reports/figures/temporal_smoothing_effect.png
```

Acceptance criteria:

- Chung minh temporal smoothing/window giam nhap nhay va false alerts.
- TPRI co cong thuc final, co vi du session.
- Claim an toan: "session-level risk summarization", khong claim medical risk.

## TASK-1509: Them explainability cho model final

Muc tieu: neu dung SVM/RF/ergonomic, can giai thich feature nao quan trong.

Can lam:

1. Tao script:

```text
src/26_model_explainability.py
```

2. Phuong phap:

| Model | Explainability |
|---|---|
| Logistic Regression | Coefficients. |
| Random Forest | Feature importance. |
| SVM/ANN | Permutation importance. |
| Rule-based | Rule flags and thresholds. |

3. Output:

```text
reports/results/feature_importance.csv
reports/FEATURE_IMPORTANCE_REPORT.md
reports/figures/feature_importance_top20.png
```

Acceptance criteria:

- Co top 20 features quan trong.
- Giai thich duoc vi sao ergonomic features co ich.
- Neu neck/hand features khong quan trong, phai noi trung thuc.

## TASK-1510: Tao final paper package

Muc tieu: gom tat ca ket qua thanh bo artifact viet luan van/bai bao.

Can lam:

1. Tao/cap nhat:

```text
reports/EXPERIMENT_PROTOCOL_FINAL.md
reports/FINAL_RESULTS_TABLES.md
reports/FINAL_FIGURE_LIST.md
reports/SPRINGER_MANUSCRIPT_DRAFT.md
reports/THESIS_CHAPTER_OUTLINE.md
reports/CLAIM_BOUNDARY_AND_LIMITATIONS.md
```

2. Bang final can co:

| Bang | Noi dung |
|---|---|
| Table 1 | Dataset statistics. |
| Table 2 | Feature groups. |
| Table 3 | Model comparison. |
| Table 4 | Ablation study. |
| Table 5 | Video-wise/person-wise results. |
| Table 6 | Runtime benchmark. |
| Table 7 | Literature contextual comparison. |

3. Hinh final can co:

| Hinh | Noi dung |
|---|---|
| Figure 1 | System pipeline. |
| Figure 2 | App screenshot light/dark. |
| Figure 3 | Confusion matrix. |
| Figure 4 | ROC/PR curve. |
| Figure 5 | Threshold sweep. |
| Figure 6 | Feature importance. |
| Figure 7 | TPRI/session timeline. |
| Figure 8 | Error case examples. |

Acceptance criteria:

- Co du material de viet luan van chuong thuc nghiem.
- Co du material de viet paper applied research.
- Tat ca claim trong paper khop voi CSV/report moi.

---

## Thu tu thuc thi de dat hieu qua cao nhat

Lam theo thu tu:

1. TASK-1501: Chot feature schema final.
2. TASK-1502: Train va dong goi model registry.
3. TASK-1503: Calibrate threshold.
4. TASK-1506: Chay final evaluation protocol.
5. TASK-1507: Hard-case mining va error taxonomy.
6. TASK-1509: Explainability/feature importance.
7. TASK-1504: Tich hop model final vao app.
8. TASK-1508: Temporal features va TPRI validation.
9. TASK-1505: Mo rong external validation neu co them video.
10. TASK-1510: Final paper package.

Neu thoi gian rat gap, uu tien 5 task:

1. TASK-1501
2. TASK-1502
3. TASK-1503
4. TASK-1506
5. TASK-1510

## Ket qua mong doi sau khi hoan thanh

Sau task nay, du an se manh hon o cac diem:

1. **Do chinh xac**: dung model/feature set tot nhat thay vi ANN raw mac dinh.
2. **Tinh khoa hoc**: co final protocol ro, tranh data leakage.
3. **Tinh moi**: co interpretable ergonomic feature schema, temporal risk/session analysis.
4. **Tinh thuyet phuc**: co hard-case figures, feature importance, statistical test, CI.
5. **Tinh san pham**: app dung model final, luu model_id/threshold/feature_set trong log.

## Claim khoa hoc nen huong toi

Claim an toan va manh:

> This study presents a real-time webcam-based working posture monitoring system that combines MediaPipe pose landmarks, interpretable ergonomic geometric features, calibrated machine-learning classifiers, and session-level temporal posture risk scoring. The proposed ergonomic feature schema improved internal external-set performance over raw landmarks, while video-wise and participant-wise analyses were used to assess generalization and failure cases.

Khong nen claim:

```text
State-of-the-art posture recognition.
New deep learning architecture.
Medical diagnosis.
New public benchmark dataset.
Clinically validated ergonomic assessment.
```
