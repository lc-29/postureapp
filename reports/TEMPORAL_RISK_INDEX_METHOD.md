# Temporal Posture Risk Index Method

## Purpose

Temporal Posture Risk Index (TPRI) turns frame/session logs into a session-level
score from 0 to 100. The score is designed for comparing demo sessions and for
research reporting. It is not a clinical or medical diagnosis.

## Inputs

The script reads SQLite tables:

- `PhienLamViec`: session start/end, frame counts, posture durations, warnings.
- `NhatKyTuThe`: time-stamped posture status changes and warning events.

Run:

```powershell
python src/12_temporal_risk_index.py
```

Generated local outputs:

- `reports/results/session_risk_index.csv`
- `reports/results/session_risk_daily_summary.csv`
- `reports/results/temporal_risk_summary.txt`

These generated files are ignored by Git because they are derived from local
session logs.

## Formula

```text
risk_index = 100 * (
  0.40 * incorrect_time_ratio
  + 0.25 * long_bad_posture_ratio
  + 0.20 * warning_rate_norm
  + 0.15 * no_person_or_low_confidence_ratio
)
```

Components:

| Component | Meaning | Default range |
|---|---|---:|
| `incorrect_time_ratio` | Incorrect posture seconds divided by session duration. | 0-1 |
| `long_bad_posture_ratio` | Continuous incorrect-posture segments at least 5 seconds divided by session duration. | 0-1 |
| `warning_rate_norm` | Warnings/hour normalized by a cap of 12 warnings/hour. | 0-1 |
| `no_person_or_low_confidence_ratio` | No-person/low-confidence frames divided by total frames, with log-duration fallback. | 0-1 |

## Risk levels

| Range | Level |
|---:|---|
| `[0, 25)` | LOW |
| `[25, 50)` | MEDIUM |
| `[50, 75)` | HIGH |
| `[75, 100]` | CRITICAL |

## Current local run summary

The current local database run produced 50 sessions:

| Level | Count |
|---|---:|
| LOW | 19 |
| MEDIUM | 25 |
| HIGH | 6 |
| CRITICAL | 0 |

The highest observed session-level score was `61.053` (HIGH). Because this is
derived from local demo logs, use it as an application evaluation example rather
than as dataset-level model performance.
