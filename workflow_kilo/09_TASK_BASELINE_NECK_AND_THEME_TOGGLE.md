# 09. Task baseline neck posture va theme toggle

Ngay cap nhat: 2026-05-27

Pham vi phan tich:

- `src/posture_baseline.py`
- `tests/test_posture_baseline.py`
- `src/4_main_desktop_app.py`
- `src/3_database_setup.py`
- `reports/GUI_QA_CHECKLIST.md`

## Ket luan nhanh

Co 2 yeu cau moi:

1. Kiem tra lai rule baseline `mui so voi vai` de phan biet:
   - Rut co nhe/vua: van tinh la tu the dung.
   - Rut co qua sau, mui thap gan ngang vai: tinh la sai tu the.
2. Them nut/chon che do de nguoi dung doi qua lai Light mode va Dark mode.

## Phan tich baseline hien tai

Trong `src/posture_baseline.py`:

```python
NOSE_TO_SHOULDER_Y_THRESHOLD = -0.03
nose_to_shoulder_y = nose.y - mid_shoulder_y

if float(features["nose_to_shoulder_y"]) > NOSE_TO_SHOULDER_Y_THRESHOLD:
    warnings.append("Co dau hieu cui dau")
```

Luu y he toa do:

- MediaPipe image coordinate co `y` tang tu tren xuong duoi.
- `nose_to_shoulder_y` am nhieu: mui nam cao hon vai nhieu, thuong la dung.
- `nose_to_shoulder_y` gan `0`: mui gan ngang vai, co the la rut co/cui dau sau.
- `nose_to_shoulder_y` duong: mui thap hon vai, gan nhu chac chan sai.

Voi nguong hien tai `-0.03`:

| Vi du | Y nghia | Rule hien tai |
|---:|---|---|
| `-0.09` | Mui cao hon vai ro | Correct neu khong co loi khac |
| `-0.04` | Rut co/cui nhe-vua | Correct |
| `-0.02` | Mui rat gan vai | Incorrect |
| `0.00` | Mui ngang vai | Incorrect |

Nhu vay logic hien tai ve mat y tuong da gan voi yeu cau cua nguoi dung, nhung con 3 van de:

1. Chua co unit test cho case rut co vua van dung va rut co sau la sai.
2. Nguong tuyet doi `-0.03` co the khong on dinh giua nguoi cao/thap, camera gan/xa, vai rong/hep.
3. Ten warning `"Co dau hieu cui dau"` chua dung voi truong hop rut co sau; nen doi thanh thong diep ro hon, vi day khong phai luc nao cung la cui dau.

## Phan tich theme hien tai

Sau dot UI truoc:

- App dang mac dinh `ctk.set_appearance_mode("light")`.
- Mau UI gom trong `THEME`.
- Nhung `THEME` hien la mot palette light co dinh, chua co dark palette.
- Chua co control trong sidebar de doi theme.
- Chua co truong database de luu theme nguoi dung da chon.

Can lam theo huong an toan:

- Them theme manager nho trong `4_main_desktop_app.py`.
- Ho tro `light` va `dark` palette.
- Them segmented button/switch trong sidebar.
- Khi doi theme, apply lai cac widget chinh va chart/table style.
- Neu co the, luu `cheDoGiaoDien` vao bang `CaiDat`; neu muon it rui ro, co the chi runtime truoc, persist sau.

## Quy trinh lam

Lam theo thu tu:

1. Them test baseline cho cac muc rut co.
2. Chinh rule/nguong baseline sau khi test mo ta dung hanh vi.
3. Dong bo app GUI neu `4_main_desktop_app.py` van con ban copy baseline.
4. Them theme toggle runtime.
5. Neu runtime on, them persist vao database.
6. Cap nhat QA.

Quy uoc trang thai:

- `Todo`: chua lam.
- `Doing`: dang lam.
- `Blocked`: can video/camera/manual QA.
- `Done`: da verify.

## Backlog task tuan tu

### TASK-069 - Them test baseline cho rut co vua va rut co sau

Uu tien: P0

Trang thai: Done

Muc tieu: khoa hanh vi mong muon truoc khi doi nguong.

Pham vi:

- `tests/test_posture_baseline.py`

Cach lam:

1. Dung `make_landmarks()` hien co.
2. Them case `rut co vua`:
   - Vai giu `y=0.42`.
   - Nose co the dat `y=0.37` hoac `0.38`.
   - Ky vong: `CORRECT` neu khong co loi khac.
3. Them case `rut co sau / mui gan vai`:
   - Vai giu `y=0.42`.
   - Nose dat `y=0.405` hoac `0.415`.
   - Ky vong: `INCORRECT`.
   - Warning nen chua tu khoa `co`, `rut`, `cui`, hoac thong diep moi.
