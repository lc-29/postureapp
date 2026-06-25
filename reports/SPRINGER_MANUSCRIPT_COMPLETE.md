# Webcam-Based Working Posture Error Detection Using MediaPipe Pose and Lightweight Machine Learning

## Abstract

Prolonged computer work can lead to sustained incorrect sitting postures, but many posture monitoring systems rely on wearable sensors, pressure cushions, depth cameras, or controlled hardware. This paper presents a webcam-based desktop system for working posture error detection using OpenCV, MediaPipe Pose landmarks, engineered posture features, lightweight machine learning classifiers, and real-time warning logic. MediaPipe Pose is used to extract 33 body landmarks from webcam, IP camera, or MP4 video input. The system constructs raw 99-dimensional landmark features, body-normalized landmark features, and ergonomic geometric indicators related to shoulder alignment, torso inclination, head position, neck compression, and hand-to-mouth proximity. A self-collected dataset contains 84 raw videos from five participants and 11,022 sampled frames, including 4,438 Correct posture samples and 6,584 Incorrect posture samples. A corrected external set contains 10 videos and 1,658 frames. The current desktop application integrates an ANN/Keras classifier, while the experimental protocol compares rule-based detection, ANN, Logistic Regression, SVM RBF, Random Forest, MLP, and HistGradientBoosting. On the corrected external set, the ANN achieved 90.17% accuracy and 90.34% F1 for the Incorrect class, compared with 67.49% accuracy and 75.40% F1 for the rule-based baseline. The best selected experimental model, HistGradientBoosting with normalized landmarks and threshold 0.65, achieved 96.50% accuracy, 96.76% F1, and 92.97% MCC. Runtime evaluation showed approximately 28 FPS across representative views.

## Keywords

Working posture detection; MediaPipe Pose; Human pose estimation; Machine learning; Webcam-based monitoring

## 1. Introduction

Incorrect working posture during long computer use is a common ergonomic problem in office, study, and remote-work environments. Sustained forward head posture, shoulder imbalance, torso leaning, and neck compression may not be noticed immediately by the user. A practical monitoring system should therefore provide continuous feedback without requiring special hardware or intrusive wearable devices.

Existing sitting posture recognition systems have used pressure sensors, smart chairs, motion sensors, RGB-D cameras, and camera-based computer vision. Sensor-based and smart-chair systems can provide high-quality measurements, but they require additional equipment and are less convenient for ordinary laptop or desktop users (Tsai et al., 2023; Odesola et al., 2024). Depth-camera and RGB-D approaches can exploit richer geometry, but the hardware is not always available in daily computer work settings (Kulikajevas et al., 2021). Recent pose estimation frameworks, including OpenPose and MediaPipe, make it possible to estimate human body landmarks from ordinary RGB video (Cao et al., 2018; Lugaresi et al., 2019; Bazarevsky et al., 2020).

For a desktop posture monitoring application, a gap remains between recognition accuracy and practical deployment. A useful system should combine low-cost webcam input, interpretable posture indicators, a machine learning classifier, a clear baseline, real-time warning behavior, and local logging for later review. Several studies report sitting posture classification or feedback systems, but fewer present an end-to-end desktop pipeline with self-collected webcam/video data, feature ablation, rule-based comparison, classifier benchmarking, runtime evaluation, and session-level logging in one system (Estrada et al., 2023; Nadeem et al., 2024; Krauter et al., 2024).

This study follows the direction of using existing pose estimation and machine learning models with a project-specific dataset and feature representation. The contribution is not a new pose estimation model or a new deep learning architecture. Instead, the contribution is an applied, reproducible pipeline for webcam-based working posture error detection.

The main contributions are:

1. A self-collected webcam/video dataset with metadata and binary project-specific labels, Correct posture and Incorrect posture.
2. A unified feature representation based on 33 MediaPipe Pose landmarks, including raw 99-dimensional features, body-normalized features, and ergonomic geometric indicators.
3. An evaluation protocol including a rule-based baseline, ANN and classical machine learning classifiers, corrected external testing, participant-wise evaluation, runtime FPS measurement, and integration into a Python desktop application.

## 2. Related Work

### 2.1 Sensor-Based and Depth-Camera-Based Sitting Posture Recognition

