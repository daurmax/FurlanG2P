# FurlanG2P

Tools and library code for converting Friulian (Furlan) text to phonemes. The
project ships a small gold lexicon and a rule-based engine that together provide
an experimental ``ipa`` command-line tool. Other pieces of the pipeline – text
normalisation, tokenisation, full G2P and phonology – are present as skeletons
and currently raise ``NotImplementedError``.

## Installation

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

2. Install the project:

   ```bash
   pip install -e .
   ```

3. (Optional) Add development tools for linting, typing and tests:

   ```bash
   pip install -e .[dev]
   ```

## Usage

The package exposes a ``furlang2p`` CLI. At present only the experimental
``ipa`` subcommand does real work; the ``normalize``, ``g2p`` and
``phonemize-csv`` commands are stubs that abort with ``NotImplementedError``.

Phonemise short phrases via the seed lexicon with rule-based fallback:

```bash
furlang2p ipa ìsule glace
# -> ˈi.zu.le ˈɡlat͡ʃe
```

Wrap each token in ``/slashes/`` or force rule-based conversion:

```bash
furlang2p ipa --with-slashes glaç
furlang2p ipa --rules-only glaç
```

Underscores act as short/long pause markers and the ``--sep`` option controls
output token separation:

```bash
furlang2p ipa --sep '|' _ ìsule __
# -> _|ˈi.zu.le|__
```

See ``furlang2p ipa --help`` for full details.

## Development

Run the following checks before committing code:

```bash
isort .
black .
ruff check .
mypy src
pytest -q
```

## VS Code integration

A ``.vscode/tasks.json`` file provides shortcuts for common actions:

- **Install dependencies** – ``pip install -e .[dev]``
- **Format** – run ``isort`` and ``black``
- **Lint** – run ``ruff``
- **Type check** – run ``mypy`` on ``src``
- **Test** – execute ``pytest -q``

From VS Code press ``Ctrl+Shift+B`` or run *Tasks: Run Task* from the Command
Palette and choose the desired action.

## References

Authoritative grammar/orthography (ARLeF):

- **GRAFIE** (official orthography, cj/gj, c~ç, long vowels with circumflex): https://arlef.it/app/uploads/documenti/Grafie_cuadrileng%C3%A2l_ed2017.pdf
- **Dut par furlan – Lezione 7** (when to write circumflex; patterns like ``pôc``, ``côr``): https://arlef.it/app/uploads/2020/12/dutparfurlan_lez-7-ita-def.pdf

Overview of long vowels and dialectal diphthongisation:

- Wikipedia (Friulian language): https://en.wikipedia.org/wiki/Friulian_language

Quick alphabet/pronunciation overview:

- Omniglot: https://www.omniglot.com/writing/friulian.htm

Gold IPA sources (Wiktionary) are embedded in ``src/furlan_g2p/data/seed_lexicon.tsv`` and cited in tests.

## Contributing

Pull requests that flesh out the skeleton or expand test coverage are welcome.
Please open an issue to discuss major changes.
