# Experiment Protocol

## 1. Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Database

```powershell
python src/3_database_setup.py
```

Output mong doi: `database/posture_app.db` ton tai, co cac bang `NguoiDung`, `CaiDat`, `PhienLamViec`, `NhatKyTuThe`, `ThongKeNgay`, `ThongTinModel`.

## 3. Feature extraction

CSV frame-wise 99 features:

```powershell
python src/2_extract_features.py --input-root dataset/raw_videos --sample-fps 2.0 --output dataset/posture_data_2fps.csv
```

CSV co metadata cho video-wise evaluation:

```powershell
python src/2_extract_features.py --include-metadata --input-root dataset/raw_videos --sample-fps 2.0 --output dataset/posture_data_2fps_with_metadata.csv
```

Thong so mac dinh:

- Seed train/evaluation: `42`.
- Sample FPS: `2.0`.
- Label: `0=correct`, `1=incorrect`.

## 4. Train ANN

```powershell
python src/5_train_ann_local.py --dataset dataset/posture_data_2fps.csv --output-dir models/local_training
```

Smoke test nhanh:

```powershell
python src/5_train_ann_local.py --epochs 2 --patience 1 --max-rows 400 --output-dir models/tmp_smoke
```

Output mong doi:

- `ann_best.keras`
- `scaler.pkl`
- `metrics.txt`
- `classification_report.txt`
- `confusion_matrix.csv`
- `training_curves.png`

## 5. External evaluation

```powershell
python src/6_evaluate_external.py
```

Output mong doi trong `reports/results/`:

- `external_metrics.txt`
- `external_confusion_matrix.csv`
- `external_threshold_sweep.csv`

## 6. Video-wise readiness check

```powershell
python src/7_video_wise_evaluation.py --dataset dataset/posture_data_2fps.csv
```

Neu CSV chua co metadata, script se tao protocol ghi ro can trich xuat lai voi `--include-metadata`.

## 7. Run GUI

```powershell
python src/4_main_desktop_app.py
```

Kiem tra ca ANN mode va baseline mode voi webcam hoac video file.

## Ghi chu nghien cuu

Ket qua local frame-wise rat cao nen can bao cao trung thuc ve nguy co leakage. Ket qua video-wise/person-wise nen duoc them truoc khi nop nghien cuu chinh thuc.
