"""High-level pipeline service (skeleton)."""

from __future__ import annotations

from ..g2p.phonemizer import G2PPhonemizer
from ..normalization.normalizer import Normalizer
from ..phonology.stress import StressAssigner
from ..phonology.syllabifier import Syllabifier
from ..tokenization.tokenizer import Tokenizer


class PipelineService:
    """Orchestrates normalization -> tokenization -> G2P -> phonology."""

    def __init__(self) -> None:
        self.normalizer = Normalizer()
        self.tokenizer = Tokenizer()
        self.phonemizer = G2PPhonemizer()
        self.syllabifier = Syllabifier()
        self.stress = StressAssigner()

    def process_text(self, text: str) -> tuple[str, list[str]]:
        """Return ``(normalized_text, phoneme_sequence_as_list)``."""
        raise NotImplementedError("Pipeline processing is not implemented yet.")

    def process_csv(self, input_csv_path: str, output_csv_path: str, delimiter: str = "|") -> None:
        """Phonemize an LJSpeech-like metadata CSV file."""
        raise NotImplementedError("CSV batch processing is not implemented yet.")


__all__ = ["PipelineService"]
