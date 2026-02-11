# Dialect-Aware Pipeline Agent Prompt

> Extend the Lexicon class and G2P pipeline with dialect-aware lookup and fallback logic.

---

## READ FIRST

1. `README.md` — Project overview
2. `AGENTS.md` — Agent guidelines
3. `src/furlan_g2p/g2p/lexicon.py` — Current lexicon implementation
4. `src/furlan_g2p/g2p/phonemizer.py` — Current phonemizer
5. `src/furlan_g2p/services/` — Pipeline service
6. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A2_lexicon_schema.json` — Schema handoff
7. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A3_lexicon_builder.json` — Builder handoff
8. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/00_request.md` — Full requirements

---

## Context

This is part of workpack: `2026-02-01_feature_hybrid-g2p-paradigm`

**Objective**: Extend the existing Lexicon class and G2P pipeline to support dialect-aware lookups with intelligent fallback, integrating the new schema.

---

## Delivery Mode

- **PR-based**: Create a PR targeting `feature/hybrid-g2p-paradigm`

---

## Objective

Upgrade the lexicon lookup and phonemizer to work with the new multi-dialect lexicon schema. The pipeline must:

- Prioritize dialect-specific entries
- Fallback to universal entries when dialect entry is missing
- Support configuration of dialect behavior
- Maintain backward compatibility with existing API

This is the integration point between the new lexicon infrastructure and the existing G2P pipeline.

---

## Reference Points

- **Current Lexicon**: Study `g2p/lexicon.py` for LRU cache and lookup patterns
- **Current Phonemizer**: Study `g2p/phonemizer.py` for rule fallback pattern
- **New Schema**: Use `LexiconEntry` and `LexiconConfig` from A2
- **New Storage**: Use I/O from `lexicon/storage.py`

---

## Implementation Requirements

### 1. Extend Lexicon Class

Either refactor existing `g2p/lexicon.py` or create new `lexicon/lookup.py`:

**New capabilities**:
- Load from new JSONL format (in addition to TSV)
- Index by (lemma, dialect) for fast lookup
- Support `LexiconConfig` for behavior control
- Return `LexiconEntry` objects (not just IPA strings)

**Lookup logic**:
1. If `dialect` specified and entry exists for that dialect → return it
2. If `fallback_to_universal` and universal entry exists → return it
3. Return None (let rules handle it)

**Caching**:
- Maintain LRU cache for performance
- Cache key includes dialect

### 2. Create DialectAwareLexicon

New class that wraps the lookup logic:

```
class DialectAwareLexicon:
    def __init__(self, entries: list[LexiconEntry], config: LexiconConfig)
    def lookup(self, word: str, dialect: str | None = None) -> LexiconEntry | None
    def lookup_ipa(self, word: str, dialect: str | None = None) -> str | None
    def get_alternatives(self, word: str, dialect: str | None = None) -> list[str]
    def has_entry(self, word: str, dialect: str | None = None) -> bool
    def stats() -> dict  # Entry counts by dialect, source, etc.
```

### 3. Update Phonemizer Integration

Modify `g2p/phonemizer.py` (or create wrapper) to:
- Accept dialect parameter in `to_phonemes`
- Use DialectAwareLexicon for lookups
- Pass dialect to rules if rules support dialect-specific behavior
- Log when using fallback (dialect entry not found)

### 4. Pipeline Service Update

Update `services/` to:
- Accept dialect configuration
- Pass dialect through the pipeline
- Support per-request dialect override

### 5. Backward Compatibility

Ensure:
- Existing Lexicon API still works
- Existing TSV loading still works
- Default behavior (no dialect specified) matches previous behavior

---

## Contracts

### DialectAwareLexicon

| Method | Returns | Notes |
|--------|---------|-------|
| `lookup(word, dialect)` | `LexiconEntry \| None` | Full entry |
| `lookup_ipa(word, dialect)` | `str \| None` | Just IPA string |
| `get_alternatives(word, dialect)` | `list[str]` | Alternative IPAs |
| `has_entry(word, dialect)` | `bool` | Existence check |
| `stats()` | `dict` | Statistics |

### Updated IG2PPhonemizer (if needed)

| Method | Returns | Notes |
|--------|---------|-------|
| `to_phonemes(tokens, dialect)` | `list[str]` | Add optional dialect param |

---

## Scope

### In Scope

- DialectAwareLexicon class
- Extended Lexicon loading (JSONL support)
- Dialect parameter in phonemizer
- Fallback logic implementation
- Pipeline service updates
- Backward compatibility

### Out of Scope

- ML exception model (A5)
- CLI commands (A6, A7)
- Tests (A8)
- Documentation (A9)

---

## Acceptance Criteria

- [ ] Lexicon loads from both TSV and JSONL
- [ ] Dialect-specific lookup returns correct entries
- [ ] Fallback to universal works when configured
- [ ] Phonemizer accepts dialect parameter
- [ ] Existing API still works (backward compatible)
- [ ] LRU caching still works
- [ ] mypy passes

---

## Constraints

- **CRITICAL**: Do not break existing functionality
- Maintain LRU cache efficiency
- Keep memory footprint reasonable for large lexicons

---

## Verification

```bash
pip install -e ".[dev]"
python -c "from furlan_g2p.lexicon import DialectAwareLexicon; print('OK')"
# Verify existing tests still pass
pytest tests/test_g2p.py -v
mypy src/furlan_g2p/g2p/ src/furlan_g2p/lexicon/
ruff check src/
```

---

## Handoff Output (JSON) — REQUIRED

**Path**: `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A4_dialect_pipeline.json`

---

## Stop Conditions

- **STOP** if A2 or A3 outputs not available (wait)
- **STOP** if existing tests fail significantly (investigate)
- **CONTINUE** for minor API design questions (document choices)

---

## Deliverables

- [ ] `src/furlan_g2p/lexicon/lookup.py` (or updated `g2p/lexicon.py`)
- [ ] Updated `g2p/phonemizer.py`
- [ ] Updated service layer
- [ ] Handoff output JSON
- [ ] PR created
