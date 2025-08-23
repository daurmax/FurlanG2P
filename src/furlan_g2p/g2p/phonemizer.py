"""Grapheme-to-phoneme conversion utilities (skeleton)."""

from __future__ import annotations

from collections.abc import Iterable

from ..core.interfaces import IG2PPhonemizer
from .lexicon import Lexicon
from .rules import PhonemeRules


class G2PPhonemizer(IG2PPhonemizer):
    """Phonemizer that combines a lexicon and LTS rules (skeleton)."""

    def __init__(self, lexicon: Lexicon | None = None, rules: PhonemeRules | None = None) -> None:
        self.lexicon = lexicon or Lexicon()
        self.rules = rules or PhonemeRules()

    def to_phonemes(self, tokens: Iterable[str]) -> list[str]:
        """Convert token strings into a flat list of phoneme symbols."""
        raise NotImplementedError("Phonemization is not implemented yet.")


__all__ = ["G2PPhonemizer"]
