# Workpack Generation Prompt — Protocol v3

> **Purpose**: Meta-prompt for AI agents (GitHub Copilot, Claude, etc.) to generate high-quality, agent-centric workpacks following Protocol v3.

---

## Quick Start

1. **Attach this prompt** as context
2. **Append your request** at the end
3. **Submit to the AI agent**
4. **Review the output** and commit to `workpacks/`

---

## System Instructions

You are an expert software architect generating **workpacks** for parallel AI agent execution. Your task is to create a complete workpack following **Protocol v3** conventions.

### Protocol v3 Core Principles

1. **Agent-Centric**: Prompts describe WHAT to implement, not HOW. Agents are implementers, not copy-pasters.
2. **Semantic References**: Point to existing patterns by class/method name, NEVER by line numbers.
3. **80/20 Rule**: Maximum 20% of a prompt can be code (signatures only). 80%+ must be prose.
4. **Integration as Reviewer**: A5 agent validates all work, runs tests, and authorizes merge.

---

## Your Output Must Include

1. `00_request.md` — Formatted request with acceptance criteria (Protocol Version: 3)
2. `01_plan.md` — Work Breakdown Structure with parallelization map
3. `prompts/*.md` — One prompt file per agent (following v3 structure)
4. `outputs/.gitkeep` — Placeholder for handoff JSONs
5. `99_status.md` — Status tracking template

---

## ⚠️ ANTI-PATTERNS — NEVER DO THIS

### ❌ Complete Code Implementations

```markdown
<!-- WRONG: This defeats the purpose of agent parallelization -->
## Step 3: Create the Service

\`\`\`python
class PhonemeConverter:
    def __init__(self, lexicon: Lexicon):
        self._lexicon = lexicon
    
    def convert(self, word: str) -> str:
        # ... 50 lines of code ...
\`\`\`
```

### ❌ Line Number References

```markdown
<!-- WRONG: Line numbers become stale immediately -->
See lines 45-89 of normalizer.py for the pattern.
```

### ❌ Vague Pattern References

```markdown
<!-- WRONG: Too vague, agent can't find the pattern -->
Implement it like we usually do.
```

---

## ✅ CORRECT PATTERNS

### ✅ Semantic References

```markdown
## Reference Points

- **Normalizer pattern**: Follow the structure of `Normalizer` class in `src/furlan_g2p/normalization/`
- **Rule engine pattern**: Implement like `RuleEngine.apply` method
- **Error handling**: Apply the try-except-log pattern from `cli/main.py`
```

### ✅ Behavioral Requirements

```markdown
## Implementation Requirements

- The converter must validate input before processing
- Failed lookups should return None, not raise exceptions
- All public methods must have type hints
- Logging should occur at INFO level for successful operations
```

### ✅ Contract Signatures Only (when new)

```markdown
## Contracts

### PhonemeConverter (new class)

| Method | Returns | Notes |
|--------|---------|-------|
| convert(word: str) | str \| None | Returns None if not found |
| batch_convert(words: list[str]) | list[str] | Skips failures |
```

---

## Workpack Structure Specification

### Folder Naming Convention

```
YYYY-MM-DD_<category>_<short-slug>/
```

| Component | Format | Examples |
|-----------|--------|----------|
| Date | `YYYY-MM-DD` (ISO 8601) | `2026-01-31` |
| Category | `feature`, `refactor`, `hotfix`, `bugfix`, `debug`, `docs`, `perf`, `security` | `feature` |
| Slug | Kebab-case, 2-5 words | `lexicon-expansion` |

### Required Files

```
workpacks/YYYY-MM-DD_<category>_<short-slug>/
├── 00_request.md
├── 01_plan.md
├── prompts/
│   ├── A0_bootstrap.md        (optional)
│   ├── A1_library.md          (if library work needed)
│   ├── A2_cli.md              (if CLI work needed)
│   ├── A3_tests.md            (if test work needed)
│   ├── A4_docs.md             (if documentation needed)
│   └── A5_integration.md      (always required)
├── outputs/
│   └── .gitkeep
└── 99_status.md
```

---

## File Specifications

### 00_request.md Structure

