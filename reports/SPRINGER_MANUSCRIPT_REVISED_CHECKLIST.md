# Springer Manuscript Revised Checklist

This checklist records the current status of `SPRINGER_MANUSCRIPT_REVISED.md` against the writing guide and the project evidence.

| Item | Status | Note |
|---|---|---|
| Abstract under 250 words | Passed | Current abstract is 206 words. |
| Abstract avoids citation | Passed | No citation is used in the abstract. |
| Keywords contain 3-5 terms | Passed | Current manuscript has 5 keywords. |
| Forbidden placeholder text removed | Passed | No unfinished submission-note placeholder remains. |
| Raw figure placeholders removed | Passed | No raw figure insertion placeholder remains. |
| Introduction states practical problem | Passed | Computer-work posture errors and webcam motivation are stated. |
| Introduction states prior limitations | Passed | Sensor, smart-chair, wearable, RGB-D, and incomplete desktop pipeline limitations are stated. |
| Introduction states research gap | Passed | Gap is linked to webcam + MediaPipe + features + baseline + benchmark + warning/logging. |
| Contributions are concrete | Passed | Three contributions are listed. |
| Related Work has three groups | Passed | Sensor/depth, RGB vision, and pose-landmark groups are used. |
| Related Work closes with research gap | Passed | Final paragraph states the specific gap. |
| Proposed Method has consistent module names | Passed | Module names match text, diagram, and Algorithm 1. |
| Pseudocode included | Passed | Algorithm 1 is included. |
| Formulas use LaTeX text | Passed | Normalization and evaluation formulas are written in LaTeX blocks. |
| Dataset table is split-oriented | Passed | Main dataset table uses development/training, corrected external, and manifest rows. |
| Dataset labels are described as project-specific | Passed | Manuscript does not claim expert annotation. |
| External set limitation is stated | Passed | External set is identified as P01 only. |
| ANN app model and HGB selected experimental model are separated | Passed | This distinction is stated in setup, results, limitations, and conclusion. |
| Results use concrete metrics | Passed | Main result tables use exact percentages and FP/FN counts. |
| Literature comparison avoids leaderboard claim | Passed | Manuscript says literature metrics are contextual, not directly comparable. |
| Desktop implementation is concise | Passed | Implementation section focuses on feasibility, warning, logging, and analysis support. |
| Conclusion avoids citation | Passed | No author-year citation is used in the conclusion section. |
| No state-of-the-art claim | Passed | Manuscript avoids SOTA/general superiority claims. |
| References avoid blog/tutorial as main scientific sources | Passed | Main reference list uses papers, dataset, arXiv, and official documentation. |
| Springer template final conversion | Needs work | Convert to the exact venue template after choosing conference/journal. |
| Missing figures exported | Needs work | See `FIGURE_EXPORT_TODO.md`. |
| Public benchmark evaluation | Needs work | MultiPosture or similar benchmark has not yet been run. |
| Expert ergonomic validation | Needs work | No expert annotation or RULA/REBA validation yet. |
| Full GUI FPS measurement | Needs work | Runtime benchmark measures processing latency, not full GUI refresh. |
| HGB integration into app | Needs work | App currently uses ANN/Keras mode. |

## Final Submission Checklist

Before submission, complete these items:

1. Export all required figures as image files.
2. Replace Mermaid diagrams with image files if the final Springer template does not support Mermaid.
3. Convert references to the exact format required by the selected Springer venue.
4. Verify all citations in text appear in the reference list.
5. Verify every figure and table is cited in the text.
6. Confirm that no result is reported without an existing project file or experiment report.
7. Add public benchmark results only after running the benchmark with a clear label-mapping protocol.
8. Add expert annotation only if the annotation source and rubric can be described accurately.
