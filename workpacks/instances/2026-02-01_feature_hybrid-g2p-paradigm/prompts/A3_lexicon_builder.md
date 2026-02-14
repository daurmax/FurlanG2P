# WikiPron & LexiconBuilder Agent Prompt

> Implement LexiconBuilder with WikiPron ingestion and IPA canonicalization.

---

## READ FIRST

1. `README.md` — Project overview
2. `AGENTS.md` — Agent guidelines
3. `src/furlan_g2p/phonology/` — Existing IPA/phonology utilities
4. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A2_lexicon_schema.json` — Schema handoff
5. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/00_request.md` — Full requirements
6. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/01_plan.md` — Work breakdown

---

## Context

This is part of workpack: `2026-02-01_feature_hybrid-g2p-paradigm`

**Objective**: Create the LexiconBuilder class that ingests pronunciation data from WikiPron and other sources, normalizes IPA to the project inventory, and outputs structured lexicon files.

---

## Delivery Mode

- **PR-based**: Create a PR targeting `feature/hybrid-g2p-paradigm`

---

## Objective

Implement the lexicon building infrastructure that enables bootstrapping a large pronunciation dictionary from available resources. This is **Phase 1** of the roadmap — creating the data ingestion pipeline.

The builder must:
- Parse WikiPron TSV format (word, IPA, optional dialect)
- Canonicalize IPA symbols to the project inventory
- Validate entries and report issues
- Support incremental building from multiple sources
- Output to TSV or JSONL formats

---

## Reference Points

- **Lexicon schema**: Use `LexiconEntry` from A2_lexicon_schema
- **Storage**: Use I/O functions from `lexicon/storage.py`
- **Phoneme inventory**: Check existing phoneme definitions in `phonology/` if available
- **Interface pattern**: Follow ABC pattern from `core/interfaces.py`

---

## Implementation Requirements

### 1. Add to `src/furlan_g2p/lexicon/` package

New files:
- `builder.py` — LexiconBuilder class
- `wikipron.py` — WikiPron-specific parsing
- `canonicalizer.py` — IPA normalization

### 2. WikiPron Parser

**WikiPron TSV format**: `word\tIPA` or `word\tIPA\tlanguage_code`

Parser requirements:
- Handle UTF-8 encoding with BOM
- Skip malformed lines with warning
- Extract dialect from language code if present (e.g., `fur` → default, could have variants)
- Handle multi-pronunciation entries (same word, different IPA)

### 3. IPA Canonicalizer

Normalize IPA symbols to a consistent inventory:
- Map common variants (e.g., `g` → `ɡ`, `'` → `ˈ`)
- Remove tie bars or handle them consistently
- Handle diacritics (combining characters)
- Flag unknown symbols for review

Create a mapping table as configuration (not hardcoded).

### 4. LexiconBuilder Class

**Responsibilities**:
- Accept entries from multiple sources
- Deduplicate: same (lemma, dialect) → merge alternatives or keep highest confidence
- Track source and assign confidence based on source type
- Validate against phoneme inventory (if available)
- Export to various formats

**Methods**:
- `add_source(path: Path, source_type: str, dialect: str | None = None) -> int` — Add entries from file
- `add_entry(entry: LexiconEntry) -> bool` — Add single entry, return success
- `merge_entry(entry: LexiconEntry) -> None` — Merge with existing or add
- `validate() -> list[ValidationIssue]` — Check all entries
- `build() -> list[LexiconEntry]` — Return final entry list
- `export(path: Path, format: str = "jsonl") -> None` — Write to file

### 5. Validation and Reporting

- Count entries per source
- Count entries per dialect
- List unknown IPA symbols encountered
- List duplicate entries (same lemma, different IPA)
- Generate summary report

---

## Contracts

### ILexiconBuilder (interface in `core/interfaces.py`)

| Method | Returns | Notes |
|--------|---------|-------|
| `add_source(path, source_type, dialect)` | `int` | Returns entry count |
| `add_entry(entry)` | `bool` | Returns success |
| `build()` | `list[LexiconEntry]` | Final entries |
| `validate()` | `list[ValidationIssue]` | Issues found |

### IPACanonicalize (utility class)

| Method | Returns | Notes |
|--------|---------|-------|
| `canonicalize(ipa: str)` | `str` | Normalized IPA |
| `get_unknown_symbols(ipa: str)` | `set[str]` | Unknown symbols |

---

## Scope

### In Scope

- LexiconBuilder class
- WikiPron parser
- IPA canonicalizer with mapping table
- Validation and reporting
- ILexiconBuilder interface

### Out of Scope

- COF/Hunspell wordlist ingestion (future prompt)
- Frequency calculation (future prompt)
- Gold set creation tools (future prompt)
- CLI commands (A6)

---

## Acceptance Criteria

- [ ] WikiPron TSV files can be parsed
- [ ] IPA canonicalization maps common variants
- [ ] Unknown IPA symbols are logged/reported
- [ ] Duplicate handling works (merge alternatives)
- [ ] Multiple sources can be combined
- [ ] Export to TSV and JSONL works
- [ ] Validation reports issues clearly
- [ ] mypy passes

---

## Constraints

- **CRITICAL**: No network access — files are pre-downloaded
- IPA mapping table should be configurable (TSV or YAML)
- Keep memory efficient for large lexicons (streaming if needed)

---

## Verification

```bash
pip install -e ".[dev]"
python -c "from furlan_g2p.lexicon import LexiconBuilder; print('OK')"
python -c "from furlan_g2p.lexicon.canonicalizer import IPACanonicalize; print('OK')"
mypy src/furlan_g2p/lexicon/
ruff check src/furlan_g2p/lexicon/
```

---

## Handoff Output (JSON) — REQUIRED

**Path**: `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A3_lexicon_builder.json`

---

## Stop Conditions

- **STOP** if A2 lexicon schema is not available (wait)
- **CONTINUE** for IPA mapping questions (document choices, use reasonable defaults)

---

## Deliverables

- [ ] `src/furlan_g2p/lexicon/builder.py`
- [ ] `src/furlan_g2p/lexicon/wikipron.py`
- [ ] `src/furlan_g2p/lexicon/canonicalizer.py`
- [ ] IPA mapping configuration file
- [ ] Updated `core/interfaces.py` with `ILexiconBuilder`
- [ ] Handoff output JSON
- [ ] PR created
