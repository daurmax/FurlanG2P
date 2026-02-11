"""Lexicon schema and storage for the Furlan G2P system."""

from __future__ import annotations

from .builder import LexiconBuilder, ValidationIssue
from .canonicalizer import IPACanonicalize, load_ipa_mapping
from .lookup import DialectAwareLexicon
from .schema import LexiconConfig, LexiconEntry
from .storage import detect_format, read_jsonl, read_tsv, write_jsonl, write_tsv
from .wikipron import WikiPronEntry, iter_wikipron_entries

__all__ = [
    "DialectAwareLexicon",
    "IPACanonicalize",
    "LexiconBuilder",
    "LexiconEntry",
    "LexiconConfig",
    "ValidationIssue",
    "read_tsv",
    "write_tsv",
    "read_jsonl",
    "write_jsonl",
    "detect_format",
    "load_ipa_mapping",
    "WikiPronEntry",
    "iter_wikipron_entries",
]
