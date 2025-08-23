"""Letter-to-sound rules engine (skeleton)."""

from __future__ import annotations

from collections.abc import Iterable


class PhonemeRules:
    """Letter-to-sound rules engine (skeleton)."""

    def __init__(self, phoneme_inventory: Iterable[str] | None = None) -> None:
        self._inventory = set(phoneme_inventory or ())

    def apply(self, word: str) -> list[str]:
        """Return a list of phoneme symbols for the given word."""
        raise NotImplementedError("LTS rules are not implemented yet.")


__all__ = ["PhonemeRules"]
