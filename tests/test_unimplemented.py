from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest

from furlan_g2p.g2p.lexicon import Lexicon
from furlan_g2p.g2p.phonemizer import G2PPhonemizer
from furlan_g2p.g2p.rules import PhonemeRules
from furlan_g2p.normalization.normalizer import Normalizer
from furlan_g2p.phonology.stress import StressAssigner
from furlan_g2p.phonology.syllabifier import Syllabifier
from furlan_g2p.services.pipeline import PipelineService
from furlan_g2p.tokenization.tokenizer import Tokenizer


def expect_not_impl(fn: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
    with pytest.raises(NotImplementedError):
        fn(*args, **kwargs)


def test_normalizer_unimplemented() -> None:
    n = Normalizer()
    expect_not_impl(n.normalize, "text")


def test_tokenizer_unimplemented() -> None:
    t = Tokenizer()
    expect_not_impl(t.split_sentences, "text.")
    expect_not_impl(t.split_words, "text")


def test_g2p_unimplemented() -> None:
    lex = Lexicon()
    rules = PhonemeRules()
    g2p = G2PPhonemizer(lex, rules)
    expect_not_impl(g2p.to_phonemes, ["hello"])


def test_phonology_unimplemented() -> None:
    s = Syllabifier()
    expect_not_impl(s.syllabify, ["h", "e", "l", "o"])
    a = StressAssigner()
    expect_not_impl(a.assign_stress, [["h", "e"], ["l", "o"]])


def test_pipeline_unimplemented() -> None:
    p = PipelineService()
    expect_not_impl(p.process_text, "hello world")
    expect_not_impl(p.process_csv, "in.csv", "out.csv")
