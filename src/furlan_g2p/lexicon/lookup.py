"""Dialect-aware lexicon lookup and loading helpers."""

from __future__ import annotations

import csv
import json
import logging
import unicodedata
from collections.abc import Iterable
from dataclasses import replace
from functools import lru_cache
from importlib import resources
from pathlib import Path

from ..phonology import canonicalize_ipa
from .schema import LexiconConfig, LexiconEntry
from .storage import detect_format, read_jsonl, read_tsv

logger = logging.getLogger(__name__)

_DIALECT_ALIASES: dict[str, str] = {
    "central": "central",
    "cent": "central",
    "western": "western",
    "west": "western",
    "western_codroipo": "western",
    "carnic": "carnic",
    "carn": "carnic",
    "carnia": "carnic",
}


def _canonical_word(word: str, case_sensitive: bool) -> str:
    """Return a normalized lookup key for ``word``."""

    normalized = unicodedata.normalize("NFC", word.strip())
    return normalized if case_sensitive else normalized.lower()


def _normalize_dialect(dialect: str | None) -> str | None:
    """Normalize dialect aliases to canonical schema codes."""

    if dialect is None:
        return None
    value = dialect.strip().lower()
    if not value:
        return None
    return _DIALECT_ALIASES.get(value, value)


class DialectAwareLexicon:
    """Read-only lexicon with dialect-aware lookup and universal fallback.

    Parameters
    ----------
    entries:
        Lexicon entries to index.
    config:
        Lookup behavior settings.

    Examples
    --------
    >>> from furlan_g2p.lexicon import LexiconConfig, LexiconEntry
    >>> lex = DialectAwareLexicon(
    ...     [
    ...         LexiconEntry(lemma="cjase", ipa="ˈcaze"),
    ...         LexiconEntry(lemma="cjase", ipa="ˈca:ze", dialect="western"),
    ...     ],
    ...     config=LexiconConfig(default_dialect="western"),
    ... )
    >>> lex.lookup_ipa("cjase")
    'ˈca:ze'
    """

    def __init__(
        self,
        entries: list[LexiconEntry],
        config: LexiconConfig | None = None,
    ) -> None:
        self.config = config or LexiconConfig()
        self._entries: dict[tuple[str, str | None], LexiconEntry] = {}
        self._entries_by_lemma: dict[str, list[LexiconEntry]] = {}

        for entry in entries:
            normalized = self._normalize_entry(entry)
            self._merge_entry(normalized)

        for (lemma_key, _dialect), entry in self._entries.items():
            self._entries_by_lemma.setdefault(lemma_key, []).append(entry)

    @classmethod
    def from_path(
        cls,
        path: str | Path,
        config: LexiconConfig | None = None,
    ) -> DialectAwareLexicon:
        """Load entries from TSV or JSONL and build a dialect-aware lexicon.

        Parameters
        ----------
        path:
            Input file path.
        config:
            Lookup configuration.

        Returns
        -------
        DialectAwareLexicon
            Instantiated lexicon.
        """

        file_path = Path(path)
        file_format = detect_format(file_path)
        if file_format == "jsonl":
            entries = read_jsonl(file_path)
        elif file_format == "tsv":
            entries = cls._read_tsv_with_compat(file_path)
        else:
            raise ValueError(f"Unsupported lexicon format: {file_path}")
        return cls(entries, config=config)

    @classmethod
    def load_seed(cls, config: LexiconConfig | None = None) -> DialectAwareLexicon:
        """Load the packaged seed lexicon as universal entries."""

        with (
            resources.files("furlan_g2p.data")
            .joinpath("seed_lexicon.tsv")
            .open("r", encoding="utf-8") as handle
        ):
            reader = csv.DictReader(handle, delimiter="\t")
            entries: list[LexiconEntry] = []
            for row in reader:
                lemma = row["word"].strip()
                ipa = canonicalize_ipa(row["ipa"].strip())
                raw_variants = json.loads(row.get("variants_json", "[]") or "[]")
                alternatives = [canonicalize_ipa(value) for value in raw_variants]
                source = row["source"].strip() or "seed"
                entries.append(
                    LexiconEntry(
                        lemma=lemma,
                        ipa=ipa,
                        dialect=None,
                        source=source,
                        alternatives=alternatives,
                    )
                )
        return cls(entries=entries, config=config)

    def lookup(self, word: str, dialect: str | None = None) -> LexiconEntry | None:
        """Return the best matching entry for ``word`` and optional ``dialect``."""

        normalized_word = _canonical_word(word, self.config.case_sensitive)
        if not normalized_word:
            return None
        normalized_dialect = _normalize_dialect(dialect)
        entry, used_fallback = self._lookup_cached(normalized_word, normalized_dialect)
        if used_fallback and normalized_dialect is not None:
            logger.info(
                "Lexicon fallback to universal entry for word=%r dialect=%r",
                word,
                normalized_dialect,
            )
        return entry

    def lookup_ipa(self, word: str, dialect: str | None = None) -> str | None:
        """Return the primary IPA for ``word`` and optional ``dialect``."""

        entry = self.lookup(word, dialect=dialect)
        return entry.ipa if entry is not None else None

    def get_alternatives(self, word: str, dialect: str | None = None) -> list[str]:
        """Return alternative pronunciations for ``word``."""

        entry = self.lookup(word, dialect=dialect)
        if entry is None:
            return []

        seen: set[str] = {entry.ipa}
        alternatives: list[str] = []

        for value in entry.alternatives:
            if value in seen:
                continue
            seen.add(value)
            alternatives.append(value)

        if self.config.return_alternatives:
            lemma_key = _canonical_word(word, self.config.case_sensitive)
            for candidate in self._entries_by_lemma.get(lemma_key, []):
                for value in [candidate.ipa, *candidate.alternatives]:
                    if value in seen:
                        continue
                    seen.add(value)
                    alternatives.append(value)

        return alternatives

    def has_entry(self, word: str, dialect: str | None = None) -> bool:
        """Return ``True`` if an entry exists for ``word``."""

        return self.lookup(word, dialect=dialect) is not None

    def stats(self) -> dict[str, object]:
        """Return basic lexicon statistics."""

        by_dialect: dict[str, int] = {}
        by_source: dict[str, int] = {}
        entries_with_alternatives = 0

        for entry in self._entries.values():
            dialect_key = entry.dialect or "universal"
            by_dialect[dialect_key] = by_dialect.get(dialect_key, 0) + 1
            by_source[entry.source] = by_source.get(entry.source, 0) + 1
            if entry.alternatives:
                entries_with_alternatives += 1

        return {
            "total_entries": len(self._entries),
            "total_lemmas": len(self._entries_by_lemma),
            "entries_by_dialect": by_dialect,
            "entries_by_source": by_source,
            "entries_with_alternatives": entries_with_alternatives,
        }

    def iter_entries(self) -> Iterable[LexiconEntry]:
        """Iterate all indexed entries."""

        return self._entries.values()

    def __len__(self) -> int:
        return len(self._entries)

    @lru_cache(maxsize=8192)  # noqa: B019 - deliberate cache on bound method
    def _lookup_cached(
        self,
        normalized_word: str,
        normalized_dialect: str | None,
    ) -> tuple[LexiconEntry | None, bool]:
        if normalized_dialect is not None:
            dialect_entry = self._entries.get((normalized_word, normalized_dialect))
            if dialect_entry is not None:
                return dialect_entry, False
            if self.config.fallback_to_universal:
                universal = self._entries.get((normalized_word, None))
                if universal is not None:
                    return universal, True
            return None, False

        default_dialect = _normalize_dialect(self.config.default_dialect)
        if default_dialect is not None:
            preferred = self._entries.get((normalized_word, default_dialect))
            if preferred is not None:
                return preferred, False
            if self.config.fallback_to_universal:
                universal = self._entries.get((normalized_word, None))
                if universal is not None:
                    return universal, True

        universal = self._entries.get((normalized_word, None))
        if universal is not None:
            return universal, False

        dialect_entries = self._entries_by_lemma.get(normalized_word, [])
        if not dialect_entries:
            return None, False

        best = max(dialect_entries, key=lambda entry: entry.confidence)
        return best, False

    @classmethod
    def _read_tsv_with_compat(cls, path: Path) -> list[LexiconEntry]:
        with path.open("r", encoding="utf-8") as handle:
            header = handle.readline()
        if "variants_json" in header.lower():
            return cls._read_legacy_tsv(path)
        return read_tsv(path, format="extended")

    @staticmethod
    def _read_legacy_tsv(path: Path) -> list[LexiconEntry]:
        entries: list[LexiconEntry] = []
        with path.open("r", encoding="utf-8") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            for line_num, row in enumerate(reader, start=2):
                lemma = (row.get("word") or row.get("lemma") or "").strip()
                ipa_raw = (row.get("ipa") or "").strip()
                if not lemma or not ipa_raw:
                    logger.warning(
                        "TSV line %s skipped: empty lemma or ipa",
                        line_num,
                    )
                    continue
                try:
                    variants_json = row.get("variants_json", "[]") or "[]"
                    raw_variants = json.loads(variants_json)
                    if not isinstance(raw_variants, list):
                        raw_variants = []
                    alternatives = [canonicalize_ipa(str(value)) for value in raw_variants]
                    entries.append(
                        LexiconEntry(
                            lemma=lemma,
                            ipa=canonicalize_ipa(ipa_raw),
                            dialect=None,
                            source=(row.get("source") or "unknown").strip() or "unknown",
                            alternatives=alternatives,
                        )
                    )
                except (json.JSONDecodeError, ValueError) as exc:
                    logger.warning("TSV line %s skipped: %s", line_num, exc)
        return entries

    def _normalize_entry(self, entry: LexiconEntry) -> LexiconEntry:
        lemma = unicodedata.normalize("NFC", entry.lemma.strip())
        if not self.config.case_sensitive:
            lemma = lemma.lower()
        ipa = canonicalize_ipa(entry.ipa)
        dialect = _normalize_dialect(entry.dialect)

        alternatives: list[str] = []
        seen: set[str] = set()
        for alt in entry.alternatives:
            normalized = canonicalize_ipa(alt)
            if not normalized or normalized == ipa or normalized in seen:
                continue
            seen.add(normalized)
            alternatives.append(normalized)

        return replace(
            entry,
            lemma=lemma,
            ipa=ipa,
            dialect=dialect,
            alternatives=alternatives,
        )

    def _merge_entry(self, entry: LexiconEntry) -> None:
        key = (entry.lemma, entry.dialect)
        existing = self._entries.get(key)
        if existing is None:
            self._entries[key] = entry
            return

        if entry.confidence > existing.confidence:
            primary = entry
            secondary = existing
        else:
            primary = existing
            secondary = entry

        merged_alternatives = self._merge_alternatives(primary, secondary)
        self._entries[key] = replace(primary, alternatives=merged_alternatives)

    @staticmethod
    def _merge_alternatives(primary: LexiconEntry, secondary: LexiconEntry) -> list[str]:
        seen: set[str] = {primary.ipa}
        merged: list[str] = []

        for value in [*primary.alternatives, *secondary.alternatives, secondary.ipa]:
            if value in seen:
                continue
            seen.add(value)
            merged.append(value)

        return merged


__all__ = ["DialectAwareLexicon"]
