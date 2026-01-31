# CLI Agent Prompt

> Implement CLI commands for lexicon building, evaluation, and coverage analysis.

---

## READ FIRST

Read these files before starting (in priority order):

1. `README.md` — Project overview
2. `AGENTS.md` — Agent guidelines
3. `src/furlan_g2p/cli/` — Existing CLI implementation
4. `docs/usage.md` — Current CLI usage documentation
5. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/00_request.md` — Full requirements
6. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/01_plan.md` — Work breakdown
7. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A1_library.json` — Library handoff
8. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v3)

---

## Context

This is part of workpack: `2026-02-01_feature_hybrid-g2p-paradigm`

**Objective**: Add CLI subcommands for lexicon operations (build, info, export), evaluation (against gold sets), and coverage analysis (measuring OOV rates).

---

## Delivery Mode

- **PR-based**: Create a PR targeting `feature/hybrid-g2p-paradigm` and link it in `99_status.md`

---

## Objective

Extend the FurlanG2P CLI with commands for the new hybrid G2P workflow:

1. **Lexicon commands** — Build lexicons from WikiPron/TSV sources, inspect lexicon info, export to different formats
2. **Evaluation commands** — Compute WER/PER/stress accuracy against gold sets
3. **Coverage commands** — Analyze OOV rates against a wordlist

These commands expose the new library functionality implemented in A1_library to end users and enable scripted workflows for lexicon development and quality assurance.

---

## Reference Points

- **CLI pattern**: Follow the existing `click` command structure in `src/furlan_g2p/cli/`
- **Subcommand pattern**: Use `@cli.group()` for command groupings like existing commands
- **Error handling**: Follow the try-except-exit pattern used in existing CLI commands
- **Output formatting**: Use the same output conventions (JSON for programmatic, readable text for interactive)
- **Service layer**: Call service functions rather than implementing logic in CLI layer

---

## Implementation Requirements

### 1. Lexicon Command Group (`furlan-g2p lexicon`)

Create a `lexicon` command group with subcommands:

**`furlan-g2p lexicon build`**
- Accept one or more input files (WikiPron TSV format)
- Options: `--output` (path), `--format` (tsv/jsonl), `--dialect` (default dialect tag)
- Validate inputs and report counts/warnings
- Use LexiconBuilder from the library

**`furlan-g2p lexicon info`**
- Accept lexicon file path
- Display statistics: entry count, dialect breakdown, source breakdown, coverage of phoneme inventory

**`furlan-g2p lexicon export`**
- Convert between lexicon formats (TSV ↔ JSONL)
- Options: `--input`, `--output`, `--format`

### 2. Evaluate Command (`furlan-g2p evaluate`)

Create an `evaluate` command:

- Accept gold set file (TSV: word, expected_ipa)
- Run G2P pipeline on words
- Compute and display WER, PER, stress accuracy
- Options: `--dialect`, `--output` (JSON results), `--verbose` (per-word errors)
- Use evaluation module from the library

### 3. Coverage Command (`furlan-g2p coverage`)

Create a `coverage` command:

- Accept wordlist file (one word per line)
- Check each word against lexicon + rules
- Report: lexicon hits, rule hits, OOV count, coverage percentage
- Options: `--lexicon` (custom lexicon), `--dialect`, `--output` (JSON)
- Useful for identifying words needing annotation

### General Requirements

- All commands must have `--help` with clear descriptions
- Support JSON output for programmatic use (via `--json` or `--output` options)
- Progress indicators for batch operations
- Consistent error messages following existing patterns

---

## Contracts

Use interfaces and classes from A1_library:

- `LexiconBuilder` from `furlan_g2p.lexicon.builder`
- `LexiconEntry` from `furlan_g2p.lexicon.schema`
- `Evaluator` (or functions) from `furlan_g2p.evaluation.metrics`
- `Lexicon` from `furlan_g2p.lexicon` (extended version)

---

## Scope

### In Scope

- `furlan-g2p lexicon build` command
- `furlan-g2p lexicon info` command
- `furlan-g2p lexicon export` command
- `furlan-g2p evaluate` command
- `furlan-g2p coverage` command
- Help text and usage examples

### Out of Scope

- Library implementation (done in A1_library)
- Test implementation (done in A3_tests)
- Documentation updates (done in A4_docs)
- ML model commands (future work)

---

## Acceptance Criteria

- [ ] `furlan-g2p lexicon build` creates lexicon from WikiPron files
- [ ] `furlan-g2p lexicon info` displays lexicon statistics
- [ ] `furlan-g2p lexicon export` converts between formats
- [ ] `furlan-g2p evaluate` computes WER/PER/stress against gold set
- [ ] `furlan-g2p coverage` reports OOV rates against wordlist
- [ ] All commands have `--help` with clear descriptions
- [ ] JSON output option works for all commands
- [ ] Error handling is consistent with existing commands

---

## Constraints

- **CRITICAL**: CLI layer must be thin — delegate to service/library functions
- Follow existing `click` patterns and conventions
- No new dependencies beyond what's in `[dev]`
- Consistent exit codes: 0 for success, 1 for errors

---

## Verification

### Commands

```bash
# Install in development mode
pip install -e ".[dev]"

# Verify help texts
furlan-g2p --help
furlan-g2p lexicon --help
furlan-g2p lexicon build --help
furlan-g2p evaluate --help
furlan-g2p coverage --help

# Run linting
ruff check src/furlan_g2p/cli/

# Type checking
mypy src/furlan_g2p/cli/
```

### Verification Checklist

- [ ] All new commands appear in `--help`
- [ ] Commands execute without errors (basic smoke test)
- [ ] Type checking passes
- [ ] Linting passes
- [ ] Error messages are clear and actionable

---

## Handoff Output (JSON) — REQUIRED

After completing the work, create/update:

**Path**: `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A2_cli.json`

```json
{
  "schema_version": "1.0",
  "workpack": "2026-02-01_feature_hybrid-g2p-paradigm",
  "prompt": "A2_cli",
  "component": "cli",
  "delivery_mode": "pr",
  "branch": {
    "base": "feature/hybrid-g2p-paradigm",
    "work": "feature/hybrid-g2p-paradigm-cli",
    "merge_target": "feature/hybrid-g2p-paradigm"
  },
  "summary": "Implemented CLI commands for lexicon building, evaluation, and coverage analysis",
  "handoff": {
    "files_modified": ["src/furlan_g2p/cli/main.py"],
    "files_created": [
      "src/furlan_g2p/cli/lexicon_commands.py",
      "src/furlan_g2p/cli/evaluate_command.py",
      "src/furlan_g2p/cli/coverage_command.py"
    ],
    "verification": {
      "commands_run": ["furlan-g2p --help", "mypy src/", "ruff check src/"],
      "all_passed": true
    },
    "next_steps": [
      "A3_tests can implement CLI tests",
      "A4_docs can document new commands"
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

- **STOP** if A1_library interfaces are not available (wait for library completion)
- **STOP** if existing CLI structure requires major refactoring (escalate)
- **CONTINUE** for minor formatting/output questions (document choices)

---

## Deliverables

- [ ] CLI commands for lexicon operations
- [ ] CLI command for evaluation
- [ ] CLI command for coverage
- [ ] Help text for all new commands
- [ ] Handoff output JSON created
- [ ] PR created and linked in `99_status.md`
