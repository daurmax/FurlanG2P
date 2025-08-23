FurlanG2P

FurlanG2P is a library-first skeleton for building a grapheme-to-phoneme (G2P) and text normalization toolkit, designed for TTS prototyping. This repository currently ships a clean, scalable structure with interfaces, services, and a CLI scaffold — domain logic is intentionally unimplemented and should be filled in later.

Features (skeleton)

- src/ layout, Python ≥ 3.10
- Clear module boundaries (core, normalization, tokenization, g2p, phonology, services, cli, config)
- Public API via furlan_g2p.__init__
- CLI entrypoint: furlang2p
- Tests using pytest

Install (editable)

```bash
pip install -e ".[dev]"
```

CLI

```bash
furlang2p --help
```

Library usage

```python
from furlan_g2p import Normalizer, Tokenizer, G2PPhonemizer

# Instantiate and call methods (these raise NotImplementedError in the skeleton)
```

Contributing

Open issues and PRs are welcome.

License

MIT
