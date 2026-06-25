# Final Reproducibility Log

Ngay cap nhat: 2026-05-28

## Correction note

Ngay 2026-05-28, `dataset/external_videos/incorrect/P01_incorrect_004.mp4`
da duoc thay bang video sai tu the dung sau khi phat hien noi dung cu bi nhap
nham la video dung tu the. Cac lenh external evaluation ben duoi da duoc chay
lai tren external dataset da sua.

## Commands executed

```powershell
.\.venv\Scripts\python.exe src/2_extract_features.py --input-root dataset/external_videos --sample-fps 2 --include-metadata --output dataset/processed/posture_external_test_2fps_with_metadata.csv
```

Ket qua: tao external metadata CSV voi 1658 rows va 108 columns.

```powershell
.\.venv\Scripts\python.exe src/6_evaluate_external.py --dataset dataset/processed/posture_external_test_2fps_with_metadata.csv
```

Ket qua chinh:

- Accuracy: 0.901689
- Precision incorrect: 0.956085
- Recall incorrect: 0.856180
- F1 incorrect: 0.903379
- Macro F1: 0.901659
- MCC: 0.809012
- ROC-AUC: 0.982257
- PR-AUC: 0.985054
- Brier score: 0.078710

```powershell
.\.venv\Scripts\python.exe src/7_video_wise_evaluation.py --dataset dataset/processed/posture_external_test_2fps_with_metadata.csv
```

Ket qua chinh:

- Unique source videos: 10
- Mean video accuracy: 0.900001
- Std video accuracy: 0.117696
- Mean video F1 incorrect: 0.459245

```powershell
.\.venv\Scripts\python.exe src/8_compare_algorithms.py --dataset dataset/processed/posture_external_test_2fps_with_metadata.csv
```

Ket qua chinh:

- SVM RBF dat accuracy 0.911942 va F1 incorrect 0.915802 tren raw landmark benchmark.
- ANN dat accuracy 0.901689 va F1 incorrect 0.903379.
- Rule-based dat accuracy 0.674910 va F1 incorrect 0.753994.

```powershell
.\.venv\Scripts\python.exe src/9_ablation_study.py --dataset dataset/posture_data_2fps.csv
```

Ket qua chinh:

- `normalized_plus_ergonomic` dat accuracy 0.934240 va F1 0.944381 tren split noi bo frame-level.

```powershell
.\.venv\Scripts\python.exe src/13_runtime_benchmark.py --max-frames 120 --frame-stride 15 --width 640 --height 360
```

Ket qua chinh:

- Mean total latency: 27.908 ms
- P95 total latency: 30.026 ms
- Estimated processing FPS: 35.831

```powershell
.\.venv\Scripts\python.exe src/14_generate_paper_artifacts.py
```

Ket qua: sinh `reports/figures/`, `reports/tables/`, va `reports/PAPER_ARTIFACTS.md`.

## Verification

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
```

Ket qua: `20 passed, 1 skipped`.

```powershell
.\.venv\Scripts\python.exe -m py_compile src/1_rule_based_baseline.py src/2_extract_features.py src/3_database_setup.py src/4_main_desktop_app.py src/5_train_ann_local.py src/6_evaluate_external.py src/7_video_wise_evaluation.py src/8_compare_algorithms.py src/9_ablation_study.py src/10_export_statistics.py src/11_statistical_analysis.py src/12_temporal_risk_index.py src/13_runtime_benchmark.py src/14_generate_paper_artifacts.py src/posture_baseline.py src/statistics_service.py src/utils.py
```

Ket qua: pass.

```powershell
$env:TF_CPP_MIN_LOG_LEVEL='3'; python -c "import importlib.util; from pathlib import Path; p=Path('src/4_main_desktop_app.py').resolve(); spec=importlib.util.spec_from_file_location('main_app', p); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); app=mod.PostureApp(); print('app init ok', app.current_theme_mode, app.smoothing_window_frames, app.smoothing_threshold); app.destroy()"
```

Ket qua: `app init ok light 5 0.5`.

## Remaining limitations

- Full training metadata CSV chua duoc re-extract vi raw train videos lon.
- Person-wise validation chua hoan thien.
- GUI screenshots light/dark can chup manual.
- SVM RBF/ergonomic va SVM RBF/raw dang tot hon ANN trong mot so benchmark external, nhung chua duoc dong goi vao app.
