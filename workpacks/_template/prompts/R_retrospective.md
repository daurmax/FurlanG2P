# Retrospective (R-Series) — Protocol v5

> Post-merge retrospective capturing lessons learned, cost data, and improvement signals for future workpacks.

> **When**: Fill this out **after** the workpack is merged to `main`. It is the last artifact produced.

---

## READ FIRST

1. `./workpacks/instances/<workpack>/00_request.md` — Original request and acceptance criteria
2. `./workpacks/instances/<workpack>/01_plan.md` — Full plan with WBS
3. `./workpacks/instances/<workpack>/99_status.md` — Final status
4. `./workpacks/instances/<workpack>/outputs/*.json` — All agent handoff outputs

---

## Context

**Workpack**: `YYYY-MM-DD_<category>_<short-slug>`
**Merge Date**: YYYY-MM-DD
**Total Duration**: <!-- e.g., 3 days from first commit to merge -->

---

## What Went Well

<!-- List things that worked effectively -->

- Item 1
- Item 2

---

## What Didn't Go Well

<!-- List problems, friction, or surprises -->

- Item 1
- Item 2

---

## Metrics

### B-Series Summary

| Metric | Value |
|--------|-------|
| Total B-series created | 0 |
| Blocker count | 0 |
| Major count | 0 |
| Minor count | 0 |
| V-loop iterations | 0 |
| Budget warning triggered | No |

### Execution Cost (optional)

<!-- Populated from output JSON `execution` blocks, if available -->

| Prompt | Model | Tokens In | Tokens Out | Duration |
|--------|-------|-----------|------------|----------|
| A1_library | — | — | — | — |
| A2_cli | — | — | — | — |
| A5_integration_meta | — | — | — | — |
| **Total** | — | **—** | **—** | **—** |

### Estimation Accuracy

| Prompt | Estimated Effort | Actual Effort | Delta |
|--------|-----------------|---------------|-------|
| A1_library | M | — | — |
| A2_cli | S | — | — |

---

## Root Causes of B-Series

<!-- For each B-series bug, explain WHY it occurred — not what it was -->

| B# | Root Cause Category | Description |
|----|---------------------|-------------|
| B1 | Incomplete spec | Acceptance criterion missed edge case |
| B2 | Integration gap | Library/CLI contract mismatch |

**Root Cause Categories**: `incomplete_spec`, `integration_gap`, `regression`, `environment`, `unclear_prompt`, `agent_error`, `tooling`, `other`

---

## Prompt Quality Assessment

<!-- Rate each prompt's effectiveness -->

| Prompt | Quality | Issue (if any) |
|--------|---------|----------------|
| A1_library | ✅ Good | — |
| A2_cli | ⚠️ Fair | Reference Points were stale |
| A5_integration | ✅ Good | — |

**Quality levels**: ✅ Good (agent succeeded without issues), ⚠️ Fair (minor clarifications needed), ❌ Poor (agent struggled, prompt needs rewrite)

---

## Lessons Learned

<!-- Actionable takeaways to improve future workpacks -->

| # | Lesson | Applicable To |
|---|--------|---------------|
| 1 | <!-- Lesson --> | <!-- Future workpacks, PROMPT_STYLE_GUIDE, templates, etc. --> |
| 2 | <!-- Lesson --> | <!-- Where to apply --> |

---

## Style Guide Updates

<!-- If lessons suggest changes to the PROMPT_STYLE_GUIDE.md, list them here -->

- [ ] Update to apply: <!-- description -->
- [ ] N/A — No style guide changes needed

---

## Cross-Workpack Notes

<!-- If this workpack revealed issues that affect other workpacks, note them -->

| Affected Workpack | Issue | Action |
|-------------------|-------|--------|
| — | — | — |

---

## Handoff Output (JSON) — OPTIONAL

If the R-series retrospective is tracked as an output:

**Path**: `./workpacks/instances/<workpack>/outputs/R1_retrospective.json`

<!-- lint-ignore-code-block -->
```json
{
  "schema_version": "1.0",
  "workpack": "<workpack>",
  "prompt": "R1_retrospective",
  "component": "meta",
  "delivery_mode": "direct_push",
  "branch": {
    "base": "main",
    "work": "main",
    "merge_target": "main"
  },
  "artifacts": { "pr_url": "", "commit_shas": [] },
  "changes": {
    "files_modified": [],
    "files_created": ["workpacks/instances/<workpack>/prompts/R1_retrospective.md"],
    "contracts_changed": [],
    "breaking_change": false
  },
  "verification": { "commands": [], "regression_added": false, "regression_notes": "" },
  "execution": {
    "model": "",
    "tokens_in": 0,
    "tokens_out": 0,
    "duration_ms": 0
  },
  "handoff": {
    "summary": "Retrospective completed for workpack.",
    "next_steps": [],
    "known_issues": []
  },
  "notes": ""
}
```
