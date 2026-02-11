# Plan

> Hybrid G2P paradigm: expanded lexicon, evaluation infrastructure, ML exception model interface, dialect conditioning.

## Summary

This workpack implements a paradigm shift from pure rule-based G2P to a hybrid architecture combining:
1. Large lexicon (from WikiPron/Wiktionary)
2. Deterministic rules (fallback)
3. Optional ML exception model (for stress/irregularities)
4. Dialect conditioning (single model, multiple variants)

The work is structured in phases matching the research roadmap, with each phase adding capabilities while maintaining backward compatibility.

## Work Breakdown Structure (WBS)

| # | Task | Agent | Depends On | Estimated Effort |
|---|------|-------|------------|------------------|
| 1 | Create feature branch | A0_bootstrap | - | XS |
| 2 | Create evaluation module (WER, PER, stress accuracy) | A1_evaluation | A0 | M |
| 3 | Define lexicon schema with dialect/confidence/frequency | A2_lexicon_schema | A0 | S |
| 4 | Create LexiconBuilder with WikiPron ingestion | A3_lexicon_builder | A2 | M |
| 5 | Update G2P pipeline for dialect-aware lookup | A4_dialect_pipeline | A2, A3 | M |
| 6 | Define IExceptionModel interface and [ml] extra | A5_ml_interface | A0 | S |
| 7 | Add CLI commands for lexicon (build, info, export, validate) | A6_cli_lexicon | A3, A4 | M |
| 8 | Add CLI commands (evaluate, coverage) | A7_cli_evaluate | A1, A4 | M |
| 9 | Create test suite for new modules | A8_tests | A1-A7 | M |
| 10 | Update documentation (architecture, usage, READMEs) | A9_docs | A1-A8 | M |
| 11 | Integration, validation, and merge | A10_integration | A1-A9 | M |

**Effort**: XS <30min, S 30min-2h, M 2h-4h, L 4h-8h

## Parallelization Map

```
Phase 0 (sequential):
  └── A0_bootstrap.md (create feature branch)

Phase 1 (parallel — core infrastructure):
  ├── A1_evaluation.md ──────────────────────┐
  ├── A2_lexicon_schema.md ──────────────────┤
  └── A5_ml_interface.md ────────────────────┤
                                             │
Phase 2 (parallel — builders):               │
  ├── A3_lexicon_builder.md (needs A2) ──────┤
  └── A4_dialect_pipeline.md (needs A2,A3) ──┤
                                             │
Phase 3 (parallel — CLI):                    │
  ├── A6_cli_lexicon.md (needs A3,A4) ───────┤
  └── A7_cli_evaluate.md (needs A1,A4) ──────┤
                                             │
Phase 4 (sequential — tests & docs):         │
  ├── A8_tests.md (needs A1-A7) ─────────────┤
  └── A9_docs.md (needs A1-A8) ──────────────┤
                                             │
Phase 5 (sequential — merge reviewer):       │
  └── A10_integration.md ◄───────────────────┘
```

### Parallel Groups

| Group | Agents | Notes |
|-------|--------|-------|
| Group A | A1, A2, A5 | Independent core infrastructure |
| Group B | A3, A4 | Depend on A2, can run after schema |
| Group C | A6, A7 | CLI commands, need builders complete |
| Group D | A8, A9 | Tests and docs, need implementation |

### Sequential Dependencies

| Must Complete First | Before Starting |
|---------------------|-----------------|
| A0_bootstrap | All others |
| A2_lexicon_schema | A3_lexicon_builder, A4_dialect_pipeline |
| A3_lexicon_builder | A4_dialect_pipeline, A6_cli_lexicon |
| A1_evaluation, A4_dialect_pipeline | A7_cli_evaluate |
| A1-A7 | A8_tests |
| A1-A8 | A9_docs |
| A1-A9, A2, A5** can run in parallel as initial infrastructure
2. **A3, A4** form the builder layer and depend on schema (A2)
3. **A6, A7** are CLI layers that can run in parallel once builders complete
4. **A8** tests require all implementation complete (A1-A7)
5. **A9** docs need tests to verify examples
6. **A10
1. **A1_library** is the critical path — defines all new interfaces and implementations
2. **A4_docs** can run in parallel for architecture documentation, but usage docs depend on A2_cli
3. **A3_tests** can start with interface/unit tests while waiting for CLI
4. **A5_integration** acts as merge reviewer and runs full validation suite

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| WikiPron extraction yields few Friulian entries | Med | Med | Fallback to manual extraction from Wiktionary; document minimal requirements |
| IPA canonicalization mismatches | Med | Med | Create mapping table and validation tests; log warnings for unknown symbols |
| ML dependencies conflict with base install | Low | High | Strict separation via optional `[ml]` extra; import guards |
| Dialect conditioning complexity | Med | Med | Start with simple prefix approach; defer embedding to future work |
| Breaking changes to existing Lexicon | Low | Med | Extend rather than replace; maintain backward compatibility |

