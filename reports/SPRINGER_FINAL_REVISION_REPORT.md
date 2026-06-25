# Springer Final Revision Report

## Output Files

Created or updated:

- `reports/SPRINGER_MANUSCRIPT_FINAL_DRAFT.md`
- `reports/SPRINGER_FINAL_REVISION_REPORT.md`
- `reports/FIGURE_EXPORT_TODO.md`

Existing files were not deleted. Source code files were not modified.

## What Was Revised in the Final Draft

1. Title was refined to emphasize the main technical novelty more clearly:
   - webcam-based working posture error detection;
   - normalized MediaPipe landmarks;
   - lightweight machine learning.
2. Abstract was shortened and reorganized around the publication-guide pattern:
   - why the problem matters;
   - how the system works;
   - what dataset and results support the contribution.
3. Keywords were adjusted to better represent:
   - research subject;
   - field;
   - technology;
   - novelty;
   - data.
4. Introduction now includes a short workplace/posture-feedback context using review papers already present in the references.
5. Related Work keeps the three required groups and closes with a short research-gap paragraph.
6. Proposed Method now opens with a clearer proposition: the system contribution is the combination of normalized landmarks, ergonomic features, local classifier comparison, temporal smoothing, and session logging.
7. Proposed Method now ends the algorithm section with a reproducibility-oriented statement instead of only describing software behavior.
8. Dataset and Feature Extraction now includes a clearer labeling protocol:
   - labels are assigned from source posture class during video/sample generation;
   - no expert ergonomic annotation protocol was found;
   - labels are treated as project-specific binary labels.
9. Experimental Setup now has a specific `Evaluation Protocol` subsection.
10. Experimental Setup states:
    - development set is used for training/model registry;
    - corrected external set is not used for training;
    - participant-wise evaluation holds out one participant;
    - frame-level random split can be optimistic;
    - threshold calibration selected 0.65.
11. Hardware details are not invented. The manuscript now says hardware was not recorded and runtime is reported as project-level processing measurement.
12. Desktop Application Implementation now includes the sentence required by the prompt:
    - `The application is used to verify real-time deployment of the proposed pipeline and is not evaluated as a commercial product.`
13. Google AI Edge documentation reference was changed from `2026` to `n.d.` because documentation pages can change and the project file did not provide a stable publication year.
14. `FIGURE_EXPORT_TODO.md` was updated to mention `SPRINGER_MANUSCRIPT_FINAL_DRAFT.md` and to state that Mermaid diagrams should be exported to PNG/SVG before Springer submission.

## What Is Still Missing

1. Real MediaPipe skeleton overlay figure from the project data.
2. Desktop GUI screenshot figure.
3. Exported PNG/SVG system architecture figure.
4. Exported PNG/SVG feature construction figure.
5. SQLite/dashboard/logging-flow figure.
6. Hardware details for runtime benchmarking.
7. Public benchmark evaluation, such as MultiPosture.
8. Expert ergonomic annotation or RULA/REBA-style validation.
9. Integration of the selected HistGradientBoosting model into the desktop app.
10. Exact Springer venue template conversion.

## Figures That Need Supplementation

See `reports/FIGURE_EXPORT_TODO.md`.

High-priority missing figures:

1. `reports/figures/system_architecture.png`
2. `reports/figures/feature_construction_pipeline.png`
3. `reports/figures/mediapipe_landmark_sample.png`
4. `reports/figures/desktop_gui_screenshot.png`
5. `reports/figures/sqlite_logging_flow.png`

Already available:

1. `reports/figures/external_confusion_matrix.png`
2. `reports/figures/external_threshold_sweep.png`
3. `reports/figures/temporal_smoothing_effect.png`
4. `reports/figures/feature_importance_top20.png`
5. `reports/figures/tpri_distribution.png`

## References That Need Checking

1. Google AI Edge documentation:
   - changed to `n.d.` because it is official documentation, not a fixed scholarly publication.
2. Sahoo et al. (2026):
   - web lookup found the MDPI page for DOI `10.3390/a19010048`.
   - keep, but still verify against the final bibliography style required by the venue.
3. Wang et al. (2025):
   - web lookup found the MDPI/PMC page for DOI `10.3390/e27121196`.
   - keep, but verify title punctuation and final volume/issue format when formatting references.
4. arXiv and official documentation references:
   - use them only for technical/methodological background.
   - do not treat them as the main evidence for sitting-posture recognition performance.

## Information Not Found in Project Artifacts

These items were not invented:

1. Hardware specification for runtime experiments.
2. Expert ergonomic annotation protocol.
3. Inter-rater agreement.
4. RULA/REBA score mapping.
5. Public benchmark results.
6. Whether the final desktop app already uses HistGradientBoosting.
7. Final Springer venue citation style.

## Does the Manuscript Still Look Like a Thesis or Project Report?

The final draft is closer to a scientific paper than the previous report-like version. The remaining project-report signals are:

1. The Desktop Application Implementation section still depends on a future GUI screenshot.
2. The paper still references local artifacts indirectly through project-level results.
3. The dataset is small, so the manuscript must keep the limitation language.
4. The exact Springer format has not yet been applied.

These issues do not invalidate the draft, but they should be addressed before formal submission.

## Final Quality Checks

| Check | Status |
|---|---|
| Abstract under 250 words | Passed |
| Abstract has no citation | Passed |
| Keywords contain 3-5 terms | Passed |
| No SOTA claim | Passed |
| No new-model claim | Passed |
| No forbidden AI-style phrases | Passed |
| Related Work closes with research gap | Passed |
| Proposed Method includes pseudocode | Passed |
| Dataset labels are project-specific | Passed |
| Corrected external set only P01 is stated | Passed |
| ANN/Keras app model and HGB selected experimental model are separated | Passed |
| Hardware details not invented | Passed |
| Conclusion has no citation | Passed |
| Figure export tasks documented | Passed |
