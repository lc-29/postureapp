# Springer Critical Fix Report

Task source: `workflow_kilo/17_TASK_SPRINGER_CRITICAL_FIX_TODO_FOR_CODEX.md`

Main revised files:

- `reports/springer_overleaf/main_revised.tex`
- `reports/springer_overleaf/main_revised.pdf`
- `reports/springer_overleaf/main.tex`
- `reports/springer_overleaf/main.pdf`
- `reports/springer_overleaf/references.bib`

## Fix Summary

| Issue | Fixed? | Location | What changed | Remaining risk |
|---|---|---|---|---|
| Clarify threshold calibration set | Yes | `main_revised.tex`, Section 5.1 and Section 6.3 | Verified from `src/22_calibrate_threshold.py` and `reports/THRESHOLD_CALIBRATION_REPORT.md` that threshold 0.65 was calibrated on the corrected external set. The paper now reports this as calibrated external performance, not a strictly independent hold-out result. | A future protocol should calibrate threshold on development/validation data and reserve external data only for final testing. |
| Clarify labeling protocol | Yes | `main_revised.tex`, Section 4 | Kept truthful wording: labels are project-specific, assigned from source video posture class during sample generation, and no expert annotation/inter-rater agreement/RULA/REBA exists. Added context from manifest and external correction reports. | The project still lacks formal expert ergonomic labeling. |
| Add rule-based baseline threshold table | Yes | `main_revised.tex`, Table `tab:rule_thresholds` | Extracted thresholds from `src/posture_baseline.py`: visibility 0.50, shoulder y diff 0.06, shoulder tilt 10 deg, torso lean 12 deg, head offset 0.10, neck clearance ratio 0.12, hand-mouth ratio 0.45, absolute hand-mouth distance 0.13, hand visibility 0.35. | Thresholds are heuristic baseline values, not clinical ergonomic criteria. |
| Add ergonomic/geometric feature definition table | Yes | `main_revised.tex`, Table `tab:ergonomic_definitions` | Added definitions, main landmarks, and purpose for ergonomic features using `src/feature_schema.py`, `src/16_build_ergonomic_features.py`, and `reports/FEATURE_SCHEMA_FINAL.md`. | Some features remain heuristic and depend on MediaPipe landmark quality. |
| Add hardware/runtime details if available | Partially | `main_revised.tex`, Section 5 and Limitations | Added available runtime setup: 640x360 input frames, MediaPipe complexity 1, max 120 sampled frames per representative video. | CPU/RAM/GPU were not found in current project artifacts. No value was invented. |
| Fix Table 1 mixed levels | Yes | `main_revised.tex`, Table 1 | Removed `Full video manifest` row from the split table. Added manifest information in prose after the table. | None. |
| Clarify positive class in result table headers | Yes | `main_revised.tex`, Tables 3, 4, 5 | Changed headers to `Precision Inc.`, `Recall Inc.`, and `F1 Inc.` where applicable. | None. |
| Add MCC to Table 4 | Yes | `main_revised.tex`, Table 4 | Added MCC values from model registry summary. To keep width manageable, Table 4 now reports Accuracy, Recall Inc., F1 Inc., and MCC. | Precision Inc. is omitted from Table 4 to reduce table width; it remains discussed elsewhere. |
| Add FP/FN to Table 5 | Yes | `main_revised.tex`, Table 5 | Added FP=34 and FN=24 for the final selected model. | None. |
| Add GUI screenshot | Not fixed | Report only | No real GUI screenshot was found in the project artifacts. No image was invented and no placeholder was inserted into the manuscript. | Run the app, capture a privacy-safe screenshot, and add it later if needed. |
| Check temporal smoothing figure | Yes | `main_revised.tex`, Fig. smoothing caption | Inspected `reports/figures/temporal_smoothing_effect.png`. It already shows frame probability, temporal mean, and threshold. Caption was revised to match actual content. | Figure does not show warning region/event; manuscript no longer claims it does. |
| Increase references to 20-30 if quality sources exist | Yes | `main_revised.tex`, Related Work; `references.bib` | Added citations already present in BibTeX/project context: Jiang et al. survey and Kim et al. MediaPipe Pose study. Cited references increased to 20. | Do not add more references unless they support specific text. |
| Fix reference capitalization | Yes | `references.bib` | Protected key terms with braces: `{MediaPipe}`, `{OpenPose}`, `{BlazePose}`, `{IoT}`, `{COVID-19}`, `{Kolmogorov-Arnold}`, `{MultiPosture}`, `{ALIGN}`, `{LAViTSPose}`. | None. |
| Check Sahoo et al. 2026 | Yes | `references.bib` and previous web/project check | Kept Sahoo et al. because DOI `10.3390/a19010048` was present and previously verified against the MDPI page. | Since it is a 2026 source, verify final citation details again near submission date. |
| Add Data/Code/Ethics note | Yes | `main_revised.tex`, before Conclusion | Added a short data/code/ethics note stating raw videos are not planned for public release due to identifiable participants; anonymized landmarks may be shared if venue and consent permit. | Consent documentation is not present in project artifacts, so the text does not claim consent. |
| Avoid overclaiming | Yes | Throughout `main_revised.tex` | Kept existing-model + new dataset/features framing; no SOTA claim; HGB is experimental best model, not app model. | None. |
| Remove unfinished manuscript placeholders | Yes | `main_revised.tex` | No image placeholder or unfinished submission note is included in the manuscript. GUI screenshot remains a report/TODO item only. | None. |

## Evidence Read

- `src/22_calibrate_threshold.py`
- `src/23_final_evaluation_protocol.py`
- `src/21_train_model_registry.py`
- `reports/THRESHOLD_CALIBRATION_REPORT.md`
- `reports/FINAL_EVALUATION_REPORT.md`
- `reports/EXPERIMENT_PROTOCOL_FINAL.md`
- `reports/DATASET_MANIFEST.md`
- `reports/DATASET_VIDEO_MANIFEST_SUMMARY.md`
- `src/posture_baseline.py`
- `src/feature_schema.py`
- `src/16_build_ergonomic_features.py`
- `reports/FEATURE_SCHEMA_FINAL.md`
- `reports/RUNTIME_BENCHMARK.md`
- `reports/figures/temporal_smoothing_effect.png`

## Verification

Compile command:

```powershell
cd D:\posture_detection_app\reports\springer_overleaf
& "D:\Tools Springer\tectonic\tectonic.exe" -X compile main_revised.tex
```

Result:

- `main_revised.pdf` generated successfully.
- No fatal LaTeX errors.
- Remaining warnings are layout warnings (`Underfull \hbox` / bibliography line breaks), not compile blockers.

Additional checks:

| Check | Result |
|---|---|
| `main_revised.tex` exists | Passed |
| `main_revised.pdf` exists | Passed |
| Citation keys used in manuscript exist in `references.bib` | Passed |
| Referenced figures exist | Passed |
| No fake hardware value added | Passed |
| No fake GUI screenshot added | Passed |
| No fake DOI added | Passed |
| No SOTA claim added | Passed |

## Files Produced

| Required output | Status |
|---|---|
| `reports/springer_overleaf/main_revised.tex` | Created |
| `reports/springer_overleaf/main_revised.pdf` | Created |
| `reports/SPRINGER_CRITICAL_FIX_REPORT.md` | Created |

`reports/springer_overleaf/main.tex` was also synchronized with `main_revised.tex`, so Overleaf's default main file now contains the critical fixes.