Sensor-based posture recognition has been widely studied using pressure cushions, force sensors, motion capture devices, and smart chairs. Tsai et al. (2023) used pressure sensors embedded in a chair cushion to recognize multiple sitting postures with high accuracy. Luna-Perejon et al. (2021) also investigated sitting posture classification using pressure sensors and artificial neural networks. Feradov et al. (2022) studied improper sitting posture detection using motion capture sensors, while Odesola et al. (2024) reviewed smart sensing chairs for sitting posture detection and monitoring.

These approaches are useful references because they show the value of continuous sitting posture monitoring. However, they also depend on dedicated hardware. This limits direct adoption for students or office users who only have a laptop camera or a low-cost webcam. Depth-camera methods reduce the need for body-worn sensors but still require special devices. For example, Kulikajevas et al. (2021) used RGB-D camera sequences and deep learning to recognize sitting postures. Such systems provide richer spatial information than RGB webcams, but their assumptions differ from a low-cost desktop application.

### 2.2 Vision-Based Posture Recognition Using RGB Cameras

RGB camera-based posture recognition is closer to the target environment of this study. Estrada et al. (2023) modeled proper and improper sitting posture of computer users using machine vision in a work-from-home context. Their work is relevant because it uses visual input for posture monitoring rather than pressure or wearable sensors. Chen (2019) studied sitting posture recognition based on OpenPose, showing how body pose estimation can be used as an intermediate representation for posture classification.

Vision-based approaches reduce hardware cost, but they must handle camera angle, lighting variation, person size, and partial landmark instability. In this project, these issues are addressed by using MediaPipe Pose landmarks, normalized landmark features, and additional ergonomic geometric indicators. The system is not designed as a generic image classifier; it focuses on landmark-derived tabular features that can be used with lightweight machine learning models.

### 2.3 Pose-Landmark-Based Posture Analysis Using OpenPose and MediaPipe

OpenPose introduced a real-time multi-person 2D pose estimation approach using part affinity fields (Cao et al., 2018). MediaPipe later provided a framework for building perception pipelines and supports efficient on-device pose tracking (Lugaresi et al., 2019; Bazarevsky et al., 2020). MediaPipe Pose and related landmark-based methods are attractive for desktop posture monitoring because they provide a compact body representation without requiring a large image classifier.

Recent work has also used pose landmarks for sitting posture recognition and feedback. The MultiPosture dataset provides MediaPipe-derived body joint keypoints for multi-task sitting posture recognition (Carneros Prado et al., 2024). Carneros-Prado et al. (2024) compared neural approaches for sitting posture recognition, while Sahoo et al. (2026) proposed a real-time IoT framework for sitting posture detection. Reviews by Nadeem et al. (2024), Krauter et al. (2024), and Roggio et al. (2024) show that sitting posture recognition remains an active area with different sensing modalities, feedback mechanisms, and validation protocols.

Compared with these works, the present study emphasizes an end-to-end desktop implementation using webcam/video input, MediaPipe Pose landmarks, interpretable feature engineering, rule-based baseline comparison, classifier benchmarking, runtime evaluation, and SQLite-based session logging. Literature results are used only as contextual background because datasets, labels, sensors, and validation protocols differ.

## 3. Proposed Method

The proposed webcam-based posture monitoring system processes frames from a webcam, IP camera, or MP4 video file. Each frame is captured by OpenCV and passed to MediaPipe Pose for landmark extraction. Landmark coordinates are converted into feature vectors and classified as Correct posture or Incorrect posture. The result is then passed through temporal smoothing, thresholding, warning logic, and SQLite logging.

[Insert Fig. 1 here: System architecture of the proposed webcam-based posture monitoring system]

Fig. 1. System architecture of the proposed webcam-based posture monitoring system.

The processing modules are:

1. OpenCV Frame Capture Module.
2. Landmark Extraction Module.
3. Feature Construction Module.
4. Posture Classification Module.
5. Rule-Based Baseline Module.
6. Warning and Logging Module.
7. Dashboard Statistics Module.

### 3.1 Landmark Extraction

For each input frame, MediaPipe Pose estimates 33 pose landmarks. Each landmark contains normalized image coordinates and a relative depth value. The raw landmark representation is:

```text
x_i, y_i, z_i,  i = 0, 1, ..., 32
```

