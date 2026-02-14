# CLI Lexicon Commands Agent Prompt

> Implement CLI commands for lexicon building, info, and export.

---

## READ FIRST

1. `README.md` — Project overview
2. `AGENTS.md` — Agent guidelines
3. `src/furlan_g2p/cli/` — Existing CLI implementation
4. `docs/usage.md` — Current CLI documentation
5. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A2_lexicon_schema.json` — Schema handoff
6. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A3_lexicon_builder.json` — Builder handoff
7. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/00_request.md` — Full requirements

---

## Context

This is part of workpack: `2026-02-01_feature_hybrid-g2p-paradigm`

**Objective**: Add CLI commands for lexicon operations: building from sources, inspecting lexicons, and format conversion.

---

## Delivery Mode

- **PR-based**: Create a PR targeting `feature/hybrid-g2p-paradigm`

---

## Objective

Expose the lexicon building functionality through CLI commands. Users need to:
- Build lexicons from WikiPron and other sources
- Inspect existing lexicons (statistics, validation)
- Convert between formats (TSV ↔ JSONL)

These commands support the data preparation workflow for the hybrid G2P system.

---

## Reference Points

- **CLI pattern**: Follow existing `click` patterns in `src/furlan_g2p/cli/`
- **Error handling**: Follow try-except-exit pattern from existing commands
- **Output format**: Use consistent JSON/text output conventions
- **LexiconBuilder**: Use from `furlan_g2p.lexicon.builder`

---

## Implementation Requirements

### 1. Create `src/furlan_g2p/cli/lexicon.py`

Command group: `furlan-g2p lexicon`

### 2. Build Command

`furlan-g2p lexicon build`

**Arguments**:
- `INPUT_FILES` — One or more source files (positional, multiple)

**Options**:
- `--output, -o PATH` — Output file path (required)
- `--format, -f [tsv|jsonl]` — Output format (default: jsonl)
- `--source-type [wikipron|tsv|manual]` — Source type for confidence assignment
- `--dialect TEXT` — Default dialect for entries without dialect
- `--validate / --no-validate` — Run validation after build (default: validate)
- `--verbose, -v` — Verbose output

**Behavior**:
- Parse all input files
- Merge entries (handle duplicates)
- Validate if requested
- Write to output
- Print summary (entry count, sources, dialects, issues)

### 3. Info Command

`furlan-g2p lexicon info`

**Arguments**:
- `LEXICON_FILE` — Lexicon file to inspect (positional)

**Options**:
- `--json` — Output as JSON
- `--verbose, -v` — Include per-dialect breakdown

**Output**:
- Total entry count
- Entries by dialect
- Entries by source
- Entries with alternatives
- Entries with stress markers
- Validation issues (if any)

### 4. Export Command

`furlan-g2p lexicon export`

**Arguments**:
- `INPUT_FILE` — Source lexicon (positional)
- `OUTPUT_FILE` — Destination file (positional)

**Options**:
- `--format, -f [tsv|jsonl|tsv-simple]` — Output format
- `--dialect TEXT` — Filter to specific dialect
- `--min-confidence FLOAT` — Filter by minimum confidence

**Behavior**:
- Read input
- Apply filters
- Write to output format
- Support TSV (extended), TSV-simple (just word\tipa), JSONL

### 5. Validate Command

`furlan-g2p lexicon validate`

**Arguments**:
- `LEXICON_FILE` — Lexicon file to validate (positional)

**Options**:
- `--strict` — Treat warnings as errors
- `--json` — Output as JSON

**Output**:
- List of validation issues
- Exit code 0 if valid, 1 if issues found (or warnings in strict mode)

### 6. Integration with Main CLI

Register commands in main CLI entry point.

---

## Scope

### In Scope

- `furlan-g2p lexicon build` command
- `furlan-g2p lexicon info` command
- `furlan-g2p lexicon export` command
- `furlan-g2p lexicon validate` command
- Help text for all commands
- Error handling

### Out of Scope

- Evaluation commands (A7)
- Coverage commands (A7)
- Library implementation (already done in A2, A3)

---

## Acceptance Criteria

- [ ] `furlan-g2p lexicon --help` shows all subcommands
- [ ] `build` creates lexicon from input files
- [ ] `info` displays lexicon statistics
- [ ] `export` converts between formats
- [ ] `validate` checks lexicon integrity
- [ ] All commands have --help with clear descriptions
- [ ] Error messages are clear and actionable
- [ ] Exit codes are correct (0 success, 1 error)

---

## Constraints

- CLI layer must be thin — delegate to library
- Follow existing CLI patterns exactly
- No new dependencies

---

## Verification

```bash
pip install -e ".[dev]"
furlan-g2p lexicon --help
furlan-g2p lexicon build --help
furlan-g2p lexicon info --help

# Smoke test with sample data
echo -e "test\ttɛst" > /tmp/sample.tsv
furlan-g2p lexicon build /tmp/sample.tsv -o /tmp/lexicon.jsonl
furlan-g2p lexicon info /tmp/lexicon.jsonl

mypy src/furlan_g2p/cli/
ruff check src/furlan_g2p/cli/
```

---

## Handoff Output (JSON) — REQUIRED

**Path**: `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A6_cli_lexicon.json`

---

## Stop Conditions

- **STOP** if A2/A3 library components not available (wait)
- **CONTINUE** for minor CLI design questions (document choices)

---

## Deliverables

- [ ] `src/furlan_g2p/cli/lexicon.py`
- [ ] Updated CLI entry point registration
- [ ] Handoff output JSON
- [ ] PR created
