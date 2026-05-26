# 05. Checklist hoan thanh du an

Dung checklist nay sau khi lam backlog de quyet dinh du an da san sang demo/viet bao cao chua.

## A. Cai dat va chay lai

- [ ] Tao moi virtual environment thanh cong.
- [ ] Cai `requirements.txt` thanh cong.
- [ ] `python src/3_database_setup.py` chay OK.
- [ ] `python -m pytest tests` khong treo webcam.
- [ ] README huong dan duoc nguoi khac lam theo.

## B. Du lieu

- [ ] Co `reports/DATASET_MANIFEST.md`.
- [ ] Ghi ro so video train/external.
- [ ] Ghi ro so mau CSV va phan bo label.
- [ ] Ghi ro cach gan nhan correct/incorrect.
- [ ] Ghi ro dieu kien quay: camera, goc quay, anh sang, do phan giai.
- [ ] Neu co the, them `source_video` va `frame_index` vao CSV moi.

## C. Model va danh gia

- [ ] Co metrics local tu `models/local_training/metrics.txt`.
- [ ] Co external metrics trong `reports/results/`.
- [ ] Co confusion matrix local va external.
- [ ] Co threshold sweep.
- [ ] Co so sanh rule-based vs ANN.
- [ ] Co canh bao trong bao cao ve frame-wise split.
- [ ] Neu kip, co video-wise/person-wise evaluation.

## D. Code

- [ ] README va file doc khong loi encoding.
- [ ] Test webcam/video duoc danh dau manual hoac skip.
- [ ] Baseline logic khong bi copy-paste giua script va GUI.
- [ ] Cac file chinh compile duoc:

```powershell
python -m py_compile src/1_rule_based_baseline.py src/2_extract_features.py src/3_database_setup.py src/4_main_desktop_app.py src/5_train_ann_local.py
```

- [ ] Cac script moi co help/argparse neu can.
- [ ] Khong xoa dataset/model/database hien co.

## E. Ung dung desktop

- [ ] Mo duoc app.
- [ ] Chay ANN mode voi webcam hoac video file.
- [ ] Chay rule-based mode.
- [ ] Start/Stop khong crash.
- [ ] Canh bao am thanh co the bat/tat.
- [ ] Thong ke ngay hien thi duoc.
- [ ] Database co phien lam viec sau khi stop.
- [ ] Message loi than thien khi thieu model/scaler/database.
- [ ] Co `reports/GUI_QA_CHECKLIST.md` va da tick ket qua test thu cong.

## F. Bao cao Springer

- [ ] Co `reports/springer_paper_outline.md`.
- [ ] Co `reports/springer_method_draft.md`.
- [ ] Co `reports/springer_results_draft.md`.
- [ ] Co `reports/FIGURE_TABLE_PLAN.md`.
- [ ] Co `reports/RELATED_WORK_TODO.md`.
- [ ] Co hinh pipeline.
- [ ] Co screenshot GUI.
- [ ] Co bang dataset distribution.
- [ ] Co bang model architecture.
- [ ] Co bang metrics local/external.
- [ ] Co phan limitations trung thuc.
- [ ] Co Declarations placeholders.

## G. Dieu kien "xong" de nop/demo

Du an duoc xem la xong o muc do do an/nghien cuu ung dung khi:

- App chay duoc tren may demo bang webcam hoac video file.
- Model/scaler/database ton tai va dung duong dan.
- Co metrics local va external.
- Co README tai lap.
- Co checklist GUI da test thu cong.
- Co ban thao bao cao Springer it nhat gom Abstract, Method, Results, Discussion, Limitations.

## Lenh kiem tra cuoi cung goi y

```powershell
python src/3_database_setup.py
python -m pytest tests
python src/6_evaluate_external.py
python src/10_export_statistics.py
python -m py_compile src/1_rule_based_baseline.py src/2_extract_features.py src/3_database_setup.py src/4_main_desktop_app.py src/5_train_ann_local.py
```

Neu `src/6_evaluate_external.py` hoac `src/10_export_statistics.py` chua ton tai, hay lam TASK-011 va TASK-020 truoc.
