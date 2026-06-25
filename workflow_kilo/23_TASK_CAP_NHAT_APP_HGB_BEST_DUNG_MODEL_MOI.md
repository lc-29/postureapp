# 23_TASK_CAP_NHAT_APP_HGB_BEST_DUNG_MODEL_MOI

## Muc tieu

Cap nhat app desktop `src/4_main_desktop_app.py` de che do HistGradientBoosting trong app dung dung cac model hien co theo dung muc tieu:

1. `HistGradientBoosting (balanced best)`
   - Dung model moi tot nhat ve tong the tren external P06/P07.
   - Model: `hist_gradient_boosting__ergonomic_v2_with_view`
   - Feature set: `ergonomic_v2_with_view`
   - Threshold: `0.76`
   - Phu hop de bao cao ket qua khoa hoc vi can bang FP/FN tot hon.

2. `HistGradientBoosting (high recall demo)`
   - Dung model HGB cu ma app dang hard-code hien tai.
   - Model: `hist_gradient_boosting__normalized_99`
   - Feature set: `normalized_99`
   - Threshold: `0.50`
   - Phu hop demo realtime khi muc tieu la it bo sot tu the sai.

Khong xoa che do ANN. ANN van giu de doi chieu/baseline neural network, nhung khong nen dat lam model demo chinh neu ket qua external thap.

## Ly do can sua task theo huong 2 che do HGB

Ket qua so sanh tren external P06/P07:

| Model | Feature set | Threshold | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC | FP | FN |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| HGB high recall cu | `normalized_99` | 0.50 | 67.38% | 63.62% | 97.69% | 77.06% | 0.3785 | 1427 | 59 |
| HGB balanced moi | `ergonomic_v2_with_view` | 0.76 | 89.31% | 93.48% | 87.01% | 90.13% | 0.7875 | 155 | 332 |

Nhan xet:

- Model moi tot hon tong the: Accuracy, Precision, F1, MCC cao hon va FP giam manh.
- Model cu co Recall Incorrect cao hon, nen it bo sot tu the sai hon trong demo realtime.
- Rieng video `P07_incorrect_side_90_001.mp4`, model cu tot hon model moi.
- Vi demo hoi dong la demo realtime, can co che do high recall de khi nguoi demo co tinh sai tu the thi app bao sai ro rang.
- Vi bao cao khoa hoc can can bang FP/FN va khong bao nham qua nhieu, can co che do balanced best.

## Hien trang app truoc khi sua

Trong `src/4_main_desktop_app.py`, app hien dang:

- Co mode UI: `HistGradientBoosting (best)`.
- Hard-code:
  - `HGB_MODEL_ID = "hist_gradient_boosting__normalized_99"`
  - `HGB_MODEL_PATH = models/registry/hist_gradient_boosting__normalized_99/model.pkl`
  - `HGB_THRESHOLD_PATH = models/registry/hist_gradient_boosting__normalized_99/threshold.json`
- `predict_frame_hgb()` chi tao feature `normalized_99`.
- App chua dung model moi `hist_gradient_boosting__ergonomic_v2_with_view`.

Can sua de app co 2 mode HGB ro rang thay vi mot mode `best` gay nham lan.

## Nguyen tac bat buoc

- Khong xoa model cu.
- Khong ghi de ANN.
- Khong ghi de `models/ann_best.keras` va `models/scaler.pkl`.
- Khong thay doi ket qua bao cao bang tay.
- Khong lam ro ri du lieu external vao train.
- Khong ep mot model duy nhat cho moi muc tieu.
- Neu mode la `balanced best`, phai dung threshold registry/model threshold `0.76`.
- Neu mode la `high recall demo`, phai dung threshold cua model cu `0.50`, tru khi co calibration moi ro rang.
- Smoothing chi lam muot xac suat, khong duoc dung nham `smoothingThreshold` thay threshold model neu mode HGB da co threshold rieng.
- Neu source la video file, suy ra `view_angle` tu ten file.
- Neu source la webcam/IP camera, tam thoi dung `unknown` hoac them UI chon goc quay neu lam kip.

## Dau vao can doc

- `src/4_main_desktop_app.py`
- `src/feature_schema.py`
- `src/model_registry_service.py`
- `models/model_registry.json`
- `models/registry/hist_gradient_boosting__normalized_99/model.pkl`
- `models/registry/hist_gradient_boosting__normalized_99/threshold.json`
- `models/registry/hist_gradient_boosting__ergonomic_v2_with_view/model.pkl`
- `models/registry/hist_gradient_boosting__ergonomic_v2_with_view/threshold.json`
- `models/registry/hist_gradient_boosting__ergonomic_v2_with_view/feature_schema.json`
- `reports/MODEL_IMPROVEMENT_FP_REDUCTION_REPORT.md`
- `reports/ANN_LOCAL_REBUILD_REPORT.md`

## Dau ra bat buoc

- `src/4_main_desktop_app.py` co 2 che do HGB:
  - `HistGradientBoosting (balanced best)`
  - `HistGradientBoosting (high recall demo)`
