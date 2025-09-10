# FurlanG2P

Tools and library code for converting Friulian (Furlan) text to phonemes.  The
repository includes a small gold lexicon with IPA variants, a dialect-aware
letter‑to‑sound rule engine backed by a curated phoneme inventory, a
configurable normalization routine, a sentence/word tokenizer with abbreviation
handling, a syllabifier with basic Friulian phonotactics, a stress assigner that
accounts for long vowels and marked accents, and an IPA canonicalizer. The
normalizer can spell out numbers up to 999 999 999 999 and expand units,
abbreviations and acronyms, with rules loadable from JSON or YAML files. These
pieces back an experimental `furlang2p` CLI. Other parts of the pipeline—full
G2P services and several CLI commands—remain placeholders that raise
`NotImplementedError`.

## Project layout

- `src/furlan_g2p/cli/` – command-line interface entry points.
- `src/furlan_g2p/g2p/` – lexicon, rules and simple converters.
- `src/furlan_g2p/normalization/` – configurable text normalizer.
- `src/furlan_g2p/tokenization/` – sentence and word tokenizer.
- `src/furlan_g2p/phonology/` – canonical IPA helpers, syllabifier and stress
  assigner.
- `examples/` – sample inputs and outputs.
- `docs/` – supplementary documentation and bibliography.
- `scripts/` – helper scripts (future automation).
- `tests/` – minimal tests covering the implemented pieces and stubs.

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

### Loading normalizer configuration

Normalization rules can be customised via external JSON or YAML files. A helper
utility loads the file into a :class:`NormalizerConfig` dataclass:

```python
from furlan_g2p.config import load_normalizer_config
from furlan_g2p.normalization.normalizer import Normalizer

cfg = load_normalizer_config("norm_rules.yml")
norm = Normalizer(cfg)
print(norm.normalize("1964 kg"))
# -> mil nûfcent e sessantecuatri chilogram
```

### Loading tokenizer configuration

Sentence splitting can be customised by listing abbreviations that should not
end a sentence.  The list is read from JSON or YAML into a
``TokenizerConfig``:

```python
from furlan_g2p.config import load_tokenizer_config
from furlan_g2p.tokenization import Tokenizer

cfg = load_tokenizer_config("tok_rules.yml")  # {"abbrev_no_split": ["sig"]}
tok = Tokenizer(cfg)
print(tok.split_sentences("Al è rivât il Sig. Bepo. O ven?"))
# -> ['Al è rivât il Sig. Bepo.', 'O ven?']
```

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
