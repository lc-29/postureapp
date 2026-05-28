# 07. Phan tich du an va task phat trien tiep

Ngay cap nhat: 2026-05-27

## Tom tat trang thai hien tai

Du an da co pipeline kha day du cho mot he thong desktop phat hien tu the:

- Capture tu webcam, camera IP hoac video file bang OpenCV.
- MediaPipe Pose trich xuat 33 landmark thanh 99 feature.
- ANN binary classifier va rule-based baseline.
- GUI CustomTkinter co che do ANN/rule-based, canh bao am thanh va thong ke.
- SQLite luu phien lam viec, nhat ky tu the va thong ke ngay.
- Co script train, external evaluation, threshold sweep, algorithm comparison, ablation, statistical analysis va Temporal Posture Risk Index.
- Co tai lieu README, experiment protocol, dataset manifest, paper outline, method/results draft va checklist giao hang.

Kiem chung nhanh ngay 2026-05-27:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
# 15 passed, 1 skipped

python -m py_compile src/1_rule_based_baseline.py src/2_extract_features.py src/3_database_setup.py src/4_main_desktop_app.py src/5_train_ann_local.py src/6_evaluate_external.py src/7_video_wise_evaluation.py src/8_compare_algorithms.py src/9_ablation_study.py src/10_export_statistics.py src/11_statistical_analysis.py src/12_temporal_risk_index.py src/posture_baseline.py src/utils.py
# pass
```

Luu y moi truong:

- Python he thong `C:\Users\duong\AppData\Local\Programs\Python\Python311\python.exe` chua cai `pytest`, nen `python -m pytest tests -q` fail neu khong active `.venv`.
- `.venv` hien tai dung Python 3.11.9, pytest 9.0.3, TensorFlow 2.16.2, scikit-learn 1.6.1.

Ket qua hien co dang co gia tri bao cao:

- External ANN: accuracy `0.793164`, precision `0.945988`, recall `0.659849`, F1 `0.777425` tai threshold `0.5`.
- Best threshold sweep theo F1: threshold `0.10`, accuracy `0.804361`, precision `0.912863`, recall `0.710441`, F1 `0.799031`.
- Rule-based tren external: accuracy `0.566293`, precision `0.584427`, recall `0.719053`, F1 `0.644788`.
- McNemar test ANN vs rule-based: p-value `2.19314e-60`, ANN khac biet co y nghia thong ke tren external frame-level set.

## Diem con thieu lon

1. Validation khoa hoc van con yeu: CSV chinh chua co `source_video`, `frame_index`, `participant_id`, nen chua co video-wise/person-wise split that.
2. GUI van con copy logic rule-based dai trong `src/4_main_desktop_app.py` du da co `src/posture_baseline.py`.
3. App va script con hard-code mot so path thay vi dung chung `src/config.py`.
4. Threshold tot nhat tren external la `0.10`, nhung app/evaluation mac dinh van dung `0.5`; can quyet dinh threshold deployment va ghi ro ly do.
5. Chua co model card/reproducibility metadata de biet model nao duoc train tu dataset nao, threshold nao, commit nao.
6. Checklist GUI va final delivery chua duoc tick bang ngay test, nguoi test, screenshot.
7. Related work con mot so nguon o trang thai `Need source`; paper chua san sang nop neu chua co citation that.
8. Chua co dong goi/launcher chuan cho nguoi dung khong mo terminal.

## Quy trinh lam tiep

Lam theo thu tu:

1. Chon task co uu tien P0 truoc.
2. Tao branch neu can sua code: `codex/task-xxx-ten-ngan`.
3. Doc file pham vi truoc khi sua, khong sua ngoai scope.
4. Chay lenh Verify cua task.
5. Cap nhat muc `Trang thai` trong file nay thanh `Done` kem bang chung.
6. Neu task sinh artifact local rieng tu nhu log SQLite, khong commit neu da bi ignore hoac co du lieu ca nhan.

Quy uoc trang thai:

- `Todo`: chua lam.
- `Doing`: dang lam.
- `Blocked`: bi chan, can thong tin/du lieu.
- `Done`: da verify xong.

## Backlog task moi

### TASK-040 - Chuan hoa huong dan chay test bang virtualenv

Uu tien: P0

Trang thai: Todo

Muc tieu: tranh nham lan giua Python he thong va `.venv`, dam bao nguoi khac chay test dung moi truong.

Pham vi:

- `README.md`
- `reports/FINAL_DELIVERY_CHECKLIST.md`
- Co the them `reports/ENVIRONMENT_CHECK.md`

Cach lam:

1. Ghi ro lenh activate `.venv` tren PowerShell.
2. Them lenh verify bang `.\.venv\Scripts\python.exe -m pytest tests -q`.
3. Ghi ro neu `python -m pytest` bao `No module named pytest` thi dang dung sai interpreter hoac chua cai requirements.
4. Ghi version Python khuyen nghi: 3.10 hoac 3.11.

Verify:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
Get-Content README.md
```