- App van giu mode `ANN`.
- App van giu mode `Rule-based Baseline`.
- Report:
  - `reports/APP_HGB_MODE_UPDATE_REPORT.md`
- Neu them test:
  - `tests/test_app_hgb_modes.py` hoac test service tuong ung.

## Buoc 1. Doi ten va them mode UI

Trong danh sach mode combobox, cap nhat thanh:

- `ANN`
- `HistGradientBoosting (balanced best)`
- `HistGradientBoosting (high recall demo)`
- `Rule-based Baseline`

Khong nen giu ten `HistGradientBoosting (best)` mot minh vi de gay nham lan:

- `balanced best` la best theo metric tong the.
- `high recall demo` la best theo muc tieu demo canh bao sai tu the.

Neu muon tuong thich nguoi dung cu, co the map chuoi cu:

- `HistGradientBoosting (best)` => `HistGradientBoosting (balanced best)`

## Buoc 2. Tao cau hinh model HGB tap trung

Them cau truc cau hinh trong `4_main_desktop_app.py`, vi du:

```python
HGB_BALANCED_MODE_NAME = "HistGradientBoosting (balanced best)"
HGB_HIGH_RECALL_MODE_NAME = "HistGradientBoosting (high recall demo)"

HGB_MODE_CONFIGS = {
    HGB_BALANCED_MODE_NAME: {
        "model_id": "hist_gradient_boosting__ergonomic_v2_with_view",
        "feature_set": "ergonomic_v2_with_view",
    },
    HGB_HIGH_RECALL_MODE_NAME: {
        "model_id": "hist_gradient_boosting__normalized_99",
        "feature_set": "normalized_99",
    },
}
```

Duoc phep doc threshold tu file `threshold.json` cua tung model.

## Buoc 3. Sua ham nhan dien mode

Cap nhat:

- `is_hgb_mode()`
- `is_learned_model_mode()`
- cac noi so sanh `self.prediction_mode == HGB_MODE_NAME`

Yeu cau:

- `is_hgb_mode()` tra ve True neu mode nam trong `HGB_MODE_CONFIGS`.
- `is_learned_model_mode()` van True voi ANN hoac bat ky HGB mode nao.

## Buoc 4. Load model HGB theo mode duoc chon

Trong `load_ai_components()`:

- Neu mode HGB:
  - lay config theo `self.prediction_mode`
  - load `model.pkl` theo `model_id`
  - load `threshold.json`
  - luu:
    - `self.hgb_model`
    - `self.hgb_model_id`
    - `self.hgb_feature_set`
    - `self.hgb_threshold`

Neu co the, dung `model_registry_service.load_registry_model()` cho balanced best. Tuy nhien high recall demo can load theo model id cu, nen neu service chua ho tro model id tuy chon thi cap nhat service hoac load truc tiep an toan.

Yeu cau log console khi load:

```text
Dang load HGB mode: HistGradientBoosting (balanced best)
model_id=hist_gradient_boosting__ergonomic_v2_with_view
feature_set=ergonomic_v2_with_view
threshold=0.76
```

## Buoc 5. Tao frame DataFrame tu MediaPipe landmarks

Trong `predict_frame_hgb()`, sau khi co `results.pose_landmarks.landmark`:

1. Tao dict 1 dong gom 99 cot:
   - `landmark_0_x`, `landmark_0_y`, `landmark_0_z`
   - ...
   - `landmark_32_x`, `landmark_32_y`, `landmark_32_z`
2. Them metadata:
   - `source_video`
   - `frame_index`
   - `timestamp_sec`
   - `sample_fps`
   - `video_fps`
   - `participant_id`
   - `view_angle`
   - `camera_type`

Khong can `label` khi predict realtime.

## Buoc 6. Suy ra view_angle

Them ham:

```python
def infer_current_view_angle(self) -> str:
    ...
```

Logic:

- Neu source la video file:
  - ten file chua `side_90` => `side_90`
  - ten file chua `side_30` => `side_30`
  - ten file chua `front` => `front`
  - nguoc lai => `unknown`
- Neu webcam/IP camera:
  - tam thoi => `unknown`

Ghi limitation vao report:

- Khi webcam realtime dung `view_unknown`, model balanced v2 co the khac so voi video co view label.
- Neu muon demo webcam on hon voi balanced model, nen them combobox chon goc quay sau.

## Buoc 7. Predict bang feature_schema

Trong `predict_frame_hgb()`:

- Khong chi dung `build_normalized_landmark_vector()` nua.
- Dung:

```python
x, _ = build_feature_matrix(frame_df, self.hgb_feature_set)
raw_prob_incorrect = self.hgb_model.predict_proba(x)[0, 1]
```

Yeu cau:

- Neu `self.hgb_feature_set == "normalized_99"`, `build_feature_matrix()` tu tinh normalized.
- Neu `self.hgb_feature_set == "ergonomic_v2_with_view"`, `build_feature_matrix()` tu tinh ergonomic v2 va view one-hot.
- Neu model khong co `predict_proba`, fallback hop ly bang `predict`.

