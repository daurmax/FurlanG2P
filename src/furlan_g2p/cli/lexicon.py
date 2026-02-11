"""CLI commands for lexicon ingestion, inspection and export."""

from __future__ import annotations

import json
from pathlib import Path

import click

from ..lexicon import (
    LexiconBuilder,
    LexiconEntry,
    ValidationIssue,
    detect_format,
    read_jsonl,
    read_tsv,
    write_jsonl,
    write_tsv,
)

_WARNING_ISSUE_KINDS: set[str] = {"duplicate_pronunciation"}


def _issue_severity(issue: ValidationIssue) -> str:
    """Return severity level for a validation issue.

    Args:
        issue: Validation issue reported by ``LexiconBuilder``.

    Returns:
        Severity label (``"warning"`` or ``"error"``).
    """

    if issue.kind in _WARNING_ISSUE_KINDS:
        return "warning"
    return "error"


def _issue_as_dict(issue: ValidationIssue) -> dict[str, object]:
    """Serialize a ``ValidationIssue`` to a JSON-safe dictionary.

    Args:
        issue: Validation issue to serialize.

    Returns:
        Dictionary with issue attributes and severity.
    """

    payload: dict[str, object] = {
        "kind": issue.kind,
        "severity": _issue_severity(issue),
        "message": issue.message,
    }
    if issue.lemma is not None:
        payload["lemma"] = issue.lemma
    if issue.dialect is not None:
        payload["dialect"] = issue.dialect
    if issue.ipa is not None:
        payload["ipa"] = issue.ipa
    if issue.source is not None:
        payload["source"] = issue.source
    if issue.details:
        payload["details"] = issue.details
    return payload


def _format_issue(issue: ValidationIssue) -> str:
    """Return a compact single-line issue rendering.

    Args:
        issue: Validation issue to format.

    Returns:
        Human-readable issue line.
    """

    scope: list[str] = []
    if issue.lemma is not None:
        scope.append(f"lemma={issue.lemma}")
    if issue.dialect is not None:
        scope.append(f"dialect={issue.dialect}")
    scope_str = f" ({', '.join(scope)})" if scope else ""
    return f"{_issue_severity(issue).upper()} {issue.kind}{scope_str}: {issue.message}"


def _count_by_source(entries: list[LexiconEntry]) -> dict[str, int]:
    """Count entries grouped by source.

    Args:
        entries: Lexicon entries to aggregate.

    Returns:
        Mapping from source to number of entries.
    """

    counts: dict[str, int] = {}
    for entry in entries:
        counts[entry.source] = counts.get(entry.source, 0) + 1
    return counts


def _count_by_dialect(entries: list[LexiconEntry]) -> dict[str, int]:
    """Count entries grouped by dialect.

    Args:
        entries: Lexicon entries to aggregate.

    Returns:
        Mapping from dialect label to number of entries.
    """

    counts: dict[str, int] = {}
    for entry in entries:
        key = entry.dialect or "universal"
        counts[key] = counts.get(key, 0) + 1
    return counts


def _render_counts(counts: dict[str, int]) -> str:
    """Render count mappings as ``key=value`` pairs.

    Args:
        counts: Mapping to render.

    Returns:
        Comma-separated string sorted by key.
    """

    if not counts:
        return "-"
    return ", ".join(f"{key}={counts[key]}" for key in sorted(counts))


def _load_entries(path: Path) -> list[LexiconEntry]:
    """Read lexicon entries from a supported input format.

    Args:
        path: Input lexicon path.

    Returns:
        Parsed lexicon entries.

    Raises:
        click.ClickException: If the file extension is not supported.
    """

    file_format = detect_format(path)
    if file_format == "jsonl":
        return read_jsonl(path)
    if file_format == "tsv":
        return read_tsv(path, format="extended")
    raise click.ClickException(
        f"Unsupported lexicon format for '{path}'. Use .tsv/.txt or .jsonl/.ndjson."
    )


def _validate_entries(entries: list[LexiconEntry]) -> list[ValidationIssue]:
    """Run lexicon validation on an in-memory entry list.

    Args:
        entries: Entries to validate.

    Returns:
        Validation issues returned by ``LexiconBuilder``.
    """

    builder = LexiconBuilder()
    for entry in entries:
        builder.merge_entry(entry)
    return builder.validate()


@click.group(name="lexicon")
def lexicon() -> None:
    """Build, inspect, export and validate lexicon files."""


