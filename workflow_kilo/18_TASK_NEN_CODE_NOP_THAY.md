# 18_TASK_NEN_CODE_NOP_THAY

## Muc tieu

Tao goi nen source code phan mem kem file PDF bao cao de nop cho thay huong dan qua email/Drive.

Goi nen phai:

- Du de thay xem source code va chay app demo.
- Co model/scaler can thiet.
- Co model tot nhat `hist_gradient_boosting__normalized_99` da them vao app demo.
- Co database demo va dataset da xu ly dang CSV neu dung luong hop ly.
- Co file PDF bao cao thuc tap/bao cao de nop thay.
- Khong chua moi truong ao, git history, build cache, raw video nang, release exe nang, hay bao cao nghien cuu da nen rieng.

Ten file nen khuyen nghi:

```text
DUONG_LY_CU_223650_CODE_VA_BAOCAO_THUCTAP.zip
```

Thu muc dau ra khuyen nghi:

```text
D:\LUẬN VĂN 2026\CA_NHAN\BAOCAOTHUCTAP\
```

Duong dan zip cuoi:

```text
D:\LUẬN VĂN 2026\CA_NHAN\BAOCAOTHUCTAP\DUONG_LY_CU_223650_CODE_VA_BAOCAO_THUCTAP.zip
```

---

## Boi canh du an

Project goc:

```text
D:\posture_detection_app
```

App chinh:

```text
src/4_main_desktop_app.py
```

App hien co 3 mode:

```text
ANN
HistGradientBoosting (best)
Rule-based Baseline
```

Model ANN app:

```text
models/ann_best.keras
models/scaler.pkl
```

Model tot nhat theo benchmark:

```text
models/registry/hist_gradient_boosting__normalized_99/
```

File PDF bao cao can nen chung:

```text
D:\LUáº¬N VÄ‚N 2026\CA_NHAN\BAOCAOTHUCTAP\DÆ°Æ¡ng LÃ½ Cá»­_223650_DH22TIN01_BAOCAOTHUCTAP.pdf
```

Trong staging nen copy vao:

```text
bao_cao/DÆ°Æ¡ng LÃ½ Cá»­_223650_DH22TIN01_BAOCAOTHUCTAP.pdf
```

---

## Nguyen tac nen file

### Nen dua vao goi zip

| Thanh phan | Bat buoc | Ghi chu |
|---|---:|---|
| `src/` | Co | Source code chinh cua app va cac script lien quan |
| `assets/` | Co | Am thanh canh bao/icon neu co |
| `models/ann_best.keras` | Co | Model ANN dang dung trong app |
| `models/scaler.pkl` | Co | Scaler bat buoc cho ANN |
| `models/feature_schema_final.json` | Co | Schema dac trung |
| `models/model_registry.json` | Co | Registry model benchmark |
| `models/registry/hist_gradient_boosting__normalized_99/` | Co | Model HGB tot nhat da them vao app |
| `database/posture_app.db` | Co neu ton tai | Database demo de xem lich su/thong ke |
| `dataset/metadata/video_manifest.csv` | Co | Manifest video/metadata |
| `dataset/processed/*.csv` | Co neu dung luong hop ly | CSV da xu ly, khong phai video raw |
| `tests/` | Co | Test va kiem tra logic |
| `README.md` | Co | Mo ta project |
| `requirements.txt` | Co | Thu vien chay source |
| `requirements-build.txt` | Co neu ton tai | Thu vien build app |
| `run_app.bat` | Co neu ton tai | Chay nhanh tren Windows |
| `build_scripts/` | Tuy chon | Neu muon thay xem cach build exe |
| `reports/GOI_NOP_CODE_PHAN_MEM_CHO_THAY.md` | Co | Huong dan goi nop code |
| `bao_cao/DÆ°Æ¡ng LÃ½ Cá»­_223650_DH22TIN01_BAOCAOTHUCTAP.pdf` | Co | File PDF bao cao chinh de nop thay |

### Khong dua vao goi zip

| Thanh phan | Ly do |
|---|---|
| `.git/` | Lich su git khong can thiet, nang |
| `.venv/` | Moi truong ao rat nang, co the cai lai bang `requirements.txt` |
| `.pytest_cache/` | Cache test |
| `__pycache__/` | Cache Python |
| `build/` | Build trung gian |
| `dist/` | Ban exe build san, khong can neu nop source code |
| `release/` | Ban release nang, chi gui rieng neu thay yeu cau |
| `dataset/raw_videos/` | Video raw rat nang |
| `dataset/external_videos/` | Video external nang |
| `reports/springer_overleaf/` | Thuoc goi bao cao, khong phai goi source code |
| `reports/*.pdf` | Bao cao trong project khong can dua vao, vi chi copy dung file PDF bao cao chinh o `D:\LUáº¬N VÄ‚N 2026\...` |
| `reports/*.docx` | Bao cao da nen rieng |
| `reports/results/*.csv` lon | Chi dua neu that su can, khong bat buoc cho app demo |
| `*.zip` cu | Tranh nen long nhau |
| `*.tmp`, `~$*.docx` | File tam |

