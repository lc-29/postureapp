import sqlite3
from pathlib import Path

from src.statistics_service import (
    get_daily_statistics,
    get_dashboard_data,
    get_session_statistics,
    list_available_dates,
)


def create_test_db(path: Path) -> None:
    connection = sqlite3.connect(path)
    try:
        connection.execute(
            """
            CREATE TABLE ThongKeNgay (
                ngay TEXT NOT NULL UNIQUE,
                tongSoPhien INTEGER DEFAULT 0,
                tongThoiGianLamViec REAL DEFAULT 0,
                tongThoiGianDung REAL DEFAULT 0,
                tongThoiGianSai REAL DEFAULT 0,
                tongSoCanhBao INTEGER DEFAULT 0,
                tiLeDung REAL DEFAULT 0,
                tiLeSai REAL DEFAULT 0,
                ngayCapNhat TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE PhienLamViec (
                maPhien INTEGER PRIMARY KEY AUTOINCREMENT,
                thoiGianBatDau TEXT NOT NULL,
                thoiGianKetThuc TEXT,
                loaiNguon TEXT,
                giaTriNguon TEXT,
                tongSoFrame INTEGER DEFAULT 0,
                soFrameDung INTEGER DEFAULT 0,
                soFrameSai INTEGER DEFAULT 0,
                soFrameKhongCoNguoi INTEGER DEFAULT 0,
                tongThoiGianDung REAL DEFAULT 0,
                tongThoiGianSai REAL DEFAULT 0,
                soLanCanhBao INTEGER DEFAULT 0,
                doTinCayTrungBinh REAL DEFAULT 0
            )
            """
        )
        connection.execute(
            """
            INSERT INTO ThongKeNgay (
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
            VALUES ('2026-05-27', 1, 100.0, 60.0, 30.0, 2, 0.6, 0.3, '2026-05-27T10:02:00')
            """
        )
        connection.execute(
            """
            INSERT INTO PhienLamViec (
                thoiGianBatDau,
                thoiGianKetThuc,
                loaiNguon,
                giaTriNguon,
                tongSoFrame,
                soFrameDung,
                soFrameSai,
                soFrameKhongCoNguoi,
                tongThoiGianDung,
                tongThoiGianSai,
                soLanCanhBao,
                doTinCayTrungBinh
            )
            VALUES (
                '2026-05-27T10:00:00',
                '2026-05-27T10:01:40',
                'webcam',
                '0',
                100,
                60,
                30,
                10,
                60.0,
                30.0,
                2,
                0.95
            )
            """
        )
        connection.commit()
    finally:
        connection.close()


def test_statistics_service_enriches_daily_and_session_data(tmp_path):
    db_path = tmp_path / "stats.db"
    create_test_db(db_path)

    sessions = get_session_statistics(db_path, "2026-05-27")
    assert len(sessions) == 1
    assert sessions[0]["durationSeconds"] == 100.0
    assert sessions[0]["correctRatio"] == 0.6
    assert sessions[0]["incorrectRatio"] == 0.3
    assert sessions[0]["noPersonRatio"] == 0.1
    assert sessions[0]["riskLevel"] in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}

    stats = get_daily_statistics(db_path, "2026-05-27", sessions)
    assert stats["tongSoPhien"] == 1
    assert stats["tiLeKhongXacDinh"] == 0.1
    assert stats["doTinCayTrungBinh"] == 0.95
    assert stats["highestRiskIndex"] == sessions[0]["riskIndex"]


def test_dashboard_data_lists_dates_and_trend(tmp_path):
    db_path = tmp_path / "stats.db"
    create_test_db(db_path)

    assert list_available_dates(db_path) == ["2026-05-27"]

    dashboard = get_dashboard_data(db_path, "2026-05-27")
    assert dashboard["date"] == "2026-05-27"
    assert dashboard["available_dates"] == ["2026-05-27"]
    assert len(dashboard["trend"]) == 1

