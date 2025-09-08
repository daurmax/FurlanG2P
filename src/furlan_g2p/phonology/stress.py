"""Stress assignment helpers (skeleton)."""

from __future__ import annotations

from ..core.interfaces import IStressAssigner


class StressAssigner(IStressAssigner):
    """Very small stress assignment helper.

    The algorithm simply marks the first syllable with a primary stress
    symbol.  It is not linguistically accurate but adequate for testing the
    pipeline plumbing.

    Examples
    --------
    >>> StressAssigner().assign_stress([['c', 'a'], ['z', 'e']])
    [['ˈc', 'a'], ['z', 'e']]
    """

    def assign_stress(self, syllables: list[list[str]]) -> list[list[str]]:
        """Apply stress markers to ``syllables``."""

        if not syllables:
            return []
        out = [list(s) for s in syllables]
        out[0][0] = "ˈ" + out[0][0]
        return out


__all__ = ["StressAssigner"]
