"""IPA canonicalization utilities for lexicon ingestion."""

from __future__ import annotations

import csv
import io
import json
import logging
import re
import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass, field
from importlib import resources
from pathlib import Path

from ..phonology import PHONEME_INVENTORY

logger = logging.getLogger(__name__)

try:  # pragma: no cover - optional dependency
    import yaml  # type: ignore[import-untyped]
except Exception:  # pragma: no cover - optional dependency
    yaml = None

_TIE_BARS = {"\u0361", "\u035C"}  # tie bar above / below
_MULTISPACE_RE = re.compile(r"\s+")


def _parse_tsv_text(text: str) -> dict[str, str]:
    mapping: dict[str, str] = {}
    reader = csv.reader(io.StringIO(text), delimiter="\t")
    for line_num, row in enumerate(reader, start=1):
        if not row or all(not cell.strip() for cell in row):
            continue
        first = row[0].strip()
        if first.startswith("#"):
            continue
        if line_num == 1 and first.lower() in {"source", "from", "src"}:
            continue
        if len(row) < 2:
            logger.warning(
                "Mapping line %s: expected 2 columns, got %s",
                line_num,
                len(row),
            )
            continue
        src = row[0].strip()
        tgt = row[1].strip()
        if not src:
            logger.warning("Mapping line %s: empty source symbol, skipping", line_num)
            continue
        mapping[src] = tgt
    return mapping


def load_ipa_mapping(path: str | Path) -> dict[str, str]:
    """Load an IPA mapping table from TSV/JSON/YAML.

    Parameters
    ----------
    path:
        Path to the mapping table.

    Returns
    -------
    dict[str, str]
        Mapping of source symbols to canonical targets.

    Examples
    --------
    >>> mapping = load_ipa_mapping("ipa_mapping.tsv")
    >>> isinstance(mapping, dict)
    True
    """

    p = Path(path)
    suffix = p.suffix.lower()
    if suffix in {".tsv", ".txt"}:
        text = p.read_text(encoding="utf-8-sig")
        return _parse_tsv_text(text)
    if suffix == ".json":
        data = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise TypeError("IPA mapping JSON must be a mapping")
        return {str(k): str(v) for k, v in data.items()}
    if suffix in {".yml", ".yaml"}:
        if yaml is None:
            raise ImportError("pyyaml is required for YAML IPA mapping files")
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise TypeError("IPA mapping YAML must be a mapping")
        return {str(k): str(v) for k, v in data.items()}
    raise ValueError(f"Unsupported IPA mapping format: {p.suffix}")


def _load_default_mapping() -> dict[str, str]:
    resource = resources.files("furlan_g2p.data").joinpath("ipa_mapping.tsv")
    text = resource.read_text(encoding="utf-8")
    return _parse_tsv_text(text)


@dataclass(slots=True)
class IPACanonicalize:
    """Canonicalize IPA strings and flag unknown symbols.

    Parameters
    ----------
    mapping_path:
        Optional path to a TSV/YAML/JSON mapping table. If None, the packaged
        default mapping is used.
    inventory:
        Iterable of canonical phoneme symbols for validation.

    Examples
    --------
    >>> canon = IPACanonicalize()
    >>> canon.canonicalize("t͡ʃ")
    'tʃ'
    >>> canon.get_unknown_symbols("t͡ʃ")
    set()
    """

    mapping_path: str | Path | None = None
    inventory: Iterable[str] | None = None
    _mapping: dict[str, str] = field(init=False, repr=False)
    _replacement_pairs: list[tuple[str, str]] = field(init=False, repr=False)
    _inventory: set[str] = field(init=False, repr=False)
    _multi_symbols: list[str] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._mapping = (
            load_ipa_mapping(self.mapping_path)
            if self.mapping_path is not None
            else _load_default_mapping()
        )
        self._replacement_pairs = sorted(
            self._mapping.items(), key=lambda item: len(item[0]), reverse=True
        )
        self._inventory = set(self.inventory or PHONEME_INVENTORY)
        self._multi_symbols = sorted(
            (sym for sym in self._inventory if len(sym) > 1),
            key=len,
            reverse=True,
        )

    def canonicalize(self, ipa: str) -> str:
        """Return a canonical representation of ``ipa``.

        Parameters
        ----------
        ipa:
            Raw IPA string.

        Returns
        -------
        str
            Canonicalized IPA string.
        """

        text = unicodedata.normalize("NFC", ipa.strip())
        if (text.startswith("/") and text.endswith("/")) or (
            text.startswith("[") and text.endswith("]")
        ):
            text = text[1:-1]
        text = text.replace(".", "")
        for tie_bar in _TIE_BARS:
            text = text.replace(tie_bar, "")
        for src, tgt in self._replacement_pairs:
            text = text.replace(src, tgt)
        text = _MULTISPACE_RE.sub(" ", text).strip()
        return text

    def get_unknown_symbols(self, ipa: str) -> set[str]:
        """Return unknown symbols after canonicalization.

        Parameters
        ----------
        ipa:
            IPA string to inspect.

        Returns
        -------
        set[str]
            Symbols not found in the inventory.
        """

        canonical = self.canonicalize(ipa)
        unknown: set[str] = set()
        for symbol in self._segment(canonical):
            if not symbol:
                continue
            if symbol in self._inventory:
                continue
            base = "".join(
                ch for ch in symbol if unicodedata.category(ch) != "Mn"
            )
            if base in self._inventory:
                continue
            unknown.add(symbol)
        return unknown

    def _segment(self, ipa: str) -> list[str]:
        segments: list[str] = []
        i = 0
        while i < len(ipa):
            ch = ipa[i]
            if ch.isspace():
                i += 1
                continue
            if unicodedata.category(ch) == "Mn":
                if segments:
                    segments[-1] += ch
                else:
                    segments.append(ch)
                i += 1
                continue
            matched = False
            for symbol in self._multi_symbols:
                if ipa.startswith(symbol, i):
                    segments.append(symbol)
                    i += len(symbol)
                    matched = True
                    break
            if matched:
                continue
            segments.append(ch)
            i += 1
        return segments


__all__ = ["IPACanonicalize", "load_ipa_mapping"]