Done khi:

- README khong lam nguoi dung chay test bang Python global nham.
- Checklist co muc verify interpreter.

### TASK-041 - Xoa logic rule-based copy trong GUI

Uu tien: P0

Trang thai: Todo

Muc tieu: GUI dung duy nhat module `src/posture_baseline.py` cho baseline, tranh sai khac logic giua script baseline va app.

Pham vi:

- `src/4_main_desktop_app.py`
- `src/posture_baseline.py` neu can bo sung API nho
- `tests/test_posture_baseline.py`

Cach lam:

1. Tim cac constant/function baseline copy trong `src/4_main_desktop_app.py`.
2. Import `extract_posture_features`, `classify_posture_rule_based` va cac constant can hien thi tu `posture_baseline.py`.
3. Xoa function duplicate neu khong con duoc goi.
4. Giu nguyen text UI va behavior canh bao.
5. Neu GUI can feature field rieng, bo sung vao `posture_baseline.py` thay vi copy lai.

Verify:

```powershell
python -m py_compile src/4_main_desktop_app.py src/posture_baseline.py
.\.venv\Scripts\python.exe -m pytest tests/test_posture_baseline.py -q
```

Done khi:

- `src/4_main_desktop_app.py` khong con cac ham tinh baseline duplicate lon.
- Baseline mode van compile va test pass.

### TASK-042 - Dung chung config path toan du an

Uu tien: P1

Trang thai: Todo

Muc tieu: moi script dung chung path mac dinh, giam hard-code va lech cau hinh.

Pham vi:

- `src/config.py`
- `src/4_main_desktop_app.py`
- `src/6_evaluate_external.py`
- `src/8_compare_algorithms.py`
- `src/11_statistical_analysis.py`

Cach lam:

1. Them `ALARM_PATH`, `EXTERNAL_DATASET_PATH`, `RESULTS_DIR` vao `src/config.py`.
2. Doi cac script import config thay vi tu khai bao `BASE_DIR`, `MODEL_PATH`, `SCALER_PATH` lap lai.
3. Giu CLI argument hien tai de nguoi dung van override duoc path.
4. Khong doi default output.

Verify:

```powershell
python -m py_compile src/config.py src/4_main_desktop_app.py src/6_evaluate_external.py src/8_compare_algorithms.py src/11_statistical_analysis.py
.\.venv\Scripts\python.exe -m pytest tests/test_imports.py -q
```

Done khi:

- Duong dan mac dinh chi can sua o `src/config.py`.
- Cac script compile va import test pass.

### TASK-043 - Cai tien thong bao loi khi thieu artifact

Uu tien: P1

Trang thai: Todo

Muc tieu: khi thieu database/model/scaler/alarm, GUI noi ro file nao thieu va lenh sua.

