# Baseline Rule QA

Ngay cap nhat: 2026-05-27

## Neck-compression rule

Rule baseline moi tach rieng tinh huong mui gan ngang vai/rut co qua sau:

```text
vertical_clearance = mid_shoulder_y - nose_y
torso_height = mid_hip_y - mid_shoulder_y
nose_shoulder_clearance_ratio = vertical_clearance / torso_height
neck_compression_detected = nose_shoulder_clearance_ratio < 0.12
```

Luu y: toa do MediaPipe co truc `y` tang tu tren xuong duoi. Khi mui thap gan bang vai, `vertical_clearance` va ratio se nho.

## Unit test da co

| Case | File test | Ky vong |
|---|---|---|
| Tu the dung mac dinh | `tests/test_posture_baseline.py` | `CORRECT` |
| Rut co vua, mui van cao hon vai du ro | `test_rule_based_moderate_neck_compression_still_correct` | `CORRECT` |
| Rut co sau, mui gan ngang vai | `test_rule_based_deep_neck_compression_incorrect` | `INCORRECT` |
| Dau lech ngang | `test_rule_based_head_offset_incorrect` | `INCORRECT` |
| Tay gan mieng/chong cam | `test_rule_based_hand_near_mouth_incorrect` | `INCORRECT` |
| Visibility thap | `test_rule_based_low_visibility_no_person` | `NO_PERSON_OR_LOW_CONFIDENCE` |

Verify:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_posture_baseline.py -q
```

Ket qua lan gan nhat:

```text
7 passed
```

## Manual QA can lam

- Chay app o Rule-based mode.
- Dung webcam/video co tu the binh thuong.
- Thu rut co nhe/vua: app khong nen bao sai neu vai/than/dau/tay van dung.
- Thu rut co sau den khi mui gan ngang vai: app nen bao sai voi warning `"Mui gan ngang vai / rut co qua sau"`.
- Kiem tra baseline panel co hien:
  - `mui so voi vai y`
  - `khoang cach mui-vai ti le`
  - `rut co sau`

