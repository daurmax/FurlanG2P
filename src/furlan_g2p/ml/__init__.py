"""
ML-based exception models for the G2P pipeline (optional).

This module provides interfaces and implementations for machine learning-based
exception models that can predict IPA transcriptions for words not in the lexicon
or refine rule-based outputs.

The module uses import guards to gracefully handle missing ML dependencies:
- Base install: Only NullExceptionModel available (always returns None)
- With [ml] extra: Full ML models available (requires torch, transformers)

Usage:
    >>> from furlan_g2p.ml import NullExceptionModel, ML_AVAILABLE
    >>> print(f"ML support: {ML_AVAILABLE}")
    ML support: False
    >>> model = NullExceptionModel()
    >>> model.predict("furlan")
    None

Installation:
    # Base install (no ML dependencies)
    pip install furlan-g2p

    # With ML support
    pip install furlan-g2p[ml]

Exports:
    ML_AVAILABLE: bool flag indicating if ML dependencies are installed
    ExceptionPrediction: dataclass for prediction results
    IExceptionModel: abstract interface for exception models
    NullExceptionModel: default implementation (no ML required)
"""

from __future__ import annotations

# Always available (no ML dependencies)
from furlan_g2p.ml.interfaces import ExceptionPrediction, IExceptionModel
from furlan_g2p.ml.null_model import NullExceptionModel

# Check for optional ML dependencies
ML_AVAILABLE = False
_ML_IMPORT_ERROR: str | None = None

try:
    import torch  # noqa: F401
    import transformers  # noqa: F401

    ML_AVAILABLE = True
except ImportError as e:
    _ML_IMPORT_ERROR = str(e)


def require_ml() -> None:
    """
    Raise ImportError with helpful message if ML dependencies are not installed.

    Raises:
        ImportError: If torch or transformers not available.

    Examples:
        >>> require_ml()  # doctest: +SKIP
        Traceback (most recent call last):
        ImportError: ML dependencies not installed. Install with: pip install furlan-g2p[ml]
    """
    if not ML_AVAILABLE:
        msg = (
            "ML dependencies not installed. "
            "Install with: pip install furlan-g2p[ml]\n"
            f"Original error: {_ML_IMPORT_ERROR}"
        )
        raise ImportError(msg)


__all__ = [
    "ML_AVAILABLE",
    "ExceptionPrediction",
    "IExceptionModel",
    "NullExceptionModel",
    "require_ml",
]
