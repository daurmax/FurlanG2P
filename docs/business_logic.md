# Business Logic

This document describes the current algorithmic behavior of FurlanG2P. Source
references are listed in [references.md](references.md).

## Hybrid lookup strategy

FurlanG2P follows a hybrid priority model for pronunciation generation:

1. Lexicon lookup.
2. Optional ML exception prediction.
3. Deterministic rules.

Runtime details:
- The public architecture includes an ML interface (`IExceptionModel`) for
  exception handling.
- Base installs use `NullExceptionModel`, which always returns `None`.
- Current effective runtime path is therefore `lexicon -> rules`, while the
  `lexicon -> ML -> rules` chain is the supported extension point.

Lexicon-first behavior:
- Lexicon entries are high-precision and include metadata (`source`,
  `confidence`, `dialect`).
- If a lexicon hit exists, its IPA wins over rule output.

Rules fallback:
- If lookup fails, `PhonemeRules` generates IPA via deterministic orthography
  mappings.
- Unknown generated phonemes trigger validation errors (`ValueError`), which
  allows coverage analysis to classify true OOV items.

## Dialect handling

Dialect conditioning is carried through lookup, rule generation, and pipeline
service orchestration.

Lookup behavior:
- Dialect-aware keys are `(lemma, dialect)` plus optional universal entries
  `(lemma, None)`.
- Dialect aliases are normalized (`west -> western`, `carn -> carnic`, etc.).
- `LexiconConfig.fallback_to_universal=True` allows fallback to universal
  entries when no dialect-specific entry is found.

Pipeline behavior:
- Default dialect can be configured at service construction
  (`PipelineService(default_dialect=...)`).
- Per-request dialect overrides default at `process_text(..., dialect=...)`.
- CSV processing can consume row-specific dialects via `dialect_column`.

Rules behavior:
- Rule engine accepts a per-call dialect override.
- Dialect affects ambiguous mappings such as `z` and intervocalic `s`.

## Normalization and tokenization

Normalization enforces a stable orthographic surface before G2P:
- Unicode NFC normalization and lowercasing.
- Apostrophe normalization.
- Pause-marker normalization (`_`, `__`) from punctuation.
- Expansion of units, abbreviations, acronyms, ordinals, and numbers up to
  `999 999 999 999`.

Tokenization is two-stage:
- Sentence split with abbreviation shielding.
- Word split with regex token extraction while preserving pause markers.

## Lexicon schema fields

`lexicon.schema.LexiconEntry` fields and their purpose:

| Field | Type | Purpose |
| --- | --- | --- |
| `lemma` | `str` | Orthographic key used for lookup and merging. |
| `ipa` | `str` | Primary canonical pronunciation used as default output. |
| `dialect` | `str \| None` | Dialect conditioning (`central`, `western`, `carnic`) or universal (`None`). |
| `source` | `str` | Provenance (`seed`, `wikipron`, `manual`, etc.) for trust/audit. |
| `confidence` | `float` | Confidence score (`0.0..1.0`) used during merge tie-breaking. |
| `frequency` | `int \| None` | Optional corpus frequency/rank hint for downstream prioritization. |
| `alternatives` | `list[str]` | Secondary pronunciations retained for export/analysis. |

Derived behavior:
- `stress_marked` is true when IPA contains `ˈ` or `ˌ`.

## IPA canonicalization

Canonicalization is applied during ingestion, lookup normalization, and
evaluation comparison to prevent false mismatches.

What canonicalization does:
- Unicode NFC normalization.
- Bracket/slash stripping when present.
- Tie-bar removal (for affricate representation normalization).
- Symbol mapping via `data/ipa_mapping.tsv`.
- Multi-space collapse and trimmed output.

Why it matters:
- Prevents representational duplicates from being treated as separate variants.
- Makes validation against project phoneme inventory deterministic.
- Stabilizes evaluation metrics by comparing equivalent IPA forms.

## Evaluation metrics

`evaluation.Evaluator` computes three primary metrics:

- `WER` (word error rate): fraction of words where normalized predicted IPA does
  not exactly match normalized gold IPA.
- `PER` (phoneme error rate): total phoneme-level Levenshtein distance divided
  by total gold phoneme count.
- `Stress accuracy`: proportion of rows with matching primary stress marker
  position (`ˈ`) among rows where gold stress is present.

Supporting rules:
- IPA is normalized before comparison.
- Empty evaluation sets return zero-valued metrics.
- Length mismatch between prediction and gold lists raises `ValueError`.

## Coverage classification

The CLI `coverage` command classifies each word into exactly one class:

- `lexicon`: lexicon lookup hit.
- `rule_only`: no lexicon hit, but rules successfully generate a valid output.
- `oov`: neither lexicon nor rules produce a valid pronunciation.

Coverage ratio is computed as:
- `(lexicon_hits + rule_only_hits) / total_words`.

## End-to-end pipeline

`PipelineService` orchestrates:

1. Normalization.
2. Sentence splitting.
3. Word tokenization.
4. G2P lookup/generation.
5. Syllabification.
6. Stress assignment.

It returns `(normalized_text, phoneme_sequence)` for single-text use and offers
`process_csv` for batch metadata processing.
