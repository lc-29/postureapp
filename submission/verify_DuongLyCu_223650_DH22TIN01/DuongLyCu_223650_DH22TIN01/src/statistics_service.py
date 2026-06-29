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


def table_columns(connection: sqlite3.Connection, table_name: str) -> set[str]:
    rows = connection.execute(f'PRAGMA table_info("{table_name}")').fetchall()
    return {str(row[1]) for row in rows}


def _has_global_day_unique_index(connection: sqlite3.Connection) -> bool:
    """Detect the old ThongKeNgay schema where ngay was globally unique."""
    for index_row in connection.execute('PRAGMA index_list("ThongKeNgay")').fetchall():
        is_unique = int(index_row[2]) == 1
        if not is_unique:
            continue
        index_name = str(index_row[1])
        index_columns = [
            str(row[2])
            for row in connection.execute(f'PRAGMA index_info("{index_name}")').fetchall()
        ]
        if index_columns == ["ngay"]:
            return True
    return False


def create_user_scoped_daily_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS ThongKeNgay (
            maThongKe INTEGER PRIMARY KEY AUTOINCREMENT,
            maNguoiDung INTEGER NOT NULL,
            ngay TEXT NOT NULL,
            tongSoPhien INTEGER DEFAULT 0,
            tongThoiGianLamViec REAL DEFAULT 0,
            tongThoiGianDung REAL DEFAULT 0,
            tongThoiGianSai REAL DEFAULT 0,
            tongSoCanhBao INTEGER DEFAULT 0,
            tiLeDung REAL DEFAULT 0,
            tiLeSai REAL DEFAULT 0,
            ngayCapNhat TEXT NOT NULL,
            UNIQUE (maNguoiDung, ngay),
            FOREIGN KEY (maNguoiDung)
                REFERENCES NguoiDung(maNguoiDung)
                ON DELETE CASCADE
        )
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_thongke_ngay
        ON ThongKeNgay(ngay)
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_thongke_user_ngay
        ON ThongKeNgay(maNguoiDung, ngay)
        """
    )


def _default_user_id(connection: sqlite3.Connection) -> int | None:
    row = connection.execute(
        """
        SELECT maNguoiDung
        FROM NguoiDung
        WHERE tenDangNhap = 'Admin'
        ORDER BY maNguoiDung ASC
        LIMIT 1
        """
    ).fetchone()
    if row is not None:
        return int(row[0])
    row = connection.execute(
        "SELECT maNguoiDung FROM NguoiDung ORDER BY maNguoiDung ASC LIMIT 1"
    ).fetchone()
    return int(row[0]) if row is not None else None


def _rebuild_daily_stats_from_sessions(connection: sqlite3.Connection) -> None:
    if not table_exists(connection, "PhienLamViec"):
        return
    connection.execute(
        """
        INSERT OR REPLACE INTO ThongKeNgay (
            maNguoiDung,
            ngay,
            tongSoPhien,
            tongThoiGianLamViec,
            tongThoiGianDung,
            tongThoiGianSai,
            tongSoCanhBao,
            tiLeDung,
            tiLeSai,
            ngayCapNhat
        )
        SELECT
            maNguoiDung,
            substr(thoiGianBatDau, 1, 10) AS ngay,
            COUNT(*) AS tongSoPhien,
            SUM(
                CASE
                    WHEN thoiGianKetThuc IS NOT NULL
                        AND thoiGianKetThuc != ''
                        AND thoiGianBatDau IS NOT NULL
                        AND thoiGianBatDau != ''
                    THEN max(
                        0,
                        (julianday(thoiGianKetThuc) - julianday(thoiGianBatDau)) * 86400.0
                    )
                    ELSE COALESCE(tongThoiGianDung, 0) + COALESCE(tongThoiGianSai, 0)
                END
            ) AS tongThoiGianLamViec,
            SUM(COALESCE(tongThoiGianDung, 0)) AS tongThoiGianDung,
            SUM(COALESCE(tongThoiGianSai, 0)) AS tongThoiGianSai,
            SUM(COALESCE(soLanCanhBao, 0)) AS tongSoCanhBao,
            CASE
                WHEN SUM(
                    CASE
                        WHEN thoiGianKetThuc IS NOT NULL
                            AND thoiGianKetThuc != ''
                            AND thoiGianBatDau IS NOT NULL
                            AND thoiGianBatDau != ''
                        THEN max(
                            0,
                            (julianday(thoiGianKetThuc) - julianday(thoiGianBatDau)) * 86400.0
                        )
                        ELSE COALESCE(tongThoiGianDung, 0) + COALESCE(tongThoiGianSai, 0)
                    END
                ) > 0
                THEN SUM(COALESCE(tongThoiGianDung, 0)) / SUM(
                    CASE
                        WHEN thoiGianKetThuc IS NOT NULL
                            AND thoiGianKetThuc != ''
                            AND thoiGianBatDau IS NOT NULL
                            AND thoiGianBatDau != ''
                        THEN max(
                            0,
                            (julianday(thoiGianKetThuc) - julianday(thoiGianBatDau)) * 86400.0
                        )
                        ELSE COALESCE(tongThoiGianDung, 0) + COALESCE(tongThoiGianSai, 0)
                    END
                )
                ELSE 0
            END AS tiLeDung,
            CASE
                WHEN SUM(
                    CASE
                        WHEN thoiGianKetThuc IS NOT NULL
                            AND thoiGianKetThuc != ''
                            AND thoiGianBatDau IS NOT NULL
                            AND thoiGianBatDau != ''
                        THEN max(
                            0,
                            (julianday(thoiGianKetThuc) - julianday(thoiGianBatDau)) * 86400.0
                        )
                        ELSE COALESCE(tongThoiGianDung, 0) + COALESCE(tongThoiGianSai, 0)
                    END
                ) > 0
                THEN SUM(COALESCE(tongThoiGianSai, 0)) / SUM(
                    CASE
                        WHEN thoiGianKetThuc IS NOT NULL
                            AND thoiGianKetThuc != ''
                            AND thoiGianBatDau IS NOT NULL
                            AND thoiGianBatDau != ''
                        THEN max(
                            0,
                            (julianday(thoiGianKetThuc) - julianday(thoiGianBatDau)) * 86400.0
                        )
                        ELSE COALESCE(tongThoiGianDung, 0) + COALESCE(tongThoiGianSai, 0)
                    END
                )
                ELSE 0
            END AS tiLeSai,
            max(COALESCE(thoiGianKetThuc, thoiGianBatDau, datetime('now'))) AS ngayCapNhat
        FROM PhienLamViec
        WHERE maNguoiDung IS NOT NULL
            AND thoiGianBatDau IS NOT NULL
            AND thoiGianBatDau != ''
        GROUP BY maNguoiDung, substr(thoiGianBatDau, 1, 10)
        """
    )


def ensure_user_scoped_statistics_schema(connection: sqlite3.Connection) -> None:
    """Migrate daily statistics from global-by-day to per-user-by-day."""
    if not table_exists(connection, "ThongKeNgay"):
        create_user_scoped_daily_table(connection)
        connection.commit()
        return

    columns = table_columns(connection, "ThongKeNgay")
    needs_migration = "maNguoiDung" not in columns or _has_global_day_unique_index(connection)
    if not needs_migration:
        create_user_scoped_daily_table(connection)
        connection.commit()
        return

    legacy_table = "ThongKeNgay_legacy_user_scope"
    connection.execute(f'DROP TABLE IF EXISTS "{legacy_table}"')
    connection.execute(f'ALTER TABLE ThongKeNgay RENAME TO "{legacy_table}"')
    create_user_scoped_daily_table(connection)

    default_user_id = _default_user_id(connection)
    if default_user_id is not None:
        connection.execute(
            f"""
            INSERT OR IGNORE INTO ThongKeNgay (
                maNguoiDung,
                ngay,
                tongSoPhien,
                tongThoiGianLamViec,
                tongThoiGianDung,
                tongThoiGianSai,
                tongSoCanhBao,
                tiLeDung,
                tiLeSai,
                ngayCapNhat
            )
            SELECT
                ?,
                ngay,
                tongSoPhien,
                tongThoiGianLamViec,
                tongThoiGianDung,
                tongThoiGianSai,
                tongSoCanhBao,
                tiLeDung,
                tiLeSai,
                ngayCapNhat
            FROM "{legacy_table}"
            WHERE ngay IS NOT NULL
            """,
            (default_user_id,),
        )

    _rebuild_daily_stats_from_sessions(connection)
    connection.execute(f'DROP TABLE IF EXISTS "{legacy_table}"')
    connection.commit()


def list_available_dates(
    db_path: str | Path = DEFAULT_DB,
    user_id: int | None = None,
) -> list[str]:
    path = resolve_db_path(db_path)
    if not path.exists():
        return []

    with sqlite3.connect(path) as connection:
        ensure_user_scoped_statistics_schema(connection)
        dates: set[str] = set()
        if table_exists(connection, "ThongKeNgay"):
            if user_id is None:
                daily_rows = connection.execute(
                    "SELECT ngay FROM ThongKeNgay WHERE ngay IS NOT NULL"
                ).fetchall()
            else:
                daily_rows = connection.execute(
                    """
                    SELECT ngay
                    FROM ThongKeNgay
                    WHERE ngay IS NOT NULL AND maNguoiDung = ?
                    """,
                    (user_id,),
                ).fetchall()
            dates.update(
                str(row[0])
                for row in daily_rows
            )
        if table_exists(connection, "PhienLamViec"):
            if user_id is None:
                session_rows = connection.execute(
                    """
                    SELECT thoiGianBatDau
                    FROM PhienLamViec
                    WHERE thoiGianBatDau IS NOT NULL AND thoiGianBatDau != ''
                    """
                ).fetchall()
            else:
                session_rows = connection.execute(
                    """
                    SELECT thoiGianBatDau
                    FROM PhienLamViec
                    WHERE thoiGianBatDau IS NOT NULL
                        AND thoiGianBatDau != ''
                        AND maNguoiDung = ?
                    """,
                    (user_id,),
                ).fetchall()
            dates.update(
                str(row[0])[:10]
                for row in session_rows
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
    user_id: int | None = None,
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
        user_filter = ""
        params: list[Any] = [date_text + "%"]
        if user_id is not None:
            user_filter = "AND maNguoiDung = ?"
            params.append(user_id)
        rows = connection.execute(
            f"""
            SELECT
                maPhien,
                maNguoiDung,
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
                {user_filter}
            ORDER BY thoiGianBatDau ASC
            """,
            params,
        ).fetchall()

    return [enrich_session(dict(row)) for row in rows]


def get_daily_statistics(
    db_path: str | Path = DEFAULT_DB,
    date_text: str | None = None,
    sessions: list[dict[str, Any]] | None = None,
    user_id: int | None = None,
) -> dict[str, Any]:
    path = resolve_db_path(db_path)
    if not path.exists():
        raise FileNotFoundError(f"Database not found: {path}")

    if date_text is None:
        date_text = datetime.now().date().isoformat()

    stats = empty_daily_stats(date_text)
    with sqlite3.connect(path) as connection:
        connection.row_factory = sqlite3.Row
        ensure_user_scoped_statistics_schema(connection)
        if table_exists(connection, "ThongKeNgay"):
            if user_id is None:
                sql = """
                    SELECT
                        ngay,
                        SUM(tongSoPhien) AS tongSoPhien,
                        SUM(tongThoiGianLamViec) AS tongThoiGianLamViec,
                        SUM(tongThoiGianDung) AS tongThoiGianDung,
                        SUM(tongThoiGianSai) AS tongThoiGianSai,
                        SUM(tongSoCanhBao) AS tongSoCanhBao,
                        0 AS tiLeDung,
                        0 AS tiLeSai
                    FROM ThongKeNgay
                    WHERE ngay = ?
                    GROUP BY ngay
                """
                params: tuple[Any, ...] = (date_text,)
            else:
                sql = """
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
                    WHERE ngay = ? AND maNguoiDung = ?
                """
                params = (date_text, user_id)
            row = connection.execute(
                sql,
                params,
            ).fetchone()
            if row is not None:
                stats.update(dict(row))

    if sessions is None:
        sessions = get_session_statistics(path, date_text, user_id=user_id)

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
    user_id: int | None = None,
) -> list[dict[str, Any]]:
    path = resolve_db_path(db_path)
    if not path.exists():
        raise FileNotFoundError(f"Database not found: {path}")

    with sqlite3.connect(path) as connection:
        connection.row_factory = sqlite3.Row
        ensure_user_scoped_statistics_schema(connection)
        if not table_exists(connection, "ThongKeNgay"):
            return []
        if user_id is None:
            rows = connection.execute(
                """
                SELECT
                    ngay,
                    SUM(tongSoPhien) AS tongSoPhien,
                    SUM(tongThoiGianLamViec) AS tongThoiGianLamViec,
                    SUM(tongThoiGianDung) AS tongThoiGianDung,
                    SUM(tongThoiGianSai) AS tongThoiGianSai,
                    SUM(tongSoCanhBao) AS tongSoCanhBao,
                    0 AS tiLeDung,
                    0 AS tiLeSai
                FROM ThongKeNgay
                GROUP BY ngay
                ORDER BY ngay DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        else:
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
                WHERE maNguoiDung = ?
                ORDER BY ngay DESC
                LIMIT ?
                """,
                (user_id, limit),
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
    user_id: int | None = None,
) -> dict[str, Any]:
    path = resolve_db_path(db_path)
    if date_text is None:
        date_text = datetime.now().date().isoformat()

    sessions = get_session_statistics(path, date_text, user_id=user_id)
    return {
        "date": date_text,
        "available_dates": list_available_dates(path, user_id=user_id),
        "stats": get_daily_statistics(path, date_text, sessions, user_id=user_id),
        "sessions": sessions,
        "trend": get_daily_trend(path, limit=7, user_id=user_id),
    }
