# Springer Research Roadmap

Muc tieu: dua project Posture Detection App tu muc demo ky thuat len muc co the viet bao cao nghien cuu khoa hoc theo cau truc Springer.

## 0. Dinh vi dong gop khoa hoc

### Diem moi de bao cao

Ten tam thoi: **Temporal Hybrid Landmark-based Posture Risk Monitoring**.

Dong gop khong nen tuyen bo qua muc. Diem moi nen viet theo huong:

1. He thong realtime end-to-end dung webcam/video, MediaPipe Pose, ANN, rule-based baseline, canh bao va SQLite logging.
2. Pipeline lai: ANN cho phan loai frame-level, rule-based ergonomic indicators cho giai thich loi tu the.
3. Danh gia khoa hoc gom external set, threshold sweep, confidence interval va McNemar paired test.
4. De xuat/bo sung chi so rui ro theo thoi gian tu log phien lam viec: tan suat sai, thoi luong sai lien tuc, so canh bao, ty le dung/sai.
5. Quy trinh tai lap: dataset manifest, experiment protocol, QA checklist, report artifacts.

### Cau hoi nghien cuu

| Ma | Cau hoi |
|---|---|
| RQ1 | ANN landmark classifier co vuot rule-based baseline tren external dataset khong? |
| RQ2 | Threshold sigmoid co anh huong nhu the nao den precision/recall/F1 cho canh bao realtime? |
| RQ3 | Danh gia frame-wise co bi lac quan so voi video-wise/person-wise split khong? |
| RQ4 | Cac chi so ergonomic rule-based nao giai thich duoc loi tu the thuong gap? |
| RQ5 | Log theo phien co tao duoc chi so rui ro huu ich cho demo/bao cao khong? |

### Gia thuyet

| Ma | Gia thuyet | Cach kiem dinh |
|---|---|---|
| H1 | ANN co accuracy/F1 cao hon rule-based baseline tren cung external frames. | McNemar paired test, CI accuracy, F1 comparison. |
| H2 | Threshold toi uu theo F1 co recall cao hon threshold 0.5 cho lop incorrect. | Threshold sweep 0.10-0.90. |
| H3 | Video-wise split se cho metric thap hon frame-wise split. | Tao CSV metadata, split theo `source_video`. |
| H4 | Temporal risk index phan biet duoc phien tot/xau hon frame-level accuracy don le. | Session statistics tu SQLite. |

## 1. Nhiem vu du lieu

### TASK-S01 - Hoan thien dataset manifest

Pham vi:

- `reports/DATASET_MANIFEST.md`
- Video raw/external ngoai Git.

Can lam:

- Dem chinh xac so video theo label, goc quay, nguoi tham gia.
- Bo sung thiet bi camera, do phan giai, FPS goc, dieu kien anh sang.
- Ghi dinh nghia correct/incorrect.
- Ghi cach loai frame khong co pose.
- Ghi rang raw video khong commit vao Git do gioi han dung luong.

Done khi:

- Manifest co bang theo `participant`, `view`, `label`, `video_count`, `duration`, `resolution`, `fps`.

### TASK-S02 - Tao CSV metadata moi

Pham vi:

- `src/2_extract_features.py`
- `dataset/posture_data_2fps_with_metadata.csv`
- `dataset/posture_external_test_2fps_with_metadata.csv`

Can lam:

- Chay extraction voi `--include-metadata`.
- Dam bao co cot `source_video`, `frame_index`, `sample_fps`, `video_fps`, `label`.
- Neu co the, them `participant_id`, `view_angle`, `recording_session` suy ra tu ten file va manual map.

Done khi:

- `python src/7_video_wise_evaluation.py --dataset dataset/posture_data_2fps_with_metadata.csv` khong bao thieu metadata.

### TASK-S03 - Chia train/val/test nghiem tuc

Can lam:

- Frame-wise split: giu de so sanh voi ket qua cu.
- Video-wise split: train/test khac video.
- Person-wise split: neu co participant id.
- External split: giu rieng de bao cao generalization.

Done khi:

- Co `reports/results/split_summary.csv`.
- Moi split co so mau, so video, label distribution.

## 2. Nhiem vu model va diem moi

### TASK-S04 - Dong goi ANN pipeline tai lap

Can lam:

- Pin dependency da dung train: `scikit-learn==1.6.1`, `tensorflow==2.16.2`.
- Luu model metadata: dataset path, commit hash, feature schema, threshold, sklearn/tensorflow version.
- Them script `src/12_model_card.py` hoac report `reports/MODEL_CARD.md`.

Done khi:

- Nguoi khac biet model nao duoc train tu CSV nao va dung threshold nao.

### TASK-S05 - Hoan thien rule-based ergonomic indicators

Can lam:

- Xoa logic copy trong GUI, chi dung `posture_baseline.py`.
- Ghi cong thuc cho: shoulder tilt, torso lean, head offset, head lowering, hand near mouth.
- Doi ten ro: "RULA-inspired indicators", khong tuyen bo la RULA chuan.
- Them unit test cho tung indicator.

Done khi:

- GUI/baseline script/test cung dung mot module.

### TASK-S06 - Them Temporal Posture Risk Index

Pham vi de xuat:

- `src/12_temporal_risk_index.py`
- `reports/results/session_risk_index.csv`

Cong thuc de xuat:

```text
risk_index = 100 * (
  0.40 * incorrect_time_ratio
  + 0.25 * long_bad_posture_ratio
  + 0.20 * warning_rate_norm
  + 0.15 * no_person_or_low_confidence_ratio
)
```

