# Plan

> Work Breakdown Structure, sequencing, and parallelization map for this workpack.

## Summary

<!-- One-paragraph summary of what will be done -->

## Work Breakdown Structure (WBS)

<!-- Break down the work into discrete tasks -->

| # | Task | Agent | Depends On | Estimated Effort |
|---|------|-------|------------|------------------|
| 1 | Task description | Library / CLI / Tests / Docs / Integration | - | S / M / L |
| 2 | Task description | Agent | Task 1 | S / M / L |
| 3 | Task description | Agent | - | S / M / L |

**Effort**: XS <30min, S 30min-2h, M 2h-4h, L 4h-8h

## Parallelization Map

<!-- Visual or textual representation of what can run in parallel -->

```
Phase 1 (parallel):
  ├── A1_library.md  ─┐
  ├── A2_cli.md      ─┼──► Phase 2
  └── A4_docs.md     ─┘

Phase 2 (sequential):
  └── A5_integration.md
```

### Parallel Groups

| Group | Agents | Notes |
|-------|--------|-------|
| Group A | Library, CLI | Can run in parallel if no shared interfaces |
| Group B | Docs | Can run with Group A |

### Sequential Dependencies

| Must Complete First | Before Starting |
|---------------------|-----------------|
| A0_bootstrap | All others |
| Group A + B | A5_integration |

## Sequencing Notes

<!-- Any special ordering requirements -->

1. Step 1 must complete before Step 2 because...
2. Steps 3 and 4 can run in parallel because...

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

## Handoff Outputs Plan (Protocol v3)

<!-- Describe how structured handoffs will be produced -->

- **Mapping**: Each `prompts/<PROMPT>.md` produces `outputs/<PROMPT>.json` upon completion.
- **Schema**: All output JSONs must conform to `workpacks/WORKPACK_OUTPUT_SCHEMA.json`.
- **Contents**: Summary of changes, files modified/created, verification results, next steps, known issues.
- **Artifacts**: Include PR URLs and/or commit SHAs for traceability.

## Regression / Evals Plan

<!-- Describe regression testing and evaluation approach -->

- **A-series**: Ensure existing tests continue to pass; add new tests for new functionality.
- **B-series**: For each bugfix, add at least one regression test when feasible; set `verification.regression_added=true` in output.
- **Evaluation**: Manual verification steps defined in each prompt's Verification section.

## Verification Strategy

<!-- How will we verify the work is complete and correct? -->

- [ ] `pytest tests/ -v` passes
- [ ] `mypy src/` passes
- [ ] `ruff check src/ tests/` passes
- [ ] Documentation updated
- [ ] Manual verification of feature

## Branch Strategy

<!-- What branches will be created? -->

| Component | Branch Name | Base Branch | PR Target |
|-----------|-------------|-------------|-----------|
| Feature | `feature/<slug>` | `main` | `main` |

---

## Prompts to Generate

### Feature Implementation Prompts (A-series)

| File | Agent | Purpose |
|------|-------|---------|
| `prompts/A0_bootstrap.md` | Bootstrap | Create feature branch |
| `prompts/A1_library.md` | Library | Core library implementation |
| `prompts/A2_cli.md` | CLI | CLI implementation |
| `prompts/A3_tests.md` | Tests | Test implementation |
| `prompts/A4_docs.md` | Docs | Documentation |
| `prompts/A5_integration.md` | Integration | Merge and validate |

### Bug Fix Prompts (B-series)

> **Note**: B-series prompts are added post-implementation when bugs or issues are discovered.
> Delete this section if no bug fixes are needed yet.

| File | Agent | Purpose | Status |
|------|-------|---------|--------|
| `prompts/B1_<component>_<fix>.md` | Component | Description of fix | Pending |
| `prompts/B2_<component>_<fix>.md` | Component | Description of fix | Pending |

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
```
