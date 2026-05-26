# 06. Task progress and next steps

Ngay cap nhat: 2026-05-26

## Da hoan thanh trong vong nay

| Task | Trang thai | Bang chung |
|---|---|---|
| TASK-001 README | Done | `README.md` viet lai, co cai dat/chay app/train/evaluation/demo video. |
| TASK-002 encoding file nho | Done | `src/config.py`, `src/utils.py`, `tests/test_imports.py`, `tests/test_camera.py` sach mojibake. |
| TASK-003 dataset manifest | Done | `reports/DATASET_MANIFEST.md`. |
| TASK-004 experiment protocol | Done | `reports/EXPERIMENT_PROTOCOL.md`. |
| TASK-005 manual webcam tests | Done | Pytest khong mo webcam; HEVC sample skip neu thieu. |
| TASK-006 utils test | Done | `tests/test_utils.py`. |
| TASK-007 shared baseline module | Done | `src/posture_baseline.py`; baseline script import module chung. |
| TASK-008 GUI dung baseline module chung | Partial done | GUI import override sang `posture_baseline.py`; code cu chua xoa het. |
| TASK-009 baseline tests | Done | `tests/test_posture_baseline.py`. |
| TASK-011 external evaluation | Done | `src/6_evaluate_external.py`, output trong `reports/results/`. |
| TASK-012 threshold sweep | Done | `reports/results/external_threshold_sweep.csv`. |
| TASK-013 video-wise readiness | Done | `src/7_video_wise_evaluation.py`, tao protocol khi thieu metadata. |
| TASK-014 metadata extraction option | Done | `src/2_extract_features.py --include-metadata`. |
| TASK-015 train accepts metadata | Done | `src/5_train_ann_local.py` chon cot `landmark_*`. |
| TASK-016 smoke train | Done | `--max-rows` da chay pass voi 400 rows. |
| TASK-017 ANN vs rule-based | Done | `src/8_compare_algorithms.py`, `algorithm_comparison.csv`. |
| TASK-018 ablation small | Done | `src/9_ablation_study.py`, `ablation_results.csv`. |
| TASK-020 export statistics | Done | `src/10_export_statistics.py`; local session exports khong commit de tranh dua log rieng tu len Git. |
| TASK-022 video demo docs | Done | README co huong dan video file. |
| TASK-023 GUI QA checklist | Done | `reports/GUI_QA_CHECKLIST.md`. |
| TASK-024 Springer outline | Done | `reports/springer_paper_outline.md`. |
| TASK-025 Method draft | Done | `reports/springer_method_draft.md`. |
| TASK-026 Results draft | Done | `reports/springer_results_draft.md` da co external metrics. |
| TASK-027 figure/table plan | Done | `reports/FIGURE_TABLE_PLAN.md`. |
| TASK-028 related work todo | Done | `reports/RELATED_WORK_TODO.md`. |
| TASK-029 final checklist | Done | `reports/FINAL_DELIVERY_CHECKLIST.md`. |
| TASK-030 technical debt | Done | `reports/TECHNICAL_DEBT.md`. |

## Ket qua kiem thu

```text
pytest: 10 passed, 1 skipped
py_compile: pass for src/1..10 scripts and posture_baseline.py
external ANN F1: 0.777425 at threshold 0.5
best external sweep F1: 0.799031 at threshold 0.10
```

## Task moi sau self-review

### TASK-031 - Xoa han logic baseline copy trong GUI

Pham vi: `src/4_main_desktop_app.py`

Muc tieu: sau khi da import `posture_baseline.py`, xoa cac constant/function baseline cu trong GUI neu khong con dung, giu app compile va baseline mode van hien thi du feature.

Verify:

```powershell
python -m py_compile src/4_main_desktop_app.py src/posture_baseline.py
python -m pytest tests/test_posture_baseline.py
```

### TASK-032 - Re-extract CSV co metadata va chay video-wise split that

Pham vi: `src/7_video_wise_evaluation.py`, dataset CSV moi.

Muc tieu: tao `dataset/posture_data_2fps_with_metadata.csv`, sau do train/evaluate theo split `source_video`.

Verify:

```powershell
python src/2_extract_features.py --include-metadata --output dataset/posture_data_2fps_with_metadata.csv
python src/7_video_wise_evaluation.py --dataset dataset/posture_data_2fps_with_metadata.csv
```

### TASK-033 - Lam sach output TensorFlow/sklearn warnings

Pham vi: `src/6_evaluate_external.py`, `src/8_compare_algorithms.py`, docs requirements.

Muc tieu: giam log TensorFlow oneDNN trong terminal va xu ly warning version mismatch cua `scaler.pkl` bang cach ghi ro sklearn version dung de train.

Verify:

```powershell
python src/6_evaluate_external.py
```

### TASK-034 - Manual GUI QA va screenshot

Pham vi: `reports/GUI_QA_CHECKLIST.md`, `reports/figures/`.

Muc tieu: chay app voi webcam/video, tick checklist, chup screenshot GUI va sample landmark overlay cho paper.

Verify: checklist co ngay test/nguoi test/ket qua.

### TASK-035 - Cap nhat paper voi citation that

Pham vi: `reports/RELATED_WORK_TODO.md`, `reports/springer_paper_outline.md`.

Muc tieu: them citation that cho MediaPipe Pose, ergonomic posture, posture detection ML, real-time feedback. Khong dung citation tu bia.
