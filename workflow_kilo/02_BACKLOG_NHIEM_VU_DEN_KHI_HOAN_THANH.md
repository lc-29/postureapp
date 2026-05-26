# 02. Backlog nhiem vu den khi hoan thanh du an

Backlog nay duoc chia nho de Kilo Code Auto Free co the lam tung phien. Khong nen giao nhieu task cung luc.

## Phase A - Lam sach va tai lap du an

### TASK-001 - Sua README bi loi encoding va mo ta dung pipeline

Muc tieu: README doc duoc bang tieng Viet, nguoi moi cai duoc va hieu pipeline.

Pham vi:

- `README.md`

Cach lam goi y:

- Viet lai README ngan gon bang UTF-8.
- Them: muc tieu, cau truc thu muc, cai dat, khoi tao database, train nhanh, chay app, luu y webcam/video.
- Ghi ro app dung `models/ann_best.keras` va `models/scaler.pkl`.

Verify:

```powershell
Get-Content README.md
```

Done khi:

- Khong con ky tu loi encoding.
- Co it nhat 6 muc: Gioi thieu, Cau truc, Cai dat, Chay ung dung, Train/Danh gia, Luu y.

### TASK-002 - Sua encoding cac file config/utils/test nho

Muc tieu: comment/docstring tieng Viet doc duoc.

Pham vi:

- `src/config.py`
- `src/utils.py`
- `tests/test_imports.py`
- `tests/test_camera.py`

Cach lam goi y:

- Chi sua chu thich/docstring/text in ra.
- Khong doi logic.

Verify:

```powershell
python -m pytest tests/test_imports.py
```

Done khi:

- Khong con chuoi mojibake trong cac file tren.
- Import test pass hoac bao ro dependency nao thieu.

### TASK-003 - Tao tai lieu dataset manifest dang nhap tay

Muc tieu: co tai lieu mo ta du lieu de viet bao cao va tai lap.

Pham vi:

- Tao `reports/DATASET_MANIFEST.md`

Cach lam goi y:

- Ghi so video correct/incorrect, external, CSV shape, label distribution.
- Ghi cac truong can bo sung thu cong: so nguoi tham gia, tuoi/gioi tinh neu co, camera, do phan giai, anh sang, goc quay, cach gan nhan.
- Khong can doc noi dung video.

Verify:

```powershell
Get-Content reports/DATASET_MANIFEST.md
```

Done khi:

- Tai lieu co bang thong ke va danh sach thong tin can bo sung.

### TASK-004 - Tao huong dan thuc nghiem tai lap

Muc tieu: nguoi khac chay lai pipeline theo dung thu tu.

Pham vi:

- Tao `reports/EXPERIMENT_PROTOCOL.md`

Cach lam goi y:

- Mo ta thu tu: setup env, database, extract features, train, external eval, run GUI.
- Ghi seed `42`, sample FPS `2.0`, split train/val/test hien tai.
- Ghi can them video-wise/person-wise split.

Verify:

```powershell
Get-Content reports/EXPERIMENT_PROTOCOL.md
```

Done khi:

- Co lenh mau cho tung buoc va ghi ro output mong doi.

## Phase B - Test an toan va cau truc code

### TASK-005 - Bien test webcam thanh manual test

Muc tieu: `pytest` khong tu dong mo webcam.

Pham vi:

- `tests/test_mediapipe_pose.py`
- `tests/test_camera.py`
- `tests/test_videohevc.py`

Cach lam goi y:

- Dam bao cac file test khong mo camera/video o top-level.
- Doi thanh ham co `if __name__ == "__main__"` cho manual test.
- Voi pytest, bo qua manual tests bang `pytest.mark.skip` hoac tach sang `tests/manual_*.py`.

Verify:

```powershell
python -m pytest tests
```

Done khi:

- Pytest khong bi treo vi webcam.
- Neu HEVC sample khong ton tai thi test skip thay vi fail.

