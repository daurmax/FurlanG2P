# Documentation Agent Prompt

> Update all documentation for the hybrid G2P paradigm.

---

## READ FIRST

1. `README.md` — Current project README
2. `README-pypi.md` — Current PyPI README
3. `AGENTS.md` — Agent guidelines
4. `docs/architecture.md` — Current architecture docs
5. `docs/usage.md` — Current usage docs
6. `docs/business_logic.md` — Current algorithmic design
7. All handoff outputs (A1-A8)
8. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/00_request.md` — Full requirements

---

## Context

This is part of workpack: `2026-02-01_feature_hybrid-g2p-paradigm`

**Objective**: Comprehensively update all documentation to reflect the new hybrid G2P paradigm.

---

## Delivery Mode

- **PR-based**: Create a PR targeting `feature/hybrid-g2p-paradigm`

---

## Objective

Update documentation to cover:
1. New architecture (evaluation, lexicon, ML interface)
2. New CLI commands
3. Updated usage patterns
4. Hybrid lookup strategy explanation
5. Dialect handling documentation

---

## Reference Points

- **Existing docs**: Match style and structure
- **Handoff outputs**: Source of truth for what was implemented
- **README convention**: GitHub README for contributors, PyPI for end users

---

## Implementation Requirements

### 1. Architecture Documentation (`docs/architecture.md`)

Add sections for:
- **evaluation package**: Purpose, components, interfaces
- **lexicon package**: Schema, storage, builder, lookup
- **ml package**: Interface, null implementation, optional extra
- **Updated module map table** with new packages
- **Data flow diagram**: Hybrid lookup (lexicon → ML → rules)
- **Dialect conditioning explanation**

### 2. Business Logic (`docs/business_logic.md`)

Add sections for:
- **Hybrid lookup strategy**: Priority order, fallback logic
- **Dialect handling**: Matching, fallback, configuration
- **Evaluation metrics**: WER, PER, stress accuracy definitions
- **Lexicon schema fields**: Purpose of each field
- **IPA canonicalization**: What it does and why

### 3. Usage Documentation (`docs/usage.md`)

Add sections for:
- **Lexicon Building Workflow**:
  - Preparing source files
  - Running `furlan-g2p lexicon build`
  - Inspecting with `lexicon info`
  - Exporting formats
- **Evaluation Workflow**:
  - Preparing gold sets
  - Running `furlan-g2p evaluate`
  - Interpreting results
- **Coverage Analysis**:
  - Running `furlan-g2p coverage`
  - Understanding OOV
- **Dialect Selection**:
  - Configuring default dialect
  - Per-request dialect override
- **Optional ML**:
  - Installing `[ml]` extra
  - When ML is used

### 4. GitHub README (`README.md`)

Update:
- **Project description**: Mention hybrid architecture
- **Features list**: Add evaluation, lexicon building
- **Installation**: Add `[ml]` optional extra
- **Quick start**: Update examples with new commands
- **Development**: Mention new test commands

### 5. PyPI README (`README-pypi.md`)

Update:
- Brief mention of hybrid approach
- Installation variants
- Quick examples of key commands
- Keep concise and user-focused

### 6. Changelog (`docs/changelog.md`)

Add entry for this release:
- New features summary
- New modules
- New CLI commands
- Breaking changes (if any)

### 7. References (`docs/references.md`)

Add references for:
- WikiPron paper
- SIGMORPHON shared task
- ByT5 G2P paper
- COF documentation

---

## Scope

### In Scope

- All documentation files listed above
- Docstring review (spot-check public APIs)

### Out of Scope

- Code changes (already done)
- API reference generation

---

## Acceptance Criteria

- [ ] Architecture docs describe all new modules
- [ ] Business logic explains hybrid strategy
- [ ] Usage docs cover all new CLI commands
- [ ] README.md updated
- [ ] README-pypi.md updated
- [ ] Changelog has release entry
- [ ] Documentation is clear and consistent
- [ ] No broken internal links

---

## Constraints

- Keep README-pypi.md concise
- Maintain existing style
- Use consistent terminology

---

## Verification

```bash
# Check markdown formatting (if linter available)
# Otherwise manual review

# Verify new commands documented
grep -r "lexicon build\|evaluate\|coverage" docs/usage.md

# Check for placeholder text
grep -r "TODO\|FIXME\|XXX" docs/
```

---

## Handoff Output (JSON) — REQUIRED

**Path**: `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A9_docs.json`

---

## Stop Conditions

- **STOP** if implementation differs from handoff outputs (sync first)
- **CONTINUE** for minor wording questions

---

## Deliverables

- [ ] Updated `docs/architecture.md`
- [ ] Updated `docs/business_logic.md`
- [ ] Updated `docs/usage.md`
- [ ] Updated `README.md`
- [ ] Updated `README-pypi.md`
- [ ] Updated `docs/changelog.md`
- [ ] Updated `docs/references.md`
- [ ] Handoff output JSON
- [ ] PR created
