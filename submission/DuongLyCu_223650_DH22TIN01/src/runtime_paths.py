"""Runtime path helpers for development and PyInstaller builds."""

from __future__ import annotations

import importlib.util
import os
import shutil
import sys
from pathlib import Path
from typing import Any


APP_NAME = "PostureDetectionApp"
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def is_frozen() -> bool:
    """Return True when the app is running from a frozen executable."""
    return bool(getattr(sys, "frozen", False))


def executable_dir() -> Path:
    """Directory containing the executable in frozen mode, else project root."""
    if is_frozen():
        return Path(sys.executable).resolve().parent
    return PROJECT_ROOT


def bundle_dir() -> Path:
    """Directory where PyInstaller exposes bundled data files."""
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        return Path(meipass).resolve()
    return executable_dir()


def app_base_dir() -> Path:
    """Base directory for source/resources in development or frozen runtime."""
    return executable_dir() if is_frozen() else PROJECT_ROOT


def user_data_dir() -> Path:
    """Writable per-user app data directory."""
    override = os.environ.get("POSTURE_APP_USER_DATA_DIR")
    if override:
        return Path(override).expanduser().resolve()

    if os.name == "nt":
        root = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        return Path(root) / APP_NAME

    return Path.home() / ".local" / "share" / APP_NAME


def resource_path(relative_path: str | Path) -> Path:
    """
    Resolve a bundled resource path.

    Candidate order supports development, PyInstaller one-dir `_internal`, and
    resources copied next to the executable.
    """
    relative = Path(relative_path)
    if relative.is_absolute():
        return relative

    candidates = [
        bundle_dir() / relative,
        executable_dir() / relative,
        PROJECT_ROOT / relative,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    return candidates[0]


def writable_database_path() -> Path:
    """
    Return the SQLite path the app should write to.

    Development keeps the existing project database. Frozen builds use a
    per-user writable location to avoid Program Files/read-only issues.
    """
    override = os.environ.get("POSTURE_APP_DB")
    if override:
        return Path(override).expanduser().resolve()

    if is_frozen():
        return user_data_dir() / "posture_app.db"

    return PROJECT_ROOT / "database" / "posture_app.db"


def _load_database_setup_module() -> Any:
    setup_path = resource_path(Path("src") / "3_database_setup.py")
    if not setup_path.exists():
        setup_path = PROJECT_ROOT / "src" / "3_database_setup.py"
    if not setup_path.exists():
        raise FileNotFoundError(f"Cannot locate database setup script: {setup_path}")

    module_name = "posture_database_setup_runtime"
    spec = importlib.util.spec_from_file_location(module_name, setup_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load database setup module: {setup_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def ensure_runtime_database() -> Path:
    """
    Ensure the runtime SQLite database exists and has the current schema.

    A frozen app creates a clean user database on first run. Development mode
    continues using `database/posture_app.db`.
    """
    db_path = writable_database_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    if not db_path.exists():
        seed_path = resource_path(Path("database") / "posture_app.db")
        if is_frozen() and seed_path.exists() and seed_path.resolve() != db_path.resolve():
            shutil.copy2(seed_path, db_path)
        else:
            database_setup = _load_database_setup_module()
            database_setup.init_database(reset=False, db_path=db_path)

    database_setup = _load_database_setup_module()
    with database_setup.create_connection(db_path) as connection:
        database_setup.create_tables(connection)
        database_setup.create_indexes(connection)
        database_setup.insert_default_data(connection)
        connection.commit()

    return db_path