### TASK-006 - Them unit test cho `calculate_angle`

Muc tieu: co test logic nho, nhanh, khong phu thuoc webcam.

Pham vi:

- Tao `tests/test_utils.py`
- Co the sua `src/utils.py` neu can typing/docstring, khong doi logic lon.

Cach lam goi y:

- Test goc 90 do, 180 do, diem trung nhau tra `0.0`, input loi khong crash.

Verify:

```powershell
python -m pytest tests/test_utils.py
```

Done khi:

- Tat ca test moi pass.

### TASK-007 - Tao module baseline dung chung

Muc tieu: giam trung lap logic rule-based giua baseline script va GUI.

Pham vi:

- Tao `src/posture_baseline.py`
- Co the sua `src/1_rule_based_baseline.py`
- Khong sua GUI trong task nay neu thay doi qua lon.

Cach lam goi y:

- Chuyen cac hang so va ham tinh feature/classify tu `1_rule_based_baseline.py` sang module moi.
- Giu API ro: `extract_posture_features(landmarks)`, `classify_posture_rule_based(features)`.
- Script baseline import module moi.

Verify:

```powershell
python -m pytest tests/test_utils.py tests/test_imports.py
```

Done khi:

- `src/1_rule_based_baseline.py` import duoc module moi.
- Chua lam hong import.

### TASK-008 - Cho GUI dung module baseline chung

Muc tieu: xoa logic baseline copy trong `4_main_desktop_app.py`.

Pham vi:

- `src/4_main_desktop_app.py`
- `src/posture_baseline.py`

Cach lam goi y:

- Import cac ham/hang so can dung tu `posture_baseline.py`.
- Xoa cac ham trung lap neu chac chan khong con dung.
- Lam tung phan nho, uu tien khong doi giao dien.

Verify:

```powershell
python -m pytest tests/test_imports.py
python -m py_compile src/4_main_desktop_app.py src/posture_baseline.py
```

Done khi:

- GUI compile duoc.
- Baseline mode van co du lieu feature de hien thi.

### TASK-009 - Them test baseline voi landmark gia lap

Muc tieu: baseline co test logic khong can MediaPipe/camera.

Pham vi:

- Tao `tests/test_posture_baseline.py`
- Co the sua `src/posture_baseline.py` nhe neu can.

Cach lam goi y:

- Tao class/namespace gia lap co `x`, `y`, `z`, `visibility`.
- Test case tu the dung -> `CORRECT`.
- Test vai lech/than nghieng/dau lech/tay gan mieng -> `INCORRECT`.
- Test visibility thap -> `NO_PERSON_OR_LOW_CONFIDENCE`.

Verify:

```powershell
python -m pytest tests/test_posture_baseline.py
```

Done khi:

- Baseline co it nhat 4 test case pass.

### TASK-010 - Chuan hoa config duong dan trong app

Muc tieu: giam hard-code duong dan lap lai.

Pham vi:

- `src/config.py`
- `src/4_main_desktop_app.py`
- `src/5_train_ann_local.py` neu can nhe.

Cach lam goi y:

- Dung `config.py` cho `BASE_DIR`, `DATABASE_PATH`, `MODEL_PATH`, `SCALER_PATH`, `ALARM_PATH`.
- Khong doi behavior.

Verify:

```powershell
python -m py_compile src/config.py src/4_main_desktop_app.py src/5_train_ann_local.py
```

Done khi:

- Cac file compile duoc.
- Duong dan model/database van tro dung.

## Phase C - Danh gia khoa hoc va do tin cay

### TASK-011 - Tao script external evaluation

Muc tieu: danh gia model hien tai tren `posture_external_test_2fps.csv`.

Pham vi:

- Tao `src/6_evaluate_external.py`
- Tao output trong `reports/results/`

Cach lam goi y:

- Load CSV external, model `models/ann_best.keras`, scaler `models/scaler.pkl`.
- Validate 99 feature + label.
- Tinh accuracy, precision, recall, F1, confusion matrix.
- Luu `external_metrics.txt`, `external_confusion_matrix.csv`.

Verify:

```powershell
python src/6_evaluate_external.py
```

Done khi:

- Co file metrics external trong `reports/results/`.
- Script khong train lai model.

### TASK-012 - Them threshold sweep cho external evaluation

Muc tieu: tim nguong sigmoid tot hon 0.5 neu can.

Pham vi:

- `src/6_evaluate_external.py`
- Output `reports/results/external_threshold_sweep.csv`

Cach lam goi y:

- Quet threshold tu 0.1 den 0.9 buoc 0.05.
- Luu accuracy/precision/recall/F1 theo threshold.
- Ghi threshold co F1 cao nhat.

Verify:

```powershell
python src/6_evaluate_external.py
```

Done khi:

- Co CSV sweep va metrics van sinh dung.

### TASK-013 - Tao script video-wise split evaluation

Muc tieu: giam rui ro data leakage theo frame.

Pham vi:

- Tao `src/7_video_wise_evaluation.py`
- Neu can, tao `reports/results/video_wise_protocol.md`

Cach lam goi y:

- Neu CSV hien tai khong co `source_video`, script phai bao ro chua the chay video-wise split va de xuat can trich xuat lai metadata.
- Khong phai tu suy dien source video tu CSV neu khong co cot.

Verify:

```powershell
python src/7_video_wise_evaluation.py
```

Done khi:

- Script khong crash.
- Neu thieu metadata, output ghi ro yeu cau them cot `source_video` va `frame_index`.

### TASK-014 - Them metadata source video vao feature extraction

Muc tieu: CSV co the danh gia video-wise/person-wise.

Pham vi:

- `src/2_extract_features.py`
- Tao output moi, khong ghi de CSV chinh neu chua duoc phep.

Cach lam goi y:

- Them option `--include-metadata`.
- Khi bat option, them cot: `source_video`, `frame_index`, `sample_fps`, `video_fps`, `label`.
- Mac dinh giu output cu 99 feature + label de khong lam hong train script.

Verify:

```powershell
python -m py_compile src/2_extract_features.py
```

Done khi:

- Compile duoc.
- Help argparse co option moi.

### TASK-015 - Cap nhat train script de chap nhan CSV co metadata

Muc tieu: train script bo qua cot metadata neu co.

Pham vi:

- `src/5_train_ann_local.py`

Cach lam goi y:

- Xac dinh feature columns bang prefix `landmark_`.
- Yeu cau dung 99 feature landmark.
- Giu `label`.
- Neu co cot metadata thi khong dua vao model.

Verify:

```powershell
python -m py_compile src/5_train_ann_local.py
```

Done khi:

- Compile duoc.
- Van doc CSV cu duoc.

### TASK-016 - Them option train nhanh smoke test

Muc tieu: kiem tra pipeline train ma khong chay lau.

Pham vi:

- `src/5_train_ann_local.py`

Cach lam goi y:

- Them option `--max-rows` hoac `--smoke-test`.
- Neu smoke, lay tap con co stratify don gian, epochs nho.
- Output vao thu muc tam theo tham so.

Verify:

```powershell
python src/5_train_ann_local.py --epochs 2 --patience 1 --max-rows 400 --output-dir models/tmp_smoke
```

Done khi:

- Chay nhanh va sinh artifacts trong `models/tmp_smoke`.

### TASK-017 - Tao benchmark rule-based vs ANN

Muc tieu: co bang so sanh cho bao cao.

Pham vi:

- Tao `src/8_compare_algorithms.py`
- Output `reports/results/algorithm_comparison.csv`

Cach lam goi y:

- ANN danh gia tren CSV.
- Rule-based can feature hinh hoc tu landmark object; neu CSV chi co landmark x/y/z, co the reconstruct landmark namespace.
- Tinh metrics cho ANN va rule-based tren external CSV.

