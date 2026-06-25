# BAO CAO DONG GOI SOURCE CODE

## Thong tin

- Sinh vien: Duong Ly Cu
- MSSV: 223650
- Lop: DH22TIN01
- Ngay dong goi: 06/06/2026
- Ten goi: `DUONGLYCU_223650_DH22TIN01.zip`

## Thanh phan da dua vao

- Source code trong `src/`.
- Am thanh canh bao trong `assets/`.
- Model ANN `ann_best.keras` va `scaler.pkl`.
- Model `hist_gradient_boosting__normalized_99` va threshold 0.65.
- Model registry va feature schema.
- Database SQLite demo `database/posture_app.db`.
- Manifest 94 video va hai CSV co metadata.
- Automated tests va build scripts.
- README cai dat, chay app va mo ta co so du lieu.
- Ba bieu mau M-TT-01, M-TT-02, M-TT-03.
- Bao cao thuc tap PDF cua sinh vien.

Ba bieu mau va PDF duoc dat o cap goc cua ZIP, ngang hang voi thu muc
`POSTURE_DETECTION_APP`.

## Ket qua kiem tra

- Compile source: dat.
- Automated tests: 27 passed, 1 skipped.
- ANN: nap thanh cong, input 99 features, output 1.
- Scaler: nap thanh cong, 99 features.
- HGB: nap thanh cong, feature set `normalized_99`, threshold 0.65.
- SQLite integrity check: `ok`.
- Development dataset: 11,022 dong.
- Corrected external dataset: 1,658 dong.

## Thanh phan da loai

- `.git/`, `.venv/`, `.pytest_cache/`, `__pycache__/`.
- `build/`, `dist/`, `release/`.
- Video raw va external video.
- Hai CSV `combined_features` co the tao lai tu CSV metadata bang source.
- Bao cao nghien cuu, file Word/PDF trung gian va ket qua render.
- Model benchmark khong duoc app demo su dung.
- Cac file ZIP cu.

Video goc co dung luong lon va can duoc chia se bang Drive neu giang vien
yeu cau kiem tra.
