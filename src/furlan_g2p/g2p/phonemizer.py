"""Grapheme-to-phoneme conversion utilities."""

from __future__ import annotations

import logging
from collections.abc import Iterable

from ..core.interfaces import IG2PPhonemizer
from ..lexicon.lookup import DialectAwareLexicon
from ..lexicon.schema import LexiconEntry as SchemaLexiconEntry
from .lexicon import Lexicon
from .rules import PhonemeRules

logger = logging.getLogger(__name__)


def _segment_ipa(ipa: str) -> list[str]:
    """Split a canonical IPA string into phoneme symbols."""

    digraphs = ["tʃ", "dʒ", "dz", "ts"]
    segments: list[str] = []
    i = 0
    while i < len(ipa):
        for digraph in digraphs:
            if ipa.startswith(digraph, i):
                segments.append(digraph)
                i += len(digraph)
                break
        else:
            segments.append(ipa[i])
            i += 1
    return segments


class G2PPhonemizer(IG2PPhonemizer):
    """Phonemizer that combines a lexicon and rule fallback.

    Examples
    --------
    >>> G2PPhonemizer().to_phonemes(["cjase"])
    ['c', 'a', 'z', 'e']
    """

    def __init__(
        self,
        lexicon: Lexicon | DialectAwareLexicon | None = None,
        rules: PhonemeRules | None = None,
    ) -> None:
        self.lexicon = lexicon or Lexicon()
        self.rules = rules or PhonemeRules()

    def to_phonemes(self, tokens: Iterable[str], dialect: str | None = None) -> list[str]:
        """Convert token strings into a flat list of phoneme symbols.

        Parameters
        ----------
        tokens:
            Tokens to phonemize.
        dialect:
            Optional dialect code for lexicon/rule selection.
        """

        phonemes: list[str] = []
        for token in tokens:
            entry = self._lookup_entry(token, dialect=dialect)
            if entry is not None:
                if dialect is not None and entry.dialect is None:
                    logger.info(
                        "Dialect-specific lexicon entry missing for token=%r dialect=%r; "
                        "used universal entry",
                        token,
                        dialect,
                    )
                ipa = entry.ipa.replace("ˈ", "").replace("ˌ", "")
                phonemes.extend(_segment_ipa(ipa))
                continue
            phonemes.extend(self.rules.apply(token, dialect=dialect))
        return phonemes

    def _lookup_entry(self, token: str, dialect: str | None) -> SchemaLexiconEntry | None:
        if isinstance(self.lexicon, DialectAwareLexicon):
            return self.lexicon.lookup(token, dialect=dialect)
        return self.lexicon.lookup(token, dialect=dialect)


__all__ = ["G2PPhonemizer"]
