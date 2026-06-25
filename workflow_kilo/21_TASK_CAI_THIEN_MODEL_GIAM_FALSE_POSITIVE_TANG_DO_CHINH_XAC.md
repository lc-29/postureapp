# 21_TASK_CAI_THIEN_MODEL_GIAM_FALSE_POSITIVE_TANG_DO_CHINH_XAC

## Muc tieu

Cai thien chi so thuc nghiem sau khi rebuild dataset voi tap train/development P01-P05 va tap external moi P06-P07. Trong lan danh gia gan nhat, model tot nhat la `random_forest__ergonomic_14` voi external Accuracy 82.16%, F1 Incorrect 85.25%, Recall Incorrect 91.94%, Precision Incorrect 79.47%, FP=607 va FN=206. Van de chinh la false positive cao, dac biet o cac video Correct goc `side_90` va `side_30`.

Task nay yeu cau cai thien mo hinh theo cach hop le ve hoc thuat, khong dua external P06/P07 vao train neu van dung P06/P07 de bao cao ket qua unseen-participant external test.

## Nguyen tac bat buoc

- Khong sua so lieu bang tay de lam dep ket qua.
- Khong dua toan bo P06/P07 vao train roi van bao cao P06/P07 la external unseen test.
- Khong claim state-of-the-art.
- Khong xoa artifact cu; neu can ghi de artifact chuan thi phai backup truoc.
- Moi cai tien phai co bang so sanh truoc/sau.
- Uu tien giam FP tren video Correct nhung khong lam FN tang qua cao.
- Ket qua cu phai duoc giu lam baseline: `random_forest__ergonomic_14`, threshold 0.50, Accuracy 82.16%, F1 Incorrect 85.25%, FP=607, FN=206.

## Dau vao hien tai

- Raw/train videos: `dataset/raw_videos`
- External videos: `dataset/external_videos`
- Manifest: `dataset/metadata/video_manifest.csv`
- Train metadata CSV: `dataset/processed/posture_data_2fps_with_metadata.csv`
- External metadata CSV: `dataset/processed/posture_external_test_2fps_with_metadata.csv`
- Ergonomic train CSV: `dataset/processed/posture_data_2fps_ergonomic_features.csv`
- Ergonomic external CSV: `dataset/processed/posture_external_test_2fps_ergonomic_features.csv`
- Combined train CSV: `dataset/processed/posture_data_2fps_combined_features.csv`
- Combined external CSV: `dataset/processed/posture_external_test_2fps_combined_features.csv`
- Final predictions: `reports/results/final_external_predictions.csv`
- Video-wise metrics: `reports/results/final_video_wise_metrics.csv`
- Final evaluation report: `reports/FINAL_EVALUATION_REPORT.md`

## Dau ra bat buoc

- `reports/MODEL_IMPROVEMENT_FP_REDUCTION_REPORT.md`
- `reports/results/model_improvement_experiments.csv`
- `reports/results/model_improvement_video_wise.csv`
- `reports/results/model_improvement_participant_wise.csv`
- `reports/results/model_improvement_threshold_sweep.csv`
- `reports/results/model_improvement_error_cases.csv`
- `reports/figures/model_improvement_confusion_matrix.png`
- `reports/figures/model_improvement_threshold_sweep.png`
- Neu co tao model moi:
  - `models/registry/<new_model_id>/model.pkl`
  - `models/registry/<new_model_id>/scaler.pkl` neu model can scaler
  - `models/registry/<new_model_id>/threshold.json`
  - cap nhat `models/model_registry.json` nhung phai giu model cu trong registry.

## Buoc 1. Backup artifact truoc khi thu nghiem

1. Tao thu muc backup:
   - `outputs/backups/model_improvement_fp_reduction_<YYYYMMDD_HHMMSS>/`
2. Copy cac file sau vao backup:
   - `models/model_registry.json`
   - `reports/FINAL_EVALUATION_REPORT.md`
   - `reports/MODEL_SELECTION_REPORT.md`
   - `reports/results/final_evaluation_metrics.csv`
   - `reports/results/final_external_predictions.csv`
   - `reports/results/final_video_wise_metrics.csv`
   - `reports/results/final_participant_wise_metrics.csv`

## Buoc 2. Phan tich loi hien tai theo video, nguoi va goc quay

1. Doc `reports/results/final_external_predictions.csv` va `reports/results/final_video_wise_metrics.csv`.
2. Tao bang loi theo:
   - `participant_id`
   - `view_angle`
   - `source_video`
   - ground-truth label
   - TP, TN, FP, FN
   - accuracy
   - F1 Incorrect neu tinh duoc
3. Luu vao:
   - `reports/results/model_improvement_error_cases.csv`
