"""Compute session-level Temporal Posture Risk Index from SQLite logs.

The index is designed for reporting/demo, not medical diagnosis. It converts
session duration, incorrect posture persistence, warnings, and low-confidence
frames into a 0-100 score.
"""

from __future__ import annotations

import argparse
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DB = BASE_DIR / "database" / "posture_app.db"
DEFAULT_OUTPUT_DIR = BASE_DIR / "reports" / "results"

STATUS_CORRECT = "DUNG_TU_THE"
STATUS_INCORRECT = "SAI_TU_THE"
STATUS_NO_PERSON = "KHONG_PHAT_HIEN_NGUOI"


@dataclass(frozen=True)
class RiskWeights:
    incorrect_time: float = 0.40
    long_bad_posture: float = 0.25
    warning_rate: float = 0.20
    no_person: float = 0.15

    def validate(self) -> None:
        total = (
            self.incorrect_time
            + self.long_bad_posture
            + self.warning_rate
            + self.no_person
        )
        if abs(total - 1.0) > 1e-6:
            raise ValueError(f"Risk weights must sum to 1.0, got {total:.6f}.")
        if min(
            self.incorrect_time,
            self.long_bad_posture,
            self.warning_rate,
            self.no_person,
        ) < 0:
            raise ValueError("Risk weights must be non-negative.")


def parse_datetime(value: Any) -> datetime | None:
    if value is None or value == "":
        return None
    try:
        return datetime.fromisoformat(str(value))
    except ValueError:
        return None


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, float(value)))


def safe_ratio(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return 0.0
    return clamp(numerator / denominator)


def risk_level(score: float) -> str:
    if score < 25:
        return "LOW"
    if score < 50:
        return "MEDIUM"
    if score < 75:
        return "HIGH"
    return "CRITICAL"


def compute_warning_rate_norm(
    warning_count: int,
    duration_seconds: float,
    warning_rate_cap_per_hour: float,
) -> float:
    if duration_seconds <= 0 or warning_rate_cap_per_hour <= 0:
        return 0.0
    warnings_per_hour = warning_count / (duration_seconds / 3600.0)
    return clamp(warnings_per_hour / warning_rate_cap_per_hour)


def compute_risk_score(
    incorrect_time_ratio: float,
    long_bad_posture_ratio: float,
    warning_rate_norm: float,
    no_person_or_low_confidence_ratio: float,
    weights: RiskWeights,
) -> float:
    weights.validate()
    score = 100.0 * (
        weights.incorrect_time * clamp(incorrect_time_ratio)
        + weights.long_bad_posture * clamp(long_bad_posture_ratio)
        + weights.warning_rate * clamp(warning_rate_norm)
        + weights.no_person * clamp(no_person_or_low_confidence_ratio)
    )
    return round(max(0.0, min(100.0, score)), 3)


def estimate_status_durations(
    logs_df: pd.DataFrame,
    session_start: datetime | None,
    session_end: datetime | None,
) -> dict[str, float]:
    durations = {
        STATUS_CORRECT: 0.0,
        STATUS_INCORRECT: 0.0,
        STATUS_NO_PERSON: 0.0,
    }
    if logs_df.empty:
        return durations

    logs = logs_df.copy()
    logs["parsed_time"] = logs["thoiDiem"].map(parse_datetime)
    logs = logs.dropna(subset=["parsed_time"]).sort_values("parsed_time")
    if logs.empty:
        return durations

    end_time = session_end or logs["parsed_time"].max()
    previous_time = session_start or logs.iloc[0]["parsed_time"]
    previous_status: str | None = None

    for _, row in logs.iterrows():
        current_time = row["parsed_time"]
        if previous_status in durations and current_time > previous_time:
            durations[previous_status] += (current_time - previous_time).total_seconds()
        previous_status = str(row["trangThai"])
        previous_time = current_time

    if previous_status in durations and end_time and end_time > previous_time:
        durations[previous_status] += (end_time - previous_time).total_seconds()

    return durations


def estimate_long_bad_posture_seconds(
    logs_df: pd.DataFrame,
    session_start: datetime | None,
    session_end: datetime | None,
    min_bad_segment_seconds: float,
) -> float:
    if logs_df.empty or min_bad_segment_seconds <= 0:
        return 0.0

    logs = logs_df.copy()
    logs["parsed_time"] = logs["thoiDiem"].map(parse_datetime)
    logs = logs.dropna(subset=["parsed_time"]).sort_values("parsed_time")
    if logs.empty:
        return 0.0

    end_time = session_end or logs["parsed_time"].max()
    previous_time = session_start or logs.iloc[0]["parsed_time"]
    previous_status: str | None = None
    long_bad_seconds = 0.0

    for _, row in logs.iterrows():
        current_time = row["parsed_time"]
        if previous_status == STATUS_INCORRECT and current_time > previous_time:
            segment_seconds = (current_time - previous_time).total_seconds()
            if segment_seconds >= min_bad_segment_seconds:
                long_bad_seconds += segment_seconds
        previous_status = str(row["trangThai"])
        previous_time = current_time

    if previous_status == STATUS_INCORRECT and end_time and end_time > previous_time:
        segment_seconds = (end_time - previous_time).total_seconds()
        if segment_seconds >= min_bad_segment_seconds:
            long_bad_seconds += segment_seconds

    return max(0.0, long_bad_seconds)


def read_table(connection: sqlite3.Connection, table_name: str) -> pd.DataFrame:
    exists = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,),
    ).fetchone()
    if not exists:
        raise ValueError(f"Missing required table: {table_name}")
    return pd.read_sql_query(f"SELECT * FROM {table_name}", connection)


