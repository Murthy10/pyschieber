import pytest

from pyschieber.stich import stich_rules
from pyschieber.trumpf import Trumpf


@pytest.mark.parametrize("trumpf, index,", [
    (Trumpf.OBE_ABE, 2),
    (Trumpf.UNDE_UFE, 3),
    (Trumpf.BELL, 3),
    (Trumpf.ACORN, 1),
])
def test_stich(trumpf, index, players, played_cards):
    stich = stich_rules[trumpf](played_cards=played_cards)
    assert stich.player is players[index]
