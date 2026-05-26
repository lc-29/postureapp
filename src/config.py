"""Cau hinh duong dan va tham so chung cua he thong."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = BASE_DIR / "assets"
SOUNDS_DIR = ASSETS_DIR / "sounds"
DATABASE_PATH = BASE_DIR / "database" / "posture_app.db"
DATASET_CSV_PATH = BASE_DIR / "dataset" / "posture_data.csv"
MODEL_PATH = BASE_DIR / "models" / "ann_best.keras"
SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"

CAMERA_INDEX = 0
WARNING_SECONDS = 5
WARNING_COOLDOWN_SECONDS = 15
