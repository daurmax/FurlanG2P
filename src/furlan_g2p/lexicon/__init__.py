"""Lexicon schema and storage for the Furlan G2P system."""

from __future__ import annotations

from .schema import LexiconConfig, LexiconEntry
from .storage import detect_format, read_jsonl, read_tsv, write_jsonl, write_tsv

__all__ = [
    "LexiconEntry",
    "LexiconConfig",
    "read_tsv",
    "write_tsv",
    "read_jsonl",
    "write_jsonl",
    "detect_format",
]
