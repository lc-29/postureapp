# Error Analysis

Dataset: external evaluation CSV

## Summary

| Item | Value |
|---|---:|
| Rows | 1697 |
| Correct predictions | 1346 |
| False positives | 35 |
| False negatives | 316 |
| Accuracy | 0.793164 |
| Precision incorrect | 0.945988 |
| Recall incorrect | 0.659849 |
| F1 incorrect | 0.777425 |
| MCC | 0.629328 |
| ROC-AUC | 0.950458 |
| PR-AUC | 0.957466 |
| Brier score | 0.186415 |

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
dataset\external_videos\incorrect\P01_incorrect_004.mp4        7             232               0
dataset\external_videos\incorrect\P01_incorrect_005.mp4      109              54               0
```

## Lowest-probability false negatives

```text
                                           source_video  frame_index  timestamp_sec  sample_fps  video_fps participant_id  view_angle    camera_type  row_index  y_true  y_pred  prob_incorrect  threshold     error_type
dataset\external_videos\incorrect\P01_incorrect_004.mp4         1050      35.036207         2.0  29.968997            P01         NaN external_video       1370       1       0        0.000035        0.5 false_negative
dataset\external_videos\incorrect\P01_incorrect_004.mp4          574      19.153127         2.0  29.968997            P01         NaN external_video       1336       1       0        0.000039        0.5 false_negative
dataset\external_videos\incorrect\P01_incorrect_004.mp4          532      17.751678         2.0  29.968997            P01         NaN external_video       1333       1       0        0.000042        0.5 false_negative
dataset\external_videos\incorrect\P01_incorrect_004.mp4          546      18.218828         2.0  29.968997            P01         NaN external_video       1334       1       0        0.000043        0.5 false_negative
dataset\external_videos\incorrect\P01_incorrect_004.mp4          476      15.883081         2.0  29.968997            P01         NaN external_video       1329       1       0        0.000043        0.5 false_negative
dataset\external_videos\incorrect\P01_incorrect_004.mp4          560      18.685977         2.0  29.968997            P01         NaN external_video       1335       1       0        0.000044        0.5 false_negative
dataset\external_videos\incorrect\P01_incorrect_004.mp4         3332     111.181564         2.0  29.968997            P01         NaN external_video       1533       1       0        0.000044        0.5 false_negative
dataset\external_videos\incorrect\P01_incorrect_004.mp4          518      17.284529         2.0  29.968997            P01         NaN external_video       1332       1       0        0.000048        0.5 false_negative
dataset\external_videos\incorrect\P01_incorrect_004.mp4          448      14.948782         2.0  29.968997            P01         NaN external_video       1327       1       0        0.000050        0.5 false_negative
dataset\external_videos\incorrect\P01_incorrect_004.mp4         3318     110.714415         2.0  29.968997            P01         NaN external_video       1532       1       0        0.000050        0.5 false_negative
```

## Highest-probability false positives

```text
                                       source_video  frame_index  timestamp_sec  sample_fps  video_fps participant_id  view_angle    camera_type  row_index  y_true  y_pred  prob_incorrect  threshold     error_type
dataset\external_videos\correct\P01_correct_003.mp4           14       0.467228         2.0  29.963945            P01         NaN external_video        292       0       1        0.998955        0.5 false_positive
dataset\external_videos\correct\P01_correct_004.mp4          672      22.449463         2.0  29.933901            P01         NaN external_video        482       0       1        0.979107        0.5 false_positive
dataset\external_videos\correct\P01_correct_004.mp4          980      32.738800         2.0  29.933901            P01         NaN external_video        504       0       1        0.933046        0.5 false_positive
dataset\external_videos\correct\P01_correct_004.mp4          910      30.400314         2.0  29.933901            P01         NaN external_video        499       0       1        0.919525        0.5 false_positive
dataset\external_videos\correct\P01_correct_004.mp4          714      23.852554         2.0  29.933901            P01         NaN external_video        485       0       1        0.910122        0.5 false_positive
dataset\external_videos\correct\P01_correct_004.mp4          700      23.384857         2.0  29.933901            P01         NaN external_video        484       0       1        0.902682        0.5 false_positive
dataset\external_videos\correct\P01_correct_004.mp4          126       4.209274         2.0  29.933901            P01         NaN external_video        443       0       1        0.895773        0.5 false_positive
dataset\external_videos\correct\P01_correct_004.mp4          294       9.821640         2.0  29.933901            P01         NaN external_video        455       0       1        0.864080        0.5 false_positive
dataset\external_videos\correct\P01_correct_004.mp4          952      31.803406         2.0  29.933901            P01         NaN external_video        502       0       1        0.849809        0.5 false_positive
dataset\external_videos\correct\P01_correct_004.mp4          938      31.335709         2.0  29.933901            P01         NaN external_video        501       0       1        0.848429        0.5 false_positive
```

## Recommended fixes

1. Re-extract CSV co metadata video/person de phan tich loi theo nguon.
2. Them normalized body-scale features va ergonomic angle features.
3. Chon threshold theo muc tieu recall/precision cua app.
4. Them temporal smoothing truoc khi ghi log/canh bao.
