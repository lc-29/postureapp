"""Export SQLite app statistics to CSV files for reports/demo."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DB = BASE_DIR / "database" / "posture_app.db"
DEFAULT_OUTPUT_DIR = BASE_DIR / "reports" / "results"

EXPORTS = {
    "PhienLamViec": "session_statistics.csv",
    "ThongKeNgay": "daily_statistics.csv",
    "NhatKyTuThe": "posture_log_statistics.csv",
}


def table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
    cursor = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,),
    )
    return cursor.fetchone() is not None


def export_statistics(args: argparse.Namespace) -> None:
    db_path = Path(args.database)
    output_dir = Path(args.output_dir)
    if not db_path.is_absolute():
        db_path = BASE_DIR / db_path
    if not output_dir.is_absolute():
        output_dir = BASE_DIR / output_dir

    if not db_path.exists():
        raise FileNotFoundError(
            f"Database not found: {db_path}. Run: python src/3_database_setup.py"
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as connection:
        for table_name, file_name in EXPORTS.items():
            output_path = output_dir / file_name
            if not table_exists(connection, table_name):
                output_path.write_text("", encoding="utf-8")
                print(f"Missing table {table_name}; wrote empty file: {output_path}")
                continue

            df = pd.read_sql_query(f"SELECT * FROM {table_name}", connection)
            df.to_csv(output_path, index=False, encoding="utf-8-sig")
            print(f"Exported {len(df)} rows from {table_name} to {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export SQLite statistics to CSV.")
    parser.add_argument("--database", default=str(DEFAULT_DB))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    return parser.parse_args()


if __name__ == "__main__":
    export_statistics(parse_args())
