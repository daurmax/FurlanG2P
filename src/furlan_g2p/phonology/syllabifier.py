"""Syllabification helpers."""

from __future__ import annotations

from collections.abc import Iterable

from ..core.interfaces import ISyllabifier


def _is_vowel(ph: str) -> bool:
    return ph[0] in "aeiou"


class Syllabifier(ISyllabifier):
    """Naive syllabifier.

    Each vowel starts a new syllable and trailing consonants are attached to
    the preceding vowel.  This is intentionally simplistic but sufficient for
    demonstration purposes.

    Examples
    --------
    >>> Syllabifier().syllabify(['c', 'a', 'z', 'e'])
    [['c', 'a'], ['z', 'e']]
    """

    def syllabify(self, phonemes: Iterable[str]) -> list[list[str]]:
        """Split a phoneme sequence into syllables."""

        syllables: list[list[str]] = []
        current: list[str] = []
        for ph in phonemes:
            current.append(ph)
            if _is_vowel(ph):
                syllables.append(current)
                current = []
        if current:
            syllables.append(current)
        return syllables


__all__ = ["Syllabifier"]
