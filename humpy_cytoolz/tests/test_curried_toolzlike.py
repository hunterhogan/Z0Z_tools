from .dev_skip_test import dev_skip_test
import humpy_cytoolz
import humpy_cytoolz.curried
import types

@dev_skip_test
def test_toolzcurry_is_class():
    import humpy_toolz
    assert isinstance(humpy_toolz.curry, type) is True
    assert isinstance(humpy_toolz.curry, types.FunctionType) is False

@dev_skip_test
def test_cytoolz_like_toolz():
    import humpy_toolz
    import humpy_toolz.curried
    for key, val in vars(humpy_toolz.curried).items():
        if isinstance(val, humpy_toolz.curry):
            if val.func is humpy_toolz.curry:
                continue
            assert hasattr(humpy_cytoolz.curried, key), 'cytoolz.curried.%s does not exist' % key
            assert isinstance(getattr(humpy_cytoolz.curried, key), humpy_cytoolz.curry), 'cytoolz.curried.%s should be curried' % key

@dev_skip_test
def test_toolz_like_cytoolz():
    import humpy_toolz
    import humpy_toolz.curried
    for key, val in vars(humpy_cytoolz.curried).items():
        if isinstance(val, humpy_cytoolz.curry):
            assert hasattr(humpy_toolz.curried, key), 'cytoolz.curried.%s should not exist' % key
            assert isinstance(getattr(humpy_toolz.curried, key), humpy_toolz.curry), 'cytoolz.curried.%s should not be curried' % key
