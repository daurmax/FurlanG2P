# Integration Agent Prompt — Merge Reviewer

> Validate all agent outputs, run full test suite, cross-check acceptance criteria, and authorize merge.

---

## READ FIRST

Read these files before starting (in priority order):

1. `README.md` — Project overview
2. `AGENTS.md` — Agent guidelines
3. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/00_request.md` — Full requirements and acceptance criteria
4. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/01_plan.md` — Work breakdown
5. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A1_library.json` — Library handoff
6. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A2_cli.json` — CLI handoff
7. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A3_tests.json` — Tests handoff
8. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A4_docs.json` — Docs handoff
9. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v3)

---

## Context

This is part of workpack: `2026-02-01_feature_hybrid-g2p-paradigm`

**Objective**: Act as Merge Reviewer — validate all agent outputs, run full verification suite, cross-check acceptance criteria, and authorize or block the merge to `main`.

---

## Delivery Mode

- **PR-based**: Merge the feature branch PR to `main` after validation

---

## Role: Merge Reviewer

As the Integration agent, you are the **Merge Reviewer** with authority to:

1. **Validate** all agent output JSONs
2. **Run** full test and quality suite
3. **Cross-check** all acceptance criteria from `00_request.md`
4. **Authorize** merge if all criteria pass
5. **Block** merge if critical issues are found

You are the final gate before code reaches `main`.

---

## Objective

Perform comprehensive validation of the hybrid G2P paradigm implementation:

1. Ensure all sub-PRs are merged to the feature branch
2. Validate all handoff output JSONs exist and are valid
3. Run the complete verification suite (tests, types, linting)
4. Manually verify key acceptance criteria
5. Create the final PR from `feature/hybrid-g2p-paradigm` to `main`
6. Document any known issues or follow-up work needed

---

## Validation Checklist

### 1. Handoff Output Validation

Verify each output JSON exists and is valid:

- [ ] `outputs/A0_bootstrap.json` — Branch created
- [ ] `outputs/A1_library.json` — Library implementation complete
- [ ] `outputs/A2_cli.json` — CLI commands complete
- [ ] `outputs/A3_tests.json` — Tests complete with coverage
- [ ] `outputs/A4_docs.json` — Documentation updated

For each output, verify:
- `schema_version` is "1.0"
- `verification.all_passed` is true
- No blocking `known_issues`

### 2. Verification Suite

Run the complete verification suite:

```bash
# Install all dependencies
pip install -e ".[dev,ml]"

# Run full test suite
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/furlan_g2p --cov-report=term-missing

# Type checking
mypy src/

# Linting
ruff check src/ tests/

# Format check
ruff format --check src/ tests/
```

All commands must pass with no errors.

### 3. Acceptance Criteria Cross-Check

Verify each AC from `00_request.md`:

| AC ID | Criterion | Verification Method | Status |
|-------|-----------|---------------------|--------|
| AC1 | LexiconBuilder ingests WikiPron | `pytest tests/test_lexicon_builder.py -v` | ⬜ |
| AC2 | Lexicon schema with dialect/confidence | `pytest tests/test_lexicon.py::test_schema -v` | ⬜ |
| AC3 | Evaluation metrics (WER, PER, stress) | `pytest tests/test_evaluation.py -v` | ⬜ |
| AC4 | Dialect-aware lexicon lookup | `pytest tests/test_g2p.py -v` | ⬜ |
| AC5 | IExceptionModel interface | `python -c "from furlan_g2p.ml import IExceptionModel"` | ⬜ |
| AC6 | CLI commands | `furlan-g2p lexicon --help && furlan-g2p evaluate --help` | ⬜ |
| AC7 | Documentation updated | Manual review of `docs/` | ⬜ |
| AC8 | Type hints and mypy pass | `mypy src/` | ⬜ |
| AC9 | Test coverage ≥80% | `pytest --cov-fail-under=80` | ⬜ |
| AC10 | ML optional extra | `pip install -e ".[ml]"` | ⬜ |

### 4. Integration Smoke Tests

Perform manual smoke tests:

