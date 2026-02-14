# Lexicon Schema & Storage Agent Prompt

> Define lexicon data schema and storage formats (TSV/JSONL) with dialect and confidence support.

---

## READ FIRST

1. `README.md` — Project overview
2. `AGENTS.md` — Agent guidelines
3. `src/furlan_g2p/g2p/lexicon.py` — Current lexicon implementation
4. `src/furlan_g2p/core/types.py` — Type definition patterns
5. `src/furlan_g2p/data/` — Current seed lexicon location
6. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/00_request.md` — Full requirements
7. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/01_plan.md` — Work breakdown

---

## Context

This is part of workpack: `2026-02-01_feature_hybrid-g2p-paradigm`

**Objective**: Define the extended lexicon data schema and storage layer to support dialect variants, source tracking, confidence scores, and multiple pronunciations.

---

## Delivery Mode

- **PR-based**: Create a PR targeting `feature/hybrid-g2p-paradigm`

---

## Objective

Create the data foundation for the expanded lexicon system. This prompt focuses on **schema design and I/O** — not the builder logic or pipeline integration.

The new lexicon schema must:
- Support multiple dialects per lemma
- Track data source and confidence
- Store frequency information for prioritization
- Handle alternative pronunciations (n-best)
- Maintain backward compatibility with existing TSV format

---

## Reference Points

- **Current Lexicon**: Study `g2p/lexicon.py` for existing TSV loading and LRU cache patterns
- **Type patterns**: Follow dataclass style from `core/types.py`
- **Config pattern**: Use dataclass-based config like `normalization/` and `tokenization/`

---

## Implementation Requirements

### 1. Create `src/furlan_g2p/lexicon/` package

Structure:
- `__init__.py` — Public exports
- `schema.py` — Data model (LexiconEntry, LexiconConfig)
- `storage.py` — I/O operations (read/write TSV and JSONL)

### 2. LexiconEntry Dataclass

Define with these fields:
- `lemma: str` — Word form (required)
- `ipa: str` — Primary IPA pronunciation (required)
- `dialect: str | None` — Dialect code ("central", "western", "carnic") or None for universal
- `source: str` — Origin identifier ("seed", "wikipron", "manual", "cof")
- `confidence: float` — Confidence score 0.0-1.0 (default 1.0)
- `frequency: int | None` — Corpus frequency rank (None if unknown)
- `alternatives: list[str]` — Alternative pronunciations (empty list default)
- `stress_marked: bool` — Whether IPA includes stress markers (derived field)

### 3. LexiconConfig Dataclass

Configuration for lexicon behavior:
- `default_dialect: str | None` — Default dialect for lookups
- `fallback_to_universal: bool` — If dialect entry not found, try universal (default True)
- `case_sensitive: bool` — Case-sensitive lookup (default False)
- `return_alternatives: bool` — Include alternatives in lookup (default False)

### 4. Storage Layer

**TSV Format (backward compatible)**
Simple format: `lemma\tipa`
Extended format: `lemma\tipa\tdialect\tsource\tconfidence`

**JSONL Format (full schema)**
One JSON object per line with all fields.

**Functions to implement**:
- `read_tsv(path: Path, format: str = "simple") -> list[LexiconEntry]`
- `write_tsv(entries: list[LexiconEntry], path: Path, format: str = "simple") -> None`
- `read_jsonl(path: Path) -> list[LexiconEntry]`
- `write_jsonl(entries: list[LexiconEntry], path: Path) -> None`
- `detect_format(path: Path) -> str` — Auto-detect file format

### 5. Validation

- Validate IPA strings contain only valid characters
- Validate dialect codes against allowed values
- Validate confidence in range [0.0, 1.0]
- Log warnings for validation issues, don't fail hard

---

## Contracts

### LexiconEntry (dataclass)

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `lemma` | `str` | required | Word form |
| `ipa` | `str` | required | Primary pronunciation |
| `dialect` | `str \| None` | `None` | Dialect code |
| `source` | `str` | `"unknown"` | Data origin |
| `confidence` | `float` | `1.0` | Confidence score |
| `frequency` | `int \| None` | `None` | Corpus frequency |
| `alternatives` | `list[str]` | `[]` | Alt pronunciations |

### LexiconConfig (dataclass)

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `default_dialect` | `str \| None` | `None` | Default for lookups |
| `fallback_to_universal` | `bool` | `True` | Fallback behavior |
| `case_sensitive` | `bool` | `False` | Case sensitivity |

---

## Scope

### In Scope

- LexiconEntry and LexiconConfig dataclasses
- TSV read/write (simple and extended formats)
- JSONL read/write
- Format detection
- Basic validation

### Out of Scope

- LexiconBuilder (A3)
- WikiPron ingestion (A3)
- Lexicon lookup class (A4)
- CLI commands (A6)

---

## Acceptance Criteria

- [ ] `LexiconEntry` dataclass has all required fields
- [ ] `LexiconConfig` dataclass is defined
- [ ] TSV read/write works for both simple and extended formats
- [ ] JSONL read/write round-trips correctly
- [ ] Validation logs warnings for invalid data
- [ ] Backward compatible with existing seed lexicon format
- [ ] mypy passes

---

## Constraints

- **CRITICAL**: Maintain backward compatibility with existing TSV format
- No new dependencies for I/O (use stdlib `csv`, `json`)
- All dataclasses must be immutable (frozen=True or use field factories carefully)

---

## Verification

```bash
pip install -e ".[dev]"
python -c "from furlan_g2p.lexicon import LexiconEntry, LexiconConfig; print('OK')"
python -c "from furlan_g2p.lexicon.storage import read_tsv, write_jsonl; print('OK')"
mypy src/furlan_g2p/lexicon/
ruff check src/furlan_g2p/lexicon/
```

---

## Handoff Output (JSON) — REQUIRED

**Path**: `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A2_lexicon_schema.json`

---

## Stop Conditions

- **STOP** if existing lexicon format cannot be preserved (escalate)
- **CONTINUE** for minor schema questions (document choices)

---

## Deliverables

- [ ] `src/furlan_g2p/lexicon/__init__.py`
- [ ] `src/furlan_g2p/lexicon/schema.py`
- [ ] `src/furlan_g2p/lexicon/storage.py`
- [ ] Handoff output JSON
- [ ] PR created
