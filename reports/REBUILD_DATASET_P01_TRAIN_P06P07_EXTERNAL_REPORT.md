# Rebuild Dataset P01 Train - P06/P07 External Report

- Updated: 2026-06-25 03:42:10
- Task: `workflow_kilo/20_TASK_REBUILD_DATASET_P01_TRAIN_P06P07_EXTERNAL_BENCHMARK.md`
- Backup folder: `outputs\backups\rebuild_dataset_p06_p07_20260625_024450`
- Protocol status: **completed**

## 1. Split Moi

Cac video external P01 cu da duoc dua vao raw/train vi P01 da xuat hien trong dataset goc. External final moi dung P06 va P07 de kiem tra unseen participants.

| Split | Videos | Participants | Correct videos | Incorrect videos | Purpose |
|---|---:|---|---:|---:|---|
| Raw/development | 94 | P01-P05 | 39 | 55 | Train/model selection development |
| External unseen-participant | 23 | P06-P07 | 11 | 12 | Final external test on new people |

## 2. Dataset Manifest Moi

### Raw by Participant and Label

| participant_id | label_name | count |
| --- | --- | --- |
| P01 | correct | 14 |
| P01 | incorrect | 15 |
| P02 | correct | 4 |
| P02 | incorrect | 7 |
| P03 | correct | 6 |
| P03 | incorrect | 12 |
| P04 | correct | 7 |
| P04 | incorrect | 9 |
| P05 | correct | 8 |
| P05 | incorrect | 12 |

### External by Participant and Label

| participant_id | label_name | count |
| --- | --- | --- |
| P06 | correct | 5 |
| P06 | incorrect | 5 |
| P07 | correct | 6 |
| P07 | incorrect | 7 |

### Raw by View Angle and Label

| view_angle | label_name | count |
| --- | --- | --- |
| front | correct | 9 |
| front | incorrect | 15 |
| side_30 | correct | 8 |
| side_30 | incorrect | 9 |
| side_90 | correct | 17 |
| side_90 | incorrect | 26 |
| unknown | correct | 5 |
| unknown | incorrect | 5 |

### External by View Angle and Label

| view_angle | label_name | count |
| --- | --- | --- |
| front | correct | 3 |
| front | incorrect | 4 |
| side_30 | correct | 3 |
| side_30 | incorrect | 4 |
| side_90 | correct | 5 |
| side_90 | incorrect | 4 |

## 3. CSV Shape Moi

| File | Shape | Participants | Label Distribution |
|---|---:|---|---|
| `posture_data_2fps_with_metadata.csv` | 12680 x 108 | P01, P02, P03, P04, P05 | {0: 5206, 1: 7474} |
| `posture_external_test_2fps_with_metadata.csv` | 4556 x 108 | P06, P07 | {0: 2001, 1: 2555} |
| `posture_data_2fps_combined_features.csv` | 12680 x 122 | P01, P02, P03, P04, P05 | {0: 5206, 1: 7474} |
| `posture_external_test_2fps_combined_features.csv` | 4556 x 122 | P06, P07 | {0: 2001, 1: 2555} |

## 4. Benchmark Moi

### Top Model Registry Results

