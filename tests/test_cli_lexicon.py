from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from furlan_g2p.cli.app import cli


def _write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
        encoding="utf-8",
    )


def test_lexicon_help_lists_subcommands() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["lexicon", "--help"])
    assert result.exit_code == 0
    assert "build" in result.output
    assert "info" in result.output
    assert "export" in result.output
    assert "validate" in result.output


def test_lexicon_build_and_info_json(tmp_path: Path) -> None:
    source = tmp_path / "sample.tsv"
    source.write_text("lemma\tipa\ntest\tˈtest\n", encoding="utf-8")
    built = tmp_path / "lexicon.jsonl"

    runner = CliRunner()
    build_result = runner.invoke(
        cli,
        [
            "lexicon",
            "build",
            str(source),
            "--output",
            str(built),
            "--source-type",
            "tsv",
            "--format",
            "jsonl",
        ],
    )
    assert build_result.exit_code == 0
    assert built.exists()

    info_result = runner.invoke(cli, ["lexicon", "info", str(built), "--json"])
    assert info_result.exit_code == 0
    payload = json.loads(info_result.output)
    assert payload["total_entries"] == 1
    assert payload["entries_by_source"]["tsv"] == 1
    assert payload["entries_with_stress_markers"] == 1


def test_lexicon_export_applies_filters(tmp_path: Path) -> None:
    source = tmp_path / "lexicon.jsonl"
    _write_jsonl(
        source,
        [
            {
                "lemma": "cjase",
                "ipa": "ˈcaze",
                "dialect": "central",
                "source": "manual",
                "confidence": 1.0,
            },
            {
                "lemma": "cjase",
                "ipa": "ˈcjaze",
                "dialect": "western",
                "source": "manual",
                "confidence": 0.4,
            },
        ],
    )
    exported = tmp_path / "lexicon.tsv"

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "lexicon",
            "export",
            str(source),
            str(exported),
            "--format",
            "tsv-simple",
            "--dialect",
            "central",
            "--min-confidence",
            "0.8",
        ],
    )
    assert result.exit_code == 0
    lines = exported.read_text(encoding="utf-8").strip().splitlines()
    assert lines == ["lemma\tipa", "cjase\tˈcaze"]


def test_lexicon_validate_strict_exit_code(tmp_path: Path) -> None:
    source = tmp_path / "duplicates.jsonl"
    _write_jsonl(
        source,
        [
            {
                "lemma": "cjase",
                "ipa": "a",
                "dialect": "central",
                "source": "manual",
                "confidence": 1.0,
            },
            {
                "lemma": "cjase",
                "ipa": "e",
                "dialect": "central",
                "source": "manual",
                "confidence": 1.0,
            },
        ],
    )

    runner = CliRunner()
    non_strict = runner.invoke(cli, ["lexicon", "validate", str(source)])
    assert non_strict.exit_code == 0
    assert "duplicate_pronunciation" in non_strict.output

    strict = runner.invoke(cli, ["lexicon", "validate", str(source), "--strict"])
    assert strict.exit_code == 1
    assert "duplicate_pronunciation" in strict.output
