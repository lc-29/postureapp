# Deployment Release Notes

Ngay cap nhat: 2026-05-27

## Version

`PostureDetectionApp 0.1.0-demo`

## Scope

Ban release nay dong goi app desktop CustomTkinter de chay demo realtime:

- Webcam/camera IP/video file input.
- MediaPipe Pose.
- ANN posture classifier.
- Rule-based baseline mode.
- Sound warning.
- SQLite session logging.
- Statistics dashboard.
- Light/Dark theme.
- Temporal smoothing settings.

Khong dong goi dataset, notebooks, reports nghien cuu, tests, hay raw videos.

## Runtime files

- `PostureDetectionApp.exe`
- `models/ann_best.keras`
- `models/scaler.pkl`
- `assets/sounds/alarm.wav`

## Build artifacts

- `dist/PostureDetectionApp/PostureDetectionApp.exe`
- `release/PostureDetectionApp_0.1.0-demo/`
- `release/PostureDetectionApp_0.1.0-demo.zip`

Release zip size: `661,155,257` bytes.

## Runtime database

Database writable nam tai:

```text
%LOCALAPPDATA%\PostureDetectionApp\posture_app.db
```

App se tu tao database lan dau neu chua co.

## Known limitations

- Build TensorFlow/MediaPipe co kich thuoc lon.
- Lan dau mo app co the cham.
- Windows SmartScreen co the canh bao neu app chua code-sign.
- QA tren may sach can thuc hien manual.
- Export CSV research trong ban exe da dong goi khong phai luong chinh; dung source Python neu can export.

## Suggested next release

- Dong goi Random Forest/scikit-learn model de giam kich thuoc va tang F1 external.
- Tao Inno Setup installer.
- Code-sign exe neu phat hanh ngoai moi truong noi bo.
