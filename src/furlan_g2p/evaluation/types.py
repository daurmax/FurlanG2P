"""Type definitions for evaluation results."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class WordResult:
    """Per-word evaluation breakdown.

    Attributes:
        word: Original word (orthographic form)
        predicted: Predicted IPA transcription
        gold: Gold standard IPA transcription
        is_correct: Whether predicted exactly matches gold
        phoneme_distance: Levenshtein distance at phoneme level
    """

    word: str
    predicted: str
    gold: str
    is_correct: bool
    phoneme_distance: float


@dataclass
class EvaluationResult:
    """Aggregate evaluation metrics.

    Attributes:
        wer: Word error rate [0.0, 1.0]
        per: Phoneme error rate [0.0, ∞) - can exceed 1.0 for heavy insertions
        stress_accuracy: Stress marker position accuracy [0.0, 1.0]
        word_count: Total number of words evaluated
        correct_count: Number of words with exact match
        details: Optional per-word breakdown
    """

    wer: float
    per: float
    stress_accuracy: float
    word_count: int
    correct_count: int
    details: list[WordResult] = field(default_factory=list)


__all__ = [
    "WordResult",
    "EvaluationResult",
]