4. Them assert cho feature `nose_to_shoulder_y` de de debug.

Verify:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_posture_baseline.py -q
```

Done khi:

- Test moi mo ta ro rut co vua dung, rut co sau sai.

Bang chung: da them 2 test trong `tests/test_posture_baseline.py`; `7 passed`.

### TASK-070 - Chuan hoa rule `nose_to_shoulder_y` thanh neck-compression rule

Uu tien: P0

Trang thai: Done

Muc tieu: rule phan biet rut co/cui dau sau ro hon, it phu thuoc scale camera hon.

Pham vi:

- `src/posture_baseline.py`
- `tests/test_posture_baseline.py`

Cach lam:

1. Giu feature cu `nose_to_shoulder_y` de khong lam hong UI/debug.
2. Them feature moi de de giai thich, vi du:
   - `nose_shoulder_clearance`
   - `nose_shoulder_clearance_ratio`
   - `neck_compression_detected`
3. Tinh ratio theo kich thuoc co the on dinh hon:
   - `vertical_clearance = mid_shoulder_y - nose.y`
   - `torso_height = mid_hip_y - mid_shoulder_y`
   - `clearance_ratio = vertical_clearance / torso_height`
4. Dat nguong de rut co vua van dung, rut co sau sai. Goi y ban dau:
   - `MIN_NOSE_SHOULDER_CLEARANCE_RATIO = 0.12`
   - Neu `clearance_ratio < 0.12` thi sai.
5. Doi warning tu `"Co dau hieu cui dau"` thanh ro hon:
   - `"Mui gan ngang vai / rut co qua sau"`
6. Ghi comment ngan ve he toa do `y` tang xuong duoi.

Verify:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_posture_baseline.py -q
python -m py_compile src/posture_baseline.py
```

Done khi:

- Test baseline pass.
- Rut co vua khong bi flag sai.
- Rut co sau gan ngang vai bi flag sai.

Bang chung: `src/posture_baseline.py` co `nose_shoulder_clearance_ratio` va `neck_compression_detected`.

### TASK-071 - Dong bo GUI voi baseline module duy nhat

Uu tien: P0

Trang thai: Done

Muc tieu: dam bao app dung rule baseline moi, khong dung ban copy cu trong `4_main_desktop_app.py`.

Pham vi:

- `src/4_main_desktop_app.py`
- `src/posture_baseline.py`

Ly do:

- Hien `src/4_main_desktop_app.py` van co nhieu constant/function baseline duplicate nhu `NOSE_TO_SHOULDER_Y_THRESHOLD`, `extract_posture_features`, `classify_posture_rule_based`.
- Neu chi sua `src/posture_baseline.py` ma GUI van goi ban copy cu, app co the khong thay doi hanh vi.

Cach lam:

1. Tim cac function/constant baseline duplicate trong `4_main_desktop_app.py`.
2. Xac dinh ham `predict_frame_rule_based` dang goi ban nao.
3. Import ro rang tu `posture_baseline.py`:
   - `extract_posture_features`
   - `classify_posture_rule_based`
4. Xoa hoac rename ban duplicate trong GUI de tranh shadow import.
5. Cap nhat baseline info panel de hien feature moi:
   - `nose_shoulder_clearance_ratio`
   - `neck_compression_detected`
6. Khong doi ANN mode trong task nay.

Verify:

```powershell
python -m py_compile src/4_main_desktop_app.py src/posture_baseline.py
.\.venv\Scripts\python.exe -m pytest tests/test_posture_baseline.py -q
```

Manual verify:

- Chay app Rule-based mode voi video/webcam.
- Baseline panel hien feature moi.

Done khi:

- GUI rule-based dung module baseline chung.
- Khong con rui ro sua module baseline nhung GUI khong doi.

Bang chung: `src/4_main_desktop_app.py` import `create_default_features`, `extract_posture_features`, `classify_posture_rule_based` tu `posture_baseline.py`; baseline panel hien feature moi.

### TASK-072 - Them regression test cho compare algorithms neu baseline doi

Uu tien: P1

Trang thai: Done

Muc tieu: doi rule baseline khong lam script so sanh ANN vs rule-based bi vo.

Pham vi:

- `src/8_compare_algorithms.py`
- Co the them `tests/test_compare_algorithms_smoke.py`

Cach lam:

1. Tao test smoke nho voi DataFrame 1-2 row landmark gia lap.
2. Goi `landmarks_from_feature_row` va `classify_posture_rule_based`.
3. Dam bao feature moi khong lam script crash.

Verify:

