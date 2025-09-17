# Changelog

All notable changes to this project are documented in this file.

## [0.0.2]

### Added
- Experimental `furlang2p ipa` CLI subcommand that combines the seed lexicon with a
  rule-based fallback, supports pause tokens and optional IPA slashes.
- Packaged Friulian seed lexicon, canonical IPA normaliser and lightweight rule
  engine derived from the sources in `docs/references.md`.
- Minimal-yet-functional implementations for normalization, tokenization,
  grapheme-to-phoneme conversion, syllabification, stress assignment, pipeline
  processing and basic file I/O.
- Continuous-integration workflow covering linting, formatting, typing and test
  runs across Python 3.10–3.12, plus an automated release workflow that bumps
  versions, builds wheels/sdists and publishes to PyPI.
- Documentation updates describing rule rationale and bibliographic references,
  alongside a property-based test suite for the new components.

### Changed
- Project metadata now reads the package version from `src/furlan_g2p/__about__.py`
  via Hatch's dynamic versioning and lists the maintainer contact details.

## [0.0.1]

### Added
- Initial library skeleton with interface stubs, CLI scaffold and packaging
  configuration to explore a Friulian G2P pipeline.
