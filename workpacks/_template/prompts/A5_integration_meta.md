# Integration Agent Prompt (Meta Repo) — Merge Reviewer (V1 Gate)

> The Integration Agent is the **final gatekeeper** for workpack completion. It validates that all agents followed their directives, executes test suites, and authorizes the merge. In Protocol v4+, this is the **V1 verification gate**.

> **Fixed Role**: This prompt is ALWAYS named `A5_integration_meta.md` regardless of how many A-series prompts exist. A5 is a role, not a sequence number.

---

## READ FIRST

- `./README.md` — Project overview
- `./AGENTS.md` — Agent guidelines
- `./workpacks/instances/<workpack>/00_request.md` — Original request and acceptance criteria
- `./workpacks/instances/<workpack>/01_plan.md` — Full plan with WBS
- `./workpacks/instances/<workpack>/99_status.md` — Current completion status
- `./workpacks/instances/<workpack>/outputs/*.json` — All agent handoff outputs
- `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v5)

---

## Context

This is part of workpack: `YYYY-MM-DD_<category>_<short-slug>`

**Objective**: Validate all workpack deliverables, execute test suites, and complete integration.

---

## Delivery Mode

- **PR-based**: Open a PR targeting `main` and link it in `99_status.md`.
- **Direct push**: Push directly to `main`; record commits in `99_status.md`.

---

## Role: Merge Reviewer (V1 Verification Gate)

The Integration Agent has **four responsibilities**:

1. **Validate Agent Outputs** — Verify all completed prompts have valid output JSONs
2. **Execute Test Suites** — Run tests, type checks, and lint to catch regressions
3. **Cross-Check Acceptance Criteria** — Ensure all AC from `00_request.md` are satisfied
4. **Generate B-Series if Blocked** — If verification fails, create B-series prompts (with mandatory `## Severity`) and ensure `V2_bugfix_verify.md` exists

**Authority**: The Integration Agent can **block the merge** if verification fails.

**V-Loop Awareness**: If this agent blocks the merge and creates B-series prompts, it must also ensure `V2_bugfix_verify.md` exists (create from template `_template/prompts/V_bugfix_verify.md` if first B-series).

---

## Prerequisites Checklist

Before starting integration, verify:

- [ ] All A-series prompts marked complete in `99_status.md`
- [ ] All B-series prompts (if any) marked complete in `99_status.md`
- [ ] All `outputs/*.json` files exist for completed prompts
- [ ] All component PRs merged or ready

---

## Phase 1: Validate Agent Outputs

### 1.1 Run Workpack Linter

```bash
python workpacks/tools/workpack_lint.py
```

- [ ] Linter passes with no errors
- [ ] All warnings reviewed (v3 code-block warnings acceptable during transition)

### 1.2 Review Output JSONs

For each `outputs/<PROMPT>.json`:

- [ ] `workpack` field matches the workpack folder name
- [ ] `prompt` field matches the prompt basename
- [ ] `verification.commands` lists the commands actually run
- [ ] `handoff.summary` describes what was done
- [ ] `changes.files_modified` and `changes.files_created` are populated

### 1.3 Cross-Reference with 99_status.md

- [ ] Every prompt marked ✅/🟢 has a corresponding output JSON
- [ ] No output JSON exists for prompts not marked complete

---

## Subagent Strategy

The A5 agent may spawn subagents for parallelizable validation tasks:

- **Subagent 1**: Run Python tests (`python -m pytest tests/ -v`) while main agent validates output JSONs
- **Subagent 2**: Run type checks (`mypy src/ tests/`) while main agent cross-checks acceptance criteria
- **Subagent 3**: Run workpack linter while other checks proceed

> Document subagent usage in the output JSON `handoff.summary`.

---

## Task Tracking

This prompt involves multi-step verification work. If your tool/model supports a structured todo list (e.g., `manage_todo_list`), use it to:

1. Break verification into discrete steps (output validation, pytest, mypy, ruff, AC cross-check, etc.)
2. Mark each step in-progress before starting and completed immediately after
3. Use the list as a checkpoint — do not skip verification steps

> Task tracking is optional if the tool/model does not support it, but strongly encouraged when available.

---

## Phase 2: Execute Test Suites (Standard Checklist)

### 2.1 Python Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run type checking
mypy src/ tests/

# Run linting
ruff check src/ tests/
```

**Pass criteria**:
- [ ] All tests pass (0 failures)
- [ ] Type checking passes without errors
- [ ] Linting passes without errors
- [ ] No new warnings introduced (or warnings are documented)

### 2.2 Workpack-Specific Verification

<!--
Add workpack-specific verification commands here.
These are custom checks beyond the standard test suites.
-->

<!-- Example:
```bash
# Verify CLI command works
furlang2p --help

