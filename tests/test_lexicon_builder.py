from __future__ import annotations

import json
from pathlib import Path

import pytest

from furlan_g2p.lexicon import IPACanonicalize, LexiconBuilder, LexiconEntry
from furlan_g2p.lexicon.storage import read_jsonl, read_tsv
from furlan_g2p.lexicon.wikipron import iter_wikipron_entries


def _write_tsv(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines), encoding="utf-8-sig")


def test_wikipron_parser_valid_and_malformed_lines(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    tsv_path = tmp_path / "wikipron.tsv"
    _write_tsv(
        tsv_path,
        [
            "word\tipa\tlanguage_code",
            "cjase\t'caze\tfur-central",
            "aghe\t'aɡe\tfur",
            "badline",
            "\tˈvoid\tfur-west",
        ],
    )

    entries = list(iter_wikipron_entries(tsv_path, default_dialect="western"))
    assert len(entries) == 2
    assert entries[0].lemma == "cjase"
    assert entries[0].ipa == "'caze"
    assert entries[0].dialect == "central"
    assert entries[1].dialect == "western"
    assert "expected 2 columns" in caplog.text
    assert "empty lemma or ipa" in caplog.text


def test_builder_merges_alternatives_and_keeps_highest_confidence() -> None:
    builder = LexiconBuilder()
    entry_one = LexiconEntry(
        lemma="cjase",
        ipa="a",
        source="manual",
        confidence=0.6,
        alternatives=["b"],
    )
    entry_two = LexiconEntry(
        lemma="cjase",
        ipa="a",
        source="wikipron",
        confidence=0.9,
        alternatives=["c"],
    )

    assert builder.add_entry(entry_one)
    assert builder.add_entry(entry_two)

    entries = builder.build()
    assert len(entries) == 1
    merged = entries[0]
    assert merged.source == "wikipron"
    assert merged.confidence == 0.9
    assert set(merged.alternatives) == {"b", "c"}

    issues = builder.validate()
    assert any(issue.kind == "duplicate_pronunciation" for issue in issues)


def test_builder_canonicalizes_wikipron_entries(sample_wikipron_file: Path) -> None:
    builder = LexiconBuilder()
    count = builder.add_source(sample_wikipron_file, source_type="wikipron")

    assert count == 2
    by_lemma = {entry.lemma: entry for entry in builder.build()}
    assert by_lemma["cjase"].ipa == "ˈcaze"
    assert by_lemma["aghe"].ipa == "ˈage"
    assert by_lemma["cjase"].source == "wikipron"
    assert by_lemma["cjase"].confidence == pytest.approx(0.85)


def test_builder_reports_unknown_symbols() -> None:
    canon = IPACanonicalize(inventory={"a"})
    builder = LexiconBuilder(canonicalizer=canon)
    builder.add_entry(LexiconEntry(lemma="cjase", ipa="x"))

    issues = builder.validate()
    assert any(
        issue.kind == "unknown_symbol" and "x" in issue.details.get("symbols", [])
        for issue in issues
    )


def test_builder_add_source_multi_source_and_summary(tmp_path: Path) -> None:
    tsv_path = tmp_path / "source.tsv"
    tsv_path.write_text("lemma\tipa\ncjase\tˈcaze\n", encoding="utf-8")

    jsonl_path = tmp_path / "source.jsonl"
    jsonl_path.write_text(
        json.dumps(
            {
                "lemma": "aghe",
                "ipa": "ˈaɡe",
                "dialect": "central",
                "source": "manual",
                "confidence": 0.8,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    builder = LexiconBuilder()
    assert builder.add_source(tsv_path, source_type="tsv") == 1
    assert builder.add_source(jsonl_path, source_type="jsonl") == 1

    summary = builder.summary()
    assert summary["total_entries"] == 2
    assert summary["entries_by_source"] == {"tsv": 1, "manual": 1}
    assert summary["entries_by_dialect"] == {"universal": 1, "central": 1}


def test_builder_export_jsonl_and_tsv(tmp_path: Path) -> None:
    builder = LexiconBuilder()
    builder.add_entry(LexiconEntry(lemma="cjase", ipa="a"))

    jsonl_path = tmp_path / "lexicon.jsonl"
    tsv_path = tmp_path / "lexicon.tsv"

    builder.export(jsonl_path, format="jsonl")
    builder.export(tsv_path, format="tsv_extended")

    jsonl_entries = read_jsonl(jsonl_path)
    tsv_entries = read_tsv(tsv_path, format="extended")

    assert jsonl_entries[0].lemma == "cjase"
    assert tsv_entries[0].lemma == "cjase"


def test_builder_export_unsupported_format_raises(tmp_path: Path) -> None:
    builder = LexiconBuilder()
    builder.add_entry(LexiconEntry(lemma="cjase", ipa="a"))
    with pytest.raises(ValueError, match="Unsupported export format"):
        builder.export(tmp_path / "lexicon.invalid", format="xml")


def test_builder_add_source_detects_unknown_file_format(tmp_path: Path) -> None:
    path = tmp_path / "source.csv"
    path.write_text("lemma,ipa\ncjase,ˈcaze\n", encoding="utf-8")
    builder = LexiconBuilder()
    with pytest.raises(ValueError, match="Unsupported lexicon format"):
        builder.add_source(path, source_type="auto")


def test_builder_validation_reports_duplicate_and_unknown_alternative() -> None:
    canon = IPACanonicalize(inventory={"a"})
    builder = LexiconBuilder(canonicalizer=canon)
    builder.add_entry(LexiconEntry(lemma="cjase", ipa="a"))
    builder.add_entry(LexiconEntry(lemma="cjase", ipa="x", confidence=0.2))

    issues = builder.validate()
    kinds = [issue.kind for issue in issues]
    assert "duplicate_pronunciation" in kinds
    assert "unknown_symbol" in kinds


def test_builder_add_entry_rejects_lemma_empty_after_strip() -> None:
    builder = LexiconBuilder()
    accepted = builder.add_entry(LexiconEntry(lemma="   ", ipa="a"))
    assert accepted is False
