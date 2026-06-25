# Springer Manuscript Checklist

File checked: `reports/SPRINGER_MANUSCRIPT_COMPLETE.md`

## Scope and Claim Control

| Item | Status | Note |
|---|---|---|
| Research direction is Existing model + new dataset/features | Pass | The manuscript explicitly states that the contribution is not a new pose estimation model or new AI architecture. |
| No state-of-the-art claim | Pass | The manuscript uses contextual comparison only. |
| No switch to web/mobile/YOLO/CNN direction | Pass | The manuscript stays with desktop Python, OpenCV, MediaPipe Pose, ANN, and lightweight ML. |
| App ANN and best experimental HGB are separated | Pass | The manuscript states that the app currently uses ANN mode and HGB is the best selected experimental model. |
| External set limitation P01 only is stated | Pass | Stated in Dataset, Participant-Wise Evaluation, and Limitations. |
| Project-specific labels are stated | Pass | The manuscript states that Correct/Incorrect labels are project-specific and not expert-validated. |

## Structure

| Required section | Status |
|---|---|
| Title | Pass |
| Abstract | Pass |
| Keywords | Pass |
| Introduction | Pass |
| Related Work | Pass |
| Proposed Method | Pass |
| Dataset and Feature Extraction | Pass |
| Experimental Setup | Pass |
| Results and Discussion | Pass |
| Desktop Application Implementation | Pass |
| Limitations | Pass |
| Conclusion and Future Work | Pass |
| References | Pass |

## Abstract and Keywords

| Item | Status | Note |
|---|---|---|
| Abstract below 250 words | Pass | Approximately 219 words. |
| Abstract contains problem, method, dataset, results, contribution | Pass | All five elements are included. |
| Keywords at most 5 | Pass | 5 keywords. |

## Data and Results

| Item | Status | Note |
|---|---|---|
| Dataset sizes match project artifacts | Pass | 84 raw videos, 5 participants, 11,022 samples, 10 external videos, 1,658 external samples. |
| ANN external result included | Pass | Accuracy 90.17%, F1 incorrect 90.34%. |
| Rule-based external result included | Pass | Accuracy 67.49%, F1 incorrect 75.40%. |
| Final selected model result included | Pass | Accuracy 96.50%, Precision 96.22%, Recall 97.30%, F1 96.76%, MCC 92.97%, FP 34, FN 24. |
| Runtime benchmark included | Pass | front 28.32 FPS, side_30 28.03 FPS, side_90 29.34 FPS. |
| Frame-level split optimism noted | Pass | Stated in Experimental Setup and Discussion. |

## Figures and Tables

| Item | Status | Note |
|---|---|---|
| At least 6 figure placeholders/captions | Pass | Fig. 1 to Fig. 6 included. |
| At least 5 tables/captions | Pass | Table 1 to Table 7 included. |
| Every mentioned figure has caption | Pass | All figure placeholders include captions. |
| Every table has caption | Pass | All tables include captions. |

## References

| Item | Status | Note |
|---|---|---|
| Uses project references only | Pass | References are from `TAILIEUTHAMKHAO.md` and `RELATED_PAPERS.bib`. |
| No invented DOI | Pass | DOI/URL values come from project files. |
| Blog/tutorial not used as academic Related Work source | Pass | Google official documentation is used only as implementation/methodology reference. |
| Author-year citations used in manuscript body | Pass | In-text citations use author-year style. |
| References do not use "et al." | Pass | Author names are listed as available from project files. |

## Remaining Work Before Submission

1. Insert real figures or exported PNGs for all figure placeholders.
2. Confirm whether the target Springer venue requires numeric citations instead of author-year citations.
3. Check official Springer template formatting, author block, affiliation block, and page limit.
4. If possible, integrate the selected HGB registry model into the desktop app or keep the manuscript wording as currently written.
5. Add expert ergonomic annotation or RULA/REBA-inspired labeling if the scope is expanded beyond a posture warning prototype.
6. Consider a public dataset benchmark such as MultiPosture after license and label mapping checks.
