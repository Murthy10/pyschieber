import pytest

from pyschieber.card import Card
from pyschieber.suit import Suit
from pyschieber.player.challenge_player.strategy.mode.trumpf_color_mode import TrumpfColorMode


@pytest.mark.parametrize("suit, cards, score", [
    (Suit.ROSE,
     [Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 11), Card(Suit.BELL, 8), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)],
     15),
    (Suit.ROSE,
     [Card(Suit.BELL, 14), Card(Suit.BELL, 12), Card(Suit.BELL, 9), Card(Suit.BELL, 8), Card(Suit.BELL, 6),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)],
     19),
    (Suit.ROSE,
     [Card(Suit.BELL, 14), Card(Suit.BELL, 11), Card(Suit.BELL, 9), Card(Suit.ACORN, 12), Card(Suit.ACORN, 6),
      Card(Suit.ACORN, 7), Card(Suit.ROSE, 11), Card(Suit.ROSE, 7), Card(Suit.ROSE, 9)],
     59),
    (Suit.ROSE,
     [Card(Suit.BELL, 11), Card(Suit.BELL, 9), Card(Suit.BELL, 6), Card(Suit.ACORN, 14), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 7), Card(Suit.ROSE, 14), Card(Suit.ROSE, 7), Card(Suit.ROSE, 9)],
     41),
    (Suit.ROSE,
     [Card(Suit.BELL, 14), Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 10), Card(Suit.BELL, 6),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)],
     36),
    (Suit.ROSE,
     [Card(Suit.BELL, 6), Card(Suit.BELL, 7), Card(Suit.BELL, 8), Card(Suit.BELL, 10), Card(Suit.ACORN, 6),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)],
     24),

    (Suit.BELL,
     [Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 11), Card(Suit.BELL, 8), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)],
     60),
    (Suit.BELL,
     [Card(Suit.BELL, 14), Card(Suit.BELL, 12), Card(Suit.BELL, 9), Card(Suit.BELL, 8), Card(Suit.BELL, 6),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)],
     57),
    (Suit.BELL,
     [Card(Suit.BELL, 14), Card(Suit.BELL, 11), Card(Suit.BELL, 9), Card(Suit.ACORN, 12), Card(Suit.ACORN, 6),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)],
     57),
    (Suit.BELL,
     [Card(Suit.BELL, 11), Card(Suit.BELL, 9), Card(Suit.BELL, 6), Card(Suit.ACORN, 14), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)],
     63),
    (Suit.BELL,
     [Card(Suit.BELL, 14), Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 10), Card(Suit.BELL, 6),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.SHIELD, 13), Card(Suit.ROSE, 12)],
     60),
    (Suit.BELL,
     [Card(Suit.BELL, 6), Card(Suit.BELL, 7), Card(Suit.BELL, 8), Card(Suit.BELL, 10), Card(Suit.ACORN, 6),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)],
     44),

    (Suit.ACORN,
     [Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 11), Card(Suit.BELL, 8), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)],
     40),
    (Suit.ACORN,
     [Card(Suit.BELL, 14), Card(Suit.BELL, 12), Card(Suit.BELL, 9), Card(Suit.BELL, 8), Card(Suit.BELL, 6),
      Card(Suit.ACORN, 9), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ACORN, 11)],
     49),
    (Suit.ACORN,
     [Card(Suit.BELL, 14), Card(Suit.BELL, 12), Card(Suit.BELL, 13), Card(Suit.ROSE, 12), Card(Suit.ACORN, 6),
      Card(Suit.ACORN, 12), Card(Suit.ACORN, 14), Card(Suit.ACORN, 13), Card(Suit.ROSE, 9)],
     54),
    (Suit.ACORN,
     [Card(Suit.BELL, 11), Card(Suit.BELL, 9), Card(Suit.BELL, 6), Card(Suit.ACORN, 14), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)],
     36),
    (Suit.ACORN,
     [Card(Suit.BELL, 14), Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 10), Card(Suit.BELL, 6),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)],
     26),
    (Suit.ACORN,
     [Card(Suit.BELL, 6), Card(Suit.BELL, 7), Card(Suit.BELL, 8), Card(Suit.BELL, 10), Card(Suit.ACORN, 6),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)],
     24),

    (Suit.SHIELD,
     [Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 11), Card(Suit.BELL, 8), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)],
     20),
    (Suit.SHIELD,
     [Card(Suit.BELL, 14), Card(Suit.BELL, 12), Card(Suit.BELL, 9), Card(Suit.BELL, 8), Card(Suit.BELL, 6),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)],
     24),
    (Suit.SHIELD,
     [Card(Suit.BELL, 14), Card(Suit.BELL, 11), Card(Suit.BELL, 9), Card(Suit.ACORN, 12), Card(Suit.ACORN, 6),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 11), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)],
     44),
    (Suit.SHIELD,
     [Card(Suit.BELL, 11), Card(Suit.BELL, 9), Card(Suit.BELL, 6), Card(Suit.ACORN, 14), Card(Suit.ACORN, 13),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)],
     30),
    (Suit.SHIELD,
     [Card(Suit.BELL, 14), Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 10), Card(Suit.BELL, 6),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 11), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)],
     42),
    (Suit.SHIELD,
     [Card(Suit.BELL, 6), Card(Suit.BELL, 7), Card(Suit.BELL, 8), Card(Suit.BELL, 10), Card(Suit.ACORN, 6),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)],
     12),
])
def test_calculate_score_trumpf_colors(suit, cards, score):
    tcm = TrumpfColorMode(suit)
    s = tcm.calculate_mode_score(cards, geschoben=False)
    assert s == score


