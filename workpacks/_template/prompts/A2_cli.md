# CLI Agent Prompt

> CLI agent for FurlanG2P. Handles changes to the `furlang2p` command-line interface, subcommands, batch processing, and CLI output formatting.

> **v5**: This template includes YAML front-matter. Fill in `depends_on` and `repos` before use.

---

## YAML Front-Matter (v5)

```yaml
---
depends_on: [A1_library]    # typically depends on library changes being ready
repos: [FurlanG2P]          # repos this prompt touches
---
```

---

## READ FIRST

1. `./README.md` — Project overview, CLI usage section
2. `./AGENTS.md` — Agent guidelines
3. `./README-pypi.md` — PyPI user-facing documentation
4. `./workpacks/instances/<workpack>/00_request.md` — Original request
5. `./workpacks/instances/<workpack>/01_plan.md` — Full plan
6. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v5)

---

## Context

This is part of workpack: `YYYY-MM-DD_<category>_<short-slug>`

**Objective**: <!-- One-line summary of the CLI work to be done -->

---

## Delivery Mode

- **PR-based**: Open a PR targeting `main` and link it in `99_status.md`.
- **Direct push**: Push directly to `main`; record commits in `99_status.md`.

---

## Primary Modules

| Module | Path | Purpose |
|--------|------|---------|
| CLI commands | `src/furlan_g2p/cli/` | Click/argparse command definitions |
| Scripts | `scripts/` | Standalone helper scripts |

---

## Objective

<!--
Describe WHAT CLI changes must be accomplished.
Focus on end goals: new subcommands, changed output formats, batch features.
-->

---

## Reference Points

<!--
Point to existing patterns by name — NEVER by line numbers.

Example:
- **CLI pattern**: Follow the structure of the existing `phonemize` subcommand
- **Batch processing**: See `csv_batch_process` in `src/furlan_g2p/cli/`
- **Output format**: Follow the JSON output pattern from `evaluate` subcommand
-->

- **Reference 1**: <!-- Description -->

---

## Implementation Requirements

<!--
Describe WHAT the CLI must do, not HOW to code it.

Example:
- Add a new `coverage` subcommand that accepts a word list file
- Output must support both JSON and TSV formats via --format flag
- Progress bar should be shown for batch operations
-->

- Requirement 1
- Requirement 2

---

## Subagent Strategy

<!--
Identify parallelizable CLI subtasks.
-->

---

## Task Tracking

If your tool/model supports a structured todo list (e.g., `manage_todo_list`), use it to track each subcommand or CLI change as a discrete step.

---

## Scope

### In Scope

- CLI command changes in `src/furlan_g2p/cli/`
- CLI-specific tests

### Out of Scope

- Core library logic (handled by A1_library)
- ML model changes (handled by A4_ml)
- Documentation beyond CLI help text (handled by A6_docs)

---

## Acceptance Criteria

- [ ] <!-- Specific, testable criterion from 00_request.md -->
- [ ] `furlang2p --help` shows new/updated commands
- [ ] All existing CLI tests pass

---

## Constraints

- Follow existing CLI framework conventions (Click/argparse as used)
- `--help` text must be clear and complete
- Follow ruff/mypy configs in `pyproject.toml`

---

## Verification

### Commands

```bash
pip install -e ".[dev]"
python -m pytest tests/ -v -k cli
mypy src/furlan_g2p/cli/
ruff check src/furlan_g2p/cli/
furlang2p --help
```

---

## Handoff Output (JSON) — REQUIRED

**Path**: `./workpacks/instances/<workpack>/outputs/A2_cli.json`

<!-- lint-ignore-code-block -->
```json
{
  "schema_version": "1.0",
  "workpack": "<workpack>",
  "prompt": "A2_cli",
  "component": "cli",
  "delivery_mode": "<pr|direct_push>",
  "branch": {
    "base": "<base-branch>",
    "work": "<work-branch>",
    "merge_target": "main"
  },
  "repos": ["FurlanG2P"],
  "artifacts": { "pr_url": "", "commit_shas": [] },
  "changes": { "files_modified": [], "files_created": [], "contracts_changed": [], "breaking_change": false },
  "change_details": [],
  "verification": {
    "commands": [
      {"cmd": "python -m pytest tests/ -v -k cli", "result": "pass"},
      {"cmd": "furlang2p --help", "result": "pass"}
    ],
    "regression_added": false,
    "regression_notes": ""
  },
  "execution": { "model": "", "tokens_in": 0, "tokens_out": 0, "duration_ms": 0 },
  "handoff": { "summary": "", "next_steps": [], "known_issues": [] },
  "notes": ""
}
```

---

## Stop Conditions

Stop and escalate if:

- Required library API not yet available (wait for A1_library)
- CLI framework change needed (architectural decision required)

---

## Deliverables

- [ ] CLI changes implemented
- [ ] CLI tests added/updated
- [ ] `furlang2p --help` accurate
- [ ] Output JSON created