```powershell
python -m py_compile src/8_compare_algorithms.py
.\.venv\Scripts\python.exe -m pytest tests/test_posture_baseline.py -q
```

Done khi:

- Doi baseline khong pha evaluation script.

Bang chung: da them `tests/test_compare_algorithms_smoke.py`; `tests/test_compare_algorithms_smoke.py tests/test_posture_baseline.py` pass.

### TASK-073 - Tao dark palette va theme manager

Uu tien: P0

Trang thai: Done

Muc tieu: ho tro light/dark mode dung cung design token, khong hard-code rieng tung widget.

Pham vi:

- `src/4_main_desktop_app.py`
- Co the tao `src/ui_theme.py` neu muon tach file

Cach lam:

1. Doi `THEME` thanh `THEMES = {"light": {...}, "dark": {...}}`.
2. Them `self.current_theme_mode = "light"`.
3. Them helper:
   - `get_theme()`
   - `set_theme_mode(mode)`
   - `apply_theme_to_existing_widgets()`
4. Dark palette can doc duoc:
   - `app_bg`: `#0f172a`
   - `surface`: `#111827`
   - `surface_muted`: `#1f2937`
   - `surface_subtle`: `#172033`
   - `border`: `#334155`
   - `text`: `#f8fafc`
   - `muted`: `#cbd5e1`
5. Chua can persist database trong task nay; chi runtime.

Verify:

```powershell
python -m py_compile src/4_main_desktop_app.py
```

Manual verify:

- App mac dinh light mode van mo duoc.
- Goi tam `set_theme_mode("dark")` sau init khong crash.

Done khi:

- Code co 2 palette va co the doi mode runtime bang helper.

Bang chung: `THEMES = {"light": ..., "dark": ...}` va `set_theme_mode`.

### TASK-074 - Them UI control doi Light/Dark mode

Uu tien: P0

Trang thai: Done

Muc tieu: nguoi dung co nut/chon che do theme truc tiep trong sidebar.

Pham vi:

- `src/4_main_desktop_app.py`
- `reports/GUI_QA_CHECKLIST.md`

Cach lam:

1. Trong sidebar, them section hoac control trong header:
   - `CTkSegmentedButton(values=["Light", "Dark"])`, hoac
   - `CTkSwitch(text="Dark mode")`.
2. Khi nguoi dung doi:
   - Goi `ctk.set_appearance_mode("light"/"dark")`.
   - Goi `self.set_theme_mode(...)`.
   - Cap nhat widget colors cua main window, sidebar, video frame, status section, KPI cards.
3. Khi statistics dashboard dang mo, co the:
   - Reload dashboard theo theme moi, hoac
   - Ghi note can dong/mo lai dashboard sau khi doi theme.
4. Them QA case:
   - Doi Light -> Dark -> Light khong crash.
   - Text/charts doc duoc sau khi doi.

Verify:

```powershell
python -m py_compile src/4_main_desktop_app.py
```

Manual verify:

```powershell
.\.venv\Scripts\python.exe src\4_main_desktop_app.py
```

Done khi:

- Nguoi dung co the doi theme tu UI.
- App khong can restart de thay doi theme chinh.

Bang chung: sidebar co `CTkSegmentedButton(values=["Light", "Dark"])`.

### TASK-075 - Luu theme mode vao database settings

Uu tien: P1

Trang thai: Done

Muc tieu: app nho theme nguoi dung chon sau khi dong/mo lai.

Pham vi:

- `src/3_database_setup.py`
- `src/4_main_desktop_app.py`
- Co the them test database neu da co service test

Cach lam:

1. Them cot moi vao bang `CaiDat`, vi du:
   - `cheDoGiaoDien TEXT NOT NULL DEFAULT 'light'`
2. Them migration nhe trong app startup:
   - Neu bang `CaiDat` chua co cot `cheDoGiaoDien`, `ALTER TABLE` them cot.
   - Khong bat nguoi dung reset database.
3. `load_cai_dat` doc `cheDoGiaoDien`.
4. `read_gui_settings` va `save_cai_dat_from_gui` luu theme.
5. Khi init app, apply theme sau khi doc database.

Verify:

```powershell
python -m py_compile src/3_database_setup.py src/4_main_desktop_app.py
```

Manual verify:

- Chon Dark, luu cai dat, dong app, mo lai app van Dark.
- Chon Light, luu cai dat, dong app, mo lai app van Light.

Done khi:

- Theme persist qua database cu va database moi.

Bang chung: `CaiDat.cheDoGiaoDien`, migration `ALTER TABLE`, load/save settings da cap nhat.

### TASK-076 - Cap nhat statistics dashboard theo theme runtime

Uu tien: P1

Trang thai: Done