@pytest.mark.parametrize("suit, cards, highest, lowest", [
    (Suit.ROSE,
     [Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 11), Card(Suit.BELL, 8), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)],
     Card(Suit.ROSE, 9), Card(Suit.SHIELD, 7)),
    (Suit.ROSE,
     [Card(Suit.BELL, 14), Card(Suit.BELL, 12), Card(Suit.BELL, 9), Card(Suit.BELL, 8), Card(Suit.BELL, 6),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.ROSE, 9)],
     Card(Suit.ROSE, 9), Card(Suit.BELL, 6)),
    (Suit.ROSE,
     [Card(Suit.BELL, 14), Card(Suit.BELL, 11), Card(Suit.BELL, 9), Card(Suit.ACORN, 12), Card(Suit.ACORN, 6),
      Card(Suit.ACORN, 7), Card(Suit.ROSE, 11), Card(Suit.ROSE, 7), Card(Suit.ROSE, 9)],
     Card(Suit.ROSE, 11), Card(Suit.ACORN, 6)),
    (Suit.ROSE,
     [Card(Suit.BELL, 11), Card(Suit.BELL, 9), Card(Suit.BELL, 6), Card(Suit.ACORN, 14), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 7), Card(Suit.ROSE, 14), Card(Suit.ROSE, 7), Card(Suit.ROSE, 9)],
     Card(Suit.ROSE, 9), Card(Suit.BELL, 6)),
    (Suit.ROSE,
     [Card(Suit.BELL, 14), Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 10), Card(Suit.BELL, 6),
     Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)],
     Card(Suit.ROSE, 13), Card(Suit.BELL, 6)),
    (Suit.ROSE,
     [Card(Suit.BELL, 6), Card(Suit.BELL, 7), Card(Suit.BELL, 8), Card(Suit.BELL, 10), Card(Suit.ACORN, 8),
      Card(Suit.ACORN, 7), Card(Suit.SHIELD, 14), Card(Suit.ROSE, 13), Card(Suit.ROSE, 12)],
     Card(Suit.ROSE, 13), Card(Suit.BELL, 6)),
])
def test_sort_by_rank_trumpf_colors(suit, cards, lowest, highest):
    tcm = TrumpfColorMode(suit)
    sorted = tcm.sort_by_rank(cards)
    assert sorted[-1] == lowest and sorted[0] == highest


@pytest.mark.parametrize("suit, cards, has_only_jack", [
    (Suit.ROSE,
     [Card(Suit.BELL, 13), Card(Suit.BELL, 12), Card(Suit.BELL, 11), Card(Suit.BELL, 8), Card(Suit.ACORN, 12),
      Card(Suit.ACORN, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.SHIELD, 9)],
     False),
    (Suit.ROSE,
     [Card(Suit.BELL, 14), Card(Suit.BELL, 12), Card(Suit.BELL, 9), Card(Suit.BELL, 8), Card(Suit.BELL, 6),
      Card(Suit.ROSE, 11), Card(Suit.SHIELD, 12), Card(Suit.SHIELD, 7), Card(Suit.SHIELD, 9)],
     True),
    (Suit.ROSE,
     [Card(Suit.BELL, 14), Card(Suit.BELL, 11), Card(Suit.BELL, 9), Card(Suit.ACORN, 12), Card(Suit.ACORN, 6),
      Card(Suit.ACORN, 7), Card(Suit.ROSE, 11), Card(Suit.ROSE, 7), Card(Suit.ROSE, 9)],
     False),
])
def test_has_only_jack_trumpf_colors(suit, cards, has_only_jack):
    tcm = TrumpfColorMode(suit)
    assert has_only_jack == tcm.has_only_jack_of_trumpf(cards)
