# 11 Task Deploy Desktop Tkinter Product

Ngay tao: 2026-05-27

## Muc tieu

Dong goi `src/4_main_desktop_app.py` thanh mot ung dung desktop Windows co the chay nhu demo san pham:

- Nguoi dung mo file `.exe`.
- App co GUI CustomTkinter.
- App load duoc model `models/ann_best.keras`.
- App load duoc scaler `models/scaler.pkl`.
- App phat duoc am thanh `assets/sounds/alarm.wav`.
- App tao/doc/ghi duoc SQLite database.
- App mo duoc webcam, camera IP, va video file.
- App co package de copy sang may khac hoac tao installer.

## Execution status 2026-05-27

| Task | Trang thai | Output |
|---|---|---|
| TASK-200 | DONE | Runtime scope da chot: app/model/scaler/sound/runtime DB, khong dong goi dataset/reports/notebooks/tests. |
| TASK-201 | DONE | `src/runtime_paths.py`, app/config/statistics da dung runtime paths. |
| TASK-202 | DONE | `ensure_runtime_database()` tao/migrate DB runtime. |
| TASK-203 | DONE | `build_scripts/posture_app.spec`, build thanh cong. |
| TASK-204 | DONE | `build_scripts/smoke_test_dist.ps1`, smoke runtime files PASS. |
| TASK-205 | DONE | `release/PostureDetectionApp_0.1.0-demo/` va zip release. |
| TASK-206 | DONE | `release_docs/README_RUN_APP.md`. |
| TASK-207 | NOT STARTED | Installer Inno Setup tuy chon, chua can cho portable demo. |
| TASK-208 | PARTIAL DONE | Dev-machine smoke PASS; clean-machine manual QA con pending. |
| TASK-209 | DOCUMENTED | Huong toi uu RF/sklearn da ghi trong release notes/task. |
| TASK-210 | DONE | `release/VERSION.txt`, `reports/DEPLOYMENT_RELEASE_NOTES.md`. |

Build output:

- `dist/PostureDetectionApp/PostureDetectionApp.exe`
- `release/PostureDetectionApp_0.1.0-demo.zip`

## Ket luan deploy phu hop voi project hien tai

Nen deploy theo huong:

> Windows desktop app, PyInstaller `onedir`, kem folder `models/`, `assets/`, database seed, va runtime writable database trong `%LOCALAPPDATA%`.

Khong nen uu tien `onefile` luc dau vi:

- TensorFlow va MediaPipe rat lon.
- Startup onefile cham.
- De loi do native DLL, model files, MediaPipe assets.
- Kho debug khi app loi tren may khac.

Neu muon san pham nhe hon ve sau, huong tot la dong goi model Random Forest/scikit-learn thay ANN TensorFlow, vi benchmark moi cho thay Random Forest dang co F1 external cao hon ANN.

## TASK-200: Chot pham vi ban deploy dau tien

Muc tieu: xac dinh ban deploy la ban demo san pham, khong kem dataset/raw videos.

Can dong goi:

- `src/4_main_desktop_app.py`
- `src/posture_baseline.py`
- `src/statistics_service.py`
- `src/utils.py`
- `models/ann_best.keras`
- `models/scaler.pkl`
- `assets/sounds/alarm.wav`
- Database seed hoac script tao database.

Khong dong goi:

- `dataset/`
- `reports/`
- `notebooks/`
- `tests/`
- `models/local_training/`
- `models/models_old/`
- `models/tmp_smoke/`

Done khi:

- Co danh sach file runtime ro rang.
- Xac nhan app deploy chi phuc vu chay/demo, khong train/evaluate.

## TASK-201: Tach helper duong dan runtime cho PyInstaller

Muc tieu: app tim dung file khi chay bang Python va khi chay bang `.exe`.

Can tao file moi:

- `src/runtime_paths.py`

Noi dung can co:

- `is_frozen()`: kiem tra `getattr(sys, "frozen", False)`.
- `app_base_dir()`: khi frozen dung thu muc exe hoac `_MEIPASS`; khi dev dung root project.
- `user_data_dir()`: Windows dung `%LOCALAPPDATA%/PostureDetectionApp`.
- `resource_path(relative_path)`: tim assets/model kem app.
- `writable_database_path()`: database runtime trong user data dir.

Can sua:

- `src/4_main_desktop_app.py`
- `src/config.py`
- neu can: `src/3_database_setup.py`

Ly do:

- File trong `dist/` co the doc duoc.
- Database trong `Program Files` hoac folder read-only co the khong ghi duoc.
- SQLite nen nam trong `%LOCALAPPDATA%` de app co quyen ghi.

