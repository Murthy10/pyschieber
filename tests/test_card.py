import pytest

from schieber.suit import Suit

from schieber.card import Card, from_string_to_card, from_card_to_tuple, from_tuple_to_card, from_string_to_tuple, \
    from_tuple_to_string


@pytest.fixture(scope='module')
def card_string():
    return '<ROSE:6>'


@pytest.fixture(scope='module')
def card():
    return Card(suit=Suit.ROSE, value=6)


@pytest.fixture(scope='module')
def card_tuple():
    return 0, 0


def test_card_str(card, card_string):
    assert str(card) == card_string


def test_from_string_to_card(card, card_string):
    assert card == from_string_to_card(card_string)


def test_from_card_to_tuple(card, card_tuple):
    assert card_tuple == from_card_to_tuple(card)


def test_from_tuple_to_card(card, card_tuple):
    assert card == from_tuple_to_card(card_tuple)


def test_from_string_to_tuple(card_tuple, card_string):
    assert card_tuple == from_string_to_tuple(card_string)


def test_from_tuple_to_string(card_tuple, card_string):
    assert card_string == from_tuple_to_string(card_tuple)


def test_from_string_not_card(card):
    rose_7 = Card(suit=Suit.ROSE, value=7)
    assert card != from_string_to_card(str(rose_7))
