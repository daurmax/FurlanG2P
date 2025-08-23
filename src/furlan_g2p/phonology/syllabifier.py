"""Syllabification helpers (skeleton)."""

from __future__ import annotations

from collections.abc import Iterable

from ..core.interfaces import ISyllabifier


class Syllabifier(ISyllabifier):
    """Syllabifier (skeleton)."""

    def syllabify(self, phonemes: Iterable[str]) -> list[list[str]]:
        """Split a phoneme sequence into syllables."""
        raise NotImplementedError("Syllabification is not implemented yet.")


__all__ = ["Syllabifier"]
