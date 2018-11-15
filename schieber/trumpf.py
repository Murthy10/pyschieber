from enum import Enum

from schieber.suit import Suit

Trumpf = Enum('Trumpf', ['OBE_ABE', 'UNDE_UFE'] + [str(suit.name) for suit in Suit] + ['SCHIEBEN'])

def get_trumpf(trumpf):
    return {
        'OBE_ABE': Trumpf.OBE_ABE,
        'UNDE_UFE': Trumpf.UNDE_UFE,
        'ROSE': Trumpf.ROSE,
        'BELL': Trumpf.BELL,
        'ACORN': Trumpf.ACORN,
        'SHIELD': Trumpf.SHIELD,
    }[trumpf]