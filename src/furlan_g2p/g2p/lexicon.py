"""In-memory lexicon utilities (skeleton)."""

from __future__ import annotations


class Lexicon:
    """In-memory lexicon for word -> phoneme sequence (space-separated string)."""

    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    def get(self, word: str) -> str | None:
        """Retrieve the phoneme sequence for ``word``."""
        raise NotImplementedError("Lexicon lookup is not implemented yet.")

    def add(self, word: str, phonemes: str) -> None:
        """Add a phoneme sequence for ``word``."""
        raise NotImplementedError("Lexicon updates are not implemented yet.")


__all__ = ["Lexicon"]