```bash
# Test lexicon building (with sample data)
echo -e "test\ttɛst" > /tmp/sample.tsv
furlan-g2p lexicon build /tmp/sample.tsv --output /tmp/lexicon.jsonl

# Test evaluation (basic)
furlan-g2p evaluate --help

# Test coverage analysis
furlan-g2p coverage --help

# Verify imports work
python -c "
from furlan_g2p.evaluation import metrics
from furlan_g2p.lexicon import LexiconBuilder, LexiconEntry
from furlan_g2p.ml.interfaces import IExceptionModel
print('All imports successful')
"
```

---

## Implementation Requirements

### Merge Process

1. Ensure all agent PRs are merged to `feature/hybrid-g2p-paradigm`
2. Pull latest feature branch
3. Run full verification suite
4. Address any failing tests or issues
5. Create PR: `feature/hybrid-g2p-paradigm` → `main`
6. Fill in PR description with summary of changes
7. Request review if required by project policy
8. Merge after approval

### Issue Resolution

If issues are found:

- **Minor issues** (typos, style): Fix directly on feature branch
- **Test failures**: Create B-series bugfix prompt or fix directly
- **Blocking issues**: Document in handoff, do NOT merge, escalate

---

## Scope

### In Scope

- Handoff output validation
- Full verification suite execution
- Acceptance criteria cross-check
- Integration smoke tests
- PR creation and merge
- Known issues documentation

### Out of Scope

- New feature implementation
- Major refactoring
- Performance optimization

---

## Acceptance Criteria

- [ ] All handoff outputs exist and are valid
- [ ] All tests pass
- [ ] Type checking passes
- [ ] Linting passes
- [ ] All 10 acceptance criteria verified
- [ ] PR created with proper description
- [ ] Merge completed to `main`

---

## Constraints

- **CRITICAL**: Do NOT merge if any acceptance criteria fail
- **CRITICAL**: Do NOT merge if tests fail
- Document all known issues in handoff output
- Record all verification command outputs

---

## Verification

### Commands

See "Verification Suite" section above.

### Verification Checklist

- [ ] All agent outputs validated
- [ ] pytest passes
- [ ] mypy passes
- [ ] ruff check passes
- [ ] All ACs verified
- [ ] Smoke tests pass
- [ ] PR merged successfully

---

## Handoff Output (JSON) — REQUIRED

After completing the work, create/update:

**Path**: `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A5_integration.json`

```json
{
  "schema_version": "1.0",
  "workpack": "2026-02-01_feature_hybrid-g2p-paradigm",
  "prompt": "A5_integration",
  "component": "integration",
  "delivery_mode": "pr",
  "branch": {
    "base": "main",
    "work": "feature/hybrid-g2p-paradigm",
    "merge_target": "main"
  },
  "summary": "Validated all agents, ran verification suite, merged to main",
  "handoff": {
    "files_modified": [],
    "files_created": [],
    "verification": {
      "commands_run": [
        "pytest tests/ -v",
        "mypy src/",
        "ruff check src/ tests/",
        "pytest --cov=src/furlan_g2p --cov-fail-under=80"
      ],
      "all_passed": true,
      "acceptance_criteria": {
        "AC1": "✅ Passed",
        "AC2": "✅ Passed",
        "AC3": "✅ Passed",
        "AC4": "✅ Passed",
        "AC5": "✅ Passed",
        "AC6": "✅ Passed",
        "AC7": "✅ Passed",
        "AC8": "✅ Passed",
        "AC9": "✅ Passed",
        "AC10": "✅ Passed"
      }
    },
    "next_steps": [
      "Phase 1 complete - consider Phase 2 (actual WikiPron extraction)",
      "Consider neural model implementation for Phase 3"
    ],
    "known_issues": []
  },
  "artifacts": {
    "pr_url": "<PR_URL>",
    "merge_commit": "<MERGE_COMMIT_SHA>"
  }
}
```

---

## Stop Conditions

- **STOP AND BLOCK MERGE** if any acceptance criteria fail
- **STOP AND BLOCK MERGE** if tests fail
- **STOP AND ESCALATE** if handoff outputs are missing
- **CONTINUE** for minor issues that can be fixed in-place

---

## Deliverables

- [ ] All handoff outputs validated
- [ ] Full verification suite passed
- [ ] All acceptance criteria verified
- [ ] PR created: `feature/hybrid-g2p-paradigm` → `main`
- [ ] PR merged successfully
- [ ] Handoff output JSON created
- [ ] `99_status.md` updated with final status
