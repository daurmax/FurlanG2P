"""Abstract base interfaces for ML-based exception models."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ExceptionPrediction:
    """
    Result type for ML-based exception model predictions.

    Represents a predicted IPA transcription with confidence score and optional alternatives.
    Used when ML models predict pronunciations for words not in the lexicon or to override
    rule-based outputs.

    Attributes:
        ipa: Predicted IPA transcription with stress markers.
        confidence: Model confidence score in range [0.0, 1.0].
        source: Identifier of the model that produced this prediction.
        alternatives: Optional N-best list of alternative predictions with their confidences.

    Examples:
        >>> pred = ExceptionPrediction(
        ...     ipa="ˈfuɾlan",
        ...     confidence=0.95,
        ...     source="bert-g2p-v1",
        ...     alternatives=[("fuɾˈlan", 0.03), ("ˈfuɾlɐn", 0.02)]
        ... )
        >>> pred.confidence
        0.95
    """

    ipa: str
    confidence: float
    source: str
    alternatives: list[tuple[str, float]] = field(default_factory=list)


class IExceptionModel(ABC):
    """
    Interface for ML-based exception models in the G2P pipeline.

    Exception models provide predictions for words that:
    - Are not found in the lexicon
    - Require special handling beyond rule-based conversion
    - Need reranking or correction of rule-based outputs

    Pipeline Integration:
    - Called after lexicon lookup fails
    - Called after rules produce output (for reranking/correction)
    - Prediction used if confidence exceeds configured threshold

    Implementations must handle:
    - Lazy loading of model weights
    - Graceful degradation when models unavailable
    - Optional dialect-specific predictions

    Examples:
        >>> model: IExceptionModel = NullExceptionModel()
        >>> model.is_available()
        False
        >>> model.predict("graçie")
        None
    """

    @abstractmethod
    def predict(self, word: str, dialect: str | None = None) -> ExceptionPrediction | None:
        """
        Predict IPA transcription for a single word.

        Args:
            word: Orthographic word to transcribe.
            dialect: Optional dialect identifier for dialect-aware predictions.

        Returns:
            ExceptionPrediction if model is confident, None otherwise.

        Notes:
            Return None when:
            - Model confidence below threshold
            - Word outside model's domain
            - Model not available

        Examples:
            >>> model.predict("furlan")
            ExceptionPrediction(ipa="ˈfuɾlan", confidence=0.95, source="model-v1")
            >>> model.predict("xyz123")  # Low confidence
            None
        """
        raise NotImplementedError

    @abstractmethod
    def predict_batch(
        self, words: list[str], dialect: str | None = None
    ) -> list[ExceptionPrediction | None]:
        """
        Predict IPA transcriptions for multiple words (batch processing).

        Args:
            words: List of orthographic words to transcribe.
            dialect: Optional dialect identifier for dialect-aware predictions.

        Returns:
            List of predictions (same length as input), None for low-confidence predictions.

        Notes:
            Batch processing can be significantly more efficient than individual predictions
            for models that support batching (e.g., transformer-based models).

        Examples:
            >>> model.predict_batch(["cjase", "graçie"])
            [ExceptionPrediction(...), ExceptionPrediction(...)]
        """
        raise NotImplementedError

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if model is loaded and ready for predictions.

        Returns:
            True if model is available, False otherwise.

        Notes:
            Returns False when:
            - Model weights not loaded
            - Required dependencies missing
            - Model initialization failed

        Examples:
            >>> model.is_available()
            True
        """
        raise NotImplementedError

    @abstractmethod
    def get_model_info(self) -> dict[str, str | bool | int]:
        """
        Return model metadata.

        Returns:
            Dictionary with model information including:
            - name: Model identifier
            - version: Model version
            - available: Whether model is ready
            - Additional implementation-specific fields

        Examples:
            >>> model.get_model_info()
            {'name': 'bert-g2p', 'version': '1.0', 'available': True}
        """
        raise NotImplementedError


__all__ = [
    "ExceptionPrediction",
    "IExceptionModel",
]
