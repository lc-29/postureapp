# Dataset Manifest

Ngay cap nhat: 2026-05-26

## Tong quan

| Hang muc | Gia tri |
|---|---:|
| Raw train videos - correct | 34 |
| Raw train videos - incorrect | 50 |
| External videos - correct | 5 |
| External videos - incorrect | 5 |
| Train CSV | `dataset/posture_data_2fps.csv` |
| Train CSV rows | 11022 |
| Train CSV columns | 100 |
| External CSV | `dataset/posture_external_test_2fps.csv` |
| External CSV rows | 1697 |
| External CSV columns | 100 |
| Feature columns | 99 landmark features |
| Label column | `label` (`0=correct`, `1=incorrect`) |

## Label distribution

| Dataset | Correct (`0`) | Incorrect (`1`) |
|---|---:|---:|
| Train CSV | 4438 | 6584 |
| External CSV | 768 | 929 |

## Feature schema

Moi mau gom 33 MediaPipe Pose landmarks. Moi landmark co 3 toa do:

- `landmark_N_x`
- `landmark_N_y`
- `landmark_N_z`

CSV co cot `label` o cuoi. CSV hien tai chua co `source_video` va `frame_index`, nen chua the danh gia video-wise/person-wise mot cach kiem chung.

## Can bo sung thu cong

| Thong tin | Trang thai | Ghi chu |
|---|---|---|
| So nguoi tham gia | Can bo sung | Can tach ro train/external neu co. |
| Tuoi/gioi tinh/chieu cao | Can bo sung | Chi ghi neu co dong y va can cho bao cao. |
| Thiet bi camera | Can bo sung | Webcam/laptop/phone, model neu biet. |
| Do phan giai video | Can bo sung | Co the lay bang OpenCV/ffprobe. |
| FPS goc | Can bo sung | CSV duoc sample ve 2 FPS. |
| Dieu kien anh sang | Can bo sung | Sang/toi/nguoc sang. |
| Goc quay | Mot phan trong ten file | Front, side 30, side 90. |
| Cach gan nhan | Can mo ta | Dinh nghia correct/incorrect va nguoi gan nhan. |
| Tieu chi loai frame | Can mo ta | Vi du khong co pose/visibility thap. |

## Rui ro du lieu

- Split hien tai co nguy co frame leakage neu train/test chia theo frame.
- Chua co cot video/person id trong CSV chinh.
- Video raw khong nam trong Git do gioi han dung luong; can luu dataset goc bang Git LFS, cloud storage hoac o cung backup.
