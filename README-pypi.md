# FurlanG2P

Utilities for converting Friulian (Furlan) text to phonemes. The package
includes a tiny gold lexicon with variant transcriptions, a dialect-aware
letter‑to‑sound rule engine, a configurable normalization routine, a
sentence/word tokenizer, a syllabifier with basic phonotactics, a stress
assigner aware of long vowels and accent marks, and an IPA canonicalizer that
together provide an experimental `furlang2p` command-line tool. The normalizer
spells out numbers up to 999 999 999 999 and can expand units, abbreviations and
acronyms, with rules loaded from JSON or YAML files, while the tokenizer can
skip sentence splits after configurable abbreviations.  The CLI also offers
subcommands to normalize text, output phoneme sequences and batch phonemize
metadata CSV files.

## Installation

```bash
pip install furlang2p
```

## CLI usage

Phonemise short phrases using the experimental `ipa` subcommand:

```bash
furlang2p ipa "ìsule glace"
# -> ˈizule ˈglatʃe
```

Wrap tokens in slashes or force rule-only conversion:

```bash
furlang2p ipa --with-slashes "glaç"
# -> /ˈglatʃ/

furlang2p ipa --rules-only "glaç"
# -> glatʃ
```

Use underscores as pause markers and customise the token separator:

```bash
furlang2p ipa --sep '|' _ "ìsule" __
# -> _|ˈizule|__
```

Other available subcommands:

- Normalize and expand numbers/abbreviations:

  ```bash
  furlang2p normalize "CJASE 1964 kg"
  # -> cjase mil nûfcent e sessantecuatri chilogram
  ```

- Convert a phrase to phonemes:

  ```bash
  furlang2p g2p "Cjase"
  # -> ˈc a z e
  ```

- Phonemize a metadata CSV:

  ```bash
  furlang2p phonemize-csv --in metadata.csv --out out.csv
  ```

The repository also ships a convenience script providing the same batch
conversion:

```bash
python scripts/generate_phonemes.py --in metadata.csv --out out.csv
```

All subcommands validate inputs and emit clear error messages for missing
files or conflicting arguments.

## Python usage

The same components can be invoked programmatically:

```python
from furlan_g2p.g2p.lexicon import Lexicon
from furlan_g2p.g2p.rule_engine import RuleEngine
from furlan_g2p.phonology import canonicalize_ipa

lex = Lexicon.load_seed()
rules = RuleEngine()
word = "glaç"
ipa = lex.get(word) or canonicalize_ipa(rules.convert(word))
print(ipa)
# -> ˈglatʃ
```

## Project links

- Source code and issue tracker: https://github.com/daurmax/FurlanG2P
- Bibliography and references: https://github.com/daurmax/FurlanG2P/blob/main/docs/references.md
