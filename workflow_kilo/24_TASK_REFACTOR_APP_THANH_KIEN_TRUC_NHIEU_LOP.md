# 24_TASK_REFACTOR_APP_THANH_KIEN_TRUC_NHIEU_LOP

## Muc tieu

Tai cau truc phan app desktop hien dang nam chu yeu trong `src/4_main_desktop_app.py` thanh package `src/app/` co phan cap ro rang, gan voi mo hinh 3 lop:

- Presentation/UI layer
- Business/Service layer
- Data access/Repository layer

Quan trong: app hien tai dang hoat dong tot, nen refactor phai lam an toan, tung buoc, tranh lam hong code. Khong refactor cac script thuc nghiem/trich xuat/train model neu khong lien quan den runtime app.

## Hien trang hien tai

File app chinh:

- `src/4_main_desktop_app.py`

File nay dang gom nhieu vai tro:

- UI CustomTkinter
- Dang nhap/dang ky/OTP
- Mo webcam/IP camera/video
- MediaPipe Pose
- ANN/HGB/Rule-based prediction
- Canh bao/smoothing/cooldown
- SQLite session/log/settings/statistics
- Dashboard thong ke
- Light/dark mode

Dieu nay lam app kho bao tri va kho sua loi. Muc tieu refactor la tach code theo module de biet chuc nang nao nam o dau, nhung van giu hanh vi app nhu hien tai.

## Nguyen tac bat buoc

- Khong xoa `src/4_main_desktop_app.py` ngay.
- Khong doi logic model neu khong can.
- Khong doi database schema neu khong can.
- Khong doi cac script research/experiment:
  - `2_extract_features.py`
  - `15_build_video_manifest.py`
  - `16_build_ergonomic_features.py`
  - `21_train_model_registry.py`
  - `22_calibrate_threshold.py`
  - `23_final_evaluation_protocol.py`
  - `27_model_improvement_fp_reduction.py`
  - `28_train_ann_local_rebuild.py`
- Khong ghi de model/dataset/report.
- Sau moi buoc tach code lon, phai chay test/syntax check.
- Neu gap rui ro cao, dung lai va ghi vao report thay vi co tinh tach het.
- Uu tien giu app chay duoc hon la tach code qua dep.

## Kien truc dich

Tao cau truc:

```text
src/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   └── theme.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── auth_view.py
│   │   ├── dashboard_view.py
│   │   └── widgets.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── app_controller.py
│   │   ├── camera_controller.py
│   │   └── auth_controller.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── model_service.py
│   │   ├── posture_service.py
│   │   ├── warning_service.py
│   │   ├── session_service.py
│   │   └── statistics_service.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── user_repository.py
│   │   ├── settings_repository.py
│   │   ├── session_repository.py
│   │   └── posture_log_repository.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── app_state.py
│   │   ├── entities.py
│   │   └── prediction_result.py
│   └── utils/
│       ├── __init__.py
│       ├── paths.py
│       ├── video_source.py
│       └── image_utils.py
├── 4_main_desktop_app.py
└── ...
```

Neu khong kip tach het, chap nhan muc tieu trung gian:

- Tao `src/app/`.
- Tach cac service/repository/util it rui ro truoc.
- `main_window.py` co the tam thoi van chua nhe hoan toan.
- `src/4_main_desktop_app.py` van chay duoc.

## Buoc 1. Backup truoc khi refactor

Tao thu muc:

- `outputs/backups/app_refactor_before_<YYYYMMDD_HHMMSS>/`

Copy toi thieu:

- `src/4_main_desktop_app.py`
- `src/auth_service.py`
- `src/statistics_service.py`
- `src/runtime_paths.py`
- `src/model_registry_service.py`
- `src/feature_schema.py`
- `src/3_database_setup.py`
- cac test lien quan trong `tests/`

Ghi backup path vao report.

## Buoc 2. Tao package `src/app/`

Tao cac thu muc va file `__init__.py`:

- `src/app/`
- `src/app/config/`
- `src/app/ui/`
- `src/app/controllers/`
- `src/app/services/`
- `src/app/repositories/`
- `src/app/models/`
- `src/app/utils/`

Chua can di chuyen logic lon ngay.

## Buoc 3. Tao entrypoint moi nhung giu entrypoint cu

Tao:

- `src/app/main.py`

Ban dau co the import app cu:

```python
from importlib import import_module


def main() -> None:
    legacy_app = import_module("4_main_desktop_app")
    legacy_app.main()


if __name__ == "__main__":
    main()
```