---

## Cac buoc thuc thi

### Buoc 1. Kiem tra nhanh trang thai project

Chay:

```powershell
cd D:\posture_detection_app
Get-ChildItem -Force
```

Kiem tra cac file/to thu muc bat buoc ton tai:

```text
src/4_main_desktop_app.py
assets/
models/ann_best.keras
models/scaler.pkl
models/model_registry.json
models/registry/hist_gradient_boosting__normalized_99/model.pkl
models/registry/hist_gradient_boosting__normalized_99/threshold.json
database/posture_app.db
README.md
requirements.txt
D:\LUẬN VĂN 2026\CA_NHAN\BAOCAOTHUCTAP\Dương Lý Cử_223650_DH22TIN01_BAOCAOTHUCTAP.pdf
```

Neu thieu file bat buoc, dung lai va bao ro file nao thieu.

Lenh kiem tra rieng file PDF bao cao:

```powershell
Test-Path "D:\LUẬN VĂN 2026\CA_NHAN\BAOCAOTHUCTAP\Dương Lý Cử_223650_DH22TIN01_BAOCAOTHUCTAP.pdf"
Get-Item "D:\LUẬN VĂN 2026\CA_NHAN\BAOCAOTHUCTAP\Dương Lý Cử_223650_DH22TIN01_BAOCAOTHUCTAP.pdf" |
  Select-Object FullName, Length, LastWriteTime
```

### Buoc 2. Kiem tra app source co compile duoc

Chay:

```powershell
.\.venv\Scripts\python.exe -m py_compile src/4_main_desktop_app.py
```

Neu `.venv` khong ton tai, co the dung:

```powershell
python -m py_compile src/4_main_desktop_app.py
```

Yeu cau:

- Khong co syntax error.
- Khong can mo GUI app trong task nay.

### Buoc 3. Tao thu muc staging

Tao thu muc tam:

```text
D:\LUẬN VĂN 2026\CA_NHAN\BAOCAOTHUCTAP\DUONG_LY_CU_223650_CODE_VA_BAOCAO_THUCTAP/
```

Neu thu muc da ton tai, xoa rieng thu muc staging nay truoc khi tao lai. Khong xoa thu muc project goc.

### Buoc 4. Copy cac thanh phan can nop vao staging

Copy cac thu muc/file sau:

```text
src/
assets/
tests/
build_scripts/
README.md
requirements.txt
requirements-build.txt
run_app.bat
reports/GOI_NOP_CODE_PHAN_MEM_CHO_THAY.md
```

Copy model can thiet:

```text
models/ann_best.keras
models/scaler.pkl
models/feature_schema_final.json
models/model_registry.json
models/registry/hist_gradient_boosting__normalized_99/
```

Copy database demo:

```text
database/posture_app.db
```

Copy dataset nhe:

```text
dataset/metadata/video_manifest.csv
dataset/processed/posture_data_2fps_with_metadata.csv
dataset/processed/posture_data_2fps_combined_features.csv
dataset/processed/posture_external_test_2fps_with_metadata.csv
dataset/processed/posture_external_test_2fps_combined_features.csv
```

Neu cac CSV processed qua nang voi email, van co the giu trong zip gui Drive. Neu can gui email truc tiep, tao ban nhe hon khong co `dataset/processed/*.csv` va ghi ro trong README.

Copy file PDF bao cao chinh vao staging:

```text
bao_cao/Dương Lý Cử_223650_DH22TIN01_BAOCAOTHUCTAP.pdf
```

Nguon copy:

```text
D:\LUẬN VĂN 2026\CA_NHAN\BAOCAOTHUCTAP\Dương Lý Cử_223650_DH22TIN01_BAOCAOTHUCTAP.pdf
```

Yeu cau:

- Phai copy dung file PDF tren, khong copy ca thu muc `D:\LUáº¬N VÄ‚N 2026`.
- Khong doi noi dung PDF.
- Co the giu nguyen ten file tieng Viet co dau.

### Buoc 5. Tao README nop tháº§y rieng trong staging

Tao file:

```text
D:\LUẬN VĂN 2026\CA_NHAN\BAOCAOTHUCTAP\DUONG_LY_CU_223650_CODE_VA_BAOCAO_THUCTAP/HUONG_DAN_CHAY_DEMO.txt
```

Noi dung can co:

