# Webcam-Based Working Posture Error Detection Using Normalized MediaPipe Landmarks and Lightweight Machine Learning

## Abstract

Incorrect sitting posture during computer work is difficult to monitor continuously without extra hardware. This paper presents an applied webcam-based desktop system for detecting working posture errors using MediaPipe Pose landmarks, body-normalized features, ergonomic geometric indicators, and lightweight machine learning. The system captures frames from a webcam, IP camera, or MP4 video, extracts 33 MediaPipe Pose landmarks, constructs raw, normalized, and ergonomic feature groups, predicts Correct posture or Incorrect posture, smooths frame-level predictions, triggers warnings, and stores session logs in SQLite. A self-collected dataset was built from 84 raw videos of five participants, producing 11,022 sampled frames with 4,438 Correct and 6,584 Incorrect samples. A corrected external set contains 10 videos and 1,658 frames from P01. On the corrected external set, the ANN/Keras application model increased Incorrect-class F1 from 75.40% for the rule-based baseline to 90.34%. The selected experimental model, HistGradientBoosting with normalized landmarks and threshold 0.65, achieved 96.50% accuracy, 96.22% precision, 97.30% recall, 96.76% F1 for the Incorrect class, and 92.97% MCC. Runtime tests reached 28.03-29.34 FPS on representative views. The results support the feasibility of low-cost webcam-based posture monitoring using normalized landmarks, while participant diversity, independent external validation, and expert ergonomic annotation remain limitations.

## Keywords

Working posture detection; MediaPipe Pose; Human pose estimation; Machine learning; Webcam dataset

## 1. Introduction

Prolonged computer use is associated with posture errors such as forward head posture, shoulder imbalance, neck compression, and torso leaning. These errors often occur gradually during study or office work, so users may not notice them until discomfort appears. A practical monitoring system should therefore work with hardware that users already have, such as a laptop camera or a low-cost webcam, and should provide feedback without requiring a pressure cushion, wearable sensor, smart chair, or depth camera.

Previous posture monitoring studies have used pressure sensors, force sensors, motion-capture devices, smart chairs, RGB-D cameras, and RGB camera systems. Sensor-based systems can reach high accuracy in controlled settings, but they require dedicated hardware and are less convenient for ordinary desktop deployment (Luna-Perejon et al., 2021; Bourahmoune et al., 2022; Tsai et al., 2023; Odesola et al., 2024). Depth-camera and RGB-D approaches provide richer geometric information, but they assume hardware that many users do not have (Zeng et al., 2017; Kulikajevas et al., 2021). RGB camera and pose-estimation approaches reduce this hardware barrier, yet a complete desktop pipeline still needs clear feature construction, a transparent baseline, model comparison, runtime evaluation, warning logic, and logging for later analysis.

This paper follows an Applied Research direction. It does not propose a new pose estimation model or claim general superiority over prior studies. Instead, it applies an existing pose estimation model, MediaPipe Pose, to a project-specific webcam dataset and studies whether normalized landmark features, ergonomic geometric features, rule-based detection, and lightweight classifiers can support a usable desktop posture monitoring system.

The contributions are:

1. A self-collected webcam/video dataset with metadata and project-specific Correct posture and Incorrect posture labels.
2. A unified feature representation comparing raw MediaPipe Pose landmarks, body-normalized landmarks, ergonomic geometric indicators, and combined feature groups.
3. An evaluation and implementation pipeline covering a rule-based baseline, ANN/Keras application model, lightweight classifier benchmarking, corrected external evaluation, participant-wise evaluation, threshold calibration, runtime FPS, warning behavior, and SQLite logging.

## 2. Related Work

**Sensor-based and depth-camera-based posture recognition.** Sensor-based posture systems commonly use pressure cushions, force sensors, inertial sensors, or smart chairs. Luna-Perejon et al. (2021) built an IoT sitting-posture classification device using force-sensitive resistors and neural networks. Bourahmoune et al. (2022) proposed an intelligent posture training system based on a pressure-sensing IoT cushion. Tsai et al. (2023) reported an automated sitting posture recognition system using pressure sensors, and Wang et al. (2022) studied sitting posture recognition using a spiking neural network with pressure data. These systems show that dedicated sensors can provide useful posture signals, but they add hardware cost and may be less suitable for webcam-only desktop use.