The raw feature vector therefore contains 99 values:

```latex
\mathbf{x}_{raw} =
[x_0, y_0, z_0, x_1, y_1, z_1, \ldots, x_{32}, y_{32}, z_{32}]
```

where \(x_i\), \(y_i\), and \(z_i\) are the MediaPipe coordinates of landmark \(i\). If no pose landmarks are detected, the frame is marked as no person detected and is not classified as a normal posture sample.

### 3.2 Feature Construction

The system uses three main feature groups. The first group, `raw_99`, contains the 99 raw MediaPipe landmark coordinates. The second group, `normalized_99`, centers landmark coordinates around the shoulder midpoint and scales them by body size. The third group, `ergonomic_14`, contains interpretable geometric indicators related to posture risk.

The shoulder midpoint is defined as:

```latex
\mathbf{s}_{mid} = \frac{\mathbf{s}_{left} + \mathbf{s}_{right}}{2}
```

where \(\mathbf{s}_{left}\) and \(\mathbf{s}_{right}\) are the left and right shoulder landmark coordinates in the image plane.

The body scale is computed as:

```latex
\alpha = \max(w_s, l_t, \epsilon)
```

where \(w_s\) is the shoulder width, \(l_t\) is the torso length proxy, and \(\epsilon\) is a small constant used to avoid division by zero.

The normalized coordinates are:

```latex
\hat{x}_i = \frac{x_i - s_{mid,x}}{\alpha}, \quad
\hat{y}_i = \frac{y_i - s_{mid,y}}{\alpha}, \quad
\hat{z}_i = \frac{z_i}{\alpha}
```

where \(\hat{x}_i\), \(\hat{y}_i\), and \(\hat{z}_i\) are normalized coordinates for landmark \(i\), and \(s_{mid,x}\), \(s_{mid,y}\) are the shoulder midpoint coordinates.

[Insert Fig. 2 here: MediaPipe Pose landmarks and selected ergonomic indicators]

Fig. 2. MediaPipe Pose landmarks and selected ergonomic indicators used for posture feature construction.

### 3.3 Posture Classification

The current desktop application uses an ANN/Keras classifier. The ANN architecture is:

```text
Input -> Dense(128) -> BatchNorm -> Dropout
      -> Dense(64) -> BatchNorm -> Dropout
      -> Dense(32) -> Dropout
      -> Dense(1, sigmoid)
```

The output is a probability of Incorrect posture. Given a probability \(p\) and threshold \(\tau\), the predicted class is:

```latex
\hat{y} =
\begin{cases}
1, & p \ge \tau \\
0, & p < \tau
\end{cases}
```

where \(\hat{y}=1\) denotes Incorrect posture and \(\hat{y}=0\) denotes Correct posture. In the current application, the ANN model is loaded from `ann_best.keras` and the scaler is loaded from `scaler.pkl`.

The experimental protocol also trains and compares Logistic Regression, SVM RBF, Random Forest, MLP, and HistGradientBoosting. The best selected model in the current experimental protocol is `hist_gradient_boosting__normalized_99` with a calibrated threshold of 0.65. This selected model is reported as the best experimental model, while the current desktop application is described as using ANN mode unless the registry model is integrated later.

### 3.4 Rule-Based Baseline

A rule-based baseline is used to provide an interpretable comparison. It uses geometric indicators such as shoulder height difference, shoulder tilt angle, torso lean angle, horizontal head offset, nose-to-shoulder vertical position, neck compression, and hand-to-mouth proximity. If one or more indicators exceed predefined thresholds, the frame is classified as Incorrect posture.

The rule-based baseline is not intended to replace the classifier. It provides a transparent reference showing how much a learned model improves over manually selected thresholds under the same external evaluation set.

### 3.5 Realtime Warning and Logging

The predicted probability is smoothed across a short frame window. A warning is triggered only when the smoothed probability exceeds the configured threshold for a minimum duration. A cooldown period prevents repeated warnings from being played too frequently. The system logs session information, posture status changes, warning events, frame counts, confidence values, and statistics to SQLite.

The approximate processing rate is computed as:

```latex
FPS = \frac{N}{T}
```

where \(N\) is the number of processed frames and \(T\) is the processing time in seconds.

## 4. Dataset and Feature Extraction

