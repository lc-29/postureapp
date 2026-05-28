# Research Submission Readiness Checklist

Ngay cap nhat: 2026-05-28

| Hang muc | Trang thai | Ghi chu |
|---|---|---|
| Video renamed P01-P05 | Done | Da ap dung mapping P03->P02, P04->P03, P05->P04, P06->P05. |
| `video_manifest.csv` created | Done | `dataset/metadata/video_manifest.csv`, 94 video, SHA256 day du. |
| Raw metadata CSV extracted | Done | `dataset/processed/posture_data_2fps_with_metadata.csv`, 11022 rows, 108 columns. |
| External metadata CSV extracted | Done | `dataset/processed/posture_external_test_2fps_with_metadata.csv`, 1697 rows, 108 columns. |
| Ergonomic features generated | Done | Ergonomic va combined CSV da tao trong `dataset/processed/`. |
| Video-wise evaluation done | Done | `reports/results/video_wise_summary.md`. |
| Participant-wise evaluation done | Done | Raw va combined summaries da tao trong `reports/results/`. |
| Benchmark classifiers done | Done | `reports/BENCHMARK_CLASSIFIERS_SUMMARY.md`. |
| Ablation study done | Done | `reports/FEATURE_ABLATION_SUMMARY.md`. |
| Error analysis done | Done | `reports/ERROR_ANALYSIS_BY_VIDEO_PERSON_VIEW.md`. |
| Runtime benchmark done | Done | `reports/RUNTIME_BENCHMARK.md`, front/side_30/side_90. |
| Paper tables generated | Done | `reports/tables/`. |
| Paper figures generated | Done | `reports/figures/`. |
| Dataset statement written | Partial | `reports/DATASET_MANIFEST.md` da cap nhat; can bo sung consent/privacy neu nop that. |
| Limitations written | Partial | Da co trong cac report; can dua vao ban paper cuoi. |

## Ket luan san sang

Du an da co du nen tang thuc nghiem de viet ban thao nghien cuu theo huong:

> Metadata-rich webcam posture dataset, interpretable ergonomic features, classifier benchmark, participant-wise validation, and realtime desktop posture monitoring.

Can lam tiep truoc khi nop hoi thao:

1. Viet ro quy trinh thu thap va gan nhan du lieu.
2. Bo sung thong tin consent/rieng tu neu video co nguoi that.
3. Chon ket qua chinh de dua vao paper, tranh dua qua nhieu bang phu.
4. Kiem tra lai related work va citation tu PDF/full paper.
5. Viet limitations trung thuc: 5 participants, external set chi P01, dataset chua public raw video.
