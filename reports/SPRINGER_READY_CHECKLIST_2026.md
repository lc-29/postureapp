# Springer Ready Checklist 2026

Ngay cap nhat: 2026-05-27

## Muc tieu

Checklist nay danh gia muc do san sang cua do an neu viet theo chuan bao cao nghien cuu/Springer.

## Trang thai tong quan

| Hang muc | Trang thai | Muc san sang |
|---|---|---|
| Problem statement | Da co | 70% |
| System pipeline | Da co | 80% |
| GUI/app implementation | Da co | 85% |
| Dataset manifest | Da co | 65% |
| Feature schema | Da co | 60% |
| ANN model | Da co | 70% |
| Rule-based baseline | Da co | 75% |
| External evaluation | Da co | 70% |
| Statistical tests | Da co | 75% |
| Video-wise evaluation | Chua runnable | 20% |
| Person-wise evaluation | Chua co | 0% |
| Algorithm benchmark | Chua day du | 25% |
| Error analysis | Chua co | 10% |
| Runtime analysis | Chua co | 10% |
| Figures/tables | Mot phan | 45% |
| Model card | Chua co | 0% |
| Data/ethics statement | Chua co | 0% |

## Paper structure de xuat

1. Introduction
2. Related Work
3. Materials and Methods
4. System Design
5. Experimental Protocol
6. Results
7. Discussion
8. Limitations
9. Conclusion and Future Work

## Cac bang nen co

| Bang | Trang thai | Ghi chu |
|---|---|---|
| Dataset statistics | Da co mot phan | Can them metadata video/person. |
| Feature groups | Can bo sung | Tach raw landmarks, ergonomic, temporal. |
| Model comparison | Can bo sung | ANN, rule, KNN, SVM, RF, XGBoost. |
| External metrics | Da co | Can them MCC, ROC-AUC, PR-AUC. |
| Ablation study | Da co mot phan | Can chay lai tren protocol ro. |
| Runtime benchmark | Chua co | FPS, latency, CPU/RAM. |
| Literature comparison | Da co mot phan | Can cite chuan va tranh so sanh truc tiep qua dataset khac. |

## Cac hinh nen co

| Hinh | Trang thai | Ghi chu |
|---|---|---|
| System pipeline | Can tao | Camera -> MediaPipe -> features -> model/rules -> app/log/dashboard. |
| GUI screenshot light/dark | Can tao | Phuc vu implementation/results. |
| Confusion matrix | Can export | External test. |
| ROC/PR curves | Chua co | Can update evaluator. |
| Threshold-F1 curve | Da co y tuong | Can export thanh image. |
| TPRI distribution | Can tao | Histogram/session risk groups. |
| Error examples | Can tao | False positive/false negative frames neu co frame export. |

## Minimum de viet bai tot nghiep/khoa luan

Can hoan thanh:

- Model card.
- Error analysis.
- Runtime benchmark.
- Bang comparison voi baseline.
- Hinh pipeline va screenshots app.
- Limitations viet ro.

## Minimum de nop bai theo huong Springer workshop/chapter

Can hoan thanh them:

- Video-wise split.
- Benchmark nhieu model.
- ROC-AUC/PR-AUC/MCC.
- Statistical comparison giua cac model.
- Related work verified citation.
- Data availability/ethics statement.

## Minimum de claim robust generalization

Can hoan thanh:

- Person-wise split.
- Dataset lon hon, nhieu nguoi, nhieu camera angles.
- External test doc lap hon.
- Confidence interval theo video/person, khong chi theo frame.
- Robustness theo lighting/background/distance.

## Claim boundary

Duoc viet:

- "The proposed system outperformed the local rule-based baseline on the external frame-level test set."
- "The system provides realtime monitoring, interpretable alerts, and session-level risk summaries."
- "The current evaluation provides preliminary evidence for feasibility."

Khong nen viet:

- "The proposed method is superior to existing methods."
- "The dataset is a benchmark."
- "The model is clinically validated."
- "The system provides medical diagnosis."

## Readiness verdict

Hien tai do an san sang cho **demo tot nghiep va applied system report**. De len muc bai theo chuan Springer, can uu tien protocol danh gia va benchmark truoc khi mo rong them giao dien.
