"""Load and run models from models/model_registry.json."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

try:
    from feature_schema import build_feature_matrix
except ImportError:
    from src.feature_schema import build_feature_matrix


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = BASE_DIR / "models" / "model_registry.json"


@dataclass
class RegistryModel:
    model_id: str
    feature_set: str
    threshold: float
    model: Any

    def predict_proba_incorrect(self, df: pd.DataFrame) -> np.ndarray:
        x, _ = build_feature_matrix(df, self.feature_set)
        if hasattr(self.model, "predict_proba"):
            return np.asarray(self.model.predict_proba(x))[:, 1]
        decision = np.asarray(self.model.decision_function(x))
        return 1.0 / (1.0 + np.exp(-decision))

    def predict_label(self, df: pd.DataFrame) -> np.ndarray:
        return (self.predict_proba_incorrect(df) >= self.threshold).astype(int)


def load_registry_model(registry_path: str | Path = DEFAULT_REGISTRY, model_id: str | None = None) -> RegistryModel:
    registry_path = Path(registry_path)
    if not registry_path.is_absolute():
        registry_path = BASE_DIR / registry_path
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    resolved_id = model_id or registry["selected_model_id"]
    entry = registry["entries"][resolved_id]
    model_path = BASE_DIR / entry["model_path"]
    threshold_path = BASE_DIR / entry["threshold_path"]
    threshold = 0.5
    if threshold_path.exists():
        threshold_payload = json.loads(threshold_path.read_text(encoding="utf-8"))
        threshold = float(threshold_payload.get("default", threshold))
    return RegistryModel(
        model_id=resolved_id,
        feature_set=entry["feature_set"],
        threshold=threshold,
        model=joblib.load(model_path),
    )

