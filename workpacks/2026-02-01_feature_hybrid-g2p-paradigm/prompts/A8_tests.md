# Tests Agent Prompt

> Implement comprehensive test suite for all new hybrid G2P modules.

---

## READ FIRST

1. `README.md` — Project overview
2. `AGENTS.md` — Agent guidelines
3. `tests/` — Existing test structure
4. All previous handoff outputs:
   - `outputs/A1_evaluation.json`
   - `outputs/A2_lexicon_schema.json`
   - `outputs/A3_lexicon_builder.json`
   - `outputs/A4_dialect_pipeline.json`
   - `outputs/A5_ml_interface.json`
   - `outputs/A6_cli_lexicon.json`
   - `outputs/A7_cli_evaluate.json`
5. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/00_request.md` — Acceptance criteria

---

## Context

This is part of workpack: `2026-02-01_feature_hybrid-g2p-paradigm`

**Objective**: Create comprehensive tests for all new modules achieving ≥80% coverage for new code.

---

## Delivery Mode

- **PR-based**: Create a PR targeting `feature/hybrid-g2p-paradigm`

---

## Objective

Implement a robust test suite covering all new functionality. Tests ensure:
- Evaluation metrics compute correctly
- Lexicon schema and storage work as designed
- LexiconBuilder processes sources correctly
- Dialect-aware pipeline functions properly
- ML interface contracts are correct
- CLI commands accept arguments and produce expected output

Target: ≥80% coverage for new modules.

---

## Reference Points

- **Test pattern**: Follow existing patterns in `tests/`
- **Fixtures**: Use pytest fixtures for shared data
- **Parametrize**: Use `@pytest.mark.parametrize` for multiple cases
- **CLI testing**: Use `click.testing.CliRunner`

---

## Implementation Requirements

### 1. Test Organization

Create test files matching module structure:
- `tests/test_evaluation.py`
- `tests/test_lexicon_schema.py`
- `tests/test_lexicon_builder.py`
- `tests/test_lexicon_lookup.py`
- `tests/test_ml_interface.py`
- `tests/test_cli_lexicon.py`
- `tests/test_cli_evaluate.py`

### 2. Evaluation Tests (`test_evaluation.py`)

**WER Tests**:
- Perfect match → 0.0
- Complete mismatch → 1.0
- Partial match → expected fraction
- Empty input handling
- Unicode normalization

**PER Tests**:
- Identical phonemes → 0.0
- Single substitution
- Insertions and deletions
- Phoneme tokenization edge cases

**Stress Accuracy Tests**:
- Correct stress position
- Wrong position
- Missing stress markers
- Multiple stress markers

### 3. Lexicon Schema Tests (`test_lexicon_schema.py`)

- LexiconEntry creation with all fields
- LexiconEntry defaults
- LexiconConfig defaults
- Validation of confidence range
- Serialization round-trip

### 4. Lexicon Storage Tests (`test_lexicon_storage.py`)

- TSV simple format read/write
- TSV extended format read/write
- JSONL read/write
- Format detection
- Malformed input handling
- UTF-8 with BOM

### 5. LexiconBuilder Tests (`test_lexicon_builder.py`)

- WikiPron parsing (valid data)
- WikiPron parsing (malformed lines)
- IPA canonicalization
- Unknown symbol detection
- Duplicate merging
- Multi-source building
- Validation output

### 6. Dialect Lookup Tests (`test_lexicon_lookup.py`)

- Dialect-specific lookup
- Fallback to universal
- Case insensitivity
- LRU cache behavior
- Stats generation

### 7. ML Interface Tests (`test_ml_interface.py`)

- NullExceptionModel returns None
- is_available() returns False
- Interface import without ML deps
- ML_AVAILABLE flag

### 8. CLI Tests (`test_cli_lexicon.py`, `test_cli_evaluate.py`)

- Command help texts
- Build command with valid input
- Build command with invalid input
- Info command output
- Export command format conversion
- Evaluate command output
- Coverage command output
- Exit codes

### 9. Fixtures (`conftest.py`)

Create shared fixtures:
- Sample LexiconEntry list
- Sample WikiPron file (temp)
- Sample gold set file (temp)
- Sample wordlist file (temp)
- CliRunner instance

---

## Scope

### In Scope

- Unit tests for all new modules
- Integration tests for CLI
- Fixtures and sample data
- Coverage verification

### Out of Scope

- Performance tests
- Actual ML model tests (just interface)
- End-to-end pipeline tests (existing tests cover this)

---

## Acceptance Criteria

- [ ] All new tests pass
- [ ] Coverage ≥80% for `furlan_g2p/evaluation/`
- [ ] Coverage ≥80% for `furlan_g2p/lexicon/`
- [ ] Coverage ≥80% for `furlan_g2p/ml/`
- [ ] CLI tests cover success and error cases
- [ ] No flaky tests
- [ ] Existing tests still pass

---

## Constraints

- No network access in tests
- No actual ML models required
- Keep test data small (inline or small files)
- Tests must be deterministic

---

## Verification

```bash
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/furlan_g2p --cov-report=term-missing

# Coverage for new modules
pytest tests/ --cov=src/furlan_g2p/evaluation --cov=src/furlan_g2p/lexicon --cov=src/furlan_g2p/ml --cov-fail-under=80

# Verify no regressions
pytest tests/ -x  # Stop on first failure
```

---

## Handoff Output (JSON) — REQUIRED

**Path**: `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A8_tests.json`

Include coverage percentage in `artifacts.coverage_report`.

---

## Stop Conditions

- **STOP** if previous modules (A1-A7) not complete (wait)
- **STOP** if coverage cannot reach 80% (escalate)
- **CONTINUE** for minor test design questions

---

## Deliverables

- [ ] All test files created
- [ ] Fixtures in conftest.py
- [ ] Sample test data
- [ ] All tests passing
- [ ] Coverage ≥80%
- [ ] Handoff output JSON
- [ ] PR created
