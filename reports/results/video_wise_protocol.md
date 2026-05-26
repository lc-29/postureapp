# Video-wise Evaluation Protocol

Status: not runnable yet.

CSV checked: `D:\posture_detection_app\dataset\posture_data_2fps.csv`

Missing required columns: `frame_index, source_video`

To run video-wise or person-wise evaluation, re-extract features with metadata:

```powershell
python src/2_extract_features.py --include-metadata --output dataset/posture_data_2fps_with_metadata.csv
```

Required metadata:

- `source_video`: source file for each sampled frame.
- `frame_index`: frame index inside the source video.
- `label`: class label.

Do not infer source video from the current frame-only CSV; that would make the
split unverifiable.
