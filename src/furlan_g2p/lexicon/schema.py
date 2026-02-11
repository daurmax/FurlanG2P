"""Data models for lexicon entries and configuration."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Final

# Valid IPA characters - includes common IPA symbols, diacritics, and stress marks
_IPA_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[a-zɑɐɒæɓʙβɔɕçɗɖðʤʣʥʤʨʦʧɚɝɛɞɤəɘɜɡɢɣɠʛħɦɧʜɪɨɩʝɟʄɭɬɫɮɰmɱɯɲnɳŋɴɵɸɹɾʁɻrʀʂʃtʈθʧʉʊʋⱱʌɣwɯxχʏyzʐʑʒʔʡʕʢˈˌːˑ̪̺̻̼̯̩̰̝̞̟̠̤̥̬̆̚˞\s]+$",
    re.IGNORECASE,
)

# Valid dialect codes
_VALID_DIALECTS: Final[set[str]] = {"central", "western", "carnic"}


@dataclass(frozen=True)
class LexiconEntry:
    """A single lexicon entry with dialect and source information.

    Parameters
    ----------
    lemma : str
        Word form.
    ipa : str
        Primary IPA pronunciation.
    dialect : str | None
        Dialect code ("central", "western", "carnic") or None for universal entries.
    source : str
        Origin identifier (e.g., "seed", "wikipron", "manual", "cof").
    confidence : float
        Confidence score in range [0.0, 1.0].
    frequency : int | None
        Corpus frequency rank (None if unknown).
    alternatives : list[str]
        Alternative pronunciations (empty list by default).

    Attributes
    ----------
    stress_marked : bool
        Whether the primary IPA contains stress markers (ˈ or ˌ).

    Examples
    --------
    >>> entry = LexiconEntry(
    ...     lemma="cjase",
    ...     ipa="ˈcaze",
    ...     dialect=None,
    ...     source="seed",
    ...     confidence=1.0,
    ...     frequency=None,
    ...     alternatives=[],
    ... )
    >>> entry.stress_marked
    True
    """

    lemma: str
    ipa: str
    dialect: str | None = None
    source: str = "unknown"
    confidence: float = 1.0
    frequency: int | None = None
    alternatives: list[str] = field(default_factory=list)

    @property
    def stress_marked(self) -> bool:
        """Check if the primary IPA contains stress markers."""
        return "ˈ" in self.ipa or "ˌ" in self.ipa

    def __post_init__(self) -> None:
        """Validate field values."""
        # Validate required fields
        if not self.lemma:
            raise ValueError("lemma cannot be empty")
        if not self.ipa:
            raise ValueError("ipa cannot be empty")

        # Validate confidence range
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"confidence must be in [0.0, 1.0], got {self.confidence}")

        # Validate dialect code
        if self.dialect is not None and self.dialect not in _VALID_DIALECTS:
            raise ValueError(
                f"Invalid dialect '{self.dialect}'. "
                f"Valid dialects: {', '.join(sorted(_VALID_DIALECTS))}"
            )

        # Validate frequency (if provided)
        if self.frequency is not None and self.frequency < 0:
            raise ValueError(f"frequency must be non-negative, got {self.frequency}")

        # Convert alternatives to list if needed (for frozen dataclass compatibility)
        if not isinstance(self.alternatives, list):
            object.__setattr__(self, "alternatives", list(self.alternatives))


@dataclass(slots=True)
class LexiconConfig:
    """Configuration for lexicon lookup behavior.

    Parameters
    ----------
    default_dialect : str | None
        Default dialect for lookups. If None, no dialect preference is set.
    fallback_to_universal : bool
        If True, fall back to universal entries (dialect=None) when a
        dialect-specific entry is not found.
    case_sensitive : bool
        If True, perform case-sensitive lookups.
    return_alternatives : bool
        If True, include alternative pronunciations in lookup results.

    Examples
    --------
    >>> config = LexiconConfig(default_dialect="central", fallback_to_universal=True)
    >>> config.default_dialect
    'central'
    >>> config.case_sensitive
    False
    """

    default_dialect: str | None = None
    fallback_to_universal: bool = True
    case_sensitive: bool = False
    return_alternatives: bool = False

    def __post_init__(self) -> None:
        """Validate configuration values."""
        if self.default_dialect is not None and self.default_dialect not in _VALID_DIALECTS:
            raise ValueError(
                f"Invalid default_dialect '{self.default_dialect}'. "
                f"Valid dialects: {', '.join(sorted(_VALID_DIALECTS))}"
            )


__all__ = ["LexiconEntry", "LexiconConfig"]