Muc tieu: dashboard/chart/table doi mau dung theo Light/Dark mode.

Pham vi:

- `src/4_main_desktop_app.py`

Cach lam:

1. Cac function chart dung theme hien tai thay vi global light token:
   - `apply_chart_style`
   - `embed_chart`
   - `style_session_tree`
2. Khi dashboard mo trong Dark mode:
   - figure face/axis/bg dung dark surface.
   - tick/label/grid doc duoc.
3. Bang `ttk.Treeview` co style rieng cho dark mode.
4. Kiem tra empty state va risk colors tren ca hai theme.

Verify:

```powershell
python -m py_compile src/4_main_desktop_app.py
```

Manual verify:

- Light dashboard doc duoc.
- Dark dashboard doc duoc.
- Doi theme va mo lai dashboard khong crash.

Done khi:

- Statistics khong bi lech theme khi nguoi dung chon Dark.

Bang chung: chart/table/dashboard dung `THEME` dong theo mode hien tai.

### TASK-077 - Cap nhat QA va acceptance notes cho baseline/theme

Uu tien: P0

Trang thai: Done

Muc tieu: co checklist verify dung hanh vi moi.

Pham vi:

- `reports/GUI_QA_CHECKLIST.md`
- `reports/UI_ACCEPTANCE_NOTES.md`
- Co the tao `reports/BASELINE_RULE_QA.md`

Cach lam:

1. Them QA case baseline:
   - Rut co vua van dung.
   - Mui gan ngang vai/rut co sau bi sai.
   - Dau lech ngang van bi sai.
   - Tay gan mieng/chong cam van bi sai.
2. Them QA case theme:
   - Light mode default.
   - Dark mode switch.
   - Doi qua lai khi camera chua chay.
   - Doi qua lai khi camera dang chay.
   - Dashboard doc duoc trong 2 theme.
3. Ghi case nao can camera/video va case nao test unit duoc.

Verify:

```powershell
Get-Content reports/GUI_QA_CHECKLIST.md
```

Done khi:

- Checklist phu hop baseline rule moi va theme toggle.

Bang chung: `reports/GUI_QA_CHECKLIST.md`, `reports/UI_ACCEPTANCE_NOTES.md`, `reports/BASELINE_RULE_QA.md`.

### TASK-078 - Chay full verification sau khi sua baseline/theme

Uu tien: P0

Trang thai: Done

Muc tieu: dam bao thay doi baseline/theme khong pha app.

Pham vi:

- Toan bo file bi sua trong TASK-069 den TASK-077

Verify bat buoc:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
python -m py_compile src/1_rule_based_baseline.py src/2_extract_features.py src/3_database_setup.py src/4_main_desktop_app.py src/5_train_ann_local.py src/6_evaluate_external.py src/7_video_wise_evaluation.py src/8_compare_algorithms.py src/9_ablation_study.py src/10_export_statistics.py src/11_statistical_analysis.py src/12_temporal_risk_index.py src/posture_baseline.py src/statistics_service.py src/utils.py
.\.venv\Scripts\python.exe src\4_main_desktop_app.py
```

Manual verify:

- App mo duoc.
- Light/Dark toggle hoat dong.
- Rule-based mode dung rule rut co moi.
- ANN mode van load model/scaler va start duoc.

Done khi:

- Full test pass.
- App mo duoc khong traceback.
- Manual QA ghi ket qua vao checklist.

Bang chung:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
# 20 passed, 1 skipped

python -m py_compile src/1_rule_based_baseline.py src/2_extract_features.py src/3_database_setup.py src/4_main_desktop_app.py src/5_train_ann_local.py src/6_evaluate_external.py src/7_video_wise_evaluation.py src/8_compare_algorithms.py src/9_ablation_study.py src/10_export_statistics.py src/11_statistical_analysis.py src/12_temporal_risk_index.py src/posture_baseline.py src/statistics_service.py src/utils.py
# pass
```

Khoi tao app va doi theme Light/Dark bang script ngan: pass. Manual QA voi webcam/video van can tick trong `reports/GUI_QA_CHECKLIST.md`.

## Thu tu de xuat

Lam theo thu tu nay de it rui ro:

1. TASK-069: test baseline truoc.
2. TASK-070: sua rule trong module baseline.
3. TASK-071: dam bao GUI dung module baseline moi.
4. TASK-073 va TASK-074: theme toggle runtime.
5. TASK-076: dashboard/chart theo theme.
6. TASK-075: persist theme vao database.
7. TASK-077 va TASK-078: QA va verify cuoi.

Neu can lam nhanh nhat cho demo:

1. TASK-069
2. TASK-070
3. TASK-071
4. TASK-073
5. TASK-074
6. TASK-078