| model_id | feature_set | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | macro_f1 | mcc | roc_auc | pr_auc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| random_forest__ergonomic_14 | ergonomic_14 | 82.16% | 79.47% | 91.94% | 85.25% | 81.34% | 0.6405 | 0.8222 | 0.8487 |
| logistic_regression__ergonomic_14 | ergonomic_14 | 83.54% | 94.74% | 74.79% | 83.60% | 83.54% | 0.6944 | 0.9226 | 0.9335 |
| random_forest__normalized_99 | normalized_99 | 77.17% | 74.84% | 89.32% | 81.44% | 75.90% | 0.5378 | 0.8585 | 0.8855 |
| hist_gradient_boosting__ergonomic_14 | ergonomic_14 | 79.13% | 82.44% | 79.77% | 81.08% | 78.90% | 0.5786 | 0.8442 | 0.8602 |
| hist_gradient_boosting__combined_normalized_ergonomic | combined_normalized_ergonomic | 77.70% | 80.55% | 79.41% | 79.98% | 77.41% | 0.5483 | 0.8121 | 0.8478 |
| random_forest__combined_raw_ergonomic | combined_raw_ergonomic | 69.36% | 64.95% | 98.55% | 78.30% | 63.10% | 0.4269 | 0.7830 | 0.8086 |
| random_forest__raw_99 | raw_99 | 69.27% | 64.92% | 98.36% | 78.21% | 63.05% | 0.4234 | 0.7320 | 0.7379 |
| svm_rbf__combined_normalized_ergonomic | combined_normalized_ergonomic | 73.42% | 72.46% | 84.85% | 78.17% | 72.10% | 0.4565 | 0.7680 | 0.8108 |
| hist_gradient_boosting__raw_99 | raw_99 | 67.08% | 63.06% | 99.69% | 77.25% | 58.84% | 0.3931 | 0.5470 | 0.6002 |
| hist_gradient_boosting__normalized_99 | normalized_99 | 67.38% | 63.62% | 97.69% | 77.06% | 60.32% | 0.3785 | 0.7002 | 0.7641 |

Selected model: `random_forest__ergonomic_14`.

### Top Classifier Benchmark Results

| algorithm | feature_set | accuracy | precision | recall | f1 | macro_f1 | mcc | roc_auc | pr_auc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Random Forest | ergonomic | 81.89% | 79.52% | 91.19% | 84.96% | 81.11% | 0.6341 | 0.8222 | 0.8487 |
| Logistic Regression | ergonomic | 83.54% | 94.74% | 74.79% | 83.60% | 83.54% | 0.6944 | 0.9226 | 0.9335 |
| HistGradientBoosting | ergonomic | 79.13% | 82.44% | 79.77% | 81.08% | 78.90% | 0.5786 | 0.8442 | 0.8602 |
| Random Forest | raw | 69.38% | 65.02% | 98.28% | 78.26% | 63.25% | 0.4249 | 0.7320 | 0.7379 |
| Random Forest | combined | 69.29% | 64.92% | 98.43% | 78.24% | 63.05% | 0.4245 | 0.7830 | 0.8086 |
| HistGradientBoosting | raw | 67.08% | 63.06% | 99.69% | 77.25% | 58.84% | 0.3931 | 0.5470 | 0.6002 |
| HistGradientBoosting | combined | 65.39% | 61.89% | 99.65% | 76.35% | 55.90% | 0.3569 | 0.8333 | 0.8701 |
| KNN | ergonomic | 73.05% | 78.74% | 71.15% | 74.75% | 72.92% | 0.4628 | 0.8035 | 0.8148 |
| SVM RBF | combined | 60.56% | 58.71% | 100.00% | 73.98% | 46.24% | 0.2446 | 0.6628 | 0.7297 |
| SVM RBF | raw | 57.62% | 56.95% | 100.00% | 72.57% | 39.67% | 0.1412 | 0.6460 | 0.6909 |

## 5. Threshold Calibration

| threshold | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | mcc | false_positive | false_negative |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.5000 | 82.16% | 79.47% | 91.94% | 85.25% | 0.6405 | 607 | 206 |
| 0.4500 | 80.09% | 76.03% | 94.21% | 84.15% | 0.6066 | 759 | 148 |
| 0.5500 | 76.80% | 79.44% | 79.10% | 79.27% | 0.5293 | 523 | 534 |
| 0.4000 | 70.87% | 66.97% | 94.83% | 78.50% | 0.4310 | 1195 | 132 |
| 0.3500 | 64.33% | 61.74% | 95.69% | 75.06% | 0.2941 | 1515 | 110 |
| 0.3000 | 62.47% | 60.37% | 96.28% | 74.21% | 0.2515 | 1615 | 95 |
| 0.2500 | 59.02% | 58.04% | 97.22% | 72.68% | 0.1553 | 1796 | 71 |
| 0.1000 | 57.09% | 56.66% | 99.88% | 72.30% | 0.1089 | 1952 | 3 |

Selected threshold used in final evaluation: `0.50`.

