"""CLI commands for evaluation and coverage analysis."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import click

from ..evaluation import EvaluationResult, Evaluator, WordResult
from ..g2p.lexicon import Lexicon
from ..g2p.phonemizer import G2PPhonemizer
from ..g2p.rules import PhonemeRules
from ..services.pipeline import PipelineService

OutputFormat = Literal["text", "json"]
CoverageStatus = Literal["lexicon", "rule_only", "oov"]


@dataclass(frozen=True)
class GoldEntry:
    """A single row from the gold TSV set."""

    word: str
    ipa: str
    dialect: str | None


@dataclass(frozen=True)
class CoverageRecord:
    """Classification for one word in coverage analysis."""

    word: str
    status: CoverageStatus


@dataclass(frozen=True)
class CoverageReport:
    """Aggregate coverage statistics and detailed classifications."""

    total_words: int
    lexicon_hits: int
    rule_only_hits: int
    oov_hits: int
    records: list[CoverageRecord]


def _format_percent(value: float) -> str:
    """Return ``value`` as a percentage string with two decimals."""

    return f"{value * 100.0:.2f}%"


def _ratio(count: int, total: int) -> float:
    """Return ``count / total`` or ``0.0`` when ``total`` is zero."""

    return float(count) / float(total) if total > 0 else 0.0


def _load_gold_entries(path: Path) -> list[GoldEntry]:
    """Parse a gold TSV file into ``GoldEntry`` rows.

    Args:
        path: TSV path in ``word\\tipa`` or ``word\\tipa\\tdialect`` format.

    Returns:
        Parsed gold entries.

    Raises:
        ValueError: If the TSV contains malformed rows.
    """

    entries: list[GoldEntry] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_num, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            parts = [value.strip() for value in line.split("\t")]
            if len(parts) < 2:
                raise ValueError(
                    f"Invalid gold TSV at line {line_num}: expected at least 2 columns"
                )

            word = parts[0]
            ipa = parts[1]
            dialect = parts[2] if len(parts) >= 3 and parts[2] else None
            if not word or not ipa:
                raise ValueError(
                    f"Invalid gold TSV at line {line_num}: word and IPA must be non-empty"
                )

            entries.append(GoldEntry(word=word, ipa=ipa, dialect=dialect))

    if not entries:
        raise ValueError("Gold file is empty or contains only comments/blank lines")
    return entries


def _load_wordlist(path: Path) -> list[str]:
    """Read a one-word-per-line wordlist.

    Args:
        path: Wordlist file path.

    Returns:
        Non-empty word list.

    Raises:
        ValueError: If the wordlist contains no usable words.
    """

    words: list[str] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            words.append(line)

    if not words:
        raise ValueError("Wordlist is empty or contains only comments/blank lines")
    return words


def _build_pipeline(lexicon_path: Path | None) -> PipelineService:
    """Construct a ``PipelineService`` with optional custom lexicon."""

    if lexicon_path is None:
        return PipelineService()
    lexicon = Lexicon.load(lexicon_path)
    phonemizer = G2PPhonemizer(lexicon=lexicon)
    return PipelineService(phonemizer=phonemizer)


def _build_lexicon(lexicon_path: Path | None) -> Lexicon:
    """Load the seed lexicon or a custom lexicon path."""

    if lexicon_path is None:
        return Lexicon.load_seed()
    return Lexicon.load(lexicon_path)


def _predict_ipa(
    service: PipelineService,
    word: str,
    dialect: str | None,
) -> str:
    """Generate IPA for ``word`` via pipeline output flattening."""

    _normalized, phonemes = service.process_text(word, dialect=dialect)
    return "".join(phonemes)


def _word_result_to_payload(result: WordResult) -> dict[str, object]:
    """Serialize a ``WordResult`` into a JSON-safe dictionary."""

    return {
        "word": result.word,
        "predicted": result.predicted,
        "expected": result.gold,
        "is_correct": result.is_correct,
        "phoneme_distance": result.phoneme_distance,
    }


def _build_evaluation_payload(
    result: EvaluationResult,
    gold_file: Path,
    dialect: str | None,
    failures: list[tuple[str, str]],
    include_details: bool,
) -> dict[str, object]:
    """Build a JSON payload for evaluation output."""

    payload: dict[str, object] = {
        "gold_file": str(gold_file),
        "dialect": dialect,
        "word_count": result.word_count,
        "correct_count": result.correct_count,
        "error_count": result.word_count - result.correct_count,
        "wer": result.wer,
        "per": result.per,
        "stress_accuracy": result.stress_accuracy,
        "errors": [
            _word_result_to_payload(detail) for detail in result.details if not detail.is_correct
        ],
        "prediction_failures": [{"word": word, "error": error} for word, error in failures],
    }
    if include_details:
        payload["details"] = [_word_result_to_payload(detail) for detail in result.details]
    return payload


def _format_evaluation_text(
    result: EvaluationResult,
    show_errors: bool,
    include_details: bool,
    failures: list[tuple[str, str]],
) -> str:
    """Render evaluation metrics in human-readable text."""

    lines = [
        f"Total words evaluated: {result.word_count}",
        f"Correct words: {result.correct_count}",
        f"WER: {result.wer:.4f} ({_format_percent(result.wer)})",
        f"PER: {result.per:.4f}",
        (
            "Stress accuracy: "
            f"{result.stress_accuracy:.4f} ({_format_percent(result.stress_accuracy)})"
        ),
    ]

    if failures:
        lines.append(f"Prediction failures: {len(failures)}")

    if include_details:
        lines.append("Details:")
        for detail in result.details:
            status = "OK" if detail.is_correct else "ERR"
            lines.append(
                f"{status}\t{detail.word}\tpredicted={detail.predicted}\t"
                f"expected={detail.gold}\tdistance={detail.phoneme_distance:.0f}"
            )
    elif show_errors:
        errors = [detail for detail in result.details if not detail.is_correct]
        if not errors:
            lines.append("Errors: none")
        else:
            lines.append("Errors:")
            for detail in errors:
                lines.append(f"{detail.word}\tpredicted={detail.predicted}\texpected={detail.gold}")

    if failures and (show_errors or include_details):
        lines.append("Prediction failure details:")
        for word, error in failures:
            lines.append(f"{word}\terror={error}")

    return "\n".join(lines)


def _classify_word(
    word: str,
    lexicon: Lexicon,
    rules: PhonemeRules,
    dialect: str | None,
) -> CoverageStatus:
    """Classify a word as lexicon, rule-only, or OOV."""

    if lexicon.has_entry(word, dialect=dialect):
        return "lexicon"
    try:
        rule_output = rules.apply(word, dialect=dialect)
    except ValueError:
        return "oov"
    return "rule_only" if rule_output else "oov"


def _analyze_coverage(
    words: list[str],
    lexicon: Lexicon,
    rules: PhonemeRules,
    dialect: str | None,
) -> CoverageReport:
    """Compute coverage classifications and aggregate counters."""

    records = [
        CoverageRecord(word=word, status=_classify_word(word, lexicon, rules, dialect))
        for word in words
    ]
    lexicon_hits = sum(1 for item in records if item.status == "lexicon")
    rule_only_hits = sum(1 for item in records if item.status == "rule_only")
    oov_hits = sum(1 for item in records if item.status == "oov")
    return CoverageReport(
        total_words=len(records),
        lexicon_hits=lexicon_hits,
        rule_only_hits=rule_only_hits,
        oov_hits=oov_hits,
        records=records,
    )


def _build_coverage_payload(
    report: CoverageReport,
    wordlist_file: Path,
    dialect: str | None,
    include_details: bool,
    include_oov_words: bool,
) -> dict[str, object]:
    """Build a JSON payload for coverage output."""

    total = report.total_words
    lexicon_ratio = _ratio(report.lexicon_hits, total)
    rule_only_ratio = _ratio(report.rule_only_hits, total)
    oov_ratio = _ratio(report.oov_hits, total)
    coverage_ratio = _ratio(report.lexicon_hits + report.rule_only_hits, total)

    payload: dict[str, object] = {
        "wordlist_file": str(wordlist_file),
        "dialect": dialect,
        "total_words": total,
        "lexicon_hits": {"count": report.lexicon_hits, "ratio": lexicon_ratio},
        "rule_only_words": {"count": report.rule_only_hits, "ratio": rule_only_ratio},
        "oov_words": {"count": report.oov_hits, "ratio": oov_ratio},
        "coverage_ratio": coverage_ratio,
    }

    if include_oov_words:
        payload["oov_list"] = sorted({item.word for item in report.records if item.status == "oov"})

    if include_details:
        payload["details"] = [{"word": item.word, "status": item.status} for item in report.records]

    return payload


def _format_coverage_text(
    report: CoverageReport,
    show_oov: bool,
    include_details: bool,
) -> str:
    """Render coverage metrics in human-readable text."""

    total = report.total_words
    lexicon_ratio = _ratio(report.lexicon_hits, total)
    rule_only_ratio = _ratio(report.rule_only_hits, total)
    oov_ratio = _ratio(report.oov_hits, total)
    coverage_ratio = _ratio(report.lexicon_hits + report.rule_only_hits, total)

    lines = [
        f"Total words: {total}",
        f"Lexicon hits: {report.lexicon_hits} ({_format_percent(lexicon_ratio)})",
        f"Rule-only words: {report.rule_only_hits} ({_format_percent(rule_only_ratio)})",
        f"OOV words: {report.oov_hits} ({_format_percent(oov_ratio)})",
        f"Coverage: {_format_percent(coverage_ratio)}",
    ]

    if show_oov:
        oov_words = sorted({item.word for item in report.records if item.status == "oov"})
        if oov_words:
            lines.append("OOV list:")
            lines.extend(oov_words)
        else:
            lines.append("OOV list: none")

    if include_details:
        lines.append("Details:")
        lines.extend(f"{item.word}\t{item.status}" for item in report.records)

    return "\n".join(lines)


def _render_json(payload: dict[str, object]) -> str:
    """Serialize payload as indented UTF-8 JSON."""

    return json.dumps(payload, ensure_ascii=False, indent=2)


def _emit_output(content: str, output_path: Path | None) -> None:
    """Write content to stdout or a file."""

    if output_path is None:
        click.echo(content)
        return
    output_path.write_text(content, encoding="utf-8")


@click.command("evaluate")
@click.argument("gold_file", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--dialect",
    "dialect",
    type=str,
    default=None,
    help="Dialect override for prediction.",
)
@click.option(
    "--output",
    "-o",
    "output_path",
    type=click.Path(dir_okay=False),
    default=None,
    help="Write detailed results to file.",
)
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["text", "json"], case_sensitive=False),
    default="text",
    show_default=True,
    help="Output format.",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Show per-word errors.",
)
@click.option(
    "--lexicon",
    "lexicon_path",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="Custom lexicon TSV/JSONL path.",
)
def evaluate_command(
    gold_file: str,
    dialect: str | None,
    output_path: str | None,
    fmt: OutputFormat,
    verbose: bool,
    lexicon_path: str | None,
) -> None:
    """Evaluate G2P output against a gold TSV file."""

    gold_file_path = Path(gold_file)
    output_file_path = Path(output_path) if output_path is not None else None
    lexicon_file_path = Path(lexicon_path) if lexicon_path is not None else None

    try:
        gold_entries = _load_gold_entries(gold_file_path)
        service = _build_pipeline(lexicon_file_path)
        evaluator = Evaluator()
    except (OSError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc

    predictions: list[tuple[str, str]] = []
    gold: list[tuple[str, str]] = []
    failures: list[tuple[str, str]] = []

    for entry in gold_entries:
        active_dialect = dialect or entry.dialect
        try:
            predicted = _predict_ipa(service, entry.word, dialect=active_dialect)
        except Exception as exc:  # pragma: no cover - defensive CLI fallback
            predicted = ""
            failures.append((entry.word, str(exc)))
        predictions.append((entry.word, predicted))
        gold.append((entry.word, entry.ipa))

    result = evaluator.evaluate(predictions, gold)
    summary_payload = _build_evaluation_payload(
        result=result,
        gold_file=gold_file_path,
        dialect=dialect,
        failures=failures,
        include_details=verbose,
    )
    stdout_content = (
        _render_json(summary_payload)
        if fmt == "json"
        else _format_evaluation_text(
            result=result,
            show_errors=verbose,
            include_details=False,
            failures=failures,
        )
    )
    click.echo(stdout_content)

    if output_path is not None:
        detailed_payload = _build_evaluation_payload(
            result=result,
            gold_file=gold_file_path,
            dialect=dialect,
            failures=failures,
            include_details=True,
        )
        detailed_content = (
            _render_json(detailed_payload)
            if fmt == "json"
            else _format_evaluation_text(
                result=result,
                show_errors=True,
                include_details=True,
                failures=failures,
            )
        )
        _emit_output(detailed_content, output_file_path)


@click.command("coverage")
@click.argument("wordlist_file", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--lexicon",
    "lexicon_path",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="Custom lexicon TSV/JSONL path.",
)
@click.option(
    "--dialect",
    "dialect",
    type=str,
    default=None,
    help="Dialect for lookup and rules.",
)
@click.option(
    "--output",
    "-o",
    "output_path",
    type=click.Path(dir_okay=False),
    default=None,
    help="Write detailed results to file.",
)
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["text", "json"], case_sensitive=False),
    default="text",
    show_default=True,
    help="Output format.",
)
@click.option(
    "--show-oov",
    is_flag=True,
    default=False,
    help="Include OOV word list in output.",
)
def coverage_command(
    wordlist_file: str,
    lexicon_path: str | None,
    dialect: str | None,
    output_path: str | None,
    fmt: OutputFormat,
    show_oov: bool,
) -> None:
    """Analyze lexicon/rule coverage for a wordlist."""

    wordlist_file_path = Path(wordlist_file)
    output_file_path = Path(output_path) if output_path is not None else None
    lexicon_file_path = Path(lexicon_path) if lexicon_path is not None else None

    try:
        words = _load_wordlist(wordlist_file_path)
        lexicon = _build_lexicon(lexicon_file_path)
        rules = PhonemeRules()
    except (OSError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc

    report = _analyze_coverage(words=words, lexicon=lexicon, rules=rules, dialect=dialect)
    summary_payload = _build_coverage_payload(
        report=report,
        wordlist_file=wordlist_file_path,
        dialect=dialect,
        include_details=False,
        include_oov_words=show_oov,
    )
    stdout_content = (
        _render_json(summary_payload)
        if fmt == "json"
        else _format_coverage_text(report=report, show_oov=show_oov, include_details=False)
    )
    click.echo(stdout_content)

    if output_path is not None:
        detailed_payload = _build_coverage_payload(
            report=report,
            wordlist_file=wordlist_file_path,
            dialect=dialect,
            include_details=True,
            include_oov_words=True,
        )
        detailed_content = (
            _render_json(detailed_payload)
            if fmt == "json"
            else _format_coverage_text(report=report, show_oov=True, include_details=True)
        )
        _emit_output(detailed_content, output_file_path)


__all__ = ["evaluate_command", "coverage_command"]
