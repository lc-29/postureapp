"""Data preparation helpers for the desktop statistics dashboard."""

from __future__ import annotations

import importlib.util
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


try:
    from runtime_paths import app_base_dir, resource_path, writable_database_path
except ImportError:
    from src.runtime_paths import app_base_dir, resource_path, writable_database_path


BASE_DIR = app_base_dir()
DEFAULT_DB = writable_database_path()
TEMPORAL_RISK_PATH = resource_path(Path("src") / "12_temporal_risk_index.py")


def _load_temporal_risk_module() -> Any:
    module_name = "temporal_risk_index_for_stats"
    if module_name in sys.modules:
        return sys.modules[module_name]

    spec = importlib.util.spec_from_file_location(module_name, TEMPORAL_RISK_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load temporal risk module: {TEMPORAL_RISK_PATH}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


temporal_risk = _load_temporal_risk_module()


def parse_datetime(value: Any) -> datetime | None:
    if value is None or value == "":
        return None
    try:
        return datetime.fromisoformat(str(value))
    except ValueError:
        return None


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value if value is not None else default)
    except (TypeError, ValueError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value if value is not None else default)
    except (TypeError, ValueError):
        return default


def safe_ratio(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return 0.0
    return max(0.0, min(1.0, numerator / denominator))


def resolve_db_path(db_path: str | Path = DEFAULT_DB) -> Path:
    path = Path(db_path)
    return path if path.is_absolute() else resource_path(path)


def empty_daily_stats(date_text: str) -> dict[str, Any]:
    return {
        "ngay": date_text,
        "tongSoPhien": 0,
        "tongThoiGianLamViec": 0.0,
        "tongThoiGianDung": 0.0,
        "tongThoiGianSai": 0.0,
        "tongSoCanhBao": 0,
        "tiLeDung": 0.0,
        "tiLeSai": 0.0,
        "thoiGianKhongXacDinh": 0.0,
        "tiLeKhongXacDinh": 0.0,
        "doTinCayTrungBinh": 0.0,
        "highestRiskIndex": 0.0,
        "averageRiskIndex": 0.0,
        "highestRiskLevel": "LOW",
    }


def table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
    row = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,),
    ).fetchone()
    return row is not None


def list_available_dates(db_path: str | Path = DEFAULT_DB) -> list[str]:
    path = resolve_db_path(db_path)
    if not path.exists():
        return []

    with sqlite3.connect(path) as connection:
        dates: set[str] = set()
        if table_exists(connection, "ThongKeNgay"):
            dates.update(
                str(row[0])
                for row in connection.execute(
                    "SELECT ngay FROM ThongKeNgay WHERE ngay IS NOT NULL"
                ).fetchall()
            )
        if table_exists(connection, "PhienLamViec"):
            dates.update(
                str(row[0])[:10]
                for row in connection.execute(
                    """
                    SELECT thoiGianBatDau
                    FROM PhienLamViec
                    WHERE thoiGianBatDau IS NOT NULL AND thoiGianBatDau != ''
                    """
                ).fetchall()
            )
    return sorted(dates, reverse=True)


def compute_session_duration(row: dict[str, Any]) -> float:
    started_at = parse_datetime(row.get("thoiGianBatDau"))
    ended_at = parse_datetime(row.get("thoiGianKetThuc"))
    timestamp_seconds = (
        (ended_at - started_at).total_seconds()
        if started_at is not None and ended_at is not None and ended_at > started_at
        else 0.0
    )
    summary_seconds = (
        safe_float(row.get("tongThoiGianDung"))
        + safe_float(row.get("tongThoiGianSai"))
    )
    return max(timestamp_seconds, summary_seconds, 0.0)


