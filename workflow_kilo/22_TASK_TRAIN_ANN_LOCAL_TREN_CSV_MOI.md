# 22_TASK_TRAIN_ANN_LOCAL_TREN_CSV_MOI

## Muc tieu

Train lai model ANN/Keras tren may local bang CSV moi sau khi rebuild dataset:

- Train/development: 94 video, P01-P05.
- External unseen test: 23 video, P06-P07.
- Khong dung Kaggle.
- Khong dua P06/P07 vao train neu van dung P06/P07 de bao cao external test.
- So sanh ANN moi voi ANN cu va model tot nhat hien tai `hist_gradient_boosting__ergonomic_v2_with_view`.

Ket qua mong muon la co model ANN local moi, co scaler moi, co evaluation report ro rang. Chi cap nhat app dung ANN moi neu ANN moi tot hon ANN cu va khong qua kem model HGB moi.

## Boi canh hien tai

CSV moi da co:

- `dataset/processed/posture_data_2fps_with_metadata.csv`
  - 12680 rows x 108 columns
  - P01-P05
  - Correct: 5206, Incorrect: 7474
- `dataset/processed/posture_external_test_2fps_with_metadata.csv`
  - 4556 rows x 108 columns
  - P06-P07
  - Correct: 2001, Incorrect: 2555
- `dataset/processed/posture_data_2fps_ergonomic_v2_features.csv`
- `dataset/processed/posture_external_test_2fps_ergonomic_v2_features.csv`
- `dataset/processed/posture_data_2fps_combined_v2_features.csv`
- `dataset/processed/posture_external_test_2fps_combined_v2_features.csv`

ANN cu trong app:

- `models/ann_best.keras`
- `models/scaler.pkl`
- File nay la model cu, chua train lai tren dataset moi P01-P05/P06-P07.

Model tot nhat hien tai:

- `models/registry/hist_gradient_boosting__ergonomic_v2_with_view/model.pkl`
- threshold: `0.76`
- external Accuracy: 89.31%
- F1 Incorrect: 90.13%
- Precision Incorrect: 93.48%
- Recall Incorrect: 87.01%
- FP: 155
- FN: 332

## Nguyen tac bat buoc

- Khong train tren external P06/P07.
- Khong ghi de `models/ann_best.keras` va `models/scaler.pkl` truoc khi backup.
- Khong tuyen bo ANN moi tot hon neu chua co evaluation tren external P06/P07.
- Khong chi dua vao validation split frame-level noi bo de ket luan.
- Phai bao cao ro neu ANN moi kem HGB moi.
- Neu ANN moi khong tot, giu HGB moi lam model chinh va ANN chi lam model doi chieu.

## Dau ra bat buoc

Model/artifact:

- `models/local_training_rebuild/ann_raw_99.keras`
- `models/local_training_rebuild/scaler_raw_99.pkl`
- `models/local_training_rebuild/ann_normalized_99.keras`
- `models/local_training_rebuild/scaler_normalized_99.pkl`
- `models/local_training_rebuild/ann_ergonomic_v2_with_view.keras`
- `models/local_training_rebuild/scaler_ergonomic_v2_with_view.pkl`
- `models/local_training_rebuild/ann_training_summary.json`

Ket qua:

- `reports/results/ann_local_rebuild_metrics.csv`
- `reports/results/ann_local_rebuild_predictions.csv`
- `reports/results/ann_local_rebuild_video_wise.csv`
- `reports/results/ann_local_rebuild_participant_wise.csv`
- `reports/results/ann_local_rebuild_threshold_sweep.csv`

Hinh:

- `reports/figures/ann_local_rebuild_confusion_matrix.png`
- `reports/figures/ann_local_rebuild_training_curves.png`
- `reports/figures/ann_local_rebuild_threshold_sweep.png`

Bao cao:

- `reports/ANN_LOCAL_REBUILD_REPORT.md`

Script neu can tao moi:

- `src/28_train_ann_local_rebuild.py`

## Buoc 1. Kiem tra moi truong local

Chay trong VS Code terminal tai thu muc project:

```powershell
.venv\Scripts\python.exe -c "import tensorflow as tf; print(tf.__version__)"
```

Neu TensorFlow chua co, cai trong `.venv`:

```powershell
.venv\Scripts\python.exe -m pip install tensorflow
```