Depth and RGB-D approaches reduce the need for wearable sensors but still require special imaging hardware. Zeng et al. (2017) recognized learner sitting posture from depth images. Kulikajevas et al. (2021) used RGB-D sequences and a deep recurrent hierarchical model for sitting posture recognition. These studies are important references for computer-vision-based posture analysis, but their hardware assumptions differ from a webcam-only application.

**RGB camera and pose-landmark-based posture recognition.** RGB camera systems are closer to ordinary laptop and office settings. Estrada et al. (2023) modeled proper and improper sitting posture of computer users using machine vision. Chen (2019) used OpenPose for sitting posture recognition, showing that pose estimation can act as an intermediate representation for posture classification. Chaikhamwang et al. (2025) studied MediaPipe and computer vision for office-syndrome risk reduction. These works motivate the use of visual landmarks rather than raw image classification alone.

Pose estimation methods provide the technical basis for such systems. OpenPose introduced real-time multi-person 2D pose estimation using part affinity fields (Cao et al., 2019). MediaPipe provides a graph-based framework for perception pipelines (Lugaresi et al., 2019), while BlazePose supports on-device real-time body pose tracking (Bazarevsky et al., 2020). MediaPipe Pose is suitable for a lightweight desktop application because it returns compact landmark coordinates that can be converted into tabular features. Google AI Edge documentation is used only as an implementation reference for the pose landmarker, not as a Related Work substitute for peer-reviewed studies.

**Reviews, datasets, and ergonomic context.** Recent reviews describe the diversity of sensing modalities, datasets, feedback strategies, and validation protocols in posture recognition (Jiang et al., 2023; Nadeem et al., 2024; Krauter et al., 2024; Roggio et al., 2024). The MultiPosture dataset provides MediaPipe-derived body keypoints for multi-task sitting posture recognition (Carneros Prado et al., 2024), and Carneros-Prado et al. (2024) compared neural models for that task. Ergonomic assessment methods such as RULA and REBA remain relevant for future expert annotation and risk interpretation (McAtamney and Corlett, 1993; Hignett and McAtamney, 2000), although this project does not yet use expert ergonomic scores as labels.

The gap addressed in this paper is therefore specific: a webcam-only desktop pipeline that combines MediaPipe Pose landmarks, normalized and ergonomic feature groups, an interpretable rule-based baseline, multiple lightweight classifiers, calibrated external evaluation, runtime measurement, warning behavior, and local logging. The contribution is the applied system and evaluation protocol, not MediaPipe itself.

## 3. Proposed Webcam-Based Posture Monitoring System

The proposed system processes input from a webcam, an IP camera, or an MP4 video file through a sequential pipeline. First, the OpenCV Frame Capture Module reads frames from the selected input source. The Landmark Extraction Module then applies MediaPipe Pose to detect 33 body landmarks. Next, the Feature Construction Module converts these landmarks into raw, normalized, and ergonomic feature groups. The Posture Classification Module estimates the probability of Correct or Incorrect posture. The Temporal Smoothing Module reduces short-term frame-level fluctuations before the Warning and Logging Module triggers alerts when the duration and cooldown conditions are satisfied. Finally, SQLite Session Logs and Dashboard Statistics store session-level posture information for later analysis. Fig. 1 summarizes this processing flow.

Fig. 1. System architecture of the proposed webcam-based posture monitoring system.

**Landmark extraction.** For each input frame, MediaPipe Pose estimates 33 body landmarks. Each landmark provides normalized image coordinates and a relative depth value. The raw landmark vector is:

```latex
\mathbf{x}_{raw} =
[x_0, y_0, z_0, x_1, y_1, z_1, \ldots, x_{32}, y_{32}, z_{32}]
```

Here, \(x_i\), \(y_i\), and \(z_i\) are the MediaPipe coordinates of landmark \(i\). The vector has 99 values. If landmarks are not detected, the frame is treated as a no-person-detected frame rather than a normal posture classification sample.

**Feature construction.** The system uses three main feature groups. The `raw_99` group contains all 33 landmarks with \(x\), \(y\), and \(z\) coordinates. The `normalized_99` group centers landmarks at the shoulder midpoint and scales them by a body-size proxy. The `ergonomic_14` group contains interpretable geometric indicators related to the head, neck, shoulders, upper torso, and hand-to-mouth relation.

The shoulder midpoint is:

