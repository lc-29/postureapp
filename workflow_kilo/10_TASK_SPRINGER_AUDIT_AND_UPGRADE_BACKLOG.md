# 10 Task Springer Audit And Upgrade Backlog

Ngay tao: 2026-05-27

## Muc tieu

Thuc thi cac nhiem vu tiep theo de do an posture detection app dat muc day du hon ve thuat toan, du lieu, thuc nghiem, bao cao, va claim khoa hoc theo chuan Springer.

## Nguyen tac thuc thi

- Lam tu tren xuong duoi.
- Moi task phai co output ro rang trong `reports/` hoac code/test tuong ung.
- Khong claim tot hon literature neu chua co benchmark cung protocol.
- Khong sua lon GUI truoc khi hoan thien evaluation protocol.
- Moi thay doi code phai chay pytest/py_compile toi thieu.

## Execution status 2026-05-27

| Task | Trang thai | Output chinh |
|---|---|---|
| TASK-100 | DONE | `reports/MODEL_CARD_ANN_CURRENT.md` |
| TASK-101 | PARTIAL DONE | Extractor da ho tro metadata; da tao external metadata CSV. Full train metadata CSV chua chay vi raw train videos lon. |
| TASK-102 | DONE cho external metadata | `reports/results/video_wise_metrics.csv`, `reports/results/video_wise_summary.md` |
| TASK-103 | DONE | `reports/results/algorithm_benchmark_full.csv` |
| TASK-104 | DONE | `reports/results/external_predictions.csv`, `reports/ERROR_ANALYSIS.md` |
| TASK-105 | DONE | `roc_curve.png`, `pr_curve.png`, `calibration_curve.png` |
| TASK-106 | PARTIAL DONE | `reports/results/ablation_full.csv`; app/train schema moi chua thay model default. |
| TASK-107 | DONE | App co smoothing window va smoothing threshold trong GUI/config. |
| TASK-108 | DONE | `reports/RUNTIME_BENCHMARK.md`, `reports/results/runtime_benchmark.csv` |
| TASK-109 | PARTIAL DONE | Figures/tables da sinh; GUI screenshots con can chup manual. |
| TASK-110 | DONE | `reports/RELATED_WORK_TODO.md` cap nhat claim rule/source. |
| TASK-111 | DONE | `reports/DATA_ETHICS_STATEMENT.md` |
| TASK-112 | DONE | Cap nhat `springer_method_draft.md`, `springer_results_draft.md`, `springer_paper_outline.md` |
| TASK-113 | DONE | `reports/FINAL_REPRODUCIBILITY_LOG.md` |

## TASK-100: Tao model card cho ANN hien tai

Trang thai: DONE ngay 2026-05-27. Output: `reports/MODEL_CARD_ANN_CURRENT.md`.

Muc tieu: ghi lai model hien tai de tai lap.

Pham vi:

- Tao `reports/MODEL_CARD_ANN_CURRENT.md`.
- Ghi dataset, feature schema, label, threshold, external metrics, limitations, intended use.

Buoc lam:

1. Doc `reports/DATASET_MANIFEST.md`.
2. Doc metrics trong `reports/results/`.
3. Kiem tra file model trong `models/`.
4. Viet model card ngan gon, co bang metric.

Done khi:

- File model card ton tai.
- Co muc limitations va intended use.

## TASK-101: Re-extract dataset co metadata

Muc tieu: sua pipeline de CSV co the video-wise evaluation.

Pham vi:

- Sua `src/2_extract_features.py`.
- Them cot `source_video`, `frame_index`, `timestamp_sec`.
- Neu co thong tin, them `participant_id`, `view_angle`, `camera_type`.

Buoc lam:

1. Kiem tra input raw videos trong `dataset/raw_*`.
2. Xac dinh schema metadata toi thieu.
3. Sua extractor de giu metadata.
4. Xuat CSV moi vao `dataset/processed/`.
5. Cap nhat `reports/DATASET_MANIFEST.md`.

