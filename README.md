# FurlanG2P

Tools and library code for converting Friulian (Furlan) text to phonemes.
The repository includes a small gold lexicon, a rule-based orthography to IPA
converter, a normalization routine, syllabifier and stress assigner. These
pieces back an experimental `furlang2p` CLI. Other parts of the pipeline—
tokenisation, full G2P services and several CLI commands—remain placeholders
that raise `NotImplementedError`.

## Project layout

- `src/furlan_g2p/cli/` – command-line interface entry points.
- `src/furlan_g2p/g2p/` – lexicon, rules and simple converters.
- `src/furlan_g2p/normalization/` – experimental text normalizer.
- `src/furlan_g2p/phonology/` – canonical IPA helpers, syllabifier and stress
  assigner.
- `examples/` – sample inputs and outputs.
- `docs/` – supplementary documentation and bibliography.
- `scripts/` – helper scripts (future automation).
- `tests/` – minimal tests covering the implemented pieces and stubs.

See [docs/project_structure.md](docs/project_structure.md) for a full module
overview and development roadmap.

## Business logic overview

The project is organised into focused modules:

- **Normalization** – lowercases text and collapses whitespace. *TODO:* load
  rule sets from configuration and expand coverage for numbers and acronyms.
- **Tokenization** – regex-based sentence and word splitter. *TODO:* handle
  abbreviations and preserve pause markers.
- **G2P** – small lexicon with rule-based fallback to generate IPA strings.
  *TODO:* implement the `PhonemeRules` engine and grow the lexicon.
- **Phonology** – IPA canonicalization, syllabifier and stress assigner.
  *TODO:* refine syllabification and stress rules.
- **Services** – pipeline and file I/O helpers. *TODO:* expose dependency
  injection and batch utilities.
- **CLI** – user-facing commands; only `ipa` is functional. *TODO:* implement
  `normalize`, `g2p` and `phonemize-csv` subcommands.

## Quick local run (how to launch the CLI and test phrases)

1. Create and activate a virtual environment:

   - macOS / Linux:
     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```
   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - Windows (cmd.exe):
     ```
     python -m venv .venv
     .\.venv\Scripts\activate
     ```

2. Install the package in editable mode so the `furlang2p` console script becomes available:

   ```bash
   pip install -e .
   ```

3. Run the CLI and test short phrases (examples):

   - Basic phonemize using the seed lexicon with rule fallback:
     ```bash
     furlang2p ipa "ìsule glace"
     # -> ˈizule ˈglatʃe
     ```

   - Wrap each token in slashes:
     ```bash
     furlang2p ipa --with-slashes "glaç"
     # -> /ˈglatʃ/
     ```

   - Force rule-based conversion (skip lexicon lookup):
     ```bash
     furlang2p ipa --rules-only "glaç"
     # -> glatʃ
     ```

   - Use underscores as pause markers and change token separator:
     ```bash
     furlang2p ipa --sep '|' _ "ìsule" __
     # -> _|ˈizule|__
     ```

   Notes:
   - Quotes around the phrase are recommended to preserve spacing and punctuation.
   - The CLI is experimental; some commands (`normalize`, `g2p`, `phonemize-csv`) are stubs that raise `NotImplementedError`.

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

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](LICENSE).
