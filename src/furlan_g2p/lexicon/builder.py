"""LexiconBuilder for assembling pronunciation dictionaries."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from pathlib import Path

from ..core.interfaces import ILexiconBuilder
from .canonicalizer import IPACanonicalize
from .schema import LexiconEntry
from .storage import detect_format, read_jsonl, read_tsv, write_jsonl, write_tsv
from .wikipron import iter_wikipron_entries

logger = logging.getLogger(__name__)

_DEFAULT_SOURCE_CONFIDENCE: dict[str, float] = {
    "seed": 1.0,
    "manual": 1.0,
    "wikipron": 0.85,
    "tsv": 0.75,
    "jsonl": 0.75,
    "unknown": 0.5,
}


@dataclass(slots=True)
class ValidationIssue:
    """Validation issue raised during lexicon checks."""

    kind: str
    message: str
    lemma: str | None = None
    dialect: str | None = None
    ipa: str | None = None
    source: str | None = None
    details: dict[str, object] = field(default_factory=dict)


class LexiconBuilder(ILexiconBuilder):
    """Build and validate lexicon entries from multiple sources."""

    def __init__(
        self,
        canonicalizer: IPACanonicalize | None = None,
        default_dialect: str | None = None,
        source_confidence: Mapping[str, float] | None = None,
    ) -> None:
        self._canonicalizer = canonicalizer or IPACanonicalize()
        self.default_dialect = default_dialect
        self._source_confidence = {
            key.lower(): value for key, value in (source_confidence or {}).items()
        }
        self._entries: dict[tuple[str, str | None], LexiconEntry] = {}

    def add_source(
        self,
        path: Path,
        source_type: str,
        dialect: str | None = None,
    ) -> int:
        """Add entries from a file source.

        Parameters
        ----------
        path:
            Path to the source file.
        source_type:
            Source identifier (e.g., "wikipron", "tsv", "jsonl").
        dialect:
            Default dialect to apply when the source lacks dialect metadata.

        Returns
        -------
        int
            Number of entries ingested (including merged duplicates).
        """

        source = source_type.strip().lower()
        count = 0
        if source == "wikipron":
            default_dialect = dialect or self.default_dialect
            for record in iter_wikipron_entries(path, default_dialect=default_dialect):
                entry = self._make_entry_from_wikipron(
                    record.lemma, record.ipa, record.dialect, source
                )
                if entry is None:
                    continue
                if self.add_entry(entry):
                    count += 1
            return count

        if source in {"tsv", "jsonl"}:
            entries = self._read_source_entries(path, source)
        else:
            fmt = detect_format(path)
            if fmt == "unknown":
                raise ValueError(f"Unsupported lexicon format for {path}")
            entries = self._read_source_entries(path, fmt)

        for entry in entries:
            adjusted = self._apply_source_defaults(entry, source, dialect)
            if self.add_entry(adjusted):
                count += 1
        return count

    def add_entry(self, entry: LexiconEntry) -> bool:
        """Add a single entry and return success status."""

        normalized = self._normalize_entry(entry)
        if normalized is None:
            return False
        self._merge_normalized_entry(normalized)
        return True

    def merge_entry(self, entry: LexiconEntry) -> None:
        """Merge an entry into the builder, updating alternatives as needed."""

        normalized = self._normalize_entry(entry)
        if normalized is None:
            return
        self._merge_normalized_entry(normalized)

    def validate(self) -> list[ValidationIssue]:
        """Validate entries and return a list of issues."""

        issues: list[ValidationIssue] = []
        for entry in self._entries.values():
            unknown = self._canonicalizer.get_unknown_symbols(entry.ipa)
            if unknown:
                issues.append(
                    ValidationIssue(
                        kind="unknown_symbol",
                        message="Unknown IPA symbols found in primary pronunciation",
                        lemma=entry.lemma,
                        dialect=entry.dialect,
                        ipa=entry.ipa,
                        source=entry.source,
                        details={"symbols": sorted(unknown)},
                    )
                )
            if entry.alternatives:
                issues.append(
                    ValidationIssue(
                        kind="duplicate_pronunciation",
                        message="Multiple pronunciations recorded for lemma",
                        lemma=entry.lemma,
                        dialect=entry.dialect,
                        ipa=entry.ipa,
                        source=entry.source,
                        details={"alternatives": list(entry.alternatives)},
                    )
                )
            for alt in entry.alternatives:
                alt_unknown = self._canonicalizer.get_unknown_symbols(alt)
                if alt_unknown:
                    issues.append(
                        ValidationIssue(
                            kind="unknown_symbol",
                            message="Unknown IPA symbols found in alternative pronunciation",
                            lemma=entry.lemma,
                            dialect=entry.dialect,
                            ipa=alt,
                            source=entry.source,
                            details={"symbols": sorted(alt_unknown)},
                        )
                    )
        return issues

    def build(self) -> list[LexiconEntry]:
        """Return the final list of entries."""

        return sorted(
            self._entries.values(),
            key=lambda entry: (entry.lemma.lower(), entry.dialect or ""),
        )

    def export(self, path: Path, format: str = "jsonl") -> None:
        """Export entries to disk.

        Parameters
        ----------
        path:
            Destination path.
        format:
            Export format ("jsonl", "tsv", "tsv_simple", "tsv_extended").
        """

        fmt = format.strip().lower()
        entries = self.build()
        if fmt == "jsonl":
            write_jsonl(entries, path)
        elif fmt in {"tsv", "tsv_extended", "extended"}:
            write_tsv(entries, path, format="extended")
        elif fmt in {"tsv_simple", "simple"}:
            write_tsv(entries, path, format="simple")
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def summary(self) -> dict[str, object]:
        """Return a summary report of the current lexicon state."""

        by_source: dict[str, int] = {}
        by_dialect: dict[str, int] = {}
        duplicates: list[dict[str, object]] = []
        unknown_symbols: set[str] = set()

        for entry in self._entries.values():
            by_source[entry.source] = by_source.get(entry.source, 0) + 1
            dialect_key = entry.dialect or "universal"
            by_dialect[dialect_key] = by_dialect.get(dialect_key, 0) + 1
            unknown_symbols.update(self._canonicalizer.get_unknown_symbols(entry.ipa))
            for alt in entry.alternatives:
                unknown_symbols.update(self._canonicalizer.get_unknown_symbols(alt))
            if entry.alternatives:
                duplicates.append(
                    {
                        "lemma": entry.lemma,
                        "dialect": entry.dialect,
                        "ipa": entry.ipa,
                        "alternatives": list(entry.alternatives),
                    }
                )

        return {
            "total_entries": len(self._entries),
            "entries_by_source": by_source,
            "entries_by_dialect": by_dialect,
            "unknown_symbols": sorted(unknown_symbols),
            "duplicates": duplicates,
        }

    def _read_source_entries(self, path: Path, source: str) -> list[LexiconEntry]:
        if source == "tsv":
            return read_tsv(path, format="extended")
        if source == "jsonl":
            return read_jsonl(path)
        raise ValueError(f"Unsupported source type: {source}")

    def _make_entry_from_wikipron(
        self,
        lemma: str,
        ipa: str,
        dialect: str | None,
        source: str,
    ) -> LexiconEntry | None:
        confidence = self._source_confidence.get(
            source, _DEFAULT_SOURCE_CONFIDENCE.get(source, 1.0)
        )
        try:
            return LexiconEntry(
                lemma=lemma,
                ipa=ipa,
                dialect=dialect,
                source=source,
                confidence=confidence,
                alternatives=[],
            )
        except ValueError as exc:
            logger.warning("Invalid WikiPron entry for %s: %s", lemma, exc)
            return None

    def _apply_source_defaults(
        self,
        entry: LexiconEntry,
        source: str,
        dialect: str | None,
    ) -> LexiconEntry:
        updated = entry
        if updated.source == "unknown":
            updated = replace(updated, source=source or "unknown")
        if updated.confidence == 1.0 and updated.source in {"unknown", source}:
            confidence = self._source_confidence.get(
                updated.source,
                _DEFAULT_SOURCE_CONFIDENCE.get(updated.source, updated.confidence),
            )
            updated = replace(updated, confidence=confidence)
        if updated.dialect is None:
            default = dialect or self.default_dialect
            if default is not None:
                updated = replace(updated, dialect=default)
        return updated

    def _normalize_entry(self, entry: LexiconEntry) -> LexiconEntry | None:
        try:
            lemma = entry.lemma.strip()
            if not lemma:
                logger.warning("Skipped entry with empty lemma")
                return None
            ipa = self._canonicalizer.canonicalize(entry.ipa)
            if not ipa:
                logger.warning("Skipped entry with empty IPA for lemma %s", lemma)
                return None
            dialect = entry.dialect or self.default_dialect
            normalized = replace(entry, lemma=lemma, ipa=ipa, dialect=dialect)
            alternatives: list[str] = []
            seen: set[str] = set()
            for alt in normalized.alternatives:
                alt_norm = self._canonicalizer.canonicalize(alt)
                if not alt_norm or alt_norm == ipa or alt_norm in seen:
                    continue
                seen.add(alt_norm)
                alternatives.append(alt_norm)
            if alternatives != normalized.alternatives:
                normalized = replace(normalized, alternatives=alternatives)
            return normalized
        except ValueError as exc:
            logger.warning("Invalid lexicon entry for %s: %s", entry.lemma, exc)
            return None

    def _merge_normalized_entry(self, entry: LexiconEntry) -> None:
        key = (entry.lemma, entry.dialect)
        existing = self._entries.get(key)
        if existing is None:
            self._entries[key] = entry
            return
        if entry.ipa == existing.ipa:
            merged_alts = self._merge_alternatives(existing, entry, existing.ipa)
            updated = existing
            if merged_alts != existing.alternatives:
                updated = replace(updated, alternatives=merged_alts)
            if entry.confidence > existing.confidence:
                updated = replace(updated, confidence=entry.confidence, source=entry.source)
            self._entries[key] = updated
            return
        if entry.confidence > existing.confidence:
            new_primary = entry.ipa
            new_source = entry.source
            new_confidence = entry.confidence
            new_frequency = entry.frequency
        else:
            new_primary = existing.ipa
            new_source = existing.source
            new_confidence = existing.confidence
            new_frequency = existing.frequency
        new_alternatives = self._merge_alternatives(existing, entry, new_primary)
        if new_frequency is None:
            new_frequency = entry.frequency or existing.frequency
        self._entries[key] = replace(
            existing,
            ipa=new_primary,
            alternatives=new_alternatives,
            source=new_source,
            confidence=new_confidence,
            frequency=new_frequency,
        )

    @staticmethod
    def _merge_alternatives(
        existing: LexiconEntry,
        incoming: LexiconEntry,
        primary: str,
    ) -> list[str]:
        seen: set[str] = set()
        merged: list[str] = []
        candidates = list(existing.alternatives) + list(incoming.alternatives)
        for candidate in candidates:
            if candidate == primary or candidate in seen:
                continue
            seen.add(candidate)
            merged.append(candidate)
        for candidate in (existing.ipa, incoming.ipa):
            if candidate == primary or candidate in seen:
                continue
            seen.add(candidate)
            merged.append(candidate)
        return merged


__all__ = ["LexiconBuilder", "ValidationIssue"]
