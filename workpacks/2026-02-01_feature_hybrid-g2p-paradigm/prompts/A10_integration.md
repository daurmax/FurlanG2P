# Integration Agent Prompt — Merge Reviewer

> Validate all agent outputs, run full verification suite, and authorize merge.

---

## READ FIRST

1. `README.md` — Project overview
2. `AGENTS.md` — Agent guidelines
3. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/00_request.md` — All acceptance criteria
4. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/01_plan.md` — Work breakdown
5. All handoff outputs (A0-A9)
6. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Protocol v3

---

## Context

This is part of workpack: `2026-02-01_feature_hybrid-g2p-paradigm`

**Objective**: Act as Merge Reviewer — validate all outputs, run verification suite, cross-check acceptance criteria, authorize or block merge.

---

## Delivery Mode

- **PR-based**: Merge feature branch to `main` after validation

---

## Role: Merge Reviewer

You have authority to:
1. **Validate** all agent output JSONs
2. **Run** full verification suite
3. **Cross-check** all acceptance criteria
4. **Authorize** merge if all pass
5. **Block** merge if critical issues found

---

## Validation Checklist

### 1. Handoff Output Validation

Verify each output JSON exists and is valid:

| Prompt | JSON Path | Required Fields |
|--------|-----------|-----------------|
| A0_bootstrap | `outputs/A0_bootstrap.json` | branch.work |
| A1_evaluation | `outputs/A1_evaluation.json` | files_created, verification.all_passed |
| A2_lexicon_schema | `outputs/A2_lexicon_schema.json` | files_created |
| A3_lexicon_builder | `outputs/A3_lexicon_builder.json` | files_created |
| A4_dialect_pipeline | `outputs/A4_dialect_pipeline.json` | files_modified |
| A5_ml_interface | `outputs/A5_ml_interface.json` | files_created |
| A6_cli_lexicon | `outputs/A6_cli_lexicon.json` | files_created |
| A7_cli_evaluate | `outputs/A7_cli_evaluate.json` | files_created |
| A8_tests | `outputs/A8_tests.json` | artifacts.coverage_report |
| A9_docs | `outputs/A9_docs.json` | files_modified |

### 2. Verification Suite

```bash
# Install all dependencies
pip install -e ".[dev,ml]"

# Run full test suite
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/furlan_g2p --cov-report=term-missing

# Coverage threshold for new modules
pytest tests/ --cov=src/furlan_g2p/evaluation --cov=src/furlan_g2p/lexicon --cov=src/furlan_g2p/ml --cov-fail-under=80

# Type checking
mypy src/

# Linting
ruff check src/ tests/

# Format check
ruff format --check src/ tests/
```

### 3. Acceptance Criteria Cross-Check

| AC ID | Criterion | Verification | Status |
|-------|-----------|--------------|--------|
| AC1 | LexiconBuilder ingests WikiPron | `pytest tests/test_lexicon_builder.py -v` | ⬜ |
| AC2 | Lexicon schema with dialect/confidence | `pytest tests/test_lexicon_schema.py -v` | ⬜ |
| AC3 | Evaluation metrics (WER, PER, stress) | `pytest tests/test_evaluation.py -v` | ⬜ |
| AC4 | Dialect-aware lexicon lookup | `pytest tests/test_lexicon_lookup.py -v` | ⬜ |
| AC5 | IExceptionModel interface | `python -c "from furlan_g2p.ml import IExceptionModel"` | ⬜ |
| AC6 | CLI commands | `furlan-g2p lexicon --help && furlan-g2p evaluate --help` | ⬜ |
| AC7 | Documentation updated | Manual review of `docs/` | ⬜ |
| AC8 | Type hints and mypy pass | `mypy src/` | ⬜ |
| AC9 | Test coverage ≥80% | `pytest --cov-fail-under=80` | ⬜ |
| AC10 | ML optional extra | `pip install -e ".[ml]"` | ⬜ |

### 4. Smoke Tests

```bash
# Verify imports
python -c "
from furlan_g2p.evaluation import Evaluator
from furlan_g2p.lexicon import LexiconBuilder, LexiconEntry, DialectAwareLexicon
from furlan_g2p.ml import IExceptionModel, NullExceptionModel, ML_AVAILABLE
print('All imports OK')
"

# Verify CLI commands
furlan-g2p --help
furlan-g2p lexicon --help
furlan-g2p evaluate --help
furlan-g2p coverage --help

# Basic lexicon build test
echo -e "test\ttɛst" > /tmp/test.tsv
furlan-g2p lexicon build /tmp/test.tsv -o /tmp/lex.jsonl
furlan-g2p lexicon info /tmp/lex.jsonl
```

---

## Merge Process

1. Ensure all agent PRs merged to `feature/hybrid-g2p-paradigm`
2. Pull latest feature branch
3. Run full verification suite
4. Fix any issues found
5. Create PR: `feature/hybrid-g2p-paradigm` → `main`
6. Include summary of all changes
7. Merge after approval

---

## Scope

### In Scope

- Handoff output validation
- Verification suite execution
- Acceptance criteria cross-check
- Smoke tests
- PR creation and merge
- Known issues documentation

### Out of Scope

- New feature implementation
- Major refactoring

---

## Acceptance Criteria

- [ ] All 10 handoff outputs exist and are valid
- [ ] All tests pass
- [ ] Type checking passes
- [ ] Linting passes
- [ ] Coverage ≥80% for new modules
- [ ] All 10 acceptance criteria verified
- [ ] PR merged to `main`

---

## Constraints

- **DO NOT MERGE** if any AC fails
- **DO NOT MERGE** if tests fail
- Document all known issues

---

## Handoff Output (JSON) — REQUIRED

**Path**: `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A10_integration.json`

Include:
- All AC verification results
- Coverage report
- PR URL
- Merge commit SHA

---

## Stop Conditions

- **STOP AND BLOCK** if any AC fails
- **STOP AND BLOCK** if tests fail
- **STOP AND ESCALATE** if outputs missing

---

## Deliverables

- [ ] All handoff outputs validated
- [ ] Full verification suite passed
- [ ] All ACs verified
- [ ] PR created and merged
- [ ] `99_status.md` updated
- [ ] Handoff output JSON created
