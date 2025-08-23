"""FurlanG2P public API."""

from __future__ import annotations

from importlib import metadata

from .core.interfaces import (
    IG2PPhonemizer,
    INormalizer,
    IStressAssigner,
    ISyllabifier,
    ITokenizer,
)
from .g2p.phonemizer import G2PPhonemizer
from .normalization.normalizer import Normalizer
from .phonology.stress import StressAssigner
from .phonology.syllabifier import Syllabifier
from .tokenization.tokenizer import Tokenizer

try:
    version = metadata.version("furlang2p")
except metadata.PackageNotFoundError:  # pragma: no cover
    version = "0.0.0"

__all__ = [
    "version",
    "INormalizer",
    "ITokenizer",
    "IG2PPhonemizer",
    "ISyllabifier",
    "IStressAssigner",
    "Normalizer",
    "Tokenizer",
    "G2PPhonemizer",
    "Syllabifier",
    "StressAssigner",
]