Pham vi:

- `src/4_main_desktop_app.py`
- `reports/GUI_QA_CHECKLIST.md`

Cach lam:

1. Kiem tra `get_db_connection`, `load_ai_components`, `get_alarm_path`.
2. Messagebox can co absolute path, lenh goi y va cach chuyen sang baseline mode neu ANN artifact thieu.
3. Log loi ra terminal ngan gon.
4. Them case QA cho database/model/scaler/alarm missing.

Verify:

```powershell
python -m py_compile src/4_main_desktop_app.py
Get-Content reports/GUI_QA_CHECKLIST.md
```

Done khi:

- Message loi co hanh dong tiep theo, khong chi la stack trace.
- Checklist co case test missing artifact.

### TASK-044 - Tao CSV co metadata tu raw video

Uu tien: P0 cho nghien cuu, P1 cho demo app

Trang thai: Blocked neu khong co raw video local

Muc tieu: tao dataset co `source_video`, `frame_index`, `sample_fps`, `video_fps` de danh gia video-wise.

Pham vi:

- `dataset/posture_data_2fps_with_metadata.csv`
- `reports/DATASET_MANIFEST.md`
- Raw video folder local, khong dua video lon vao Git

Cach lam:

1. Xac dinh raw video folder dang dung cho correct/incorrect.
2. Chay extract voi metadata.
3. Kiem tra shape, label distribution va so `source_video`.
4. Cap nhat manifest voi duong dan raw data hoac external storage.

Verify:

```powershell
python src/2_extract_features.py --include-metadata --output dataset/posture_data_2fps_with_metadata.csv
python src/7_video_wise_evaluation.py --dataset dataset/posture_data_2fps_with_metadata.csv
```

Done khi:

- CSV moi co day du metadata.
- `video_wise_protocol.md` khong con bao thieu `source_video/frame_index`.

### TASK-045 - Implement video-wise train/evaluation that

Uu tien: P0 cho paper

Trang thai: Todo, phu thuoc TASK-044

Muc tieu: thay `src/7_video_wise_evaluation.py` tu check-only thanh train/evaluate split theo `source_video`.

Pham vi:

- `src/7_video_wise_evaluation.py`
- `reports/results/video_wise_metrics.txt`
- `reports/results/video_wise_confusion_matrix.csv`
- `reports/springer_results_draft.md`

Cach lam:

1. Load CSV metadata.
2. Split theo `source_video`, khong de frame cung video nam o ca train va test.
3. Stratify theo video label neu kha thi; neu khong kha thi ghi ro han che.
4. Fit scaler tren train only.
5. Train ANN nho hoac load pipeline tuy muc tieu; khong dung scaler fit tren full data.
6. Luu metrics va confusion matrix.
7. Cap nhat results draft, so sanh frame-wise vs video-wise.

Verify:

```powershell
python src/7_video_wise_evaluation.py --dataset dataset/posture_data_2fps_with_metadata.csv
Get-Content reports/results/video_wise_metrics.txt
```

Done khi:

- Co metric video-wise that.
- Bao cao ghi ro protocol va khong claim qua muc frame-wise.

### TASK-046 - Quyet dinh threshold deployment cho ANN

Uu tien: P1

Trang thai: Todo

Muc tieu: thong nhat threshold app dung va threshold bao cao, vi external sweep cho F1 tot nhat tai `0.10` thay vi `0.5`.

Pham vi:

- `src/config.py`
- `src/4_main_desktop_app.py`
- `src/6_evaluate_external.py`
- `reports/springer_results_draft.md`
- `reports/MODEL_CARD.md` neu da co

Cach lam:

1. Doc `reports/results/external_threshold_sweep.csv`.
2. Chon threshold theo muc tieu: can bang F1, uu tien recall sai tu the, hoac giu precision cao.
3. Them config `ANN_DECISION_THRESHOLD`.
4. GUI dung config nay va hien thi trong setting hoac log.
5. Bao cao ghi ca threshold 0.5 va threshold deployment neu khac nhau.

