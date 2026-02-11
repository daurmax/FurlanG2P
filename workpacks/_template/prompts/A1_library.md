# Library Agent Prompt

> Prompt for the library agent to implement core library functionality.

---

## READ FIRST

Read these files before starting (in priority order):

1. `README.md` — Project overview and setup
2. `AGENTS.md` — Agent guidelines and conventions
3. `docs/architecture.md` — Component interactions
4. `docs/business_logic.md` — Algorithmic design
5. `./workpacks/<workpack>/00_request.md` — Original request and acceptance criteria
6. `./workpacks/<workpack>/01_plan.md` — Full work breakdown and dependencies
7. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v3)

---

## Context

This is part of workpack: `YYYY-MM-DD_<category>_<short-slug>`

**Objective**: <!-- One-line summary of what the library agent must accomplish -->

---

## Delivery Mode

<!-- Choose one based on 00_request.md -->

- **PR-based**: Create a PR targeting `main` and link it in `99_status.md`
- **Direct push**: Push directly to feature branch; record commits in `99_status.md`

---

## Objective

<!-- 
Detailed description of WHAT to accomplish (1-3 paragraphs).
Focus on the end goal and business value, not implementation details.
-->

---

## Reference Points

<!--
Semantic references to existing code patterns the agent should follow.
Use class names, method names, or file paths — NEVER line numbers.

Example:
- **Normalizer pattern**: Follow the structure of `Normalizer` class in `src/furlan_g2p/normalization/`
- **Rule engine pattern**: Implement like `RuleEngine` with the same configuration style
- **Error handling**: Apply the try-except-log pattern from CLI modules
- **Type hints**: Follow the style used throughout `src/furlan_g2p/`
-->

- **Pattern reference 1**: <!-- Description -->
- **Pattern reference 2**: <!-- Description -->

---

## Implementation Requirements

<!--
Behavioral specifications the implementation must satisfy.
Describe WHAT the code must do, not HOW it should look.
Use bullet points for clarity.

Example:
- The converter must validate input before processing
- Logging should occur at INFO level for successful operations
- Failed lookups should return None, not raise exceptions
- All public methods must have type hints and docstrings
-->

- Requirement 1
- Requirement 2
- Requirement 3

---

## Contracts

<!--
If new classes/functions are needed, define them here with signatures only.
If using existing contracts, reference them by name and location.

Example for NEW contract:
### PhonemeConverter (new class)
| Method | Returns | Notes |
|--------|---------|-------|
| convert(word: str) | str \| None | Returns None if not found |
| batch_convert(words: list[str]) | list[str] | Skips failures |

Example for EXISTING contract:
Use existing `Normalizer` from `src/furlan_g2p/normalization/`. No modifications needed.
-->

<!-- Define new contracts or reference existing ones -->

---

## Scope

### In Scope

- <!-- Item 1 -->
- <!-- Item 2 -->

### Out of Scope

- <!-- Item 1 (handled by other agent or future work) -->
- <!-- Item 2 -->

---

## Acceptance Criteria

<!-- 
Copy from 00_request.md, filtered to library-relevant criteria.
Each criterion must be specific and testable.
-->

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

---

## Constraints

<!--
Hard rules that must not be violated.
Mark critical constraints clearly.
-->

- **CRITICAL**: <!-- Constraint that must never be violated -->
- All code must have type hints
- Follow ruff/mypy configurations in `pyproject.toml`
- Consult `docs/references.md` for linguistic rules

---

## Verification

### Commands

```bash
# Install in development mode
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Run specific test module (if applicable)
pytest tests/test_<module>.py -v

# Type checking
mypy src/

# Linting
ruff check src/ tests/
```

### Verification Checklist

- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Type checking passes
- [ ] Linting passes
- [ ] No regressions in existing functionality

---

## Handoff Output (JSON) — REQUIRED

After completing the work, create/update:

**Path**: `./workpacks/<workpack>/outputs/A1_library.json`

**Rules**:
- Must conform to `workpacks/WORKPACK_OUTPUT_SCHEMA.json`
- Keep factual and concise — NO secrets/tokens/credentials
- Include PR URL in `artifacts.pr_url` if PR-based delivery
- List all modified/created files and verification commands run

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
    "merge_target": "<merge-target>"
  },
  "artifacts": {
    "pr_url": "<if PR-based>",
    "commit_shas": ["<sha1>", "<sha2>"]
  },
  "changes": {
    "files_modified": ["src/furlan_g2p/..."],
    "files_created": ["src/furlan_g2p/..."],
    "contracts_changed": [],
    "breaking_change": false
  },
  "verification": {
    "commands": [
      { "cmd": "pytest tests/ -v", "result": "pass" },
      { "cmd": "mypy src/", "result": "pass" },
      { "cmd": "ruff check src/", "result": "pass" }
    ],
    "regression_added": true
  },
  "handoff": {
    "summary": "<one-line summary of what was done>",
    "known_issues": [],
    "next_steps": ["A2_cli can proceed", "A3_tests should add coverage"]
  }
}
```

---

## Stop Conditions

### Continue if:
- Tests pass but coverage could be improved (note in known_issues)
- Minor style issues remain (note in known_issues)

### Escalate if:
- Existing tests fail and the fix is non-obvious
- Requirements conflict with existing architecture
- Linguistic rules in `docs/references.md` are ambiguous

---

## Deliverables

- [ ] Implementation complete in `src/furlan_g2p/`
- [ ] All tests pass
- [ ] Type checking passes
- [ ] `outputs/A1_library.json` created
- [ ] `99_status.md` updated with A1 status