def enrich_session(row: dict[str, Any]) -> dict[str, Any]:
    duration_seconds = compute_session_duration(row)
    correct_seconds = safe_float(row.get("tongThoiGianDung"))
    incorrect_seconds = safe_float(row.get("tongThoiGianSai"))
    warning_count = safe_int(row.get("soLanCanhBao"))
    total_frames = safe_int(row.get("tongSoFrame"))
    correct_frames = safe_int(row.get("soFrameDung"))
    incorrect_frames = safe_int(row.get("soFrameSai"))
    no_person_frames = safe_int(row.get("soFrameKhongCoNguoi"))

    correct_ratio = safe_ratio(correct_seconds, duration_seconds)
    incorrect_ratio = safe_ratio(incorrect_seconds, duration_seconds)
    no_person_ratio = safe_ratio(no_person_frames, total_frames)
    long_bad_ratio = incorrect_ratio if incorrect_seconds >= 5.0 else 0.0
    warning_rate_norm = temporal_risk.compute_warning_rate_norm(
        warning_count=warning_count,
        duration_seconds=duration_seconds,
        warning_rate_cap_per_hour=12.0,
    )
    risk_index = temporal_risk.compute_risk_score(
        incorrect_time_ratio=incorrect_ratio,
        long_bad_posture_ratio=long_bad_ratio,
        warning_rate_norm=warning_rate_norm,
        no_person_or_low_confidence_ratio=no_person_ratio,
        weights=temporal_risk.RiskWeights(),
    )

    enriched = dict(row)
    enriched.update(
        {
            "durationSeconds": duration_seconds,
            "correctRatio": correct_ratio,
            "incorrectRatio": incorrect_ratio,
            "noPersonRatio": no_person_ratio,
            "warningRateNorm": warning_rate_norm,
            "riskIndex": risk_index,
            "riskLevel": temporal_risk.risk_level(risk_index),
            "dataQualityNote": "ok" if total_frames > 0 else "no_frame_summary",
            "totalFrames": total_frames,
            "correctFrames": correct_frames,
            "incorrectFrames": incorrect_frames,
            "noPersonFrames": no_person_frames,
            "averageConfidence": safe_float(row.get("doTinCayTrungBinh")),
        }
    )
    return enriched


def get_session_statistics(
    db_path: str | Path = DEFAULT_DB,
    date_text: str | None = None,
) -> list[dict[str, Any]]:
    path = resolve_db_path(db_path)
    if not path.exists():
        raise FileNotFoundError(f"Database not found: {path}")

    if date_text is None:
        date_text = datetime.now().date().isoformat()

    with sqlite3.connect(path) as connection:
        connection.row_factory = sqlite3.Row
        if not table_exists(connection, "PhienLamViec"):
            return []
        rows = connection.execute(
            """
            SELECT
                maPhien,
                thoiGianBatDau,
                thoiGianKetThuc,
                loaiNguon,
                giaTriNguon,
                tongThoiGianDung,
                tongThoiGianSai,
                soLanCanhBao,
                tongSoFrame,
                soFrameDung,
                soFrameSai,
                soFrameKhongCoNguoi,
                doTinCayTrungBinh
            FROM PhienLamViec
            WHERE thoiGianBatDau LIKE ?
            ORDER BY thoiGianBatDau ASC
            """,
            (date_text + "%",),
        ).fetchall()

    return [enrich_session(dict(row)) for row in rows]