Verify:

```powershell
python src/6_evaluate_external.py --threshold 0.10
python -m py_compile src/config.py src/4_main_desktop_app.py
```

Done khi:

- App va bao cao dung threshold co ly do ro rang.
- Khong con nham lan giua threshold evaluation va deployment.

### TASK-047 - Tao model card va reproducibility metadata

Uu tien: P1

Trang thai: Todo

Muc tieu: ghi ro model dang deploy duoc train/evaluate nhu the nao.

Pham vi:

- Tao `reports/MODEL_CARD.md`
- Co the tao `src/13_generate_model_card.py`

Cach lam:

1. Ghi intended use: nhac nho tu the, khong chan doan y te.
2. Ghi model path, scaler path, feature schema 99 landmark, threshold, dataset path.
3. Ghi Python/TensorFlow/scikit-learn versions.
4. Ghi external metrics, statistical CI, limitations.
5. Ghi ngay tao va commit hash neu repo co Git commit.

Verify:

```powershell
Get-Content reports/MODEL_CARD.md
```

Done khi:

- Nguoi khac doc model card biet model dung cho gi, khong dung cho gi, va tai lap bang artifact nao.

### TASK-048 - Hoan thien GUI QA va screenshot

Uu tien: P1

Trang thai: Todo

Muc tieu: co bang chung app desktop da duoc test thu cong.

Pham vi:

- `reports/GUI_QA_CHECKLIST.md`
- `reports/figures/` hoac thu muc screenshot duoc chon
- Khong commit anh co thong tin rieng tu neu co

Cach lam:

1. Chay GUI voi ANN mode.
2. Chay GUI voi rule-based mode.
3. Test webcam, video file, bat/tat am thanh, stop/start lai, thong ke ngay.
4. Test missing model/scaler/database bang cach doi ten tam thoi va khoi phuc lai.
5. Dien ngay test, nguoi test, ket qua.
6. Chup screenshot GUI va landmark overlay cho paper/demo.

Verify:

```powershell
Get-Content reports/GUI_QA_CHECKLIST.md
```

Done khi:

- Checklist co ket qua that, khong de trong.
- Screenshot can cho paper/demo da co hoac ghi ro vi tri luu ngoai Git.

### TASK-049 - Bo sung citation that va hoan thien Related Work

Uu tien: P0 cho paper

Trang thai: Todo

Muc tieu: paper khong dung citation gia dinh/placeholder.

Pham vi:

- `reports/RELATED_WORK_TODO.md`
- `reports/RELATED_PAPERS.bib`
- `reports/springer_paper_outline.md`
- `reports/LITERATURE_METRICS_COMPARISON.md`

Cach lam:

1. Tim nguon that cho BlazePose/MediaPipe Pose.
2. Tim nguon ergonomic posture assessment/RULA hoac nguon khoa hoc tuong duong.
3. Tim paper posture detection webcam/pose-estimation/ML gan bai nay.
4. Dien BibTeX that, DOI/URL ro rang.
5. Cap nhat related work bang so sanh cong bang, khong bien thanh leaderboard.

Verify:

```powershell
Get-Content reports/RELATED_WORK_TODO.md
Get-Content reports/RELATED_PAPERS.bib
```

Done khi:

- Khong con dong quan trong nao o trang thai `Need source`.
- Moi citation trong outline co nguon that.

### TASK-050 - Tao experiment runner mot lenh

Uu tien: P2

Trang thai: Todo

Muc tieu: giam loi khi chay nhieu script evaluation/report.

Pham vi:

- Tao `scripts/run_evaluation.ps1` hoac `src/13_run_evaluation_pipeline.py`
- `README.md`

Cach lam:

