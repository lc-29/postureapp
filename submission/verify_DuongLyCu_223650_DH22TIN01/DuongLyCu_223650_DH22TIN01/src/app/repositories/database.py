"""SQLite connection helper for the app repository layer."""

from __future__ import annotations

import sqlite3

try:
    from runtime_paths import ensure_runtime_database
except ImportError:
    from src.runtime_paths import ensure_runtime_database


def get_db_connection() -> sqlite3.Connection:
    """Create a SQLite connection and enable foreign keys."""
    db_path = ensure_runtime_database()
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

