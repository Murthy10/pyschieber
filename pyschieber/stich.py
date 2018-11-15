from collections import namedtuple

PlayedCard = namedtuple('PlayedCard', ['player', 'card'])
Stich = namedtuple('Stich', ['player', 'played_cards', 'trumpf'])


def played_card_dict(played_card):
    """
    Returns a dictionary containing:
    - the player who played the card
    - the played card
    :param played_card:
    :return:
    """
    return {
        'player_id': played_card.player.id,
        'card': str(played_card.card)
    }


def stich_dict(stich):
    """
    Returns a dictionary of the stich containing:
    - the id of the player who is winner of the stich
    - the trumpf
    - the cards played in the stich
    :param stich:
    :return:
    """
    return {
        'player_id': stich.player.id,
        'trumpf': stich.trumpf.name,
        'played_cards': [played_card_dict(played_card) for played_card in stich.played_cards]
    }