4. Trong report, bat buoc neu ro cac video co FP cao nhat, toi thieu:
   - `dataset\external_videos\correct\P06_correct_side_90_002.mp4`
   - `dataset\external_videos\correct\P06_correct_side_90_001.mp4`
   - `dataset\external_videos\correct\P07_correct_side_90_003.mp4`
   - `dataset\external_videos\correct\P06_correct_side_30_001.mp4`
5. Ket luan tam thoi:
   - Loi chu yeu la model nhan nham Correct thanh Incorrect o goc nghieng.
   - Can uu tien feature va mo hinh view-aware.

## Buoc 3. Kiem tra chat luong nhan va video bi loi cao

1. Xuat 10-20 frame dai dien cho moi video co FP/FN cao vao:
   - `reports/figures/model_improvement_error_frames/`
2. Moi frame can co overlay:
   - skeleton neu co
   - true label
   - predicted label
   - probability neu co
   - source video
   - timestamp
3. Tao bang nhan xet thu cong trong report:
   - video co dung nhan khong?
   - video co doan transition/chua ngoi on dinh khong?
   - co bi che mat, thieu landmark, goc quay qua kho, anh sang yeu khong?
4. Neu phat hien label/video sai ro rang:
   - khong sua ngay am tham.
   - ghi vao `reports/MODEL_IMPROVEMENT_FP_REDUCTION_REPORT.md` muc "Data quality issues".
   - de xuat cach sua rieng: trim video, tach clip, doi label, hoac loai frame transition.

## Buoc 4. Bo sung feature theo goc nhin va do tin cay landmark

Kiem tra file tao feature hien tai, uu tien `src/16_build_ergonomic_features.py`. Bo sung feature moi neu chua co:

### 4.1 Feature cho dau-co-vai

- `ear_shoulder_y_ratio_left`
- `ear_shoulder_y_ratio_right`
- `ear_shoulder_y_ratio_mean`
- `nose_ear_dx_ratio`
- `nose_shoulder_dx_ratio`
- `head_forward_ratio`
- `neck_to_shoulder_angle_left`
- `neck_to_shoulder_angle_right`
- `head_neck_torso_angle`

### 4.2 Feature cho than tren

- `shoulder_hip_dx_ratio`
- `shoulder_hip_dy_ratio`
- `torso_side_lean_ratio`
- `hip_shoulder_torso_angle`

### 4.3 Feature ve visibility / missing landmarks

Neu CSV co visibility hoac co the lay tu pipeline MediaPipe:

- `mean_upper_body_visibility`
- `min_upper_body_visibility`
- `low_visibility_count`

Neu CSV hien tai khong co visibility:

- Ghi ro trong report la chua co visibility.
- Khong bịa cot visibility.
- De xuat cap nhat extractor o task rieng neu can.

### 4.4 Feature view-aware

Them `view_angle` one-hot cho cac experiment co metadata:

- `view_front`
- `view_side_30`
- `view_side_90`
- `view_unknown`

Tao cac feature set moi:

- `ergonomic_v2`
- `ergonomic_v2_with_view`
- `combined_v2`
- `combined_v2_with_view`

Luu file moi:

- `dataset/processed/posture_data_2fps_ergonomic_v2_features.csv`
- `dataset/processed/posture_external_test_2fps_ergonomic_v2_features.csv`
- `dataset/processed/posture_data_2fps_combined_v2_features.csv`
- `dataset/processed/posture_external_test_2fps_combined_v2_features.csv`

## Buoc 5. Thu nghiem model moi theo huong view-aware

Chay benchmark voi cac feature set:

- `ergonomic_14`
- `ergonomic_v2`
- `ergonomic_v2_with_view`
- `normalized_99`
- `combined_v2`
- `combined_v2_with_view`

Model can thu:

- Logistic Regression
- SVM RBF
- Random Forest
- Extra Trees neu scikit-learn co san
- HistGradientBoosting
- MLP sklearn
- ANN/Keras neu script hien tai ho tro

Yeu cau:

- Train tren P01-P05.
- Test external tren P06-P07.
- Khong train tren external P06/P07.
- Luu ket qua vao:
  - `reports/results/model_improvement_experiments.csv`

Metric bat buoc:

- Accuracy
- Precision Incorrect
- Recall Incorrect
- F1 Incorrect
- Macro F1
- MCC
- ROC-AUC neu co probability
- PR-AUC neu co probability
- FP
- FN

## Buoc 6. Thu nghiem chien luoc class weight va threshold

Voi 3 model/feature set tot nhat o Buoc 5:

1. Thu `class_weight=None`.
2. Thu `class_weight=balanced` neu model ho tro.
3. Sweep threshold tu 0.30 den 0.80 voi step 0.01.
4. Chon threshold theo 2 muc tieu:
   - `best_f1_incorrect`
   - `best_balanced_fp_fn`: uu tien F1 cao nhung FP khong qua cao va FN khong tang manh.

Luu:

- `reports/results/model_improvement_threshold_sweep.csv`
- `reports/figures/model_improvement_threshold_sweep.png`

