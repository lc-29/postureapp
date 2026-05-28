"""Cau hinh duong dan va tham so chung cua he thong."""

from pathlib import Path

try:
    from runtime_paths import app_base_dir, resource_path, writable_database_path
except ImportError:
    from src.runtime_paths import app_base_dir, resource_path, writable_database_path

BASE_DIR = app_base_dir()
ASSETS_DIR = resource_path("assets")
SOUNDS_DIR = ASSETS_DIR / "sounds"
DATABASE_PATH = writable_database_path()
DATASET_CSV_PATH = BASE_DIR / "dataset" / "posture_data.csv"
MODEL_PATH = resource_path(Path("models") / "ann_best.keras")
SCALER_PATH = resource_path(Path("models") / "scaler.pkl")

CAMERA_INDEX = 0
WARNING_SECONDS = 5
WARNING_COOLDOWN_SECONDS = 15
