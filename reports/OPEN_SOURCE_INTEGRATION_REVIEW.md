# Open-source Integration Review

Ngay cap nhat: 2026-05-26

## Ket luan chon thu vien

Da tich hop `statsmodels==0.14.6` vao project.

Ly do chon:

- Phu hop truc tiep voi nhu cau bao cao khoa hoc: confidence interval, paired statistical test, inference.
- Nhe hon viec thay pose backend bang MMPose/OpenPose.
- Khong pha pipeline hien tai da dung MediaPipe Pose va TensorFlow.
- Co the tao bang ket qua Springer: accuracy 95% CI va McNemar p-value.

Artifacts da them:

- `src/11_statistical_analysis.py`
- `reports/results/statistical_accuracy_ci.csv`
- `reports/results/paired_mcnemar_table.csv`
- `reports/results/statistical_analysis.txt`

## Cac ma nguon mo/thu vien da xem

| Candidate | Phu hop | Quyet dinh | Ly do |
|---|---|---|---|
| MediaPipe Pose | Dang dung | Giu lam pose backend chinh | Official docs noi Pose Landmarker dung duoc cho posture analysis, output 33 landmark, ho tro image/video/live stream. |
| statsmodels | Rat phu hop | Da cai dat | Co McNemar test va confidence interval cho ty le, phu hop bao cao khoa hoc. |
| MMPose / RTMPose | Co tiem nang | Chua cai dat vao runtime chinh | Research-grade pose toolbox, nhung nang, can PyTorch/CUDA/weights, lam tang rui ro cai dat demo. De lam task mo rong neu can benchmark pose backend. |
| RULA/ergonomic toolkits | Co gia tri ly thuyet | Chua nhung vao code | RULA can thong tin task/force/repetition/recovery va nhieu quy tac chuyen nganh; neu gan nhan sai se lam bai yeu. Nen chi lam "RULA-inspired ergonomic indicators" truoc, khong tu nhan la RULA score chuan. |

## Nguon tham khao da kiem tra

- MediaPipe Pose Landmarker official docs: https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker
- MediaPipe GitHub: https://github.com/google-ai-edge/mediapipe
- statsmodels GitHub/docs: https://github.com/statsmodels/statsmodels, https://www.statsmodels.org/
- McNemar docs: https://www.statsmodels.org/dev/generated/statsmodels.stats.contingency_tables.mcnemar.html
- Proportion confidence interval docs: https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_confint.html
- MMPose overview: https://mmpose.com/
- Ergonomic postural assessment with open-source pose estimation: https://www.sciencedirect.com/science/article/abs/pii/S0169814121000822
- RULA overview: https://virtualfactory.gitbook.io/vlft/tools/rula

## Huong tich hop tiep theo neu can diem moi manh hon

1. Them `src/12_temporal_risk_index.py`: tinh chi so rui ro theo phien tu SQLite/log frame.
2. Them video-wise split that sau khi co CSV metadata.
3. Them runtime/FPS benchmark: MediaPipe + ANN vs MediaPipe + rule-based.
4. Neu co GPU/thoi gian, tao optional branch benchmark MMPose/RTMPose, khong dua vao demo mac dinh.
