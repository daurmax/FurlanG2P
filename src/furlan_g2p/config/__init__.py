"""Config data structures and loading utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .schemas import NormalizerConfig

try:  # pragma: no cover - optional dependency
    import yaml  # type: ignore[import-untyped]
except Exception:  # pragma: no cover - optional dependency
    yaml = None


def load_normalizer_config(path: str | Path) -> NormalizerConfig:
    """Load a :class:`NormalizerConfig` from a JSON or YAML file.

    Parameters
    ----------
    path:
        Path to a configuration file.  Supported formats are JSON, ``.yml`` and
        ``.yaml``.  YAML loading requires the optional :mod:`pyyaml` dependency.

    Returns
    -------
    NormalizerConfig
        Parsed configuration dataclass.

    Raises
    ------
    ValueError
        If the file extension is not recognised.
    ImportError
        If a YAML file is provided but :mod:`pyyaml` is not installed.
    """

    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() == ".json":
        data: dict[str, Any] = json.loads(text)
    elif p.suffix.lower() in {".yml", ".yaml"}:
        if yaml is None:
            raise ImportError("pyyaml is required for YAML config files")
        data = yaml.safe_load(text)
    else:  # pragma: no cover - defensive
        raise ValueError(f"Unsupported config format: {p.suffix}")
    if not isinstance(data, dict):  # pragma: no cover - defensive
        raise TypeError("Configuration file must contain a mapping")
    return NormalizerConfig(**data)


__all__ = ["load_normalizer_config", "NormalizerConfig"]