```latex
\mathbf{s}_{mid} = \frac{\mathbf{s}_{left} + \mathbf{s}_{right}}{2}
```

Here, \(\mathbf{s}_{left}\) and \(\mathbf{s}_{right}\) are the left and right shoulder points in the image plane.

The body scale is:

```latex
\alpha = \max(w_s, l_t, \epsilon)
```

Here, \(w_s\) is shoulder width, \(l_t\) is a torso-length proxy, and \(\epsilon\) prevents division by zero.

The normalized landmark coordinates are:

```latex
\hat{x}_i = \frac{x_i - s_{mid,x}}{\alpha}, \quad
\hat{y}_i = \frac{y_i - s_{mid,y}}{\alpha}, \quad
\hat{z}_i = \frac{z_i}{\alpha}
```

Here, \(\hat{x}_i\), \(\hat{y}_i\), and \(\hat{z}_i\) are normalized coordinates for landmark \(i\). The ergonomic features include `shoulder_y_diff`, `shoulder_tilt_angle`, `torso_lean_angle`, `head_offset_x`, `nose_to_shoulder_y`, `nose_shoulder_clearance_ratio`, `neck_compression_detected`, hand-mouth ratios, `chin_rest_detected`, `shoulder_width`, `torso_length`, `head_shoulder_distance`, and `min_hand_mouth_ratio`.

Fig. 2. Feature construction from MediaPipe Pose landmarks to raw, normalized, ergonomic, and combined feature groups.

Table 1. Main ergonomic/geometric features used by the project.

| Feature | Definition | Main landmarks | Purpose |
|---|---|---|---|
| `shoulder_width` | 2D distance between left and right shoulders. | Left shoulder, right shoulder | Body-scale proxy for normalization. |
| `shoulder_tilt_angle` | Shoulder-line angle in degrees. | Left shoulder, right shoulder | Detect shoulder imbalance or tilted sitting. |
| `torso_lean_angle` | Upper-body centerline angle relative to the vertical direction. | Shoulder midpoint, hip midpoint | Detect torso leaning. |
| `head_offset_x` | Horizontal nose offset from the shoulder midpoint. | Nose, left/right shoulders | Detect head displacement from the shoulder axis. |
| `nose_shoulder_clearance_ratio` | Nose-to-shoulder vertical clearance normalized by torso height. | Nose, shoulders, hips | Detect deep neck compression. |
| `neck_compression_detected` | Binary indicator when the clearance ratio is below the rule threshold. | Nose, shoulders, hips | Mark deep neck compression risk. |
| `min_hand_mouth_ratio` | Minimum left/right hand-mouth distance normalized by shoulder width. | Wrist/index/pinky/thumb, mouth landmarks | Detect hand near mouth or chin area. |
| `chin_rest_detected` | Binary indicator when either hand is near the mouth/chin proxy. | Hand landmarks, mouth landmarks | Detect possible chin/hand support. |

Table 1 summarizes the ergonomic features most relevant to the rule-based baseline and error interpretation. The definitions are intentionally compact because the experimental classifier primarily uses feature groups rather than a new ergonomic scoring model.

**Classification.** The ANN/Keras application model is a feed-forward neural network with three hidden layers. The input layer receives the selected posture feature vector. The hidden layers contain 128, 64, and 32 neurons, respectively. Batch normalization and dropout are applied after the first two hidden layers, while dropout is also applied after the third hidden layer. The output layer contains one sigmoid neuron that estimates the probability of Incorrect posture.

Given the estimated Incorrect-posture probability \(p\) and threshold \(\tau\), the predicted label is:

```latex
\hat{y} =
\begin{cases}
1, & p \ge \tau \\
0, & p < \tau
\end{cases}
```

Here, \(\hat{y}=1\) denotes Incorrect posture and \(\hat{y}=0\) denotes Correct posture. The application loads `ann_best.keras` and `scaler.pkl`. The desktop demo also exposes the selected HistGradientBoosting model as a separate option, but the paper distinguishes between the original ANN/Keras application model and the selected experimental model.

**Rule-based baseline.** The rule-based baseline uses manually defined geometric thresholds. It checks shoulder imbalance, shoulder tilt, torso lean, head offset, nose-to-shoulder relation, neck compression, and hand-mouth proximity. A frame is labeled Incorrect posture when one or more rules indicate risk. This baseline is retained because it is interpretable and does not require training.

