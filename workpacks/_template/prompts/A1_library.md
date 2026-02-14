# Library Agent Prompt

> Core library agent for FurlanG2P. Handles changes to the G2P engine, lexicon, normalization, tokenization, phonology, and evaluation modules.

> **v5**: This template includes YAML front-matter. Fill in `depends_on` and `repos` before use.

---

## YAML Front-Matter (v5)

```yaml
---
depends_on: [A0_bootstrap]   # prompt stems this depends on
repos: [FurlanG2P]           # repos this prompt touches
---
```

---

## READ FIRST

1. `./README.md` — Project overview and layout
2. `./AGENTS.md` — Agent guidelines
3. `./docs/architecture.md` — Architecture documentation
4. `./docs/business_logic.md` — Business logic rules and references
5. `./workpacks/instances/<workpack>/00_request.md` — Original request
6. `./workpacks/instances/<workpack>/01_plan.md` — Full plan
7. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v5)

---

## Context

This is part of workpack: `YYYY-MM-DD_<category>_<short-slug>`

**Objective**: <!-- One-line summary of the library work to be done -->

---

## Delivery Mode

- **PR-based**: Open a PR targeting `main` and link it in `99_status.md`.
- **Direct push**: Push directly to `main`; record commits in `99_status.md`.

---

## Primary Modules

The library agent works across the following source modules:

| Module | Path | Purpose |
|--------|------|---------|
| G2P engine | `src/furlan_g2p/g2p/` | Phonemizer, rule engine, legacy adapter |
| Lexicon | `src/furlan_g2p/lexicon/` | Schema, storage, builder, dialect lookup |
| Normalization | `src/furlan_g2p/normalization/` | Text normalization, unit/abbreviation expansion |
| Tokenization | `src/furlan_g2p/tokenization/` | Sentence/word splitting, abbreviation handling |
| Phonology | `src/furlan_g2p/phonology/` | IPA canonicalization, syllabifier, stress |
| Evaluation | `src/furlan_g2p/evaluation/` | Metrics (WER, PER, stress accuracy) |
| Services | `src/furlan_g2p/services/` | Pipeline orchestration, file I/O |

---

## Objective

<!--
Describe WHAT library changes must be accomplished.
Focus on end goals and behavioral requirements.
-->

---

## Reference Points

<!--
Point to existing patterns, classes, or methods by name — NEVER by line numbers.

Example:
- **G2P pattern**: Follow the structure of `Phonemizer.phonemize` method in `src/furlan_g2p/g2p/`
- **Lexicon access**: Implement like `LexiconLookup.lookup_word` method
- **Rule engine**: Follow existing `RuleEngine.apply_rules` pattern
- **References**: Consult `docs/references.md` for linguistic accuracy
-->

- **Reference 1**: <!-- Description -->

---

## Implementation Requirements

<!--
Describe WHAT the library must do, not HOW to code it.

Example:
- The normalizer must handle abbreviation expansion for common Friulian units
- Lexicon lookup must support dialect fallback (central → universal)
- G2P rules must validate output against the phoneme inventory
- All public APIs must have type hints and docstrings
-->

- Requirement 1
- Requirement 2

---

## Contracts

<!--
New interfaces/types — signatures only (no implementations).
For existing interfaces, reference them by name.
-->

---

## Subagent Strategy

<!--
Identify subtasks that can be delegated to subagents for parallel execution.

Example:
- **Subagent 1**: Implement lexicon changes while main agent works on rules
- **Subagent 2**: Update evaluation metrics while main agent works on normalization
-->

---

## Task Tracking

If your tool/model supports a structured todo list (e.g., `manage_todo_list`), use it to:

1. Break library work into discrete steps (lexicon changes, rule updates, etc.)
2. Mark each step in-progress before starting and completed immediately after
3. Helps avoid losing track in multi-module changes

---

## Scope

### In Scope

- Core library module changes listed above
- Unit tests for changed modules

### Out of Scope

- CLI changes (handled by A2_cli agent)
- ML model changes (handled by A4_ml agent)
- Documentation updates (handled by A6_docs agent)

---

## Acceptance Criteria

- [ ] <!-- Specific, testable criterion from 00_request.md -->
- [ ] All existing tests pass
- [ ] Type hints present on all new/modified public APIs
- [ ] Docstrings with examples on new public methods

---

## Constraints

- Runtime deps must remain minimal; optional deps go behind extras
- Follow ruff/mypy configs in `pyproject.toml`
- Consult `docs/references.md` when changing linguistic logic
- Public interfaces must remain backward-compatible unless explicitly planned

---

## Verification

### Commands

```bash
# Install
pip install -e ".[dev]"

# Test
python -m pytest tests/ -v

# Type check
mypy src/ tests/

# Lint
ruff check src/ tests/
```

### Verification Checklist

- [ ] All tests pass
- [ ] No type errors
- [ ] No lint errors
- [ ] New tests cover changed code

---

## Handoff Output (JSON) — REQUIRED

After completing the work, create/update:

**Path**: `./workpacks/instances/<workpack>/outputs/A1_library.json`

<!-- lint-ignore-code-block -->
```json
{
  "schema_version": "1.0",
  "workpack": "<workpack>",
  "prompt": "A1_library",
  "component": "library",
  "delivery_mode": "<pr|direct_push>",
  "branch": {
    "base": "<base-branch>",
    "work": "<work-branch>",
    "merge_target": "main"
  },
  "repos": ["FurlanG2P"],
  "artifacts": {
    "pr_url": "",
    "commit_shas": []
  },
  "changes": {
    "files_modified": [],
    "files_created": [],
    "contracts_changed": [],
    "breaking_change": false
  },
  "change_details": [],
  "verification": {
    "commands": [
      {"cmd": "pip install -e \".[dev]\"", "result": "pass"},
      {"cmd": "python -m pytest tests/ -v", "result": "pass"},
      {"cmd": "mypy src/ tests/", "result": "pass"},
      {"cmd": "ruff check src/ tests/", "result": "pass"}
    ],
    "regression_added": false,
    "regression_notes": ""
  },
  "execution": {
    "model": "",
    "tokens_in": 0,
    "tokens_out": 0,
    "duration_ms": 0
  },
  "handoff": {
    "summary": "",
    "next_steps": [],
    "known_issues": []
  },
  "notes": ""
}
```

---

## Stop Conditions

Stop and escalate if:

- Change requires breaking a public API
- Linguistic question arises that is not covered by `docs/references.md`
- Test failures in unrelated modules suggest a deeper issue

---

## Deliverables

- [ ] Library changes implemented
- [ ] Tests added/updated
- [ ] Verification commands pass
- [ ] Output JSON created
