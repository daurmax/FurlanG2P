"""Null implementation of IExceptionModel for base installs without ML dependencies."""

from __future__ import annotations

from furlan_g2p.ml.interfaces import ExceptionPrediction, IExceptionModel


class NullExceptionModel(IExceptionModel):
    """
    Default exception model when ML dependencies are not installed.

    This implementation always returns None for predictions, allowing the
    G2P pipeline to function without optional ML dependencies. It serves as
    a graceful fallback when the [ml] extra is not installed.

    Examples:
        >>> model = NullExceptionModel()
        >>> model.is_available()
        False
        >>> model.predict("furlan")
        None
        >>> model.get_model_info()
        {'name': 'null', 'available': False}
    """

    def predict(self, word: str, dialect: str | None = None) -> ExceptionPrediction | None:
        """
        Always return None (no prediction available).

        Args:
            word: Orthographic word (ignored).
            dialect: Dialect identifier (ignored).

        Returns:
            None (model not available).
        """
        return None

    def predict_batch(
        self, words: list[str], dialect: str | None = None
    ) -> list[ExceptionPrediction | None]:
        """
        Return list of None values matching input length.

        Args:
            words: List of orthographic words.
            dialect: Dialect identifier (ignored).

        Returns:
            List of None values (no predictions available).
        """
        return [None] * len(words)

    def is_available(self) -> bool:
        """
        Return False (null model never available for predictions).

        Returns:
            False
        """
        return False

    def get_model_info(self) -> dict[str, str | bool | int]:
        """
        Return metadata indicating null model.

        Returns:
            Dictionary with name='null' and available=False.
        """
        return {"name": "null", "available": False}


__all__ = ["NullExceptionModel"]
