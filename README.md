# FurlanG2P

Tools and library code for converting Friulian (Furlan) text to phonemes. The
project currently ships a small gold lexicon and a rule-based engine that powers
an experimental `furlang2p` CLI. Other components—text normalisation,
tokenisation, full G2P and phonology—are placeholders that raise
`NotImplementedError`.

## Project layout

- `src/furlan_g2p/` – Python package with modules for normalisation,
  tokenisation, G2P and phonology.
- `examples/` – sample inputs and outputs.
- `scripts/` – helper scripts (future automation).
- `docs/` – supplementary documentation and bibliography.
- `tests/` – minimal tests ensuring modules import and stubs raise
  `NotImplementedError`.

## Building

The project uses [Hatchling](https://hatch.pypa.io/) as build backend.
Create source and wheel distributions with:

```bash
python -m build
```

For local development install the package in editable mode along with
optional tooling:

```bash
pip install -e .[dev]
```

## Testing

Before submitting changes, run the quality and test suite:

```bash
ruff check .
black --check .
mypy .
pytest
```

## References

FurlanG2P follows published descriptions of Friulian orthography and
phonology as well as lemma-level IPA transcriptions. A curated bibliography is
available in [docs/references.md](docs/references.md); consult it when modifying
rules, lexicon entries or phonological behaviour.

## Contributing

Pull requests that flesh out the skeleton or expand test coverage are welcome.
Please open an issue to discuss major changes.
