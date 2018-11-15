import pytest

from schieber.card import Card
from schieber.player.greedy_player.trumpf_decision import choose_trumpf, TrumpfType
from schieber.suit import Suit
from schieber.trumpf import Trumpf


@pytest.mark.parametrize("cards, trumpf, trumpf_type", [
    ([Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 11), Card(Suit.BELL, 8), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)], Trumpf.BELL,
     TrumpfType.UNDER_4),
    ([Card(Suit.BELL, 14), Card(Suit.BELL, 12), Card(Suit.BELL, 9), Card(Suit.BELL, 8), Card(Suit.BELL, 6),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)], Trumpf.BELL,
     TrumpfType.NELL_ASS_5),
    ([Card(Suit.BELL, 14), Card(Suit.BELL, 11), Card(Suit.BELL, 9), Card(Suit.ACORN, 12), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)], Trumpf.BELL,
     TrumpfType.UNDER_NELL_ASS),
    ([Card(Suit.BELL, 11), Card(Suit.BELL, 9), Card(Suit.BELL, 6), Card(Suit.ACORN, 14), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)], Trumpf.BELL,
     TrumpfType.UNDER_NELL_3_2_ASS),
    ([Card(Suit.BELL, 14), Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 10), Card(Suit.BELL, 6),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)], Trumpf.OBE_ABE,
     TrumpfType.STICHE_5),
    ([Card(Suit.BELL, 6), Card(Suit.BELL, 7), Card(Suit.BELL, 8), Card(Suit.BELL, 10), Card(Suit.ACORN, 6),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)], Trumpf.UNDE_UFE,
     TrumpfType.STICHE_5),
])
def test_choose_trumpf_no_schieben(cards, trumpf, trumpf_type):
    evaluate_trumpf, evaluate_trumpf_type = choose_trumpf(cards=cards, geschoben=False)
    assert (evaluate_trumpf, evaluate_trumpf_type) == (trumpf, trumpf_type)


@pytest.mark.parametrize("cards, trumpf, trumpf_type", [
    ([Card(Suit.BELL, 10), Card(Suit.BELL, 12), Card(Suit.BELL, 6), Card(Suit.BELL, 8), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)], Trumpf.ACORN,
     TrumpfType.HAVE_TO_DECIDE),
    ([Card(Suit.BELL, 10), Card(Suit.BELL, 12), Card(Suit.BELL, 6), Card(Suit.BELL, 7), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)], Trumpf.UNDE_UFE,
     TrumpfType.HAVE_TO_DECIDE),
])
def test_choose_trumpf_schieben(cards, trumpf, trumpf_type):
    evaluate_trumpf, evaluate_trumpf_type = choose_trumpf(cards=cards, geschoben=True)
    assert (evaluate_trumpf, evaluate_trumpf_type) == (trumpf, trumpf_type)
