# Bugfix Verification Agent Prompt (V-Loop)

> Post-bugfix verification gate. This prompt runs iteratively after B-series fixes are applied until all bugs are confirmed resolved and all tests pass.

> **V-Loop**: This is a single prompt that runs multiple iterations. Do NOT create V3, V4, etc. — re-run this same prompt with updated context.

---

## READ FIRST

1. `./workpacks/instances/<workpack>/00_request.md` — Original request and acceptance criteria
2. `./workpacks/instances/<workpack>/01_plan.md` — Full plan including B-series section
3. `./workpacks/instances/<workpack>/99_status.md` — Current status of all prompts
4. `./workpacks/instances/<workpack>/outputs/*.json` — All agent handoff outputs (especially B-series)
5. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v5)

---

## Context

This is a **post-bugfix verification gate** for workpack: `YYYY-MM-DD_<category>_<short-slug>`

**Role**: V-Loop verification agent — validates that all B-series fixes are working correctly.

---

## Delivery Mode

- **Direct to feature branch**: commit verification results directly to `feature/<feature-name>`.

---

## Objective

After B-series bug fix prompts have been resolved, this verification agent:

1. Re-runs all test suites (`pytest`, `mypy`, `ruff`)
2. Verifies each B-series bug is actually fixed by re-running reproduction steps
3. Cross-checks acceptance criteria that were previously failing
4. If NEW issues are found → generates new B-series prompts (with `## Severity`) and the V-loop continues
5. If all checks pass → authorizes merge

This is an **iterative** process. The V-loop terminates when:
- All tests pass
- All B-series bugs are confirmed resolved
- All acceptance criteria are satisfied
- No new issues are discovered

---

## Reference Points

- **B-series outputs**: Read each `outputs/B#_*.json` for details of what was fixed
- **A5 output**: Read `outputs/A5_integration_meta.json` for the original blocking issues
- **Test commands**: Same as those in `A5_integration_meta.md` verification section

---

## Subagent Strategy

The V-loop agent may spawn subagents for parallelizable verification tasks:

- **Subagent 1**: Run `pytest` while main agent verifies B-series fixes
- **Subagent 2**: Run `mypy` and `ruff` while main agent checks acceptance criteria
- **Subagent 3**: Run workpack linter while other checks proceed

> Document subagent usage in the output JSON `handoff.summary`.

---

## Task Tracking

The V-loop involves multiple verification steps per iteration. If your tool/model supports a structured todo list (e.g., `manage_todo_list`), use it to:

1. Create a todo for each verification step (test suites, B-series checks, AC cross-check, budget check, decision)
2. Mark each step in-progress before starting and completed immediately after
3. At iteration boundaries, reset the list for the new iteration

> Task tracking is optional if the tool/model does not support it, but strongly encouraged when available.

---

## Implementation Requirements

### 1. Re-Run Test Suites

```bash
# Run tests
pytest

# Type checking
mypy src/ tests/

# Lint
ruff check src/ tests/
```

**Pass criteria**:
- [ ] All tests pass (0 failures)
- [ ] `mypy` reports no errors
- [ ] `ruff` reports no violations

### 2. Verify Each B-Series Fix

For each B-series prompt marked as complete:

| B# | Bug Description | Reproduction Result | Status |
|----|-----------------|---------------------|--------|
| B1 | <!-- from prompt --> | <!-- Pass/Fail --> | ✅/❌ |
| B2 | <!-- from prompt --> | <!-- Pass/Fail --> | ✅/❌ |

**Verify by**:
- Re-running reproduction steps from the B-series prompt
- Checking that the expected behavior now occurs
- Confirming regression tests pass (if added)

### 3. Cross-Check Acceptance Criteria

Re-verify any AC that was failing before B-series fixes:

| AC ID | Criterion | Previous Status | Current Status |
|-------|-----------|-----------------|----------------|
| <!-- AC# --> | <!-- from 00_request --> | ❌ | ✅/❌ |

