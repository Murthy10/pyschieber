import pytest

from pyschieber.trumpf import Trumpf


def test_trumpf_count():
    print(list(Trumpf))
    assert len(Trumpf) == 6
