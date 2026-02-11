"""Lexicon adapters for G2P lookup."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from ..lexicon.lookup import DialectAwareLexicon
from ..lexicon.schema import LexiconConfig
from ..lexicon.schema import LexiconEntry as SchemaLexiconEntry
from ..phonology import canonicalize_ipa


@dataclass(frozen=True)
class LexiconEntry:
    """Legacy G2P lexicon entry shape.

    Parameters
    ----------
    word:
        Surface form of the lemma.
    ipa:
        Primary IPA pronunciation.
    variants:
        Alternative IPA pronunciations.
    source:
        Source identifier.
    dialect:
        Dialect code or ``None`` for universal entries.
    """

    word: str
    ipa: str
    variants: tuple[str, ...]
    source: str
    dialect: str | None = None


class Lexicon:
    """Read-only lexicon compatible with the historical G2P API."""

    def __init__(
        self,
        entries: dict[str, LexiconEntry] | None = None,
        *,
        config: LexiconConfig | None = None,
        dialect_lexicon: DialectAwareLexicon | None = None,
    ) -> None:
        self.config = config or LexiconConfig()
        if dialect_lexicon is not None:
            self._dialect_lexicon = dialect_lexicon
            return

        schema_entries = self._legacy_dict_to_schema(entries or {})
        self._dialect_lexicon = DialectAwareLexicon(entries=schema_entries, config=self.config)

    @classmethod
    def load_seed(cls, config: LexiconConfig | None = None) -> Lexicon:
        """Load the packaged seed lexicon."""

        dialect_lexicon = DialectAwareLexicon.load_seed(config=config)
        return cls(config=config, dialect_lexicon=dialect_lexicon)

    @classmethod
    def load(cls, path: str | Path, config: LexiconConfig | None = None) -> Lexicon:
        """Load a lexicon from TSV or JSONL."""

        dialect_lexicon = DialectAwareLexicon.from_path(path=path, config=config)
        return cls(config=config, dialect_lexicon=dialect_lexicon)

    @lru_cache(maxsize=2048)  # noqa: B019 - deliberate cache on bound method
    def _lookup_entry(
        self,
        word: str,
        dialect: str | None = None,
    ) -> SchemaLexiconEntry | None:
        return self._dialect_lexicon.lookup(word, dialect=dialect)

    @lru_cache(maxsize=2048)  # noqa: B019 - deliberate cache on bound method
    def _lookup_legacy_entry(
        self,
        word: str,
        dialect: str | None = None,
    ) -> LexiconEntry | None:
        entry = self._lookup_entry(word, dialect=dialect)
        if entry is None:
            return None
        return self._schema_to_legacy(entry)

    def lookup(self, word: str, dialect: str | None = None) -> SchemaLexiconEntry | None:
        """Return the schema entry for ``word``."""

        if not word:
            return None
        return self._lookup_entry(word, dialect=dialect)

    def lookup_ipa(self, word: str, dialect: str | None = None) -> str | None:
        """Return the primary IPA for ``word`` if present."""

        entry = self.lookup(word, dialect=dialect)
        return entry.ipa if entry else None

    def get(self, word: str, dialect: str | None = None) -> str | None:
        """Compatibility alias returning the primary IPA string."""

        return self.lookup_ipa(word, dialect=dialect)

    def get_entry(self, word: str, dialect: str | None = None) -> LexiconEntry | None:
        """Return a legacy-shaped entry for ``word`` if present."""

        if not word:
            return None
        return self._lookup_legacy_entry(word, dialect=dialect)

    def get_alternatives(self, word: str, dialect: str | None = None) -> list[str]:
        """Return alternative pronunciations for ``word``."""

        entry = self.lookup(word, dialect=dialect)
        if entry is None:
            return []
        return list(entry.alternatives)

    def has_entry(self, word: str, dialect: str | None = None) -> bool:
        """Return ``True`` if ``word`` exists in the lexicon."""

        return self.lookup(word, dialect=dialect) is not None

    def stats(self) -> dict[str, object]:
        """Return lexicon statistics."""

        return self._dialect_lexicon.stats()

    def __contains__(self, word: str) -> bool:
        return self.has_entry(word)

    def __len__(self) -> int:
        return len(self._dialect_lexicon)

    def items(self) -> Iterable[tuple[str, LexiconEntry]]:
        for entry in self._dialect_lexicon.iter_entries():
            legacy = self._schema_to_legacy(entry)
            yield legacy.word.lower(), legacy

    @staticmethod
    def _legacy_dict_to_schema(entries: dict[str, LexiconEntry]) -> list[SchemaLexiconEntry]:
        out: list[SchemaLexiconEntry] = []
        for key, entry in entries.items():
            lemma = entry.word or key
            out.append(
                SchemaLexiconEntry(
                    lemma=lemma,
                    ipa=canonicalize_ipa(entry.ipa),
                    dialect=entry.dialect,
                    source=entry.source,
                    alternatives=[canonicalize_ipa(value) for value in entry.variants],
                )
            )
        return out

    @staticmethod
    def _schema_to_legacy(entry: SchemaLexiconEntry) -> LexiconEntry:
        return LexiconEntry(
            word=entry.lemma,
            ipa=entry.ipa,
            variants=tuple(entry.alternatives),
            source=entry.source,
            dialect=entry.dialect,
        )


__all__ = ["Lexicon", "LexiconEntry"]