The dataset is project-specific and was collected for working posture error detection. The labels are binary: Correct posture and Incorrect posture. These labels are project-specific labels and were not independently verified by expert ergonomic annotation.

The raw training set contains 84 videos from five participants, P01 to P05. The sampled 2 FPS training CSV contains 11,022 frame-level samples, including 4,438 Correct posture samples and 6,584 Incorrect posture samples. The corrected external set contains 10 videos and 1,658 samples. The external set is useful for preliminary validation, but it currently contains only P01.

Table 1. Dataset distribution used in the experiments.

| Dataset file | Videos | Participants | Samples | Correct | Incorrect |
|---|---:|---:|---:|---:|---:|
| `posture_data.csv` | This information should be completed before submission | This information should be completed before submission | 5,377 | 2,169 (40.34%) | 3,208 (59.66%) |
| `posture_data_2fps.csv` | 84 | 5 | 11,022 | 4,438 (40.26%) | 6,584 (59.74%) |
| `posture_data_2fps_with_metadata.csv` | 84 | 5 | 11,022 | 4,438 (40.26%) | 6,584 (59.74%) |
| `posture_external_test_2fps_with_metadata.csv` | 10 | 1 | 1,658 | 768 (46.32%) | 890 (53.68%) |
| `video_manifest.csv` | 94 | 5 | This information should be completed before submission | 39 videos (41.49%) | 55 videos (58.51%) |

The metadata columns include `source_video`, `frame_index`, `timestamp_sec`, `sample_fps`, `video_fps`, `participant_id`, `view_angle`, and `camera_type`. These fields support video-wise evaluation, participant-wise analysis, and error inspection.

Table 2. Feature groups used in the experiments.

| Feature group | Number of features | Description |
|---|---:|---|
| `raw_99` | 99 | 33 MediaPipe Pose landmarks with \(x\), \(y\), and \(z\) coordinates. |
| `normalized_99` | 99 | Raw landmarks centered by shoulder midpoint and scaled by body size. |
| `ergonomic_14` | 14 | Interpretable posture indicators derived from shoulders, torso, head, neck, and hand-to-mouth geometry. |
| `combined_raw_ergonomic` | 113 | Raw 99 landmark features combined with ergonomic indicators. |
| `combined_normalized_ergonomic` | 113 | Normalized 99 landmark features combined with ergonomic indicators. |

The ergonomic indicators include `shoulder_y_diff`, `shoulder_tilt_angle`, `torso_lean_angle`, `head_offset_x`, `nose_to_shoulder_y`, `nose_shoulder_clearance_ratio`, `neck_compression_detected`, left and right hand-mouth ratios, `chin_rest_detected`, `shoulder_width`, `torso_length`, `head_shoulder_distance`, and `min_hand_mouth_ratio`.

[Insert Fig. 3 here: Feature construction pipeline from MediaPipe landmarks to raw, normalized, and ergonomic features]

Fig. 3. Feature construction pipeline from MediaPipe landmarks to raw, normalized, and ergonomic features.

## 5. Experimental Setup

The experimental protocol evaluates both the current application model and additional machine learning classifiers. The current desktop application uses the ANN/Keras model and the saved scaler. The broader research protocol compares the following models:

1. Rule-based baseline.
2. ANN/Keras classifier.
3. Logistic Regression.
4. SVM RBF.
5. Random Forest.
6. MLP sklearn.
7. HistGradientBoosting.

The best selected model is chosen by Incorrect-class F1-score, with Incorrect-class recall and MCC used as tie-breakers. The selected model in the current protocol is `hist_gradient_boosting__normalized_99`, with decision threshold \(\tau = 0.65\).

The evaluation uses Accuracy, Precision, Recall, F1-score, MCC, confusion matrix, video-wise metrics, participant-wise metrics, and runtime FPS. For binary classification, TP, TN, FP, and FN denote true positives, true negatives, false positives, and false negatives, respectively. Here, the positive class is Incorrect posture.

```latex
Accuracy = \frac{TP + TN}{TP + TN + FP + FN}
```

Accuracy measures the proportion of all correctly classified samples.

```latex
Precision = \frac{TP}{TP + FP}
```

Precision measures how many predicted Incorrect posture samples are truly Incorrect.

