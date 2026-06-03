from .dicttoolz import *
from .functoolz import *
from .itertoolz import *
from .recipes import *
from functools import partial, reduce

__version__ = '1.1.0'
sorted = sorted
map = map
filter = filter
comp = compose
flip = functoolz.flip = curry(functoolz.flip)
memoize = functoolz.memoize = curry(functoolz.memoize)
from . import curried

functoolz._sigs.update_signature_registry()
__toolz_version__ = '1.1.0'

def __getattr__(name):
    if name == '__version__':
        from importlib.metadata import version
        rv = version('humpy_cytoolz')
        globals()[name] = rv
        return rv
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')
