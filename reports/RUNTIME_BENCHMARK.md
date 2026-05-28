# Runtime Benchmark

Benchmark on three representative raw videos: front, side_30, and side_90. Resolution 640x360, MediaPipe complexity 1, max 120 sampled frames per video.

| view_angle | processed_frames | pose_detection_rate | mean_total_latency_ms | p50_total_latency_ms | p95_total_latency_ms | mean_estimated_fps | mean_mediapipe_latency_ms | mean_ann_latency_ms |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| front | 52 | 1.000 | 35.315 | 31.654 | 38.805 | 28.317 | 24.713 | 8.712 |
| side_30 | 120 | 1.000 | 35.671 | 33.465 | 43.081 | 28.034 | 25.184 | 8.496 |
| side_90 | 120 | 1.000 | 34.085 | 32.112 | 38.948 | 29.339 | 23.981 | 8.247 |

Detailed frame-level CSV: `reports/results/runtime_benchmark.csv`

Summary CSV: `reports/results/runtime_benchmark_summary.csv`

Interpretation: this measures processing latency only; full GUI FPS can be lower because of drawing, Tkinter scheduling, camera buffering, audio, and logging.
