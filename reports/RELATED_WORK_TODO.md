# Related Work Todo

Khong tu bia citation. Dien bang nay bang nguon that truoc khi nop bai.

| Citation | What to use | Status |
|---|---|---|
| MediaPipe Pose Landmarker official docs | Pose landmark extraction, 33 landmarks, image/video/live stream support | Found: https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker |
| BlazePose/Google AI Blog or paper | Landmark model background | Need source |
| Ergonomic posture assessment literature | Definition of posture risk and workplace ergonomics | Need source |
| Ergonomic postural assessment using open-source pose estimation | Motivation for pose-estimation-based ergonomic assessment | Found: https://www.sciencedirect.com/science/article/abs/pii/S0169814121000822 |
| RULA overview/toolkit | Explain RULA context and why this project uses RULA-inspired indicators, not full RULA scoring | Found: https://virtualfactory.gitbook.io/vlft/tools/rula |
| statsmodels documentation | McNemar test and Wilson CI implementation for reporting | Found: https://www.statsmodels.org/ |
| Webcam posture detection with ML | Compare task setup and metrics | Found in `reports/LITERATURE_METRICS_COMPARISON.md`: Estrada et al. 2023, Kulikajevas et al. 2021, ALIGN 2026 candidate |
| ANN/SVM/KNN posture classification | Baseline comparison context | Found in `reports/LITERATURE_METRICS_COMPARISON.md`: Luna-Perejon et al. 2021, Tsai et al. 2023, Feradov et al. 2022 |
| Real-time feedback systems | Warning/behavior change motivation | Found in `reports/LITERATURE_METRICS_COMPARISON.md`: Chaikhamwang et al. 2025, ALIGN 2026 candidate |
| SQLite/local logging in health apps | Optional, for app architecture | Need source |

## Da luu nguon so sanh

- Bang doc duoc: `reports/LITERATURE_METRICS_COMPARISON.md`
- CSV may doc duoc: `reports/literature_metrics_comparison.csv`
- BibTeX cho bai Springer: `reports/RELATED_PAPERS.bib`

Ghi chu: khong dung cac so lieu nay nhu leaderboard truc tiep. Moi bai co dataset, nhan, sensor va split protocol khac nhau. Cac dong co `indexed official page` can mo full PDF lai truoc khi nop ban thao cuoi.
# Related Work Verification Update

Ngay cap nhat: 2026-05-27

## Trang thai da chuan hoa

- Bang so sanh chinh nam trong `reports/LITERATURE_METRICS_COMPARISON.md`.
- BibTeX nhap nhanh nam trong `reports/RELATED_PAPERS.bib`.
- Cac metric literature chi duoc dung nhu contextual comparison, khong dung nhu leaderboard vi khac sensor, dataset, split va label schema.

## Nguon da dung de doi chieu

- MediaPipe Pose Landmarker official docs: https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker
- Estrada et al., Applied Sciences 2023: https://www.mdpi.com/2076-3417/13/9/5402
- Kulikajevas et al., PeerJ Computer Science 2021: https://doaj.org/article/203c4c4fa85d4693a21acf6b98b29357
- Tsai et al., Sensors 2023: https://www.mdpi.com/1424-8220/23/13/5894/html
- Feradov et al., Computers 2022: https://www.mdpi.com/2073-431X/11/7/116
- Luna-Perejon et al., Electronics 2021: https://www.mdpi.com/2079-9292/10/15/1825
- RULA original paper record: https://pubmed.ncbi.nlm.nih.gov/15676903/
- Smart sensing chair review: https://pmc.ncbi.nlm.nih.gov/articles/PMC11086066/

## Claim rule

Khong viet "our method outperforms previous works". Chi viet:

> The current ANN outperformed the local rule-based baseline on the same external frame-level set. Literature values are reported for context because sensing modality, datasets, label schemes, and validation protocols differ.
