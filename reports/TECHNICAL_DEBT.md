# Technical Debt

## P0 - Must fix before final demo

| Area | Debt | Mitigation |
|---|---|---|
| Testing | Some dependencies may be missing on a fresh machine | Document Python version and run full install test. |
| GUI | Manual QA not filled yet | Execute `reports/GUI_QA_CHECKLIST.md`. |
| Evaluation | External/statistical metrics must be regenerated after model changes | Run `python src/6_evaluate_external.py` and `python src/11_statistical_analysis.py`. |

## P1 - Important before paper submission

| Area | Debt | Mitigation |
|---|---|---|
| Data | Current CSV lacks `source_video` and `frame_index` | Re-extract with `--include-metadata`. |
| Evaluation | Frame-wise split may overestimate performance | Implement video-wise/person-wise split once metadata exists. |
| Baseline | Rule-based logic is still duplicated between script and GUI | Extract shared `posture_baseline.py`. |
| Reporting | Related work citations are placeholders | Fill `RELATED_WORK_TODO.md` with real sources. |

## P2 - Nice to improve

| Area | Debt | Mitigation |
|---|---|---|
| Packaging | No one-command app build | Add PyInstaller or installer later. |
| Dataset storage | Raw videos are not in Git | Use Git LFS or external storage with manifest links. |
| UX | Error messages can be more actionable | Improve missing model/scaler/database dialogs. |
| Experiments | Ablation is still small and single-run | Repeat across splits/seeds after metadata split exists. |