@lexicon.command("build")
@click.argument(
    "input_files",
    nargs=-1,
    required=True,
    type=click.Path(exists=True, dir_okay=False),
)
@click.option(
    "--output",
    "-o",
    "output_path",
    required=True,
    type=click.Path(dir_okay=False),
    help="Output lexicon file path.",
)
@click.option(
    "--format",
    "-f",
    "output_format",
    type=click.Choice(["tsv", "jsonl"], case_sensitive=False),
    default="jsonl",
    show_default=True,
    help="Output lexicon format.",
)
@click.option(
    "--source-type",
    type=click.Choice(["wikipron", "tsv", "manual"], case_sensitive=False),
    default="tsv",
    show_default=True,
    help="Input source kind used for confidence/source defaults.",
)
@click.option(
    "--dialect",
    type=str,
    default=None,
    help="Default dialect for entries without dialect metadata.",
)
@click.option(
    "--validate/--no-validate",
    "run_validation",
    default=True,
    show_default=True,
    help="Validate merged entries before reporting summary.",
)
@click.option("--verbose", "-v", is_flag=True, help="Show detailed import and validation output.")
def cmd_lexicon_build(
    input_files: tuple[str, ...],
    output_path: str,
    output_format: str,
    source_type: str,
    dialect: str | None,
    run_validation: bool,
    verbose: bool,
) -> None:
    """Build a merged lexicon from one or more source files."""

    builder = LexiconBuilder(default_dialect=dialect)
    input_paths = [Path(item) for item in input_files]
    output_target = Path(output_path)
    ingested_total = 0

    try:
        for input_file in input_paths:
            ingested = builder.add_source(input_file, source_type=source_type, dialect=dialect)
            ingested_total += ingested
            if verbose:
                click.echo(f"Ingested {ingested} entries from {input_file}")

        validation_issues = builder.validate() if run_validation else []
        export_format = "jsonl" if output_format.lower() == "jsonl" else "tsv_extended"
        builder.export(output_target, format=export_format)

        entries = builder.build()
        by_source = _count_by_source(entries)
        by_dialect = _count_by_dialect(entries)
        warning_count = sum(1 for issue in validation_issues if _issue_severity(issue) == "warning")
        error_count = len(validation_issues) - warning_count

        click.echo(f"Built lexicon with {len(entries)} entries ({ingested_total} ingested rows).")
        click.echo(f"Output: {output_target} ({output_format.lower()})")
        click.echo(f"Sources: {_render_counts(by_source)}")
        click.echo(f"Dialects: {_render_counts(by_dialect)}")
        if run_validation:
            click.echo(
                "Validation issues: "
                f"{len(validation_issues)} (errors={error_count}, warnings={warning_count})"
            )
            if verbose:
                for issue in validation_issues:
                    click.echo(_format_issue(issue))
        elif verbose:
            click.echo("Validation skipped.")
    except FileNotFoundError as exc:  # pragma: no cover - filesystem passthrough
        filename = exc.filename or str(output_target)
        raise click.FileError(filename) from exc
    except (TypeError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc
    except click.ClickException:
        raise
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise click.ClickException(str(exc)) from exc


@lexicon.command("info")
@click.argument("lexicon_file", type=click.Path(exists=True, dir_okay=False))
@click.option("--json", "as_json", is_flag=True, help="Emit stats as JSON.")
@click.option("--verbose", "-v", is_flag=True, help="Include detailed issue and dialect output.")
def cmd_lexicon_info(lexicon_file: str, as_json: bool, verbose: bool) -> None:
    """Inspect a lexicon file and print aggregated statistics."""

    try:
        lexicon_path = Path(lexicon_file)
        entries = _load_entries(lexicon_path)
        issues = _validate_entries(entries)

        by_source = _count_by_source(entries)
        by_dialect = _count_by_dialect(entries)
        alternatives_count = sum(1 for entry in entries if entry.alternatives)
        stress_count = sum(1 for entry in entries if entry.stress_marked)
        warning_count = sum(1 for issue in issues if _issue_severity(issue) == "warning")
        error_count = len(issues) - warning_count

        payload: dict[str, object] = {
            "file": str(lexicon_path),
            "total_entries": len(entries),
            "entries_by_dialect": by_dialect,
            "entries_by_source": by_source,
            "entries_with_alternatives": alternatives_count,
            "entries_with_stress_markers": stress_count,
            "validation": {
                "total_issues": len(issues),
                "errors": error_count,
                "warnings": warning_count,
                "issues": [_issue_as_dict(issue) for issue in issues],
            },
        }

        if as_json:
            click.echo(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
            return

        click.echo(f"Lexicon file: {lexicon_path}")
        click.echo(f"Total entries: {len(entries)}")
        click.echo(f"By source: {_render_counts(by_source)}")
        click.echo(f"By dialect: {_render_counts(by_dialect)}")
        click.echo(f"Entries with alternatives: {alternatives_count}")
        click.echo(f"Entries with stress markers: {stress_count}")
        click.echo(
            f"Validation issues: {len(issues)} (errors={error_count}, warnings={warning_count})"
        )
        if verbose and by_dialect:
            click.echo("Per-dialect breakdown:")
            for dialect_name in sorted(by_dialect):
                click.echo(f"  {dialect_name}: {by_dialect[dialect_name]}")
        if verbose and issues:
            click.echo("Validation details:")
            for issue in issues:
                click.echo(f"  {_format_issue(issue)}")
    except FileNotFoundError as exc:  # pragma: no cover - filesystem passthrough
        filename = exc.filename or str(lexicon_path)
        raise click.FileError(filename) from exc
    except (TypeError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc
    except click.ClickException:
        raise
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise click.ClickException(str(exc)) from exc


@lexicon.command("export")
@click.argument("input_file", type=click.Path(exists=True, dir_okay=False))
@click.argument("output_file", type=click.Path(dir_okay=False))
@click.option(
    "--format",
    "-f",
    "output_format",
    type=click.Choice(["tsv", "jsonl", "tsv-simple"], case_sensitive=False),
    default="jsonl",
    show_default=True,
    help="Destination file format.",
)
@click.option("--dialect", type=str, default=None, help="Export only entries for this dialect.")
@click.option(
    "--min-confidence",
    type=click.FloatRange(min=0.0, max=1.0),
    default=None,
    help="Keep only entries with confidence >= threshold.",
)
def cmd_lexicon_export(
    input_file: str,
    output_file: str,
    output_format: str,
    dialect: str | None,
    min_confidence: float | None,
) -> None:
    """Convert lexicon files between supported formats with optional filtering."""

    try:
        input_path = Path(input_file)
        output_path = Path(output_file)
        entries = _load_entries(input_path)
        filtered = entries

        if dialect is not None:
            dialect_value = dialect.strip().lower()
            filtered = [
                entry
                for entry in filtered
                if entry.dialect is not None and entry.dialect == dialect_value
            ]
        if min_confidence is not None:
            filtered = [entry for entry in filtered if entry.confidence >= min_confidence]

        normalized_format = output_format.lower()
        if normalized_format == "jsonl":
            write_jsonl(filtered, output_path)
        elif normalized_format == "tsv":
            write_tsv(filtered, output_path, format="extended")
        else:
            write_tsv(filtered, output_path, format="simple")

        click.echo(
            "Exported "
            f"{len(filtered)} of {len(entries)} entries to {output_path} ({normalized_format})."
        )
    except FileNotFoundError as exc:  # pragma: no cover - filesystem passthrough
        filename = exc.filename or str(input_path)
        raise click.FileError(filename) from exc
    except (TypeError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc
    except click.ClickException:
        raise
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise click.ClickException(str(exc)) from exc


@lexicon.command("validate")
@click.argument("lexicon_file", type=click.Path(exists=True, dir_okay=False))
@click.option("--strict", is_flag=True, help="Treat warnings as errors.")
@click.option("--json", "as_json", is_flag=True, help="Emit validation report as JSON.")
def cmd_lexicon_validate(lexicon_file: str, strict: bool, as_json: bool) -> None:
    """Validate a lexicon file and return a process status code."""

    try:
        lexicon_path = Path(lexicon_file)
        entries = _load_entries(lexicon_path)
        issues = _validate_entries(entries)
        warning_count = sum(1 for issue in issues if _issue_severity(issue) == "warning")
        error_count = len(issues) - warning_count
        is_valid = error_count == 0 and (warning_count == 0 or not strict)
        exit_code = 0 if is_valid else 1

        if as_json:
            payload = {
                "file": str(lexicon_path),
                "entry_count": len(entries),
                "strict": strict,
                "valid": is_valid,
                "errors": error_count,
                "warnings": warning_count,
                "issues": [_issue_as_dict(issue) for issue in issues],
            }
            click.echo(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        else:
            if issues:
                for issue in issues:
                    click.echo(_format_issue(issue))
            else:
                click.echo("No validation issues found.")
            click.echo(
                "Summary: "
                f"errors={error_count}, warnings={warning_count}, strict={str(strict).lower()}"
            )

        if exit_code != 0:
            raise click.exceptions.Exit(exit_code)
    except FileNotFoundError as exc:  # pragma: no cover - filesystem passthrough
        filename = exc.filename or str(lexicon_path)
        raise click.FileError(filename) from exc
    except (TypeError, ValueError) as exc:
        raise click.ClickException(str(exc)) from exc
    except click.ClickException:
        raise
    except Exception as exc:  # pragma: no cover - defensive fallback
        raise click.ClickException(str(exc)) from exc


__all__ = ["lexicon"]