Done khi:

- Chay dev bang `python src/4_main_desktop_app.py` van duoc.
- Chay app init test khong loi.

## TASK-202: Them first-run database initialization

Muc tieu: neu may nguoi dung chua co database, app tu tao database lan dau.

Can lam:

- Tao function `ensure_runtime_database()`:
  - Tao folder `%LOCALAPPDATA%/PostureDetectionApp`.
  - Neu chua co `posture_app.db`, tao schema bang logic tu `src/3_database_setup.py` hoac copy seed DB.
  - Neu DB cu thieu cot moi, chay migration.

Khuyen nghi:

- Khong copy DB demo co log cu cua developer vao product.
- Tao DB moi sach, co Admin + CaiDat default.

Done khi:

- Xoa database runtime, mo app, app tu tao lai DB.
- App ghi duoc setting/theme/session.

## TASK-203: Tao file PyInstaller spec

Muc tieu: build app onedir on dinh, co du resource.

Can tao:

- `build_scripts/posture_app.spec`

Can include data:

- `models/ann_best.keras` -> `models/ann_best.keras`
- `models/scaler.pkl` -> `models/scaler.pkl`
- `assets/sounds/alarm.wav` -> `assets/sounds/alarm.wav`

Can include hidden imports co kha nang can:

- `customtkinter`
- `PIL._tkinter_finder`
- `sklearn`
- `joblib`
- `mediapipe`
- `tensorflow`
- `matplotlib.backends.backend_tkagg`

Lenh build mau:

```powershell
.\.venv\Scripts\python.exe -m pip install pyinstaller
.\.venv\Scripts\pyinstaller.exe --clean --noconfirm build_scripts/posture_app.spec
```

Output mong doi:

- `dist/PostureDetectionApp/PostureDetectionApp.exe`

Done khi:

- Build khong loi.
- Folder `dist/PostureDetectionApp/` co `.exe`, `models/`, `assets/`.

## TASK-204: Tao smoke test cho ban build

Muc tieu: kiem tra `.exe` mo duoc tren may dev.

Can tao:

- `build_scripts/smoke_test_dist.ps1`

Noi dung test:

1. Kiem tra exe ton tai.
2. Kiem tra model/scaler/sound ton tai trong dist.
3. Chay exe manual.
4. Mo GUI, xem theme light/dark.
5. Bam Start voi webcam hoac video file.
6. Bam Stop.
7. Mo thong ke.
8. Dong app.

Done khi:

- App mo duoc tu `.exe`.
- Khong can activate `.venv`.
- Database runtime duoc tao trong `%LOCALAPPDATA%`.

## TASK-205: Tao ban demo folder portable

Muc tieu: co folder co the nen zip va gui sang may khac.

Can tao:

- `release/PostureDetectionApp_<version>/`

Noi dung:

- `PostureDetectionApp.exe`
- Cac DLL/runtime do PyInstaller sinh.
- `models/`
- `assets/`
- `README_RUN_APP.md`
- `LICENSE_OR_NOTICE.md` neu can.

Khong kem:

- dataset raw.
- reports nghien cuu.
- notebooks.
- source code train.

Done khi:

- Zip folder release.
- Copy sang may Windows khac, double-click exe chay duoc.

## TASK-206: Viet README cho nguoi dung cuoi

Muc tieu: nguoi dung khong can biet Python van chay duoc app.

Can tao:

- `release_docs/README_RUN_APP.md`

Noi dung:

- Cach mo app.
- Cach chon webcam: nhap `0`.
- Cach chon video: nhap duong dan file video.
- Cach chon IP camera.
- Cach bat/tat am thanh.
- Cach doi Light/Dark.
- Cach xem thong ke.
- Loi thuong gap:
  - webcam dang bi app khac dung.
  - Windows SmartScreen can bam More info -> Run anyway.
  - video HEVC/H.265 khong doc duoc, nen convert H.264.
  - app lan dau mo cham do load TensorFlow/MediaPipe.

Done khi:

- README du de nguoi khac tu mo app.

## TASK-207: Tao installer tuy chon

Muc tieu: neu can san pham trong hon folder portable.

Lua chon:

- Inno Setup cho Windows installer.
- NSIS neu quen he sinh thai do.

Khuyen nghi:

- Ban demo/tot nghiep: dung portable zip la du.
- Ban ban giao/nguoi dung ngoai: tao Inno Setup installer.

Can installer lam:

- Copy folder app vao `%LOCALAPPDATA%` hoac `%ProgramFiles%`.
- Tao shortcut desktop.
- Tao Start Menu shortcut.
- Khong dat database writable trong `%ProgramFiles%`; database van nam `%LOCALAPPDATA%`.