Table 2. Rule-based baseline indicators used in the interpretable baseline.

| Rule indicator | Condition | Threshold | Interpretation |
|---|---|---:|---|
| Visibility gate | Mean visibility of required landmarks is lower than the gate. | 0.50 | Mark no-person or low-confidence state. |
| Shoulder vertical difference | `shoulder_y_diff` is greater than the threshold. | 0.06 | Detect uneven shoulder height. |
| Shoulder tilt | `shoulder_tilt_angle` is greater than the threshold. | 10.0 degrees | Detect shoulder-line tilt. |
| Torso lean | `torso_lean_angle` is greater than the threshold. | 12.0 degrees | Detect upper-body leaning. |
| Head offset | `head_offset_x` is greater than the threshold. | 0.10 | Detect head displacement from shoulder axis. |
| Neck compression | `nose_shoulder_clearance_ratio` is lower than the threshold. | 0.12 | Detect nose close to shoulder height, indicating deep neck compression. |
| Hand-mouth ratio | Left or right hand-mouth ratio is lower than the threshold. | 0.45 | Detect hand close to mouth/chin region. |
| Hand-mouth distance | Left or right hand-mouth distance is lower than the threshold. | 0.13 | Detect absolute hand proximity to mouth/chin proxy. |
| Hand visibility gate | Hand landmark visibility is lower than the gate. | 0.35 | Ignore low-confidence hand landmarks in hand-mouth rules. |

The threshold values in Table 2 are taken from the shared rule-based baseline utility in the project. The baseline is used as an interpretable reference rather than as an ergonomic standard.

**Temporal smoothing, warning, and logging.** The predicted Incorrect probability is smoothed across a short frame window. A warning event is triggered only if the smoothed probability exceeds the configured threshold for the required duration. A cooldown interval reduces repeated alerts. SQLite stores session, posture, warning, confidence, frame, and timing information. In the current project database, there are 64 working sessions, 989 posture log entries, and 10 daily statistics records.

Algorithm 1. Real-time working posture monitoring loop.

1. Initialize the video source, MediaPipe Pose, classifier, scaler, smoothing buffer, and SQLite session.
2. Capture the next frame from webcam, IP camera, or MP4 input.
3. Detect MediaPipe Pose landmarks.
4. If landmarks are missing or unreliable, mark the no-person state and log it when needed.
5. Construct the selected feature vector.
6. Apply the scaler if the selected classifier requires it.
7. Predict the Incorrect-posture probability.
8. Apply temporal smoothing to the recent probabilities.
9. Trigger a warning only when duration and cooldown conditions are satisfied.
10. Store the posture status and warning event in SQLite.

## 4. Experimental Protocol

The project follows an existing-model-plus-new-dataset/features protocol. MediaPipe Pose is used as an existing landmark extractor, and the experiments compare feature groups and lightweight classifiers on the project dataset.

Table 3. Dataset splits used in the experiments.

| Split | Videos | Participants | Samples | Correct | Incorrect |
|---|---:|---:|---:|---:|---:|
| Development/training set | 84 | 5 | 11,022 | 4,438 (40.26%) | 6,584 (59.74%) |
| Corrected external set | 10 | 1 | 1,658 | 768 (46.32%) | 890 (53.68%) |

The full video manifest contains 94 videos, including 84 development videos and 10 corrected external videos. At the video level, 39 videos are labeled Correct and 55 videos are labeled Incorrect.

Table 3 is split-oriented rather than file-oriented. The development set supports model training, classifier comparison, and participant-wise evaluation. The corrected external set supports the main corrected external result, but it is limited because it contains only P01. The metadata include `source_video`, `frame_index`, `timestamp_sec`, `sample_fps`, `video_fps`, `participant_id`, `view_angle`, and `camera_type`. Correct posture and Incorrect posture labels are project-specific and have not been validated by expert ergonomic annotation.

The labeling protocol follows the project video organization. Correct videos were recorded when participants maintained a relatively acceptable working posture. Incorrect videos contain intentional posture errors such as forward head posture, shoulder imbalance, torso leaning, neck compression, chin or hand support, or corresponding error types represented in the project. Labels are assigned at the video or segment level and inherited by sampled frames during feature extraction. The corrected external set is used as a project-corrected external set; no inter-rater agreement or expert ergonomic annotation is available in the current artifacts.

