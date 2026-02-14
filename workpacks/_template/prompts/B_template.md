# Bug Fix Agent Prompt (B#)

> Post-implementation bug fix prompt. Replace `B#` with the actual number (B1, B2, etc.) and update the filename accordingly.

> **v5**: This template includes YAML front-matter. Fill in `depends_on` and `repos` before use.

---

## YAML Front-Matter (v5)

```yaml
---
depends_on: []   # e.g., [A1_library] — prompt stems this fix depends on
repos: []        # e.g., [FurlanG2P] — repos this fix touches
---
```

---

## READ FIRST

1. `./README.md` — Project overview and setup
2. `./AGENTS.md` — Agent guidelines (if present)
3. `./workpacks/instances/<workpack>/00_request.md` — Original request
4. `./workpacks/instances/<workpack>/01_plan.md` — Full plan
5. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v5)

---

## Context

This is a **post-implementation bug fix** for workpack: `YYYY-MM-DD_<category>_<short-slug>`

**Component**: <!-- library | cli | tests | ml | docs | meta -->

---

## Delivery Mode

- **Direct to feature branch**: Commit directly to `feature/<feature-name>` (no sub-branch needed for bugfixes).

---

## Severity

<!-- MANDATORY in Protocol v4. Choose exactly one. -->

**Severity**: `<blocker|major|minor>`

| Level | Meaning | Merge Impact |
|-------|---------|--------------|
| `blocker` | Cannot proceed to merge | V-loop MUST NOT pass |
| `major` | Significant functionality impacted | V-loop SHOULD block |
| `minor` | Cosmetic or edge case | V-loop MAY proceed with note |

---

## Problem Description

<!--
Describe the bug clearly and concisely.
Focus on WHAT is happening vs WHAT should happen.
Do NOT propose specific code fixes here.
-->

**Expected behavior**: <!-- What should happen -->

**Actual behavior**: <!-- What is happening instead -->

---

## Reproduction Steps

<!--
How to reproduce the bug.
-->

1. <!-- Step 1 -->
2. <!-- Step 2 -->
3. <!-- Observe: actual behavior differs from expected -->

---

## Root Cause Analysis

<!--
If the cause is known, describe it at a conceptual level.
Do NOT include code snippets of the fix.

Example:
The event handler is registered multiple times because the component doesn't unsubscribe on disable.

If unknown:
"To be investigated by analyzing the component lifecycle."
-->

---

## Reference Points

<!--
Semantic references to help understand the issue and find the fix pattern.

Example:
- **Affected component**: `DebugMenuPanel` in `Assets/_Game/Scripts/Debug/`
- **Similar fix**: See how `SettingsPanel` handles event subscription cleanup
- **Relevant pattern**: Follow the dispose pattern used in `BaseScreen`
-->

- **Reference 1**: <!-- Description -->

---

## Implementation Requirements

<!--
Describe WHAT the fix must accomplish, not HOW to code it.

Example:
- The component must unsubscribe from events when disabled
- The fix must not affect the initialization flow
- Memory leaks must be prevented
-->

- Requirement 1
- Requirement 2

---

## Files Likely Affected

<!--
List files that probably need modification, but let the agent investigate.
-->

- `path/to/likely/file1.py` — <!-- Why this file -->
- `path/to/likely/file2.py` — <!-- Why this file -->

---

## Task Tracking

If your tool/model supports a structured todo list (e.g., `manage_todo_list`), use it to track the steps of this bugfix:

1. Investigate root cause
2. Implement minimal fix
3. Add regression test (if feasible)
4. Run verification commands
5. Create output JSON

> Task tracking is optional if the tool/model does not support it, but strongly encouraged when available.

---

## Scope

### In Scope

- Fixing the specific bug described
- Adding regression test if feasible

### Out of Scope

- Refactoring unrelated code
- Feature enhancements

---

## Acceptance Criteria

- [ ] Bug no longer reproducible
- [ ] No regressions introduced
- [ ] Existing tests still pass
- [ ] <!-- Additional criterion if applicable -->

---

## Constraints

- Fix must be minimal and focused on the bug
- Must not introduce breaking changes

---

## Verification

### Commands

```bash
# Build
<build command for the component>

# Run tests
<test command for the component>
```

### Verification Checklist

- [ ] Bug is fixed (verified via reproduction steps)
- [ ] Build succeeds
- [ ] Tests pass
- [ ] No new warnings or errors

---

## Regression Test

<!--
For B-series bugfixes, a regression test is strongly encouraged.
-->

- [ ] Regression test/check added (set `verification.regression_added=true` in output)
- **Regression location**: `<path/to/test/file>`
- **What it validates**: `<description of what the test checks>`

> If a regression test is not feasible, document why in `verification.regression_notes`.

---

## Handoff Output (JSON) — REQUIRED

After completing the work, create/update:

**Path**: `./workpacks/instances/<workpack>/outputs/B#_<component>_<description>.json`

<!-- lint-ignore-code-block -->
```json
{
  "schema_version": "1.0",
  "workpack": "<workpack>",
  "prompt": "B#_<component>_<description>",
  "component": "<library|cli|tests|ml|docs|meta>",
  "delivery_mode": "<pr|direct_push>",
  "severity": "<blocker|major|minor>",
  "branch": {
    "base": "feature/<feature-name>",
    "work": "feature/<feature-name>",
    "merge_target": "feature/<feature-name>"
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
    "commands": [],
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
    "summary": "",
    "next_steps": [],
    "known_issues": []
  },
  "notes": ""
}
```

---

## Stop Conditions

Stop and escalate if:

- Root cause cannot be determined
- Fix requires architectural changes
- Fix would introduce breaking changes

---

## Deliverables

- [ ] Bug fixed
- [ ] Regression test added (if feasible)
- [ ] Output JSON created (with `severity` field)
- [ ] Changes committed to feature branch
- [ ] V2_bugfix_verify.md will confirm resolution in V-loop
