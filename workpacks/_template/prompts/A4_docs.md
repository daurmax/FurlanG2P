# Documentation Agent Prompt

> Prompt for the documentation agent to create or update project documentation.

---

## READ FIRST

Read these files before starting (in priority order):

1. `README.md` — Main project README (GitHub audience)
2. `README-pypi.md` — PyPI README (end-user audience)
3. `docs/` — Supplementary documentation
4. `AGENTS.md` — Agent guidelines
5. `./workpacks/<workpack>/00_request.md` — Original request
6. `./workpacks/<workpack>/01_plan.md` — Full plan
7. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v3)

---

## Context

This is part of workpack: `YYYY-MM-DD_<category>_<short-slug>`

**Objective**: <!-- One-line summary of documentation work -->

---

## Delivery Mode

<!-- Choose one based on 00_request.md -->

- **PR-based**: Create a PR targeting `main` and link it in `99_status.md`
- **Direct push**: Push directly to feature branch; record commits in `99_status.md`

---

## Objective

<!-- 
Describe WHAT documentation to create or update.
Specify the target audience and purpose.
-->

---

## Reference Points

<!--
Reference existing documentation for style and structure.

Example:
- **README style**: Follow the format of existing README.md sections
- **Docs structure**: Follow the format in `docs/architecture.md`
- **Code examples**: Use the same style as in existing documentation
-->

- **Style reference**: <!-- Description -->

---

## Implementation Requirements

<!--
Describe WHAT the documentation must cover.

Example:
- Document the new CLI command with usage examples
- Update README.md with new feature description
- Add architecture notes to docs/architecture.md
- Include troubleshooting section for common errors
-->

- Requirement 1
- Requirement 2
- Requirement 3

---

## Documentation Targets

| File | Audience | Updates Needed |
|------|----------|----------------|
| `README.md` | GitHub contributors | <!-- What to update --> |
| `README-pypi.md` | PyPI end users | <!-- What to update --> |
| `docs/architecture.md` | Developers | <!-- What to update --> |
| `docs/business_logic.md` | Developers | <!-- What to update --> |

---

## Scope

### In Scope

- <!-- Item 1 -->
- <!-- Item 2 -->

### Out of Scope

- <!-- Item 1 -->
- <!-- Item 2 -->

---

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

---

## Constraints

- Keep documentation concise and clear
- Include code examples where helpful
- Ensure consistency with existing documentation style
- Update both README.md and README-pypi.md if user-facing changes

---

## Verification

### Commands

```bash
# Check for broken links (if tooling available)
# Verify markdown syntax

# Test code examples in documentation
python -c "<code example from docs>"
```

### Verification Checklist

- [ ] Documentation is clear and complete
- [ ] Code examples work correctly
- [ ] No broken links
- [ ] Consistent with existing style
- [ ] Spell-checked

---

## Handoff Output (JSON) — REQUIRED

After completing the work, create/update:

**Path**: `./workpacks/<workpack>/outputs/A4_docs.json`

```json
{
  "schema_version": "1.0",
  "workpack": "<workpack>",
  "prompt": "A4_docs",
  "component": "docs",
  "delivery_mode": "<pr|direct_push>",
  "branch": {
    "base": "<base-branch>",
    "work": "<work-branch>",
    "merge_target": "<merge-target>"
  },
  "artifacts": {
    "commit_shas": ["<sha1>"]
  },
  "changes": {
    "files_modified": ["README.md", "docs/..."],
    "files_created": [],
    "contracts_changed": [],
    "breaking_change": false
  },
  "verification": {
    "commands": [
      { "cmd": "manual review", "result": "pass" }
    ]
  },
  "handoff": {
    "summary": "<one-line summary>",
    "known_issues": [],
    "next_steps": []
  }
}
```

---

## Stop Conditions

### Continue if:
- Minor formatting improvements could be made

### Escalate if:
- Implementation details are unclear
- Conflicting information in existing docs

---

## Deliverables

- [ ] Documentation updated
- [ ] Code examples verified
- [ ] `outputs/A4_docs.json` created
- [ ] `99_status.md` updated