Table 4. Feature groups used in the experiments.

| Feature group | Features | Description | Role |
|---|---:|---|---|
| `raw_99` | 99 | 33 MediaPipe Pose landmarks with \(x\), \(y\), \(z\). | Basic landmark representation. |
| `normalized_99` | 99 | Landmarks centered by shoulder midpoint and scaled by body size. | Reduces body-size and camera-distance effects. |
| `ergonomic_14` | 14 | Shoulder, torso, head, neck, and hand-mouth indicators. | Interpretable posture cues. |
| `combined_raw_ergonomic` | 113 | Raw landmarks plus ergonomic indicators. | Tests raw landmarks with explicit posture cues. |
| `combined_normalized_ergonomic` | 113 | Normalized landmarks plus ergonomic indicators. | Tests normalized landmarks with explicit posture cues. |

Table 4 separates raw pose representation from interpretable ergonomic indicators. The selected experimental model uses `normalized_99`, while the ergonomic features remain useful for the rule-based baseline and for explaining posture errors.

The candidate models are the rule-based baseline, ANN/Keras, Logistic Regression, SVM RBF, Random Forest, MLP sklearn, and HistGradientBoosting. Model selection uses Incorrect-class F1 as the primary criterion, with Incorrect-class recall and MCC as tie-breakers. The selected experimental model is `hist_gradient_boosting__normalized_99`. Threshold calibration selected 0.65 in the current final protocol. Because the project artifacts indicate that calibration is tied to the corrected external protocol, the final result should be interpreted as calibrated corrected-external performance, not as a strictly independent hold-out result.

Experiments were run with Python 3.11.9. The main recorded libraries are OpenCV 4.11.0, MediaPipe 0.10.21, NumPy 1.26.4, scikit-learn 1.6.1, TensorFlow 2.16.2, matplotlib, CustomTkinter, Pillow, joblib, pytest, and statsmodels 0.14.6. Runtime benchmarking used 640 x 360 input, MediaPipe complexity 1, and up to 120 sampled frames per video. Hardware details are not recorded in the project artifacts.

For evaluation, TP, TN, FP, and FN denote true positives, true negatives, false positives, and false negatives. The positive class is Incorrect posture.

```latex
\mathrm{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}
```

Accuracy measures the proportion of all correctly classified samples.

```latex
\mathrm{Precision} = \frac{TP}{TP + FP}
```

Precision measures the proportion of predicted Incorrect samples that are truly Incorrect.

```latex
\mathrm{Recall} = \frac{TP}{TP + FN}
```

Recall measures the proportion of true Incorrect samples detected by the model.

```latex
\mathrm{F1} = \frac{2 \times \mathrm{Precision} \times \mathrm{Recall}}{\mathrm{Precision} + \mathrm{Recall}}
```

F1-score balances Precision and Recall for the Incorrect class. MCC is also reported because it is informative when both classes and error types matter.

Runtime is reported as:

```latex
\mathrm{FPS} = \frac{N}{T}
```

Here, \(N\) is the number of processed frames and \(T\) is processing time in seconds.

## 5. Evaluation and Discussion

Table 5 reports the corrected external comparison between the rule-based baseline and the ANN/Keras application model.

Table 5. Corrected external comparison between rule-based baseline and ANN/Keras application model.

| Method | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC |
|---|---:|---:|---:|---:|---:|
| Rule-based baseline | 67.49% | 63.49% | 92.81% | 75.40% | 37.56% |
| ANN/Keras application model | 90.17% | 95.61% | 85.62% | 90.34% | 80.90% |

The ANN increased Incorrect-class F1 from 75.40% to 90.34%. The rule-based baseline reached higher recall, but its precision was much lower, indicating more false warnings on Correct posture frames. This tradeoff is important for a warning system because missed posture errors and unnecessary alerts affect users in different ways.

Table 6 lists the top five model and feature combinations from the model registry before final threshold calibration.

Table 6. Top classifier and feature combinations in the model registry.

