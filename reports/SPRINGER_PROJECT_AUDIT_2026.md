# Springer Project Audit 2026

Ngay cap nhat: 2026-05-28

## Muc tieu

File nay danh gia toan bo project theo goc nhin co the viet bao cao/khoa luan/bai theo chuan Springer: muc do hoan thien, thuat toan, du lieu, dac trung, diem moi, rui ro, va viec can phat trien tiep.

## Ket luan ngan gon

Project da vuot muc demo co ban. Hien tai co:

- App desktop realtime bang CustomTkinter.
- Input webcam, camera IP, video file.
- MediaPipe Pose 33 landmarks, vector 99 dac trung.
- ANN binary classifier.
- Rule-based ergonomic baseline co test.
- External evaluation.
- Threshold sweep.
- So sanh ANN vs rule-based.
- Wilson confidence interval va McNemar paired test.
- SQLite session logging.
- Temporal Posture Risk Index (TPRI).
- Dashboard thong ke light/dark mode.
- QA/task workflow kha day du.

Nhung neu xet theo chuan Springer, project **chua nen claim state-of-the-art**. Ly do:

- Metric external da sua: ANN accuracy `90.169%`, F1 incorrect `90.338%`; SVM RBF + ergonomic features dat F1 incorrect `95.107%` trong benchmark noi bo.
- Da co metadata CSV, video-wise evaluation va participant-wise evaluation; tuy nhien external set hien chi co P01 nen chua du manh de claim robust generalization.
- Dataset con nho va metadata chua day du.
- ANN hien moi la dense classifier tren 99 landmark raw coordinates, chua co sequence/temporal model.
- Rule-based baseline huu ich cho giai thich, recall incorrect cao nhung accuracy external van thap hon ANN/SVM (`67.491%`).

Vi vay dinh vi khoa hoc nen la:

> Mot he thong webcam-based end-to-end cho giam sat tu the lam viec, ket hop ANN frame-level, ergonomic rule indicators, canh bao realtime, logging SQLite, va session-level Temporal Posture Risk Index; co external validation va statistical paired comparison voi baseline.

Khong nen viet:

> Thuat toan tot hon cac nghien cuu hien co.

Nen viet:

> He thong hoan chinh va tai lap hon nhieu prototype demo; co dong gop o muc tich hop realtime + explainable indicators + session-level risk logging/evaluation.

## Trang thai thanh phan

| Thanh phan | Trang thai | Danh gia |
|---|---|---|
| Feature extraction | Da co | Dung MediaPipe landmarks, sample 2 FPS, co option metadata. |
| Dataset CSV | Da co | Train 11022 rows, external 1658 rows; da co metadata video/person trong processed CSV. |
| ANN model | Da co | Corrected external F1 incorrect 90.338%; benchmark cho thay SVM/RF cung la ung vien manh. |
| Rule-based baseline | Da co | Giai thich tot, metric thap; vua them neck-compression rule. |
| External evaluation | Da co | Co confusion matrix, threshold sweep. |
| Statistical inference | Da co | Wilson CI va McNemar paired test. |
| Video-wise evaluation | Da co | Da sinh `reports/results/video_wise_metrics.csv`. |
| Person-wise evaluation | Da co | Da sinh raw va combined leave-one-participant-out metrics. |
| Temporal risk index | Da co | Diem moi kha tot, can validate them. |
| GUI | Da nang cap | Light/dark, dashboard, table, risk; can manual QA/screenshot. |
| Runtime benchmark | Da co | Co FPS/latency cho front/side_30/side_90. |
| Error analysis | Da co | Co phan tich false negative/false positive theo video/person/view. |
| Model card | Da co | `reports/MODEL_CARD_ANN_CURRENT.md`. |
| Related work | Mot phan | Da co bang so sanh, can citation verified full-text. |

## Kiem chung hien tai

