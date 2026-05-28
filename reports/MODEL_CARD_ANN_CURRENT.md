# Model Card ANN Current

Ngay cap nhat: 2026-05-27

## Model identity

| Hang muc | Gia tri |
|---|---|
| Model file | `models/ann_best.keras` |
| Scaler file | `models/scaler.pkl` |
| Model type | Dense ANN / MLP binary classifier |
| Task | Frame-level sitting posture classification |
| Output | Probability for `incorrect` posture |
| Default decision threshold | `0.50` |
| Suggested alert threshold to review | `0.10` from external F1 sweep |
| Label schema | `0=correct`, `1=incorrect` |

## Intended use

Model duoc dung trong desktop app de ho tro giam sat tu the lam viec theo thoi gian thuc bang webcam/video. Ket qua nen duoc xem la canh bao ho tro hanh vi, khong phai chan doan y te hay danh gia ergonomic chinh thuc.

## Out-of-scope use

- Khong dung de chan doan benh ly cot song/co/vai.
- Khong dung lam ergonomic certification.
- Khong dung cho moi truong an toan-critical.
- Khong nen dung de so sanh truc tiep voi nguoi khac neu chua co video-wise/person-wise protocol.

## Training data

| Hang muc | Gia tri |
|---|---:|
| Train CSV | `dataset/posture_data_2fps.csv` |
| Rows | 11022 |
| Columns | 100 |
| Feature columns | 99 |
| Correct frames | 4438 |
| Incorrect frames | 6584 |

CSV gom 33 MediaPipe Pose landmarks, moi landmark co 3 toa do `x/y/z`, va cot `label`. CSV hien tai chua co `source_video`, `frame_index`, `participant_id`, nen chua ho tro video-wise/person-wise validation that.

## External evaluation data

| Hang muc | Gia tri |
|---|---:|
| External CSV | `dataset/posture_external_test_2fps.csv` |
| Rows | 1697 |
| Columns | 100 |
| Correct frames | 768 |
| Incorrect frames | 929 |
| External videos | 10 |

## Feature schema

Feature dau vao la 99 cot:

- `landmark_0_x`, `landmark_0_y`, `landmark_0_z`
- ...
- `landmark_32_x`, `landmark_32_y`, `landmark_32_z`

Model dung `StandardScaler` luu tai `models/scaler.pkl`.

## Architecture

Kien truc theo `src/5_train_ann_local.py`:

1. Input 99 features.
2. Dense 128 ReLU.
3. BatchNormalization.
4. Dropout 0.30.
5. Dense 64 ReLU.
6. BatchNormalization.
7. Dropout 0.25.
8. Dense 32 ReLU.
9. Dropout 0.20.
10. Dense 1 sigmoid.

Training dung Adam learning rate `0.001`, binary cross-entropy, early stopping, model checkpoint, reduce learning rate on plateau, va class weights.

## Internal split metrics

Nguon: `models/local_training/metrics.txt`.

| Metric | Gia tri |
|---|---:|
| Internal test accuracy | 99.819% |
| Internal test precision incorrect | 99.899% |
| Internal test recall incorrect | 99.798% |
| Internal test F1 incorrect | 99.848% |
| Internal confusion matrix | `[[665, 1], [2, 986]]` |

Can dien giai can than: metric internal rat cao co the bi anh huong boi frame-level split va frame similarity. Khong nen dung metric nay de claim generalization.

## External metrics

Nguon: `reports/results/external_metrics.txt`.

| Threshold | Accuracy | Precision incorrect | Recall incorrect | F1 incorrect |
|---:|---:|---:|---:|---:|
| 0.50 | 79.316% | 94.599% | 65.985% | 77.743% |
| 0.10 | 80.436% | 91.286% | 71.044% | 79.903% |

Confusion matrix tai threshold 0.50:

|  | Pred correct | Pred incorrect |
|---|---:|---:|
| True correct | 733 | 35 |
| True incorrect | 316 | 613 |

## Comparison with local baseline

Nguon: `reports/results/algorithm_comparison.csv` va `reports/results/statistical_analysis.txt`.

| Model | Accuracy | Precision incorrect | Recall incorrect | F1 incorrect |
|---|---:|---:|---:|---:|
| ANN threshold 0.50 | 79.316% | 94.599% | 65.985% | 77.743% |
| Rule-based baseline | 56.629% | 58.443% | 71.905% | 64.479% |

ANN co accuracy va F1 cao hon baseline rule-based tren external frame-level set. McNemar paired test co p-value `2.19314e-60`, cho thay khac biet co y nghia thong ke tren tap frame hien tai.

## Known limitations

- External recall incorrect con thap, bo sot `316` incorrect frames tai threshold 0.50.
- Chua co video-wise/person-wise split vi CSV thieu metadata.
- Chua benchmark Logistic Regression, KNN, SVM, Random Forest, XGBoost tren cung split.
- Raw landmark coordinates chua duoc normalize theo body scale/camera position.
- Chua co ROC-AUC, PR-AUC, MCC, calibration curve trong evaluator hien tai.
- Chua co runtime/latency benchmark.
- Chua co clinical/ergonomic validation.

## Recommended next actions

1. Re-extract CSV co `source_video`, `frame_index`, `timestamp_sec`.
2. Chay video-wise evaluation.
3. Benchmark nhieu model tabular.
4. Them ROC/PR/calibration va prediction CSV.
5. Them temporal smoothing vao app.
6. Cap nhat threshold mac dinh dua tren muc tieu san pham: precision cao hay recall cao.

## Reporting statement

Statement an toan de dua vao bao cao:

> The ANN model significantly outperformed the local rule-based baseline on the external frame-level test set. However, video-wise/person-wise validation and broader algorithm benchmarks are required before claiming robust generalization or superiority over external methods.
