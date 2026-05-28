# Final Reproducibility Log

Ngay cap nhat: 2026-05-27

## Commands executed

```powershell
.\.venv\Scripts\python.exe src/2_extract_features.py --input-root dataset/external_videos --sample-fps 2 --include-metadata --output dataset/processed/posture_external_test_2fps_with_metadata.csv
```

Ket qua: tao external metadata CSV voi 1697 rows va 108 columns.

```powershell
.\.venv\Scripts\python.exe src/6_evaluate_external.py --dataset dataset/processed/posture_external_test_2fps_with_metadata.csv
```

Ket qua chinh:

- Accuracy: 0.793164
- Precision incorrect: 0.945988
- Recall incorrect: 0.659849
- F1 incorrect: 0.777425
- Macro F1: 0.792125
- MCC: 0.629328
- ROC-AUC: 0.950458
- PR-AUC: 0.957466
- Brier score: 0.186415

```powershell
.\.venv\Scripts\python.exe src/7_video_wise_evaluation.py --dataset dataset/processed/posture_external_test_2fps_with_metadata.csv
```

Ket qua chinh:

- Unique source videos: 10
- Mean video accuracy: 0.824817
- Std video accuracy: 0.287630
- Mean video F1 incorrect: 0.377173

```powershell
.\.venv\Scripts\python.exe src/8_compare_algorithms.py --dataset dataset/processed/posture_external_test_2fps_with_metadata.csv
```

Ket qua chinh:

- Random Forest dat accuracy 0.870359 va F1 incorrect 0.883721.
- ANN dat accuracy 0.793164 va F1 incorrect 0.777425.
- Rule-based dat accuracy 0.567472 va F1 incorrect 0.646095.

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
- Random Forest dang tot hon ANN tren external benchmark, nhung chua duoc dong goi vao app.