Done khi:

- CSV moi co metadata.
- Script cu khong bi hong.
- Co test/command verify so cot va label distribution.

## TASK-102: Hoan thien video-wise evaluation

Muc tieu: danh gia model theo video, khong chi theo frame.

Pham vi:

- Sua `src/7_video_wise_evaluation.py`.
- Tao `reports/results/video_wise_metrics.csv`.
- Tao `reports/results/video_wise_summary.md`.

Buoc lam:

1. Doc CSV metadata moi.
2. Group theo `source_video`.
3. Tinh metric tung video.
4. Tinh mean/std va confidence interval.
5. Ghi limitations neu video qua it.

Done khi:

- Script chay duoc tu command line.
- Co bang metric theo video.

## TASK-103: Them benchmark nhieu thuat toan

Muc tieu: biet ANN co phai lua chon tot trong project khong.

Pham vi:

- Sua `src/8_compare_algorithms.py`.
- Benchmark Logistic Regression, KNN, SVM, Random Forest, XGBoost/LightGBM neu dependency co san, MLP/ANN, rule-based.

Buoc lam:

1. Kiem tra dependencies hien co.
2. Dung cung train/external split.
3. Standardize features cho model can thiet.
4. Tinh accuracy, precision, recall, F1, macro F1, MCC, ROC-AUC, PR-AUC.
5. Export `reports/results/algorithm_benchmark_full.csv`.

Done khi:

- Co bang comparison day du.
- Neu bo qua XGBoost vi chua cai, ghi ro ly do.

## TASK-104: Them prediction-level export va error analysis

Muc tieu: hieu model sai o dau.

Pham vi:

- Sua `src/6_evaluate_external.py`.
- Tao `reports/results/external_predictions.csv`.
- Tao `reports/ERROR_ANALYSIS.md`.

Buoc lam:

1. Export y_true, y_pred, probability, threshold, source metadata neu co.
2. Tach false positives va false negatives.
3. Thong ke loi theo video/label/confidence.
4. Neu co frame image, luu minh hoa top errors.

Done khi:

- Co prediction CSV.
- Co error analysis noi ro FN/FP chinh.

## TASK-105: Them ROC/PR curve va calibration

Muc tieu: danh gia threshold va do tin cay xac suat.

Pham vi:

- Cap nhat evaluator.
- Xuat `roc_curve.png`, `pr_curve.png`, `calibration_curve.png`.

Buoc lam:

1. Tinh ROC-AUC va PR-AUC.
2. Ve curve bang matplotlib.
3. Tinh Brier score.
4. De xuat threshold app mac dinh dua tren validation/external analysis.

Done khi:

- Cac hinh va metric duoc luu trong `reports/results/`.

## TASK-106: Feature normalization va ablation moi

Muc tieu: giam phu thuoc camera/vi tri nguoi.

Pham vi:

- Sua extractor/training pipeline de them normalized landmarks.
- Sua `src/9_ablation_study.py`.

Buoc lam:

1. Normalize landmark theo mid-shoulder/mid-hip.
2. Scale theo shoulder width/torso length.
3. Tao ablation: raw, normalized, ergonomic, raw+ergonomic, normalized+ergonomic.
4. Export `reports/results/ablation_full.csv`.

Done khi:

- Co ablation tren protocol ro.
- Biet feature group nao dong gop nhieu nhat.

## TASK-107: Temporal smoothing trong app

Muc tieu: giam nhap nhay canh bao va tang tinh dung trong realtime.

Pham vi:

- Sua `src/4_main_desktop_app.py`.
- Them setting smoothing window va alert duration.

Buoc lam:

1. Luu rolling probabilities.
2. Dung EMA hoac majority vote.
3. Chi canh bao khi sai lien tuc tren N giay.
4. Log ca raw prediction va smoothed prediction neu can.

Done khi:

- App chay on dinh.
- Co QA note ve smoothing.

## TASK-108: Runtime benchmark

