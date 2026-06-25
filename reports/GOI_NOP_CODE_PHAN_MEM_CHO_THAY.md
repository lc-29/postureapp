# Goi nop code phan mem cho thay huong dan

**Muc dich:** Huong dan nen nen nhung gi khi nop phan code/phan mem cua du an phat hien loi tu the lam viec qua webcam.  
**Ngay tao:** 01/06/2026  
**Khuyen nghi ten file nen:** `POSTURE_DETECTION_CODE_DEMO_DUONG_LY_CU.zip`

---

## 1. Ket luan ngan gon

Neu thay yeu cau **nop code phan mem**, nen nen mot goi source code gon, co the chay lai duoc tren may khac. Khong nen nen toan bo thu muc project vi se rat nang, co nhieu file tam, moi truong ao, build trung gian va video raw.

Nen nop:

- Source code app.
- Model can thiet de app chay.
- File cau hinh/chay app.
- Database demo neu muon thay xem thong ke.
- Dataset da xu ly dang CSV/metadata neu thay muon kiem tra train/evaluation.
- Huong dan chay.

Khong nen nop qua email:

- `.venv`
- `.git`
- `build`
- `dist`
- `release`
- `__pycache__`
- video raw/external neu qua nang
- file PDF/Word bao cao neu ban da nen rieng

---

## 2. Goi code nen nen de gui thay

Nen tao file zip gom cac thanh phan sau:

| Thanh phan | Nen dua vao? | Ly do |
|---|---:|---|
| `src/` | Co | Source code chinh cua app, train/evaluate, feature schema |
| `assets/` | Co | Am thanh canh bao, icon neu co |
| `models/ann_best.keras` | Co | Model ANN dang dung trong app |
| `models/scaler.pkl` | Co | Scaler bat buoc de ANN du doan dung |
| `models/feature_schema_final.json` | Co | Mo ta schema dac trung |
| `models/model_registry.json` | Co | Registry chon model tot nhat |
| `models/registry/hist_gradient_boosting__normalized_99/` | Co | Model tot nhat da them vao app demo |
| `database/posture_app.db` | Nen co | Cho thay xem lich su/demo thong ke SQLite |
| `dataset/metadata/video_manifest.csv` | Co | Manifest video va metadata |
| `dataset/processed/*.csv` | Nen co neu dung luong cho phep | Du lieu da xu ly de train/evaluate, nhe hon video raw |
| `tests/` | Co | Chung minh co test/kiem tra logic |
| `README.md` | Co | Mo ta tong quan cach chay |
| `requirements.txt` | Co | Danh sach thu vien Python |
| `requirements-build.txt` | Co neu co | Phuc vu dong goi app neu can |
| `run_app.bat` | Co | Tien cho thay chay nhanh tren Windows |
| `build_scripts/` | Tuy chon | Chi can neu thay muon xem cach build exe |

---

## 3. Thu muc/file khong nen nen vao goi code

| Thanh phan | Ly do khong nen dua vao |
|---|---|
| `.venv/` | Moi truong ao rat nang, may thay co the cai lai bang `requirements.txt` |
| `.git/` | Lich su git nang va khong can thiet khi nop zip |
| `.pytest_cache/` | Cache test, khong co gia tri nop |
| `__pycache__/` | File cache Python |
| `build/` | Build trung gian, nang, co the tao lai |
| `dist/` | Ban exe da build, neu thay chi yeu cau code thi khong can |
| `release/` | Ban release co the rat nang, chi gui rieng neu thay yeu cau demo exe |
| `reports/` | Ban da co bao cao rieng, nen nen bao cao thanh goi rieng |
| `dataset/raw_videos/` | Video raw rat nang, khong nen gui email |
| `dataset/external_videos/` | Video external cung nen gui Drive neu can |
| file `*.zip`, `*.docx`, `*.pdf` bao cao | Tranh lap voi goi bao cao rieng |

---

## 4. Goi video/dataset nen xu ly rieng

