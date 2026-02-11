"""Core metric functions for G2P evaluation."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from furlan_g2p.core.interfaces import IEvaluator
from furlan_g2p.evaluation.types import EvaluationResult, WordResult


def _normalize_ipa(ipa: str) -> str:
    """Normalize IPA for comparison.

    - Normalize Unicode to NFC
    - Strip whitespace and common punctuation
    - Canonicalize common variants (g→ɡ, tie bars)

    Args:
        ipa: Raw IPA string

    Returns:
        Normalized IPA string
    """
    # Normalize Unicode composition
    normalized = unicodedata.normalize("NFC", ipa)

    # Strip spaces, commas, periods, etc.
    normalized = re.sub(r"[\s.,;:!?]+", "", normalized)

    # Canonicalize Latin g to IPA ɡ (U+0261)
    normalized = normalized.replace("g", "ɡ")

    # Remove tie bars (often optional in IPA)
    normalized = normalized.replace("\u0361", "")  # Combining double inverted breve

    return normalized


def _tokenize_phonemes(ipa: str) -> list[str]:
    """Split IPA into phoneme tokens.

    Handles:
    - Diacritics (combining characters)
    - Affricates (single phoneme with modifiers)
    - Stress markers as separate tokens

    Args:
        ipa: IPA string (should be normalized first)

    Returns:
        List of phoneme tokens
    """
    phonemes: list[str] = []
    i = 0
    ipa_len = len(ipa)

    while i < ipa_len:
        char = ipa[i]

        # Start building a phoneme token
        token = char
        i += 1

        # Collect any combining diacritics
        while i < ipa_len and unicodedata.category(ipa[i]) in ("Mn", "Mc", "Me"):
            token += ipa[i]
            i += 1

        phonemes.append(token)

    return phonemes


def _levenshtein_distance(seq1: list[str], seq2: list[str]) -> int:
    """Compute Levenshtein edit distance between two sequences.

    Args:
        seq1: First sequence of tokens
        seq2: Second sequence of tokens

    Returns:
        Minimum edit distance (insertions, deletions, substitutions)
    """
    m, n = len(seq1), len(seq2)

    # Initialize DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1] == seq2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],  # deletion
                    dp[i][j - 1],  # insertion
                    dp[i - 1][j - 1],  # substitution
                )

    return dp[m][n]


def _extract_stress_position(ipa: str) -> int | None:
    """Extract position of primary stress marker in IPA string.

    Args:
        ipa: IPA string (normalized)

    Returns:
        Index of stress marker (ˈ), or None if not found
    """
    stress_marker = "ˈ"  # U+02C8 PRIMARY STRESS
    idx = ipa.find(stress_marker)
    return idx if idx >= 0 else None


class Evaluator(IEvaluator):
    """Standard G2P evaluation metrics implementation."""

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

        Raises:
            ValueError: If predictions and gold have different lengths
        """
        if len(predictions) != len(gold):
            raise ValueError(
                f"Length mismatch: {len(predictions)} predictions vs {len(gold)} gold"
            )

        if len(predictions) == 0:
            return EvaluationResult(
                wer=0.0,
                per=0.0,
                stress_accuracy=0.0,
                word_count=0,
                correct_count=0,
                details=[],
            )

        details: list[WordResult] = []
        correct_count = 0
        total_phoneme_distance = 0.0
        total_gold_phonemes = 0
        stress_matches = 0
        stress_comparable = 0

        for (word_pred, ipa_pred), (word_gold, ipa_gold) in zip(predictions, gold):
            # Normalize IPA
            norm_pred = _normalize_ipa(ipa_pred)
            norm_gold = _normalize_ipa(ipa_gold)

            # Check exact match
            is_correct = norm_pred == norm_gold
            if is_correct:
                correct_count += 1

            # Compute phoneme distance
            phonemes_pred = _tokenize_phonemes(norm_pred)
            phonemes_gold = _tokenize_phonemes(norm_gold)

            distance = _levenshtein_distance(phonemes_pred, phonemes_gold)
            total_phoneme_distance += distance
            total_gold_phonemes += len(phonemes_gold)

            # Check stress accuracy
            stress_pred = _extract_stress_position(norm_pred)
            stress_gold = _extract_stress_position(norm_gold)

            if stress_gold is not None:
                stress_comparable += 1
                if stress_pred == stress_gold:
                    stress_matches += 1

            details.append(
                WordResult(
                    word=word_pred,
                    predicted=ipa_pred,
                    gold=ipa_gold,
                    is_correct=is_correct,
                    phoneme_distance=float(distance),
                )
            )

        # Calculate aggregate metrics
        word_count = len(predictions)
        wer = 1.0 - (correct_count / word_count)
        per = total_phoneme_distance / total_gold_phonemes if total_gold_phonemes > 0 else 0.0
        stress_accuracy = stress_matches / stress_comparable if stress_comparable > 0 else 0.0

        return EvaluationResult(
            wer=wer,
            per=per,
            stress_accuracy=stress_accuracy,
            word_count=word_count,
            correct_count=correct_count,
            details=details,
        )

    def word_error_rate(self, predictions: list[str], gold: list[str]) -> float:
        """Compute word error rate only.

        Args:
            predictions: List of predicted IPA strings
            gold: List of gold IPA strings

        Returns:
            WER in range [0.0, 1.0]

        Raises:
            ValueError: If predictions and gold have different lengths
        """
        if len(predictions) != len(gold):
            raise ValueError(
                f"Length mismatch: {len(predictions)} predictions vs {len(gold)} gold"
            )

        if len(predictions) == 0:
            return 0.0

        correct_count = sum(
            1
            for pred, gld in zip(predictions, gold)
            if _normalize_ipa(pred) == _normalize_ipa(gld)
        )

        return 1.0 - (correct_count / len(predictions))

    def phoneme_error_rate(self, predictions: list[str], gold: list[str]) -> float:
        """Compute phoneme error rate only.

        Args:
            predictions: List of predicted IPA strings
            gold: List of gold IPA strings

        Returns:
            PER in range [0.0, ∞) - can exceed 1.0 for heavy insertions

        Raises:
            ValueError: If predictions and gold have different lengths
        """
        if len(predictions) != len(gold):
            raise ValueError(
                f"Length mismatch: {len(predictions)} predictions vs {len(gold)} gold"
            )

        if len(predictions) == 0:
            return 0.0

        total_distance = 0
        total_gold_phonemes = 0

        for pred, gld in zip(predictions, gold):
            norm_pred = _normalize_ipa(pred)
            norm_gold = _normalize_ipa(gld)

            phonemes_pred = _tokenize_phonemes(norm_pred)
            phonemes_gold = _tokenize_phonemes(norm_gold)

            total_distance += _levenshtein_distance(phonemes_pred, phonemes_gold)
            total_gold_phonemes += len(phonemes_gold)

        return total_distance / total_gold_phonemes if total_gold_phonemes > 0 else 0.0

    def stress_accuracy(self, predictions: list[str], gold: list[str]) -> float:
        """Compute stress marker position accuracy only.

        Args:
            predictions: List of predicted IPA strings
            gold: List of gold IPA strings

        Returns:
            Stress accuracy in range [0.0, 1.0]

        Raises:
            ValueError: If predictions and gold have different lengths
        """
        if len(predictions) != len(gold):
            raise ValueError(
                f"Length mismatch: {len(predictions)} predictions vs {len(gold)} gold"
            )

        if len(predictions) == 0:
            return 0.0

        stress_matches = 0
        stress_comparable = 0

        for pred, gld in zip(predictions, gold):
            norm_pred = _normalize_ipa(pred)
            norm_gold = _normalize_ipa(gld)

            stress_pred = _extract_stress_position(norm_pred)
            stress_gold = _extract_stress_position(norm_gold)

            if stress_gold is not None:
                stress_comparable += 1
                if stress_pred == stress_gold:
                    stress_matches += 1

        return stress_matches / stress_comparable if stress_comparable > 0 else 0.0

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

        Raises:
            FileNotFoundError: If TSV file not found
            ValueError: If TSV format is invalid
        """
        if not tsv_path.exists():
            raise FileNotFoundError(f"TSV file not found: {tsv_path}")

        gold_list: list[tuple[str, str]] = []
        pred_list: list[tuple[str, str]] = []

        with tsv_path.open("r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split("\t")
                if len(parts) < 2:
                    raise ValueError(f"Invalid TSV format at line {line_num}: {line}")

                word = parts[0]
                ipa = parts[1]
                dialect = parts[2] if len(parts) > 2 else None

                # Apply dialect filter
                if dialect_filter is not None and dialect != dialect_filter:
                    continue

                # Skip if no prediction available
                if word not in predictions:
                    continue

                gold_list.append((word, ipa))
                pred_list.append((word, predictions[word]))

        return self.evaluate(pred_list, gold_list)


__all__ = [
    "Evaluator",
]
