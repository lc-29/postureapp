# Final Results Tables

Ngay cap nhat: 2026-05-28

## Table 1. Dataset statistics

| Split | Videos | Rows | Correct rows | Incorrect rows |
|---|---:|---:|---:|---:|
| Raw training | 84 | 11022 | 4438 | 6584 |
| Corrected external | 10 | 1658 | 768 | 890 |

## Table 2. Selected model

| Item | Value |
|---|---|
| Model ID | `hist_gradient_boosting__normalized_99` |
| Algorithm | HistGradientBoosting |
| Feature set | `normalized_99` |
| Feature count | 99 |
| Selected threshold | 0.65 |
| Registry | `models/model_registry.json` |

## Table 3. Corrected external frame-level result

| Metric | Value |
|---|---:|
| Accuracy | 96.502% |
| Accuracy 95% CI | [95.504%, 97.284%] |
| Precision incorrect | 96.222% |
| Recall incorrect | 97.303% |
| F1 incorrect | 96.760% |
| F1 95% bootstrap CI | [95.859%, 97.607%] |
| Macro-F1 | 96.480% |
| MCC | 92.966% |
| ROC-AUC | 99.088% |
| PR-AUC | 99.213% |
| False positives | 34 |
| False negatives | 24 |

## Table 4. Model selection top results

Source: `reports/MODEL_SELECTION_REPORT.md`

| Model | Feature set | Accuracy | F1 incorrect | MCC |
|---|---|---:|---:|---:|
| HistGradientBoosting | normalized_99 | 95.959% | 96.284% | 91.893% |
| Random Forest | normalized_99 | 95.899% | 96.243% | 91.792% |
| SVM RBF | ergonomic_14 | 95.356% | 95.618% | 90.715% |
| SVM RBF | normalized_99 | 94.512% | 95.008% | 89.043% |
| Random Forest | combined_normalized_ergonomic | 94.270% | 94.834% | 88.647% |

## Table 5. Participant-wise result for selected model

| Participant held out | Accuracy | F1 incorrect | MCC |
|---|---:|---:|---:|
| P01 | 90.806% | 91.089% | 82.636% |
| P02 | 79.347% | 84.158% | 56.552% |
| P03 | 93.025% | 94.701% | 85.551% |
| P04 | 86.667% | 88.498% | 75.922% |
| P05 | 93.556% | 94.928% | 86.111% |
| Mean | 88.680% | 90.675% | 77.355% |

## Table 6. Temporal smoothing effect

| Method | Accuracy | False positives | False negatives |
|---|---:|---:|---:|
| Frame-level final model | 96.502% | 34 | 24 |
| 5-second temporal mean | 97.648% | 31 | 8 |

## Table 7. Main remaining limitations

| Limitation | Impact | Fix |
|---|---|---|
| Corrected external set currently has P01 only | Weak participant-independent claim | Add external videos from new participants. |
| Model final not yet integrated into Tkinter app | App still uses older ANN by default | Load `models/model_registry.json` in app. |
| Error taxonomy first-pass inferred | Needs manual review for paper figures | Review exported frames manually. |
| No clinical/ergonomic expert validation | Cannot claim medical/official ergonomic assessment | Add expert annotation or RULA-inspired comparison. |