Neu import ten file bat dau bang so gay kho, co the giu `src/4_main_desktop_app.py` la entrypoint chinh trong giai doan 1 va tao `src/app/main.py` sau khi tach class `PostureApp`.

Muc tieu cuoi:

- `python src/4_main_desktop_app.py` van chay.
- `python -m app.main` hoac `python src/app/main.py` cung chay neu kha thi.

## Buoc 4. Tach config/constants truoc

Tach cac hang so it rui ro sang:

- `src/app/config/constants.py`

Nhom hang so:

- model paths/mode names
- video size/inference size
- capture settings
- thresholds rule-based
- status text/color neu phu hop

Can lam than trong:

- Neu tach lam import vong tron, dung lai.
- Co the tach tung nhom nho.

Sau khi tach:

```powershell
.venv\Scripts\python.exe -m py_compile src\4_main_desktop_app.py
```

## Buoc 5. Tach theme

Tach theme/palette sang:

- `src/app/config/theme.py`

Chua can doi UI layout. Chi tach:

- `THEMES`
- `THEME`
- `app_font`
- cac helper mau neu co

Neu qua phuc tap, chi tao file theme va de TODO trong report.

## Buoc 6. Tach utils

Tach cac ham tien ich it phu thuoc UI sang:

- `src/app/utils/paths.py`
  - wrapper cho resource_path/app_base_dir neu can
- `src/app/utils/video_source.py`
  - `resolve_source`
  - `infer_current_view_angle` neu tach duoc
- `src/app/utils/image_utils.py`
  - cac ham resize/convert image neu it phu thuoc class

Sau moi lan tach, chay:

```powershell
.venv\Scripts\python.exe -m py_compile src\4_main_desktop_app.py
```

## Buoc 7. Tach model service

Tao:

- `src/app/services/model_service.py`

Muc tieu tach logic model khoi UI:

- load ANN
- load scaler
- load HGB mode configs
- load HGB threshold
- predict ANN
- predict HGB
- build landmark DataFrame
- goi `build_feature_matrix`

De xuat tao class:

```python
class ModelService:
    def load_ann(...)
    def load_hgb(...)
    def predict_ann(...)
    def predict_hgb(...)
```

Can giu hanh vi:

- ANN van dung raw_99 + scaler.
- HGB balanced dung `ergonomic_v2_with_view`, threshold 0.76.
- HGB high recall dung `normalized_99`, threshold 0.50.

Neu tach het qua rui ro, it nhat tach:

- `HGB_MODE_CONFIGS`
- `load_hgb_model`
- `load_hgb_threshold`
- `build_landmark_frame_dataframe`

## Buoc 8. Tach warning service

Tao:

- `src/app/services/warning_service.py`

Tach logic:

- sai lien tuc bao nhieu giay moi canh bao
- cooldown canh bao
- phat am thanh/co nen phat am thanh

Neu logic hien tai phu thuoc qua nhieu state trong `PostureApp`, co the chi tao helper/data class va ghi TODO.

## Buoc 9. Tach repository layer

Tao:

- `src/app/repositories/database.py`
- `src/app/repositories/user_repository.py`
- `src/app/repositories/settings_repository.py`
- `src/app/repositories/session_repository.py`
- `src/app/repositories/posture_log_repository.py`

Muc tieu:

- UI khong query SQL truc tiep trong tuong lai.
- Cac ham SQLite duoc gom theo bang/chuc nang.

Can lam an toan:

- Truoc tien co the move wrapper nho quanh cac ham hien co.
- Khong doi schema.
- Khong doi ten cot.
- Khong doi logic user-scoped database.

Neu refactor SQL qua lon, dung lai va chi tao khung repository + report.

## Buoc 10. Tach UI neu an toan

UI la phan rui ro cao nhat. Lam cuoi cung.

Co the tach:

- `src/app/ui/main_window.py`
  - class `PostureApp`
- `src/app/ui/auth_view.py`
  - cac ham tao man hinh login/register/OTP neu tach duoc
- `src/app/ui/dashboard_view.py`
  - thong ke/dashboard
- `src/app/ui/widgets.py`
  - helper tao entry/section/card

Muc tieu cuoi:

- `PostureApp` nam trong `src/app/ui/main_window.py`.
- `src/app/main.py` import `PostureApp` va start.
- `src/4_main_desktop_app.py` tro thanh wrapper:

```python
from app.main import main


if __name__ == "__main__":
    main()
```

Neu khong kip hoac rui ro:

- De `PostureApp` trong `4_main_desktop_app.py`.
- Ghi ro giai doan 1 moi tach service/utils/repository.

