"""I/O operations for lexicon data in TSV and JSONL formats."""

from __future__ import annotations

import csv
import json
import logging
from pathlib import Path
from typing import Literal

from .schema import LexiconEntry

logger = logging.getLogger(__name__)

FormatType = Literal["simple", "extended"]
FileFormat = Literal["tsv", "jsonl", "unknown"]


def detect_format(path: Path) -> FileFormat:
    """Detect the file format based on extension.

    Parameters
    ----------
    path : Path
        Path to the file to detect.

    Returns
    -------
    FileFormat
        One of "tsv", "jsonl", or "unknown".

    Examples
    --------
    >>> detect_format(Path("lexicon.tsv"))
    'tsv'
    >>> detect_format(Path("lexicon.jsonl"))
    'jsonl'
    """
    suffix = path.suffix.lower()
    if suffix in {".tsv", ".txt"}:
        return "tsv"
    if suffix in {".jsonl", ".ndjson"}:
        return "jsonl"
    return "unknown"


def read_tsv(path: Path, format: FormatType = "simple") -> list[LexiconEntry]:
    """Read lexicon entries from a TSV file.

    Supports two formats:
    - "simple": lemma\\tipa (2 columns, backward compatible)
    - "extended": lemma\\tipa\\tdialect\\tsource\\tconfidence (5 columns)

    The function auto-detects format based on the number of columns.
    For simple format, uses default values for extended fields.

    Parameters
    ----------
    path : Path
        Path to the TSV file.
    format : FormatType, optional
        Expected format ("simple" or "extended"). Auto-detected if not specified.

    Returns
    -------
    list[LexiconEntry]
        List of lexicon entries read from the file.

    Examples
    --------
    >>> entries = read_tsv(Path("seed_lexicon.tsv"))
    >>> len(entries) > 0
    True
    """
    entries: list[LexiconEntry] = []

    with path.open("r", encoding="utf-8-sig") as f:
        reader = csv.reader(f, delimiter="\t")

        for line_num, row in enumerate(reader, start=1):
            # Skip empty rows
            if not row or all(not cell.strip() for cell in row):
                continue

            # Skip header row if it looks like a header
            if line_num == 1 and len(row) > 0 and row[0].lower() in {"word", "lemma"}:
                continue

            try:
                if len(row) < 2:
                    logger.warning(f"Line {line_num}: insufficient columns, skipping")
                    continue

                lemma = row[0].strip()
                ipa = row[1].strip()

                # Basic validation
                if not lemma or not ipa:
                    logger.warning(f"Line {line_num}: empty lemma or ipa, skipping")
                    continue

                # Extended format: parse additional fields
                dialect: str | None = None
                source = "unknown"
                confidence = 1.0
                frequency: int | None = None
                alternatives: list[str] = []

                if len(row) >= 3 and row[2].strip():
                    dialect = row[2].strip() if row[2].strip().lower() != "none" else None

                if len(row) >= 4 and row[3].strip():
                    source = row[3].strip()

                if len(row) >= 5 and row[4].strip():
                    try:
                        confidence = float(row[4].strip())
                    except ValueError:
                        logger.warning(
                            f"Line {line_num}: invalid confidence '{row[4]}', using default 1.0"
                        )

                if len(row) >= 6 and row[5].strip():
                    try:
                        frequency = int(row[5].strip())
                    except ValueError:
                        logger.warning(f"Line {line_num}: invalid frequency '{row[5]}', using None")

                # Parse alternatives if present (JSON array)
                if len(row) >= 7 and row[6].strip():
                    try:
                        alternatives = json.loads(row[6].strip())
                        if not isinstance(alternatives, list):
                            alternatives = []
                            logger.warning(
                                f"Line {line_num}: alternatives not a list, using empty list"
                            )
                    except json.JSONDecodeError:
                        logger.warning(
                            f"Line {line_num}: invalid JSON in alternatives, using empty list"
                        )

                entry = LexiconEntry(
                    lemma=lemma,
                    ipa=ipa,
                    dialect=dialect,
                    source=source,
                    confidence=confidence,
                    frequency=frequency,
                    alternatives=alternatives,
                )
                entries.append(entry)

            except ValueError as e:
                logger.warning(f"Line {line_num}: validation error - {e}")
                continue
            except Exception as e:
                logger.warning(f"Line {line_num}: unexpected error - {e}")
                continue

    logger.info(f"Loaded {len(entries)} entries from {path}")
    return entries


