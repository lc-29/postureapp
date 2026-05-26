# Literature Metrics Comparison

Updated: 2026-05-26

Purpose: collect real reported numbers from related sitting-posture and ergonomic-monitoring papers so the project can compare its current method without inventing citations or overstating results.

## Comparison Rules

- These values are not directly comparable as a leaderboard. The papers use different sensors, labels, participants, split protocols, and deployment assumptions.
- The safest Springer wording is "contextual comparison" rather than "outperforms" unless the same public dataset and split are used.
- Use the project metrics as an external validation baseline, then explain gaps: binary labels, webcam/MediaPipe landmarks, frame-level evaluation, and no person-wise split yet.
- Rows marked "indexed official page" should be checked again from the full paper/PDF before final submission. The source URL is official, but the browser could not extract full-text lines due publisher challenge pages.

## Current Project Metrics

Source files:

- `reports/results/external_metrics.txt`
- `reports/results/algorithm_comparison.csv`
- `reports/results/statistical_analysis.txt`
- `reports/DATASET_MANIFEST.md`

| Item | Value |
|---|---:|
| External dataset rows | 1697 |
| External labels | 768 correct, 929 incorrect |
| External raw videos | 5 correct, 5 incorrect |
| Feature schema | 33 MediaPipe landmarks x 3 coordinates = 99 features |
| ANN threshold | 0.50 |
| ANN accuracy | 79.316% |
| ANN precision, incorrect class | 94.599% |
| ANN recall, incorrect class | 65.985% |
| ANN F1, incorrect class | 77.743% |
| ANN Wilson 95% accuracy CI | [77.324%, 81.176%] |
| Best threshold by F1 | 0.10 |
| Best-threshold accuracy | 80.436% |
| Best-threshold F1 | 79.903% |
| Rule-based accuracy | 56.629% |
| Rule-based F1 | 64.479% |
| ANN vs rule-based McNemar p-value | 2.19314e-60 |

## Primary Comparison Table