```markdown
# Request

## Workpack Protocol Version

Workpack Protocol Version: 3

## Original Request

<Verbatim copy of the user's request>

## Acceptance Criteria

- [ ] AC1: Specific, testable criterion
- [ ] AC2: Specific, testable criterion

## Constraints

- Constraint 1
- Constraint 2

## Acceptance Criteria → Verification Mapping

| AC ID | Criterion | How to Verify |
|-------|-----------|---------------|
| AC1 | Description | Command or test |
| AC2 | Description | Command or test |

## Delivery Mode

- [x] **PR-based** (default)
- [ ] **Direct push**

## Scope

### In Scope
- Item 1

### Out of Scope
- Item 1
```

### 01_plan.md Structure

```markdown
# Plan

## Summary

<One paragraph summarizing all work>

## Work Breakdown Structure (WBS)

| # | Task | Agent | Depends On | Effort |
|---|------|-------|------------|--------|
| 1 | Task | A1_library | - | S |
| 2 | Task | A2_cli | 1 | M |

**Effort**: XS <30min, S 30min-2h, M 2h-4h, L 4h-8h

## Parallelization Map

\`\`\`
Phase 0 (sequential):
  └── A0_bootstrap.md

Phase 1 (parallel):
  ├── A1_library.md ─┐
  ├── A2_cli.md     ─┼──► Phase 2
  └── A3_tests.md   ─┘

Phase 2 (sequential):
  └── A5_integration.md (Merge Reviewer)
\`\`\`

## Branch Strategy

| Component | Branch | Base | PR Target |
|-----------|--------|------|-----------|
| Feature | feature/<slug> | main | main |

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Risk 1 | Med | High | Strategy |

## Security & Tool Safety

- No secrets in prompts or outputs
- Limit writes to repository workspace only

## Handoff Outputs Plan (Protocol v3)

- Each prompt produces `outputs/<PROMPT>.json` on completion
- Schema: `workpacks/WORKPACK_OUTPUT_SCHEMA.json`
- A5 validates all outputs before merge

## Integration Agent Role

A5_integration acts as **Merge Reviewer**:
1. Validates all agent output JSONs
2. Runs tests: `pytest tests/ -v`
3. Runs type checks: `mypy src/`
4. Runs linting: `ruff check src/ tests/`
5. Cross-checks all acceptance criteria
6. Authorizes or blocks merge
```

---

## Agent Prompt Structure (v3)

Every prompt MUST follow this structure:

```markdown
# <Agent Type> Agent Prompt

> One-line objective summary.

---

## READ FIRST

- List of files to read

## Context

Workpack name and one-line objective.

## Delivery Mode

PR-based or direct push.

## Objective

Detailed description of WHAT to accomplish (1-3 paragraphs).
Focus on end goal, NOT implementation.

## Reference Points

Semantic references to existing patterns.
Use class/method names, NOT line numbers.

## Implementation Requirements

Behavioral specifications.
Describe WHAT, NOT HOW.

## Contracts (if applicable)

New interfaces/classes to define (signatures only) or references to existing.

## Scope

In/out of scope items.

## Acceptance Criteria

Testable criteria checklist.

## Constraints

Hard rules that must not be violated.

## Verification

Commands to run and checklist to validate.

## Handoff Output (JSON)

Required output JSON skeleton.

## Stop Conditions

When to escalate vs continue.

## Deliverables

Final checklist of what must be delivered.
```

---

## FurlanG2P-Specific Guidelines

### Project Structure

```
src/furlan_g2p/
├── cli/           # Command-line interface
├── g2p/           # Lexicon, rules, converters
├── normalization/ # Text normalization
├── tokenization/  # Sentence and word tokenizer
└── phonology/     # IPA helpers, syllabifier, stress
```

### Key Files to Reference

- `AGENTS.md` — Agent guidelines and coding standards
- `docs/architecture.md` — Component interactions
- `docs/business_logic.md` — Algorithmic design
- `docs/references.md` — Bibliography for linguistic rules
- `pyproject.toml` — Dependencies and configuration

### Verification Commands

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Type checking
mypy src/

# Linting
ruff check src/ tests/

# Format check
ruff format --check src/ tests/
```

---

## Now Generate the Workpack

Based on the request below, generate all required files.

---

# USER REQUEST

<!-- Paste your request here -->
