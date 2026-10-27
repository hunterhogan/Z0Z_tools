from humpy_cytoolz import get_in
from humpy_cytoolz.utils import raises


def test_get_in_doctest():
    assert raises(KeyError, lambda: get_in(['y'], {}, no_default=True))
