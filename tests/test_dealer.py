import pytest

from pyschieber.player.random_player import RandomPlayer

from pyschieber.dealer import Dealer


@pytest.fixture(scope="module")
def players():
    return [RandomPlayer(name='Tick'), RandomPlayer(name='Trick'), RandomPlayer(name='Track'),
            RandomPlayer(name='Dagobert')]


def test_deal_cards(players):
    dealer = Dealer(players=players)
    dealer.deal_cards()
    for player in players:
        assert len(player.cards) == 9


def test_shuffle_cards(players):
    dealer = Dealer(players=players)
    card = dealer.deck.cards[0]
    dealer.shuffle_cards()
    assert dealer.deck.cards[0] != card


def test_dealer_deck_count(players):
    dealer = Dealer(players=players)
    assert len(dealer.deck.cards) == 36
