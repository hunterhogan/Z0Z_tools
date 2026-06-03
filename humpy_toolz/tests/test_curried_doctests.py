import doctest
import humpy_toolz

def test_doctests() -> None:
    humpy_toolz.__test__ = {}
    for name, func in vars(humpy_toolz).items():
        if isinstance(func, humpy_toolz.curry):
            humpy_toolz.__test__[name] = func.func
    assert doctest.testmod(humpy_toolz).failed == 0
    del humpy_toolz.__test__
