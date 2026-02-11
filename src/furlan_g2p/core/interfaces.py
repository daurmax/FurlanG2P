"""Abstract base interfaces for FurlanG2P components."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from furlan_g2p.evaluation.types import EvaluationResult
    from furlan_g2p.lexicon.builder import ValidationIssue
    from furlan_g2p.lexicon.schema import LexiconEntry


class INormalizer(ABC):
    """Interface for text normalization."""

    @abstractmethod
    def normalize(self, text: str) -> str:
        """Return a normalized text string."""
        raise NotImplementedError


class ITokenizer(ABC):
    """Interface for sentence/word tokenization."""

    @abstractmethod
    def split_sentences(self, text: str) -> list[str]:
        """Split text into sentences."""
        raise NotImplementedError

    @abstractmethod
    def split_words(self, sentence: str) -> list[str]:
        """Split a sentence into tokens/words (keeping pause markers if any)."""
        raise NotImplementedError


class IG2PPhonemizer(ABC):
    """Interface for grapheme-to-phoneme conversion."""

    @abstractmethod
    def to_phonemes(self, tokens: Iterable[str], dialect: str | None = None) -> list[str]:
        """Map tokens to a flat sequence of phoneme symbols."""
        raise NotImplementedError


class ISyllabifier(ABC):
    """Interface for syllabification."""

    @abstractmethod
    def syllabify(self, phonemes: Iterable[str]) -> list[list[str]]:
        """Return a list of syllables, each as a list of phoneme strings."""
        raise NotImplementedError


class IStressAssigner(ABC):
    """Interface for lexical or post-lexical stress assignment."""

    @abstractmethod
    def assign_stress(self, syllables: list[list[str]]) -> list[list[str]]:
        """Return syllables with stress markers applied."""
        raise NotImplementedError


class IEvaluator(ABC):
    """Interface for G2P evaluation metrics."""

    @abstractmethod
    def evaluate(
        self,
        predictions: list[tuple[str, str]],
        gold: list[tuple[str, str]],
    ) -> EvaluationResult:
        """Compute all metrics (WER, PER, stress accuracy).

        Args:
            predictions: List of (word, predicted_ipa) tuples
            gold: List of (word, gold_ipa) tuples

        Returns:
            EvaluationResult with aggregate metrics and per-word details
        """
        raise NotImplementedError

    @abstractmethod
    def word_error_rate(self, predictions: list[str], gold: list[str]) -> float:
        """Compute word error rate only.

        Args:
            predictions: List of predicted IPA strings
            gold: List of gold IPA strings

        Returns:
            WER in range [0.0, 1.0]
        """
        raise NotImplementedError

    @abstractmethod
    def phoneme_error_rate(self, predictions: list[str], gold: list[str]) -> float:
        """Compute phoneme error rate only.

        Args:
            predictions: List of predicted IPA strings
            gold: List of gold IPA strings

        Returns:
            PER in range [0.0, ∞)
        """
        raise NotImplementedError

    @abstractmethod
    def stress_accuracy(self, predictions: list[str], gold: list[str]) -> float:
        """Compute stress marker position accuracy only.

        Args:
            predictions: List of predicted IPA strings
            gold: List of gold IPA strings

        Returns:
            Stress accuracy in range [0.0, 1.0]
        """
        raise NotImplementedError

    @abstractmethod
    def evaluate_from_tsv(
        self,
        tsv_path: Path,
        predictions: dict[str, str],
        dialect_filter: str | None = None,
    ) -> EvaluationResult:
        """Evaluate against a gold set TSV file.

        Args:
            tsv_path: Path to TSV file (word\\tipa or word\\tipa\\tdialect)
            predictions: Dictionary mapping words to predicted IPA
            dialect_filter: Optional dialect code to filter by

        Returns:
            EvaluationResult with metrics
        """
        raise NotImplementedError


class ILexiconBuilder(ABC):
    """Interface for lexicon ingestion and validation."""

    @abstractmethod
    def add_source(self, path: Path, source_type: str, dialect: str | None = None) -> int:
        """Add entries from a file-based source.

        Args:
            path: Path to the input file.
            source_type: Source identifier (e.g., "wikipron", "tsv").
            dialect: Optional dialect override.

        Returns:
            Number of entries ingested.
        """
        raise NotImplementedError

    @abstractmethod
    def add_entry(self, entry: LexiconEntry) -> bool:
        """Add a single lexicon entry.

        Args:
            entry: LexiconEntry instance.

        Returns:
            True if the entry was accepted.
        """
        raise NotImplementedError

    @abstractmethod
    def merge_entry(self, entry: LexiconEntry) -> None:
        """Merge a single entry into the lexicon."""
        raise NotImplementedError

    @abstractmethod
    def build(self) -> list[LexiconEntry]:
        """Return the final list of lexicon entries."""
        raise NotImplementedError

    @abstractmethod
    def validate(self) -> list[ValidationIssue]:
        """Validate entries and return issues."""
        raise NotImplementedError


__all__ = [
    "INormalizer",
    "ITokenizer",
    "IG2PPhonemizer",
    "ISyllabifier",
    "IStressAssigner",
    "IEvaluator",
    "ILexiconBuilder",
]