Neu may khong co GPU thi van train duoc bang CPU vi dataset hien tai khong lon.

## Buoc 2. Backup ANN cu

Tao thu muc:

- `outputs/backups/ann_before_local_rebuild_<YYYYMMDD_HHMMSS>/`

Copy cac file neu ton tai:

- `models/ann_best.keras`
- `models/scaler.pkl`
- `models/local_training/ann_best.keras`
- `models/local_training/scaler.pkl`
- `models/local_training/metrics.txt`
- `models/local_training/classification_report.txt`
- `models/local_training/confusion_matrix.csv`

## Buoc 3. Kiem tra script train ANN cu

Doc file:

- `src/5_train_ann_local.py`

Xac dinh:

- Dang doc CSV nao.
- Dang train feature raw 99 hay feature khac.
- Dang split train/validation nhu the nao.
- Co evaluate external P06/P07 khong.
- Co luu scaler/model dung duong dan khong.

Neu script cu chi train raw 99 va khong evaluate external, tao script moi:

- `src/28_train_ann_local_rebuild.py`

Khong sua manh script cu neu khong can.

## Buoc 4. Tao feature matrix cho 3 cau hinh ANN

Can train it nhat 3 ANN:

### 4.1 ANN raw_99

Input:

- 99 cot `landmark_0_x ... landmark_32_z`

Train:

- `dataset/processed/posture_data_2fps_with_metadata.csv`

External:

- `dataset/processed/posture_external_test_2fps_with_metadata.csv`

### 4.2 ANN normalized_99

Input:

- 99 cot normalized landmark, tinh bang `src/feature_schema.py`.

Train:

- tu `posture_data_2fps_with_metadata.csv`

External:

- tu `posture_external_test_2fps_with_metadata.csv`

### 4.3 ANN ergonomic_v2_with_view

Input:

- 14 ergonomic cu
- 13 ergonomic v2
- 4 one-hot view angle
- tong 31 feature

Train:

- `dataset/processed/posture_data_2fps_combined_v2_features.csv`

External:

- `dataset/processed/posture_external_test_2fps_combined_v2_features.csv`

Luu y:

- `view_angle` external co front/side_30/side_90.
- Voi webcam realtime, neu chua co view selector thi view co the la `unknown`; can ghi limitation vao report.

## Buoc 5. Kien truc ANN de train

Dung kien truc gan voi project hien tai:

```text
Input
Dense 128, ReLU
BatchNorm
Dropout 0.30
Dense 64, ReLU
BatchNorm
Dropout 0.25
Dense 32, ReLU
Dropout 0.20
Dense 1, sigmoid
```

Training config de xuat:

- loss: binary_crossentropy
- optimizer: Adam learning_rate=0.001
- metrics: accuracy, precision, recall
- batch_size: 32 hoac 64
- epochs: toi da 100
- EarlyStopping monitor `val_loss`, patience 10, restore_best_weights=True
- ReduceLROnPlateau monitor `val_loss`, patience 5
- class_weight: can thu ca `None` va `balanced`
- random seed: 42

## Buoc 6. Split validation noi bo dung cach

Khong split random theo frame mot cach duy nhat.

Toi thieu phai co:

1. Internal validation split theo frame de theo doi training.
2. External evaluation tren P06/P07 la ket qua quan trong nhat.

Neu co thoi gian, them participant-wise validation tren P01-P05:

- hold-out P01
- hold-out P02
- hold-out P03
- hold-out P04
- hold-out P05

## Buoc 7. Train va luu model

Train tung cau hinh:

- `ann_raw_99`
- `ann_normalized_99`
- `ann_ergonomic_v2_with_view`

Moi cau hinh can luu:

- model `.keras`
- scaler `.pkl`
- training history
- validation metrics
- external predictions
- threshold sweep

Khong ghi de `models/ann_best.keras` trong buoc nay.

## Buoc 8. Threshold calibration cho ANN

Voi moi ANN, sweep threshold tu 0.30 den 0.80, step 0.01 tren external P06/P07.

Tinh:

- Accuracy
- Precision Incorrect
- Recall Incorrect
- F1 Incorrect
- Macro F1
- MCC
- FP
- FN

Chon threshold theo:

- F1 Incorrect cao nhat
- neu F1 tuong duong, uu tien MCC cao hon
- neu dung cho app canh bao, can giai thich trade-off FP/FN

