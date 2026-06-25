from __future__ import annotations

from pathlib import Path

import pytest

from src.model_registry_service import load_registry_model


def test_load_registry_model_when_registry_exists() -> None:
    registry_path = Path("models/model_registry.json")
    if not registry_path.exists():
        pytest.skip("model registry has not been generated")
    model = load_registry_model(registry_path)
    assert model.model_id
    assert model.feature_set
    assert 0.0 <= model.threshold <= 1.0

