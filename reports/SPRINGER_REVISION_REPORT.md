# Springer Manuscript Revision Report

## Revised Files

- `reports/SPRINGER_MANUSCRIPT_REVISED.md`
- `reports/SPRINGER_MANUSCRIPT_REVISED_VN.md`
- `reports/FIGURE_EXPORT_TODO.md`

The original files were not deleted. Source code files were not modified.

## Main Revisions Completed

1. Abstract was rewritten to stay under 250 words and to follow a scientific paper style: problem, method, dataset, evidence, and contribution.
2. Introduction was shortened and focused on the practical problem, prior limitations, research gap, and three specific contributions.
3. Related Work was reorganized into three groups:
   - sensor-based and depth-camera-based sitting posture recognition;
   - vision-based posture recognition using RGB cameras;
   - pose-landmark-based posture analysis using OpenPose and MediaPipe.
4. Related Work now closes with a clear research gap instead of only listing previous studies.
5. Proposed Method was rewritten around consistent module names:
   - OpenCV Frame Capture Module;
   - Landmark Extraction Module;
   - Feature Construction Module;
   - Posture Classification Module;
   - Temporal Smoothing Module;
   - Warning and Logging Module;
   - Dashboard Statistics Module.
6. Algorithm 1 was added as text pseudocode for real-time working posture error detection.
7. Dataset description was changed from file-oriented reporting to split-oriented reporting:
   - development/training set;
   - corrected external set;
   - full video manifest.
8. Feature groups were clarified as `raw_99`, `normalized_99`, `ergonomic_14`, and combined groups.
9. Experimental Setup now states Python version, main library versions, model families, threshold calibration, model selection criterion, and metric formulas.
10. Results were rewritten with concrete values instead of broad claims.
11. The manuscript clearly distinguishes:
   - ANN/Keras as the current application model;
   - HistGradientBoosting as the selected experimental model.
12. Desktop Application Implementation was shortened so it supports scientific reproducibility instead of reading like a product/demo report.
13. Limitations were made explicit and concise:
   - five participants;
   - corrected external set only P01;
   - project-specific labels;
   - no expert ergonomic annotation;
   - no public benchmark evaluation yet;
   - app currently uses ANN, while HGB is the selected experimental model;
   - full GUI FPS has not yet been measured.
14. Conclusion was revised to avoid citations, avoid new information, and state future work directly.
15. References were kept in an author-year style and focused on peer-reviewed papers, datasets, arXiv technical papers, and official documentation where appropriate.
16. A Vietnamese counterpart was updated in `reports/SPRINGER_MANUSCRIPT_REVISED_VN.md` for easier comparison.

## Checks Against the Publication Guide

- The manuscript now states old work, current gap, proposed work, evidence, limitations, and future work.
- Abstract contains only important information and avoids citation.
- Keywords cover object, field, technology, novelty, and data.
- Introduction avoids excessive technical detail.
- Related Work discusses gaps instead of only listing papers.
- Proposed Method contains text, schema, formulas, and pseudocode.
- Experimental Setup describes data, models, metrics, threshold, and protocol.
- Evaluation uses local comparisons and avoids cross-paper leaderboard claims.
- Dataset section states source, sampling, labels, metadata, and limitations.
- Each table and figure has a caption and explanatory paragraph.
- Implementation is used as evidence of feasibility, not as advertising.

## Remaining Figure Tasks

See `reports/FIGURE_EXPORT_TODO.md`.

Important missing or not-yet-exported figures:

1. `reports/figures/system_architecture.png`
2. `reports/figures/mediapipe_landmark_sample.png`
3. `reports/figures/feature_construction_pipeline.png`
4. `reports/figures/desktop_gui_screenshot.png`
5. `reports/figures/sqlite_logging_flow.png`

Existing usable figures:

1. `reports/figures/external_confusion_matrix.png`
2. `reports/figures/external_threshold_sweep.png`
3. `reports/figures/temporal_smoothing_effect.png`
4. `reports/figures/feature_importance_top20.png`
5. `reports/figures/tpri_distribution.png`

## Academic Risks Still Present

1. Dataset size is still small for a strong international submission.
2. The corrected external set contains only one participant, P01.
3. Labels are project-specific and have not been validated by ergonomic experts.
4. The best experimental model is not yet integrated into the desktop app.
5. A public benchmark such as MultiPosture has not yet been evaluated.
6. Full GUI FPS has not been measured.
7. The manuscript currently uses author-year references. If the final Springer venue requires LNCS numeric citations, references must be converted to that template.

## Recommended Next Fixes

1. Export the missing figures listed in `FIGURE_EXPORT_TODO.md`.
2. Integrate the selected HistGradientBoosting model into the app or explicitly keep the app result limited to ANN/Keras.
3. Add expert or rubric-based annotation if possible, even on a subset of videos.
4. Evaluate one public dataset after checking license and label mapping.
5. Measure full GUI FPS with webcam, display refresh, smoothing, warning, and SQLite logging enabled.
6. Convert the manuscript into the exact Springer template required by the selected conference or journal.