```latex
Recall = \frac{TP}{TP + FN}
```

Recall measures how many true Incorrect posture samples are detected.

```latex
F1 = \frac{2 \times Precision \times Recall}{Precision + Recall}
```

F1-score balances Precision and Recall for the Incorrect posture class.

The internal frame-level split of the ANN training dataset can be optimistic because neighboring frames from the same videos may share similar pose patterns. Therefore, the corrected external set, video-wise analysis, participant-wise evaluation, and runtime evaluation are more important for reporting project validity.

## 6. Results and Discussion

### 6.1 Rule-Based Baseline and ANN Classifier

Table 3 compares the rule-based baseline and the ANN/Keras classifier on the corrected external set. The ANN substantially improves accuracy and F1-score over the rule-based baseline. The rule-based method has high recall because broad thresholds detect many Incorrect samples, but it also produces more false alarms, which reduces precision and overall accuracy.

Table 3. Rule-based baseline and ANN classifier on the corrected external set.

| Method | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC |
|---|---:|---:|---:|---:|---:|
| Rule-based baseline | 67.49% | 63.49% | 92.81% | 75.40% | 37.56% |
| ANN/Keras classifier | 90.17% | 95.61% | 85.62% | 90.34% | 80.90% |

### 6.2 Classifier and Feature Comparison

The model registry compares multiple classifiers and feature groups. Table 4 shows the top five ranked models before final threshold calibration. The normalized landmark representation performed strongly, suggesting that body-scale normalization reduces person-size and camera-distance bias.

Table 4. Top-ranked classifier and feature combinations in the model registry.

| Rank | Model | Feature group | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | HistGradientBoosting | `normalized_99` | 95.96% | 95.07% | 97.53% | 96.28% | 91.89% |
| 2 | Random Forest | `normalized_99` | 95.90% | 94.67% | 97.87% | 96.24% | 91.79% |
| 3 | SVM RBF | `ergonomic_14` | 95.36% | 96.89% | 94.38% | 95.62% | 90.72% |
| 4 | SVM RBF | `normalized_99` | 94.51% | 92.82% | 97.30% | 95.01% | 89.04% |
| 5 | Random Forest | `combined_normalized_ergonomic` | 94.27% | 91.89% | 97.98% | 94.83% | 88.65% |

The `ergonomic_14` feature group achieved competitive performance with SVM RBF, although it used only 14 interpretable indicators. This is useful for explaining posture errors, while normalized landmarks remain stronger for the final selected model.

### 6.3 Final Selected Model on Corrected External Evaluation

After threshold calibration, the selected model is HistGradientBoosting with `normalized_99` features and threshold 0.65. Table 5 reports the final corrected external frame-level result.

Table 5. Final selected model performance on the corrected external set.

| Model | Feature group | Threshold | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC | FP | FN |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| HistGradientBoosting | `normalized_99` | 0.65 | 96.50% | 96.22% | 97.30% | 96.76% | 92.97% | 34 | 24 |

[Insert Fig. 4 here: Confusion matrix of the final selected model on the corrected external set]

Fig. 4. Confusion matrix of the final selected model on the corrected external set.

The confusion matrix contains 34 false positives and 24 false negatives. False positives mostly represent Correct frames classified as Incorrect posture. In a real application, this may cause unnecessary warnings. False negatives represent missed Incorrect posture frames and are more critical for health-related feedback. The calibrated threshold was selected to balance these errors while maintaining high Incorrect-class recall.

### 6.4 Participant-Wise Evaluation

Participant-wise evaluation on the raw dataset was performed using held-out participants. Table 6 reports the per-participant results. The mean F1-score for the Incorrect class is 90.67%, but performance varies across participants. P02 is the most difficult held-out participant in the current dataset.

Table 6. Leave-one-participant-out evaluation on the raw dataset.

| Held-out participant | Samples | Accuracy | Precision Incorrect | Recall Incorrect | F1 Incorrect | MCC |
|---|---:|---:|---:|---:|---:|---:|
| P01 | 3,524 | 90.81% | 98.28% | 84.88% | 91.09% | 82.64% |
| P02 | 1,225 | 79.35% | 77.87% | 91.55% | 84.16% | 56.55% |
| P03 | 2,208 | 93.03% | 99.85% | 90.05% | 94.70% | 85.55% |
| P04 | 1,815 | 86.67% | 79.37% | 100.00% | 88.50% | 75.92% |
| P05 | 2,250 | 93.56% | 95.63% | 94.24% | 94.93% | 86.11% |
| Mean | - | 88.68% | - | - | 90.67% | 77.35% |

