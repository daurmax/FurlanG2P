from __future__ import annotations

import builtins
import importlib

import pytest

from furlan_g2p.ml import (
    ML_AVAILABLE,
    ExceptionPrediction,
    NullExceptionModel,
    require_ml,
)


def test_null_exception_model_returns_none_predictions() -> None:
    model = NullExceptionModel()
    assert model.predict("cjase") is None
    assert model.predict("cjase", dialect="central") is None
    assert model.predict_batch(["cjase", "aghe"]) == [None, None]


def test_null_exception_model_availability_and_info() -> None:
    model = NullExceptionModel()
    assert model.is_available() is False
    assert model.get_model_info() == {"name": "null", "available": False}


def test_exception_prediction_dataclass_contract() -> None:
    prediction = ExceptionPrediction(
        ipa="ˈfuɾlan",
        confidence=0.95,
        source="model-v1",
        alternatives=[("fuɾˈlan", 0.05)],
    )

    assert prediction.ipa == "ˈfuɾlan"
    assert prediction.confidence == pytest.approx(0.95)
    assert prediction.source == "model-v1"
    assert prediction.alternatives == [("fuɾˈlan", 0.05)]


def test_ml_available_flag_and_require_ml_behavior() -> None:
    assert isinstance(ML_AVAILABLE, bool)
    if ML_AVAILABLE:
        require_ml()
    else:
        with pytest.raises(ImportError, match="ML dependencies not installed"):
            require_ml()


def test_module_import_without_optional_ml_dependencies(monkeypatch: pytest.MonkeyPatch) -> None:
    module = importlib.import_module("furlan_g2p.ml")
    original_import = builtins.__import__

    def fake_import(
        name: str,
        globals_: dict[str, object] | None = None,
        locals_: dict[str, object] | None = None,
        fromlist: tuple[str, ...] | None = None,
        level: int = 0,
    ) -> object:
        if name in {"torch", "transformers"}:
            raise ImportError(f"forced missing dependency: {name}")
        return original_import(name, globals_, locals_, fromlist, level)

    with monkeypatch.context() as patch_ctx:
        patch_ctx.setattr(builtins, "__import__", fake_import)
        reloaded = importlib.reload(module)
        assert reloaded.ML_AVAILABLE is False
        with pytest.raises(ImportError, match="ML dependencies not installed"):
            reloaded.require_ml()

    importlib.reload(module)