| Rank | Model | Feature group | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | HistGradientBoosting | `normalized_99` | 95.96% | 95.07% | 97.53% | 96.28% | 91.89% |
| 2 | Random Forest | `normalized_99` | 95.90% | 94.67% | 97.87% | 96.24% | 91.79% |
| 3 | SVM RBF | `ergonomic_14` | 95.36% | 96.89% | 94.38% | 95.62% | 90.72% |
| 4 | SVM RBF | `normalized_99` | 94.51% | 92.82% | 97.30% | 95.01% | 89.04% |
| 5 | Random Forest | `combined_normalized_ergonomic` | 94.27% | 91.89% | 97.98% | 94.83% | 88.65% |

The top two configurations use `normalized_99`, suggesting that body normalization is useful under the current project protocol. SVM RBF with only `ergonomic_14` also performs strongly, showing that interpretable geometric indicators carry useful posture information. These results are local to the project dataset and should not be interpreted as a leaderboard against other studies.

Table 7 reports the calibrated corrected-external performance of the selected experimental model.

Table 7. Final selected experimental model on the corrected external set.

| Model | Feature group | Threshold | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC | FP | FN |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| HistGradientBoosting | `normalized_99` | 0.65 | 96.50% | 96.22% | 97.30% | 96.76% | 92.97% | 34 | 24 |

The selected model produced 34 false positives and 24 false negatives. False positives may produce unnecessary warnings, while false negatives are missed Incorrect posture frames. For a health-oriented warning system, recall for Incorrect posture is important, but excessive false alerts can reduce user trust. The selected threshold balances these factors under the current calibrated protocol.

Fig. 3. Confusion matrix of the final selected model on the corrected external set.

Fig. 4. Threshold calibration on the corrected external set.

Table 8 reports leave-one-participant-out evaluation on the raw development dataset.

Table 8. Leave-one-participant-out evaluation on the raw dataset.

| Held-out participant | Samples | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC |
|---|---:|---:|---:|---:|---:|---:|
| P01 | 3,524 | 90.81% | 98.28% | 84.88% | 91.09% | 82.64% |
| P02 | 1,225 | 79.35% | 77.87% | 91.55% | 84.16% | 56.55% |
| P03 | 2,208 | 93.03% | 99.85% | 90.05% | 94.70% | 85.55% |
| P04 | 1,815 | 86.67% | 79.37% | 100.00% | 88.50% | 75.92% |
| P05 | 2,250 | 93.56% | 95.63% | 94.24% | 94.93% | 86.11% |
| Mean | - | 88.68% | - | - | 90.67% | 77.35% |

The participant-wise result is stronger evidence than a random internal frame split because the held-out participant is not used for training in each fold. However, it still uses the same project collection process. The lower P02 result suggests that body shape, camera placement, or posture style can affect performance.

Table 9 reports processing latency on representative videos.

Table 9. Runtime benchmark on representative videos.

| View angle | Processed frames | Pose detection rate | Mean total latency | p95 latency | Estimated FPS |
|---|---:|---:|---:|---:|---:|
| front | 52 | 100.00% | 35.31 ms | 38.80 ms | 28.32 |
| side_30 | 120 | 100.00% | 35.67 ms | 43.08 ms | 28.03 |
| side_90 | 120 | 100.00% | 34.08 ms | 38.95 ms | 29.34 |

The measured 28.03-29.34 FPS supports real-time feasibility for the core processing pipeline. This benchmark measures processing latency only. Full GUI FPS can be lower because drawing, Tkinter scheduling, camera buffering, audio playback, and SQLite logging add overhead.

Fig. 5. Temporal smoothing example showing raw frame probability, temporal mean, and decision threshold on corrected external predictions.

Fig. 6. SQLite logging flow used by the desktop application for session-level posture analysis.

The literature comparison should be treated as contextual. Sensor-based studies, RGB-D studies, RGB camera studies, and pose-landmark studies use different devices, label sets, participants, and split protocols. Therefore, this paper compares models only within the same project protocol and uses external literature to explain the research position rather than to claim superiority.

The main limitations are clear. The development set includes only five participants, and the corrected external set includes only P01. Labels are project-specific and have not been validated by expert ergonomic annotation or RULA/REBA-style scoring. The final selected model result is calibrated corrected-external performance rather than a strictly independent hold-out result. Public benchmark evaluation, such as on MultiPosture, has not yet been completed. Full GUI FPS has also not been measured.

**Data, Code, and Ethics Note.** Raw videos are not planned for public release because they may contain identifiable participants. Extracted landmark features may be shared after anonymization if participant consent and venue requirements permit. The collected data were used only for academic evaluation in this project. The current artifacts do not contain a formal consent form or ethics approval document, so the paper does not claim formal ethical approval.

