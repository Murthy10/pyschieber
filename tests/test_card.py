import pytest

from pyschieber.suit import Suit

from pyschieber.card import Card, from_string_to_card


@pytest.fixture(scope='module')
def card_string():
    return '<ROSE:6>'


@pytest.fixture(scope='module')
def card():
    return Card(suit=Suit.ROSE, value=6)


def test_card_str(card, card_string):
    assert str(card) == card_string


def test_from_string_to_card(card, card_string):
    assert card == from_string_to_card(card_string)


def test_from_string_not_card(card):
    rose_7 = Card(suit=Suit.ROSE, value=7)
    assert card != from_string_to_card(str(rose_7))