def get_daily_statistics(
    db_path: str | Path = DEFAULT_DB,
    date_text: str | None = None,
    sessions: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    path = resolve_db_path(db_path)
    if not path.exists():
        raise FileNotFoundError(f"Database not found: {path}")

    if date_text is None:
        date_text = datetime.now().date().isoformat()

    stats = empty_daily_stats(date_text)
    with sqlite3.connect(path) as connection:
        connection.row_factory = sqlite3.Row
        if table_exists(connection, "ThongKeNgay"):
            row = connection.execute(
                """
                SELECT
                    ngay,
                    tongSoPhien,
                    tongThoiGianLamViec,
                    tongThoiGianDung,
                    tongThoiGianSai,
                    tongSoCanhBao,
                    tiLeDung,
                    tiLeSai
                FROM ThongKeNgay
                WHERE ngay = ?
                """,
                (date_text,),
            ).fetchone()
            if row is not None:
                stats.update(dict(row))

    if sessions is None:
        sessions = get_session_statistics(path, date_text)

    if sessions and safe_int(stats.get("tongSoPhien")) == 0:
        stats["tongSoPhien"] = len(sessions)
        stats["tongThoiGianLamViec"] = sum(s["durationSeconds"] for s in sessions)
        stats["tongThoiGianDung"] = sum(safe_float(s.get("tongThoiGianDung")) for s in sessions)
        stats["tongThoiGianSai"] = sum(safe_float(s.get("tongThoiGianSai")) for s in sessions)
        stats["tongSoCanhBao"] = sum(safe_int(s.get("soLanCanhBao")) for s in sessions)

    total_work = safe_float(stats.get("tongThoiGianLamViec"))
    total_correct = safe_float(stats.get("tongThoiGianDung"))
    total_incorrect = safe_float(stats.get("tongThoiGianSai"))
    unknown_seconds = max(0.0, total_work - total_correct - total_incorrect)
    stats["thoiGianKhongXacDinh"] = unknown_seconds
    stats["tiLeDung"] = safe_ratio(total_correct, total_work)
    stats["tiLeSai"] = safe_ratio(total_incorrect, total_work)
    stats["tiLeKhongXacDinh"] = safe_ratio(unknown_seconds, total_work)

    total_confidence_frames = sum(safe_int(s.get("totalFrames")) for s in sessions)
    if total_confidence_frames > 0:
        weighted_confidence = sum(
            safe_float(s.get("averageConfidence")) * safe_int(s.get("totalFrames"))
            for s in sessions
        )
        stats["doTinCayTrungBinh"] = weighted_confidence / total_confidence_frames

    if sessions:
        risks = [safe_float(session.get("riskIndex")) for session in sessions]
        highest_risk = max(risks, default=0.0)
        stats["highestRiskIndex"] = highest_risk
        stats["averageRiskIndex"] = sum(risks) / len(risks)
        stats["highestRiskLevel"] = temporal_risk.risk_level(highest_risk)

    return stats


def get_daily_trend(
    db_path: str | Path = DEFAULT_DB,
    limit: int = 7,
) -> list[dict[str, Any]]:
    path = resolve_db_path(db_path)
    if not path.exists():
        raise FileNotFoundError(f"Database not found: {path}")

    with sqlite3.connect(path) as connection:
        connection.row_factory = sqlite3.Row
        if not table_exists(connection, "ThongKeNgay"):
            return []
        rows = connection.execute(
            """
            SELECT
                ngay,
                tongSoPhien,
                tongThoiGianLamViec,
                tongThoiGianDung,
                tongThoiGianSai,
                tongSoCanhBao,
                tiLeDung,
                tiLeSai
            FROM ThongKeNgay
            ORDER BY ngay DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    trend = []
    for row in reversed(rows):
        item = dict(row)
        total_work = safe_float(item.get("tongThoiGianLamViec"))
        item["tiLeDung"] = safe_ratio(safe_float(item.get("tongThoiGianDung")), total_work)
        item["tiLeSai"] = safe_ratio(safe_float(item.get("tongThoiGianSai")), total_work)
        trend.append(item)
    return trend


def get_dashboard_data(
    db_path: str | Path = DEFAULT_DB,
    date_text: str | None = None,
) -> dict[str, Any]:
    path = resolve_db_path(db_path)
    if date_text is None:
        date_text = datetime.now().date().isoformat()

    sessions = get_session_statistics(path, date_text)
    return {
        "date": date_text,
        "available_dates": list_available_dates(path),
        "stats": get_daily_statistics(path, date_text, sessions),
        "sessions": sessions,
        "trend": get_daily_trend(path, limit=7),
    }
