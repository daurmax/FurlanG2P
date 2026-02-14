# Tests Agent Prompt

> Test infrastructure agent for FurlanG2P. Handles test suite expansion, fixtures, golden sets, and coverage improvements.

> **v5**: This template includes YAML front-matter. Fill in `depends_on` and `repos` before use.

---

## YAML Front-Matter (v5)

```yaml
---
depends_on: [A1_library]    # tests typically depend on library changes
repos: [FurlanG2P]          # repos this prompt touches
---
```

---

## READ FIRST

1. `./README.md` — How to run tests
2. `./AGENTS.md` — Agent guidelines
3. `./tests/` — Existing test structure
4. `./workpacks/instances/<workpack>/00_request.md` — Original request
5. `./workpacks/instances/<workpack>/01_plan.md` — Full plan
6. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v5)

---

## Context

This is part of workpack: `YYYY-MM-DD_<category>_<short-slug>`

**Objective**: <!-- One-line summary of the test work to be done -->

---

## Delivery Mode

- **PR-based**: Open a PR targeting `main` and link it in `99_status.md`.
- **Direct push**: Push directly to `main`; record commits in `99_status.md`.

---

## Primary Modules

| Module | Path | Purpose |
|--------|------|---------|
| Tests | `tests/` | pytest suites, fixtures, golden sets |
| Examples | `examples/` | Usage examples (also serve as integration tests) |

---

## Objective

<!--
Describe WHAT test improvements must be made.
Focus on coverage gaps, missing fixtures, golden sets needed.
-->

---

## Reference Points

<!--
Example:
- **Test pattern**: Follow existing test structure in `tests/test_g2p.py`
- **Fixture pattern**: See `conftest.py` fixtures
- **Golden sets**: See `tests/golden/` for expected output format
-->

---

## Implementation Requirements

<!--
Example:
- Add parameterized tests for all dialect variants
- Create golden set fixtures for common Friulian words
- Ensure coverage of error paths (invalid input, missing lexicon entries)
-->

- Requirement 1
- Requirement 2

---

## Scope

### In Scope
- Test file creation/modification under `tests/`
- Fixture and golden set data
- Coverage configuration

### Out of Scope
- Library code changes (handled by A1_library)
- CLI code changes (handled by A2_cli)

---

## Verification

```bash
pip install -e ".[dev]"
python -m pytest tests/ -v --tb=short
python -m pytest tests/ --cov=furlan_g2p --cov-report=term-missing
```

---

## Handoff Output (JSON) — REQUIRED

**Path**: `./workpacks/instances/<workpack>/outputs/A3_tests.json`

<!-- lint-ignore-code-block -->
```json
{
  "schema_version": "1.0",
  "workpack": "<workpack>",
  "prompt": "A3_tests",
  "component": "tests",
  "delivery_mode": "<pr|direct_push>",
  "branch": { "base": "<base-branch>", "work": "<work-branch>", "merge_target": "main" },
  "repos": ["FurlanG2P"],
  "artifacts": { "pr_url": "", "commit_shas": [] },
  "changes": { "files_modified": [], "files_created": [], "contracts_changed": [], "breaking_change": false },
  "change_details": [],
  "verification": {
    "commands": [
      {"cmd": "python -m pytest tests/ -v", "result": "pass"}
    ],
    "regression_added": false,
    "regression_notes": ""
  },
  "execution": { "model": "", "tokens_in": 0, "tokens_out": 0, "duration_ms": 0 },
  "handoff": { "summary": "", "next_steps": [], "known_issues": [] },
  "notes": ""
}
```

---

## Stop Conditions

Stop and escalate if:

- Library API under test is not yet implemented
- Golden set data requires linguistic expertise not in docs

---

## Deliverables

- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Output JSON created