Can lam:

- Tinh tu SQLite session/log.
- Ghi ro moi thanh phan, range 0-100.
- Tao bang session-level risk.
- Them interpretability: Low/Medium/High.

Done khi:

- Co output CSV va mot doan Method/Results cho chi so nay.

## 3. Nhiem vu danh gia khoa hoc

### TASK-S07 - Chay external evaluation chuan

Da co:

- `src/6_evaluate_external.py`
- `reports/results/external_metrics.txt`
- `reports/results/external_threshold_sweep.csv`

Can lam tiep:

- Chay lai sau khi pin dependency.
- Them PR-AUC/ROC-AUC neu can.
- Luu prediction-level CSV de ve error analysis.

### TASK-S08 - Statistical inference

Da co:

- `statsmodels==0.14.6`
- `src/11_statistical_analysis.py`
- Wilson CI va McNemar test.

Ket qua hien tai:

- ANN accuracy: `0.793164`, 95% CI `[0.773242, 0.811763]`.
- Rule-based accuracy: `0.566293`, 95% CI `[0.542591, 0.589697]`.
- McNemar p-value: `2.19314e-60`.

Can lam tiep:

- Them bootstrap CI cho F1 neu can.
- Bao cao rang McNemar la paired frame-level test, chua thay the video-wise validation.

### TASK-S09 - Video-wise/person-wise evaluation

Can lam:

- Sau TASK-S02, implement split theo `source_video`.
- Train model moi chi tren train videos.
- Evaluate held-out videos.
- So sanh frame-wise vs video-wise.

Done khi:

- Co `reports/results/video_wise_metrics.txt`.
- Co bang so sanh frame-wise, video-wise, external.

### TASK-S10 - Error analysis

Can lam:

- Lay cac frame/video ANN sai nhieu nhat.
- Nhom loi theo: goc quay, occlusion, low light, side view, hand near face.
- Tao `reports/results/error_analysis.md`.

Done khi:

- Discussion co ly do tai sao external recall thap hon local.

### TASK-S11 - Runtime evaluation

Can lam:

- Do FPS tren webcam/video cho ANN mode va rule-based mode.
- Do CPU/RAM neu co the.
- Bao cao min/mean/p95 latency.

Done khi:

- Co `reports/results/runtime_benchmark.csv`.

## 4. Nhiem vu ung dung va demo

### TASK-S12 - Manual GUI QA

Can lam:

- Chay webcam.
- Chay video file.
- Test missing model/scaler/database.
- Test bat/tat audio.
- Test start/stop 5 lan.
- Fill `reports/GUI_QA_CHECKLIST.md`.

### TASK-S13 - Screenshot va hinh minh hoa

Can lam:

- `reports/figures/gui_ann_mode.png`
- `reports/figures/gui_rule_based_mode.png`
- `reports/figures/sample_landmarks.png`
- `reports/figures/pipeline_diagram.png`
- `reports/figures/confusion_matrix_external.png`

Done khi:

- Moi figure trong paper outline co file nguon.

### TASK-S14 - Dong goi demo

Can lam:

- Script setup nhanh.
- Huong dan demo 5 phut.
- Checklist truoc khi nop.

Done khi:

- Nguoi khac clone repo, cai requirements, chay database setup, chay GUI duoc.

## 5. Nhiem vu viet bai Springer

### TASK-S15 - Abstract

Can co:

- Problem.
- Method.
- Dataset size.
- External metrics.
- Statistical result.
- Limitation.

### TASK-S16 - Introduction

Can co:

- Tac hai tu the sai khi lam viec.
- Vi sao webcam-based low-cost monitoring co y nghia.
- Khoang trong: nhieu demo realtime thieu external/statistical/session-level evaluation.
- Contributions.

### TASK-S17 - Related Work

Can co citation that cho:

- MediaPipe/BlazePose.
- Ergonomic posture assessment: RULA/REBA/OWAS.
- Pose-estimation-based ergonomic assessment.
- ML posture classification.
- Real-time feedback systems.

Khong duoc bia citation.

### TASK-S18 - Materials and Methods

Can co:

- Dataset acquisition.
- Feature extraction 99 landmarks.
- ANN architecture.
- Rule-based baseline.
- Temporal risk index.
- GUI/logging architecture.
- Experimental setup.

### TASK-S19 - Results

Can co bang:

- Dataset distribution.
- Local frame-wise metrics.
- External metrics.
- Threshold sweep best threshold.
- ANN vs rule-based + McNemar.
- Video-wise metrics neu co.
- Runtime benchmark.

### TASK-S20 - Discussion, limitations, conclusion

Can co:

- Giai thich external recall thap hon local.
- Noi ro frame-wise leakage risk.
- Khong claim y te.
- Goc quay/anh sang/occlusion limitations.
- Ke hoach future work: bigger dataset, subject-wise validation, RULA expert labels.

## 6. Dinh nghia "du san sang nop"

Project du san sang nop/demo khi:

- `python -m pytest tests` pass.
- `python -m py_compile src/*.py` pass.
- GUI chay duoc ANN va rule-based.
- Co external metrics, statistical analysis, algorithm comparison.
- Co video-wise hoac it nhat protocol + metadata extraction hoan chinh.
- Co figure/table plan va screenshots.
- Paper draft co Abstract, Method, Results, Discussion, Limitations.

Project du san sang gui Springer workshop/conference khi:

- Co citation that.
- Co split video-wise/person-wise hoac external validation du manh.
- Co statistical inference.
- Co limitations trung thuc.
- Co data/code availability statement.
