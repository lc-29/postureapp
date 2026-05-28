# Dataset Manifest

Ngay cap nhat: 2026-05-28

## Tong quan

| Hang muc | Gia tri |
|---|---:|
| Raw videos - correct | 34 |
| Raw videos - incorrect | 50 |
| Raw videos total | 84 |
| External videos - correct | 5 |
| External videos - incorrect | 5 |
| External videos total | 10 |
| All videos total | 94 |
| Raw participants | 5 (`P01`-`P05`) |
| Raw view angles | `front`, `side_30`, `side_90` |
| Total video duration | 6009.429 seconds |
| Total video size | 33179.269 MB |

## Video manifest

Manifest chuan da duoc tao tai:

```text
dataset/metadata/video_manifest.csv
```

Report tom tat:

```text
reports/DATASET_VIDEO_MANIFEST_SUMMARY.md
```

Manifest co cac cot:

```text
dataset_split, source_video, file_name, label, label_name, participant_id,
view_angle, camera_type, duration_sec, fps, width, height, total_frames,
file_size_mb, sha256, notes
```

## CSV da trich xuat

| Dataset | File | Rows | Columns |
|---|---|---:|---:|
| Raw metadata | `dataset/processed/posture_data_2fps_with_metadata.csv` | 11022 | 108 |
| External metadata | `dataset/processed/posture_external_test_2fps_with_metadata.csv` | 1697 | 108 |
| Raw ergonomic | `dataset/processed/posture_data_2fps_ergonomic_features.csv` | 11022 | 23 |
| External ergonomic | `dataset/processed/posture_external_test_2fps_ergonomic_features.csv` | 1697 | 23 |
| Raw combined | `dataset/processed/posture_data_2fps_combined_features.csv` | 11022 | 122 |
| External combined | `dataset/processed/posture_external_test_2fps_combined_features.csv` | 1697 | 122 |

## Label distribution

| Dataset | Correct (`0`) | Incorrect (`1`) |
|---|---:|---:|
| Raw metadata CSV | 4438 | 6584 |
| External metadata CSV | 768 | 929 |

## Raw participants

| Participant | Video count |
|---|---:|
| P01 | 19 |
| P02 | 11 |
| P03 | 18 |
| P04 | 16 |
| P05 | 20 |

Ghi chu: du lieu da duoc rename sau khi xoa participant cu `P02`. Mapping da ap dung:

| Ma cu | Ma moi |
|---|---|
| P01 | P01 |
| P03 | P02 |
| P04 | P03 |
| P05 | P04 |
| P06 | P05 |

Report doi ten:

```text
reports/dataset_rename_plan.csv
```

## Feature schema

### Raw feature set

Moi frame gom 33 MediaPipe Pose landmarks. Moi landmark co 3 toa do:

- `landmark_N_x`
- `landmark_N_y`
- `landmark_N_z`

Tong: 99 raw landmark features.

### Metadata columns

CSV metadata co them:

- `source_video`
- `frame_index`
- `timestamp_sec`
- `sample_fps`
- `video_fps`
- `participant_id`
- `view_angle`
- `camera_type`
- `label`

### Ergonomic feature set

Mo ta chi tiet tai:

```text
reports/ERGONOMIC_FEATURES_DESCRIPTION.md
```

Nhom dac trung ergonomic gom shoulder, torso, head/neck va hand/chin-rest indicators. Visibility khong duoc dung vi CSV 99 feature hien tai khong luu MediaPipe visibility that.

## Kiem chung da co

| Hang muc | File ket qua |
|---|---|
| Video-wise evaluation | `reports/results/video_wise_summary.md` |
| Participant-wise raw | `reports/results/participant_wise_summary_raw.md` |
| Participant-wise combined | `reports/results/participant_wise_summary_combined.md` |
| Classifier benchmark external | `reports/BENCHMARK_CLASSIFIERS_SUMMARY.md` |
| Feature ablation | `reports/FEATURE_ABLATION_SUMMARY.md` |
| Error analysis | `reports/ERROR_ANALYSIS_BY_VIDEO_PERSON_VIEW.md` |
| Runtime benchmark | `reports/RUNTIME_BENCHMARK.md` |

## Rui ro du lieu

- External videos hien tai chi co `P01`, nen external test kiem tra video moi nhung chua kiem tra nguoi moi.
- Raw participant-wise evaluation da duoc bo sung de danh gia theo nguoi, nhung dataset van chi co 5 nguoi nen can trinh bay la preliminary.
- Raw videos khong nam trong Git do dung luong va rieng tu; metadata va SHA256 duoc luu de kiem chung local.
- Neu nop hoi thao, nen mo ta ro quy trinh thu thap, tieu chi gan nhan, thiet bi quay va consent/rieng tu.