## 6. Final External Metrics P06-P07

| Metric | Value |
|---|---:|
| Samples | 4556 |
| Accuracy | 82.16% |
| Precision Incorrect | 79.47% |
| Recall Incorrect | 91.94% |
| F1 Incorrect | 85.25% |
| Macro F1 | 81.34% |
| MCC | 0.6405 |
| ROC-AUC | 0.8222 |
| PR-AUC | 0.8487 |
| False Positive | 607 |
| False Negative | 206 |

Confusion matrix moi da xuat tai:

```text
reports/figures/external_confusion_matrix.png
reports/figures/external_threshold_sweep.png
```

## 7. Video-wise Error Summary

| source_video | participant_id | label | n | accuracy | f1_incorrect | false_positive | false_negative |
| --- | --- | --- | --- | --- | --- | --- | --- |
| dataset\external_videos\correct\P06_correct_side_90_002.mp4 | P06 | 0 | 160 | 0.00% | 0.00% | 160 | 0 |
| dataset\external_videos\correct\P06_correct_side_90_001.mp4 | P06 | 0 | 190 | 7.89% | 0.00% | 175 | 0 |
| dataset\external_videos\correct\P07_correct_side_90_003.mp4 | P07 | 0 | 230 | 33.91% | 0.00% | 152 | 0 |
| dataset\external_videos\correct\P06_correct_side_30_001.mp4 | P06 | 0 | 157 | 42.68% | 0.00% | 90 | 0 |
| dataset\external_videos\incorrect\P07_incorrect_side_30_002.mp4 | P07 | 1 | 238 | 58.40% | 73.74% | 0 | 99 |
| dataset\external_videos\incorrect\P07_incorrect_front_002.mp4 | P07 | 1 | 201 | 81.59% | 89.86% | 0 | 37 |
| dataset\external_videos\incorrect\P07_incorrect_side_90_002.mp4 | P07 | 1 | 246 | 88.62% | 93.97% | 0 | 28 |
| dataset\external_videos\correct\P06_correct_front_001.mp4 | P06 | 0 | 179 | 90.50% | 0.00% | 17 | 0 |
| dataset\external_videos\incorrect\P07_incorrect_front_003.mp4 | P07 | 1 | 206 | 94.66% | 97.26% | 0 | 11 |
| dataset\external_videos\incorrect\P07_incorrect_side_90_001.mp4 | P07 | 1 | 234 | 94.87% | 97.37% | 0 | 12 |
| dataset\external_videos\incorrect\P06_incorrect_side_30_002.mp4 | P06 | 1 | 192 | 95.31% | 97.60% | 0 | 9 |
| dataset\external_videos\correct\P06_correct_front_002.mp4 | P06 | 0 | 100 | 97.00% | 0.00% | 3 | 0 |

Nhan xet quan trong:

- External P06-P07 kho hon external P01 cu, nen accuracy/f1 giam la ket qua hop ly va co gia tri khoa hoc.
- Nhieu false positive tap trung o video correct side_90 cua P06, dac biet `P06_correct_side_90_002.mp4` va `P06_correct_side_90_001.mp4`.
- Day la bang chung can phan tich trong Error Analysis/Future Work: model dang nhay voi goc side_90 cua nguoi moi.

## 8. Participant-wise Raw Evaluation

| held_out_participant | n | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | mcc | false_positive | false_negative |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P01 | 5182 | 84.89% | 83.39% | 90.46% | 86.78% | 0.6953 | 512 | 271 |
| P02 | 1225 | 88.82% | 85.92% | 97.28% | 91.25% | 0.7706 | 117 | 20 |
| P03 | 2208 | 82.16% | 88.89% | 84.82% | 86.81% | 0.5945 | 162 | 232 |
| P04 | 1815 | 74.88% | 67.12% | 100.00% | 80.33% | 0.5701 | 456 | 0 |
| P05 | 2250 | 88.00% | 90.40% | 90.90% | 90.65% | 0.7390 | 139 | 131 |

## 9. Feature Importance

Top feature importance cua selected model:

