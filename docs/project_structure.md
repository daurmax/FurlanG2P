# Project structure and status

This document outlines the main business logic modules in FurlanG2P, their responsibilities, current development state and planned work.

## Normalization (`src/furlan_g2p/normalization/`)
**Purpose.** Convert raw text into a normalized form.

**Status.** `Normalizer` collapses whitespace and lowercases tokens; an `ExperimentalNormalizer` offers rudimentary tokenization for testing.

**TODO.**
- Load rule sets from configuration.
- Expand normalization rules for numbers, acronyms and punctuation.
- Unify experimental normalizer with the public API.

## Tokenization (`src/furlan_g2p/tokenization/`)
**Purpose.** Split normalized text into sentences and word tokens.

**Status.** Regex-based splitter without abbreviation handling or pause management.

**TODO.**
- Handle abbreviations and honorifics that should not split sentences.
- Preserve pause markers and non speech tokens.
- Provide word-level configuration hooks.

## G2P (`src/furlan_g2p/g2p/`)
**Purpose.** Map tokens to phoneme sequences using a lexicon and rule engine.

**Status.** `Lexicon` loads a small TSV; `RuleEngine` covers a handful of digraphs and vowel contrasts; `PhonemeRules.apply` is unimplemented.

**TODO.**
- Grow the packaged lexicon and expose source metadata.
- Implement the `PhonemeRules` letter‑to‑sound engine.
- Support dialectal variants and a managed phoneme inventory.

## Phonology (`src/furlan_g2p/phonology/`)
**Purpose.** Post-process phoneme strings: canonicalization, syllabification and stress.

**Status.** Heuristic `Syllabifier` and penultimate-stress `StressAssigner` are in place; other phonological processes are absent.

**TODO.**
- Refine syllabification to cover complex clusters and hiatus.
- Implement lexical and post‑lexical stress rules.
- Expand helpers for allophony and prosody.

## Services (`src/furlan_g2p/services/`)
**Purpose.** High-level orchestration and I/O helpers.

**Status.** `PipelineService` chains the normalizer, tokenizer, phonemizer and phonology; `IOService` handles UTF‑8 text files.

**TODO.**
- Allow dependency injection and configuration of pipeline components.
- Wire services into CLI subcommands and batch processors.
- Add streaming and asynchronous interfaces.

## CLI (`src/furlan_g2p/cli/`)
**Purpose.** User-facing command-line tools.

**Status.** Only the `ipa` command works; `normalize`, `g2p` and `phonemize-csv` raise `NotImplementedError`.

**TODO.**
- Implement remaining subcommands using `PipelineService`.
- Provide option groups for dialect, output format and config files.
- Add CSV batch phonemization utility.

## Config (`src/furlan_g2p/config/`)
**Purpose.** Typed configuration schemas for pipeline components.

**Status.** Dataclasses exist but are not yet loaded from user-provided files.

**TODO.**
- Parse configuration from TOML/YAML files.
- Validate and merge user overrides.

## Core (`src/furlan_g2p/core/`)
**Purpose.** Shared interfaces, type aliases and exceptions.

**Status.** Interfaces define stable public contracts.

**TODO.**
- Extend error hierarchy with richer context.
- Document interface guarantees for contributors.

## Data (`src/furlan_g2p/data/`)
**Purpose.** Packaged resources such as the seed lexicon.

**Status.** Contains a minimal TSV lexicon for testing.

**TODO.**
- Expand lexical coverage and include metadata about sources and variants.

