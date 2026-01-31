# CLI Agent Prompt

> Prompt for the CLI agent to implement command-line interface functionality.

---

## READ FIRST

Read these files before starting (in priority order):

1. `README.md` — Project overview and CLI usage
2. `AGENTS.md` — Agent guidelines and conventions
3. `src/furlan_g2p/cli/` — Existing CLI structure
4. `./workpacks/<workpack>/00_request.md` — Original request and acceptance criteria
5. `./workpacks/<workpack>/01_plan.md` — Full work breakdown and dependencies
6. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v3)

---

## Context

This is part of workpack: `YYYY-MM-DD_<category>_<short-slug>`

**Objective**: <!-- One-line summary of what the CLI agent must accomplish -->

---

## Delivery Mode

<!-- Choose one based on 00_request.md -->

- **PR-based**: Create a PR targeting `main` and link it in `99_status.md`
- **Direct push**: Push directly to feature branch; record commits in `99_status.md`

---

## Objective

<!-- 
Detailed description of WHAT to accomplish (1-3 paragraphs).
Focus on the end goal and user experience.
-->

---

## Reference Points

<!--
Semantic references to existing CLI patterns.

Example:
- **Command pattern**: Follow the structure of `ipa_command` in `src/furlan_g2p/cli/`
- **Option handling**: Use Click decorators like existing commands
- **Output formatting**: Follow the console output style from `ipa` command
-->

- **Pattern reference 1**: <!-- Description -->
- **Pattern reference 2**: <!-- Description -->

---

## Implementation Requirements

<!--
Behavioral specifications for the CLI.

Example:
- The command must accept file input via --input option
- Output should go to stdout by default, with --output option for file
- Error messages should go to stderr with appropriate exit codes
- Help text must be clear and include examples
-->

- Requirement 1
- Requirement 2
- Requirement 3

---

## Contracts

<!--
CLI command signatures (Click decorators).

Example:
### new-command (new subcommand)
| Option | Type | Default | Notes |
|--------|------|---------|-------|
| --input | Path | - | Input file path |
| --output | Path | stdout | Output destination |
| --format | Choice | text | Output format: text, json |
-->

<!-- Define new commands or reference existing ones -->

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

- **CRITICAL**: <!-- Critical constraint -->
- CLI must work on Windows and Unix
- Use Click for all CLI handling
- Follow existing CLI patterns in the project

---

## Verification

### Commands

```bash
# Install in development mode
pip install -e ".[dev]"

# Test CLI help
furlang2p --help
furlang2p <new-command> --help

# Test basic functionality
furlang2p <new-command> <test-input>

# Run CLI-specific tests
pytest tests/test_cli.py -v

# Type checking
mypy src/furlan_g2p/cli/

# Linting
ruff check src/furlan_g2p/cli/
```

### Verification Checklist

- [ ] CLI help is clear and complete
- [ ] Command works as expected
- [ ] Error handling is appropriate
- [ ] Tests pass
- [ ] Type checking passes

---

## Handoff Output (JSON) — REQUIRED

After completing the work, create/update:

**Path**: `./workpacks/<workpack>/outputs/A2_cli.json`

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
    "merge_target": "<merge-target>"
  },
  "artifacts": {
    "pr_url": "<if PR-based>",
    "commit_shas": ["<sha1>"]
  },
  "changes": {
    "files_modified": ["src/furlan_g2p/cli/..."],
    "files_created": [],
    "contracts_changed": [],
    "breaking_change": false
  },
  "verification": {
    "commands": [
      { "cmd": "furlang2p --help", "result": "pass" },
      { "cmd": "pytest tests/test_cli.py -v", "result": "pass" },
      { "cmd": "mypy src/furlan_g2p/cli/", "result": "pass" }
    ],
    "regression_added": true
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
- Minor help text improvements could be made

### Escalate if:
- Library API (A1) is not ready or has issues
- Click version conflicts

---

## Deliverables

- [ ] CLI command implemented
- [ ] Help text complete
- [ ] Tests pass
- [ ] `outputs/A2_cli.json` created
- [ ] `99_status.md` updated
