# Evaluation Module Agent Prompt

> Implement evaluation infrastructure: WER, PER, and stress accuracy metrics.

---

## READ FIRST

1. `README.md` — Project overview
2. `AGENTS.md` — Agent guidelines and coding standards
3. `docs/architecture.md` — Current component interactions
4. `src/furlan_g2p/core/interfaces.py` — Existing interface patterns
5. `src/furlan_g2p/core/types.py` — Type definition patterns
6. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/00_request.md` — Full requirements
7. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/01_plan.md` — Work breakdown
8. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Protocol v3 conventions

---

## Context

This is part of workpack: `2026-02-01_feature_hybrid-g2p-paradigm`

**Objective**: Create the evaluation module with standard G2P metrics (WER, PER, stress accuracy) to enable quantitative comparison of different approaches.

---

## Delivery Mode

- **PR-based**: Create a PR targeting `feature/hybrid-g2p-paradigm`

---

## Objective

Implement a standalone evaluation package that computes standard G2P quality metrics. This is **Phase 0** of the roadmap — establishing the measurement infrastructure before building the lexicon and ML components.

The evaluation module enables:
- Comparing rule-based vs hybrid approaches quantitatively
- Measuring progress as the lexicon grows
- Validating dialect-specific accuracy
- Regression testing for future changes

---

## Reference Points

- **Interface pattern**: Follow the ABC pattern in `core.interfaces` (e.g., `INormalizer`)
- **Type definitions**: Use dataclass style from `core/types.py`
- **Exception pattern**: Follow `core/exceptions.py` hierarchy
- **Levenshtein distance**: Use standard edit distance algorithm (can use `rapidfuzz` or implement)

---

## Implementation Requirements

### 1. Create `src/furlan_g2p/evaluation/` package

Structure:
- `__init__.py` — Public exports
- `metrics.py` — Core metric functions
- `types.py` — Result dataclasses

### 2. Metric Functions

**Word Error Rate (WER)**
- Definition: Percentage of words where predicted IPA ≠ gold IPA
- Must normalize IPA before comparison (strip whitespace, normalize Unicode)
- Handle empty inputs gracefully

**Phoneme Error Rate (PER)**
- Definition: Levenshtein distance over phoneme sequences, normalized by gold length
- Split IPA strings into phoneme tokens (handle diacritics, affricates)
- Return value in range [0.0, 1.0+] (can exceed 1.0 for insertions)

**Stress Accuracy**
- Definition: Percentage of words where stress marker position matches
- Extract stress marker (`ˈ`) position from syllabified output
- Handle words without stress markers

### 3. Result Types

Create dataclasses for:
- `EvaluationResult` — Aggregate metrics (wer, per, stress_accuracy, word_count)
- `WordResult` — Per-word breakdown (word, predicted, gold, is_correct, phoneme_distance)

### 4. Batch Evaluation

- Function to evaluate against a gold set file (TSV format: `word\tipa` or `word\tipa\tdialect`)
- Support filtering by dialect
- Return both aggregate and per-word results

### 5. IPA Normalization for Comparison

- Canonicalize IPA symbols before comparison
- Strip non-phonemic content (spaces, punctuation)
- Handle common variations (e.g., `g` vs `ɡ`, tie bars)

---

## Contracts

### IEvaluator (new interface in `core/interfaces.py`)

| Method | Returns | Notes |
|--------|---------|-------|
| `evaluate(predictions: list[tuple[str, str]], gold: list[tuple[str, str]])` | `EvaluationResult` | Compute all metrics |
| `word_error_rate(predictions: list[str], gold: list[str])` | `float` | WER only |
| `phoneme_error_rate(predictions: list[str], gold: list[str])` | `float` | PER only |
| `stress_accuracy(predictions: list[str], gold: list[str])` | `float` | Stress only |

### EvaluationResult (dataclass)

| Field | Type | Notes |
|-------|------|-------|
| `wer` | `float` | Word error rate [0.0, 1.0] |
| `per` | `float` | Phoneme error rate [0.0, ∞) |
| `stress_accuracy` | `float` | Stress accuracy [0.0, 1.0] |
| `word_count` | `int` | Total words evaluated |
| `correct_count` | `int` | Words with exact match |
| `details` | `list[WordResult]` | Per-word breakdown (optional) |

---

## Scope

### In Scope

- Evaluation package with metrics
- IEvaluator interface
- Result dataclasses
- IPA normalization for comparison
- Batch evaluation from TSV

### Out of Scope

- CLI commands (A7)
- Lexicon components (A2, A3)
- ML components (A5)
- Integration with pipeline

---

## Acceptance Criteria

- [ ] `furlan_g2p.evaluation` package is importable
- [ ] WER computes correctly for edge cases (empty, identical, completely wrong)
- [ ] PER uses proper phoneme tokenization
- [ ] Stress accuracy handles missing stress markers
- [ ] Batch evaluation reads TSV format
- [ ] All functions have type hints and docstrings
- [ ] mypy passes

---

## Constraints

- **CRITICAL**: Use minimal dependencies (prefer `rapidfuzz` if available, else stdlib)
- Follow existing code patterns strictly
- All public APIs must be in `__init__.py`

---

## Verification

```bash
pip install -e ".[dev]"
python -c "from furlan_g2p.evaluation import Evaluator, EvaluationResult; print('OK')"
mypy src/furlan_g2p/evaluation/
ruff check src/furlan_g2p/evaluation/
```

---

## Handoff Output (JSON) — REQUIRED

**Path**: `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A1_evaluation.json`

---

## Stop Conditions

- **STOP** if phoneme tokenization requires complex IPA parsing not yet available
- **CONTINUE** for edge case questions (document assumptions)

---

## Deliverables

- [ ] `src/furlan_g2p/evaluation/__init__.py`
- [ ] `src/furlan_g2p/evaluation/metrics.py`
- [ ] `src/furlan_g2p/evaluation/types.py`
- [ ] Updated `src/furlan_g2p/core/interfaces.py` with `IEvaluator`
- [ ] Handoff output JSON
- [ ] PR created
