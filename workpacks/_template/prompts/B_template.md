# Bug Fix Agent Prompt (B#)

> Post-implementation bug fix prompt. Replace `B#` with the actual number (B1, B2, etc.) and update the filename accordingly.

---

## READ FIRST

1. `README.md` — Project overview
2. `AGENTS.md` — Agent guidelines
3. `./workpacks/<workpack>/00_request.md` — Original request
4. `./workpacks/<workpack>/01_plan.md` — Full plan
5. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v3)

---

## Context

This is a **post-implementation bug fix** for workpack: `YYYY-MM-DD_<category>_<short-slug>`

**Component**: <!-- library | cli | tests | docs | normalization | g2p | phonology | tokenization -->

---

## Delivery Mode

- **Direct to feature branch**: Commit directly to `feature/<feature-name>` (no sub-branch needed for bugfixes).

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
The stress assignment fails because long vowels are not detected correctly.

If unknown:
"To be investigated by analyzing the stress assignment logic."
-->

---

## Reference Points

<!--
Semantic references to help understand the issue and find the fix pattern.

Example:
- **Affected component**: `StressAssigner` in `src/furlan_g2p/phonology/`
- **Similar fix**: See how `Syllabifier` handles edge cases
- **Relevant pattern**: Follow the validation pattern used in `Normalizer`
-->

- **Reference 1**: <!-- Description -->

---

## Implementation Requirements

<!--
Describe WHAT the fix must accomplish, not HOW to code it.

Example:
- The stress assigner must correctly identify long vowels
- The fix must not affect other stress patterns
- Edge cases must be handled gracefully
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
- Type hints required for any new/modified code

---

## Verification

### Commands

```bash
# Run all tests
pytest tests/ -v

# Run specific test (if applicable)
pytest tests/test_<module>.py -v -k "<test_name>"

# Type check
mypy src/

# Lint
ruff check src/ tests/
```

### Checklist

- [ ] Bug no longer occurs
- [ ] All tests pass
- [ ] Type checking passes
- [ ] Linting passes
- [ ] Regression test added

---

## Handoff Output (JSON) — REQUIRED

After completing, create: `outputs/B#_<component>_<description>.json`

```json
{
  "schema_version": "1.0",
  "workpack": "<workpack>",
  "prompt": "B#_<component>_<description>",
  "component": "<component>",
  "delivery_mode": "direct_push",
  "branch": {
    "base": "feature/<slug>",
    "work": "feature/<slug>",
    "merge_target": "main"
  },
  "artifacts": {
    "commit_shas": ["<sha>"]
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
      { "cmd": "mypy src/", "result": "pass" }
    ],
    "regression_added": true
  },
  "handoff": {
    "summary": "<one-line summary of the fix>",
    "known_issues": [],
    "next_steps": []
  }
}
```

---

## Stop Conditions

### Continue if:
- Fix is straightforward and tests pass

### Escalate if:
- Root cause is unclear
- Fix would require significant refactoring
- Multiple components are affected

---

## Deliverables

- [ ] Bug fixed
- [ ] Regression test added
- [ ] All tests pass
- [ ] `outputs/B#_<component>_<description>.json` created
- [ ] `99_status.md` updated
