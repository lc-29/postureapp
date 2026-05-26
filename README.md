# Posture Detection App

## Gioi thieu

Ung dung desktop phat hien loi tu the lam viec qua webcam, camera IP hoac file video. Pipeline chinh:

`OpenCV -> MediaPipe Pose -> 33 landmarks -> 99 features (x, y, z) -> ANN hoac rule-based baseline -> canh bao realtime -> SQLite logging -> thong ke ngay`.

Day la he thong ho tro nhac nho tu the, khong phai cong cu chan doan y te.

## Cau truc

| Duong dan | Vai tro |
|---|---|
| `src/1_rule_based_baseline.py` | Baseline rule-based chay doc lap qua OpenCV. |
| `src/2_extract_features.py` | Trich xuat 99 landmark features tu video thanh CSV. |
| `src/3_database_setup.py` | Tao SQLite schema va du lieu mac dinh. |
| `src/4_main_desktop_app.py` | GUI CustomTkinter realtime. |
| `src/5_train_ann_local.py` | Train ANN tu CSV landmark. |
| `src/6_evaluate_external.py` | Danh gia model hien tai tren external CSV. |
| `src/10_export_statistics.py` | Export thong ke tu SQLite sang CSV. |
| `dataset/*.csv` | Dataset landmark da trich xuat. |
| `models/ann_best.keras` | ANN model dang duoc app su dung. |
| `models/scaler.pkl` | StandardScaler dung kem model. |
| `reports/` | Tai lieu, ket qua danh gia va checklist. |

## Cai dat

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Neu dung Python moi hon ma TensorFlow khong cai duoc, hay dung Python 3.10 hoac 3.11.

## Chay ung dung

Khoi tao database truoc khi demo:

```powershell
python src/3_database_setup.py
```

Chay GUI:

```powershell
python src/4_main_desktop_app.py
```

App mac dinh dung:

- Model: `models/ann_best.keras`
- Scaler: `models/scaler.pkl`
- Database: `database/posture_app.db`
- Am thanh canh bao: `assets/sounds/alarm.wav`

## Demo bang webcam hoac video

Trong GUI, co the chon nguon dau vao la webcam, camera IP hoac duong dan file video. Khi demo bang video file, nhap duong dan file vao o nguon camera/video trong man hinh cau hinh, sau do bam Start.

Luu y:

- Webcam co the bi khoa neu dang duoc ung dung khac su dung.
- Mot so video HEVC/H.265 khong doc duoc bang OpenCV; neu gap loi, hay convert sang H.264.
- Dataset video raw khong duoc dua len Git vi nhieu file lon hon gioi han 100 MB cua GitHub.

## Train/Danh gia

Train ANN tu CSV hien tai:

```powershell
python src/5_train_ann_local.py --dataset dataset/posture_data_2fps.csv --output-dir models/local_training
```

Smoke test train nhanh:

```powershell
python src/5_train_ann_local.py --epochs 2 --patience 1 --max-rows 400 --output-dir models/tmp_smoke
```

Danh gia external test:

```powershell
python src/6_evaluate_external.py
```

Ket qua duoc luu trong `reports/results/`.

## Luu y tai lap

- Seed mac dinh: `42`.
- Sample FPS mac dinh khi trich xuat: `2.0`.
- CSV chinh gom 99 feature `landmark_0_x` den `landmark_32_z` va cot `label`.
- Neu muon danh gia video-wise/person-wise, can trich xuat CSV moi voi metadata:

```powershell
python src/2_extract_features.py --include-metadata --output dataset/posture_data_2fps_with_metadata.csv
```

## Kiem tra nhanh

```powershell
python -m pytest tests
python -m py_compile src/1_rule_based_baseline.py src/2_extract_features.py src/3_database_setup.py src/4_main_desktop_app.py src/5_train_ann_local.py src/6_evaluate_external.py src/7_video_wise_evaluation.py src/8_compare_algorithms.py src/9_ablation_study.py src/10_export_statistics.py src/posture_baseline.py
```