Done khi:

- Cai dat xong co shortcut.
- Uninstall xoa app files, khong bat buoc xoa user data.

## TASK-208: Kiem tra tren may sach

Muc tieu: dam bao app khong phu thuoc `.venv` cua developer.

May test nen co:

- Windows 10/11.
- Khong cai Python.
- Co webcam neu test camera.

Checklist:

- Double-click exe mo app.
- App khong bao thieu DLL.
- Start webcam duoc.
- Start video file duoc.
- Stop khong treo.
- Light/Dark doi duoc.
- Thong ke mo duoc.
- Database co log moi.

Done khi:

- Co file `reports/DEPLOYMENT_QA_REPORT.md`.

## TASK-209: Toi uu kich thuoc va toc do khoi dong

Muc tieu: san pham nhe va mo nhanh hon.

Viec can xem:

- TensorFlow lam ban build rat lon.
- Neu chi can inference tabular, Random Forest co the thay ANN.
- Benchmark moi cho thay Random Forest external F1 cao hon ANN.

Huong toi uu:

1. Train/export Random Forest model `.joblib`.
2. Sua app de load model scikit-learn neu config chon RF.
3. Neu bo TensorFlow khoi runtime, file build se nhe hon nhieu.
4. Giu ANN la che do research, RF la che do product neu metric video/person-wise xac nhan.

Done khi:

- Co so sanh size build ANN vs RF.
- Co quyet dinh model default cho product.

## TASK-210: Dong bang phien ban release

Muc tieu: moi ban build co version va log ro.

Can tao:

- `release/VERSION.txt`
- `reports/DEPLOYMENT_RELEASE_NOTES.md`

Thong tin can ghi:

- Version app.
- Ngay build.
- Python version.
- Dependency versions.
- Model file hash/size.
- Known limitations.
- Cach rollback.

Done khi:

- Co release notes.
- Co hash cho exe/model/scaler.

## Lenh deploy de xuat

### 1. Chuan bi moi truong

```powershell
cd D:\posture_detection_app
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
```

### 2. Kiem tra app truoc build

```powershell
python -m pytest tests -q
python -m py_compile src/4_main_desktop_app.py src/posture_baseline.py src/statistics_service.py src/utils.py
python src/4_main_desktop_app.py
```

### 3. Build app

```powershell
pyinstaller --clean --noconfirm build_scripts/posture_app.spec
```

### 4. Chay app da build

```powershell
.\dist\PostureDetectionApp\PostureDetectionApp.exe
```

### 5. Tao zip release

```powershell
Compress-Archive -Path .\dist\PostureDetectionApp\* -DestinationPath .\release\PostureDetectionApp_windows_demo.zip -Force
```

## Cau truc release mong doi

```text
release/
  PostureDetectionApp_0.1.0/
    PostureDetectionApp.exe
    models/
      ann_best.keras
      scaler.pkl
    assets/
      sounds/
        alarm.wav
    README_RUN_APP.md
    VERSION.txt
```

## Rui ro deploy can biet

| Rui ro | Cach xu ly |
|---|---|
| Exe qua nang | Chap nhan ban demo; ve sau chuyen Random Forest/sklearn de bo TensorFlow. |
| App khong ghi duoc DB | Dung `%LOCALAPPDATA%/PostureDetectionApp/posture_app.db`. |
| Thieu model/scaler | Dua vao PyInstaller datas va smoke test. |
| MediaPipe/TensorFlow loi DLL | Dung PyInstaller onedir, build tren Windows cung kien truc voi may chay. |
| Windows SmartScreen canh bao | Viet README huong dan, neu release that thi can code signing. |
| Webcam khong mo | Huong dan dong app khac, test camera index `0`, `1`. |
| Video HEVC khong doc | Convert sang H.264 MP4. |

## Uu tien thuc thi

1. TASK-201
2. TASK-202
3. TASK-203
4. TASK-204
5. TASK-205
6. TASK-206
7. TASK-208
8. TASK-210
9. TASK-207 neu can installer
10. TASK-209 neu can toi uu kich thuoc/performance

## Definition of Done cho ban san pham demo

- Co folder `dist/PostureDetectionApp/`.
- Double-click `.exe` mo GUI.
- Chay webcam/video duoc.
- Model/scaler/sound load duoc.
- Database runtime ghi duoc.
- Light/Dark, smoothing, dashboard hoat dong.
- Co README cho nguoi dung.
- Co QA report deploy.
- Co zip release co version.