## 6. Conclusion and Future Work

This paper presented a webcam-based working posture error detection system using MediaPipe Pose landmarks, normalized and ergonomic feature groups, a rule-based baseline, lightweight machine learning classifiers, and a Python desktop implementation. The study follows an Applied Research direction: existing pose estimation is combined with a project-specific dataset, feature engineering, classifier comparison, warning behavior, and local logging.

The project dataset contains 84 raw videos from five participants and 11,022 sampled frames. The corrected external set contains 10 videos and 1,658 frames. On this external set, the ANN/Keras application model increased Incorrect-class F1 from 75.40% for the rule-based baseline to 90.34%. The selected experimental model, HistGradientBoosting with `normalized_99` and threshold 0.65, achieved 96.50% accuracy, 96.76% Incorrect-class F1, and 92.97% MCC. Runtime testing reached 28.03-29.34 FPS on representative videos.

These results indicate that MediaPipe Pose landmarks and lightweight tabular classifiers can support a low-cost desktop posture warning pipeline. The rule-based baseline remains useful because it explains posture cues, while learned classifiers improve classification under the current data protocol. SQLite logging and dashboard statistics add session-level evidence for later analysis.

Future work should expand the dataset to more participants, camera positions, lighting conditions, and working environments. Expert ergonomic annotation or RULA/REBA-inspired labeling should be added if stronger ergonomic interpretation is required. Public benchmark evaluation, such as MultiPosture, should be performed after license and label-mapping checks. The selected HistGradientBoosting model should remain aligned with the desktop app behavior. Finally, the binary labels should be extended to multi-class posture types when sufficient labeled data are available.

## References

Bazarevsky, V., Grishchenko, I., Raveendran, K., Zhu, T., Zhang, F., & Grundmann, M. (2020). *BlazePose: On-device real-time body pose tracking*. arXiv. https://doi.org/10.48550/arXiv.2006.10204

Bourahmoune, K., Ishac, K., & Amagasa, T. (2022). Intelligent posture training: Machine-learning-powered human sitting posture recognition based on a pressure-sensing IoT cushion. *Sensors, 22*(14), 5337. https://doi.org/10.3390/s22145337

Cao, Z., Hidalgo, G., Simon, T., Wei, S.-E., & Sheikh, Y. (2019). OpenPose: Realtime multi-person 2D pose estimation using part affinity fields. *IEEE Transactions on Pattern Analysis and Machine Intelligence, 43*(1), 172-186. https://doi.org/10.1109/TPAMI.2019.2929257

Carneros Prado, D., Cabanero Gomez, L., Fontecha, J., Hervas, R., Gonzalez Diaz, I., & Johnson, E. (2024). *MultiPosture: A dataset of body joints keypoints extracted using MediaPipe for multi-task sitting posture recognition with upper and lower body labels* (Version v1) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.14230872

Carneros-Prado, D., Cabanero-Gomez, L., Johnson, E., Gonzalez, I., Fontecha, J., & Hervas, R. (2024). A comparison between multilayer perceptrons and Kolmogorov-Arnold networks for multi-task classification in sitting posture recognition. *IEEE Access, 12*, 180198-180209. https://doi.org/10.1109/ACCESS.2024.3510034

Chaikhamwang, S., Montri, W., Janthajirakowit, C., & Fongmanee, S. (2025). An intelligent platform for behavior modification and office syndrome risk reduction using MediaPipe and computer vision. *International Journal of Advanced Computer Science and Applications, 16*(10). https://doi.org/10.14569/IJACSA.2025.0161038

Chen, K. (2019). Sitting posture recognition based on OpenPose. *IOP Conference Series: Materials Science and Engineering, 677*(3), 032057. https://doi.org/10.1088/1757-899X/677/3/032057

Estrada, J. E., Vea, L. A., & Devaraj, M. (2023). Modelling proper and improper sitting posture of computer users using machine vision for a human-computer intelligent interactive system during COVID-19. *Applied Sciences, 13*(9), 5402. https://doi.org/10.3390/app13095402

Feradov, F., Markova, V., & Ganchev, T. (2022). Automated detection of improper sitting postures in computer users based on motion capture sensors. *Computers, 11*(7), 116. https://doi.org/10.3390/computers11070116

