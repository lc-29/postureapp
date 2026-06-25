# Feature Schema Final

Ngay cap nhat: 2026-05-28

## Muc tieu

Feature schema final chuan hoa cach tao dac trung cho train, benchmark, evaluation
va app. Muc tieu la tranh viec moi script tu chon feature khac nhau, dong thoi
lam ro dong gop khoa hoc cua do an: ket hop raw MediaPipe landmarks, normalized
landmarks va ergonomic geometric indicators.

## File chinh

| Artifact | Duong dan |
|---|---|
| Module feature schema | `src/feature_schema.py` |
| Schema final | `models/feature_schema_final.json` |
| Unit test | `tests/test_feature_schema.py` |

## Feature sets ho tro

| Feature set | So feature | Y nghia |
|---|---:|---|
| `raw_99` | 99 | 33 MediaPipe landmarks, moi diem gom x/y/z. |
| `normalized_99` | 99 | Raw landmarks duoc center theo shoulder midpoint va scale theo max shoulder width/torso length. |
| `ergonomic_14` | 14 | Cac chi bao geometric co kha nang giai thich tu the. |
| `combined_raw_ergonomic` | 113 | Raw landmarks + ergonomic indicators. |
| `combined_normalized_ergonomic` | 113 | Normalized landmarks + ergonomic indicators. |

## Ergonomic indicators

| Feature | Y nghia ergonomic |
|---|---|
| `shoulder_y_diff` | Lech doc giua hai vai. |
| `shoulder_tilt_angle` | Do nghieng cua duong vai. |
| `torso_lean_angle` | Do nghieng truc than tren. |
| `head_offset_x` | Do lech ngang cua mui so voi trung diem vai. |
| `nose_to_shoulder_y` | Vi tri doc cua mui so voi vai, ho tro phat hien cui/thu co. |
| `nose_shoulder_clearance_ratio` | Khoang cach mui-vai chuan hoa theo shoulder width. |
| `neck_compression_detected` | Co bao rui ro rut co sau. |
| `left_hand_mouth_ratio` | Khoang cach tay trai den mieng/cam chuan hoa. |
| `right_hand_mouth_ratio` | Khoang cach tay phai den mieng/cam chuan hoa. |
| `chin_rest_detected` | Co bao tay gan mieng/cam. |
| `shoulder_width` | Do rong vai trong anh. |
| `torso_length` | Do dai than tren proxy. |
| `head_shoulder_distance` | Khoang cach mui den trung diem vai. |
| `min_hand_mouth_ratio` | Khoang cach gan nhat giua tay va mieng/cam. |

## Ket qua lien quan

Feature schema moi da duoc dung trong `src/21_train_model_registry.py`. Ket qua
chon model final:

| Model | Feature set | Accuracy | F1 incorrect | MCC |
|---|---|---:|---:|---:|
| HistGradientBoosting | `normalized_99` | 95.959% | 96.284% | 91.893% |

Sau threshold calibration:

| Threshold | Accuracy | Precision incorrect | Recall incorrect | F1 incorrect |
|---:|---:|---:|---:|---:|
| 0.65 | 96.502% | 96.222% | 97.303% | 96.760% |

## Diem moi co the viet trong paper

Diem moi khong nam o MediaPipe landmarks, vi landmarks la cong cu co san. Diem
co the claim an toan la:

> The project uses a unified feature schema that compares raw pose landmarks,
> body-normalized landmarks, interpretable ergonomic geometric indicators, and
> combined feature sets under the same evaluation protocol.

Khong nen claim:

> MediaPipe landmarks are novel features.

