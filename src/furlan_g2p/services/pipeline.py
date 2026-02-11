"""High-level pipeline service."""

from __future__ import annotations

import csv

from ..g2p.lexicon import Lexicon
from ..g2p.phonemizer import G2PPhonemizer
from ..lexicon.schema import LexiconConfig
from ..normalization.normalizer import Normalizer
from ..phonology.stress import StressAssigner
from ..phonology.syllabifier import Syllabifier
from ..tokenization.tokenizer import Tokenizer


class PipelineService:
    """Orchestrates normalization -> tokenization -> G2P -> phonology.

    Parameters
    ----------
    default_dialect:
        Default dialect applied when requests do not provide one.
    lexicon_config:
        Lexicon lookup behavior configuration.
    phonemizer:
        Optional custom phonemizer instance.
    """

    def __init__(
        self,
        default_dialect: str | None = None,
        lexicon_config: LexiconConfig | None = None,
        phonemizer: G2PPhonemizer | None = None,
    ) -> None:
        self.lexicon_config = lexicon_config or LexiconConfig(default_dialect=default_dialect)
        self.default_dialect = default_dialect or self.lexicon_config.default_dialect

        self.normalizer = Normalizer()
        self.tokenizer = Tokenizer()
        self.phonemizer = phonemizer or G2PPhonemizer(lexicon=Lexicon(config=self.lexicon_config))
        self.syllabifier = Syllabifier()
        self.stress = StressAssigner()

    def process_text(
        self,
        text: str,
        dialect: str | None = None,
    ) -> tuple[str, list[str]]:
        """Return ``(normalized_text, phoneme_sequence_as_list)``.

        Examples
        --------
        >>> PipelineService().process_text("Cjase")
        ('cjase', ['ˈc', 'a', 'z', 'e'])
        """

        active_dialect = dialect or self.default_dialect

        norm = self.normalizer.normalize(text)
        sentences = self.tokenizer.split_sentences(norm)
        tokens: list[str] = []
        for sentence in sentences:
            tokens.extend(self.tokenizer.split_words(sentence))
        phonemes = self.phonemizer.to_phonemes(tokens, dialect=active_dialect)
        syllables = self.syllabifier.syllabify(phonemes)
        stressed = self.stress.assign_stress(syllables)
        flat = [phoneme for syllable in stressed for phoneme in syllable]
        return norm, flat

    def process_csv(
        self,
        input_csv_path: str,
        output_csv_path: str,
        delimiter: str = "|",
        dialect: str | None = None,
        dialect_column: int | None = None,
    ) -> None:
        """Phonemize an LJSpeech-like metadata CSV file.

        Parameters
        ----------
        input_csv_path:
            Input CSV path.
        output_csv_path:
            Output CSV path.
        delimiter:
            CSV delimiter.
        dialect:
            Optional fallback dialect applied to every row.
        dialect_column:
            Optional zero-based column index containing per-row dialect tags.
        """

        with (
            open(input_csv_path, encoding="utf-8") as src,
            open(output_csv_path, "w", encoding="utf-8", newline="") as dst,
        ):
            reader = csv.reader(src, delimiter=delimiter)
            writer = csv.writer(dst, delimiter=delimiter)
            for row in reader:
                if len(row) < 2:
                    continue

                row_dialect = dialect
                if (
                    dialect_column is not None
                    and dialect_column >= 0
                    and len(row) > dialect_column
                    and row[dialect_column].strip()
                ):
                    row_dialect = row[dialect_column].strip()

                norm, phonemes = self.process_text(row[1], dialect=row_dialect)
                writer.writerow([row[0], norm, " ".join(phonemes)])


__all__ = ["PipelineService"]
