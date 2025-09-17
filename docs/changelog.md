# Changelog

All notable changes to this project are documented in this file. The project
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) conventions
adapted for a lightweight semantic versioning scheme.

## [0.0.2] - 2025-09-17

### Added
- Experimental `furlang2p ipa` CLI subcommand with options for rule-only
  conversion, slash-wrapped tokens and custom separators.
- Packaged gold lexicon, IPA canonicalisation helpers and a rule-based engine
  that back the CLI and service layer.
- Initial `docs/rationale.md` and `docs/references.md` notes describing the rule
  ordering and bibliography consulted for linguistic choices.
- Continuous integration and automated release workflows executed via GitHub
  Actions.
- Seed Hypothesis-powered property tests and Click-based CLI tests covering the
  new behaviour.

### Changed
- Normaliser, tokenizer, grapheme-to-phoneme converter, syllabifier, stress
  assigner, pipeline service and IO utilities now provide working
  implementations instead of raising ``NotImplementedError``.
- The phonemiser loads pronunciations from the packaged lexicon and falls back
  to deterministic letter-to-sound rules.
- Project metadata is now sourced dynamically from ``src/furlan_g2p/__about__.py``
  and includes updated author, repository URLs and development dependencies.
- `.gitignore` allows committed VS Code tasks and ignores Hypothesis caches.
- README content was expanded with quickstart instructions, CLI examples and
  contributor guidance aligned with the implemented features.

## [0.0.1]

### Added
- Initial public release with project scaffolding, stubbed modules, packaging
  configuration and placeholder tests.
