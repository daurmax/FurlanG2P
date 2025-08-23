# FurlanG2P

Friulian (Furlan) G2P library. This repository aims for a maintainable, test-driven path: start with a tiny gold lexicon (citable IPA) and a minimal, explicit ruleset; evolve toward full normalization, tokenization, G2P, and phonology.

## Status

- ✅ Packaged seed lexicon with gold IPA.
- ✅ Minimal rules: circumflex length; `ç`, `ce/ci` → `t͡ʃ`; `cj` → `c`; intervocalic `s` → `z`; basic `c/ch`, `g/gh`.
- ⏳ CLI and pipeline remain unimplemented stubs (by design for now).

## References

Authoritative grammar/orthography (ARLeF):
- **GRAFIE** (official orthography, cj/gj, c~ç, long vowels with circumflex): https://arlef.it/app/uploads/documenti/Grafie_cuadrileng%C3%A2l_ed2017.pdf
- **Dut par furlan – Lezione 7** (when to write circumflex; patterns like `pôc`, `côr`): https://arlef.it/app/uploads/2020/12/dutparfurlan_lez-7-ita-def.pdf

Overview of long vowels and dialectal diphthongization:
- Wikipedia (Friulian language): https://en.wikipedia.org/wiki/Friulian_language

Quick alphabet/pronunciation overview:
- Omniglot: https://www.omniglot.com/writing/friulian.htm

Gold IPA sources (Wiktionary) are embedded in `src/furlan_g2p/data/seed_lexicon.tsv` and cited in tests.

