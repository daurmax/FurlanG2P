from __future__ import annotations

import json
from pathlib import Path

from furlan_g2p.lexicon import DialectAwareLexicon, LexiconConfig, LexiconEntry


def test_lookup_prefers_dialect_specific_entry() -> None:
    lexicon = DialectAwareLexicon(
        [
            LexiconEntry(lemma="cjase", ipa="ˈcaze", dialect=None, source="seed"),
            LexiconEntry(lemma="cjase", ipa="ˈca:ze", dialect="western", source="manual"),
        ],
        config=LexiconConfig(default_dialect="western"),
    )

    assert lexicon.lookup_ipa("cjase", dialect="western") == "ˈca:ze"


def test_lookup_falls_back_to_universal() -> None:
    lexicon = DialectAwareLexicon(
        [LexiconEntry(lemma="cjase", ipa="ˈcaze", dialect=None, source="seed")],
        config=LexiconConfig(fallback_to_universal=True),
    )

    assert lexicon.lookup_ipa("cjase", dialect="central") == "ˈcaze"


def test_lookup_without_fallback_returns_none() -> None:
    lexicon = DialectAwareLexicon(
        [LexiconEntry(lemma="cjase", ipa="ˈcaze", dialect=None, source="seed")],
        config=LexiconConfig(fallback_to_universal=False),
    )

    assert lexicon.lookup("cjase", dialect="central") is None


def test_lookup_is_case_insensitive_by_default() -> None:
    lexicon = DialectAwareLexicon([LexiconEntry(lemma="Cjase", ipa="ˈcaze", source="seed")])
    assert lexicon.lookup_ipa("cjase") == "ˈcaze"
    assert lexicon.lookup_ipa("CJASE") == "ˈcaze"


def test_lookup_case_sensitive_mode() -> None:
    lexicon = DialectAwareLexicon(
        [LexiconEntry(lemma="Cjase", ipa="ˈcaze", source="seed")],
        config=LexiconConfig(case_sensitive=True),
    )
    assert lexicon.lookup_ipa("Cjase") == "ˈcaze"
    assert lexicon.lookup_ipa("cjase") is None


def test_lookup_lru_cache_registers_hits() -> None:
    lexicon = DialectAwareLexicon([LexiconEntry(lemma="cjase", ipa="ˈcaze", source="seed")])

    before = lexicon._lookup_cached.cache_info()
    lexicon.lookup("cjase")
    lexicon.lookup("cjase")
    after = lexicon._lookup_cached.cache_info()

    assert after.hits >= before.hits + 1
    assert after.currsize >= before.currsize


def test_stats_generation_counts_sources_and_dialects() -> None:
    lexicon = DialectAwareLexicon(
        [
            LexiconEntry(lemma="cjase", ipa="ˈcaze", source="seed"),
            LexiconEntry(lemma="aghe", ipa="ˈaɡe", dialect="central", source="manual"),
            LexiconEntry(lemma="aghe", ipa="ˈaʒe", dialect="central", source="manual"),
        ]
    )

    stats = lexicon.stats()
    assert stats["total_entries"] == 2
    assert stats["total_lemmas"] == 2
    assert stats["entries_by_source"] == {"seed": 1, "manual": 1}
    assert stats["entries_by_dialect"] == {"universal": 1, "central": 1}
    assert stats["entries_with_alternatives"] == 1


def test_get_alternatives_respects_return_alternatives_flag() -> None:
    entries = [
        LexiconEntry(lemma="cjase", ipa="ˈcaze", dialect=None, source="seed"),
        LexiconEntry(lemma="cjase", ipa="ˈca:ze", dialect="western", source="manual"),
    ]
    plain = DialectAwareLexicon(entries, config=LexiconConfig(return_alternatives=False))
    rich = DialectAwareLexicon(entries, config=LexiconConfig(return_alternatives=True))

    assert plain.get_alternatives("cjase") == []
    assert set(rich.get_alternatives("cjase")) == {"ˈca:ze"}


def test_from_path_supports_jsonl_and_legacy_tsv(tmp_path: Path) -> None:
    jsonl_path = tmp_path / "lexicon.jsonl"
    jsonl_path.write_text(
        json.dumps({"lemma": "cjase", "ipa": "ˈcaze", "source": "manual"}) + "\n",
        encoding="utf-8",
    )
    jsonl_lex = DialectAwareLexicon.from_path(jsonl_path)
    assert jsonl_lex.lookup_ipa("cjase") == "ˈcaze"

    legacy_tsv = tmp_path / "legacy.tsv"
    legacy_tsv.write_text(
        "\n".join(
            [
                "word\tipa\tvariants_json\tsource",
                'aghe\tˈaɡe\t["ˈaʒe"]\tseed',
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    tsv_lex = DialectAwareLexicon.from_path(legacy_tsv)
    assert tsv_lex.lookup_ipa("aghe") == "ˈage"
    assert tsv_lex.get_alternatives("aghe") == ["ˈaʒe"]