Trong report phai giai thich:

- threshold nao tang Precision Incorrect
- threshold nao giam FP
- threshold nao lam FN tang
- threshold nao phu hop app canh bao realtime

## Buoc 7. Thu nghiem temporal/video-level decision

Dung `reports/results/final_external_predictions.csv` hoac predictions moi de tao danh gia:

1. Frame-level.
2. Smoothed frame-level:
   - window = 3, 5, 7, 10 frame.
3. Video-level majority vote.
4. Video-level mean probability threshold.
5. Warning-level metric:
   - video Incorrect duoc xem la phat hien dung neu co canh bao on dinh sau N giay.

Luu:

- `reports/results/model_improvement_temporal_evaluation.csv`

Yeu cau giai thich:

- Ket qua frame-level co the thap hon vi tung frame nhieu nhieu.
- Trong app thuc te, smoothing va warning cooldown moi la hanh vi nguoi dung nhin thay.
- Khong thay the frame-level metric, chi bo sung goc nhin thuc te.

## Buoc 8. Chon model cai thien va cap nhat registry

Chi chon model moi neu thoa mot trong cac dieu kien:

- F1 Incorrect cao hon baseline it nhat 2 diem phan tram va MCC khong giam.
- Hoac Precision Incorrect tang ro va FP giam ro trong khi Recall Incorrect van >= 85%.
- Hoac video-level metric tot hon ro, co giai thich hop ly cho app canh bao.

Neu model moi tot hon:

1. Luu model vao `models/registry/<new_model_id>/`.
2. Luu threshold vao `threshold.json`.
3. Cap nhat `models/model_registry.json`.
4. Ghi ro model moi co duoc tich hop vao app chua.

Neu model moi chua tot hon:

1. Khong doi selected model.
2. Van giu bao cao experiment.
3. Ghi ro ly do va de xuat buoc tiep theo: bo sung video Correct side_90/side_30 vao train, them participant, hoac trim/clean external.

## Buoc 9. Tao final report sau cai thien

Tao file:

- `reports/MODEL_IMPROVEMENT_FP_REDUCTION_REPORT.md`

Report bat buoc co cac muc:

1. Muc tieu cai thien.
2. Baseline truoc cai thien.
3. Phan tich loi FP/FN theo video, nguoi, goc quay.
4. Data quality review.
5. Feature moi da them.
6. Benchmark model/feature set.
7. Threshold calibration.
8. Temporal/video-level evaluation.
9. Model duoc chon sau cai thien.
10. So sanh truoc/sau.
11. Ket luan co nen cap nhat bai bao/bao cao khong.
12. Viec tiep theo de tang ket qua hop le.

Bang so sanh truoc/sau bat buoc:

| Version | Model | Feature set | Threshold | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC | FP | FN |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline after rebuild | random_forest | ergonomic_14 | 0.50 | 82.16% | 79.47% | 91.94% | 85.25% | 0.6405 | 607 | 206 |
| Improved candidate | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

## Buoc 10. Kiem tra cuoi

Chay checklist va ghi vao report:

- [ ] External test chi gom P06/P07.
- [ ] Train/development chi gom P01-P05.
- [ ] Khong co leakage external vao train.
- [ ] Co so sanh baseline truoc/sau.
- [ ] Co video-wise va participant-wise evaluation.
- [ ] Co threshold sweep.
- [ ] Co confusion matrix moi.
- [ ] Co error cases voi frame minh hoa.
- [ ] Co giai thich neu ket qua van thap.
- [ ] Co de xuat bo sung du lieu hop le de tang chi so.

## Huong cai thien du lieu neu model van thap

Neu sau khi thu feature/model moi ma chi so van thap, khong nen ep model qua muc. Khi do can cai thien du lieu:

1. Quay them video Correct cho P01-P05 o goc `side_90` va `side_30`.
2. Quay them Correct va Incorrect cho P06/P07 nhung chi dua vao train neu co them P08/P09 lam external moi.
3. Tach clip transition ra khoi video chinh.
4. Giu moi clip chi chua mot nhan ro rang.
5. Can bang so frame Correct/Incorrect theo tung goc quay.
6. Them metadata ve khoang cach camera, chieu cao camera, anh sang, loai ghe/ban neu co.

## Ket qua mong doi

Ket qua ly tuong nhung khong bat buoc:

- Accuracy external tang tu 82.16% len khoang 85-90% neu du lieu phu hop.
- F1 Incorrect tang tu 85.25% len khoang 88-92%.
- FP giam ro tren cac video Correct side_90/side_30.
- Recall Incorrect van giu >= 85%.

Neu khong dat duoc muc tren, ket qua van co gia tri nghien cuu neu report chi ra duoc nguyen nhan: domain shift theo participant, goc quay, label ambiguity, hoac thieu feature side-view.
