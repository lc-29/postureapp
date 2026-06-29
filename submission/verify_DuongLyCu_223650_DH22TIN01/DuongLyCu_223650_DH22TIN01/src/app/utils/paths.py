"""Path helper adapter for app-layer imports."""

from __future__ import annotations

try:
    from runtime_paths import (
        app_base_dir,
        ensure_runtime_database,
        is_frozen,
        resource_path,
        writable_database_path,
    )
except ImportError:
    from src.runtime_paths import (
        app_base_dir,
        ensure_runtime_database,
        is_frozen,
        resource_path,
        writable_database_path,
    )

__all__ = [
    "app_base_dir",
    "ensure_runtime_database",
    "is_frozen",
    "resource_path",
    "writable_database_path",
]

