from enum import Enum

Wies = Enum('Wies', ['SEQUENCE_3', 'SEQUENCE_4', 'SEQUENCE_5', '4_SAME', '4_UNDER', '4_NAELL'])

points_wies = {Wies.SEQUENCE_3: 20, Wies.SEQUENCE_4: 50, Wies.SEQUENCE_5: 100, '4_NAELL': 150, '4_UNDER': 200}


# TODO: Implement Wiesen and the corresponding rules

def wies_allowed(wies, hand_cards):
    allowed = False
    if not len(wies) >= 3:
        return False
    if not set(wies) < set(hand_cards):
        return False
    return allowed
