"""Smoke tests for the experimental rule engine.

These are *not* gold pronunciations; they merely check that individual
orthographic contexts map to the expected IPA segments.
"""

import pytest

from furlan_g2p.g2p.rule_engine import RuleEngine


@pytest.fixture(scope="module")
def eng() -> RuleEngine:
    return RuleEngine()


def test_intervocalic_s_and_ss(eng: RuleEngine) -> None:
    assert eng.convert("asa") == "/aza/"
    assert eng.convert("assa") == "/asa/"


def test_ce_ci_and_c_elsewhere(eng: RuleEngine) -> None:
    assert eng.convert("ce") == "/t͡ʃe/"
    assert eng.convert("ci") == "/t͡ʃi/"
    assert eng.convert("ca") == "/ka/"


def test_cedilla(eng: RuleEngine) -> None:
    assert eng.convert("ça") == "/t͡ʃa/"


def test_cj_and_gj(eng: RuleEngine) -> None:
    assert eng.convert("cjala") == "/cala/"
    assert eng.convert("gjala") == "/ɟala/"
