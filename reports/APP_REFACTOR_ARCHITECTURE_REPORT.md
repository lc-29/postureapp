# Bao cao tai cau truc app desktop theo kien truc nhieu lop

## 1. Muc tieu

Tai cau truc phan runtime desktop app tu file lon `src/4_main_desktop_app.py` sang package `src/app/` theo huong 3 lop:

- Presentation/UI layer: giao dien CustomTkinter.
- Business/Service layer: xu ly model, posture prediction, warning, session.
- Data access/Repository layer: SQLite connection va repository theo nhom bang.

Muc tieu uu tien trong lan refactor nay la giu app dang chay on dinh, tach cac phan it rui ro truoc, khong doi logic model, dataset, database schema hoac cac script thuc nghiem.

## 2. Backup truoc refactor

Backup da tao tai:

```text
outputs/backups/app_refactor_before_20260625_162020/
```

Noi dung backup gom:

- `src/4_main_desktop_app.py`
- `src/auth_service.py`
- `src/statistics_service.py`
- `src/runtime_paths.py`
- `src/model_registry_service.py`
- `src/feature_schema.py`
- `src/3_database_setup.py`
- thu muc `tests/`

## 3. Cau truc thu muc moi

Da tao package:

```text
src/app/
  __init__.py
  main.py
  config/
    __init__.py
    constants.py
    theme.py
  ui/
    __init__.py
    main_window.py
    auth_view.py
    dashboard_view.py
    widgets.py
  controllers/
    __init__.py
    app_controller.py
    auth_controller.py
    camera_controller.py
  services/
    __init__.py
    model_service.py
    posture_service.py
    session_service.py
    statistics_service.py
    warning_service.py
  repositories/
    __init__.py
    database.py
    user_repository.py
    settings_repository.py
    session_repository.py
    posture_log_repository.py
  models/
    __init__.py
    app_state.py
    entities.py
    prediction_result.py
  utils/
    __init__.py
    paths.py
    video_source.py
    image_utils.py
```

## 4. File da tach logic

### `src/app/config/constants.py`

Da tach cac hang so runtime:

- duong dan model/scaler/alarm/database;
- ten mode ANN, HGB balanced, HGB high-recall, rule-based;
- cau hinh HGB mode va nguong fallback;
- default settings;
- so landmark/features;
- nguong rule-based baseline;
- kich thuoc video/inference/capture;
- status text, risk text, data quality text va mau status.

### `src/app/config/theme.py`

Da tach:

- `APP_FONT_FAMILY`;
- `THEMES`;
- `THEME`;
- helper `app_font()`.

### `src/app/repositories/database.py`

Da tach helper:

- `get_db_connection()`

Helper nay tao SQLite connection va bat `PRAGMA foreign_keys = ON`.

### `src/app/utils/video_source.py`

Da tach:

- `project_path_from_text()`;
- `resolve_source()`;
- `infer_view_angle_from_source()`.

Nhom nay xu ly duong dan video/webcam/IP camera va suy ra view angle tu ten file video.

### `src/app/services/model_service.py`

Da tach logic model-service cho HGB:

- `load_hgb_model()`;
- `load_hgb_threshold()`;
- `build_landmark_frame_dataframe()`;
- `predict_hgb_probability()`.

`src/4_main_desktop_app.py` hien da goi cac helper nay thay vi tu xu ly truc tiep trong UI class.

### `src/app/main.py`

Da tao entrypoint moi:

```powershell
$env:PYTHONPATH="D:\posture_detection_app\src"
python -m app.main
```

Trong giai doan an toan nay, `app.main` van goi lai legacy module `4_main_desktop_app.py`.

## 5. File chua tach het

Chua di chuyen toan bo class `PostureApp` khoi `src/4_main_desktop_app.py`.

Ly do:

- UI CustomTkinter, camera loop, MediaPipe, alarm, SQLite session va dashboard dang phu thuoc lan nhau rat nhieu.
- Neu di chuyen toan bo class trong mot lan, rui ro gay loi import vong tron va loi UI cao.
- Lan refactor nay uu tien tao package, tach config/utils/model/database truoc, giu app chay duoc.

`src/app/ui/main_window.py`, `auth_view.py`, `dashboard_view.py`, `widgets.py`, cac controller/repository/service con lai hien la khung cho giai doan tiep theo.

## 6. Cach chay app sau refactor

Cach chay on dinh nhu truoc:

```powershell
cd D:\posture_detection_app
.venv\Scripts\activate
python src\4_main_desktop_app.py
```

Cach chay qua entrypoint moi:

```powershell
cd D:\posture_detection_app
.venv\Scripts\activate
$env:PYTHONPATH="D:\posture_detection_app\src"
python -m app.main
```

## 7. Kiem tra da chay

Da chay syntax check:

```powershell
.venv\Scripts\python.exe -m py_compile src\4_main_desktop_app.py src\app\main.py src\app\config\constants.py src\app\config\theme.py src\app\services\model_service.py src\app\repositories\database.py src\app\utils\video_source.py
```

Ket qua: pass.

Da chay import check:

```powershell
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0, 'src'); import app; print('app package ok')"
.venv\Scripts\python.exe -c "import sys; sys.path.insert(0, 'src'); from app.main import main; print(main)"
```

Ket qua: pass.

Da chay pytest lien quan:

```powershell
.venv\Scripts\python.exe -m pytest tests\test_feature_schema.py tests\test_model_registry_service.py
```

Ket qua:

```text
4 passed
```

## 8. Gioi han con lai

- `PostureApp` van con nam trong `src/4_main_desktop_app.py`.
- SQL chi moi tach connection helper, chua tach het query theo repository.
- Warning/cooldown/session/dashboard chua tach thanh service doc lap.
- Chua them test tu dong cho UI vi CustomTkinter/camera can test thu cong.

## 9. Huong refactor tiep theo

Thu tu nen lam tiep:

1. Tach SQL session/log/settings thanh repository that su.
2. Tach warning/cooldown/smoothing thanh `WarningService`.
3. Tach camera capture/read/update loop thanh `CameraController`.
4. Tach auth UI va dashboard UI sau cung.
5. Khi cac dependency da gon, moi chuyen `PostureApp` sang `src/app/ui/main_window.py` va bien `src/4_main_desktop_app.py` thanh wrapper gon.

## 10. Cau tra loi khi bao cao

Neu duoc hoi vi sao truoc day code nam trong mot file:

> Giai doan dau em uu tien hoan thien chuc nang demo, train model va thuc nghiem nen app duoc phat trien tap trung trong file chinh. Sau khi chuc nang on dinh, em bat dau tai cau truc thanh package nhieu lop de de bao tri, de thay model, de kiem thu va de mo rong.

Neu duoc hoi kien truc moi:

> Em tach app theo huong 3 lop: UI layer cho CustomTkinter, service/controller layer cho xu ly nghiep vu nhu camera, model, warning va session, repository layer cho SQLite. Cac script nghien cuu nhu trich xuat CSV, train model va benchmark duoc giu rieng ben ngoai app runtime.

