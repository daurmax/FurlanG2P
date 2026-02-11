"""WikiPron TSV parsing utilities."""

from __future__ import annotations

import csv
import logging
import re
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

_DIALECT_ALIASES: dict[str, str] = {
    "central": "central",
    "cent": "central",
    "western": "western",
    "west": "western",
    "carnic": "carnic",
    "carn": "carnic",
}


@dataclass(frozen=True)
class WikiPronEntry:
    """Parsed WikiPron record."""

    lemma: str
    ipa: str
    language_code: str | None = None
    dialect: str | None = None


def _dialect_from_language_code(
    language_code: str | None,
    default_dialect: str | None = None,
) -> str | None:
    if not language_code:
        return default_dialect
    code = language_code.strip().lower()
    if not code:
        return default_dialect
    if not code.startswith("fur"):
        return default_dialect
    tokens = re.split(r"[-_]", code)
    for token in tokens[1:]:
        if token in _DIALECT_ALIASES:
            return _DIALECT_ALIASES[token]
    for key, value in _DIALECT_ALIASES.items():
        if key in code:
            return value
    return default_dialect


def iter_wikipron_entries(
    path: Path,
    default_dialect: str | None = None,
) -> Iterator[WikiPronEntry]:
    """Iterate WikiPron entries from a TSV file.

    Parameters
    ----------
    path:
        Path to the WikiPron TSV file.
    default_dialect:
        Dialect to use when the language code does not specify one.

    Yields
    ------
    WikiPronEntry
        Parsed entry records.

    Examples
    --------
    >>> path = Path("wikipron.tsv")
    >>> isinstance(next(iter_wikipron_entries(path)), WikiPronEntry)
    True
    """

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        for line_num, row in enumerate(reader, start=1):
            if not row or all(not cell.strip() for cell in row):
                continue
            if line_num == 1 and row[0].strip().lower() in {"word", "lemma"}:
                continue
            if len(row) < 2:
                logger.warning(
                    "WikiPron line %s: expected 2 columns, got %s",
                    line_num,
                    len(row),
                )
                continue
            lemma = row[0].strip()
            ipa = row[1].strip()
            if not lemma or not ipa:
                logger.warning("WikiPron line %s: empty lemma or ipa, skipping", line_num)
                continue
            language_code = row[2].strip() if len(row) >= 3 and row[2].strip() else None
            dialect = _dialect_from_language_code(language_code, default_dialect)
            yield WikiPronEntry(
                lemma=lemma,
                ipa=ipa,
                language_code=language_code,
                dialect=dialect,
            )


__all__ = ["WikiPronEntry", "iter_wikipron_entries"]