Google AI Edge. (n.d.). *Pose landmark detection guide*. MediaPipe Solutions. https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker

Hignett, S., & McAtamney, L. (2000). Rapid entire body assessment (REBA). *Applied Ergonomics, 31*(2), 201-205. https://doi.org/10.1016/S0003-6870(99)00039-3

Jiang, X., Hu, Z., Wang, S., & Zhang, Y. (2023). A survey on artificial intelligence in posture recognition. *Computer Modeling in Engineering & Sciences, 137*(1), 35-82. https://doi.org/10.32604/cmes.2023.027676

Kim, J.-W., Choi, J.-Y., Ha, E. J., & Choi, J.-H. (2023). Human pose estimation using MediaPipe Pose and optimization method based on a humanoid model. *Applied Sciences, 13*(4), 2700. https://doi.org/10.3390/app13042700

Krauter, C., Angerbauer, K., Sousa Calepso, A., Achberger, A., Mayer, S., & Sedlmair, M. (2024). Sitting posture recognition and feedback: A literature review. In *Proceedings of the CHI Conference on Human Factors in Computing Systems*. Association for Computing Machinery. https://doi.org/10.1145/3613904.3642657

Kulikajevas, A., Maskeliunas, R., & Damasevicius, R. (2021). Detection of sitting posture using hierarchical image composition and deep learning. *PeerJ Computer Science, 7*, e442. https://doi.org/10.7717/peerj-cs.442

Lugaresi, C., Tang, J., Nash, H., McClanahan, C., Uboweja, E., Hays, M., Zhang, F., Chang, C.-L., Yong, M. G., Lee, J., Chang, W.-T., Hua, W., Georg, M., & Grundmann, M. (2019). *MediaPipe: A framework for building perception pipelines*. arXiv. https://arxiv.org/abs/1906.08172

Luna-Perejon, F., Montes-Sanchez, J. M., Duran-Lopez, L., Vazquez-Baeza, A., Beasley-Bohorquez, I., & Sevillano-Ramos, J. L. (2021). IoT device for sitting posture classification using artificial neural networks. *Electronics, 10*(15), 1825. https://doi.org/10.3390/electronics10151825

McAtamney, L., & Corlett, E. N. (1993). RULA: A survey method for the investigation of work-related upper limb disorders. *Applied Ergonomics, 24*(2), 91-99. https://doi.org/10.1016/0003-6870(93)90080-S

Nadeem, M., Elbasi, E., Zreikat, A. I., & Sharsheer, M. (2024). Sitting posture recognition systems: Comprehensive literature review and analysis. *Applied Sciences, 14*(18), 8557. https://doi.org/10.3390/app14188557

Odesola, D. F., Kulon, J., Verghese, S., Partlow, A., & Gibson, C. (2024). Smart sensing chairs for sitting posture detection, classification, and monitoring: A comprehensive review. *Sensors, 24*(9), 2940. https://doi.org/10.3390/s24092940

Roggio, F., Trovato, B., Sortino, M., & Musumeci, G. (2024). A comprehensive analysis of the machine learning pose estimation models used in human movement and posture analyses: A narrative review. *Heliyon, 10*(21), e39977. https://doi.org/10.1016/j.heliyon.2024.e39977

Tlili, F., Haddad, R., Bouallegue, R., & Shubair, R. (2022). Machine learning algorithms application for the proposed sitting posture monitoring system. *Procedia Computer Science, 203*, 239-246. https://doi.org/10.1016/j.procs.2022.07.031

Tsai, M.-C., Chu, E. T.-H., & Lee, C.-R. (2023). An automated sitting posture recognition system utilizing pressure sensors. *Sensors, 23*(13), 5894. https://doi.org/10.3390/s23135894

Wang, J., Hafidh, B., Dong, H., & El Saddik, A. (2022). *Sitting posture recognition using a spiking neural network*. arXiv. https://doi.org/10.48550/arXiv.2212.12908

Zeng, X., Sun, B., Wang, E., Luo, W., & Liu, T. (2017). A method of learner's sitting posture recognition based on depth image. In *Proceedings of the 2017 2nd International Conference on Control, Automation and Artificial Intelligence (CAAI 2017)* (pp. 558-563). Atlantis Press. https://doi.org/10.2991/caai-17.2017.125
