# Library Agent Prompt

> Implement core hybrid G2P infrastructure: evaluation module, lexicon schema, builder, and ML interface.

---

## READ FIRST

Read these files before starting (in priority order):

1. `README.md` — Project overview and setup
2. `AGENTS.md` — Agent guidelines and conventions
3. `docs/architecture.md` — Current component interactions
4. `docs/business_logic.md` — Algorithmic design
5. `docs/references.md` — Bibliography for linguistic rules
6. `src/furlan_g2p/core/interfaces.py` — Existing interface patterns
7. `src/furlan_g2p/g2p/lexicon.py` — Current lexicon implementation
8. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/00_request.md` — Full requirements
9. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/01_plan.md` — Work breakdown
10. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v3)

---

## Context

This is part of workpack: `2026-02-01_feature_hybrid-g2p-paradigm`

**Objective**: Implement core library components for the hybrid G2P paradigm including evaluation metrics, extended lexicon with dialect support, lexicon builder with WikiPron ingestion, and ML exception model interface.

---

## Delivery Mode

- **PR-based**: Create a PR targeting `feature/hybrid-g2p-paradigm` and link it in `99_status.md`

---

## Objective

This prompt covers the foundational library work for the hybrid G2P paradigm shift. The implementation introduces:

1. **Evaluation module** — Compute standard G2P metrics (WER, PER, stress accuracy) to enable quantitative comparison of approaches
2. **Extended lexicon schema** — Support dialect variants, source tracking, confidence scores, and frequency data
3. **LexiconBuilder** — Ingest lexicon data from WikiPron format and other sources, normalizing IPA to the project inventory
4. **IExceptionModel interface** — Define the contract for pluggable ML-based exception handlers
5. **Dialect-aware G2P pipeline** — Update the phonemizer to prioritize lexicon lookup with dialect conditioning

The design must maintain backward compatibility with existing code while enabling the new hybrid approach.

---

## Reference Points

- **Interface pattern**: Follow the abstract base class pattern in `core.interfaces` (e.g., `INormalizer`, `IG2PPhonemizer`)
- **Lexicon pattern**: Extend the existing `Lexicon` class in `g2p/lexicon.py` — preserve the TSV loading and LRU cache behavior
- **Type definitions**: Follow the dataclass style in `core/types.py` for new data structures
- **Exception handling**: Use the exception hierarchy in `core/exceptions.py` for new error types
- **Configuration pattern**: Follow the config dataclass approach from `normalization/` and `tokenization/`

---

## Implementation Requirements

### 1. Evaluation Module (`src/furlan_g2p/evaluation/`)

Create a new `evaluation` package with:

- **Metrics implementation**: Functions for computing WER (word error rate), PER (phoneme edit distance normalized), and stress accuracy
- **Result types**: Dataclasses for evaluation results including per-word breakdowns
- **Batch evaluation**: Support evaluating against a gold set (TSV/JSONL format)
- All functions must handle edge cases (empty input, missing stress markers, etc.)
- Phoneme comparison must normalize IPA symbols before comparison

### 2. Lexicon Schema (`src/furlan_g2p/lexicon/`)

Create a new `lexicon` package (refactoring from `g2p/lexicon.py`) with:

- **LexiconEntry dataclass**: Fields for `lemma`, `ipa`, `dialect` (optional), `source`, `confidence`, `frequency`, `alternatives`
- **LexiconConfig dataclass**: Configuration for lexicon behavior (dialect priority, fallback mode)
- **Multi-pronunciation support**: Entries can have multiple IPA alternatives
- Maintain compatibility with existing TSV format while supporting extended JSONL format

### 3. LexiconBuilder (`src/furlan_g2p/lexicon/builder.py`)

Implement a builder class that:

- Ingests WikiPron TSV format (`word\tipa` or `word\tipa\tdialect`)
- Normalizes IPA symbols to the project inventory (using existing canonicalizer if available)
- Validates entries against the phoneme inventory
- Supports incremental building (add from multiple sources)
- Logs warnings for entries with unknown IPA symbols
- Outputs to both TSV and JSONL formats

### 4. IExceptionModel Interface (`src/furlan_g2p/ml/interfaces.py`)

Define an abstract interface for ML-based exception models:

- Accept word/graphemes as input with optional dialect conditioning
- Return IPA string with stress markers
- Include confidence score in output
- Define a "null" implementation that always returns None (for when ML is disabled)
- Interface must be importable without ML dependencies

### 5. Dialect-Aware Pipeline Updates

Update `g2p/phonemizer.py` or create wrapper:

- Lookup prioritizes lexicon with dialect matching
- Fallback order: exact dialect match → default dialect → rules
- Optional exception model integration point
- Preserve existing behavior when dialect is not specified

### 6. Optional ML Extra

Update `pyproject.toml`:

- Add `[ml]` optional extra with placeholder dependencies (e.g., `torch`, `transformers`)
- Ensure base install has no ML dependencies
- Add import guards in ML module

---

## Contracts

### ILexiconBuilder (new interface in `core/interfaces.py`)

| Method | Returns | Notes |
|--------|---------|-------|
| `add_source(path: Path, format: str)` | `int` | Add entries from file, return count |
| `add_entry(entry: LexiconEntry)` | `None` | Add single entry |
| `build()` | `Lexicon` | Finalize and return lexicon |
| `validate()` | `list[ValidationError]` | Check for issues |

### IEvaluator (new interface in `core/interfaces.py`)

| Method | Returns | Notes |
|--------|---------|-------|
| `evaluate(predictions: list, gold: list)` | `EvaluationResult` | Compute all metrics |
| `word_error_rate(pred: list, gold: list)` | `float` | WER only |
| `phoneme_error_rate(pred: list, gold: list)` | `float` | PER only |

