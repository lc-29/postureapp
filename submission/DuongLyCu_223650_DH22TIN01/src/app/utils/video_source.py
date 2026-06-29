"""Video source and path helpers used by the desktop runtime."""

from __future__ import annotations

from pathlib import Path

try:
    from app.config.constants import BASE_DIR
except ImportError:
    from src.app.config.constants import BASE_DIR

try:
    from runtime_paths import resource_path
except ImportError:
    from src.runtime_paths import resource_path


def project_path_from_text(path_text: str | None, fallback: Path) -> Path:
    """Convert a database path into an absolute project/resource path."""
    if not path_text:
        return fallback

    path = Path(path_text)
    if path.is_absolute():
        return path

    return resource_path(path)


def resolve_source(source_text: str) -> tuple[int | str, str]:
    """Classify webcam, IP camera, or video file source for OpenCV."""
    source = str(source_text).strip()
    if source == "":
        source = "0"

    if source.isdigit():
        return int(source), "webcam"

    lower_source = source.lower()
    if lower_source.startswith(("http://", "https://", "rtsp://")):
        return source, "ip_camera"

    source_path = Path(source)
    project_source_path = BASE_DIR / source_path
    if source_path.exists():
        return source, "video_file"

    if not source_path.is_absolute() and project_source_path.exists():
        return str(project_source_path), "video_file"

    return source, "video_file"


def infer_view_angle_from_source(source_text: str, source_type: str) -> str:
    """Infer camera view from the video filename when available."""
    if source_type != "video_file":
        return "unknown"

    source_name = Path(str(source_text).lower()).name
    if "side_90" in source_name:
        return "side_90"
    if "side_30" in source_name:
        return "side_30"
    if "front" in source_name:
        return "front"
    return "unknown"