# Check documentation
# python -m sphinx docs/ docs/_build/
```
-->

---

## Phase 3: Cross-Check Acceptance Criteria

### 3.1 Load Acceptance Criteria

Read `./workpacks/<workpack>/00_request.md` and extract all acceptance criteria.

### 3.2 Verification Matrix

For each acceptance criterion:

| AC ID | Criterion | How Verified | Result |
|-------|-----------|--------------|--------|
| AC1 | <!-- from 00_request --> | <!-- test/manual/command --> | ✅/❌ |
| AC2 | <!-- from 00_request --> | <!-- test/manual/command --> | ✅/❌ |

**All AC must be ✅ to proceed with merge.**

### 3.3 Review Handoff Summaries

Read `handoff.summary` from each output JSON to understand what each agent delivered.

- [ ] Summaries align with the acceptance criteria
- [ ] No `known_issues` entries that block acceptance

### 3.4 B-Series Generation (if blocked)

If any acceptance criterion fails or tests fail:

1. Create B-series prompt(s) for each issue found, following `_template/prompts/B_template.md`
2. **Assign severity** to each: `blocker`, `major`, or `minor`
3. If these are the first B-series prompts, create `V2_bugfix_verify.md` from `_template/prompts/V_bugfix_verify.md`
4. Update `01_plan.md` with B-series section (including severity and V-loop phase)
5. Update `99_status.md` with B-series and V-series tracking
6. Set merge decision to **BLOCK** with clear blocking reasons

---

## Phase 4: Finalize and Deliver

### 4.1 Update Workpack Status

Edit `./workpacks/instances/<workpack>/99_status.md`:

- [ ] Mark A5_integration_meta as ✅ Complete
- [ ] Set overall status to 🟢 Complete
- [ ] Add PR links or commit SHAs
- [ ] Add merge order if applicable

### 5.2 Deliver According to Mode

**PR-based**:
1. Create PR targeting `main`
2. Link PR in `99_status.md`
3. Request review if required

**Direct push**:
1. Push to `main`
2. Record commit SHAs in `99_status.md`

---

## Scope

### In Scope

- Validating all agent outputs
- Running test suites
- Cross-checking acceptance criteria
- Finalizing workpack status

### Out of Scope

- Fixing failing tests (escalate instead)

---

## Acceptance Criteria

- [ ] All tests pass (`python -m pytest tests/ -v`)
- [ ] Type checking passes (`mypy src/ tests/`)
- [ ] Linting passes (`ruff check src/ tests/`)
- [ ] All acceptance criteria verified
- [ ] `99_status.md` updated to complete
- [ ] Delivered according to delivery mode

---

## Constraints

- **CRITICAL**: Do NOT push to `main` without a PR (unless direct push delivery mode)
- **CRITICAL**: Do NOT mark complete if any test fails — escalate instead
- **CRITICAL**: A5 is a fixed role name — never renumber to A3 or other

---

## Handoff Output (JSON) — REQUIRED

After completing the work, create/update:

**Path**: `./workpacks/instances/<workpack>/outputs/A5_integration_meta.json`

<!-- lint-ignore-code-block -->
```json
{
  "schema_version": "1.0",
  "workpack": "<workpack>",
  "prompt": "A5_integration_meta",
  "component": "meta",
  "delivery_mode": "<pr|direct_push>",
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
      {"cmd": "python workpacks/tools/workpack_lint.py", "result": "pass"},
      {"cmd": "python -m pytest tests/ -v", "result": "pass"},
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
  "handoff": {
    "summary": "All agents validated, tests passed, workpack complete.",
    "next_steps": [],
    "known_issues": []
  },
  "notes": ""
}
```

---

## Stop Conditions

Stop and **block the merge** if:

- Any test suite fails (escalate with failure details)
- Linter reports errors (not just warnings)
- Acceptance criteria cannot be verified
- Git issues affecting the working tree
- `known_issues` in any output JSON are blocking

> **Authority**: As the Merge Reviewer, you have the authority to reject the integration if quality gates fail. Document the reason and escalate to the user.

---

## Deliverables

- [ ] Linter validation complete
- [ ] Test suites executed and passed
- [ ] Acceptance criteria cross-checked
- [ ] `99_status.md` updated
- [ ] Output JSON created
- [ ] Delivered according to delivery mode
