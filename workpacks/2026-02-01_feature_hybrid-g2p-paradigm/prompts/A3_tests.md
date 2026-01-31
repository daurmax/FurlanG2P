# Tests Agent Prompt

> Implement comprehensive test suite for new hybrid G2P modules.

---

## READ FIRST

Read these files before starting (in priority order):

1. `README.md` — Project overview
2. `AGENTS.md` — Agent guidelines
3. `tests/` — Existing test structure and patterns
4. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/00_request.md` — Full requirements
5. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/01_plan.md` — Work breakdown
6. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A1_library.json` — Library handoff
7. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A2_cli.json` — CLI handoff
8. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v3)

---

## Context

This is part of workpack: `2026-02-01_feature_hybrid-g2p-paradigm`

**Objective**: Create comprehensive tests for the evaluation module, lexicon module, ML interfaces, and new CLI commands. Target ≥80% coverage for new modules.

---

## Delivery Mode

- **PR-based**: Create a PR targeting `feature/hybrid-g2p-paradigm` and link it in `99_status.md`

---

## Objective

Implement a robust test suite covering all new functionality introduced by the hybrid G2P paradigm workpack. The tests ensure:

1. **Evaluation metrics** work correctly for edge cases and normal operations
2. **Lexicon schema** validates data properly and handles multi-pronunciation entries
3. **LexiconBuilder** correctly ingests WikiPron format and normalizes IPA
4. **IExceptionModel** interface can be implemented and null implementation works
5. **CLI commands** accept correct arguments and produce expected output

Tests should follow the project's existing patterns and achieve ≥80% coverage for new modules.

---

## Reference Points

- **Test pattern**: Follow existing test structure in `tests/` directory
- **Fixture pattern**: Use pytest fixtures for shared test data
- **Parametrize pattern**: Use `@pytest.mark.parametrize` for multiple test cases
- **CLI testing**: Use `click.testing.CliRunner` for CLI command tests
- **Coverage**: Use `pytest-cov` for coverage measurement

---

## Implementation Requirements

### 1. Evaluation Module Tests (`tests/test_evaluation.py`)

Test the evaluation metrics:

- **WER tests**: Perfect match, complete mismatch, partial match, empty input
- **PER tests**: Phoneme-level accuracy with IPA normalization
- **Stress accuracy tests**: Correct stress, wrong position, missing stress
- **Batch evaluation tests**: Multiple words, mixed results
- Edge cases: empty strings, single phonemes, no stress markers

### 2. Lexicon Module Tests (`tests/test_lexicon.py`)

Test schema and storage:

- **LexiconEntry tests**: Required fields, optional fields, validation
- **Multi-pronunciation tests**: Entries with alternatives
- **Dialect handling tests**: Dialect lookup priority, fallback behavior
- **Storage tests**: TSV read/write round-trip, JSONL read/write round-trip

### 3. LexiconBuilder Tests (`tests/test_lexicon_builder.py`)

Test the builder:

- **WikiPron ingestion**: Valid format, malformed lines, encoding issues
- **IPA normalization**: Known symbols, unknown symbols, warnings
- **Incremental building**: Multiple sources, deduplication
- **Validation**: Detect invalid entries, report errors
- **Output formats**: TSV and JSONL export

### 4. ML Interface Tests (`tests/test_ml_interfaces.py`)

Test interface contracts:

- **IExceptionModel**: Abstract method signatures
- **Null implementation**: Always returns None, `is_available()` returns False
- **Import guards**: Module importable without ML dependencies
- **Mock implementation**: Test with a simple mock model

### 5. CLI Tests (`tests/test_cli_lexicon.py`, `tests/test_cli_evaluate.py`)

Test CLI commands:

- **Lexicon build**: Valid input, invalid input, output verification
- **Lexicon info**: Statistics output format
- **Lexicon export**: Format conversion
- **Evaluate**: Gold set processing, metric output
- **Coverage**: Wordlist processing, coverage calculation
- **Error handling**: Missing files, invalid formats, exit codes

### 6. Test Fixtures (`tests/conftest.py`)

