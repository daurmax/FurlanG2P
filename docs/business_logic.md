# Business Logic

This document summarises the algorithms and linguistic rules implemented in FurlanG2P.

## Normalisation
- NFC‐normalises input and lowercases.
- Converts curly apostrophes to straight ones.
- Maps `, ; :` to short pause `_` and `. ? !` to long pause `__`.
- Expands units, abbreviations, acronyms and ordinals via `NormalizerConfig` mappings.
- Numbers up to 999 999 999 999 are spelled out in Friulian (`number_to_words_fr`).

## Tokenisation
- `split_sentences` replaces non‑terminal abbreviations with a sentinel character then splits on sentence‑final punctuation.
- `split_words` normalises apostrophes and extracts tokens with a regex that preserves underscore pause markers.

## Grapheme‑to‑Phoneme
- `Lexicon` provides IPA transcriptions from `seed_lexicon.tsv`; lookups are NFC‑lowercased and LRU‑cached.
- `PhonemeRules` performs deterministic orthography→IPA mapping:
  - handles digraphs (`ch`, `gh`, `cj`, `gj`, `gn`, `gl`, `ss`).
  - converts circumflex vowels to long monophthongs (`â`→`aː`, etc.).
  - applies contextual voicing (`s`→`z` between vowels, `z` dialectal choices).
  - segments the resulting IPA and validates symbols against `PHONEME_INVENTORY`.
- `G2PPhonemizer` consults the lexicon first and falls back to the rule engine; stress markers are stripped before segmentation.

## Phonology
- `canonicalize_ipa` removes tie bars and normalises variant symbols (`t͡ʃ`→`tʃ`, `ɹ`→`r`, etc.).
- `Syllabifier` merges standalone length marks with the preceding vowel and applies onset maximisation with a whitelist of clusters.
- `StressAssigner` preserves pre‑marked stress, otherwise stresses the last long vowel or the penultimate syllable.

## Pipeline
`PipelineService` chains normalisation → sentence split → word split → G2P → syllabification → stress assignment and returns the normalised text alongside the final phoneme sequence.