### 4. B-Series Budget Check

Count total B-series prompts in this workpack:

- **≤5**: Normal workflow
- **6-8**: Emit warning in output: `"b_series_budget_warning": true`
- **>8**: Suggest re-scoping in output and `handoff.known_issues`

### 5. Decision

If ALL checks pass:
- Set merge decision to **PASS**
- Proceed with merge authorization

If ANY check fails:
- Generate new B-series prompts for new issues found (with `## Severity`)
- Update `01_plan.md` and `99_status.md`
- Set merge decision to **FAIL — new B-series created, V-loop continues**
- This prompt will be re-run after new B-series are resolved

---

## Scope

### In Scope

- Verifying B-series fixes are working
- Re-running test suites
- Cross-checking acceptance criteria
- Generating new B-series if new bugs found
- Authorizing or blocking merge

### Out of Scope

- Modifying code outside the scope of this verification
- Refactoring or feature work

---

## Acceptance Criteria

- [ ] All test suites pass
- [ ] All B-series bugs confirmed resolved
- [ ] All acceptance criteria verified
- [ ] No new blocking issues discovered
- [ ] B-series budget assessed

---

## Constraints

- **CRITICAL**: Do NOT implement fixes — only verify and report
- **CRITICAL**: Do NOT push to `main` without a PR — all work targets the feature branch
- **CRITICAL**: If new bugs found, create B-series prompts with `## Severity`

---

## Handoff Output (JSON) — REQUIRED

After completing the verification, create/update:

**Path**: `./workpacks/instances/<workpack>/outputs/V2_bugfix_verify.json`

<!-- lint-ignore-code-block -->
```json
{
  "schema_version": "1.0",
  "workpack": "<workpack>",
  "prompt": "V2_bugfix_verify",
  "component": "meta",
  "delivery_mode": "<pr|direct_push>",
  "iteration": 1,
  "branch": {
    "base": "<base-branch>",
    "work": "<work-branch>",
    "merge_target": "main"
  },
  "repos": [],
  "artifacts": {
    "pr_url": "",
    "commit_shas": []
  },
  "changes": {
    "files_modified": [],
    "files_created": [],
    "contracts_changed": [],
    "breaking_change": false
  },
  "change_details": [],
  "verification": {
    "commands": [
      {"cmd": "pytest", "result": "pass"},
      {"cmd": "mypy src/ tests/", "result": "pass"},
      {"cmd": "ruff check src/ tests/", "result": "pass"}
    ],
    "regression_added": false,
    "regression_notes": ""
  },
  "execution": {
    "model": "",
    "tokens_in": 0,
    "tokens_out": 0,
    "duration_ms": 0
  },
  "b_series_resolved": ["B1_xxx", "B2_xxx"],
  "b_series_remaining": [],
  "b_series_budget_warning": false,
  "severity": null,
  "handoff": {
    "summary": "V-loop iteration 1: all B-series fixes verified, tests pass, AC satisfied.",
    "next_steps": [],
    "known_issues": []
  },
  "notes": ""
}
```

**Iteration tracking**: Increment `"iteration"` on each re-run. Previous iteration outputs may be kept as `V2_bugfix_verify_iter1.json`, etc., or overwritten.

---

## Stop Conditions

Stop and **block the merge** if:

- A blocker-severity bug cannot be resolved
- The V-loop has run 3+ iterations without convergence (suggest re-scoping)
- Test infrastructure is broken (not a code issue)

> **Authority**: As the V-loop gate agent, you have authority to reject integration if quality gates fail.

---

## Deliverables

- [ ] All test suites executed
- [ ] Each B-series fix verified
- [ ] Acceptance criteria cross-checked
- [ ] B-series budget assessed
- [ ] Output JSON created (with iteration count)
- [ ] `99_status.md` updated
- [ ] Merge decision rendered (PASS or FAIL with new B-series)