```text
HUONG DAN CHAY DEMO

1. Cai Python 3.10 hoac 3.11.
2. Mo PowerShell tai thu muc nay.
3. Tao moi truong ao:
   python -m venv .venv

4. Kich hoat:
   .\.venv\Scripts\activate

5. Cai thu vien:
   pip install -r requirements.txt

6. Chay app:
   python src/4_main_desktop_app.py

Che do trong app:
- ANN
- HistGradientBoosting (best)
- Rule-based Baseline

Ghi chu:
- File PDF bao cao nam trong thu muc bao_cao/.
- Thu muc nay khong kem video raw vi dung luong lon.
- Neu can xem video goc, vui long dung link Drive rieng.
```

### Buoc 6. Nen zip

Tao zip:

```powershell
Compress-Archive `
  -Path "D:\LUẬN VĂN 2026\CA_NHAN\BAOCAOTHUCTAP\DUONG_LY_CU_223650_CODE_VA_BAOCAO_THUCTAP" `
  -DestinationPath "D:\LUẬN VĂN 2026\CA_NHAN\BAOCAOTHUCTAP\DUONG_LY_CU_223650_CODE_VA_BAOCAO_THUCTAP.zip" `
  -Force
```

### Buoc 7. Kiem tra zip sau khi tao

Kiem tra zip ton tai:

```powershell
Test-Path "D:\LUẬN VĂN 2026\CA_NHAN\BAOCAOTHUCTAP\DUONG_LY_CU_223650_CODE_VA_BAOCAO_THUCTAP.zip"
```

Kiem tra dung luong:

```powershell
Get-Item "D:\LUẬN VĂN 2026\CA_NHAN\BAOCAOTHUCTAP\DUONG_LY_CU_223650_CODE_VA_BAOCAO_THUCTAP.zip" |
  Select-Object FullName, Length, LastWriteTime
```

Liet ke nhanh noi dung zip:

```powershell
Add-Type -AssemblyName System.IO.Compression.FileSystem
[IO.Compression.ZipFile]::OpenRead("D:\LUẬN VĂN 2026\CA_NHAN\BAOCAOTHUCTAP\DUONG_LY_CU_223650_CODE_VA_BAOCAO_THUCTAP.zip").Entries |
  Select-Object -First 80 FullName
```

Yeu cau kiem tra:

- Co `src/4_main_desktop_app.py`.
- Co `models/ann_best.keras`.
- Co `models/scaler.pkl`.
- Co `models/registry/hist_gradient_boosting__normalized_99/model.pkl`.
- Co `database/posture_app.db`.
- Co `bao_cao/DÆ°Æ¡ng LÃ½ Cá»­_223650_DH22TIN01_BAOCAOTHUCTAP.pdf`.
- Co `requirements.txt`.
- Co `HUONG_DAN_CHAY_DEMO.txt`.
- Khong co `.venv/`.
- Khong co `.git/`.
- Khong co `build/`.
- Khong co `dist/`.
- Khong co `release/`.
- Khong co `dataset/raw_videos/`.
- Khong co `dataset/external_videos/`.

### Buoc 8. Tao bao cao xac nhan

Tao file:

```text
D:\LUẬN VĂN 2026\CA_NHAN\BAOCAOTHUCTAP\ZIP_CODE_SUBMISSION_REPORT.md
```

Noi dung can co:

- Ten zip da tao.
- Duong dan zip.
- Dung luong zip.
- Danh sach thanh phan chinh da dua vao.
- Ten va duong dan file PDF bao cao da dua vao.
- Danh sach thanh phan da loai tru.
- Ket qua check `py_compile`.
- Ghi chu: video raw khong kem theo, gui Drive neu thay can.

---

## Ket qua can dat

Sau khi thuc thi task nay, phai co:

```text
D:\LUẬN VĂN 2026\CA_NHAN\BAOCAOTHUCTAP\DUONG_LY_CU_223650_CODE_VA_BAOCAO_THUCTAP.zip
D:\LUẬN VĂN 2026\CA_NHAN\BAOCAOTHUCTAP\ZIP_CODE_SUBMISSION_REPORT.md
```

Zip phai la goi code demo kem PDF bao cao, gon, dung trong tam, khong kem video raw va khong kem moi truong ao.

---

## Cau tra loi cuoi cung can bao cho nguoi dung

Sau khi thuc thi xong, tra loi ngan gon:

```text
Da tao xong goi code + bao cao nop thay:
D:\LUẬN VĂN 2026\CA_NHAN\BAOCAOTHUCTAP\DUONG_LY_CU_223650_CODE_VA_BAOCAO_THUCTAP.zip

Goi nay co source code, model ANN, scaler, model HGB tot nhat, database demo,
processed metadata/CSV, requirements, huong dan chay va file PDF bao cao:
bao_cao/Dương Lý Cử_223650_DH22TIN01_BAOCAOTHUCTAP.pdf.
Khong kem .venv, .git, build/dist/release va video raw/external de tranh qua nang.
```

