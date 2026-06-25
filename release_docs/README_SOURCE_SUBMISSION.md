# UNG DUNG PHAT HIEN LOI TU THE LAM VIEC QUA WEBCAM

## Thong tin sinh vien

- Ho va ten: Duong Ly Cu
- MSSV: 223650
- Lop: DH22TIN01

## 1. Noi dung goi nop

Thu muc app nay chua source code Python, model da huan luyen, scaler,
model HistGradientBoosting tot nhat theo thuc nghiem, co so du lieu SQLite
demo, du lieu CSV co metadata, test va script build. Ba bieu mau va file
PDF bao cao thuc tap nam o cap goc cua file ZIP, ngang hang voi thu muc app.

Video goc khong duoc kem theo vi dung luong lon. Ung dung van co the chay
voi webcam, camera IP hoac mot file video MP4 do nguoi dung tu chon.

Day la he thong ho tro nhac nho tu the, khong phai cong cu chan doan y te.

## 2. Yeu cau he thong

- Windows 10 hoac Windows 11 64-bit.
- Python 3.10 hoac Python 3.11.
- Webcam neu chay truc tiep; khong bat buoc neu dung video MP4.
- Khuyen nghi RAM tu 8 GB.
- Can Internet trong lan dau cai thu vien Python.

Khong nen dung Python 3.12 tro len neu TensorFlow/MediaPipe trong
`requirements.txt` khong cai dat duoc.

## 3. Cai dat

Mo PowerShell tai thu muc goc cua goi source, sau do chay:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Neu PowerShell chan kich hoat moi truong ao, chay lenh sau trong cua so
PowerShell hien tai va kich hoat lai:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 4. Chay ung dung

Sau khi kich hoat moi truong ao:

```powershell
python src/4_main_desktop_app.py
```

Hoac bam dup `run_app.bat` sau khi thu muc `.venv` da duoc tao va cai dat
day du thu vien.

Ung dung tu kiem tra schema database khi khoi dong. Khong can reset
database truoc moi lan chay.

## 5. Cach su dung nhanh

1. Tai muc `Nguon dau vao`, nhap `0` de dung webcam mac dinh.
2. Co the nhap `1` neu may co nhieu camera.
3. De chay video, nhap duong dan day du den file MP4.
4. De chay camera IP, nhap URL `http://...` hoac `rtsp://...`.
5. Chon che do nhan dien:
   - `ANN`: model Keras dang duoc tich hop trong app.
   - `HistGradientBoosting (best)`: model thuc nghiem tot nhat.
   - `Rule-based Baseline`: baseline dua tren cac nguong hinh hoc.
6. Bam `Bat dau` de nhan dien va `Dung` de ket thuc phien.
7. Mo phan thong ke de xem lich su, thoi gian dung/sai tu the va muc rui ro.

## 6. Model va dac trung

### ANN/Keras

- Model: `models/ann_best.keras`
- Scaler: `models/scaler.pkl`
- Dau vao: 99 dac trung toa do x, y, z cua 33 MediaPipe Pose landmarks.

Scaler chuan hoa vector dac trung truoc khi ANN du doan xac suat
`Incorrect posture`.

### HistGradientBoosting

- Registry: `models/model_registry.json`
- Model:
  `models/registry/hist_gradient_boosting__normalized_99/model.pkl`
- Schema:
  `models/registry/hist_gradient_boosting__normalized_99/feature_schema.json`
- Nguong:
  `models/registry/hist_gradient_boosting__normalized_99/threshold.json`

Model nay dung 99 landmark da chuan hoa theo co the. Day la model dat ket
qua tot nhat trong protocol thuc nghiem hien tai va duoc them nhu mot lua
chon trong app demo.

## 7. Co so du lieu

Database demo:

```text
database/posture_app.db
```

Database SQLite chua cac bang:

- `NguoiDung`
- `CaiDat`
- `PhienLamViec`
- `NhatKyTuThe`
- `ThongKeNgay`
- `ThongTinModel`

Khi chay tu source, app su dung database trong thu muc `database`.
Nen sao luu file nay truoc khi muon reset du lieu demo.

Chi chay lenh sau khi that su muon tao lai database:

```powershell
python src/3_database_setup.py
```

## 8. Du lieu kem theo

Goi nop chi kem du lieu da trich xuat, khong kem video:

- `dataset/metadata/video_manifest.csv`
- `dataset/processed/posture_data_2fps_with_metadata.csv`
- `dataset/processed/posture_external_test_2fps_with_metadata.csv`

Day la cac CSV phuc vu kiem tra metadata, train va danh gia. Hai CSV
`combined_features` khong kem theo de giu file ZIP phu hop gui email; co
the tao lai bang cac script feature extraction trong `src/`. Video raw va
external video can duoc chia se bang Google Drive/OneDrive neu can.

## 9. Kiem tra source

Kiem tra cu phap:

```powershell
python -m compileall -q src
```

Chay test:

```powershell
python -m pytest tests
```

## 10. Loi thuong gap

| Loi | Cach xu ly |
|---|---|
| Khong mo duoc webcam | Dong Camera, Zoom, Teams; thu camera index `0` hoac `1`. |
| TensorFlow khong cai duoc | Dung Python 3.10/3.11 64-bit va tao lai `.venv`. |
| PowerShell chan activate | Dung `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`. |
| Video khong doc duoc | Chuyen video sang MP4 H.264; OpenCV co the khong ho tro HEVC/H.265 tren mot so may. |
| Khong co am thanh | Kiem tra loa va `assets/sounds/alarm.wav`. |
| App khoi dong cham | Lan dau TensorFlow va MediaPipe nap model co the mat nhieu thoi gian hon. |

## 11. Cau truc chinh

```text
src/                 Source code app, xu ly du lieu, train va danh gia
assets/              Am thanh canh bao
models/              Model ANN, scaler, registry va model HGB
database/            Co so du lieu SQLite demo
dataset/metadata/    Manifest video
dataset/processed/   CSV da xu ly
tests/               Automated tests
build_scripts/       Script dong goi ung dung desktop
../M-TT-*.doc         Ba bieu mau thuc tap nam ngang hang thu muc app
../*.pdf              Bao cao thuc tap nam ngang hang thu muc app
```
