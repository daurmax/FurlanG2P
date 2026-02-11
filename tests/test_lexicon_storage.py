from __future__ import annotations

import json
from pathlib import Path

import pytest

from furlan_g2p.lexicon import LexiconEntry
from furlan_g2p.lexicon.storage import (
    detect_format,
    read_jsonl,
    read_tsv,
    write_jsonl,
    write_tsv,
)


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("lexicon.tsv", "tsv"),
        ("lexicon.txt", "tsv"),
        ("lexicon.jsonl", "jsonl"),
        ("lexicon.ndjson", "jsonl"),
        ("lexicon.csv", "unknown"),
    ],
)
def test_detect_format(name: str, expected: str) -> None:
    assert detect_format(Path(name)) == expected


def test_write_and_read_tsv_simple_round_trip(
    tmp_path: Path,
    sample_lexicon_entries: list[LexiconEntry],
) -> None:
    path = tmp_path / "lexicon_simple.tsv"
    write_tsv(sample_lexicon_entries, path, format="simple")
    loaded = read_tsv(path, format="simple")

    assert [entry.lemma for entry in loaded] == [entry.lemma for entry in sample_lexicon_entries]
    assert [entry.ipa for entry in loaded] == [entry.ipa for entry in sample_lexicon_entries]
    assert all(entry.source == "unknown" for entry in loaded)


def test_write_and_read_tsv_extended_round_trip(
    tmp_path: Path,
    sample_lexicon_entries: list[LexiconEntry],
) -> None:
    path = tmp_path / "lexicon_extended.tsv"
    write_tsv(sample_lexicon_entries, path, format="extended")
    loaded = read_tsv(path, format="extended")

    assert len(loaded) == len(sample_lexicon_entries)
    assert loaded[0].lemma == sample_lexicon_entries[0].lemma
    assert loaded[0].dialect == sample_lexicon_entries[0].dialect
    assert loaded[0].source == sample_lexicon_entries[0].source
    assert loaded[0].confidence == pytest.approx(sample_lexicon_entries[0].confidence)
    assert loaded[0].frequency == sample_lexicon_entries[0].frequency
    assert loaded[0].alternatives == sample_lexicon_entries[0].alternatives


def test_write_and_read_jsonl_round_trip(
    tmp_path: Path,
    sample_lexicon_entries: list[LexiconEntry],
) -> None:
    path = tmp_path / "lexicon.jsonl"
    write_jsonl(sample_lexicon_entries, path)
    loaded = read_jsonl(path)

    assert loaded == sample_lexicon_entries


def test_read_tsv_malformed_rows_are_skipped(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    path = tmp_path / "bad.tsv"
    path.write_text(
        "\n".join(
            [
                "lemma\tipa\tdialect\tsource\tconfidence\tfrequency\talternatives",
                "bad-line-only-one-column",
                "empty_ipa\t",
                "good\tˈɡud\tcentral\tmanual\tnot-a-float\tnot-an-int\t{bad-json}",
                'good2\tˈɡud2\twestern\tmanual\t0.9\t11\t["ˈɡut"]',
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    loaded = read_tsv(path, format="extended")
    assert [entry.lemma for entry in loaded] == ["good", "good2"]
    assert loaded[0].confidence == pytest.approx(1.0)
    assert loaded[0].frequency is None
    assert loaded[0].alternatives == []
    assert "invalid confidence" in caplog.text
    assert "invalid frequency" in caplog.text
    assert "invalid JSON in alternatives" in caplog.text


def test_read_jsonl_malformed_rows_are_skipped(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    path = tmp_path / "bad.jsonl"
    path.write_text(
        "\n".join(
            [
                json.dumps({"lemma": "cjase", "ipa": "ˈcaze"}),
                '{"lemma": "missing_ipa"}',
                '{"lemma": "broken", "ipa": ',
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    loaded = read_jsonl(path)
    assert len(loaded) == 1
    assert loaded[0].lemma == "cjase"
    assert "missing required field" in caplog.text
    assert "invalid JSON" in caplog.text


def test_read_tsv_supports_utf8_bom(tmp_path: Path) -> None:
    path = tmp_path / "bom.tsv"
    path.write_text("lemma\tipa\ncjase\tˈcaze\n", encoding="utf-8-sig")

    loaded = read_tsv(path)
    assert len(loaded) == 1
    assert loaded[0].lemma == "cjase"
    assert loaded[0].ipa == "ˈcaze"
