# Integration Agent Prompt — Merge Reviewer

> The Integration Agent is the **final gatekeeper** for workpack completion. It validates that all agents followed their directives, executes test suites, and authorizes the merge.

---

## READ FIRST

- `./README.md` — Project overview
- `./AGENTS.md` — Agent guidelines
- `./workpacks/<workpack>/00_request.md` — Original request and acceptance criteria
- `./workpacks/<workpack>/01_plan.md` — Full plan with WBS
- `./workpacks/<workpack>/99_status.md` — Current completion status
- `./workpacks/<workpack>/outputs/*.json` — All agent handoff outputs
- `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v3)

---

## Context

This is part of workpack: `YYYY-MM-DD_<category>_<short-slug>`

**Objective**: Validate all workpack deliverables, execute test suites, and complete integration.

---

## Delivery Mode

- **PR-based**: Open a PR targeting `main` and link it in `99_status.md`.
- **Direct push**: Push directly to `main`; record commits in `99_status.md`.

---

## Role: Merge Reviewer

The Integration Agent has **three responsibilities**:

1. **Validate Agent Outputs** — Verify all completed prompts have valid output JSONs
2. **Execute Test Suites** — Run pytest, mypy, ruff to catch regressions
3. **Cross-Check Acceptance Criteria** — Ensure all AC from `00_request.md` are satisfied

**Authority**: The Integration Agent can **block the merge** if verification fails.

---

## Prerequisites Checklist

Before starting integration, verify:

- [ ] All A-series prompts marked complete in `99_status.md`
- [ ] All B-series prompts (if any) marked complete in `99_status.md`
- [ ] All `outputs/*.json` files exist for completed prompts

---

## Phase 1: Validate Agent Outputs

### 1.1 Review Output JSONs

For each `outputs/<PROMPT>.json`:

- [ ] `workpack` field matches the workpack folder name
- [ ] `prompt` field matches the prompt basename
- [ ] `verification.commands` lists the commands actually run
- [ ] `handoff.summary` describes what was done
- [ ] `changes.files_modified` and `changes.files_created` are populated

### 1.2 Cross-Reference with 99_status.md

- [ ] Every prompt marked ✅/🟢 has a corresponding output JSON
- [ ] No output JSON exists for prompts not marked complete

---

## Phase 2: Execute Test Suites (Standard Checklist)

### 2.1 Install Dependencies

```bash
pip install -e ".[dev]"
```

### 2.2 Run Tests

```bash
pytest tests/ -v
```

**Pass criteria**:
- [ ] All tests pass (0 failures)

### 2.3 Type Checking

```bash
mypy src/
```

**Pass criteria**:
- [ ] No type errors

### 2.4 Linting

```bash
ruff check src/ tests/
```

**Pass criteria**:
- [ ] No linting errors

### 2.5 Format Check

```bash
ruff format --check src/ tests/
```

**Pass criteria**:
- [ ] No formatting issues (or fix them)

---

## Phase 3: Cross-Check Acceptance Criteria

### 3.1 Review 00_request.md

For each acceptance criterion in `00_request.md`:

| AC ID | Criterion | Verified By | Status |
|-------|-----------|-------------|--------|
| AC1 | <!-- Copy from 00_request.md --> | <!-- Test or command --> | ⬜ |
| AC2 | <!-- Copy from 00_request.md --> | <!-- Test or command --> | ⬜ |

### 3.2 Manual Verification (if required)

- [ ] <!-- Manual check 1 -->
- [ ] <!-- Manual check 2 -->

---

## Phase 4: Complete Integration

### 4.1 If All Checks Pass

1. Create PR (if PR-based delivery)
2. Update `99_status.md` with final status
3. Create `outputs/A5_integration.json`

### 4.2 If Any Check Fails

1. Document failure in `99_status.md`
2. Create B-series bug fix prompt if needed
3. Do NOT merge until issues are resolved

---

## Verification Summary

### Commands

```bash
# Full verification suite
pip install -e ".[dev]"
pytest tests/ -v
mypy src/
ruff check src/ tests/
ruff format --check src/ tests/
```

### Final Checklist

- [ ] All agent output JSONs valid
- [ ] All tests pass
- [ ] Type checking passes
- [ ] Linting passes
- [ ] All acceptance criteria met
- [ ] No known blocking issues

---

## Handoff Output (JSON) — REQUIRED

After completing integration, create:

**Path**: `./workpacks/<workpack>/outputs/A5_integration.json`

```json
{
  "schema_version": "1.0",
  "workpack": "<workpack>",
  "prompt": "A5_integration",
  "component": "integration",
  "delivery_mode": "<pr|direct_push>",
  "branch": {
    "base": "feature/<slug>",
    "work": "feature/<slug>",
    "merge_target": "main"
  },
  "artifacts": {
    "pr_url": "<PR URL if applicable>",
    "commit_shas": ["<merge commit SHA>"]
  },
  "changes": {
    "files_modified": [],
    "files_created": [],
    "contracts_changed": [],
    "breaking_change": false
  },
  "verification": {
    "commands": [
      { "cmd": "pytest tests/ -v", "result": "pass" },
      { "cmd": "mypy src/", "result": "pass" },
      { "cmd": "ruff check src/ tests/", "result": "pass" }
    ],
    "all_ac_verified": true
  },
  "handoff": {
    "summary": "All checks passed, workpack complete",
    "known_issues": [],
    "next_steps": ["Merge PR", "Tag release if applicable"]
  }
}
```

---

## Stop Conditions

### Authorize Merge if:
- All tests pass
- All acceptance criteria verified
- No blocking issues in any agent output

### Block Merge if:
- Any test fails
- Type checking fails
- Acceptance criterion not met
- Agent output JSON missing or invalid

---

## Deliverables

- [ ] All agent outputs validated
- [ ] Full test suite passed
- [ ] All acceptance criteria verified
- [ ] `outputs/A5_integration.json` created
- [ ] `99_status.md` updated with final status
- [ ] PR created (if PR-based) or commits recorded (if direct push)