## Buoc 11. Cap nhat import path

Can dam bao cac cach chay sau khong loi:

```powershell
python src/4_main_desktop_app.py
.venv\Scripts\python.exe src\4_main_desktop_app.py
```

Neu tao duoc entrypoint moi:

```powershell
$env:PYTHONPATH="D:\posture_detection_app\src"
.venv\Scripts\python.exe -m app.main
```

Hoac:

```powershell
.venv\Scripts\python.exe src\app\main.py
```

## Buoc 12. Test sau refactor

Bat buoc chay:

```powershell
.venv\Scripts\python.exe -m py_compile src\4_main_desktop_app.py
.venv\Scripts\python.exe -m pytest tests\test_feature_schema.py tests\test_model_registry_service.py
```

Neu co them tests app:

```powershell
.venv\Scripts\python.exe -m pytest tests
```

Kiem tra import:

```powershell
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0, 'src'); import app; print('app package ok')"
```

Neu tao `app.main`, test:

```powershell
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0, 'src'); from app.main import main; print(main)"
```

## Buoc 13. Test app thu cong

Chay:

```powershell
.venv\Scripts\python.exe src\4_main_desktop_app.py
```

Kiem tra:

- Login/register van hoat dong.
- Chon webcam/video.
- Mode ANN van load duoc.
- Mode `HistGradientBoosting (balanced best)` van load duoc.
- Mode `HistGradientBoosting (high recall demo)` van load duoc.
- Rule-based Baseline van chay.
- Bat/dung camera khong loi.
- Am thanh canh bao khong loi.
- SQLite session/log van ghi rieng theo user.
- Dashboard thong ke van mo duoc.

## Buoc 14. Tao report refactor

Tao:

- `reports/APP_REFACTOR_ARCHITECTURE_REPORT.md`

Report gom:

1. Muc tieu refactor.
2. Backup path.
3. Cau truc thu muc moi.
4. File nao da tach.
5. File nao chua tach vi rui ro.
6. Cach chay app sau refactor.
7. Test da chay va ket qua.
8. Gioi han con lai.
9. Huong refactor tiep theo.

## Buoc 15. Cap nhat README chay app

Cap nhat hoac tao:

- `reports/APP_RUN_GUIDE_AFTER_REFACTOR.md`

Noi dung:

### Cach chay app hien tai

```powershell
cd D:\posture_detection_app
.venv\Scripts\activate
python src\4_main_desktop_app.py
```

Hoac neu entrypoint moi hoat dong:

```powershell
cd D:\posture_detection_app
.venv\Scripts\activate
$env:PYTHONPATH="D:\posture_detection_app\src"
python -m app.main
```

### Mode khuyen nghi khi demo

- Demo realtime: `HistGradientBoosting (high recall demo)`.
- Bao cao khoa hoc: `HistGradientBoosting (balanced best)`.
- ANN: baseline neural network.
- Rule-based: baseline giai thich duoc.

## Checklist hoan thanh

- [ ] Da backup app truoc refactor.
- [ ] Da tao `src/app/`.
- [ ] Da tao cac subpackage `config`, `ui`, `controllers`, `services`, `repositories`, `models`, `utils`.
- [ ] Da tach duoc it nhat config/utils/model-service hoac ghi ro neu chua tach vi rui ro.
- [ ] `src/4_main_desktop_app.py` van chay duoc.
- [ ] Neu co `src/app/main.py`, entrypoint moi import duoc.
- [ ] Cac script experiment van nam ngoai `src/app/`.
- [ ] Py compile pass.
- [ ] Pytest lien quan pass.
- [ ] Da tao `APP_REFACTOR_ARCHITECTURE_REPORT.md`.
- [ ] Da tao `APP_RUN_GUIDE_AFTER_REFACTOR.md`.
- [ ] Da huong dan lai cach chay app.

## Luu y khi tra loi hoi dong

Neu hoi vi sao truoc do code gom trong 1 file:

> Giai doan dau em uu tien hoan thien chuc nang va thuc nghiem nen app duoc phat trien tap trung trong file chinh. Sau khi cac chuc nang on dinh, em tai cau truc thanh package nhieu lop de de bao tri, de thay model, de kiem thu va de mo rong.

Neu hoi kien truc moi:

> Em tach app theo huong 3 lop: UI layer cho CustomTkinter, service/controller layer cho xu ly nghiep vu nhu camera, model, warning, session, va repository layer cho SQLite. Cac script nghien cuu nhu trich xuat CSV, train model, benchmark duoc giu rieng ben ngoai app runtime.

