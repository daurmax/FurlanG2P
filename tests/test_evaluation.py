from __future__ import annotations

from pathlib import Path

import pytest

from furlan_g2p.evaluation.metrics import (
    Evaluator,
    _extract_stress_position,
    _levenshtein_distance,
    _normalize_ipa,
    _tokenize_phonemes,
)


def test_normalize_ipa_handles_unicode_and_punctuation() -> None:
    assert _normalize_ipa(" t͡ʃ, g. ") == "tʃɡ"


def test_tokenize_phonemes_groups_combining_diacritics() -> None:
    assert _tokenize_phonemes("a\u0303b") == ["a\u0303", "b"]


def test_levenshtein_distance_basic_cases() -> None:
    assert _levenshtein_distance(["a"], ["a"]) == 0
    assert _levenshtein_distance(["a"], ["b"]) == 1
    assert _levenshtein_distance(["a", "b"], ["a"]) == 1


@pytest.mark.parametrize(
    ("predictions", "gold", "expected"),
    [
        (["ˈcaze"], ["ˈcaze"], 0.0),
        (["ˈcaze"], ["ˈkaze"], 1.0),
        (["ˈcaze", "ˈaɡe"], ["ˈcaze", "ˈaʒe"], 0.5),
        ([], [], 0.0),
        (["g"], ["ɡ"], 0.0),
    ],
)
def test_word_error_rate_cases(
    predictions: list[str],
    gold: list[str],
    expected: float,
) -> None:
    evaluator = Evaluator()
    assert evaluator.word_error_rate(predictions, gold) == pytest.approx(expected)


def test_word_error_rate_length_mismatch_raises() -> None:
    evaluator = Evaluator()
    with pytest.raises(ValueError, match="Length mismatch"):
        evaluator.word_error_rate(["a"], [])


@pytest.mark.parametrize(
    ("predictions", "gold", "expected"),
    [
        (["ˈcaze"], ["ˈcaze"], 0.0),
        (["a"], ["b"], 1.0),
        (["ab"], ["a"], 1.0),
        (["a"], ["ab"], 0.5),
        (["a\u0303"], ["ã"], 0.0),
        ([], [], 0.0),
    ],
)
def test_phoneme_error_rate_cases(
    predictions: list[str],
    gold: list[str],
    expected: float,
) -> None:
    evaluator = Evaluator()
    assert evaluator.phoneme_error_rate(predictions, gold) == pytest.approx(expected)


def test_phoneme_error_rate_length_mismatch_raises() -> None:
    evaluator = Evaluator()
    with pytest.raises(ValueError, match="Length mismatch"):
        evaluator.phoneme_error_rate(["a"], [])


@pytest.mark.parametrize(
    ("predictions", "gold", "expected"),
    [
        (["ˈcaze"], ["ˈcaze"], 1.0),
        (["caˈze"], ["ˈcaze"], 0.0),
        (["caze"], ["ˈcaze"], 0.0),
        (["ˈcaˈze"], ["ˈcaze"], 1.0),
        (["ˈcaze"], ["caze"], 0.0),
    ],
)
def test_stress_accuracy_cases(
    predictions: list[str],
    gold: list[str],
    expected: float,
) -> None:
    evaluator = Evaluator()
    assert evaluator.stress_accuracy(predictions, gold) == pytest.approx(expected)


def test_stress_accuracy_length_mismatch_raises() -> None:
    evaluator = Evaluator()
    with pytest.raises(ValueError, match="Length mismatch"):
        evaluator.stress_accuracy(["ˈcaze"], [])


def test_extract_stress_position() -> None:
    assert _extract_stress_position("ˈcaze") == 0
    assert _extract_stress_position("caˈze") == 2
    assert _extract_stress_position("caze") is None


def test_evaluate_returns_aggregate_and_details() -> None:
    evaluator = Evaluator()
    result = evaluator.evaluate(
        predictions=[("cjase", "ˈcaze"), ("aghe", "ˈaɡe")],
        gold=[("cjase", "ˈkaze"), ("aghe", "ˈaɡe")],
    )

    assert result.word_count == 2
    assert result.correct_count == 1
    assert result.wer == pytest.approx(0.5)
    assert result.per == pytest.approx(1.0 / 9.0)
    assert result.stress_accuracy == pytest.approx(1.0)
    assert len(result.details) == 2
    assert result.details[0].is_correct is False
    assert result.details[1].is_correct is True


def test_evaluate_length_mismatch_raises() -> None:
    evaluator = Evaluator()
    with pytest.raises(ValueError, match="Length mismatch"):
        evaluator.evaluate([("cjase", "ˈcaze")], [])


def test_evaluate_empty_lists_returns_zero_metrics() -> None:
    evaluator = Evaluator()
    result = evaluator.evaluate([], [])
    assert result.wer == 0.0
    assert result.per == 0.0
    assert result.stress_accuracy == 0.0
    assert result.word_count == 0
    assert result.correct_count == 0
    assert result.details == []


def test_evaluate_from_tsv_supports_dialect_filter(tmp_path: Path) -> None:
    gold_path = tmp_path / "gold.tsv"
    gold_path.write_text(
        "\n".join(
            [
                "# comment",
                "cjase\tˈcaze\tcentral",
                "aghe\tˈaɡe\twestern",
                "none\tˈnone\tcentral",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    predictions = {"cjase": "ˈcaze", "aghe": "ˈake"}

    evaluator = Evaluator()
    result = evaluator.evaluate_from_tsv(
        gold_path,
        predictions=predictions,
        dialect_filter="central",
    )

    assert result.word_count == 1
    assert result.correct_count == 1
    assert result.wer == 0.0


def test_evaluate_from_tsv_invalid_row_raises(tmp_path: Path) -> None:
    gold_path = tmp_path / "gold.tsv"
    gold_path.write_text("bad-row\n", encoding="utf-8")

    evaluator = Evaluator()
    with pytest.raises(ValueError, match="Invalid TSV format"):
        evaluator.evaluate_from_tsv(gold_path, predictions={"cjase": "ˈcaze"})


def test_evaluate_from_tsv_missing_file_raises(tmp_path: Path) -> None:
    evaluator = Evaluator()
    with pytest.raises(FileNotFoundError):
        evaluator.evaluate_from_tsv(tmp_path / "missing.tsv", predictions={})
