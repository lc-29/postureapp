# Algorithm Upgrade And Comparison Plan

Ngay cap nhat: 2026-05-27

## Muc tieu

File nay danh gia thuat toan hien tai va de xuat lo trinh nang cap de do an tot hon, day du hon, va bao cao duoc theo chuan nghien cuu.

## Trang thai thuat toan hien tai

Pipeline hien tai:

1. Doc webcam/video/IP camera.
2. MediaPipe Pose trich xuat 33 landmarks.
3. Tao vector 99 dac trung `x/y/z`.
4. ANN binary classifier du doan `correct`/`incorrect`.
5. Rule-based baseline sinh canh bao giai thich.
6. App ghi log SQLite va tinh thong ke/risk theo phien.

## Metric hien tai

| Hang muc | Gia tri |
|---|---:|
| External samples | 1697 frames |
| ANN accuracy threshold 0.5 | 79.316% |
| ANN precision incorrect threshold 0.5 | 94.599% |
| ANN recall incorrect threshold 0.5 | 65.985% |
| ANN F1 incorrect threshold 0.5 | 77.743% |
| ANN best F1 threshold 0.10 | 79.903% |
| Rule-based accuracy | 56.629% |
| Rule-based F1 incorrect | 64.479% |
| McNemar p-value ANN vs rule-based | 2.19314e-60 |

Nhan xet:

- ANN tot hon rule-based baseline local tren external frame-level set.
- Precision incorrect cao, nhung recall incorrect con thap; app co nguy co bo sot nhieu frame sai tu the.
- Threshold 0.10 dang hop ly hon neu uu tien canh bao som, nhung can calibration va UX tuning.

## Diem yeu ky thuat

| Diem yeu | Tac dong | Muc uu tien |
|---|---|---|
| Chua co `source_video`/`frame_index` trong CSV | Khong chay duoc video-wise validation that | Cao |
| Chua co `participant_id` | Khong biet model co generalize sang nguoi moi khong | Cao |
| Raw coordinates chua normalize | De nhay voi vi tri camera/kich thuoc nguoi | Cao |
| Chua benchmark KNN/SVM/RF/XGBoost | Khong biet ANN co that su la lua chon tot nhat | Cao |
| Chua co ROC-AUC/PR-AUC/MCC | Metric chua du cho paper | Trung binh-cao |
| Chua co temporal smoothing/model | Posture la tin hieu lien tuc nhung model dang frame-level | Cao |
| Chua co error analysis | Khong biet FN/FP xay ra o tu the/goc nhin nao | Cao |
| Chua co runtime benchmark | Chua chung minh realtime mot cach dinh luong | Trung binh |

## Nang cap feature

### Feature chuan hoa

Can them cac feature sau vao script trich xuat:

- Normalize toa do theo mid-hip hoac mid-shoulder.
- Scale theo shoulder width hoac torso length.
- Mirror/left-right robust representation neu can.
- Them visibility/confidence cua landmarks neu MediaPipe output duoc dung.

### Feature ergonomic

Can them:

- Shoulder slope angle.
- Torso lean angle.
- Head-forward offset relative to shoulder center.
- Nose-shoulder clearance ratio.
- Ear-shoulder-neck angle neu landmarks on dinh.
- Hand-to-mouth/face distance.
- Elbow/wrist desk proxy neu camera view cho phep.

### Feature temporal

Can them theo rolling window 3-10 giay:

- Bad-posture ratio.
- Consecutive bad-posture duration.
- Mean/variance cua head offset, torso lean, shoulder slope.
- Transition count giua correct/incorrect.
- Confidence dropout ratio.

## Benchmark can bo sung

Chay tat ca model tren cung train/external split:

| Model | Ly do |
|---|---|
| Logistic Regression | Baseline tuyen tinh de giai thich. |
| KNN | Baseline phi tham so, hop voi landmark distances. |
| SVM RBF | Thuong manh voi feature vectors nho/vua. |
| Random Forest | Robust voi nonlinear features, co feature importance. |
| XGBoost/LightGBM | Manh voi tabular features; can neu dependency chap nhan. |
| MLP/ANN hien tai | Model chinh hien co. |
| Rule-based baseline | Explainable baseline. |

Metric bat buoc:

- Accuracy.
- Precision/Recall/F1 cho class incorrect.
- Macro F1.
- MCC.
- ROC-AUC.
- PR-AUC.
- Confusion matrix.
- Wilson/Bootstrap CI.
- McNemar test voi model chinh.

## Nang cap protocol danh gia

### Giai doan 1: Frame-level reproducibility

- Giu split hien tai.
- Export prediction CSV gom `y_true`, `y_pred`, `probability`, `threshold`, `source_file` neu co.
- Lap lai metric tu prediction CSV.

### Giai doan 2: Video-wise split

- Re-extract feature CSV co `source_video` va `frame_index`.
- Chia train/test theo video, khong chia ngau nhien theo frame.
- Bao cao metric trung binh theo video.

### Giai doan 3: Person-wise split

- Them `participant_id` vao metadata.
- Chia train/test theo nguoi.
- Day la protocol manh nhat de claim generalization sang nguoi moi.

### Giai doan 4: Robustness

- Test theo camera angle, lighting, distance, clothing/background.
- Bao cao failure cases.

## Nang cap thuat toan de app tot hon

### Ngan han

1. Chon threshold mac dinh bang validation F1/recall thay vi co dinh 0.5.
2. Them temporal smoothing trong app:
   - Majority vote 5-15 frames.
   - Exponential moving average probability.
   - Chi canh bao khi sai lien tuc tren N giay.
3. Them feature normalization truoc khi train.
4. Them error analysis false negatives cho class incorrect.

### Trung han

1. Train model tabular manh hon: SVM, Random Forest, XGBoost.
2. Ablation study:
   - raw landmarks only
   - normalized landmarks
   - ergonomic features
   - raw + ergonomic
   - temporal features
3. Them calibration:
   - reliability curve
   - Brier score
   - Platt/isotonic calibration neu can.

### Dai han

1. Temporal model:
   - LSTM/GRU tren chuoi landmarks.
   - Temporal CNN.
   - Transformer nho neu du data.
2. Multi-class posture taxonomy:
   - leaning forward
   - rounded shoulders
   - neck compression
   - head turned
   - hand near mouth/face
   - no person/low confidence
3. Semi-supervised hoac active learning:
   - App luu frame kho, nguoi dung sua label, train lai.

## So sanh voi thuat toan khac

Ket luan hien tai:

- ANN local tot hon rule-based baseline trong project.
- Chua co bang chung tot hon KNN/SVM/RF/XGBoost vi chua benchmark.
- Chua co co so noi tot hon literature vi dataset/sensor/protocol khac va metric hien tai chua cao.

Bang statement an toan:

> The ANN model significantly outperformed the local rule-based baseline on the external frame-level test set. However, additional model benchmarks and video/person-wise validation are required before claiming superiority over alternative machine-learning approaches.

## Acceptance criteria cho nang cap thuat toan

Mot phien ban thuat toan du manh hon can dat:

- Co metadata-rich CSV.
- Co video-wise split runnable.
- Co benchmark it nhat 5 model.
- Co ROC/PR curve va prediction CSV.
- Co error analysis cho top false negatives/false positives.
- Co runtime benchmark trong app.
- Co model card ghi ro threshold, feature schema, intended use, limitations.

## File can sua trong cac task tiep theo

| File | Viec can lam |
|---|---|
| `src/2_extract_features.py` | Them metadata va normalized/ergonomic features. |
| `src/5_train_ann_local.py` | Ho tro feature schema moi, threshold/callback/model card. |
| `src/6_evaluate_external.py` | Export prediction CSV, ROC/PR, MCC, bootstrap CI. |
| `src/7_video_wise_evaluation.py` | Chay duoc khi CSV co metadata. |
| `src/8_compare_algorithms.py` | Them KNN/SVM/RF/XGBoost/LogReg/MLP. |
| `src/9_ablation_study.py` | Ablation raw/normalized/ergonomic/temporal. |
| `src/4_main_desktop_app.py` | Them temporal smoothing, threshold setting, runtime stats. |
| `reports/` | Them figures/tables/model card/error analysis. |

## Verdict

Thuat toan hien tai du tot cho demo/app realtime, nhung chua du manh de claim tot hon cac phuong phap khac. Huong nang cap dung nhat la: metadata-rich dataset, video/person-wise validation, benchmark nhieu model, feature normalization, temporal smoothing/model, va error/runtime analysis.