Luu:

- `reports/results/ann_local_rebuild_threshold_sweep.csv`

## Buoc 9. So sanh ANN moi voi baseline va HGB moi

Bang so sanh bat buoc:

| Model | Feature set | Threshold | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC | FP | FN |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ANN old app | raw_99 | app threshold | ... | ... | ... | ... | ... | ... | ... |
| ANN raw_99 rebuild | raw_99 | ... | ... | ... | ... | ... | ... | ... | ... |
| ANN normalized_99 rebuild | normalized_99 | ... | ... | ... | ... | ... | ... | ... | ... |
| ANN ergonomic_v2_with_view rebuild | ergonomic_v2_with_view | ... | ... | ... | ... | ... | ... | ... | ... |
| HGB current best | ergonomic_v2_with_view | 0.76 | 89.31% | 93.48% | 87.01% | 90.13% | 0.7875 | 155 | 332 |

Neu ANN moi kem HGB:

- khong sao.
- ghi ro HGB la model chinh nen dung cho demo.
- ANN moi co the dung lam baseline neural network.

Neu ANN moi tot hon hoac gan bang HGB:

- de xuat cap nhat app ANN mode sang model moi.

## Buoc 10. Video-wise va participant-wise evaluation

Voi ANN tot nhat, tao:

- `reports/results/ann_local_rebuild_video_wise.csv`
- `reports/results/ann_local_rebuild_participant_wise.csv`

Phai chi ra:

- Video nao con loi nhieu.
- P06 hay P07 kho hon.
- Loi chinh la FP hay FN.
- Video `P07_incorrect_side_90_001.mp4` co duoc cai thien khong.

## Buoc 11. Tao report tieng Viet

Tao file:

- `reports/ANN_LOCAL_REBUILD_REPORT.md`

Bao cao gom:

1. Muc tieu train ANN local.
2. Dataset dung de train/test.
3. Cau hinh ANN.
4. Feature set da thu.
5. Ket qua training noi bo.
6. Ket qua external P06/P07.
7. Threshold calibration.
8. So sanh ANN cu, ANN moi va HGB moi.
9. Phan tich video `P07_incorrect_side_90_001.mp4`.
10. Ket luan co nen cap nhat app ANN hay khong.
11. Huong tiep theo.

## Buoc 12. Dieu kien de cap nhat app ANN

Chi cap nhat app ANN neu:

- ANN moi F1 Incorrect external >= ANN cu it nhat 3 diem phan tram.
- MCC tang ro.
- Ket qua tren P07_incorrect_side_90_001.mp4 khong con sai hang loat.
- App co the tinh dung feature set cua ANN moi realtime.

Neu du dieu kien, lam tiep:

1. Backup:
   - `models/ann_best.keras`
   - `models/scaler.pkl`
2. Copy model tot nhat thanh:
   - `models/ann_best.keras`
   - `models/scaler.pkl`
3. Cap nhat app neu feature set khong phai raw_99.

Neu ANN tot nhat la `ergonomic_v2_with_view`, khong duoc copy thang vao app cu neu app ANN mode van chi tao raw_99. Luc do can cap nhat pipeline app ANN truoc.

## Buoc 13. Lenh chay du kien

Sau khi tao script:

```powershell
.venv\Scripts\python.exe src\28_train_ann_local_rebuild.py
```

Sau khi train xong, chay test nhanh:

```powershell
.venv\Scripts\python.exe -m pytest tests\test_feature_schema.py tests\test_model_registry_service.py
```

Neu co them test cho ANN, chay them:

```powershell
.venv\Scripts\python.exe -m pytest tests
```

## Checklist hoan thanh

- [ ] Da backup ANN cu.
- [ ] Da train ANN raw_99.
- [ ] Da train ANN normalized_99.
- [ ] Da train ANN ergonomic_v2_with_view.
- [ ] Da evaluate external P06/P07.
- [ ] Da sweep threshold.
- [ ] Da tao confusion matrix.
- [ ] Da tao video-wise evaluation.
- [ ] Da tao participant-wise evaluation.
- [ ] Da so sanh voi HGB moi.
- [ ] Da ket luan co nen cap nhat app ANN khong.
- [ ] Khong co leakage P06/P07 vao train.

