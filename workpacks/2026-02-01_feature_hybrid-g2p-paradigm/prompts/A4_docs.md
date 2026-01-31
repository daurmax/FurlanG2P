# Documentation Agent Prompt

> Update documentation for the hybrid G2P paradigm: architecture, usage, and READMEs.

---

## READ FIRST

Read these files before starting (in priority order):

1. `README.md` — Current project README (GitHub contributors)
2. `README-pypi.md` — Current PyPI README (end users)
3. `AGENTS.md` — Agent guidelines
4. `docs/architecture.md` — Current architecture documentation
5. `docs/usage.md` — Current usage documentation
6. `docs/business_logic.md` — Algorithmic design
7. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/00_request.md` — Full requirements
8. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/01_plan.md` — Work breakdown
9. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A1_library.json` — Library handoff
10. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A2_cli.json` — CLI handoff
11. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v3)

---

## Context

This is part of workpack: `2026-02-01_feature_hybrid-g2p-paradigm`

**Objective**: Update all project documentation to reflect the new hybrid G2P paradigm including architecture changes, new CLI commands, evaluation workflow, and lexicon building.

---

## Delivery Mode

- **PR-based**: Create a PR targeting `feature/hybrid-g2p-paradigm` and link it in `99_status.md`

---

## Objective

Comprehensive documentation update to cover the paradigm shift from pure rule-based G2P to the hybrid approach. This includes:

1. **Architecture documentation** — New modules, interfaces, and data flow
2. **Usage documentation** — New CLI commands and workflows
3. **README updates** — Both GitHub (README.md) and PyPI (README-pypi.md)
4. **Business logic updates** — Hybrid lookup strategy, dialect conditioning

Documentation must help both contributors (understanding the architecture) and end users (using the new features).

---

## Reference Points

- **Documentation style**: Follow existing Markdown conventions in `docs/`
- **CLI documentation**: Match the style used in `docs/usage.md`
- **Architecture diagrams**: Use ASCII art or Mermaid if already used in the project
- **README sections**: Maintain existing section structure, add new sections as needed

---

## Implementation Requirements

### 1. Architecture Documentation (`docs/architecture.md`)

Update to include:

- **New modules section**: Describe `evaluation/`, `lexicon/`, `ml/` packages
- **Module map table**: Add new modules with responsibility and maturity
- **Data flow diagram**: Show hybrid lookup: lexicon → exception model → rules
- **Interface additions**: Document new interfaces (ILexiconBuilder, IEvaluator, IExceptionModel)
- **Dialect conditioning**: Explain the prefix/conditioning approach

### 2. Business Logic Documentation (`docs/business_logic.md`)

Update to include:

- **Hybrid lookup strategy**: Priority order (lexicon → ML → rules)
- **Dialect handling**: Dialect matching and fallback logic
- **Evaluation metrics**: Definition of WER, PER, stress accuracy
- **Lexicon schema**: Field definitions and purpose
- **WikiPron integration**: How external data is normalized

### 3. Usage Documentation (`docs/usage.md`)

Add new sections:

- **Lexicon Building**: Commands and workflow for building lexicons
- **Evaluation**: How to evaluate against gold sets
- **Coverage Analysis**: How to measure OOV rates
- **Dialect Selection**: How to use dialect options
- **Optional ML**: How to install and use the `[ml]` extra

### 4. GitHub README (`README.md`)

Update to include:

- Mention hybrid architecture in project description
- Add section about lexicon building workflow
- Add section about evaluation capabilities
- Update installation section for `[ml]` optional extra
- Update CLI examples with new commands

### 5. PyPI README (`README-pypi.md`)

Update to include:

- Brief mention of hybrid G2P approach
- Installation variants (`pip install furlan-g2p[ml]`)
- Quick examples of new commands
- Keep focused on end-user needs (concise)

### 6. Changelog (`docs/changelog.md`)

Add entry for this release:

- Summary of hybrid paradigm addition
- New modules: evaluation, lexicon, ml
- New CLI commands
- Breaking changes (if any)

---

## Scope

### In Scope

- Architecture documentation updates
- Business logic documentation updates
- Usage documentation updates
- README.md updates
- README-pypi.md updates
- Changelog entry
- Docstring review (ensure public APIs are documented)

### Out of Scope

- Library implementation (done in A1_library)
- CLI implementation (done in A2_cli)
- Test implementation (done in A3_tests)
- API reference generation (if using sphinx/autodoc)

---

## Acceptance Criteria

- [ ] `docs/architecture.md` describes all new modules
- [ ] `docs/business_logic.md` explains hybrid lookup strategy
- [ ] `docs/usage.md` documents all new CLI commands
- [ ] `README.md` reflects new capabilities
- [ ] `README-pypi.md` includes new installation/usage info
- [ ] `docs/changelog.md` has entry for this release
- [ ] Documentation is clear, consistent, and follows existing style
- [ ] No broken links or references

---

## Constraints

- **CRITICAL**: Keep README-pypi.md concise (end-user focused)
- Maintain existing documentation structure and style
- Use consistent terminology across all documents
- Include practical examples where helpful
- No internal implementation details in user-facing docs

---

## Verification

### Commands

```bash
# Check for broken links (if link checker available)
# Otherwise manual review

# Verify markdown formatting
# (use editor preview or markdown linter)

# Check all new commands are documented
grep -r "lexicon\|evaluate\|coverage" docs/usage.md
```

### Verification Checklist

- [ ] All documentation files updated
- [ ] New features documented with examples
- [ ] Terminology consistent across documents
- [ ] No spelling/grammar errors (spot check)
- [ ] README sections are balanced (not too long)

---

## Handoff Output (JSON) — REQUIRED

After completing the work, create/update:

**Path**: `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A4_docs.json`

```json
{
  "schema_version": "1.0",
  "workpack": "2026-02-01_feature_hybrid-g2p-paradigm",
  "prompt": "A4_docs",
  "component": "docs",
  "delivery_mode": "pr",
  "branch": {
    "base": "feature/hybrid-g2p-paradigm",
    "work": "feature/hybrid-g2p-paradigm-docs",
    "merge_target": "feature/hybrid-g2p-paradigm"
  },
  "summary": "Updated documentation for hybrid G2P paradigm",
  "handoff": {
    "files_modified": [
      "README.md",
      "README-pypi.md",
      "docs/architecture.md",
      "docs/business_logic.md",
      "docs/usage.md",
      "docs/changelog.md"
    ],
    "files_created": [],
    "verification": {
      "commands_run": ["manual review"],
      "all_passed": true
    },
    "next_steps": [
      "A5_integration can run final validation"
    ],
    "known_issues": []
  },
  "artifacts": {
    "pr_url": "<PR_URL>"
  }
}
```

---

## Stop Conditions

- **STOP** if major architectural changes are discovered that aren't in A1_library (sync with team)
- **CONTINUE** for minor wording questions (use best judgment)
- **CONTINUE** for formatting questions (follow existing style)

---

## Deliverables

- [ ] Updated `docs/architecture.md`
- [ ] Updated `docs/business_logic.md`
- [ ] Updated `docs/usage.md`
- [ ] Updated `README.md`
- [ ] Updated `README-pypi.md`
- [ ] Updated `docs/changelog.md`
- [ ] Handoff output JSON created
- [ ] PR created and linked in `99_status.md`