Create shared fixtures:

- Sample lexicon entries (multiple dialects)
- Sample WikiPron format file
- Sample gold set file
- Sample wordlist file
- Temporary directory fixture

---

## Scope

### In Scope

- Unit tests for evaluation module
- Unit tests for lexicon module
- Unit tests for LexiconBuilder
- Unit tests for ML interfaces
- Integration tests for CLI commands
- Test fixtures and sample data
- Coverage configuration

### Out of Scope

- Library implementation (done in A1_library)
- CLI implementation (done in A2_cli)
- Documentation (done in A4_docs)
- Performance/load testing

---

## Acceptance Criteria

- [ ] All new tests pass
- [ ] Coverage ≥80% for `furlan_g2p/evaluation/`
- [ ] Coverage ≥80% for `furlan_g2p/lexicon/`
- [ ] Coverage ≥80% for `furlan_g2p/ml/`
- [ ] CLI command tests cover success and error cases
- [ ] Tests follow project conventions
- [ ] No flaky tests (deterministic)

---

## Constraints

- **CRITICAL**: Tests must not require actual ML models
- Use fixtures and mocks for external dependencies
- Tests must run without network access
- Keep test data small (embedded in fixtures or small files)
- Follow existing test naming conventions

---

## Verification

### Commands

```bash
# Install in development mode
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/furlan_g2p --cov-report=term-missing

# Run coverage with failure threshold
pytest tests/ --cov=src/furlan_g2p/evaluation --cov=src/furlan_g2p/lexicon --cov=src/furlan_g2p/ml --cov-fail-under=80

# Run specific test modules
pytest tests/test_evaluation.py -v
pytest tests/test_lexicon.py -v
pytest tests/test_cli_lexicon.py -v
```

### Verification Checklist

- [ ] All tests pass
- [ ] Coverage threshold met
- [ ] No warnings or deprecation notices
- [ ] Tests are deterministic (run multiple times)
- [ ] Test files are properly organized

---

## Handoff Output (JSON) — REQUIRED

After completing the work, create/update:

**Path**: `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A3_tests.json`

```json
{
  "schema_version": "1.0",
  "workpack": "2026-02-01_feature_hybrid-g2p-paradigm",
  "prompt": "A3_tests",
  "component": "tests",
  "delivery_mode": "pr",
  "branch": {
    "base": "feature/hybrid-g2p-paradigm",
    "work": "feature/hybrid-g2p-paradigm-tests",
    "merge_target": "feature/hybrid-g2p-paradigm"
  },
  "summary": "Implemented comprehensive test suite for hybrid G2P modules",
  "handoff": {
    "files_modified": ["tests/conftest.py"],
    "files_created": [
      "tests/test_evaluation.py",
      "tests/test_lexicon.py",
      "tests/test_lexicon_builder.py",
      "tests/test_ml_interfaces.py",
      "tests/test_cli_lexicon.py",
      "tests/test_cli_evaluate.py",
      "tests/fixtures/sample_wikipron.tsv",
      "tests/fixtures/sample_gold.tsv"
    ],
    "verification": {
      "commands_run": ["pytest tests/ -v", "pytest --cov=src/furlan_g2p --cov-fail-under=80"],
      "all_passed": true
    },
    "next_steps": [
      "A5_integration can run full validation suite"
    ],
    "known_issues": []
  },
  "artifacts": {
    "pr_url": "<PR_URL>",
    "coverage_report": "<COVERAGE_PERCENTAGE>%"
  }
}
```

---

## Stop Conditions

- **STOP** if A1_library or A2_cli outputs are not available (wait for completion)
- **STOP** if coverage cannot reach 80% due to untestable code (escalate)
- **CONTINUE** for minor test design questions (document choices)

---

## Deliverables

- [ ] Test files for all new modules
- [ ] Test fixtures and sample data
- [ ] Updated conftest.py if needed
- [ ] All tests passing
- [ ] Coverage ≥80% achieved
- [ ] Handoff output JSON created
- [ ] PR created and linked in `99_status.md`
