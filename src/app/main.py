"""New package entrypoint for the desktop app.

The large legacy module remains the stable runtime entrypoint during the
incremental refactor. This wrapper lets the app also be started with
`python -m app.main` when `src` is on PYTHONPATH.
"""

from __future__ import annotations

from importlib import import_module


def main() -> None:
    legacy_app = import_module("4_main_desktop_app")
    legacy_app.main()


if __name__ == "__main__":
    main()