Da chay gan nhat:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
# 20 passed, 1 skipped
```

```powershell
python -m py_compile src/1_rule_based_baseline.py src/2_extract_features.py src/3_database_setup.py src/4_main_desktop_app.py src/5_train_ann_local.py src/6_evaluate_external.py src/7_video_wise_evaluation.py src/8_compare_algorithms.py src/9_ablation_study.py src/10_export_statistics.py src/11_statistical_analysis.py src/12_temporal_risk_index.py src/posture_baseline.py src/statistics_service.py src/utils.py
# pass
```

## So lieu hien tai

### Dataset

| Dataset | Rows | Correct | Incorrect | Ghi chu |
|---|---:|---:|---:|---|
| Train CSV | 11022 | 4438 | 6584 | Frame-level CSV, chua co metadata video/person. |
| External CSV | 1658 | 768 | 890 | 10 external videos, corrected after replacing `P01_incorrect_004.mp4`. |

### External metrics

| Model | Accuracy | Precision incorrect | Recall incorrect | F1 incorrect |
|---|---:|---:|---:|---:|
| ANN threshold 0.5 | 90.169% | 95.609% | 85.618% | 90.338% |
| ANN best F1 threshold 0.10 | 91.375% | 92.784% | 91.011% | 91.889% |
| Rule-based | 67.491% | 63.490% | 92.809% | 75.399% |

### Statistical analysis

| Hang muc | Gia tri |
|---|---:|
| ANN Wilson 95% accuracy CI | [88.642%, 91.511%] |
| Rule-based Wilson 95% accuracy CI | [65.198%, 69.703%] |
| McNemar p-value | `1.15022e-56` |

Interpretation: ANN vuot rule-based tren paired external frames. Tuy nhien day van la frame-level paired test, khong thay the video-wise/person-wise validation.

## Doi chieu literature

### Nguon dung de doi chieu

- Google AI Edge MediaPipe Pose Landmarker official docs: Pose Landmarker supports image/video/live-stream inputs and outputs 33 pose landmarks in normalized and world coordinates. URL: https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker
- Kulikajevas et al., PeerJ Computer Science 2021: RGB-D deep recurrent hierarchical network, 91.47% accuracy at 10 fps. URL: https://doaj.org/article/203c4c4fa85d4693a21acf6b98b29357
- Tsai et al., Sensors 2023: pressure sensor sitting posture recognition, SVM highest accuracy around 99.18%. URL: https://www.mdpi.com/1424-8220/23/13/5894/html
- Estrada et al., Applied Sciences 2023: smartphone camera/MediaPipe posture classification in work-from-home setup. URL: https://www.mdpi.com/2076-3417/13/9/5402
- Feradov et al., Computers 2022: motion-capture/accelerometer Hjorth features, up to 98.4% accuracy. URL: https://www.mdpi.com/2073-431X/11/7/116
- Luna-Perejon et al., Electronics 2021: FSR/IoT chair ANN, mean accuracy 81%. URL: https://www.mdpi.com/2079-9292/10/15/1825
- McAtamney and Corlett 1993 RULA, ergonomic upper-limb assessment. URL: https://pubmed.ncbi.nlm.nih.gov/15676903/
- Smart sensing chair review, PMC 2024, contextual source for pressure-sensor posture recognition. URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC11086066/

## Thuat toan hien tai co tot chua?

Co, neu xet trong pham vi do an app realtime webcam:

- ANN co precision incorrect cao (`95.609%`) tai threshold 0.5, nghia la khi bao sai thi kha chac.
- Threshold 0.10 tang recall incorrect tu `85.618%` len `91.011%`, phu hop hon voi canh bao realtime neu muon bot bo sot.
- McNemar test cho thay ANN khac biet ro voi rule-based baseline tren external frames.

Chua tot neu xet nhu mot bai research manh:

- Van con false negatives (`128 FN` tren external) nen can toi uu threshold/temporal smoothing.
- Video-wise/person-wise da co, nhung external set chi co P01 va dataset van nho.
- Da benchmark KNN/SVM/RF/HistGradientBoosting tren cung feature, nhung chua dong goi model tot nhat vao app.
- Chua co temporal model, trong khi posture monitoring co tinh lien tuc theo thoi gian.
- Feature la raw landmark coordinates, chua chuan hoa theo co the/goc quay tot.

## Co tot hon cac thuat toan khac khong?

Khong the ket luan tot hon cac thuat toan khac trong literature.

Ket luan dung:

- Tot hon **baseline rule-based local** tren cung external frames.
- Co tinh ung dung end-to-end va logging/statistical reporting tot.
- Metric corrected external da canh tranh hon, nhung van khong the ket luan tot hon literature vi cac nghien cuu do dung dataset, sensor, label va split khac.

Bang dinh vi:

| Nhom he thong | So voi project nay |
|---|---|
| Pressure sensor chair | Thuong accuracy cao hon, nhung can phan cung/chair sensor. |
| RGB-D/depth camera | Thuong robust hon voi 3D/depth, nhung phan cung dat hon webcam. |
| Motion-capture/IMU | Metric cao, nhung can wearable/sensor gan nguoi. |
| Webcam/MediaPipe | Gan voi project nhat; can video/person split va benchmark them de canh tranh. |
| Project hien tai | Manh o tich hop app + external eval + TPRI + logging, yeu o validation protocol va metric. |

## Diem moi co the bao cao

### Diem moi chinh

1. **End-to-end webcam posture monitoring**: tu camera/video -> MediaPipe -> ANN/rule-based -> canh bao -> SQLite -> dashboard.
2. **Hybrid frame-level classifier + ergonomic indicators**: ANN cho performance, rule-based cho giai thich loi vai/than/dau/tay/rut co.
3. **Temporal Posture Risk Index**: tong hop log theo phien thanh risk score 0-100, khac voi chi bao cao frame accuracy.
4. **Statistical reporting**: external set, threshold sweep, Wilson CI, McNemar paired test.
5. **Reproducibility workflow**: dataset manifest, experiment protocol, QA checklist, model/report artifacts.

### Diem moi vua phai, khong nen thoi phong

- Neck-compression feature/rule trong baseline la cai tien practical, nhung khong du de claim novelty khoa hoc lon.
- Light/dark dashboard la diem san pham, khong phai dong gop thuat toan.
- SQLite session logging + risk index co the la dong gop ung dung neu trinh bay ro.

## Du lieu va dac trung co gi moi hon nguoi khac?

### Du lieu

Chua co diem moi manh ve dataset.

- Train/external video rieng la tot cho do an.
- External set co 10 video la diem cong.
- Nhung dataset nho, chua co participant metadata, chua public raw videos, chua person-wise split.

Nen viet:

> We collected a project-specific webcam/video dataset and an external video set for preliminary generalization testing.

Khong nen viet:

> We propose a new benchmark dataset.

### Dac trung

Feature 99 raw MediaPipe landmark coordinates khong moi; nhieu nghien cuu dung MediaPipe/keypoints.

Diem co gia tri:

- Feature schema don gian, realtime, tai lap.
- Rule-based indicators co tinh giai thich: shoulder tilt, torso lean, head offset, neck compression, hand near mouth.
- TPRI dung log theo thoi gian, khong chi frame features.

Nen viet:

> The feature design combines raw MediaPipe landmark coordinates for learning with interpretable ergonomic indicators for explanation and session-level risk aggregation.

Khong nen viet:

> The landmark feature representation is novel.

## Diem can phat trien them de bai manh hon

1. Mo rong external set sang nhieu participant/camera hon.
2. Chot protocol final cho video-wise/person-wise split.
3. Dong goi SVM/RF/ANN theo model registry va feature schema.
4. Them bootstrap CI cho F1 theo video/person.
5. Lam error taxonomy cho false negative/false positive.
6. Bo sung cau hinh may cho runtime benchmark.
7. Cap nhat model card voi commit hash, feature schema, threshold, dependency versions, intended use.
8. Figure/table cho paper: pipeline, GUI, confusion matrix, threshold curve, TPRI distribution.
9. Related work citations can duoc verify tu full paper/PDF.
10. Manual GUI QA va screenshots.

## Dinh vi Springer de xuat

### Title goi y

**A Hybrid Landmark-Based Desktop System for Real-Time Sitting Posture Monitoring with Session-Level Temporal Risk Analysis**

### Contributions goi y

1. A real-time desktop posture monitoring pipeline using webcam/video input and MediaPipe landmarks.
2. A hybrid inference design combining ANN classification and interpretable ergonomic rule indicators.
3. A session-level Temporal Posture Risk Index computed from SQLite posture logs.
4. An evaluation protocol including external frame-level validation, threshold sweep, confidence intervals, and paired ANN-vs-baseline testing.

### Limitation can noi ro

- Not medical diagnosis.
- Small dataset.
- Frame-wise evaluation risk.
- No person-wise validation yet.
- Camera angle/lighting/occlusion sensitivity.
- External recall needs improvement.