def resolve_path(path_text: str | Path) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else BASE_DIR / path


def compute_session_rows(
    sessions_df: pd.DataFrame,
    logs_df: pd.DataFrame,
    weights: RiskWeights,
    min_bad_segment_seconds: float,
    warning_rate_cap_per_hour: float,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for _, session in sessions_df.sort_values("maPhien").iterrows():
        session_id = int(session["maPhien"])
        session_logs = logs_df[logs_df["maPhien"] == session_id] if not logs_df.empty else logs_df

        start_time = parse_datetime(session.get("thoiGianBatDau"))
        end_time = parse_datetime(session.get("thoiGianKetThuc"))
        timestamp_duration = (
            (end_time - start_time).total_seconds()
            if start_time is not None and end_time is not None and end_time > start_time
            else 0.0
        )
        summary_duration = max(
            float(session.get("tongThoiGianDung") or 0.0)
            + float(session.get("tongThoiGianSai") or 0.0),
            0.0,
        )
        duration_seconds = max(timestamp_duration, summary_duration)

        status_durations = estimate_status_durations(session_logs, start_time, end_time)
        log_incorrect_seconds = status_durations.get(STATUS_INCORRECT, 0.0)
        table_incorrect_seconds = float(session.get("tongThoiGianSai") or 0.0)
        incorrect_seconds = max(table_incorrect_seconds, log_incorrect_seconds)

        long_bad_seconds = estimate_long_bad_posture_seconds(
            session_logs,
            start_time,
            end_time,
            min_bad_segment_seconds,
        )
        if long_bad_seconds <= 0 and table_incorrect_seconds >= min_bad_segment_seconds:
            long_bad_seconds = table_incorrect_seconds

        total_frames = int(session.get("tongSoFrame") or 0)
        no_person_frames = int(session.get("soFrameKhongCoNguoi") or 0)
        if total_frames > 0:
            no_person_ratio = safe_ratio(no_person_frames, total_frames)
        else:
            no_person_ratio = safe_ratio(status_durations.get(STATUS_NO_PERSON, 0.0), duration_seconds)

        log_warning_count = (
            int(session_logs["daCanhBao"].fillna(0).astype(int).sum())
            if not session_logs.empty and "daCanhBao" in session_logs.columns
            else 0
        )
        warning_count = max(int(session.get("soLanCanhBao") or 0), log_warning_count)

        incorrect_time_ratio = safe_ratio(incorrect_seconds, duration_seconds)
        long_bad_posture_ratio = safe_ratio(long_bad_seconds, duration_seconds)
        warning_rate_norm = compute_warning_rate_norm(
            warning_count,
            duration_seconds,
            warning_rate_cap_per_hour,
        )

        score = compute_risk_score(
            incorrect_time_ratio=incorrect_time_ratio,
            long_bad_posture_ratio=long_bad_posture_ratio,
            warning_rate_norm=warning_rate_norm,
            no_person_or_low_confidence_ratio=no_person_ratio,
            weights=weights,
        )

        rows.append(
            {
                "session_id": session_id,
                "session_date": start_time.date().isoformat() if start_time else "",
                "source_type": session.get("loaiNguon") or "",
                "duration_seconds": round(duration_seconds, 3),
                "total_frames": total_frames,
                "incorrect_seconds": round(incorrect_seconds, 3),
                "long_bad_posture_seconds": round(long_bad_seconds, 3),
                "warning_count": warning_count,
                "no_person_frames": no_person_frames,
                "incorrect_time_ratio": round(incorrect_time_ratio, 6),
                "long_bad_posture_ratio": round(long_bad_posture_ratio, 6),
                "warning_rate_norm": round(warning_rate_norm, 6),
                "no_person_or_low_confidence_ratio": round(no_person_ratio, 6),
                "temporal_risk_index": score,
                "risk_level": risk_level(score),
                "data_quality_note": build_data_quality_note(
                    duration_seconds,
                    total_frames,
                    len(session_logs),
                    end_time is not None,
                ),
            }
        )

    return rows


def build_data_quality_note(
    duration_seconds: float,
    total_frames: int,
    log_count: int,
    has_end_time: bool,
) -> str:
    notes: list[str] = []
    if duration_seconds <= 0:
        notes.append("zero_duration")
    if total_frames <= 0:
        notes.append("no_frame_summary")
    if log_count <= 0:
        notes.append("no_posture_logs")
    if not has_end_time:
        notes.append("missing_end_time")
    return ";".join(notes) if notes else "ok"


def build_daily_summary(session_risk_df: pd.DataFrame) -> pd.DataFrame:
    if session_risk_df.empty:
        return pd.DataFrame(
            columns=[
                "session_date",
                "session_count",
                "mean_risk",
                "median_risk",
                "max_risk",
                "high_or_critical_sessions",
                "total_duration_seconds",
                "total_warnings",
            ]
        )

    grouped = session_risk_df.groupby("session_date", dropna=False)
    summary = grouped.agg(
        session_count=("session_id", "count"),
        mean_risk=("temporal_risk_index", "mean"),
        median_risk=("temporal_risk_index", "median"),
        max_risk=("temporal_risk_index", "max"),
        total_duration_seconds=("duration_seconds", "sum"),
        total_warnings=("warning_count", "sum"),
    ).reset_index()

    high_counts = grouped["risk_level"].apply(
        lambda values: int(values.isin(["HIGH", "CRITICAL"]).sum())
    )
    summary = summary.merge(
        high_counts.rename("high_or_critical_sessions").reset_index(),
        on="session_date",
        how="left",
    )
    numeric_columns = ["mean_risk", "median_risk", "max_risk", "total_duration_seconds"]
    for column in numeric_columns:
        summary[column] = summary[column].round(3)
    return summary


def write_summary_report(
    output_path: Path,
    session_risk_df: pd.DataFrame,
    daily_summary_df: pd.DataFrame,
    weights: RiskWeights,
    min_bad_segment_seconds: float,
    warning_rate_cap_per_hour: float,
) -> None:
    if session_risk_df.empty:
        distribution_text = "No sessions available."
        top_sessions_text = "No sessions available."
    else:
        distribution_text = session_risk_df["risk_level"].value_counts().to_string()
        top_sessions_text = (
            session_risk_df.sort_values("temporal_risk_index", ascending=False)
            .head(10)[
                [
                    "session_id",
                    "session_date",
                    "source_type",
                    "duration_seconds",
                    "temporal_risk_index",
                    "risk_level",
                    "data_quality_note",
                ]
            ]
            .to_string(index=False)
        )

    report = f"""Temporal Posture Risk Index Summary
===================================

Formula:
risk_index = 100 * (
  {weights.incorrect_time:.2f} * incorrect_time_ratio
  + {weights.long_bad_posture:.2f} * long_bad_posture_ratio
  + {weights.warning_rate:.2f} * warning_rate_norm
  + {weights.no_person:.2f} * no_person_or_low_confidence_ratio
)

Parameters:
- Long bad posture minimum segment: {min_bad_segment_seconds:.1f} seconds
- Warning-rate normalization cap: {warning_rate_cap_per_hour:.1f} warnings/hour

Risk levels:
- LOW: [0, 25)
- MEDIUM: [25, 50)
- HIGH: [50, 75)
- CRITICAL: [75, 100]

Session count: {len(session_risk_df)}

Risk level distribution:
{distribution_text}

Daily summary:
{daily_summary_df.to_string(index=False) if not daily_summary_df.empty else "No daily data."}

Top risk sessions:
{top_sessions_text}

Interpretation note:
The index is a temporal ergonomic monitoring score for comparing sessions in this
application. It is not a clinical or medical diagnosis. Data-quality notes should
be checked before using a session in a research table.
"""
    output_path.write_text(report, encoding="utf-8")


def compute_temporal_risk(args: argparse.Namespace) -> None:
    db_path = resolve_path(args.database)
    output_dir = resolve_path(args.output_dir)
    if not db_path.exists():
        raise FileNotFoundError(
            f"Database not found: {db_path}. Run: python src/3_database_setup.py"
        )

    weights = RiskWeights(
        incorrect_time=args.incorrect_weight,
        long_bad_posture=args.long_bad_weight,
        warning_rate=args.warning_weight,
        no_person=args.no_person_weight,
    )
    weights.validate()

    output_dir.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as connection:
        sessions_df = read_table(connection, "PhienLamViec")
        logs_df = read_table(connection, "NhatKyTuThe")

    rows = compute_session_rows(
        sessions_df=sessions_df,
        logs_df=logs_df,
        weights=weights,
        min_bad_segment_seconds=args.min_bad_segment_seconds,
        warning_rate_cap_per_hour=args.warning_rate_cap_per_hour,
    )
    session_risk_df = pd.DataFrame(rows)
    daily_summary_df = build_daily_summary(session_risk_df)

    session_output = output_dir / "session_risk_index.csv"
    daily_output = output_dir / "session_risk_daily_summary.csv"
    report_output = output_dir / "temporal_risk_summary.txt"

    session_risk_df.to_csv(session_output, index=False, encoding="utf-8-sig")
    daily_summary_df.to_csv(daily_output, index=False, encoding="utf-8-sig")
    write_summary_report(
        report_output,
        session_risk_df,
        daily_summary_df,
        weights,
        args.min_bad_segment_seconds,
        args.warning_rate_cap_per_hour,
    )

    print(f"Saved session risk index: {session_output}")
    print(f"Saved daily risk summary: {daily_output}")
    print(f"Saved summary report: {report_output}")
    if not session_risk_df.empty:
        print("\nRisk level distribution:")
        print(session_risk_df["risk_level"].value_counts().to_string())
        print("\nTop 5 risk sessions:")
        print(
            session_risk_df.sort_values("temporal_risk_index", ascending=False)
            .head(5)[
                [
                    "session_id",
                    "session_date",
                    "duration_seconds",
                    "temporal_risk_index",
                    "risk_level",
                    "data_quality_note",
                ]
            ]
            .to_string(index=False)
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute Temporal Posture Risk Index from SQLite session logs."
    )
    parser.add_argument("--database", default=str(DEFAULT_DB))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument(
        "--min-bad-segment-seconds",
        type=float,
        default=5.0,
        help="Minimum continuous incorrect-posture segment counted as long-bad posture.",
    )
    parser.add_argument(
        "--warning-rate-cap-per-hour",
        type=float,
        default=12.0,
        help="Warnings/hour mapped to warning_rate_norm=1.0.",
    )
    parser.add_argument("--incorrect-weight", type=float, default=0.40)
    parser.add_argument("--long-bad-weight", type=float, default=0.25)
    parser.add_argument("--warning-weight", type=float, default=0.20)
    parser.add_argument("--no-person-weight", type=float, default=0.15)
    return parser.parse_args()


if __name__ == "__main__":
    compute_temporal_risk(parse_args())
