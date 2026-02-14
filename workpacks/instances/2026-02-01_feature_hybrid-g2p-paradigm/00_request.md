# Request

> Paradigm shift to hybrid G2P architecture: expanded lexicon + rules + optional ML exception model with dialect conditioning.

## Workpack Protocol Version

Workpack Protocol Version: 3

## Original Request

This workpack implements a fundamental paradigm shift for FurlanG2P based on extensive research into low-resource G2P systems and best practices from SIGMORPHON shared tasks.

### Recommended Approach: Hybrid Architecture

**Priority order:**

1. **Build a large "bootstrap" lexicon** from Wiktionary (automatic extraction via WikiPron) as a high-precision source for common words
2. **Maintain deterministic rules** as fallback (cover the majority of regular forms, fundamental for transparency)
3. **Add a data-driven "exception model"** (very small), trained on a few thousand grapheme→IPA pairs for:
   - Unpredictable stress
   - Lexical variants / loanwords / irregularities  
   - Ambiguities (e.g., s/z, affricates)
4. **Manage dialects via conditioning** (dialect tag/embedding or model prefix) instead of duplicating everything

This approach is consistent with G2P low-resource shared tasks (even with 800 examples) and with work on multilingual/transfer models using "language/dialect prefix".

### Resources to Integrate

1. **WikiPron** for automatic (lemma, IPA) extraction from Friulian Wiktionary
2. **COF/Hunspell wordlist** for coverage measurement and frequency selection
3. **Gold set (2k–5k words)** with verified IPA, stress, and dialect tags
4. **Optional small neural model** with joint phoneme+stress prediction and dialect prefix

### Architecture Addition

Two new components (optional but recommended):

**A. LexiconBuilder**
- Sources: WikiPron/Wiktionary, seed TSV, potentially others
- Normalize IPA → inventory
- Store: `lemma`, `dialect`, `ipa`, `source`, `confidence`, `freq`

**B. ExceptionModel (optional)**
- Input: graphemes (+ dialect prefix)
- Output: IPA with stress
- Role: override/rerank when (a) stress uncertain, (b) irregular pattern, (c) frequent word

### Roadmap Phases

**Phase 0 (1-2 days) — Metrics & dataset skeleton**
- Define formats: TSV/JSONL for `(word, dialect, ipa, source)`
- Implement evaluator: WER (word-level), PER (phoneme edit distance), stress accuracy

**Phase 1 (1-2 weeks) — Large bootstrap lexicon**
- Integrate WikiPron extraction + filters
- Canonicalize IPA symbols to inventory
- Goal: hundreds/thousands of entries

**Phase 2 (2-4 weeks) — Coverage & active learning**
- Import COF/Hunspell wordlist
- Calculate frequencies (from Friulian Wikipedia)
- Select 2k-5k words for manual annotation (gold set) + critical dialect cases

**Phase 3 (2-6 weeks) — ExceptionModel**
- Option "light": small Transformer/LSTM with dialect prefix
- Train on: (Wiktionary + gold), use rules as "teacher" for controlled augmentation
- Export model (asset) and make optional (`pip extra`)

**Phase 4 (continuous) — Dialects**
- Add dialect tag in lexicon
- Add dialect token in model
- Prepare separate test sets per variant

## Acceptance Criteria

- [ ] AC1: `LexiconBuilder` can ingest WikiPron-format data and normalize to the project IPA inventory
- [ ] AC2: Lexicon schema supports `(lemma, dialect, ipa, source, confidence, freq)` with multi-pronunciation capability
- [ ] AC3: Evaluation module computes WER, PER, and stress accuracy metrics
- [ ] AC4: G2P pipeline uses lexicon lookup with dialect-aware fallback to rules
- [ ] AC5: Optional `ExceptionModel` interface defined with pluggable implementations
- [ ] AC6: CLI commands for lexicon building, evaluation, and coverage analysis
- [ ] AC7: Documentation covers the new hybrid architecture and evaluation workflow
- [ ] AC8: All new code has type hints and passes mypy/ruff checks
- [ ] AC9: Tests achieve ≥80% coverage for new modules
- [ ] AC10: `pip install furlan-g2p[ml]` optional extra for ML dependencies

## Constraints

- **CRITICAL**: Keep core library lightweight (no ML deps in base install)
- **CRITICAL**: All dialect variants use single codebase with conditioning, not duplication
- Runtime dependencies must remain minimal (ML behind optional `[ml]` extra)
- Follow existing interface patterns from `core.interfaces`
- Type hints everywhere, docstrings with examples
- Consult `docs/references.md` for linguistic rules

## Acceptance Criteria → Verification Mapping

| AC ID | Acceptance Criterion | How to Verify |
|-------|----------------------|---------------|
| AC1 | LexiconBuilder ingests WikiPron data | `pytest tests/test_lexicon_builder.py -v` |
| AC2 | Lexicon schema with dialect/confidence | `pytest tests/test_lexicon.py::test_schema -v` |
| AC3 | Evaluation metrics (WER, PER, stress) | `pytest tests/test_evaluation.py -v` |
| AC4 | Dialect-aware lexicon lookup | `pytest tests/test_g2p.py::test_dialect_lookup -v` |
| AC5 | ExceptionModel interface | `mypy src/` + import test |
| AC6 | CLI commands | `furlan-g2p --help` + `pytest tests/test_cli.py -v` |
| AC7 | Documentation | Manual review of `docs/` and READMEs |
| AC8 | Type checking passes | `mypy src/` |
| AC9 | Test coverage ≥80% | `pytest --cov=src/furlan_g2p --cov-fail-under=80` |
| AC10 | Optional ML extra | `pip install -e ".[ml]"` succeeds |

## Delivery Mode

- [x] **PR-based** (default, recommended) — Create feature branch and PR for review
- [ ] **Direct push**

## Scope

### In Scope

- LexiconBuilder module with WikiPron ingestion and IPA canonicalization
- Extended Lexicon class with dialect, source, confidence, frequency fields
- Evaluation module (WER, PER, stress accuracy)
- IExceptionModel interface with abstract methods
- CLI commands for lexicon operations and evaluation
- Documentation for hybrid architecture
- Test suite for new modules
- Optional `[ml]` extra in pyproject.toml

### Out of Scope

- Actual neural model training (future work)
- Full WikiPron extraction pipeline (manual extraction is acceptable)
- Forvo/audio data integration (future work)
- Active learning annotation UI (future work)
- Production deployment considerations

## Context

### Key References

- WikiPron: https://github.com/CUNY-CL/wikipron
- SIGMORPHON 2020 G2P Shared Task: https://aclanthology.org/2020.sigmorphon-1.2/
- ByT5 multilingual G2P: https://www.isca-archive.org/interspeech_2022/zhu22_interspeech.pdf
- COF (Coretôr Ortografic Furlan): https://arlef.it/struments/coretor-ortografic-furlan/
- Friulian Wiktionary IPA category: https://en.wiktionary.org/wiki/Category:Friulian_terms_with_IPA_pronunciation

### Related Project Files

- `AGENTS.md` — Coding standards
- `docs/architecture.md` — Current architecture
- `docs/references.md` — Linguistic bibliography
- `src/furlan_g2p/core/interfaces.py` — Existing interfaces
- `src/furlan_g2p/g2p/lexicon.py` — Current lexicon implementation
