# Changelog

All notable changes to this project are documented in this file. The project
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) conventions
adapted for a lightweight semantic versioning scheme.

## [0.0.5] - 2025-09-24

### Changed
- Replaced the MIT license with the Creative Commons Attribution-NonCommercial
  4.0 International license and shipped the full text in `LICENSE`.
- Updated packaging metadata and trove classifiers so distributions advertise
  the new license correctly.
- Documented the licensing change in both README variants and bumped the
  published version to `0.0.5`.

## [0.0.4] - 2025-09-17

### Added
- PyPI-focused `README-pypi.md` and packaging metadata that points to it so the
  project description on PyPI matches end-user expectations.

### Changed
- Rewrote the GitHub-facing `README.md` to highlight repository layout,
  contributor workflows and automation details for the release pipeline.
- Updated contributor guidance in `AGENTS.md` to reflect the newly implemented
  components and clarify documentation responsibilities.
- Bumped the published version to `0.0.4` to match the refreshed packaging
  assets.

## [0.0.3] - 2025-09-09

### Changed
- No code or documentation changes; retagged `0.0.2` as `0.0.3` to validate the
  automated release workflow.

## [0.0.2] - 2025-09-08

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

## [0.0.1] - 2025-08-23

### Added
- Initial public release with project scaffolding, stubbed modules, packaging
  configuration and placeholder tests.