| ID | Study | Modality / input | Task and dataset note | Method | Reported metric(s) | Source verification | Comparison note |
|---|---|---|---|---|---|---|---|
| OURS | Posture Detection App current external result | Webcam/video, MediaPipe Pose landmarks | Binary correct/incorrect, 1697 external frames from 10 external videos | ANN classifier; rule-based ergonomic baseline | ANN: accuracy 79.316%, precision 94.599%, recall 65.985%, F1 77.743%; best threshold F1 79.903%; rule-based accuracy 56.629% | Local project artifacts | Same project scope, but still frame-level. Needs video-wise/person-wise validation before strong claims. |
| L01 | Estrada, Vea, and Devaraj, Applied Sciences 2023 | Smartphone cameras, MediaPipe keypoints plus computed distances/angles | Proper vs improper sitting posture in work-from-home setting; 60 participants; 7200 annotated 10-second instances from 720,000 processed frames | Small-scale CNN / machine-learning pipeline with human pose estimation features | Overall left/right camera accuracies 85.18% and 92.07%; kappas 0.691 and 0.838. Category experiments reported up to 98.003% for left-camera elbow and 99.5425% for right-camera wrist. | Indexed official MDPI article page and SSRN abstract | Closest camera/MediaPipe comparison. Different camera placement, annotations, and per-body-part models, so compare as context only. |
| L02 | Kulikajevas, Maskeliunas, and Damasevicius, PeerJ Computer Science 2021 | RGB-D camera sequences | 11 subjects, 66 video sequences, 133 min recording, six sitting posture labels plus hierarchical grouping | Deep recurrent hierarchical network based on MobileNetV2 | Headline sitting-posture recognition accuracy 91.47% at 10 fps; reported sensitivity 0.9185, specificity 0.9595, F-score 0.9132, kappa 0.8081 for base posture grouping. The fine six-label result was lower at 68.33% accuracy. | PubMed/PMC indexed abstract and full-text snippets | Strong related computer-vision baseline. Uses RGB-D and hierarchy, not plain webcam landmarks. Useful for discussing temporal sequence/context. |
| L03 | Tsai, Chu, and Lee, Sensors 2023 | Pressure sensors embedded in chair cushion | 10 sitting postures; model setup with 6 subjects and validation with 20 additional participants / 12,000 samples | SVM, KNN, decision tree, random forest, logistic regression | SVM 99.18%, KNN 98.86%, decision tree 97.83%, random forest 98.41%, logistic regression 98.19%; 13-sensor placement kept all algorithms above 97% | PMC/MDPI indexed full-text snippets | High accuracy, but sensor-based and controlled. Useful to show pressure sensors can outperform camera-only methods at the cost of hardware. |
| L04 | Luna-Perejon et al., Electronics 2021 | FSR pressure sensors on a chair | Seven recorded postures; test set included 3369 samples from two users | Artificial neural network | Best ANN architecture reached 81.00% accuracy; specificity 96.40%, precision 82.14%, sensitivity 80.96%, F1 80.24%, AUC 0.9672 | Full MDPI article page extracted | Similar metric range to this project, but uses physical sensors and multi-class posture labels. |
| L05 | Feradov, Markova, and Ganchev, Computers 2022 | Motion-capture sensor data; accelerometers placed on arms, head/back, and fingers | Automated detection of improper sitting postures in computer users | Hjorth features with decision tree, SVM, SVM-RBF, and KNN | Highest table value: 98.4% with linear SVM using Activity+Mobility+Complexity features from arm sensors. Classifier mean for arm-sensor table: SVM 94.0%. | Full MDPI article page extracted | Wearable/motion-capture setup, not low-cost webcam. Good benchmark for sensor-rich approaches. |
| L06 | Chaikhamwang et al., IJACSA 2025 | MediaPipe and computer vision | Office-syndrome risk platform monitoring posture, eye-to-screen distance, and sitting duration | Real-time detection plus notification and stretching recommendation platform | Eye-distance detection accuracy 95.2%; long-sitting alerts 92.5%; proximity alerts 90.1% | Full IJACSA article page extracted | Not a pure posture classifier. Relevant to this project's warning, logging, and Temporal Posture Risk Index direction. |
| L07 | ALIGN: An AI-Driven IoT Framework for Real-Time Sitting Posture Detection, Algorithms 2026 | MediaPipe pose landmarks and video streams | Binary correct/incorrect posture decisions on a single-board-computer IoT framework | KNN, SVC, MLP, ResNet52, DenseNet121 | KNN 98.74%, SVC 96.64%, MLP 97.17%, ResNet52 94.37%, DenseNet121 81.53% | Indexed official MDPI article page; full page blocked by challenge during extraction | Very close conceptually, but keep as "needs full-text verification" before final paper claims. |
| L08 | Nadeem et al., Applied Sciences 2024 | Systematic review across sensing technologies | Review of sitting posture recognition systems; selected 120 articles | Literature review and analysis | Review included 70 journal articles, 49 conference papers, and 1 book chapter; notes sensor, ML, IoT, alert, and challenge categories | Full MDPI review page extracted | Use for related-work framing, not a direct metric baseline. |

## Interpretation for the Paper

Current external performance is below several lab-controlled pressure-sensor and MediaPipe studies. This is acceptable for an honest research report if the contribution is framed around a low-cost end-to-end webcam pipeline, external-set evaluation, interpretable rule-based indicators, statistical comparison against a baseline, and session-level temporal risk monitoring.

Do not claim state-of-the-art. A defensible claim is:

> The proposed system provides an end-to-end webcam-based posture monitoring pipeline with frame-level ANN classification, rule-based ergonomic indicators, and temporal risk summarization. On the current external frame set it achieved 79.32% accuracy and 77.74% F1 for the incorrect class, outperforming the local rule-based baseline on paired frames, while remaining below several controlled sensor-based and recent MediaPipe-based studies.

## Recommended Next Experiments

1. Add `source_video` and `participant_id` columns to produce video-wise/person-wise metrics.
2. Report ROC-AUC/PR-AUC and bootstrap F1 confidence intervals.
3. Compare against KNN/SVM/Random Forest/XGBoost on the same 99 MediaPipe features.
4. Run runtime benchmarks: mean FPS, p95 latency, CPU/RAM.
5. Re-check L01 and L07 full PDFs before final Springer submission because browser extraction was limited by publisher challenge pages.

