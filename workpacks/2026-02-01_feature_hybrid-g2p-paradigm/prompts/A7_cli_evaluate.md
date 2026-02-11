# CLI Evaluate & Coverage Commands Agent Prompt

> Implement CLI commands for evaluation and coverage analysis.

---

## READ FIRST

1. `README.md` — Project overview
2. `AGENTS.md` — Agent guidelines
3. `src/furlan_g2p/cli/` — Existing CLI implementation
4. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A1_evaluation.json` — Evaluation module handoff
5. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A4_dialect_pipeline.json` — Pipeline handoff
6. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/00_request.md` — Full requirements

---

## Context

This is part of workpack: `2026-02-01_feature_hybrid-g2p-paradigm`

**Objective**: Add CLI commands for evaluating G2P quality against gold sets and analyzing coverage against wordlists.

---

## Delivery Mode

- **PR-based**: Create a PR targeting `feature/hybrid-g2p-paradigm`

---

## Objective

Expose evaluation and coverage analysis through CLI commands. These are essential for:
- Measuring G2P quality quantitatively
- Tracking progress as the system improves
- Identifying words needing annotation (OOV)
- Comparing dialect-specific performance

---

## Reference Points

- **CLI pattern**: Follow existing `click` patterns
- **Evaluation module**: Use from `furlan_g2p.evaluation`
- **Pipeline service**: Use for running G2P on words
- **Output format**: Consistent JSON/text conventions

---

## Implementation Requirements

### 1. Create `src/furlan_g2p/cli/evaluate.py`

### 2. Evaluate Command

`furlan-g2p evaluate`

**Arguments**:
- `GOLD_FILE` — Gold standard file (TSV: word\tipa or word\tipa\tdialect)

**Options**:
- `--dialect TEXT` — Dialect to use for prediction (default: from gold file or system default)
- `--output, -o PATH` — Output detailed results to file
- `--format [text|json]` — Output format
- `--verbose, -v` — Show per-word errors
- `--lexicon PATH` — Use custom lexicon file

**Output**:
- WER (word error rate)
- PER (phoneme error rate)
- Stress accuracy
- Total words evaluated
- If verbose: list of errors (word, predicted, expected)

**Behavior**:
1. Load gold set
2. Run G2P on each word
3. Compare predictions to gold
4. Compute metrics
5. Display summary
6. Optionally save detailed results

### 3. Coverage Command

`furlan-g2p coverage`

**Arguments**:
- `WORDLIST_FILE` — Wordlist (one word per line)

**Options**:
- `--lexicon PATH` — Lexicon file to check against
- `--dialect TEXT` — Dialect for lexicon lookups
- `--output, -o PATH` — Output detailed results
- `--format [text|json]` — Output format
- `--show-oov` — List OOV words in output

**Output**:
- Total words
- Lexicon hits (count and %)
- Rule-only words (count and %)
- OOV words (if truly OOV — neither lexicon nor rules)
- Coverage percentage
- If --show-oov: list of OOV words

**Behavior**:
1. Load wordlist
2. For each word, check:
   - In lexicon? → lexicon hit
   - Rules produce output? → rule hit
   - Neither? → OOV
3. Compute statistics
4. Display summary

### 4. Compare Command (optional, if time permits)

`furlan-g2p compare`

**Arguments**:
- `GOLD_FILE` — Gold standard file
- `PREDICTIONS_1` — First predictions file
- `PREDICTIONS_2` — Second predictions file

**Output**:
- Side-by-side comparison
- Which system is better for which words
- Statistical significance (if applicable)

### 5. Integration

Register commands in main CLI entry point.

---

## Scope

### In Scope

- `furlan-g2p evaluate` command
- `furlan-g2p coverage` command
- JSON and text output formats
- Error handling

### Out of Scope

- Lexicon commands (A6)
- Library implementation (A1)
- Detailed compare command (nice to have)

---

## Acceptance Criteria

- [ ] `furlan-g2p evaluate --help` shows options
- [ ] `evaluate` computes and displays WER, PER, stress accuracy
- [ ] `evaluate --verbose` shows per-word errors
- [ ] `coverage` computes and displays coverage statistics
- [ ] `coverage --show-oov` lists OOV words
- [ ] JSON output is valid and parseable
- [ ] Error messages are clear

---

## Constraints

- CLI layer must be thin — delegate to library
- Evaluation must use the module from A1
- Pipeline must use components from A4

---

## Verification

```bash
pip install -e ".[dev]"
furlan-g2p evaluate --help
furlan-g2p coverage --help

# Smoke test (requires gold file)
echo -e "aghe\tˈaɡe" > /tmp/gold.tsv
furlan-g2p evaluate /tmp/gold.tsv

# Coverage test
echo -e "aghe\nfogo\ncjase" > /tmp/words.txt
furlan-g2p coverage /tmp/words.txt

mypy src/furlan_g2p/cli/
ruff check src/furlan_g2p/cli/
```

---

## Handoff Output (JSON) — REQUIRED

**Path**: `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A7_cli_evaluate.json`

---

## Stop Conditions

- **STOP** if A1 evaluation module not available (wait)
- **STOP** if A4 pipeline not available (wait)
- **CONTINUE** for output format questions (use reasonable defaults)

---

## Deliverables

- [ ] `src/furlan_g2p/cli/evaluate.py`
- [ ] Updated CLI entry point registration
- [ ] Handoff output JSON
- [ ] PR created
