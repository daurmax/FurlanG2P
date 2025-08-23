"""Sentence and word tokenization utilities (skeleton)."""

from __future__ import annotations

from ..config.schemas import TokenizerConfig
from ..core.interfaces import ITokenizer


class Tokenizer(ITokenizer):
    """Sentence and word tokenizer (skeleton)."""

    def __init__(self, config: TokenizerConfig | None = None) -> None:
        self.config = config or TokenizerConfig()

    def split_sentences(self, text: str) -> list[str]:
        """Split raw text into sentences."""
        raise NotImplementedError("Sentence splitting is not implemented yet.")

    def split_words(self, sentence: str) -> list[str]:
        """Split a sentence into tokens/words."""
        raise NotImplementedError("Word tokenization is not implemented yet.")


__all__ = ["Tokenizer"]
