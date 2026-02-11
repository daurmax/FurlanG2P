# FurlanG2P

FurlanG2P converts Friulian (Furlan) text to phonemes using a hybrid approach:
- lexicon lookup first,
- deterministic rules fallback,
- optional ML exception interface (`[ml]` extra).

It provides the `furlang2p` CLI and reusable Python APIs.

## Installation

Base package:

```bash
pip install furlang2p
```

With optional ML dependencies:

```bash
pip install "furlang2p[ml]"
```

## Quick CLI examples

```bash
furlang2p ipa "ìsule glace"
furlang2p normalize "CJASE 1964 kg"
furlang2p g2p "Cjase"
furlang2p phonemize-csv --in metadata.csv --out out.csv
```

Lexicon, evaluation, and coverage workflows:

```bash
furlang2p lexicon build source.tsv --output lexicon.jsonl --source-type tsv
furlang2p lexicon info lexicon.jsonl
furlang2p evaluate gold.tsv --verbose
furlang2p coverage words.txt --show-oov
```

## Python API

```python
from furlan_g2p.services import PipelineService

pipe = PipelineService(default_dialect="central")
norm, phonemes = pipe.process_text("Cjase")
print(norm)
print(" ".join(phonemes))
```

## Links

- Source code and issues: https://github.com/daurmax/FurlanG2P
- Changelog: https://github.com/daurmax/FurlanG2P/blob/main/docs/changelog.md
- References: https://github.com/daurmax/FurlanG2P/blob/main/docs/references.md

## License

Creative Commons Attribution-NonCommercial 4.0 International:
https://github.com/daurmax/FurlanG2P/blob/main/LICENSE