def write_tsv(entries: list[LexiconEntry], path: Path, format: FormatType = "simple") -> None:
    """Write lexicon entries to a TSV file.

    Parameters
    ----------
    entries : list[LexiconEntry]
        List of lexicon entries to write.
    path : Path
        Output path for the TSV file.
    format : FormatType, optional
        Format to use ("simple" or "extended").

    Examples
    --------
    >>> entries = [LexiconEntry(lemma="test", ipa="test")]
    >>> write_tsv(entries, Path("output.tsv"), format="simple")
    """
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")

        # Write header
        if format == "simple":
            writer.writerow(["lemma", "ipa"])
        else:
            writer.writerow(
                ["lemma", "ipa", "dialect", "source", "confidence", "frequency", "alternatives"]
            )

        for entry in entries:
            if format == "simple":
                writer.writerow([entry.lemma, entry.ipa])
            else:
                dialect_str = entry.dialect if entry.dialect is not None else ""
                freq_str = str(entry.frequency) if entry.frequency is not None else ""
                alts_str = json.dumps(entry.alternatives) if entry.alternatives else "[]"

                writer.writerow(
                    [
                        entry.lemma,
                        entry.ipa,
                        dialect_str,
                        entry.source,
                        str(entry.confidence),
                        freq_str,
                        alts_str,
                    ]
                )

    logger.info(f"Wrote {len(entries)} entries to {path} (format={format})")


def read_jsonl(path: Path) -> list[LexiconEntry]:
    """Read lexicon entries from a JSONL file.

    Each line should contain a JSON object with LexiconEntry fields.

    Parameters
    ----------
    path : Path
        Path to the JSONL file.

    Returns
    -------
    list[LexiconEntry]
        List of lexicon entries read from the file.

    Examples
    --------
    >>> entries = read_jsonl(Path("lexicon.jsonl"))
    >>> isinstance(entries, list)
    True
    """
    entries: list[LexiconEntry] = []

    with path.open("r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                data = json.loads(line)

                # Handle missing fields with defaults
                entry = LexiconEntry(
                    lemma=data["lemma"],
                    ipa=data["ipa"],
                    dialect=data.get("dialect"),
                    source=data.get("source", "unknown"),
                    confidence=data.get("confidence", 1.0),
                    frequency=data.get("frequency"),
                    alternatives=data.get("alternatives", []),
                )
                entries.append(entry)

            except KeyError as e:
                logger.warning(f"Line {line_num}: missing required field {e}")
                continue
            except json.JSONDecodeError as e:
                logger.warning(f"Line {line_num}: invalid JSON - {e}")
                continue
            except ValueError as e:
                logger.warning(f"Line {line_num}: validation error - {e}")
                continue
            except Exception as e:
                logger.warning(f"Line {line_num}: unexpected error - {e}")
                continue

    logger.info(f"Loaded {len(entries)} entries from {path}")
    return entries


def write_jsonl(entries: list[LexiconEntry], path: Path) -> None:
    """Write lexicon entries to a JSONL file.

    Each entry is written as a single-line JSON object.

    Parameters
    ----------
    entries : list[LexiconEntry]
        List of lexicon entries to write.
    path : Path
        Output path for the JSONL file.

    Examples
    --------
    >>> entries = [LexiconEntry(lemma="test", ipa="test")]
    >>> write_jsonl(entries, Path("output.jsonl"))
    """
    with path.open("w", encoding="utf-8") as f:
        for entry in entries:
            data = {
                "lemma": entry.lemma,
                "ipa": entry.ipa,
                "dialect": entry.dialect,
                "source": entry.source,
                "confidence": entry.confidence,
                "frequency": entry.frequency,
                "alternatives": entry.alternatives,
            }
            json.dump(data, f, ensure_ascii=False)
            f.write("\n")

    logger.info(f"Wrote {len(entries)} entries to {path}")


__all__ = [
    "detect_format",
    "read_tsv",
    "write_tsv",
    "read_jsonl",
    "write_jsonl",
    "FormatType",
    "FileFormat",
]
