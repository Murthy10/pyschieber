import pytest

from pyschieber.stich import stich_rules
from pyschieber.trumpf import Trumpf


def test_stich_obe_abe(players, played_cards):
    stich = stich_rules[Trumpf.OBE_ABE](played_cards=played_cards)
    assert stich.player is players[2]


def test_stich_unde_ufe(players, played_cards):
    stich = stich_rules[Trumpf.UNDE_UFE](played_cards=played_cards)
    assert stich.player is players[3]