### IExceptionModel (new interface in `ml/interfaces.py`)

| Method | Returns | Notes |
|--------|---------|-------|
| `predict(word: str, dialect: str \| None)` | `ExceptionPrediction \| None` | Return IPA with confidence or None |
| `is_available()` | `bool` | Check if model is loaded |

### LexiconEntry (dataclass in `lexicon/schema.py`)

| Field | Type | Notes |
|-------|------|-------|
| `lemma` | `str` | Word form |
| `ipa` | `str` | Primary pronunciation |
| `dialect` | `str \| None` | Dialect code or None for default |
| `source` | `str` | Origin: "wikipron", "manual", "seed" |
| `confidence` | `float` | 0.0-1.0 confidence score |
| `frequency` | `int \| None` | Corpus frequency rank |
| `alternatives` | `list[str]` | Alternative pronunciations |

---

## Scope

### In Scope

- Evaluation module with WER, PER, stress accuracy
- LexiconEntry and LexiconConfig dataclasses
- LexiconBuilder with WikiPron ingestion
- IExceptionModel interface
- Updates to Lexicon for dialect support
- ILexiconBuilder and IEvaluator interfaces
- `[ml]` optional extra in pyproject.toml

### Out of Scope

- CLI commands (handled by A2_cli)
- Test implementation (handled by A3_tests)
- Full WikiPron extraction pipeline
- Actual ML model training/loading
- Documentation updates (handled by A4_docs)

---

## Acceptance Criteria

- [ ] Evaluation module computes WER, PER, and stress accuracy correctly
- [ ] LexiconEntry dataclass has all required fields with proper types
- [ ] LexiconBuilder can ingest WikiPron TSV and normalize IPA
- [ ] IExceptionModel interface is importable without ML dependencies
- [ ] Lexicon lookup supports dialect conditioning
- [ ] `[ml]` extra defined in pyproject.toml
- [ ] All new code has type hints and docstrings
- [ ] mypy passes with no errors
- [ ] ruff check passes with no errors

---

## Constraints

- **CRITICAL**: No ML dependencies in base install — only in `[ml]` extra
- **CRITICAL**: Maintain backward compatibility with existing Lexicon API
- All public interfaces must be in `core/interfaces.py` or documented module `__init__.py`
- Follow existing code patterns (dataclasses, ABC, type hints)
- Consult `docs/references.md` for IPA inventory and phonological rules

---

## Verification

### Commands

```bash
# Install in development mode
pip install -e ".[dev]"

# Run type checking
mypy src/

# Run linting
ruff check src/

# Verify new modules are importable
python -c "from furlan_g2p.evaluation import metrics; print('OK')"
python -c "from furlan_g2p.lexicon import LexiconBuilder, LexiconEntry; print('OK')"
python -c "from furlan_g2p.ml.interfaces import IExceptionModel; print('OK')"

# Verify ML extra
pip install -e ".[ml]"
```

### Verification Checklist

- [ ] All existing tests still pass
- [ ] New modules are importable
- [ ] Type checking passes
- [ ] Linting passes
- [ ] ML import works without base dependencies
- [ ] Backward compatibility verified

---

## Handoff Output (JSON) — REQUIRED

After completing the work, create/update:

**Path**: `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A1_library.json`

```json
{
  "schema_version": "1.0",
  "workpack": "2026-02-01_feature_hybrid-g2p-paradigm",
  "prompt": "A1_library",
  "component": "library",
  "delivery_mode": "pr",
  "branch": {
    "base": "feature/hybrid-g2p-paradigm",
    "work": "feature/hybrid-g2p-paradigm-library",
    "merge_target": "feature/hybrid-g2p-paradigm"
  },
  "summary": "Implemented evaluation module, extended lexicon schema, LexiconBuilder, and IExceptionModel interface",
  "handoff": {
    "files_modified": ["pyproject.toml", "src/furlan_g2p/core/interfaces.py"],
    "files_created": [
      "src/furlan_g2p/evaluation/__init__.py",
      "src/furlan_g2p/evaluation/metrics.py",
      "src/furlan_g2p/evaluation/types.py",
      "src/furlan_g2p/lexicon/__init__.py",
      "src/furlan_g2p/lexicon/schema.py",
      "src/furlan_g2p/lexicon/builder.py",
      "src/furlan_g2p/lexicon/storage.py",
      "src/furlan_g2p/lexicon/wikipron.py",
      "src/furlan_g2p/ml/__init__.py",
      "src/furlan_g2p/ml/interfaces.py"
    ],
    "verification": {
      "commands_run": ["mypy src/", "ruff check src/", "pytest tests/ -v"],
      "all_passed": true
    },
    "next_steps": [
      "A2_cli can implement CLI commands",
      "A3_tests can implement test suite"
    ],
    "known_issues": []
  },
  "artifacts": {
    "pr_url": "<PR_URL>"
  }
}
```

---

## Stop Conditions

- **STOP** if existing Lexicon API cannot be preserved (escalate for design discussion)
- **STOP** if ML dependencies leak into base install
- **CONTINUE** for minor IPA canonicalization questions (document assumptions)
- **CONTINUE** for WikiPron format variations (support common formats)

---

## Deliverables

- [ ] `src/furlan_g2p/evaluation/` module with metrics
- [ ] `src/furlan_g2p/lexicon/` module with schema, builder, storage
- [ ] `src/furlan_g2p/ml/` module with interfaces
- [ ] Updated `pyproject.toml` with `[ml]` extra
- [ ] Updated `core/interfaces.py` with new interfaces
- [ ] Handoff output JSON created
- [ ] PR created and linked in `99_status.md`