1. Chay external evaluation.
2. Chay algorithm comparison.
3. Chay statistical analysis.
4. Chay temporal risk index neu database co log.
5. In summary cac output path.
6. Neu mot buoc fail do thieu artifact, bao ro va tiep tuc buoc khac neu hop ly.

Verify:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_evaluation.ps1
```

Done khi:

- Mot lenh sinh lai cac artifact chinh trong `reports/results/`.

### TASK-051 - Them CI nhe cho import/test/compile

Uu tien: P2

Trang thai: Todo

Muc tieu: moi lan sua code deu biet test co vo hay khong.

Pham vi:

- `.github/workflows/python-ci.yml` neu repo day len GitHub
- Hoac `reports/CI_PLAN.md` neu chua muon them workflow

Cach lam:

1. Dung Python 3.11.
2. Cai `requirements.txt`.
3. Chay pytest.
4. Chay py_compile cac file `src`.
5. Neu TensorFlow/MediaPipe lam CI nang, can tach smoke tests nhe va document ly do.

Verify:

```powershell
Get-Content .github/workflows/python-ci.yml
```

Done khi:

- Co CI hoac co plan ro neu chua the bat CI.

### TASK-052 - Dong goi ung dung demo

Uu tien: P2

Trang thai: Todo

Muc tieu: nguoi demo co cach chay app it loi hon viec go lenh Python.

Pham vi:

- `run_app.bat`
- `README.md`
- Co the them `packaging/pyinstaller.spec`

Cach lam:

1. Cap nhat `run_app.bat` de dung `.venv` neu ton tai.
2. Kiem tra database/model/scaler truoc khi mo app.
3. Neu dung PyInstaller, tao spec rieng va ghi ro assets/model/database.
4. Chua can build binary neu chua co nhu cau nop.

Verify:

```powershell
.\run_app.bat
```

Done khi:

- Co duong chay demo de nguoi khong quen terminal van dung duoc.

### TASK-053 - Bo sung test database logging

Uu tien: P1

Trang thai: Todo

Muc tieu: giam rui ro sai thong ke/ngat phien khi GUI dang chay.

Pham vi:

- `src/3_database_setup.py`
- `src/4_main_desktop_app.py`
- Tao `tests/test_database_logging.py`

Cach lam:

1. Tach cac thao tac insert/update session thanh function test duoc neu co the.
2. Dung SQLite temp file cho test.
3. Test start session, insert posture log, warning log, end session, daily stats update.
4. Khong mo GUI trong unit test.

Verify:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_database_logging.py -q
```

Done khi:

- Logic logging co unit test nhanh, khong phu thuoc webcam/GUI.

### TASK-054 - Them privacy va safety notice

Uu tien: P1 cho giao hang cong khai

Trang thai: Todo

Muc tieu: noi ro app xu ly webcam/local logs nhu the nao va gioi han y te.

Pham vi:

- `README.md`
- `reports/springer_method_draft.md`
- Co the tao `reports/PRIVACY_AND_SAFETY.md`

Cach lam:

1. Ghi app khong phai cong cu chan doan y te.
2. Ghi webcam/video duoc xu ly local theo code hien tai.
3. Ghi SQLite co the chua session log va thoi diem, can tranh commit log rieng tu.
4. Ghi han che dataset va bias goc quay/anh sang/nguoi dung.

Verify:

```powershell
Get-Content README.md
Get-Content reports/PRIVACY_AND_SAFETY.md
```

Done khi:

- Nguoi demo/doc repo hieu ro rui ro va gioi han.

## Thu tu de xuat

1. TASK-040, TASK-041, TASK-043: lam sach truoc demo.
2. TASK-044, TASK-045, TASK-046, TASK-047: lam truoc khi viet/nop paper.
3. TASK-048, TASK-049, TASK-054: hoan thien giao hang va bao cao.
4. TASK-050, TASK-051, TASK-052, TASK-053: nang chat luong engineering neu con thoi gian.