Verify:

```powershell
python src/8_compare_algorithms.py
```

Done khi:

- Co bang comparison toi thieu: algorithm, dataset, accuracy, precision, recall, f1.

### TASK-018 - Tao ablation study nho

Muc tieu: co diem nghien cuu: tac dong cua nhom feature/threshold.

Pham vi:

- Tao `src/9_ablation_study.py`
- Output `reports/results/ablation_results.csv`

Cach lam goi y:

- Phien ban nho: so sanh ANN full 99 landmarks voi mot model nho dung chi cac diem dau-vai-hong-tay.
- Khong can toi uu sau.
- Dung epochs it hoac co option.

Verify:

```powershell
python -m py_compile src/9_ablation_study.py
```

Done khi:

- Script compile va co huong dan chay.

## Phase D - Ung dung, database va trai nghiem demo

### TASK-019 - Kiem tra va sua logging SQLite nho

Muc tieu: database logging khong mat phien/canh bao.

Pham vi:

- `src/4_main_desktop_app.py`
- `src/3_database_setup.py` neu can.

Cach lam goi y:

- Doc cac ham `start_phien_lam_viec`, `end_phien_lam_viec`, `insert_nhat_ky_tu_the`, `update_thong_ke_ngay`.
- Them try/except hoac commit ro neu can.
- Khong doi schema lon.

Verify:

```powershell
python src/3_database_setup.py
python -m py_compile src/4_main_desktop_app.py
```

Done khi:

- Database setup OK.
- App compile duoc.

### TASK-020 - Them export CSV thong ke tu SQLite

Muc tieu: lay du lieu phien de dua vao bao cao/demo.

Pham vi:

- Tao `src/10_export_statistics.py`
- Output `reports/results/session_statistics.csv`, `daily_statistics.csv`

Cach lam goi y:

- Doc bang `PhienLamViec`, `ThongKeNgay`, `NhatKyTuThe` neu can.
- Khong sua database.

Verify:

```powershell
python src/10_export_statistics.py
```

Done khi:

- Sinh CSV neu database ton tai.
- Neu bang rong, van sinh file co header hoac thong bao ro.

### TASK-021 - Cai tien thong bao loi khi thieu model/scaler/database

Muc tieu: nguoi dung biet can chay lenh nao.

Pham vi:

- `src/4_main_desktop_app.py`

Cach lam goi y:

- Kiem tra luong `load_ai_components` va `get_db_connection`.
- Messagebox ghi ro duong dan thieu va lenh goi y.
- Khong doi logic prediction.

Verify:

```powershell
python -m py_compile src/4_main_desktop_app.py
```

Done khi:

- Compile duoc.
- Error message than thien hon.

### TASK-022 - Them che do video demo khong can webcam

Muc tieu: demo hoi dong bang file video co san.

Pham vi:

- `README.md`
- Co the sua `src/4_main_desktop_app.py` nhe neu can.

Cach lam goi y:

- Ghi huong dan nhap duong dan video vao GUI.
- Neu app da co chuc nang, chi bo sung README.
- Khong can tao video moi.

Verify:

```powershell
Get-Content README.md
```

Done khi:

- Co huong dan demo bang video file trong README.

### TASK-023 - Them manual QA checklist cho GUI

Muc tieu: co bang test thu cong truoc khi nop.

Pham vi:

- Tao `reports/GUI_QA_CHECKLIST.md`

Cach lam goi y:

- Test webcam, video file, model thieu, database thieu, bat/tat am thanh, thong ke ngay, baseline mode, ANN mode.
- Co cot Ket qua/Ngay test/Nguoi test.

Verify:

```powershell
Get-Content reports/GUI_QA_CHECKLIST.md
```

Done khi:

- Checklist du de nguoi khac tick khi demo.

## Phase E - Bao cao Springer

### TASK-024 - Tao skeleton bai bao Springer bang Markdown