This result supports preliminary generalization within the self-collected raw dataset. However, it does not replace a larger participant-independent external evaluation because the external corrected set currently contains only P01.

### 6.5 Runtime Evaluation

Table 7 reports runtime performance on representative front, side_30, and side_90 videos. The measured processing rate is approximately 28 FPS, which is close to real-time for a desktop demonstration. This benchmark measures processing latency only; full GUI FPS may be lower because of drawing, Tkinter scheduling, camera buffering, audio, and logging.

Table 7. Runtime benchmark on representative videos.

| View angle | Processed frames | Pose detection rate | Mean total latency | p95 latency | Estimated FPS |
|---|---:|---:|---:|---:|---:|
| front | 52 | 100.00% | 35.31 ms | 38.80 ms | 28.32 |
| side_30 | 120 | 100.00% | 35.67 ms | 43.08 ms | 28.03 |
| side_90 | 120 | 100.00% | 34.08 ms | 38.95 ms | 29.34 |

### 6.6 Discussion

The results show that learned classifiers are more effective than manually defined posture thresholds on the corrected external set. The rule-based baseline remains valuable because it is interpretable and can identify specific geometric issues such as shoulder tilt, torso lean, head offset, and neck compression. However, manually selected thresholds cannot easily adapt to camera position, body scale, and natural posture variation.

The ANN integrated into the current application provides a practical realtime classifier and outperforms the rule-based baseline. The broader experimental protocol shows that the selected HistGradientBoosting model with normalized landmarks performs better under the current corrected external evaluation. This distinction is important: the application currently uses ANN mode, while HistGradientBoosting is the best selected experimental model and should be integrated into the application before claiming product-level use of the selected model.

The very high internal ANN split result should be interpreted carefully because frame-level random splits can overestimate performance when adjacent frames are similar. The corrected external set, participant-wise evaluation, and video-wise error analysis provide more useful evidence for a scientific report. Literature values are not treated as a leaderboard because related studies use different sensors, datasets, labels, and validation protocols.

## 7. Desktop Application Implementation

The system is implemented as a Python desktop application. OpenCV is used to read webcam, IP camera, and MP4 video input. MediaPipe Pose estimates landmarks, and the application draws a skeleton overlay on the displayed frame. The user can select ANN mode or rule-based mode, configure warning duration, cooldown, smoothing window, and decision threshold.

[Insert Fig. 5 here: Desktop application interface]

Fig. 5. Desktop application interface with video preview, prediction status, controls, and statistics access.

The application displays the predicted posture status, confidence, incorrect posture duration, and warning count. If Incorrect posture persists beyond the configured warning duration, a `.wav` audio warning is played. The cooldown setting prevents the same posture episode from repeatedly triggering sound warnings.

SQLite is used for local logging. The database includes the tables `NguoiDung`, `CaiDat`, `PhienLamViec`, `NhatKyTuThe`, `ThongKeNgay`, and `ThongTinModel`. The current database contains 64 working sessions, 989 posture log entries, and 10 daily statistics entries. The dashboard summarizes session duration, posture status distribution, warning counts, and daily trends. The application also supports light and dark modes for usability.

[Insert Fig. 6 here: Statistics dashboard and SQLite logging flow]

Fig. 6. Statistics dashboard and SQLite logging flow used by the desktop application.

## 8. Limitations

The current dataset is still limited. The raw training set contains five participants, and the corrected external set currently contains only P01. Therefore, the reported results cannot be generalized to all users, workplaces, lighting conditions, camera positions, or body types.

The Correct posture and Incorrect posture labels are project-specific. They have not yet been validated by expert ergonomic annotation. The current system should therefore be treated as a posture warning prototype, not as a clinical or ergonomic assessment tool.

The desktop application currently uses ANN mode, while the experimental protocol selected HistGradientBoosting with normalized landmarks as the best model. The selected model should be integrated into the application before the deployed product behavior is described as using the final selected experimental model.