| feature | importance_mean | importance_std |
| --- | --- | --- |
| nose_shoulder_clearance_ratio | 0.2034 | 0.0000 |
| nose_to_shoulder_y | 0.1409 | 0.0000 |
| head_shoulder_distance | 0.1028 | 0.0000 |
| min_hand_mouth_ratio | 0.0916 | 0.0000 |
| head_offset_x | 0.0621 | 0.0000 |
| right_hand_mouth_ratio | 0.0575 | 0.0000 |
| torso_lean_angle | 0.0573 | 0.0000 |
| chin_rest_detected | 0.0565 | 0.0000 |
| shoulder_width | 0.0507 | 0.0000 |
| torso_length | 0.0495 | 0.0000 |
| left_hand_mouth_ratio | 0.0489 | 0.0000 |
| shoulder_y_diff | 0.0428 | 0.0000 |
| shoulder_tilt_angle | 0.0261 | 0.0000 |
| neck_compression_detected | 0.0099 | 0.0000 |

## 10. Artifact Da Cap Nhat

- `dataset/metadata/video_manifest.csv`
- `reports/DATASET_VIDEO_MANIFEST_SUMMARY.md`
- `dataset/posture_data_2fps.csv`
- `dataset/posture_external_test_2fps.csv`
- `dataset/processed/posture_data_2fps_with_metadata.csv`
- `dataset/processed/posture_external_test_2fps_with_metadata.csv`
- `dataset/processed/posture_data_2fps_ergonomic_features.csv`
- `dataset/processed/posture_external_test_2fps_ergonomic_features.csv`
- `dataset/processed/posture_data_2fps_combined_features.csv`
- `dataset/processed/posture_external_test_2fps_combined_features.csv`
- `reports/results/classifier_benchmark_external.csv`
- `models/model_registry.json`
- `models/registry/`
- `reports/MODEL_SELECTION_REPORT.md`
- `reports/results/model_registry_metrics.csv`
- `reports/results/threshold_calibration_final.csv`
- `reports/THRESHOLD_CALIBRATION_REPORT.md`
- `reports/results/final_evaluation_metrics.csv`
- `reports/results/final_external_predictions.csv`
- `reports/results/final_video_wise_metrics.csv`
- `reports/results/final_participant_wise_metrics.csv`
- `reports/FINAL_EVALUATION_REPORT.md`
- `reports/results/error_taxonomy.csv`
- `reports/ERROR_TAXONOMY_REPORT.md`
- `reports/results/temporal_window_features.csv`
- `reports/TEMPORAL_RISK_INDEX_VALIDATION.md`
- `reports/results/feature_importance.csv`
- `reports/FEATURE_IMPORTANCE_REPORT.md`
- `reports/figures/external_confusion_matrix.png`
- `reports/figures/external_threshold_sweep.png`
- `reports/figures/temporal_smoothing_effect.png`
- `reports/figures/feature_importance_top20.png`

## 11. Diem Can Luu Y

- Ket qua final moi khong duoc so sanh truc tiep nhu leaderboard voi external P01 cu vi protocol da doi.
- External moi P06-P07 la unseen-participant test set, nen ket qua giam nhung hoc thuat manh hon.
- App desktop hien tai can duoc kiem tra lai neu muon su dung selected model moi `random_forest__ergonomic_14` trong demo. Neu app van dang hard-code HGB mode cu, can them task rieng de dong bo app voi registry selected model.
- Raw co 10 video legacy P01 khong co `front/side_30/side_90` trong ten, nen view_angle cua cac video nay la `unknown`. Neu can phan tich view-angle sach hon, nen doi ten P01 legacy theo view that su sau khi xem video.

## 12. Ket Luan

Pipeline da duoc rebuild theo protocol moi:

```text
Train/development: P01-P05, 94 videos, 12680 frame samples
External unseen-participant: P06-P07, 23 videos, 4556 frame samples
Selected model: random_forest__ergonomic_14
External F1 Incorrect: 85.25%
External Accuracy: 82.16%
```

Protocol moi phu hop hon de viet luan van/bai bao vi external set hien test tren nguoi moi P06-P07 thay vi P01 da co trong du lieu goc.
