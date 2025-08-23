from __future__ import annotations

import csv
from importlib import resources


def test_seed_lexicon_tsv_is_well_formed() -> None:
    with resources.files("furlan_g2p.data").joinpath("seed_lexicon.tsv").open(
        "r", encoding="utf-8"
    ) as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = list(reader)
    assert rows, "seed_lexicon.tsv is empty"
    required = {"word", "ipa", "variants_json", "source"}
    assert required.issubset(reader.fieldnames or set())
    # no duplicates by lowercase key
    keys = [r["word"].lower() for r in rows]
    assert len(keys) == len(set(keys)), "duplicate entries detected"

