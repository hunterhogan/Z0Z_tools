from humpy_cytoolz.functoolz import curry
import operator

IGNORE = {'__abs__', '__index__', '__inv__', '__invert__', '__neg__', '__not__', '__pos__', '_abs', 'abs', 'attrgetter', 'index', 'inv', 'invert', 'is_none', 'is_not_none', 'itemgetter', 'neg', 'not_', 'pos', 'truth'}
locals().update({name: f if name in IGNORE else curry(f) for name, f in vars(operator).items() if callable(f)})
del curry
del operator