Muc tieu: chung minh app realtime.

Pham vi:

- Tao `src/13_runtime_benchmark.py` hoac them mode benchmark.
- Tao `reports/RUNTIME_BENCHMARK.md`.

Buoc lam:

1. Do FPS voi webcam/video file.
2. Do latency MediaPipe + model + UI update.
3. Ghi CPU/RAM neu co the.
4. Test it nhat 2 do phan giai.

Done khi:

- Co bang FPS/latency.
- Co ket luan cau hinh may test.

## TASK-109: Figures va tables cho paper

Muc tieu: hoan thien minh hoa de viet bao cao.

Pham vi:

- Cap nhat `reports/FIGURE_TABLE_PLAN.md`.
- Export hinh/tables vao `reports/figures/` va `reports/tables/`.

Buoc lam:

1. Tao pipeline diagram.
2. Tao confusion matrix.
3. Tao threshold curve.
4. Tao TPRI distribution.
5. Chup GUI light/dark.

Done khi:

- Moi figure co caption.
- Moi table co source data.

## TASK-110: Related work verified citation

Muc tieu: chuan hoa doi chieu literature.

Pham vi:

- Cap nhat `reports/LITERATURE_METRICS_COMPARISON.md`.
- Cap nhat `reports/RELATED_WORK_TODO.md`.

Buoc lam:

1. Mo full paper/abstract source.
2. Ghi sensor, dataset, split, metric, limitation.
3. Danh dau muc nao khong the so sanh truc tiep.
4. Viet BibTeX neu can.

Done khi:

- Khong con claim mơ ho ve "tot hon".
- Moi metric co source ro.

## TASK-111: Data availability va ethics statement

Muc tieu: tranh thieu phan bat buoc trong bao cao nghien cuu.

Pham vi:

- Tao `reports/DATA_ETHICS_STATEMENT.md`.

Buoc lam:

1. Mo ta raw videos co public hay khong.
2. Mo ta privacy/face/body data.
3. Ghi intended use va khong dung cho diagnosis.
4. Ghi limitations ve consent/demographic neu thieu.

Done khi:

- Co statement san dua vao paper.

## TASK-112: Paper draft theo chuan Springer

Muc tieu: gom cac phan da co thanh ban draft.

Pham vi:

- Cap nhat `reports/springer_method_draft.md`.
- Cap nhat `reports/springer_results_draft.md`.
- Cap nhat `reports/springer_paper_outline.md`.

Buoc lam:

1. Dung contribution claim an toan.
2. Dua bang metric moi.
3. Dua limitations ro.
4. Them future work theo task con lai.

Done khi:

- Draft co day du abstract-style contribution, methods, results, discussion, limitations.

## TASK-113: Final QA va reproducibility run

Muc tieu: chot phien ban co the nop/bao cao.

Pham vi:

- Chay lai test, py_compile, scripts experiment.
- Tao `reports/FINAL_REPRODUCIBILITY_LOG.md`.

Buoc lam:

1. Ghi commit/hash neu co git.
2. Ghi command da chay.
3. Ghi output metric chinh.
4. Ghi loi con ton tai.

Done khi:

- Co log reproducibility.
- `pytest` pass.
- Main app init duoc.

## Thu tu uu tien

1. TASK-100
2. TASK-101
3. TASK-102
4. TASK-103
5. TASK-104
6. TASK-105
7. TASK-106
8. TASK-107
9. TASK-108
10. TASK-109
11. TASK-110
12. TASK-111
13. TASK-112
14. TASK-113

## Ket qua mong doi sau backlog

Sau khi hoan thanh, do an co the noi ro:

- Thuat toan nao tot nhat tren dataset cua do an.
- ANN co tot hon cac baseline local hay khong.
- Model co generalize theo video/person hay khong.
- Diem moi nam o dau: hybrid explainability, TPRI, realtime app, statistical workflow.
- Gioi han nam o dau: dataset size, protocol, sensor/camera bias, clinical/ergonomic validation.
