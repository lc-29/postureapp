# Video-wise Evaluation Protocol

Status: metadata is present and current ANN was evaluated per source video.

CSV checked: `D:\posture_detection_app\dataset\processed\posture_external_test_2fps_with_metadata.csv`
Model: `D:\posture_detection_app\models\ann_best.keras`
Scaler: `D:\posture_detection_app\models\scaler.pkl`
Threshold: `0.5000`

Rows: 1697
Unique source videos: 10

## Video-wise summary

| Metric | Value |
|---|---:|
| Mean video accuracy | 0.824817 |
| Std video accuracy | 0.287630 |
| Mean video F1 incorrect | 0.377173 |

Per-video metrics saved to `D:\posture_detection_app\reports\results\video_wise_metrics.csv`.
Source summary saved to `D:\posture_detection_app\reports\results\video_wise_source_summary.csv`.

## Worst videos by accuracy

```text
                                           source_video  rows  label  accuracy  accuracy_ci_low  accuracy_ci_high  precision   recall       f1  mean_prob_incorrect  false_positive  false_negative
dataset\external_videos\incorrect\P01_incorrect_004.mp4   239      1  0.029289         0.014258          0.059211        1.0 0.029289 0.056911             0.043355               0             232
dataset\external_videos\incorrect\P01_incorrect_005.mp4   163      1  0.668712         0.593302          0.736352        1.0 0.668712 0.801471             0.670552               0              54
    dataset\external_videos\correct\P01_correct_004.mp4   122      0  0.737705         0.653252          0.807646        0.0 0.000000 0.000000             0.274100              32               0
dataset\external_videos\incorrect\P01_incorrect_001.mp4   155      1  0.916129         0.861799          0.950332        1.0 0.916129 0.956229             0.916541               0              13
dataset\external_videos\incorrect\P01_incorrect_003.mp4   209      1  0.923445         0.879274          0.952331        1.0 0.923445 0.960199             0.914527               0              16
```

## Limitation

Day la evaluation per-video cua model da train san tren external metadata CSV.
De co video-wise validation manh hon, can train/evaluate bang split giu lai
video/participant chua tung xuat hien trong train set.
