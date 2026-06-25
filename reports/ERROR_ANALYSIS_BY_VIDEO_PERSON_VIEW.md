# Error Analysis By Video, Participant, And View

Dataset: `D:\posture_detection_app\dataset\processed\posture_external_test_2fps_with_metadata.csv`

Threshold: `0.5000`

Predictions CSV: `D:\posture_detection_app\reports\results\predictions_external.csv`

Error cases CSV: `D:\posture_detection_app\reports\results\error_cases.csv`

## Error Counts

| error_type | count |
| --- | --- |
| correct | 1495 |
| false_negative | 128 |
| false_positive | 35 |

## Worst Videos

| source_video | label | rows | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | false_positive | false_negative | mean_prob_incorrect |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dataset\external_videos\incorrect\P01_incorrect_005.mp4 | 1 | 163 | 0.674847 | 1.000000 | 0.674847 | 0.805861 | 0 | 53 | 0.682813 |
| dataset\external_videos\incorrect\P01_incorrect_004.mp4 | 1 | 200 | 0.775000 | 1.000000 | 0.775000 | 0.873239 | 0 | 45 | 0.769268 |
| dataset\external_videos\incorrect\P01_incorrect_003.mp4 | 1 | 209 | 0.923445 | 1.000000 | 0.923445 | 0.960199 | 0 | 16 | 0.914527 |
| dataset\external_videos\incorrect\P01_incorrect_001.mp4 | 1 | 155 | 0.916129 | 1.000000 | 0.916129 | 0.956229 | 0 | 13 | 0.916541 |
| dataset\external_videos\incorrect\P01_incorrect_002.mp4 | 1 | 163 | 0.993865 | 1.000000 | 0.993865 | 0.996923 | 0 | 1 | 0.994106 |
| dataset\external_videos\correct\P01_correct_004.mp4 | 0 | 122 | 0.737705 | 0.000000 | 0.000000 | 0.000000 | 32 | 0 | 0.274100 |
| dataset\external_videos\correct\P01_correct_003.mp4 | 0 | 143 | 0.979021 | 0.000000 | 0.000000 | 0.000000 | 3 | 0 | 0.018495 |
| dataset\external_videos\correct\P01_correct_005.mp4 | 0 | 212 | 1.000000 | 0.000000 | 0.000000 | 0.000000 | 0 | 0 | 0.000162 |
| dataset\external_videos\correct\P01_correct_002.mp4 | 0 | 173 | 1.000000 | 0.000000 | 0.000000 | 0.000000 | 0 | 0 | 0.000027 |
| dataset\external_videos\correct\P01_correct_001.mp4 | 0 | 118 | 1.000000 | 0.000000 | 0.000000 | 0.000000 | 0 | 0 | 0.000015 |

## By Participant

| participant_id | rows | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | false_positive | false_negative | mean_prob_incorrect |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P01 | 1658 | 0.901689 | 0.956085 | 0.856180 | 0.903379 | 35 | 128 | 0.480408 |

## By View Angle

| view_angle | rows | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | false_positive | false_negative | mean_prob_incorrect |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| unknown | 1658 | 0.901689 | 0.956085 | 0.856180 | 0.903379 | 35 | 128 | 0.480408 |

## Interpretation Notes

- High false negative count means incorrect posture was missed.
- High false positive count means correct posture was flagged as incorrect.
- Use the worst-video table to inspect lighting, camera angle, occlusion, and intermediate posture cases.