## Security & Tool Safety

- **Untrusted inputs**: WikiPron data, external TSV files should be validated before ingestion
- **Write operations**: Limit file writes to project workspace and data directories
- **No secrets**: Never include API keys, tokens, or credentials in prompts or outputs
- **Tool safety**: Validate WikiPron URLs; sandbox file I/O operations

## Handoff Outputs Plan (Protocol v3)

- **Mapping**: Each `prompts/<PROMPT>.md` produces `outputs/<PROMPT>.json` upon completion
- **Schema**: All output JSONs must conform to `workpacks/WORKPACK_OUTPUT_SCHEMA.json`
- **Contents**: Summary of changes, files modified/created, verification results, next steps, known issues
- **Artifacts**: Include PR URLs and/or commit SHAs for traceability

## Regression / Evals Plan

- **A-series**: Ensure existing tests continue to pass; add new tests for new functionality
- **Coverage target**: ≥80% for new modules
- **Evaluation**: New evaluation module enables measuring WER/PER/stress accuracy on gold sets
- **Backward compatibility**: Existing `Lexicon` API must remain functional

## Verification Strategy

- [ ] `pytest tests/ -v` passes
- [ ] `pytest --cov=src/furlan_g2p --cov-fail-under=80` passes for new modules
- [ ] `mypy src/` passes
- [ ] `ruff check src/ tests/` passes
- [ ] `furlan-g2p --help` shows new commands
- [ ] `pip install -e ".[ml]"` succeeds (optional extra)
- [ ] Documentation builds without errors
- [ ] Manual verification of WikiPron ingestion

## Branch Strategy

| Component | Branch Name | Base Branch | PR Target |
|-----------|-------------|-------------|-----------|
| Feature | `feature/hybrid-g2p-paradigm` | `main` | `main` |

---

## Prompts to Generate

### Feature Implementation Prompts (A-series)

| File | Agent | Purpose |
|------|------evaluation.md` | Evaluation | WER, PER, stress accuracy module |
| `prompts/A2_lexicon_schema.md` | Schema | LexiconEntry, LexiconConfig, storage I/O |
| `prompts/A3_lexicon_builder.md` | Builder | WikiPron ingestion, IPA canonicalizer |
| `prompts/A4_dialect_pipeline.md` | Pipeline | Dialect-aware lookup, phonemizer updates |
| `prompts/A5_ml_interface.md` | ML Interface | IExceptionModel, NullExceptionModel, [ml] extra |
| `prompts/A6_cli_lexicon.md` | CLI Lexicon | build, info, export, validate commands |
| `prompts/A7_cli_evaluate.md` | CLI Evaluate | evaluate, coverage commands |
| `prompts/A8_tests.md` | Tests | Test suite for all new modules |
| `prompts/A9_docs.md` | Docs | Documentation updates |
| `prompts/A10_tests.md` | Tests | Test suite for new modules |
| `prompts/A4_docs.md` | Docs | Documentation updates |
| `prompts/A5_integration.md` | Integration | Merge reviewer and validation |

---

## Architecture Changes

### New Modules

```
src/furlan_g2p/
├── evaluation/          # NEW: WER, PER, stress accuracy
│   ├── __init__.py
│   ├── metrics.py       # Evaluation functions
│   └── types.py         # Evaluation result types
├── lexicon/             # NEW: Refactored lexicon module
│   ├── __init__.py
│   ├── builder.py       # LexiconBuilder class
│   ├── schema.py        # LexiconEntry, LexiconConfig
│   ├── storage.py       # TSV/JSONL I/O
│   └── wikipron.py      # WikiPron ingestion
└── ml/                  # NEW: Optional ML module
    ├── __init__.py
    └── interfaces.py    # IExceptionModel
```

### Interface Extensions

```
core/interfaces.py additions:
├── ILexiconBuilder     # Build lexicon from sources
├── IEvaluator          # Compute G2P metrics
└── IExceptionModel     # ML-based exception handling
```

### Lexicon Schema

```
LexiconEntry:
├── lemma: str
├── ipa: str
├── dialect: str | None       # "central", "western", "carnic"
├── source: str               # "wikipron", "manual", "seed"
├── confidence: float         # 0.0-1.0
├── frequency: int | None     # Corpus frequency rank
└── alternatives: list[str]   # Alternative pronunciations
```
