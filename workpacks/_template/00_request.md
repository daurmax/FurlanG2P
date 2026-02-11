# Request

> Fill in this template with the original request details.

## Workpack Protocol Version

Workpack Protocol Version: 3

## Original Request

<!-- Paste the original request verbatim here -->

```
<PASTE ORIGINAL REQUEST HERE>
```

## Acceptance Criteria

<!-- List specific, testable criteria that define "done" -->

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Constraints

<!-- List any hard constraints, rules, or limitations -->

- Constraint 1
- Constraint 2

## Acceptance Criteria → Verification Mapping

<!-- Map each acceptance criterion to how it will be verified -->

| AC ID | Acceptance Criterion | How to Verify (command/test) |
|-------|----------------------|------------------------------|
| AC1 | Feature X works correctly | `pytest tests/test_x.py -v` |
| AC2 | No type errors | `mypy src/` |
| AC3 | Documentation updated | Manual review of docs/ folder |

## Delivery Mode

<!-- Choose one delivery mode. PR-based is the default and recommended. -->

- [x] **PR-based** (default, recommended) — Create a PR for review before merging to `main`
- [ ] **Direct push** — Push directly to `main` (only if explicitly requested by user)

> **Note**: Direct push bypasses review. Use with extra caution and record all commits in `99_status.md`.

## Scope

### In Scope

- Item 1
- Item 2

### Out of Scope

- Item 1
- Item 2

## Context

<!-- Any additional context: links, screenshots, related issues -->

- Related issue: (if any)
- Related PR: (if any)
- Dependencies: (if any)
