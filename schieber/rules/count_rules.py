from schieber.trumpf import Trumpf

counting_factor = {Trumpf.ROSE: 1, Trumpf.ACORN: 1, Trumpf.BELL: 2,  Trumpf.SHIELD: 2, Trumpf.OBE_ABE: 3,
                   Trumpf.UNDE_UFE: 3}

points_obe_abe = {6: 0, 7: 0, 8: 8, 9: 0, 10: 10, 11: 2, 12: 3, 13: 4, 14: 11}
points_unde_ufe = {6: 11, 7: 0, 8: 8, 9: 0, 10: 10, 11: 2, 12: 3, 13: 4, 14: 0}
points_trumpf_color = {6: 0, 7: 0, 8: 0, 9: 14, 10: 10, 11: 20, 12: 3, 13: 4, 14: 11}
points_non_trumpf_color = {6: 0, 7: 0, 8: 0, 9: 0, 10: 10, 11: 2, 12: 3, 13: 4, 14: 11}

card_points = {Trumpf.OBE_ABE: points_obe_abe, Trumpf.UNDE_UFE: points_unde_ufe}

for trumpf in filter(lambda x: x != Trumpf.OBE_ABE and x != Trumpf.UNDE_UFE and x != Trumpf.SCHIEBEN, Trumpf):
    card_points[trumpf] = points_trumpf_color


def count_stich(cards, trumpf, last=False):
    """
    Counts the points of a stich based on the rules of Jassen
    :param cards:
    :param trumpf:
    :param last:
    :return:
    """
    points = 0 if not last else 5
    for card in cards:
        if trumpf == Trumpf.OBE_ABE or trumpf == Trumpf.UNDE_UFE or card.suit.name == trumpf.name:
            points += card_points[trumpf][card.value]
        else:
            points += points_non_trumpf_color[card.value]
    return points
