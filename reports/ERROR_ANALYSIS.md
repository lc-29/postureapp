# Error Analysis

Dataset: external evaluation CSV

## Summary

Note: metrics in this file were regenerated after replacing
`dataset/external_videos/incorrect/P01_incorrect_004.mp4` with a true
incorrect-posture video on 2026-05-28. Earlier results for this file were based
on mislabeled content and should not be used.

| Item | Value |
|---|---:|
| Rows | 1658 |
| Correct predictions | 1495 |
| False positives | 35 |
| False negatives | 128 |
| Accuracy | 0.901689 |
| Precision incorrect | 0.956085 |
| Recall incorrect | 0.856180 |
| F1 incorrect | 0.903379 |
| MCC | 0.809012 |
| ROC-AUC | 0.982257 |
| PR-AUC | 0.985054 |
| Brier score | 0.078710 |

## Main finding

Tai threshold hien tai, loi can uu tien xu ly la false negative: model bo sot frame sai tu the. Neu app uu tien canh bao som, nen xem xet threshold thap hon va temporal smoothing de giam nhap nhay.

## Error by source video

```text
                                           source_video  correct  false_negative  false_positive
    dataset\external_videos\correct\P01_correct_001.mp4      118               0               0
    dataset\external_videos\correct\P01_correct_002.mp4      173               0               0
    dataset\external_videos\correct\P01_correct_003.mp4      140               0               3
    dataset\external_videos\correct\P01_correct_004.mp4       90               0              32
    dataset\external_videos\correct\P01_correct_005.mp4      212               0               0
dataset\external_videos\incorrect\P01_incorrect_001.mp4      142              13               0
dataset\external_videos\incorrect\P01_incorrect_002.mp4      162               1               0
dataset\external_videos\incorrect\P01_incorrect_003.mp4      193              16               0
dataset\external_videos\incorrect\P01_incorrect_004.mp4      155              45               0
dataset\external_videos\incorrect\P01_incorrect_005.mp4      110              53               0
```

## Lowest-probability false negatives

```text
                                           source_video  frame_index  timestamp_sec  sample_fps  video_fps participant_id view_angle    camera_type  row_index  y_true  y_pred  prob_incorrect  threshold     error_type
dataset\external_videos\incorrect\P01_incorrect_004.mp4         2492      83.214863         2.0  29.946573            P01    unknown external_video       1473       1       0        0.000038        0.5 false_negative
dataset\external_videos\incorrect\P01_incorrect_004.mp4         2408      80.409867         2.0  29.946573            P01    unknown external_video       1467       1       0        0.000040        0.5 false_negative
dataset\external_videos\incorrect\P01_incorrect_004.mp4         2506      83.682362         2.0  29.946573            P01    unknown external_video       1474       1       0        0.000129        0.5 false_negative
dataset\external_videos\incorrect\P01_incorrect_004.mp4          490      16.362473         2.0  29.946573            P01    unknown external_video       1330       1       0        0.000131        0.5 false_negative
dataset\external_videos\incorrect\P01_incorrect_004.mp4         2478      82.747363         2.0  29.946573            P01    unknown external_video       1472       1       0        0.000160        0.5 false_negative
dataset\external_videos\incorrect\P01_incorrect_004.mp4         2394      79.942368         2.0  29.946573            P01    unknown external_video       1466       1       0        0.000221        0.5 false_negative
dataset\external_videos\incorrect\P01_incorrect_004.mp4          518      17.297471         2.0  29.946573            P01    unknown external_video       1332       1       0        0.000233        0.5 false_negative
dataset\external_videos\incorrect\P01_incorrect_004.mp4          504      16.829972         2.0  29.946573            P01    unknown external_video       1331       1       0        0.000241        0.5 false_negative
dataset\external_videos\incorrect\P01_incorrect_004.mp4         2464      82.279864         2.0  29.946573            P01    unknown external_video       1471       1       0        0.000277        0.5 false_negative
dataset\external_videos\incorrect\P01_incorrect_004.mp4          476      15.894974         2.0  29.946573            P01    unknown external_video       1329       1       0        0.000361        0.5 false_negative
```

## Highest-probability false positives

```text
                                       source_video  frame_index  timestamp_sec  sample_fps  video_fps participant_id view_angle    camera_type  row_index  y_true  y_pred  prob_incorrect  threshold     error_type
dataset\external_videos\correct\P01_correct_003.mp4           14       0.467228         2.0  29.963945            P01    unknown external_video        292       0       1        0.998955        0.5 false_positive
dataset\external_videos\correct\P01_correct_004.mp4          672      22.449463         2.0  29.933901            P01    unknown external_video        482       0       1        0.979107        0.5 false_positive
dataset\external_videos\correct\P01_correct_004.mp4          980      32.738800         2.0  29.933901            P01    unknown external_video        504       0       1        0.933046        0.5 false_positive
dataset\external_videos\correct\P01_correct_004.mp4          910      30.400314         2.0  29.933901            P01    unknown external_video        499       0       1        0.919525        0.5 false_positive
dataset\external_videos\correct\P01_correct_004.mp4          714      23.852554         2.0  29.933901            P01    unknown external_video        485       0       1        0.910122        0.5 false_positive
dataset\external_videos\correct\P01_correct_004.mp4          700      23.384857         2.0  29.933901            P01    unknown external_video        484       0       1        0.902682        0.5 false_positive
dataset\external_videos\correct\P01_correct_004.mp4          126       4.209274         2.0  29.933901            P01    unknown external_video        443       0       1        0.895773        0.5 false_positive
dataset\external_videos\correct\P01_correct_004.mp4          294       9.821640         2.0  29.933901            P01    unknown external_video        455       0       1        0.864080        0.5 false_positive
dataset\external_videos\correct\P01_correct_004.mp4          952      31.803406         2.0  29.933901            P01    unknown external_video        502       0       1        0.849809        0.5 false_positive
dataset\external_videos\correct\P01_correct_004.mp4          938      31.335709         2.0  29.933901            P01    unknown external_video        501       0       1        0.848429        0.5 false_positive
```

## Recommended fixes

1. Re-extract CSV co metadata video/person de phan tich loi theo nguon.
2. Them normalized body-scale features va ergonomic angle features.
3. Chon threshold theo muc tieu recall/precision cua app.
4. Them temporal smoothing truoc khi ghi log/canh bao.
