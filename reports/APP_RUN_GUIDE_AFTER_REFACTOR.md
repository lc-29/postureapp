# Huong dan chay app sau khi refactor

## 1. Cach chay khuyen nghi

Mo PowerShell:

```powershell
cd D:\posture_detection_app
.venv\Scripts\activate
python src\4_main_desktop_app.py
```

Cach nay van la cach chay on dinh nhat vi `src/4_main_desktop_app.py` con giu class UI chinh `PostureApp`.

## 2. Cach chay qua entrypoint moi

Neu muon chay theo package `src/app/`:

```powershell
cd D:\posture_detection_app
.venv\Scripts\activate
$env:PYTHONPATH="D:\posture_detection_app\src"
python -m app.main
```

Trong giai doan refactor hien tai, `app.main` la wrapper goi lai app chinh cu. Cach nay dung de kiem tra package moi da import duoc.

## 3. Neu chay bang VS Code

1. Mo thu muc `D:\posture_detection_app`.
2. Chon Python interpreter la `.venv`.
3. Mo terminal trong VS Code.
4. Chay:

```powershell
python src\4_main_desktop_app.py
```

## 4. Mode nen dung khi demo

- Demo realtime truoc hoi dong: `HistGradientBoosting (high recall demo)`.
- Bao cao ket qua khoa hoc: `HistGradientBoosting (balanced best)`.
- `ANN`: model neural network baseline/ung dung ban dau.
- `Rule-based Baseline`: baseline giai thich duoc, dung de so sanh.

## 5. Y nghia cac entrypoint

- `src/4_main_desktop_app.py`: entrypoint chinh, on dinh nhat.
- `src/app/main.py`: entrypoint moi theo kien truc package, hien dang wrapper de giu an toan.
- `src/app/config/`: hang so va theme.
- `src/app/services/model_service.py`: load va predict HGB.
- `src/app/repositories/database.py`: ket noi SQLite.
- `src/app/utils/video_source.py`: xu ly webcam/IP camera/video file.

## 6. Kiem tra nhanh neu bi loi

Chay syntax check:

```powershell
.venv\Scripts\python.exe -m py_compile src\4_main_desktop_app.py
```

Kiem tra package:

```powershell
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0, 'src'); import app; print('app package ok')"
```

Kiem tra test model/schema:

```powershell
.venv\Scripts\python.exe -m pytest tests\test_feature_schema.py tests\test_model_registry_service.py
```

