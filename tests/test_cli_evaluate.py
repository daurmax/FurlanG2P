from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from furlan_g2p.cli.app import cli


def test_evaluate_help_text(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(cli, ["evaluate", "--help"])
    assert result.exit_code == 0
    assert "--dialect" in result.output
    assert "--output" in result.output
    assert "--format" in result.output
    assert "--verbose" in result.output


def test_evaluate_command_text_output(sample_gold_set_file: Path, cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(cli, ["evaluate", str(sample_gold_set_file)])

    assert result.exit_code == 0
    assert "Total words evaluated: 2" in result.output
    assert "WER:" in result.output
    assert "PER:" in result.output
    assert "Stress accuracy:" in result.output


def test_evaluate_command_json_output_and_details_file(
    sample_gold_set_file: Path,
    tmp_path: Path,
    cli_runner: CliRunner,
) -> None:
    output_path = tmp_path / "evaluation.json"
    result = cli_runner.invoke(
        cli,
        [
            "evaluate",
            str(sample_gold_set_file),
            "--format",
            "json",
            "--output",
            str(output_path),
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    detailed_payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["word_count"] == 2
    assert "details" not in payload
    assert len(detailed_payload["details"]) == 2


def test_evaluate_command_invalid_gold_file_exits_nonzero(
    tmp_path: Path,
    cli_runner: CliRunner,
) -> None:
    gold_file = tmp_path / "bad_gold.tsv"
    gold_file.write_text("invalid_row_without_ipa\n", encoding="utf-8")

    result = cli_runner.invoke(cli, ["evaluate", str(gold_file)])

    assert result.exit_code != 0
    assert "Invalid gold TSV" in result.output


def test_coverage_help_text(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(cli, ["coverage", "--help"])
    assert result.exit_code == 0
    assert "--lexicon" in result.output
    assert "--dialect" in result.output
    assert "--output" in result.output
    assert "--format" in result.output
    assert "--show-oov" in result.output


def test_coverage_command_text_output(
    sample_wordlist_file: Path,
    cli_runner: CliRunner,
) -> None:
    result = cli_runner.invoke(cli, ["coverage", str(sample_wordlist_file), "--show-oov"])

    assert result.exit_code == 0
    assert "Total words:" in result.output
    assert "Lexicon hits:" in result.output
    assert "Rule-only words:" in result.output
    assert "OOV words:" in result.output
    assert "OOV list:" in result.output


def test_coverage_command_json_output_and_details_file(
    sample_wordlist_file: Path,
    tmp_path: Path,
    cli_runner: CliRunner,
) -> None:
    output_path = tmp_path / "coverage.json"
    result = cli_runner.invoke(
        cli,
        [
            "coverage",
            str(sample_wordlist_file),
            "--format",
            "json",
            "--show-oov",
            "--output",
            str(output_path),
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.output)
    detailed_payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["total_words"] == 3
    assert "details" not in payload
    assert len(detailed_payload["details"]) == 3


def test_coverage_command_empty_wordlist_exits_nonzero(
    tmp_path: Path,
    cli_runner: CliRunner,
) -> None:
    wordlist_file = tmp_path / "empty.txt"
    wordlist_file.write_text("# comment only\n", encoding="utf-8")

    result = cli_runner.invoke(cli, ["coverage", str(wordlist_file)])

    assert result.exit_code != 0
    assert "Wordlist is empty" in result.output
