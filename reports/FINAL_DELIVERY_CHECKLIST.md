# Final Delivery Checklist

## Environment

- [ ] Fresh virtual environment created.
- [ ] `pip install -r requirements.txt` succeeds.
- [ ] `python src/3_database_setup.py` succeeds.
- [ ] `python -m pytest tests` does not open webcam and does not hang.

## Runtime artifacts

- [ ] `models/ann_best.keras` exists.
- [ ] `models/scaler.pkl` exists.
- [ ] `database/posture_app.db` exists after setup.
- [ ] Demo video path is available outside Git if needed.

## Evaluation

- [ ] Local metrics reviewed.
- [ ] `python src/6_evaluate_external.py` run.
- [ ] External metrics saved in `reports/results/`.
- [ ] Threshold sweep saved.
- [ ] Statistical analysis saved: confidence interval and McNemar test.
- [ ] Video-wise metadata plan documented.

## Demo

- [ ] ANN mode tested.
- [ ] Rule-based mode tested.
- [ ] Webcam tested.
- [ ] Video file tested.
- [ ] Audio warning tested.
- [ ] SQLite session logging tested.
- [ ] `reports/GUI_QA_CHECKLIST.md` filled.

## Paper/report

- [ ] Paper outline exists.
- [ ] Method draft exists.
- [ ] Results draft updated with external metrics.
- [ ] Figure/table plan exists.
- [ ] Related work citations collected from real sources.
- [ ] Limitations section is explicit about frame-wise split and dataset size.
