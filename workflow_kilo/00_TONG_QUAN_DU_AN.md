# 00. Tong quan du an Posture Detection App

Ngay quet: 2026-05-26

## Muc tieu du an

Xay dung ung dung desktop phat hien loi tu the lam viec qua webcam, camera IP hoac video file. Pipeline hien tai:

OpenCV -> MediaPipe Pose -> 33 landmarks -> 99 dac trung `(x, y, z)` -> Rule-based baseline hoac ANN -> canh bao realtime -> luu SQLite -> thong ke ngay.

## Cau truc hien tai

| Thu muc/file | Vai tro |
|---|---|
| `src/1_rule_based_baseline.py` | Baseline rule-based chay rieng qua OpenCV, co overlay debug va canh bao sai tu the. |
| `src/2_extract_features.py` | Trich xuat 33 landmark MediaPipe Pose tu video thanh CSV 99 feature + label. |
| `src/3_database_setup.py` | Tao lai SQLite schema tieng Viet, du lieu mac dinh, smoke test database. |
| `src/4_main_desktop_app.py` | Ung dung CustomTkinter realtime: ANN, baseline mode, logging, thong ke, am thanh. |
| `src/5_train_ann_local.py` | Train ANN tu CSV, luu model/scaler/metrics/report/confusion matrix/curves. |
| `src/config.py` | Cau hinh duong dan va nguong canh bao chung. |
| `src/utils.py` | Ham tinh goc co ban. |
| `dataset/raw_videos` | Du lieu video train: `correct` va `incorrect`. |
| `dataset/external_videos` | Du lieu external test: `correct` va `incorrect`. |
| `dataset/posture_data_2fps.csv` | CSV train hien tai. |
| `dataset/posture_external_test_2fps.csv` | CSV external test hien tai. |
| `models/ann_best.keras`, `models/scaler.pkl` | Model/scaler dang duoc app dung. |
| `models/local_training` | Ket qua train local va artifacts danh gia. |
| `database/posture_app.db` | SQLite database cua app. |
| `tests` | Test thu cong/import, chua that su la automated test suite tot. |

## So lieu du lieu va model hien tai

| Hang muc | Gia tri |
|---|---:|
| Raw video train correct | 34 video |
| Raw video train incorrect | 50 video |
| External video correct | 5 video |
| External video incorrect | 5 video |
| CSV train | 11.022 mau, 100 cot |
| Feature moi mau | 99 feature landmark |
| Label train `0/correct` | 4.438 mau |
| Label train `1/incorrect` | 6.584 mau |
| CSV external test | 1.697 mau |
| Label external `0/correct` | 768 mau |
| Label external `1/incorrect` | 929 mau |
| ANN test accuracy local | 0,998186 |
| ANN test precision class incorrect | 0,998987 |
| ANN test recall class incorrect | 0,997976 |
| ANN test F1 class incorrect | 0,998481 |
| Confusion matrix local | `[[665, 1], [2, 986]]` |

## Chuc nang da co

- Mo nguon video tu webcam, camera IP hoac file video.
- Trich xuat landmark MediaPipe Pose thanh vector 99 feature.
- Hai che do danh gia tu the:
  - ANN binary classifier.
  - Rule-based baseline voi cac chi so: lech vai, nghieng vai, nghieng than, dau lech truc vai, cui dau, tay gan mieng/chong cam.
- GUI CustomTkinter dark mode.
- Canh bao am thanh khi sai tu the lien tuc qua nguong.
- Ghi nhan phien lam viec, nhat ky, thong ke ngay vao SQLite.
- Bieu do thong ke bang matplotlib, co fallback neu thieu matplotlib.
- Train ANN local co train/validation/test split, class weight, early stopping, checkpoint, confusion matrix, classification report.

## Diem manh de dua vao bao cao

- He thong end-to-end hoan chinh tu thu thap video den ung dung realtime.
- Ket hop baseline cong thai hoc co the giai thich voi ANN hoc tu landmark.
- Du lieu rieng co nhieu goc quay: front, side 30, side 90.
- Co external test set rieng de danh gia kha nang tong quat hoa.
- Co logging SQLite va thong ke hanh vi lam viec theo phien/ngay, phu hop bai toan ung dung.

## Rui ro/khoang trong hien tai

- Ten file Python bat dau bang so gay kho import/test va lam app phai copy logic baseline thay vi import truc tiep.
- `README.md`, `config.py`, `utils.py`, mot so test va comment database bi loi encoding tieng Viet.
- Logic baseline bi trung lap giua `1_rule_based_baseline.py` va `4_main_desktop_app.py`.
- Test hien tai co file mo webcam o top-level, khong phu hop `pytest` tu dong.
- Metrics local rat cao, co nguy co data leakage theo frame/video/person neu split ngau nhien tung frame.
- Chua co subject-wise/video-wise split de bao cao nghien cuu nghiem tuc.
- Chua co script danh gia external test chuan hoa thanh bang metrics rieng.
- Chua co dataset manifest ghi ro nguoi tham gia, goc quay, thoi luong, dieu kien anh sang, cach gan nhan.
- Chua co benchmark day du giua rule-based, ANN, external test, ablation feature.
- Chua co packaging/huong dan cai dat hoan thien cho nguoi khac tai lap.

## Ket luan quet nhanh

Du an da vuot qua muc prototype don le: co pipeline du lieu, model, ung dung realtime, database va thong ke. De dat muc "hoan thanh" va co the viet bao cao khoa hoc theo dinh dang Springer, can uu tien:

1. Lam sach tai lieu/encoding va cau truc repo.
2. Tach logic baseline dung chung de tranh trung lap.
3. Tao automated tests khong can webcam.
4. Bo sung danh gia video-wise/person-wise va external test.
5. Viet report theo Springer voi bang so lieu, quy trinh tai lap va gioi han ro rang.
