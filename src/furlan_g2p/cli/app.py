"""Command-line interface for FurlanG2P (skeleton)."""

from __future__ import annotations

import sys

import click

from ..services.pipeline import PipelineService


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli() -> None:
    """FurlanG2P command-line interface (skeleton)."""
    # click requires a function body
    pass


@cli.command("normalize")
@click.argument("text", nargs=-1)
def cmd_normalize(text: tuple[str, ...]) -> None:
    """Normalize text and print it."""
    PipelineService()
    _ = " ".join(text)
    raise NotImplementedError("normalize command is not implemented yet.")


@cli.command("g2p")
@click.argument("text", nargs=-1)
def cmd_g2p(text: tuple[str, ...]) -> None:
    """Convert text to phonemes and print them."""
    PipelineService()
    _ = " ".join(text)
    raise NotImplementedError("g2p command is not implemented yet.")


@cli.command("phonemize-csv")
@click.option("--in", "inp", required=True, help="Input metadata CSV (LJSpeech-like).")
@click.option("--out", "out", required=True, help="Output CSV with phonemes added.")
@click.option("--delim", "delim", default="|", show_default=True, help="CSV delimiter.")
def cmd_phonemize_csv(inp: str, out: str, delim: str) -> None:
    """Batch phonemize an LJSpeech-like CSV file."""
    PipelineService()
    raise NotImplementedError("phonemize-csv command is not implemented yet.")


def main() -> None:  # pragma: no cover - small wrapper
    try:
        cli(prog_name="furlang2p")
    except NotImplementedError as e:  # pragma: no cover - placeholder behaviour
        click.echo(f"[FurlanG2P skeleton] {e}", err=True)
        sys.exit(2)


__all__ = ["cli", "main"]
