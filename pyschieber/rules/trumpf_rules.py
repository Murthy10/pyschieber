from pyschieber.trumpf import Trumpf


def trumpf_allowed(chosen_trumpf, geschoben):
    return not (chosen_trumpf == Trumpf.SCHIEBEN and geschoben)