The project has not yet been evaluated on a public benchmark such as MultiPosture. Public datasets may help assess generalization, but label mapping and licensing must be checked before use. No state-of-the-art claim is made in this paper.

The runtime benchmark measures processing latency on representative videos. Full end-to-end GUI FPS may be lower because of rendering, Tkinter scheduling, camera buffering, sound playback, and database logging.

## 9. Conclusion and Future Work

This paper presented a webcam-based desktop system for working posture error detection using OpenCV, MediaPipe Pose landmarks, engineered posture features, lightweight machine learning classifiers, and real-time warning behavior. The study follows an existing-model-plus-new-dataset/features direction. MediaPipe Pose provides 33 body landmarks, and the proposed feature protocol compares raw landmarks, normalized landmarks, ergonomic geometric indicators, and combined feature groups.

The self-collected dataset contains 84 raw videos from five participants and 11,022 sampled frames. The corrected external set contains 10 videos and 1,658 samples. On the corrected external set, the current ANN/Keras application model achieved 90.17% accuracy and 90.34% F1 for the Incorrect posture class, outperforming the rule-based baseline under the same evaluation set. The best selected experimental model, HistGradientBoosting with normalized landmark features and threshold 0.65, achieved 96.50% accuracy, 96.76% F1 for the Incorrect class, and 92.97% MCC. Runtime evaluation showed approximately 28 FPS on representative front and side-view videos.

The results indicate that MediaPipe Pose landmarks and lightweight machine learning can support a practical desktop posture warning application. The rule-based baseline provides interpretability, while learned classifiers improve robustness over fixed thresholds. SQLite logging and dashboard statistics also make the system useful for reviewing posture behavior across sessions.

Future work should expand the dataset to include more participants, camera positions, lighting conditions, and working environments. Expert ergonomic annotation or RULA/REBA-inspired labeling should be added if the system is intended for stronger ergonomic interpretation. Public benchmark evaluation, such as MultiPosture, should be conducted after verifying license, feature format, and label mapping. The best selected experimental model should be integrated into the desktop application so that deployed behavior matches the research protocol. Finally, the binary label scheme should be extended to multi-class posture labels when sufficient data are available, such as forward head posture, shoulder imbalance, neck compression, torso leaning, and chin-resting behavior.

## References

Aziz, M. H., & Mahmood, H. A. (2023). Automated body postures assessment from still images using Mediapipe. *Journal of Optimization and Decision Making, 2*(2), 240-246. https://izlik.org/JA28RM33TT

Bagga, E., & Yang, A. (2024). *Real-time posture monitoring and risk assessment for manual lifting tasks using MediaPipe and LSTM*. arXiv. https://arxiv.org/abs/2408.12796

Bazarevsky, V., Grishchenko, I., Raveendran, K., Zhu, T., Zhang, F., & Grundmann, M. (2020). *BlazePose: On-device real-time body pose tracking*. arXiv. https://doi.org/10.48550/arXiv.2006.10204

Bourahmoune, K., Ishac, K., & Amagasa, T. (2022). Intelligent posture training: Machine-learning-powered human sitting posture recognition based on a pressure-sensing IoT cushion. *Sensors, 22*(14), 5337. https://doi.org/10.3390/s22145337

Cao, Z., Hidalgo, G., Simon, T., Wei, S.-E., & Sheikh, Y. (2018). *OpenPose: Realtime multi-person 2D pose estimation using part affinity fields*. arXiv. https://doi.org/10.48550/arXiv.1812.08008

Carneros-Prado, D., Cabanero-Gomez, L., Johnson, E., Gonzalez, I., Fontecha, J., & Hervas, R. (2024). A comparison between multilayer perceptrons and Kolmogorov-Arnold networks for multi-task classification in sitting posture recognition. *IEEE Access, 12*, 180198-180209. https://doi.org/10.1109/ACCESS.2024.3510034

Carneros Prado, D., Cabanero Gomez, L., Fontecha, J., Hervas, R., Gonzalez Diaz, I., & Johnson, E. (2024). *MultiPosture: A dataset of body joints keypoints extracted using MediaPipe for multi-task sitting posture recognition with upper and lower body labels* (Version v1) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.14230872

Chen, K. (2019). Sitting posture recognition based on OpenPose. *IOP Conference Series: Materials Science and Engineering, 677*(3), 032057. https://doi.org/10.1088/1757-899X/677/3/032057

