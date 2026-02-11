"""Shared fixtures for hybrid G2P module tests."""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from furlan_g2p.lexicon import LexiconEntry


@pytest.fixture
def cli_runner() -> CliRunner:
    """Return a Click CLI runner."""

    return CliRunner()


@pytest.fixture
def sample_lexicon_entries() -> list[LexiconEntry]:
    """Return a compact lexicon fixture used by multiple modules."""

    return [
        LexiconEntry(
            lemma="cjase",
            ipa="ˈcaze",
            dialect=None,
            source="seed",
            confidence=1.0,
            frequency=100,
            alternatives=["ˈcjaze"],
        ),
        LexiconEntry(
            lemma="cjase",
            ipa="ˈca:ze",
            dialect="western",
            source="manual",
            confidence=0.9,
            frequency=40,
            alternatives=[],
        ),
        LexiconEntry(
            lemma="aghe",
            ipa="ˈaɡe",
            dialect="central",
            source="wikipron",
            confidence=0.8,
            frequency=80,
            alternatives=[],
        ),
    ]


@pytest.fixture
def sample_wikipron_file(tmp_path: Path) -> Path:
    """Create a small WikiPron-style TSV file."""

    path = tmp_path / "wikipron.tsv"
    path.write_text(
        "\n".join(
            [
                "word\tipa\tlanguage_code",
                "cjase\t'caze\tfur-central",
                "aghe\t'aɡe\tfur-west",
                "invalid_line_only_one_column",
            ]
        )
        + "\n",
        encoding="utf-8-sig",
    )
    return path


@pytest.fixture
def sample_gold_set_file(tmp_path: Path) -> Path:
    """Create a gold-set TSV fixture."""

    path = tmp_path / "gold.tsv"
    path.write_text(
        "\n".join(
            [
                "# comment",
                "cjase\tˈcaze\tcentral",
                "aghe\tˈaɡe\twestern",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return path


@pytest.fixture
def sample_wordlist_file(tmp_path: Path) -> Path:
    """Create a small coverage wordlist fixture."""

    path = tmp_path / "wordlist.txt"
    path.write_text("cjase\naghe\n123\n", encoding="utf-8")
    return path
