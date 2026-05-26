"""Check whether a CSV is ready for video-wise evaluation."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = BASE_DIR / "dataset" / "posture_data_2fps.csv"
DEFAULT_OUTPUT = BASE_DIR / "reports" / "results" / "video_wise_protocol.md"
REQUIRED_COLUMNS = {"source_video", "frame_index", "label"}


def check_dataset(args: argparse.Namespace) -> None:
    dataset_path = Path(args.dataset)
    output_path = Path(args.output)
    if not dataset_path.is_absolute():
        dataset_path = BASE_DIR / dataset_path
    if not output_path.is_absolute():
        output_path = BASE_DIR / output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not dataset_path.exists():
        raise FileNotFoundError(f"CSV not found: {dataset_path}")

    df = pd.read_csv(dataset_path, nrows=20)
    missing = sorted(REQUIRED_COLUMNS.difference(df.columns))

    if missing:
        text = f"""# Video-wise Evaluation Protocol

Status: not runnable yet.

CSV checked: `{dataset_path}`

Missing required columns: `{', '.join(missing)}`

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
"""
        output_path.write_text(text, encoding="utf-8")
        print(text)
        return

    full_df = pd.read_csv(dataset_path)
    summary = full_df.groupby(["source_video", "label"]).size().reset_index(name="rows")
    summary_path = output_path.with_name("video_wise_source_summary.csv")
    summary.to_csv(summary_path, index=False)

    text = f"""# Video-wise Evaluation Protocol

Status: metadata is present.

CSV checked: `{dataset_path}`

Rows: {len(full_df)}
Unique source videos: {full_df['source_video'].nunique()}

Next implementation step: split by `source_video`, train on train videos only,
and evaluate on held-out videos. Source summary saved to `{summary_path}`.
"""
    output_path.write_text(text, encoding="utf-8")
    print(text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate metadata for video-wise evaluation.")
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    return parser.parse_args()


if __name__ == "__main__":
    check_dataset(parse_args())
