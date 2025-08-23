"""Property tests for the experimental rule engine."""

from hypothesis import given
from hypothesis import strategies as st

from furlan_g2p.g2p.rule_engine import RuleEngine

ALPHABET = "abcçdefghijlmnoprstuvzâêîôûàèìòù"
IPA_CHARS = set("/abcdefghijklmnopqrstuvwxyzɡɟt͡ʃʃzːˈɳɛàèìòù")


@given(st.text(alphabet=ALPHABET, min_size=1, max_size=10))
def test_outputs_are_ipa_only(s: str) -> None:
    eng = RuleEngine()
    out = eng.convert(s)
    assert all(ch in IPA_CHARS for ch in out)
