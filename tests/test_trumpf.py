from pyschieber.trumpf import Trumpf


def test_trumpf_count():
    assert len(Trumpf) == 6 + 1
