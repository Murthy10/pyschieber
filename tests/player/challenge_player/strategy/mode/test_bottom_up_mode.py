import pytest

from schieber.card import Card
from schieber.suit import Suit
from schieber.player.challenge_player.strategy.mode.bottom_up_mode import BottomUpMode


@pytest.fixture
def bum():
    return BottomUpMode()

@pytest.mark.parametrize("cards, score", [
    ([Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 11), Card(Suit.BELL, 8), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)], 0),
    ([Card(Suit.BELL, 14), Card(Suit.BELL, 12), Card(Suit.BELL, 9), Card(Suit.BELL, 8), Card(Suit.BELL, 6),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)], 13),
    ([Card(Suit.BELL, 14), Card(Suit.BELL, 11), Card(Suit.BELL, 9), Card(Suit.ACORN, 12), Card(Suit.ACORN, 6),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)], 26),
    ([Card(Suit.BELL, 11), Card(Suit.BELL, 9), Card(Suit.BELL, 6), Card(Suit.ACORN, 13), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)], 13),
    ([Card(Suit.BELL, 14), Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 10), Card(Suit.BELL, 6),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 13), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)], 13),
    ([Card(Suit.BELL, 6), Card(Suit.BELL, 7), Card(Suit.BELL, 8), Card(Suit.BELL, 10), Card(Suit.ACORN, 6),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)], 75),
])
def test_calculate_score_bottom_up(bum, cards, score):
    s = bum.calculate_mode_score(cards, geschoben=False)
    assert s == score


@pytest.mark.parametrize("cards, lowest, highest", [
    ([Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 11), Card(Suit.BELL, 8), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)], Card(Suit.BELL, 13), [Card(Suit.SHIELD, 7)]),
    ([Card(Suit.BELL, 14), Card(Suit.BELL, 12), Card(Suit.BELL, 9), Card(Suit.BELL, 8), Card(Suit.BELL, 6),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)], Card(Suit.BELL, 14), [Card(Suit.BELL, 6)]),
    ([Card(Suit.BELL, 14), Card(Suit.BELL, 11), Card(Suit.BELL, 9), Card(Suit.ACORN, 12), Card(Suit.ACORN, 6),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)], Card(Suit.BELL, 14), [Card(Suit.ACORN, 6)]),
    ([Card(Suit.BELL, 11), Card(Suit.BELL, 9), Card(Suit.BELL, 6), Card(Suit.ACORN, 13), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)], Card(Suit.SHIELD, 14), [Card(Suit.BELL, 6)]),
    ([Card(Suit.BELL, 14), Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 10), Card(Suit.BELL, 6),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 13), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)], Card(Suit.BELL, 14), [Card(Suit.BELL, 6)]),
    ([Card(Suit.BELL, 6), Card(Suit.BELL, 7), Card(Suit.BELL, 8), Card(Suit.BELL, 10), Card(Suit.ACORN, 6),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)], Card(Suit.SHIELD, 14), [Card(Suit.ACORN, 6), Card(Suit.BELL, 6)]),
])
def test_sort_by_rank_bottom_up(bum, cards, lowest, highest):
    sorted = bum.sort_by_rank(cards)
    assert sorted[-1] == lowest and sorted[0] in highest