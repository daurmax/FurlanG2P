"""Evaluation infrastructure for G2P metrics (WER, PER, stress accuracy)."""

from __future__ import annotations

from furlan_g2p.evaluation.metrics import Evaluator
from furlan_g2p.evaluation.types import EvaluationResult, WordResult

__all__ = [
    "Evaluator",
    "EvaluationResult",
    "WordResult",
]
