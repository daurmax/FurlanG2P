# FurlanG2P

FurlanG2P is a Friulian (Furlan) text-to-phoneme toolkit with a hybrid G2P
design:
- lexicon lookup first,
- deterministic rules fallback,
- optional ML exception-model interface (`[ml]` extra).

It ships as both a Python library and a `furlang2p` CLI.

## Features

- Text normalization with configurable unit/abbreviation/number expansion.
- Sentence and word tokenization with abbreviation-aware sentence splitting.
- Dialect-aware lexicon lookup (`central`, `western`, `carnic`) with universal
  fallback.
- Deterministic orthography-to-IPA rules with inventory validation.
- Lexicon lifecycle tools: build, inspect, export, validate.
- Evaluation metrics and reporting: WER, PER, stress accuracy.
- Coverage analysis (`lexicon`, `rule_only`, `oov`) for word lists.
- Optional ML interface for exception handling without adding ML deps to base
  installs.

## Project layout

- `src/furlan_g2p/cli/` CLI command definitions.
- `src/furlan_g2p/g2p/` runtime phonemizer, rules, and legacy-compatible lexicon adapter.
- `src/furlan_g2p/lexicon/` schema, storage, builder, canonicalizer, and dialect-aware lookup.
- `src/furlan_g2p/evaluation/` evaluation result types and metrics.
- `src/furlan_g2p/ml/` optional exception-model interfaces and null implementation.
- `src/furlan_g2p/normalization/` text normalizer.
- `src/furlan_g2p/tokenization/` sentence/word tokenization.
- `src/furlan_g2p/phonology/` IPA canonicalization, syllabifier, stress assigner.
- `src/furlan_g2p/services/` pipeline orchestration and file I/O helpers.
- `docs/` architecture, business logic, usage, changelog, references.
- `tests/` pytest suites (CLI + module-level checks).

Core docs:
- [Architecture](docs/architecture.md)
- [Business Logic](docs/business_logic.md)
- [Usage Guide](docs/usage.md)
- [References](docs/references.md)

## Installation

Base install:

```bash
pip install -e .
```

Contributor/dev install:

```bash
pip install -e ".[dev]"
```

Optional ML dependencies:

```bash
pip install -e ".[ml]"
```

## Quick start

```bash
furlang2p ipa "ìsule glace"
furlang2p normalize "CJASE 1964 kg"
furlang2p g2p "Cjase"
```

Lexicon workflow:

```bash
furlang2p lexicon build source.tsv --output lexicon.jsonl --source-type tsv
furlang2p lexicon info lexicon.jsonl
furlang2p lexicon export lexicon.jsonl lexicon.tsv --format tsv
furlang2p lexicon validate lexicon.jsonl --strict
```

Evaluation and coverage:

```bash
furlang2p evaluate gold.tsv --verbose
furlang2p coverage words.txt --show-oov
```

Batch phonemization:

```bash
furlang2p phonemize-csv --in metadata.csv --out out.csv
python scripts/generate_phonemes.py --in metadata.csv --out out.csv
```

## Python API

```python
from furlan_g2p.services import PipelineService

pipe = PipelineService(default_dialect="central")
norm, phonemes = pipe.process_text("Cjase")
print(norm)
print(phonemes)
```

Config loading examples are documented in [docs/usage.md](docs/usage.md).

## Build distributions

```bash
python -m build
```

## Development checks

Run before opening a PR:

```bash
ruff check .
black --check .
mypy .
pytest
```

Useful focused commands for hybrid G2P updates:

```bash
pytest tests/test_cli_lexicon.py tests/test_cli_evaluate_coverage.py
pytest tests/test_pipeline_golden.py tests/test_lexicon_gold.py
```

## CI/CD

Workflows live under `.github/workflows/`:
- `ci.yml` runs lint/type/tests on push and pull request.
- `release.yml` builds/publishes releases to PyPI.

## Sources of truth

- Friulian orthography/phonology references in [docs/references.md](docs/references.md).
- Algorithmic behavior in [docs/business_logic.md](docs/business_logic.md).
- Module interactions in [docs/architecture.md](docs/architecture.md).

## Changelog

Release history is maintained in [docs/changelog.md](docs/changelog.md).

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](LICENSE).