Estrada, J. E., Vea, L. A., & Devaraj, M. (2023). Modelling proper and improper sitting posture of computer users using machine vision for a human-computer intelligent interactive system during COVID-19. *Applied Sciences, 13*(9), 5402. https://doi.org/10.3390/app13095402

Feradov, F., Markova, V., & Ganchev, T. (2022). Automated detection of improper sitting postures in computer users based on motion capture sensors. *Computers, 11*(7), 116. https://doi.org/10.3390/computers11070116

Google AI Edge. (2026). *Pose landmark detection guide*. MediaPipe Solutions. https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker

Jiang, X., Hu, Z., Wang, S., & Zhang, Y. (2023). A survey on artificial intelligence in posture recognition. *Computer Modeling in Engineering & Sciences, 137*(1), 35-82. https://doi.org/10.32604/cmes.2023.027676

Kim, J.-W., Choi, J.-Y., Ha, E. J., & Choi, J.-H. (2023). Human pose estimation using MediaPipe Pose and optimization method based on a humanoid model. *Applied Sciences, 13*(4), 2700. https://doi.org/10.3390/app13042700

Krauter, C., Angerbauer, K., Sousa Calepso, A., Achberger, A., Mayer, S., & Sedlmair, M. (2024). Sitting posture recognition and feedback: A literature review. In *Proceedings of the CHI Conference on Human Factors in Computing Systems*. Association for Computing Machinery. https://doi.org/10.1145/3613904.3642657

Kulikajevas, A., Maskeliunas, R., & Damasevicius, R. (2021). Detection of sitting posture using hierarchical image composition and deep learning. *PeerJ Computer Science, 7*, e442. https://doi.org/10.7717/peerj-cs.442

Lugaresi, C., Tang, J., Nash, H., McClanahan, C., Uboweja, E., Hays, M., Zhang, F., Chang, C.-L., Yong, M. G., Lee, J., Chang, W.-T., Hua, W., Georg, M., & Grundmann, M. (2019). *MediaPipe: A framework for building perception pipelines*. arXiv. https://arxiv.org/abs/1906.08172

Nadeem, M., Elbasi, E., Zreikat, A. I., & Sharsheer, M. (2024). Sitting posture recognition systems: Comprehensive literature review and analysis. *Applied Sciences, 14*(18), 8557. https://doi.org/10.3390/app14188557

Odesola, D. F., Kulon, J., Verghese, S., Partlow, A., & Gibson, C. (2024). Smart sensing chairs for sitting posture detection, classification, and monitoring: A comprehensive review. *Sensors, 24*(9), 2940. https://doi.org/10.3390/s24092940

Roggio, F., Trovato, B., Sortino, M., & Musumeci, G. (2024). A comprehensive analysis of the machine learning pose estimation models used in human movement and posture analyses: A narrative review. *Heliyon, 10*(21), e39977. https://doi.org/10.1016/j.heliyon.2024.e39977

Sahoo, K. K., Patel, T., Swain, D., Gerogiannis, V. C., Kanavos, A., Singh, D. P., Kumar, M., & Acharya, B. (2026). ALIGN: An AI-driven IoT framework for real-time sitting posture detection. *Algorithms, 19*(1), 48. https://doi.org/10.3390/a19010048

Tsai, M.-C., Chu, E. T.-H., & Lee, C.-R. (2023). An automated sitting posture recognition system utilizing pressure sensors. *Sensors, 23*(13), 5894. https://doi.org/10.3390/s23135894

Wang, S., Tavares, A., Lima, C., Gomes, T., Zhang, Y., Zhao, J., & Liang, Y. (2025). LAViTSPose: A lightweight cascaded framework for robust sitting posture recognition via detection-segmentation-classification. *Entropy, 27*(12), 1196. https://doi.org/10.3390/e27121196

Zeng, X., Sun, B., Wang, E., Luo, W., & Liu, T. (2017). A method of learner's sitting posture recognition based on depth image. In *Proceedings of the 2017 2nd International Conference on Control, Automation and Artificial Intelligence (CAAI 2017)* (pp. 558-563). Atlantis Press. https://doi.org/10.2991/caai-17.2017.125
