"""Basic integration tests for the minimal pipeline implementation."""

from __future__ import annotations

from furlan_g2p.g2p.phonemizer import G2PPhonemizer
from furlan_g2p.normalization.normalizer import Normalizer
from furlan_g2p.phonology.stress import StressAssigner
from furlan_g2p.phonology.syllabifier import Syllabifier
from furlan_g2p.services.io_service import IOService
from furlan_g2p.services.pipeline import PipelineService
from furlan_g2p.tokenization.tokenizer import Tokenizer


def test_normalizer_basic() -> None:
    norm = Normalizer()
    assert norm.normalize("  Bêle  CJASE  ") == "bêle cjase"


def test_tokenizer_basic() -> None:
    tok = Tokenizer()
    assert tok.split_sentences("A. B!") == ["A.", "B!"]
    assert tok.split_words("Bêle cjase!") == ["bêle", "cjase"]


def test_g2p_basic() -> None:
    g2p = G2PPhonemizer()
    assert g2p.to_phonemes(["cjase"]) == ["c", "a", "z", "e"]


def test_phonology_basic() -> None:
    syll = Syllabifier()
    syllables = syll.syllabify(["c", "a", "z", "e"])
    assert syllables == [["c", "a"], ["z", "e"]]
    stress = StressAssigner()
    assert stress.assign_stress(syllables) == [["ˈc", "a"], ["z", "e"]]


def test_pipeline_basic() -> None:
    pipe = PipelineService()
    norm, phons = pipe.process_text("Cjase")
    assert norm == "cjase"
    assert phons == ["ˈc", "a", "z", "e"]


def test_io_service(tmp_path) -> None:  # type: ignore[no-untyped-def]
    io = IOService()
    file = tmp_path / "text.txt"
    io.write_text(str(file), "hello")
    assert io.read_text(str(file)) == "hello"
