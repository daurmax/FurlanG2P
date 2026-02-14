# Status

> Track completion status, PR links, and merge order. (Protocol v5)

## Overall Status

<!-- Update this as work progresses -->

| Status | Description |
|--------|-------------|
| 🟡 In Progress | Work is underway |

**Last Updated**: YYYY-MM-DD

## Checklist

### Workpack Artifacts
- [ ] `00_request.md` complete
- [ ] `01_plan.md` complete
- [ ] Agent prompts A-series complete
- [ ] `outputs/` folder present (Protocol v2+)
- [ ] Handoff outputs JSON updated for completed prompts
- [ ] No placeholders remain
- [ ] V-series verification completed (Protocol v4)
- [ ] B-series severity assigned for all bug reports (Protocol v4)
- [ ] YAML front-matter (depends_on, repos) in all prompts (Protocol v5)
- [ ] Execution block in all output JSONs (Protocol v5)

### Implementation Progress (A-series)
- [ ] Task 1: Description
- [ ] Task 2: Description
- [ ] Task 3: Description
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Integration complete

### Bug Fixes (B-series)

> **Note**: This section is added when bug fix prompts are created.
> Delete this section if no bug fixes are needed yet.

- [ ] B1: Bug fix description
- [ ] B2: Bug fix description

### Verification (V-series) — Protocol v4

> **V-series** prompts are mandatory verification gates.
> V1 is the A5 integration verification. V2 is the post-bugfix V-loop.

- [ ] V1 (A5 gate): Integration verification passed
- [ ] V2 (V-loop): All B-series fixes verified (if B-series exist)

## Outputs (Protocol v5)

<!-- Track handoff output JSON files for each completed prompt -->

| Prompt | Output JSON Path | Status |
|--------|------------------|--------|
| A0_bootstrap | `outputs/A0_bootstrap.json` | ⚪ Not Created |
| A1_library | `outputs/A1_library.json` | ⚪ Not Created |
| A2_cli | `outputs/A2_cli.json` | ⚪ Not Created |
| A3_tests | `outputs/A3_tests.json` | ⚪ Not Created |
| A4_ml | `outputs/A4_ml.json` | ⚪ Not Created |
| A5_integration_meta | `outputs/A5_integration_meta.json` | ⚪ Not Created |
| V2_bugfix_verify | `outputs/V2_bugfix_verify.json` | ⚪ Not Created |

### Output Status Legend

- ⚪ Not Created (prompt not complete yet)
- 🟢 Created (JSON exists and is valid)
- 🔴 Missing (prompt complete but JSON missing)

## Agent Progress

### Feature Implementation (A-series)

| Agent | Status | PR Link | Notes |
|-------|--------|---------|-------|
| A0_bootstrap | ⚪ Skipped | - | - |
| A1_library | 🔴 Not Started | - | - |
| A2_cli | 🔴 Not Started | - | - |
| A3_tests | 🔴 Not Started | - | - |
| A4_ml | 🔴 Not Started | - | - |
| A5_integration_meta | 🔴 Not Started | - | - |

### Bug Fixes (B-series)

> **Note**: This section is added when bug fix prompts are created.

| Agent | Severity | Status | Notes |
|-------|----------|--------|-------|
| B1_xxx | blocker/major/minor | 🔴 Not Started | - |
| B2_xxx | blocker/major/minor | 🔴 Not Started | - |

### Verification (V-series) — Protocol v4

| Agent | Iteration | Status | Notes |
|-------|-----------|--------|-------|
| V2_bugfix_verify | 0 | 🔴 Not Started | Runs after B-series complete |

### Retrospective (R-series) — Protocol v5

| Agent | Status | Notes |
|-------|--------|-------|
| R1_retrospective | 🔴 Not Started | Post-merge |

### B-Series Budget

| Metric | Value |
|--------|-------|
| Total B-series | 0 |
| Budget warning (>5) | No |
| Rescope needed (>8) | No |

### Status Legend

- 🔴 Not Started
- 🟡 In Progress
- 🟢 Complete
- ⚪ Skipped (not needed)

## Pull Requests

<!-- List all PRs created for this workpack -->

| Component | PR # | Title | Status |
|-----------|------|-------|--------|
| Library | - | - | - |
| CLI | - | - | - |
| Meta | - | - | - |

## Merge Order

> **v5 lifecycle**: A0 → A1–A4 (parallel) → A5/V1 (verify) → [B-series] → V2 (V-loop) → MERGE → R1

<!-- Specify the order in which PRs should be merged -->

1. Library PR (no dependencies)
2. CLI PR (after Library if shared interfaces changed)
3. Integration PR (after all component PRs)

## Issues Encountered

<!-- Document any blockers or issues -->

| Issue | Resolution | Date |
|-------|------------|------|
| - | - | - |

## Post-Completion Notes

<!-- Any lessons learned or follow-up items -->

- Lesson 1
- Follow-up item 1

## Execution Cost Summary (v5)

<!-- Populated from output JSONs after completion -->

| Prompt | Model | Tokens In | Tokens Out | Duration |
|--------|-------|-----------|------------|----------|
| A1_library | - | - | - | - |
| A2_cli | - | - | - | - |
| A5_integration_meta | - | - | - | - |
| **Total** | | **-** | **-** | **-** |
