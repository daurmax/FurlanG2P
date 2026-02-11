from __future__ import annotations

from dataclasses import asdict

import pytest

from furlan_g2p.lexicon import LexiconConfig, LexiconEntry


def test_lexicon_entry_creation_with_all_fields() -> None:
    entry = LexiconEntry(
        lemma="cjase",
        ipa="ˈcaze",
        dialect="central",
        source="manual",
        confidence=0.75,
        frequency=42,
        alternatives=["ˈkjaze"],
    )

    assert entry.lemma == "cjase"
    assert entry.ipa == "ˈcaze"
    assert entry.dialect == "central"
    assert entry.source == "manual"
    assert entry.confidence == pytest.approx(0.75)
    assert entry.frequency == 42
    assert entry.alternatives == ["ˈkjaze"]
    assert entry.stress_marked is True


def test_lexicon_entry_defaults() -> None:
    entry = LexiconEntry(lemma="aghe", ipa="aɡe")
    assert entry.dialect is None
    assert entry.source == "unknown"
    assert entry.confidence == pytest.approx(1.0)
    assert entry.frequency is None
    assert entry.alternatives == []
    assert entry.stress_marked is False


def test_lexicon_config_defaults() -> None:
    config = LexiconConfig()
    assert config.default_dialect is None
    assert config.fallback_to_universal is True
    assert config.case_sensitive is False
    assert config.return_alternatives is False


@pytest.mark.parametrize("confidence", [-0.01, 1.01])
def test_lexicon_entry_rejects_confidence_out_of_range(confidence: float) -> None:
    with pytest.raises(ValueError, match="confidence must be in"):
        LexiconEntry(lemma="cjase", ipa="ˈcaze", confidence=confidence)


def test_lexicon_entry_rejects_invalid_dialect() -> None:
    with pytest.raises(ValueError, match="Invalid dialect"):
        LexiconEntry(lemma="cjase", ipa="ˈcaze", dialect="north")


def test_lexicon_entry_rejects_negative_frequency() -> None:
    with pytest.raises(ValueError, match="frequency must be non-negative"):
        LexiconEntry(lemma="cjase", ipa="ˈcaze", frequency=-1)


def test_lexicon_entry_serialization_round_trip() -> None:
    original = LexiconEntry(
        lemma="cjase",
        ipa="ˈcaze",
        dialect="western",
        source="wikipron",
        confidence=0.85,
        frequency=12,
        alternatives=["ˈca:ze", "ˈcjaze"],
    )

    payload = asdict(original)
    restored = LexiconEntry(**payload)

    assert restored == original
    assert restored.alternatives == ["ˈca:ze", "ˈcjaze"]


def test_lexicon_entry_accepts_non_list_alternatives() -> None:
    entry = LexiconEntry(lemma="cjase", ipa="ˈcaze", alternatives=("ˈkjaze",))
    assert isinstance(entry.alternatives, list)
    assert entry.alternatives == ["ˈkjaze"]


def test_lexicon_config_rejects_invalid_default_dialect() -> None:
    with pytest.raises(ValueError, match="Invalid default_dialect"):
        LexiconConfig(default_dialect="north")
