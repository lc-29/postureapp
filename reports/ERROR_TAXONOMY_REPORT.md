# Error Taxonomy Report

Predictions: `D:\posture_detection_app\reports\results\final_external_predictions.csv`

Export directory: `D:\posture_detection_app\reports\figures\error_cases`

## Error Category Counts

| error_type | taxonomy_category | count |
| --- | --- | --- |
| false_negative | needs_manual_review | 195 |
| false_negative | startup_transition_frame | 11 |
| false_positive | needs_manual_review | 585 |
| false_positive | startup_transition_frame | 22 |

## Exported Representative Frames

| error_type | taxonomy_category | source_video | frame_index | timestamp_sec | label | pred_label | prob_incorrect | exported_frame |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| false_negative | needs_manual_review | dataset\external_videos\incorrect\P07_incorrect_side_30_002.mp4 | 238 | 7.944428 | 1 | 0 | 0.080000 | reports\figures\error_cases\false_negative\01_P07_incorrect_side_30_002_frame_238.jpg |
| false_negative | needs_manual_review | dataset\external_videos\incorrect\P07_incorrect_side_30_002.mp4 | 868 | 28.973795 | 1 | 0 | 0.088000 | reports\figures\error_cases\false_negative\02_P07_incorrect_side_30_002_frame_868.jpg |
| false_negative | needs_manual_review | dataset\external_videos\incorrect\P07_incorrect_side_30_002.mp4 | 826 | 27.571837 | 1 | 0 | 0.096000 | reports\figures\error_cases\false_negative\03_P07_incorrect_side_30_002_frame_826.jpg |
| false_negative | needs_manual_review | dataset\external_videos\incorrect\P07_incorrect_side_30_002.mp4 | 112 | 3.738554 | 1 | 0 | 0.112000 | reports\figures\error_cases\false_negative\04_P07_incorrect_side_30_002_frame_112.jpg |
| false_negative | needs_manual_review | dataset\external_videos\incorrect\P07_incorrect_side_30_002.mp4 | 854 | 28.506476 | 1 | 0 | 0.112000 | reports\figures\error_cases\false_negative\05_P07_incorrect_side_30_002_frame_854.jpg |
| false_negative | needs_manual_review | dataset\external_videos\incorrect\P07_incorrect_side_30_002.mp4 | 840 | 28.039156 | 1 | 0 | 0.120000 | reports\figures\error_cases\false_negative\06_P07_incorrect_side_30_002_frame_840.jpg |
| false_negative | needs_manual_review | dataset\external_videos\incorrect\P07_incorrect_side_30_002.mp4 | 630 | 21.029367 | 1 | 0 | 0.124000 | reports\figures\error_cases\false_negative\07_P07_incorrect_side_30_002_frame_630.jpg |
| false_negative | needs_manual_review | dataset\external_videos\incorrect\P07_incorrect_side_30_002.mp4 | 882 | 29.441114 | 1 | 0 | 0.128000 | reports\figures\error_cases\false_negative\08_P07_incorrect_side_30_002_frame_882.jpg |
| false_negative | needs_manual_review | dataset\external_videos\incorrect\P07_incorrect_side_30_002.mp4 | 126 | 4.205873 | 1 | 0 | 0.132000 | reports\figures\error_cases\false_negative\09_P07_incorrect_side_30_002_frame_126.jpg |
| false_negative | needs_manual_review | dataset\external_videos\incorrect\P07_incorrect_side_30_002.mp4 | 1400 | 46.731927 | 1 | 0 | 0.144000 | reports\figures\error_cases\false_negative\10_P07_incorrect_side_30_002_frame_1400.jpg |
| false_negative | needs_manual_review | dataset\external_videos\incorrect\P07_incorrect_side_30_002.mp4 | 1260 | 42.058734 | 1 | 0 | 0.148000 | reports\figures\error_cases\false_negative\11_P07_incorrect_side_30_002_frame_1260.jpg |
| false_negative | needs_manual_review | dataset\external_videos\incorrect\P07_incorrect_side_30_002.mp4 | 1246 | 41.591415 | 1 | 0 | 0.168000 | reports\figures\error_cases\false_negative\12_P07_incorrect_side_30_002_frame_1246.jpg |
| false_positive | needs_manual_review | dataset\external_videos\correct\P06_correct_side_90_001.mp4 | 2548 | 85.001783 | 0 | 1 | 0.964000 | reports\figures\error_cases\false_positive\01_P06_correct_side_90_001_frame_2548.jpg |
| false_positive | needs_manual_review | dataset\external_videos\correct\P06_correct_side_90_001.mp4 | 882 | 29.423694 | 0 | 1 | 0.964000 | reports\figures\error_cases\false_positive\02_P06_correct_side_90_001_frame_882.jpg |
| false_positive | needs_manual_review | dataset\external_videos\correct\P06_correct_side_90_001.mp4 | 868 | 28.956651 | 0 | 1 | 0.964000 | reports\figures\error_cases\false_positive\03_P06_correct_side_90_001_frame_868.jpg |
| false_positive | needs_manual_review | dataset\external_videos\correct\P06_correct_side_90_001.mp4 | 854 | 28.489609 | 0 | 1 | 0.964000 | reports\figures\error_cases\false_positive\04_P06_correct_side_90_001_frame_854.jpg |
| false_positive | needs_manual_review | dataset\external_videos\correct\P06_correct_side_90_001.mp4 | 896 | 29.890737 | 0 | 1 | 0.960000 | reports\figures\error_cases\false_positive\05_P06_correct_side_90_001_frame_896.jpg |
| false_positive | needs_manual_review | dataset\external_videos\correct\P06_correct_side_90_001.mp4 | 2576 | 85.935868 | 0 | 1 | 0.960000 | reports\figures\error_cases\false_positive\06_P06_correct_side_90_001_frame_2576.jpg |
| false_positive | needs_manual_review | dataset\external_videos\correct\P06_correct_side_90_001.mp4 | 2534 | 84.534740 | 0 | 1 | 0.960000 | reports\figures\error_cases\false_positive\07_P06_correct_side_90_001_frame_2534.jpg |
| false_positive | needs_manual_review | dataset\external_videos\correct\P06_correct_side_90_001.mp4 | 2282 | 76.127970 | 0 | 1 | 0.956000 | reports\figures\error_cases\false_positive\08_P06_correct_side_90_001_frame_2282.jpg |
| false_positive | needs_manual_review | dataset\external_videos\correct\P06_correct_side_90_001.mp4 | 2562 | 85.468826 | 0 | 1 | 0.956000 | reports\figures\error_cases\false_positive\09_P06_correct_side_90_001_frame_2562.jpg |
| false_positive | needs_manual_review | dataset\external_videos\correct\P06_correct_side_90_001.mp4 | 2240 | 74.726842 | 0 | 1 | 0.956000 | reports\figures\error_cases\false_positive\10_P06_correct_side_90_001_frame_2240.jpg |
| false_positive | needs_manual_review | dataset\external_videos\correct\P06_correct_side_90_001.mp4 | 2520 | 84.067697 | 0 | 1 | 0.956000 | reports\figures\error_cases\false_positive\11_P06_correct_side_90_001_frame_2520.jpg |
| false_positive | needs_manual_review | dataset\external_videos\correct\P06_correct_side_90_001.mp4 | 2506 | 83.600655 | 0 | 1 | 0.952000 | reports\figures\error_cases\false_positive\12_P06_correct_side_90_001_frame_2506.jpg |

## Manual Review Note

The taxonomy categories are first-pass labels inferred from source video and confidence. For a paper, representative exported frames should be manually reviewed before final claims.
