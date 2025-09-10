"""Text normalization utilities (skeleton)."""

from __future__ import annotations

import re
import unicodedata
from typing import Final

from ..config.schemas import NormalizerConfig
from ..core.exceptions import NormalizationError  # noqa: F401
from ..core.interfaces import INormalizer

_APOSTROPHES_RE: Final = re.compile("[\u2019\u2018\u02bc]")

# Default Friulian cardinals used if no override is provided.
_DEFAULT_NUMBERS: Final[dict[str, str]] = {
    "0": "zero",
    "1": "un",
    "2": "doi",
    "3": "trê",
    "4": "cuatri",
    "5": "cinc",
    "6": "sîs",
    "7": "siet",
    "8": "vot",
    "9": "nûf",
    "10": "dîs",
}


class Normalizer(INormalizer):
    """Simple text normalizer with basic expansion rules.

    The normalizer lowercases text, converts curly apostrophes to straight ones,
    maps punctuation to pause markers and replaces numbers, abbreviations,
    acronyms and units according to :class:`NormalizerConfig`.

    Examples
    --------
    >>> Normalizer().normalize("10 kg, Sig.")
    'dîs chilogram _ siôr'
    """

    def __init__(self, config: NormalizerConfig | None = None) -> None:
        self.config = config or NormalizerConfig()
        self._numbers_map = {**_DEFAULT_NUMBERS, **self.config.numbers_map}

    def _replace_token(self, token: str) -> str:
        token = self.config.abbreviations_map.get(token, token)
        token = self.config.acronyms_map.get(token, token)
        token = self.config.units_map.get(token, token)
        token = self._numbers_map.get(token, token)
        token = self.config.ordinal_map.get(token, token)
        return token

    def normalize(self, text: str) -> str:
        """Normalize raw input text into a canonical, speakable form.

        Parameters
        ----------
        text:
            Raw input text.

        Returns
        -------
        str
            Normalized text.

        Raises
        ------
        NormalizationError
            If the text cannot be normalized.
        """

        if not isinstance(text, str):  # pragma: no cover - defensive programming
            raise NormalizationError("Input must be a string")

        s = unicodedata.normalize("NFC", text)
        s = _APOSTROPHES_RE.sub("'", s)
        s = re.sub(r"[,;:]", f" {self.config.pause_short} ", s)
        s = re.sub(r"[.?!]", f" {self.config.pause_long} ", s)
        tokens = [t for t in re.split(r"\s+", s.strip()) if t]
        out_tokens: list[str] = []
        for raw in tokens:
            token = raw.lower()
            if token in {self.config.pause_short, self.config.pause_long}:
                out_tokens.append(token)
                continue
            out_tokens.append(self._replace_token(token))
        return " ".join(out_tokens)


__all__ = ["Normalizer"]
