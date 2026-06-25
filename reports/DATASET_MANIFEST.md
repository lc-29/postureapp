# Dataset Manifest

Updated: 2026-06-25 03:42:10

## Current Protocol

Cac video external P01 cu da duoc chuyen vao raw/development set. External set final moi gom P06-P07 de danh gia unseen participants.

| Split | Videos | Correct Videos | Incorrect Videos | Participants | Purpose |
|---|---:|---:|---:|---|---|
| Raw/development | 94 | 39 | 55 | P01-P05 | Train/development |
| External unseen-participant | 23 | 11 | 12 | P06-P07 | Final external test |

## Manifest Shape

- File: `dataset/metadata/video_manifest.csv`
- Shape: `117 x 16`
- All source videos exist on disk: yes

## Raw Participants

| participant_id | label_name | count |
| --- | --- | --- |
| P01 | correct | 14 |
| P01 | incorrect | 15 |
| P02 | correct | 4 |
| P02 | incorrect | 7 |
| P03 | correct | 6 |
| P03 | incorrect | 12 |
| P04 | correct | 7 |
| P04 | incorrect | 9 |
| P05 | correct | 8 |
| P05 | incorrect | 12 |

## External Participants

| participant_id | label_name | count |
| --- | --- | --- |
| P06 | correct | 5 |
| P06 | incorrect | 5 |
| P07 | correct | 6 |
| P07 | incorrect | 7 |

## Raw View Angles

| view_angle | label_name | count |
| --- | --- | --- |
| front | correct | 9 |
| front | incorrect | 15 |
| side_30 | correct | 8 |
| side_30 | incorrect | 9 |
| side_90 | correct | 17 |
| side_90 | incorrect | 26 |
| unknown | correct | 5 |
| unknown | incorrect | 5 |

## External View Angles

| view_angle | label_name | count |
| --- | --- | --- |
| front | correct | 3 |
| front | incorrect | 4 |
| side_30 | correct | 3 |
| side_30 | incorrect | 4 |
| side_90 | correct | 5 |
| side_90 | incorrect | 4 |

## Processed CSVs

| File | Shape | Label Distribution | Participants |
|---|---:|---|---|
| `dataset/processed/posture_data_2fps_with_metadata.csv` | 12680 x 108 | {0: 5206, 1: 7474} | P01, P02, P03, P04, P05 |
| `dataset/processed/posture_external_test_2fps_with_metadata.csv` | 4556 x 108 | {0: 2001, 1: 2555} | P06, P07 |

## Notes

- Label `0` means Correct posture; label `1` means Incorrect posture.
- External set hien chi gom P06-P07 va duoc dung de danh gia nguoi moi.
- Raw co mot so video P01 legacy khong co view trong ten file, nen `view_angle=unknown` cho phan do.
- Dataset labels are project-specific and should not be described as expert ergonomic annotation unless additional annotation evidence is added.
