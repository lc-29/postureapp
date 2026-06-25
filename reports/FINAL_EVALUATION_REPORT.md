# Final Evaluation Report

Model: `random_forest__ergonomic_14`

Feature set: `ergonomic_14`

Threshold: `0.5000`

## External Frame-Level Result

| n | threshold | accuracy | accuracy_ci_low | accuracy_ci_high | precision_incorrect | recall_incorrect | f1_incorrect | macro_f1 | mcc | roc_auc | pr_auc | brier_score | false_positive | false_negative | protocol | model_id | feature_set | f1_ci_low | f1_ci_high |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4556 | 0.500000 | 0.821554 | 0.810166 | 0.832400 | 0.794655 | 0.919374 | 0.852477 | 0.813353 | 0.640480 | 0.822246 | 0.848708 | 0.185750 | 607 | 206 | corrected_external_frame_level | random_forest__ergonomic_14 | ergonomic_14 | 0.841696 | 0.861818 |

## Worst External Videos

| source_video | label | n | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | false_positive | false_negative |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dataset\external_videos\correct\P06_correct_side_90_002.mp4 | 0 | 160 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 160 | 0 |
| dataset\external_videos\correct\P06_correct_side_90_001.mp4 | 0 | 190 | 0.078947 | 0.000000 | 0.000000 | 0.000000 | 175 | 0 |
| dataset\external_videos\correct\P07_correct_side_90_003.mp4 | 0 | 230 | 0.339130 | 0.000000 | 0.000000 | 0.000000 | 152 | 0 |
| dataset\external_videos\correct\P06_correct_side_30_001.mp4 | 0 | 157 | 0.426752 | 0.000000 | 0.000000 | 0.000000 | 90 | 0 |
| dataset\external_videos\incorrect\P07_incorrect_side_30_002.mp4 | 1 | 238 | 0.584034 | 1.000000 | 0.584034 | 0.737401 | 0 | 99 |
| dataset\external_videos\incorrect\P07_incorrect_front_002.mp4 | 1 | 201 | 0.815920 | 1.000000 | 0.815920 | 0.898630 | 0 | 37 |
| dataset\external_videos\incorrect\P07_incorrect_side_90_002.mp4 | 1 | 246 | 0.886179 | 1.000000 | 0.886179 | 0.939655 | 0 | 28 |
| dataset\external_videos\correct\P06_correct_front_001.mp4 | 0 | 179 | 0.905028 | 0.000000 | 0.000000 | 0.000000 | 17 | 0 |
| dataset\external_videos\incorrect\P07_incorrect_front_003.mp4 | 1 | 206 | 0.946602 | 1.000000 | 0.946602 | 0.972569 | 0 | 11 |
| dataset\external_videos\incorrect\P07_incorrect_side_90_001.mp4 | 1 | 234 | 0.948718 | 1.000000 | 0.948718 | 0.973684 | 0 | 12 |

## Participant-Wise Raw Dataset Result

| index | accuracy | f1_incorrect | macro_f1 | mcc |
| --- | --- | --- | --- | --- |
| mean | 0.837476 | 0.871621 | 0.823641 | 0.673907 |
| std | 0.056196 | 0.043540 | 0.062374 | 0.088207 |

| held_out_participant | n | accuracy | precision_incorrect | recall_incorrect | f1_incorrect | mcc |
| --- | --- | --- | --- | --- | --- | --- |
| P01 | 5182 | 0.848900 | 0.833874 | 0.904611 | 0.867803 | 0.695299 |
| P02 | 1225 | 0.888163 | 0.859206 | 0.972752 | 0.912460 | 0.770566 |
| P03 | 2208 | 0.821558 | 0.888889 | 0.848168 | 0.868051 | 0.594550 |
| P04 | 1815 | 0.748760 | 0.671233 | 1.000000 | 0.803279 | 0.570075 |
| P05 | 2250 | 0.880000 | 0.904006 | 0.909028 | 0.906510 | 0.739042 |

## Claim Boundary

These results are suitable for the project final protocol. They still should not be described as state-of-the-art because the external set is project-specific and currently limited in participant diversity.
