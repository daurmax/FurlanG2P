# Tests Agent Prompt

> Prompt for the tests agent to implement test coverage.

---

## READ FIRST

Read these files before starting (in priority order):

1. `README.md` — Project overview
2. `AGENTS.md` — Agent guidelines
3. `tests/` — Existing test structure
4. `./workpacks/<workpack>/00_request.md` — Original request
5. `./workpacks/<workpack>/01_plan.md` — Full plan
6. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v3)

---

## Context

This is part of workpack: `YYYY-MM-DD_<category>_<short-slug>`

**Objective**: <!-- One-line summary of test work needed -->

---

## Delivery Mode

<!-- Choose one based on 00_request.md -->

- **PR-based**: Create a PR targeting `main` and link it in `99_status.md`
- **Direct push**: Push directly to feature branch; record commits in `99_status.md`

---

## Objective

<!-- 
Describe WHAT tests need to be added or improved.
Focus on coverage goals and test types.
-->

---

## Reference Points

<!--
Reference existing test patterns.

Example:
- **Unit test pattern**: Follow the structure in `tests/test_normalizer.py`
- **Fixture pattern**: Use pytest fixtures as in existing tests
- **Parametrize pattern**: See how parametrized tests are done in `test_g2p.py`
-->

- **Pattern reference 1**: <!-- Description -->

---

## Implementation Requirements

<!--
Describe WHAT tests are needed.

Example:
- Add unit tests for the new PhonemeConverter class
- Cover edge cases: empty input, special characters, diacritics
- Add parametrized tests for common word patterns
- Include integration test for CLI command
-->

- Requirement 1
- Requirement 2
- Requirement 3

---

## Test Categories

<!--
Specify what types of tests are needed.
-->

| Category | Description | Priority |
|----------|-------------|----------|
| Unit | Individual function/class tests | High |
| Integration | Component interaction tests | Medium |
| CLI | Command-line interface tests | Medium |
| Edge cases | Boundary conditions | High |

---

## Scope

### In Scope

- <!-- Item 1 -->
- <!-- Item 2 -->

### Out of Scope

- <!-- Item 1 -->
- <!-- Item 2 -->

---

## Acceptance Criteria

- [ ] All new code has test coverage
- [ ] Edge cases are tested
- [ ] All tests pass
- [ ] No regressions

---

## Constraints

- Use pytest for all tests
- Follow existing test file naming: `test_<module>.py`
- Keep tests focused and fast

---

## Verification

### Commands

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src/furlan_g2p --cov-report=term-missing

# Run specific test file
pytest tests/test_<module>.py -v

# Type check test files
mypy tests/
```

### Verification Checklist

- [ ] All tests pass
- [ ] Coverage is adequate for new code
- [ ] Test names are descriptive
- [ ] Tests are deterministic (no flaky tests)

---

## Handoff Output (JSON) — REQUIRED

After completing the work, create/update:

**Path**: `./workpacks/<workpack>/outputs/A3_tests.json`

```json
{
  "schema_version": "1.0",
  "workpack": "<workpack>",
  "prompt": "A3_tests",
  "component": "tests",
  "delivery_mode": "<pr|direct_push>",
  "branch": {
    "base": "<base-branch>",
    "work": "<work-branch>",
    "merge_target": "<merge-target>"
  },
  "artifacts": {
    "commit_shas": ["<sha1>"]
  },
  "changes": {
    "files_modified": [],
    "files_created": ["tests/test_<module>.py"],
    "contracts_changed": [],
    "breaking_change": false
  },
  "verification": {
    "commands": [
      { "cmd": "pytest tests/ -v", "result": "pass" },
      { "cmd": "mypy tests/", "result": "pass" }
    ],
    "regression_added": true
  },
  "handoff": {
    "summary": "<one-line summary>",
    "known_issues": [],
    "next_steps": []
  }
}
```

---

## Stop Conditions

### Continue if:
- Coverage could be higher but core paths are tested

### Escalate if:
- Implementation (A1/A2) has bugs that prevent testing
- Test framework issues

---

## Deliverables

- [ ] Tests implemented in `tests/`
- [ ] All tests pass
- [ ] `outputs/A3_tests.json` created
- [ ] `99_status.md` updated
