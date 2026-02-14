# Documentation Agent Prompt

> Documentation agent for FurlanG2P. Handles updates to `docs/`, `README.md`, `README-pypi.md`, and inline docstrings.

> **v5**: This template includes YAML front-matter. Fill in `depends_on` and `repos` before use.

---

## YAML Front-Matter (v5)

```yaml
---
depends_on: [A1_library]    # docs depend on library changes being ready
repos: [FurlanG2P]          # repos this prompt touches
---
```

---

## READ FIRST

1. `./README.md` — GitHub-facing documentation
2. `./README-pypi.md` — PyPI user-facing documentation
3. `./AGENTS.md` — Agent guidelines (docs section)
4. `./docs/` — Architecture, business logic, usage, references
5. `./workpacks/instances/<workpack>/00_request.md` — Original request
6. `./workpacks/instances/<workpack>/01_plan.md` — Full plan
7. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v5)

---

## Context

This is part of workpack: `YYYY-MM-DD_<category>_<short-slug>`

**Objective**: <!-- One-line summary of docs work -->

---

## Delivery Mode

- **PR-based**: Open a PR targeting `main` and link it in `99_status.md`.
- **Direct push**: Push directly to `main`; record commits in `99_status.md`.

---

## Primary Files

| File | Audience | Purpose |
|------|----------|---------|
| `README.md` | GitHub contributors | Setup, layout, development guide |
| `README-pypi.md` | PyPI end users | Installation and usage examples |
| `docs/architecture.md` | Contributors | Module structure, data flow |
| `docs/business_logic.md` | Contributors | Linguistic rules, phonology |
| `docs/usage.md` | Users | CLI and API usage examples |
| `docs/references.md` | Contributors | Bibliography, linguistic sources |

---

## Objective

<!--
Describe WHAT documentation needs to change.
-->

---

## Implementation Requirements

<!--
Example:
- Update README.md to reflect new CLI subcommand
- Update docs/architecture.md with new module description
- Ensure README-pypi.md examples still work
-->

- Requirement 1
- Requirement 2

---

## Constraints

- `README.md` targets contributors; `README-pypi.md` targets end users — keep them distinct
- Follow AGENTS.md rules: update both READMEs when user-facing behavior changes
- Keep examples runnable and tested

---

## Verification

```bash
# Verify README examples are accurate
python -c "# run key examples from README"

# Check for broken links (if applicable)
# python -m sphinx docs/ docs/_build/
```

---

## Handoff Output (JSON) — REQUIRED

**Path**: `./workpacks/instances/<workpack>/outputs/A6_docs.json`

<!-- lint-ignore-code-block -->
```json
{
  "schema_version": "1.0",
  "workpack": "<workpack>",
  "prompt": "A6_docs",
  "component": "docs",
  "delivery_mode": "<pr|direct_push>",
  "branch": { "base": "<base-branch>", "work": "<work-branch>", "merge_target": "main" },
  "repos": ["FurlanG2P"],
  "artifacts": { "pr_url": "", "commit_shas": [] },
  "changes": { "files_modified": [], "files_created": [], "contracts_changed": [], "breaking_change": false },
  "change_details": [],
  "verification": { "commands": [], "regression_added": false, "regression_notes": "" },
  "execution": { "model": "", "tokens_in": 0, "tokens_out": 0, "duration_ms": 0 },
  "handoff": { "summary": "", "next_steps": [], "known_issues": [] },
  "notes": ""
}
```

---

## Deliverables

- [ ] Documentation updated
- [ ] Examples verified
- [ ] Output JSON created