## Buoc 8. Tach threshold model va smoothing

Can tach:

- `raw_prob_incorrect`: xac suat model tra ve.
- `prob_incorrect`: xac suat sau lam muot.
- `model_threshold`: `self.hgb_threshold`.
- `smoothing_window_frames`: so frame lam muot.

Trong HGB mode:

```python
self.probability_window.append(raw_prob_incorrect)
prob_incorrect = mean(self.probability_window)
decision_threshold = self.hgb_threshold
predicted_label = 1 if prob_incorrect >= decision_threshold else 0
```

Khong dung `self.smoothing_threshold` lam threshold cho HGB, tru khi co setting rieng cho phep override va report ro.

## Buoc 9. Cap nhat UI/log nho neu can

Neu app co panel/thong tin mode, hien thi:

- Mode dang chay.
- Model id.
- Feature set.
- Threshold.

Khong can redesign UI lon trong task nay.

## Buoc 10. Test bang service/CSV truoc

Chay:

```powershell
.venv\Scripts\python.exe -m pytest tests\test_feature_schema.py tests\test_model_registry_service.py
```

Neu them test, kiem tra:

- Load duoc HGB balanced model.
- Load duoc HGB high recall model.
- Tao dataframe 1 row tu external CSV predict khong loi voi:
  - `normalized_99`
  - `ergonomic_v2_with_view`
- Threshold dung:
  - high recall: 0.50
  - balanced: 0.76

## Buoc 11. Test nhanh bang video va webcam

### 11.1 Test video high recall demo

Chay app:

```powershell
.venv\Scripts\python.exe src\4_main_desktop_app.py
```

Trong app:

1. Mode: `HistGradientBoosting (high recall demo)`.
2. Source:
   - `D:\posture_detection_app\dataset\external_videos\incorrect\P07_incorrect_side_90_001.mp4`
3. Ky vong:
   - App bao sai tu the tot hon ANN.
   - Console log dung model `hist_gradient_boosting__normalized_99`.

### 11.2 Test video balanced best

1. Mode: `HistGradientBoosting (balanced best)`.
2. Source:
   - chon mot video Correct side_90 truoc day HGB cu hay bao nham, vi du `P06_correct_side_90_001.mp4`.
3. Ky vong:
   - Giam bao nham tu the dung thanh sai.
   - Console log dung model `hist_gradient_boosting__ergonomic_v2_with_view`.

### 11.3 Test webcam realtime

1. Mode demo khuyen nghi: `HistGradientBoosting (high recall demo)`.
2. Lam cac tu the:
   - ngoi dung
   - cui co/dua dau ve truoc
   - nghieng nguoi
   - rut co sau
3. Ky vong:
   - Khi sai tu the ro rang, app bao sai nhanh.
   - Neu ngoi dung bi bao sai qua nhieu, can tang threshold/cooldown hoac dung balanced mode.

## Buoc 12. Tao report

Tao file:

- `reports/APP_HGB_MODE_UPDATE_REPORT.md`

Report gom:

1. Hien trang truoc khi sua.
2. Ly do khong chi dung mot HGB mode.
3. Bang so sanh HGB cu va HGB moi.
4. Mode moi trong app:
   - `balanced best`
   - `high recall demo`
5. Model id, feature set, threshold cua tung mode.
6. Cach suy ra `view_angle`.
7. Ket qua test service/pytest.
8. Ket qua test app/video neu co.
9. Khuyen nghi demo:
   - demo realtime: `HistGradientBoosting (high recall demo)`
   - bao cao khoa hoc: `HistGradientBoosting (balanced best)`
10. Gioi han con lai:
   - Webcam balanced mode dang dung `view_unknown` neu chua co UI chon goc quay.
   - ANN la baseline neural network, khong nen la model chinh trong demo neu chua cai thien.

## Checklist hoan thanh

- [ ] App co mode `HistGradientBoosting (balanced best)`.
- [ ] App co mode `HistGradientBoosting (high recall demo)`.
- [ ] App van giu mode `ANN`.
- [ ] App van giu mode `Rule-based Baseline`.
- [ ] Balanced mode load model `hist_gradient_boosting__ergonomic_v2_with_view`.
- [ ] Balanced mode dung feature set `ergonomic_v2_with_view`.
- [ ] Balanced mode dung threshold `0.76`.
- [ ] High recall mode load model `hist_gradient_boosting__normalized_99`.
- [ ] High recall mode dung feature set `normalized_99`.
- [ ] High recall mode dung threshold `0.50`.
- [ ] Video file suy ra dung `view_angle` tu ten file.
- [ ] Webcam/IP camera co fallback `view_unknown`.
- [ ] `predict_frame_hgb()` dung `build_feature_matrix()`.
- [ ] HGB mode khong dung nham `smoothingThreshold` lam threshold model.
- [ ] Test feature/model registry pass.
- [ ] Da tao report `APP_HGB_MODE_UPDATE_REPORT.md`.

