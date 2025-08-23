"""Text normalization utilities (skeleton)."""

from __future__ import annotations

from ..config.schemas import NormalizerConfig
from ..core.exceptions import NormalizationError  # noqa: F401
from ..core.interfaces import INormalizer


class Normalizer(INormalizer):
    """Text normalizer (skeleton)."""

    def __init__(self, config: NormalizerConfig | None = None) -> None:
        self.config = config or NormalizerConfig()

    def normalize(self, text: str) -> str:
        """Normalize raw input text into a canonical, speakable form.

        Args:
            text: Raw input text.

        Raises:
            NormalizationError: If the text cannot be normalized.
        """
        raise NotImplementedError("Normalization logic is not implemented yet.")


__all__ = ["Normalizer"]
