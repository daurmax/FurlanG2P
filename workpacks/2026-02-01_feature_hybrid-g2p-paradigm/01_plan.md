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
| 1 | Create evaluation module (WER, PER, stress accuracy) | A1_library | - | M |
| 2 | Define lexicon schema with dialect/confidence/frequency | A1_library | - | S |
| 3 | Create LexiconBuilder with WikiPron ingestion | A1_library | 2 | M |
| 4 | Extend Lexicon class for multi-pronunciation and dialect | A1_library | 2 | M |
| 5 | Define IExceptionModel interface | A1_library | - | S |
| 6 | Update G2P pipeline for dialect-aware lookup | A1_library | 4 | M |
| 7 | Add CLI commands (lexicon build, evaluate, coverage) | A2_cli | 1, 3, 4 | M |
| 8 | Create test suite for new modules | A3_tests | 1-6 | M |
| 9 | Update documentation (architecture, usage, READMEs) | A4_docs | 1-7 | M |
| 10 | Add `[ml]` optional extra to pyproject.toml | A1_library | 5 | XS |
| 11 | Integration, validation, and merge | A5_integration | 1-10 | M |

**Effort**: XS <30min, S 30min-2h, M 2h-4h, L 4h-8h

## Parallelization Map

```
Phase 0 (sequential):
  └── A0_bootstrap.md (create feature branch)

Phase 1 (parallel — core infrastructure):
  ├── A1_library.md ─────────────────────────┐
  │   ├── Evaluation module                  │
  │   ├── Lexicon schema                     │
  │   ├── LexiconBuilder                     │
  │   ├── Extended Lexicon                   │
  │   ├── IExceptionModel interface          │
  │   └── Pipeline dialect support           │
  │                                          │
  └── A4_docs.md (parallel architecture) ────┤
                                             │
Phase 2 (sequential — CLI):                  │
  └── A2_cli.md ─────────────────────────────┤
                                             │
Phase 3 (parallel):                          │
  └── A3_tests.md ───────────────────────────┤
                                             │
Phase 4 (sequential — merge reviewer):       │
  └── A5_integration.md ◄────────────────────┘
```

### Parallel Groups

| Group | Agents | Notes |
|-------|--------|-------|
| Group A | A1_library, A4_docs | Docs can begin architecture section while library develops |
| Group B | A2_cli | Depends on library interfaces |
| Group C | A3_tests | Depends on library but can begin with interface tests |

### Sequential Dependencies

| Must Complete First | Before Starting |
|---------------------|-----------------|
| A0_bootstrap | All others |
| A1_library (interfaces) | A2_cli |
| A1_library + A2_cli | A3_tests (full suite) |
| All A-series | A5_integration |

## Sequencing Notes

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
|------|-------|---------|
| `prompts/A0_bootstrap.md` | Bootstrap | Create feature branch |
| `prompts/A1_library.md` | Library | Core library: evaluation, lexicon, builder, interfaces |
| `prompts/A2_cli.md` | CLI | CLI commands for lexicon and evaluation |
| `prompts/A3_tests.md` | Tests | Test suite for new modules |
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