Muc tieu: co ban thao noi dung khoa hoc.

Pham vi:

- Tao `reports/springer_paper_outline.md`

Cach lam goi y:

- Theo cau truc: Title, Abstract, Keywords, Introduction, Related Work, Materials and Methods, Experiments, Results, Discussion, Limitations, Conclusion, Declarations, References.
- Chen placeholder bang/hinh can co.

Verify:

```powershell
Get-Content reports/springer_paper_outline.md
```

Done khi:

- Co day du muc Springer co ban.

### TASK-025 - Viet phan Method tu code hien co

Muc tieu: bien pipeline code thanh mo ta khoa hoc.

Pham vi:

- `reports/springer_method_draft.md`

Cach lam goi y:

- Mo ta MediaPipe Pose, vector 99 feature, ANN architecture, rule-based baseline, warning logic, SQLite logging.
- Ghi ro day la he thong ho tro, khong phai chan doan y te.

Verify:

```powershell
Get-Content reports/springer_method_draft.md
```

Done khi:

- Co van ban co the dua vao paper.

### TASK-026 - Viet phan Results tu metrics hien co

Muc tieu: co ban nhap ket qua ban dau.

Pham vi:

- `reports/springer_results_draft.md`

Cach lam goi y:

- Lay metrics tu `models/local_training/metrics.txt`.
- Neu co external metrics tu TASK-011 thi dua vao.
- Ghi canh bao ve split theo frame va can video-wise/person-wise.

Verify:

```powershell
Get-Content reports/springer_results_draft.md
```

Done khi:

- Co bang ket qua local va cho external neu co.

### TASK-027 - Tao danh sach hinh/bang can chup

Muc tieu: khong thieu artifact khi viet bai.

Pham vi:

- Tao `reports/FIGURE_TABLE_PLAN.md`

Cach lam goi y:

- Hinh: pipeline, GUI, confusion matrix, training curves, database schema, sample landmarks.
- Bang: dataset distribution, model architecture, metrics local/external, comparison algorithms, ablation.

Verify:

```powershell
Get-Content reports/FIGURE_TABLE_PLAN.md
```

Done khi:

- Moi hinh/bang co nguon file hoac cach tao.

### TASK-028 - Tao file references can tim

Muc tieu: chuan bi Related Work.

Pham vi:

- Tao `reports/RELATED_WORK_TODO.md`

Cach lam goi y:

- Khong tu bia citation.
- Liet ke can tim: MediaPipe Pose paper/docs, ergonomic posture assessment, webcam posture detection, ANN/SVM/KNN posture classification, real-time feedback systems.
- De cot `Citation`, `What to use`, `Status`.

Verify:

```powershell
Get-Content reports/RELATED_WORK_TODO.md
```

Done khi:

- Co danh sach citation can bo sung bang nguon that.

### TASK-029 - Chuan bi goi nop/demo cuoi

Muc tieu: repo co the giao cho nguoi khac chay.

Pham vi:

- `README.md`
- Tao `reports/FINAL_DELIVERY_CHECKLIST.md`

Cach lam goi y:

- Checklist: env, database, model/scaler, demo video, external metrics, paper draft, screenshots.
- Khong dong goi binary moi.

Verify:

```powershell
Get-Content reports/FINAL_DELIVERY_CHECKLIST.md
```

Done khi:

- Co checklist nop do an/bai bao.

### TASK-030 - Tong ket technical debt con lai

Muc tieu: biet ro dieu gi chua lam truoc khi nop.

Pham vi:

- Tao `reports/TECHNICAL_DEBT.md`

Cach lam goi y:

- Nhom theo: code, data, evaluation, UI, deployment, paper.
- Ghi muc do uu tien P0/P1/P2.

Verify:

```powershell
Get-Content reports/TECHNICAL_DEBT.md
```

Done khi:

- Co danh sach no ky thuat minh bach va cach giam rui ro.