Thu muc `dataset` cua project hien rat nang vi co video. Kiem tra nhanh hien tai cho thay:

| Thanh phan | Dung luong uoc tinh |
|---|---:|
| `src/` | khoang 1 MB |
| `models/` | khoang 40 MB |
| `dataset/` | khoang 34.8 GB |
| `release/` | khoang 5.4 GB |

Vi vay, neu gui email thi **khong nen dinh kem raw videos**. Cach dung hon:

1. Goi email nop code zip nhe.
2. Neu thay can xem video/dataset goc, upload `dataset/raw_videos/` va `dataset/external_videos/` len Google Drive/OneDrive.
3. Trong email ghi ro: video goc qua nang nen em gui bang link Drive rieng.

---

## 5. Cau truc zip de xuat

Nen co cau truc nhu sau:

```text
POSTURE_DETECTION_CODE_DEMO_DUONG_LY_CU/
├── README.md
├── requirements.txt
├── requirements-build.txt
├── run_app.bat
├── src/
├── assets/
├── models/
│   ├── ann_best.keras
│   ├── scaler.pkl
│   ├── feature_schema_final.json
│   ├── model_registry.json
│   └── registry/
│       └── hist_gradient_boosting__normalized_99/
│           ├── model.pkl
│           ├── feature_schema.json
│           ├── metrics.json
│           └── threshold.json
├── database/
│   └── posture_app.db
├── dataset/
│   ├── metadata/
│   │   └── video_manifest.csv
│   └── processed/
│       ├── posture_data_2fps_with_metadata.csv
│       ├── posture_data_2fps_combined_features.csv
│       ├── posture_external_test_2fps_with_metadata.csv
│       └── posture_external_test_2fps_combined_features.csv
├── tests/
└── build_scripts/       # tuy chon
```

---

## 6. Cach chay ghi trong email/README cho thay

Neu thay muon chay tu source:

```powershell
cd POSTURE_DETECTION_CODE_DEMO_DUONG_LY_CU
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python src/4_main_desktop_app.py
```

Neu thay da co Python va moi truong ao:

```powershell
cd POSTURE_DETECTION_CODE_DEMO_DUONG_LY_CU
.\.venv\Scripts\python.exe src\4_main_desktop_app.py
```

Trong app co cac mode:

```text
ANN
HistGradientBoosting (best)
Rule-based Baseline
```

---

## 7. Noi dung email goi y

```text
Kinh gui thay,

Em gui thay phan code phan mem cua de tai "Xay dung ung dung phat hien loi tu the lam viec qua webcam su dung Computer Vision".

Trong file zip co source code Python, model da train, scaler, model tot nhat HistGradientBoosting, database demo, dataset da xu ly dang CSV, file requirements va huong dan chay app.

Do video goc cua dataset co dung luong lon, em khong dinh kem truc tiep trong email. Neu thay can xem video goc, em se gui them link Google Drive rieng.

Tran trong,
Duong Ly Cu
```

---

## 8. Neu thoi gian gap, nen gui toi thieu nhung gi?

Neu can nop gap trong toi nay, goi toi thieu nen co:

```text
src/
assets/
models/ann_best.keras
models/scaler.pkl
models/model_registry.json
models/registry/hist_gradient_boosting__normalized_99/
database/posture_app.db
README.md
requirements.txt
run_app.bat
```

Day la goi toi thieu de thay xem duoc code va chay demo app.

---

## 9. Goi tot nhat nen nop

Goi tot nhat nen nop la:

1. `POSTURE_DETECTION_CODE_DEMO_DUONG_LY_CU.zip`
   - chua source code, model, scaler, database demo, processed CSV, tests, README.

2. `BAO_CAO_NGHIEN_CUU_DUONG_LY_CU.zip`
   - chua PDF/Word bao cao, hinh anh, file Springer/Word neu can.

3. Link Drive rieng neu thay can:
   - `dataset/raw_videos/`
   - `dataset/external_videos/`

Lam nhu vay se gon, dung trong tam, va khong lam email bi qua dung luong.

