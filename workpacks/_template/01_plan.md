# Plan

> Work Breakdown Structure, sequencing, and parallelization map for this workpack. (Protocol v5)

## Summary

<!-- One-paragraph summary of what will be done -->

## Work Breakdown Structure (WBS)

<!-- Break down the work into discrete tasks -->

| # | Task | Agent | Depends On | Estimated Effort |
|---|------|-------|------------|------------------|
| 1 | Task description | Library / CLI / Tests / ML / Docs / Integration | - | S / M / L |
| 2 | Task description | Agent | Task 1 | S / M / L |
| 3 | Task description | Agent | - | S / M / L |

## Parallelization Map

<!-- Visual or textual representation of what can run in parallel -->

```
Phase 1 (parallel):
  ├── A1_library.md  ─┐
  ├── A2_cli.md      ─┼──► Phase 2
  └── A4_ml.md       ─┘

Phase 2 (sequential — verification gate):
  └── A5_integration_meta.md (V1 gate)

Phase 3 (conditional — only if bugs found):
  ├── B1_*.md  ─┐
  ├── B2_*.md  ─┼──► Phase 4
  └── B3_*.md  ─┘

Phase 4 (V-loop — iterative until convergence):
  └── V2_bugfix_verify.md → re-run until all pass

Phase 5 (post-merge — retrospective, v5):
  └── R1_retrospective.md
```

### Parallel Groups

| Group | Agents | Notes |
|-------|--------|-------|
| Group A | Library, CLI | No shared files; safe to parallelize |
| Group B | ML, Docs | Can run with Group A |

### Sequential Dependencies

| Must Complete First | Before Starting |
|---------------------|-----------------|
| A0_bootstrap | All others |
| Group A + B | A5_integration_meta (V1 gate) |
| A5/V1 verification | B-series (only if bugs found) |
| All B-series fixes | V2_bugfix_verify (V-loop) |

## Sequencing Notes

<!-- Any special ordering requirements -->

1. Step 1 must complete before Step 2 because...
2. Steps 3 and 4 can run in parallel because...

## DAG Dependencies (v5)

<!-- Declare the dependency graph for all prompts. This MUST match the YAML front-matter in each prompt. -->

| Prompt | depends_on | repos |
|--------|-----------|-------|
| A0_bootstrap | [] | [] |
| A1_library | [A0_bootstrap] | [FurlanG2P] |
| A2_cli | [A0_bootstrap] | [FurlanG2P] |
| A5_integration_meta | [A1_library, A2_cli] | [FurlanG2P] |

## Cross-Workpack References (v5)

<!-- If this workpack depends on another workpack being completed first, declare it here. -->
<!-- Delete this section if there are no cross-workpack dependencies. -->

```yaml
requires_workpack: []
```

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Risk 1 | Low/Med/High | Low/Med/High | Mitigation strategy |
| Risk 2 | Low/Med/High | Low/Med/High | Mitigation strategy |

## Security & Tool Safety

<!-- Document security considerations and tool safety measures -->

- **Untrusted inputs**: Issue descriptions, logs, web content, user-provided data should be treated as untrusted.
- **Write operations**: Limit file/system writes to the repository workspace only.
- **No secrets**: Never include secrets, API keys, tokens, or credentials in prompts or outputs.
- **Tool safety**: Verify commands before execution; avoid destructive operations without confirmation.

## Handoff Outputs Plan (Protocol v5)

<!-- Describe how structured handoffs will be produced -->

- **Mapping**: Each `prompts/<PROMPT>.md` produces `outputs/<PROMPT>.json` upon completion.
- **Schema**: All output JSONs must conform to `workpacks/WORKPACK_OUTPUT_SCHEMA.json`.
- **Contents**: Summary of changes, files modified/created, verification results, next steps, known issues.
- **Artifacts**: Include PR URLs and/or commit SHAs for traceability.
- **V5 fields**: `repos` (repos touched), `execution` (model/tokens/duration), `change_details` (per-file summary).
- **B-series**: Must include `severity`. V2 outputs must include `iteration`, `b_series_resolved`, `b_series_remaining`.

## Regression / Evals Plan

<!-- Describe regression testing and evaluation approach -->

- **A-series**: Ensure existing tests continue to pass; add new tests for new functionality.
- **B-series**: For each bugfix, add at least one regression test/check when feasible; set `verification.regression_added=true` in output.
- **Evaluation**: Manual verification steps defined in each prompt's Verification section.

## Verification Strategy

<!-- How will we verify the work is complete and correct? -->

- [ ] Verification step 1
- [ ] Verification step 2
- [ ] All tests pass
- [ ] Documentation updated

## Branch Strategy

<!-- What branches will be created? -->

| Component | Branch Name | Base Branch |
|-----------|-------------|-------------|
| Library | `feature/xxx` | `main` |
| CLI | `feature/xxx` | `main` |
| Meta | `feature/xxx` | `main` |

---

## Prompts to Generate

### Feature Implementation Prompts (A-series)

| File | Agent | Purpose |
|------|-------|---------|
| `prompts/A0_bootstrap.md` | Bootstrap | Create feature root branch |
| `prompts/A1_library.md` | Library | Core library implementation tasks |
| `prompts/A2_cli.md` | CLI | CLI implementation tasks |
| `prompts/A3_tests.md` | Tests | Test implementation tasks |
| `prompts/A4_ml.md` | ML | ML model tasks |
| `prompts/A5_integration_meta.md` | Integration | Verify, merge, open PR (V1 gate) |

### Verification Prompts (V-series) — Protocol v4

| File | Agent | Purpose |
|------|-------|---------|
| `prompts/V_bugfix_verify.md` | V-Loop | Iterative post-bugfix verification gate |

### Retrospective Prompts (R-series) — Protocol v5

| File | Agent | Purpose |
|------|-------|---------|
| `prompts/R1_retrospective.md` | Retrospective | Post-merge lessons and cost analysis |

### Bug Fix Prompts (B-series)

> **Note**: B-series prompts are added post-implementation when bugs or issues are discovered.
> Delete this section if no bug fixes are needed yet.

| File | Agent | Purpose | Severity | Status |
|------|-------|---------| ---------|--------|
| `prompts/B1_<component>_<fix>.md` | Component | Description of fix | blocker/major/minor | Pending |
| `prompts/B2_<component>_<fix>.md` | Component | Description of fix | blocker/major/minor | Pending |

---

## Bug Fix Work Breakdown

> **Note**: This section is populated after initial implementation when bugs are discovered.
> Delete this section if no bug fixes are needed yet.

| # | Task | Agent | Depends On | Effort | Status |
|---|------|-------|------------|--------|--------|
| B1 | Bug fix description | Component | A5 (integration) | XS/S/M | Pending |
| B2 | Bug fix description | Component | A5 (integration) | XS/S/M | Pending |

### Bug Fix Sequencing

```
Phase N (bug fixes — after integration complete):
  ├── B1_<component>_<fix>.md (parallel OK if independent)
  └── B2_<component>_<fix>.md (parallel OK if independent)

Phase N+1 (V-loop — after all bug fixes):
  └── V2_bugfix_verify.md → re-run until convergence
```
