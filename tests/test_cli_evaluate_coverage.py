from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from furlan_g2p.cli.app import cli


def test_evaluate_help_lists_options() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["evaluate", "--help"])
    assert result.exit_code == 0
    assert "--dialect" in result.output
    assert "--output" in result.output
    assert "--format" in result.output
    assert "--verbose" in result.output
    assert "--lexicon" in result.output


def test_evaluate_computes_metrics() -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        gold_path = Path("gold.tsv")
        gold_path.write_text("cjase\tˈcaze\naghe\tˈage\n", encoding="utf-8")
        result = runner.invoke(cli, ["evaluate", str(gold_path)])

    assert result.exit_code == 0
    assert "Total words evaluated: 2" in result.output
    assert "WER: 0.0000 (0.00%)" in result.output
    assert "PER: 0.0000" in result.output
    assert "Stress accuracy: 1.0000 (100.00%)" in result.output


def test_evaluate_verbose_shows_per_word_errors() -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        gold_path = Path("gold.tsv")
        gold_path.write_text("cjase\tˈkaze\n", encoding="utf-8")
        result = runner.invoke(cli, ["evaluate", str(gold_path), "--verbose"])

    assert result.exit_code == 0
    assert "Errors:" in result.output
    assert "cjase" in result.output
    assert "predicted=ˈcaze" in result.output
    assert "expected=ˈkaze" in result.output


def test_evaluate_json_output_is_parseable() -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        gold_path = Path("gold.tsv")
        out_path = Path("eval.json")
        gold_path.write_text("cjase\tˈcaze\n", encoding="utf-8")
        result = runner.invoke(
            cli,
            [
                "evaluate",
                str(gold_path),
                "--format",
                "json",
                "--output",
                str(out_path),
            ],
        )
        assert out_path.exists()
        detail_payload = json.loads(out_path.read_text(encoding="utf-8"))

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["word_count"] == 1
    assert payload["wer"] == 0.0
    assert "details" not in payload
    assert isinstance(detail_payload["details"], list)
    assert len(detail_payload["details"]) == 1


def test_coverage_help_lists_options() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["coverage", "--help"])
    assert result.exit_code == 0
    assert "--lexicon" in result.output
    assert "--dialect" in result.output
    assert "--output" in result.output
    assert "--format" in result.output
    assert "--show-oov" in result.output


def test_coverage_reports_counts_and_oov_list() -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        words_path = Path("words.txt")
        words_path.write_text("cjase\naghe\n123\n", encoding="utf-8")
        result = runner.invoke(cli, ["coverage", str(words_path), "--show-oov"])

    assert result.exit_code == 0
    assert "Total words: 3" in result.output
    assert "Lexicon hits: 1" in result.output
    assert "Rule-only words: 1" in result.output
    assert "OOV words: 1" in result.output
    assert "Coverage: 66.67%" in result.output
    assert "123" in result.output


def test_coverage_json_output_is_parseable() -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        words_path = Path("words.txt")
        out_path = Path("coverage.json")
        words_path.write_text("cjase\naghe\n123\n", encoding="utf-8")
        result = runner.invoke(
            cli,
            [
                "coverage",
                str(words_path),
                "--format",
                "json",
                "--show-oov",
                "--output",
                str(out_path),
            ],
        )
        assert out_path.exists()
        detail_payload = json.loads(out_path.read_text(encoding="utf-8"))

    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["total_words"] == 3
    assert payload["lexicon_hits"]["count"] == 1
    assert payload["rule_only_words"]["count"] == 1
    assert payload["oov_words"]["count"] == 1
    assert abs(payload["coverage_ratio"] - (2.0 / 3.0)) < 1e-6
    assert payload["oov_list"] == ["123"]
    assert isinstance(detail_payload["details"], list)
    assert len(detail_payload["details"]) == 3
