"""Stress assignment helpers (skeleton)."""

from __future__ import annotations

from ..core.interfaces import IStressAssigner


class StressAssigner(IStressAssigner):
    """Stress assignment (skeleton)."""

    def assign_stress(self, syllables: list[list[str]]) -> list[list[str]]:
        """Apply stress markers to ``syllables``."""
        raise NotImplementedError("Stress assignment is not implemented yet.")


__all__ = ["StressAssigner"]
