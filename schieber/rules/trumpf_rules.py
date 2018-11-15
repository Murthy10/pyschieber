from schieber.trumpf import Trumpf


def trumpf_allowed(chosen_trumpf, geschoben):
    """
    Disallows 'geschoben' when the partner already has chose 'geschoben'. All other trumpfs are always allowed.
    :param chosen_trumpf:
    :param geschoben:
    :return:
    """
    return not (chosen_trumpf == Trumpf.SCHIEBEN and geschoben)
