import pytest

from schieber.card import Card
from schieber.suit import Suit
from schieber.trumpf import Trumpf
from schieber.player.challenge_player.strategy.jass_strategy import JassStrategy
from schieber.player.challenge_player.challenge_player import ChallengePlayer


@pytest.fixture
def js():
    p = ChallengePlayer()
    p.id = 0
    return JassStrategy(p)

@pytest.mark.parametrize("cards, trumpf", [
    ([Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 11), Card(Suit.BELL, 8), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)], Trumpf.BELL),
    ([Card(Suit.BELL, 14), Card(Suit.BELL, 13), Card(Suit.BELL, 9), Card(Suit.ACORN, 8), Card(Suit.ACORN, 6),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)], Trumpf.ACORN),
    ([Card(Suit.BELL, 14), Card(Suit.BELL, 11), Card(Suit.ACORN, 9), Card(Suit.SHIELD, 13), Card(Suit.SHIELD, 12),
      Card(Suit.SHIELD, 10), Card(Suit.SHIELD, 8), Card(Suit.SHIELD, 9), Card(Suit.SHIELD, 6)], Trumpf.SHIELD),
    ([Card(Suit.BELL, 12), Card(Suit.BELL, 9), Card(Suit.BELL, 6), Card(Suit.ACORN, 14), Card(Suit.ROSE, 12),
      Card(Suit.ROSE, 7), Card(Suit.ROSE, 6), Card(Suit.ROSE, 14), Card(Suit.ROSE, 9)], Trumpf.ROSE),
    ([Card(Suit.BELL, 14), Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 10), Card(Suit.BELL, 6),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)], Trumpf.OBE_ABE),
    ([Card(Suit.BELL, 6), Card(Suit.BELL, 7), Card(Suit.BELL, 8), Card(Suit.BELL, 10), Card(Suit.ACORN, 6),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)], Trumpf.UNDE_UFE),
    ([Card(Suit.BELL, 6), Card(Suit.BELL, 7), Card(Suit.BELL, 9), Card(Suit.ACORN, 10), Card(Suit.ACORN, 8),
      Card(Suit.SHIELD, 7), Card(Suit.SHIELD, 10), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)], Trumpf.SCHIEBEN),
])
def test_calculate_score_top_down(js, cards, trumpf):
    t = js.chose_trumpf(cards, geschoben=False)
    assert t == trumpf
