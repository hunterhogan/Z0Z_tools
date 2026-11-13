"""Expected values and exceptions come from the targets' docstrings unless a comment names another basis."""
from __future__ import annotations

from functools import partial
from humpy_cytoolz.functoolz import (
	apply, complement, compose, compose_left, curry, do, excepts, flip, identity, juxt, memoize, pipe, return_none, thread_first, thread_last)
from humpy_cytoolz.tests import assertEqualTo, messageTestFailure
from humpy_cytoolz.tests.dataSamples.callables import addCurried, isEven, keyIgnoresKeywords, scaleSum
from hypothesis import given, strategies
from operator import add, itemgetter, mul, neg
from typing import TYPE_CHECKING
import pickle
import pytest

if TYPE_CHECKING:
	from collections.abc import Callable, Sequence
	from hunterMakesPy import CallableFunction
	from typing import Any

increment: Callable[[int], int] = (1).__add__
double: Callable[[int], int] = (2).__mul__

@pytest.mark.parametrize('x', (13, 'NE', None, [], object), ids=('13', 'NE', 'None', 'listEmpty', 'object'))
def test_identity(x: object) -> None:
	assert identity(x) is x, messageTestFailure(identity(x), x, identity.__name__, x)

@pytest.mark.parametrize('func_and_args, kwargs, expected', (
	pytest.param((double, 5), {}, 10, id='double-5'),
	pytest.param((dict,), {'N': 0}, {'N': 0}, id='dict-keywords'),
))
def test_apply(func_and_args: tuple[Any, ...], kwargs: dict[str, Any], expected: Any) -> None:
	assertEqualTo(apply(*func_and_args, **kwargs), expected, apply.__name__, *func_and_args, **kwargs)

def test_applyError() -> None:
	with pytest.raises(TypeError, match='func argument is required'):
		apply()  # pyright: ignore[reportCallIssue] # ty: ignore[missing-argument]

@pytest.mark.parametrize('val, forms, expected', (
	pytest.param(1, (increment, double), 4, id='increment-double'),
	pytest.param(1, ((add, 4), (pow, 2)), 25, id='add4-pow2'),
))
def test_thread_first(val: Any, forms: tuple[Any, ...], expected: Any) -> None:
	assertEqualTo(thread_first(val, *forms), expected, thread_first.__name__, val, *forms)

@pytest.mark.parametrize('val, forms, expected', (
	pytest.param(1, (increment, double), 4, id='increment-double'),
	pytest.param(1, ((add, 4), (pow, 2)), 32, id='add4-pow2'),
	pytest.param([1, 2, 3], ((map, increment), (filter, isEven), list), [2, 4], id='mapIncrement-filterIsEven'),
))
def test_thread_last(val: Any, forms: tuple[Any, ...], expected: Any) -> None:
	assertEqualTo(thread_last(val, *forms), expected, thread_last.__name__, val, *forms)

@pytest.mark.parametrize('funcs, args, expected', (
	pytest.param((str, increment), (3,), '4', id='str-increment'),
	# Reference: `compose(f, g, h)(x, y)` is `f(g(h(x, y)))`.
	pytest.param((str, neg, add), (3, 5), '-8', id='str-neg-add'),
))
def test_compose(funcs: tuple[Callable[..., Any], ...], args: tuple[Any, ...], expected: Any) -> None:
	assertEqualTo(compose(*funcs)(*args), expected, compose.__name__, *funcs)

@pytest.mark.parametrize('funcs, args, expected', (
	pytest.param((increment, str), (3,), '4', id='increment-str'),
	pytest.param((add, neg, str), (3, 5), '-8', id='add-neg-str'),
))
def test_compose_left(funcs: tuple[Callable[..., Any], ...], args: tuple[Any, ...], expected: Any) -> None:
	assertEqualTo(compose_left(*funcs)(*args), expected, compose_left.__name__, *funcs)

def test_pipe() -> None:
	assertEqualTo(pipe(3, double, str), '6', pipe.__name__, 3, double, str)

# Reference: the docstring: with no functions, `compose` returns the identity function.
@pytest.mark.parametrize('function', (compose, compose_left))
def test_composeEmpty(function: CallableFunction[..., Any]) -> None:
	assert function() is identity, messageTestFailure(function(), identity, function.__name__)

# Relation: `pipe(data, *funcs)` is `compose_left(*funcs)(data)`, which is `compose(*reversed(funcs))(data)`.
@given(data=strategies.integers(-89, 89), funcs=strategies.lists(strategies.sampled_from((increment, double, neg, abs)), min_size=1, max_size=5))
def test_pipeGenerated(data: int, funcs: list[Callable[[int], int]]) -> None:
	assertEqualTo((pipe(data, *funcs), compose_left(*funcs)(data)), (compose(*reversed(funcs))(data), compose(*reversed(funcs))(data)), pipe.__name__, data, *funcs)

# Reference: upstream toolz's test suite, for the metadata of a composition.
@pytest.mark.parametrize('attribute, expected', (
	pytest.param('__name__', 'str_of_abs', id='name'),
	pytest.param('__doc__', 'lambda *args, **kwargs: str(abs(*args, **kwargs))', id='doc'),
	pytest.param('__wrapped__', abs, id='wrapped'),
))
def test_composeMetadata(attribute: str, expected: Any) -> None:
	assertEqualTo(getattr(compose(str, abs), attribute), expected, compose.__name__, str, abs)

# Relation: compositions of the same functions are equal and hash equally; `compose_left` reverses the order of `compose`.
def test_composeEquality() -> None:
	assertEqualTo((compose(str, abs) == compose_left(abs, str), hash(compose(str, abs)) == hash(compose_left(abs, str)), compose(str, abs) == compose(abs, str))
		, (True, True, False), compose.__name__, str, abs)

@pytest.mark.parametrize('x, expected', (pytest.param(2, False, id='2'), pytest.param(3, True, id='3')))
def test_complement(x: int, expected: bool) -> None:
	assert complement(isEven)(x) is expected, messageTestFailure(complement(isEven)(x), expected, complement.__name__, isEven)

@pytest.mark.parametrize('funcs', (
	pytest.param((increment, double), id='positional'),
	pytest.param(([increment, double],), id='list'),
	# Reference: upstream toolz's test suite: any iterable of functions.
	pytest.param(((increment, double),), id='tuple'),
))
def test_juxt(funcs: tuple[Any, ...]) -> None:
	assertEqualTo(juxt(*funcs)(10), (11, 20), juxt.__name__, *funcs)

# Reference: upstream toolz's test suite: keyword arguments reach every function.
def test_juxtKeywords() -> None:
	assertEqualTo(juxt(dict, dict)(N=0), ({'N': 0}, {'N': 0}), juxt.__name__, dict, dict)  # pyright: ignore[reportCallIssue, reportUnknownArgumentType]

def test_do() -> None:
	log: list[object] = []
	x: object = object()
	assertEqualTo((do(log.append, x) is x, log), (True, [x]), do.__name__, log.append, x)

@pytest.mark.parametrize('args, expected', (
	pytest.param((int.__floordiv__, 2, 6), 3, id='floordiv-2-6'),
	pytest.param((isinstance, int, 1), True, id='isinstance-int-1'),
))
def test_flip(args: tuple[Any, ...], expected: Any) -> None:
	assertEqualTo(flip(*args), expected, flip.__name__, *args)

# Reference: the docstring states that `flip` is curried.
def test_flipCurried() -> None:
	assertEqualTo(flip(int.__floordiv__, 2)(4), 2, flip.__name__, int.__floordiv__, 2)

# The handler receives the exception, so `type` as the handler returns the class of the exception it caught. `return_none`
# is the documented default handler.
@pytest.mark.parametrize('exc, func, handler, x, expected', (
	pytest.param(ValueError, [1, 2].index, type, 1, 0, id='ValueError-index-1'),
	pytest.param(ValueError, [1, 2].index, type, 3, ValueError, id='ValueError-index-3'),
	pytest.param((IndexError, KeyError), itemgetter(0), return_none, [], None, id='IndexErrorKeyError-listEmpty'),
	pytest.param((IndexError, KeyError), itemgetter(0), return_none, [1], 1, id='IndexErrorKeyError-list1'),
	pytest.param((IndexError, KeyError), itemgetter(0), return_none, {}, None, id='IndexErrorKeyError-dictionaryEmpty'),
	pytest.param((IndexError, KeyError), itemgetter(0), return_none, {0: 1}, 1, id='IndexErrorKeyError-dictionary0'),
))
def test_excepts(exc: type[Exception] | tuple[type[Exception], ...], func: Callable[[Any], Any], handler: Callable[[Exception], Any], x: Any, expected: Any) -> None:
	assertEqualTo(excepts(exc, func, handler)(x), expected, excepts.__qualname__, exc, func, handler)

# Reference: upstream toolz's test suite, for the name of the wrapper.
@pytest.mark.parametrize('exc, expected', (
	pytest.param(ValueError, 'int_excepting_ValueError', id='ValueError'),
	pytest.param((ValueError, KeyError), 'int_excepting_ValueError_or_KeyError', id='ValueErrorKeyError'),
))
def test_exceptsName(exc: type[Exception] | tuple[type[Exception], ...], expected: str) -> None:
	assertEqualTo(excepts(exc, int).__name__, expected, excepts.__qualname__, exc, int)

# Reference: "Use the `cache` keyword to provide a dict-like object as an initial cache": a cached result answers without a
# call. A unary function keys its cache by its argument; other functions key it by the tuple of arguments, or by `key`.
@pytest.mark.parametrize('func, cache, key, args, expected', (
	pytest.param(abs, {-3: 13}, None, (-3,), 13, id='abs-unary'),
	pytest.param(add, {(1, 2): 13}, None, (1, 2), 13, id='add-tuple'),
	pytest.param(scaleSum, {(1, 2): 13}, keyIgnoresKeywords, (1, 2), 13, id='scaleSum-keyIgnoresKeywords'),
	pytest.param(add, {}, None, (1, 2), 3, id='add-cacheEmpty'),
))
def test_memoize(func: Callable[..., Any], cache: dict[Any, Any], key: Callable[..., Any] | None, args: tuple[Any, ...], expected: Any) -> None:
	assertEqualTo(memoize(func, cache=dict(cache), key=key)(*args), expected, memoize.__name__, func, cache, key)

# Relation: the first call stores its result in `cache` under the key that the call's arguments determine.
def test_memoizeStores() -> None:
	cache: dict[Any, Any] = {}
	memoize(add, cache=cache)(1, 2)
	assertEqualTo(cache, {(1, 2): 3}, memoize.__name__, add, cache)

# Reference: upstream toolz's test suite, for the metadata of the wrapper.
@pytest.mark.parametrize('attribute, expected', (
	pytest.param('__name__', 'scaleSum', id='name'),
	pytest.param('__doc__', scaleSum.__doc__, id='doc'),
	pytest.param('__wrapped__', scaleSum, id='wrapped'),
))
def test_memoizeMetadata(attribute: str, expected: Any) -> None:
	assertEqualTo(getattr(memoize(scaleSum), attribute), expected, memoize.__name__, scaleSum)

@pytest.mark.parametrize('args, kwargs, argsCall, kwargsCall, expected', (
	pytest.param((mul,), {}, (2, 10), {}, 20, id='mul-2-10'),
	pytest.param((scaleSum,), {'a': 1}, (2, 3), {}, 5, id='scaleSum-a1'),
	pytest.param((scaleSum, 2), {}, (3,), {'a': 1}, 5, id='scaleSum-2-a1'),
	pytest.param((scaleSum, 2, 3), {}, (), {}, 50, id='scaleSum-2-3'),
))
def test_curry(args: tuple[Any, ...], kwargs: dict[str, Any], argsCall: tuple[Any, ...], kwargsCall: dict[str, Any], expected: Any) -> None:
	assertEqualTo(curry(*args, **kwargs)(*argsCall, **kwargsCall), expected, curry.__name__, *args, **kwargs)

# Relation: while a required parameter lacks an argument, supplying the arguments in several calls returns what supplying
# them in one call returns. `scaleSum` requires `x` and `y`.
@pytest.mark.parametrize('argsFirst, argsSecond', (
	pytest.param((2,), (3, 7), id='1Then2'),
	pytest.param((2,), (3,), id='1Then1'),
	pytest.param((), (2, 3), id='0Then2'),
))
def test_curryPartial(argsFirst: tuple[int, ...], argsSecond: tuple[int, ...]) -> None:
	assertEqualTo(curry(scaleSum)(*argsFirst)(*argsSecond), scaleSum(*argsFirst, *argsSecond), curry.__name__, scaleSum)

# Reference: upstream toolz's test suite: currying a curried function or a `functools.partial` flattens to one layer;
# `keywords` is a `dict`, as it is for `functools.partial`.
@pytest.mark.parametrize('func, expected', (
	pytest.param(curry(scaleSum, 2), (scaleSum, (2, 3), dict[str, int]()), id='curry'),
	pytest.param(partial(scaleSum, 2, a=1), (scaleSum, (2, 3), dict[str, int](a=1)), id='partial'),
))
def test_curryFlattens(func: Callable[..., Any], expected: tuple[Any, ...]) -> None:
	curried: curry[..., Any] = curry(func, 3)
	assertEqualTo((curried.func, curried.args, curried.keywords), expected, curry.__name__, func, 3)

# Reference: upstream toolz's test suite: a curried function carries the metadata of the function it curries.
@pytest.mark.parametrize('attribute, expected', (
	pytest.param('__name__', 'scaleSum', id='name'),
	pytest.param('__qualname__', 'scaleSum', id='qualname'),
	pytest.param('__module__', 'humpy_cytoolz.tests.dataSamples.callables', id='module'),
	pytest.param('__doc__', scaleSum.__doc__, id='doc'),
))
def test_curryMetadata(attribute: str, expected: Any) -> None:
	assertEqualTo(getattr(curry(scaleSum), attribute), expected, curry.__name__, scaleSum)

# Relation: curried functions are equal, and hash equally, exactly when their functions and arguments are equal.
def test_curryEquality() -> None:
	assertEqualTo((curry(add, 1) == curry(add, 1), hash(curry(add, 1)) == hash(curry(add, 1)), curry(add, 1) == curry(add, 2), curry(add, 1) == curry(mul, 1))
		, (True, True, False, False), curry.__name__, add, 1)

# Reference: upstream toolz's test suite: `bind` adds arguments to a new curried function, and `call` calls without currying.
def test_curryBindCall() -> None:
	assertEqualTo((curry(add).bind(1)(2), curry(add).call(1, 2), curry(add, 1).call(2)), (3, 3, 3), curry.__name__, add)

# Reference: upstream toolz's test suite: a genuine `TypeError` from complete arguments propagates instead of currying.
@pytest.mark.parametrize('args, expected, match', (
	pytest.param((), TypeError, 'takes at least 2 arguments', id='funcAbsent'),
	pytest.param((1,), TypeError, 'Input must be callable', id='funcNotCallable'),
))
def test_curryError(args: tuple[Any, ...], expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		curry(*args)

def test_curryCallError() -> None:
	with pytest.raises(TypeError, match='unsupported operand'):
		curry(add)(1, 'N')

# Relation: unpickling a pickled function object returns an object that answers as the original does. `pickle` stores a
# function by its qualified name, so every function here is importable.
@pytest.mark.parametrize('protocol', (0, 1, 2, 3, 4, 5))
@pytest.mark.parametrize('function, args, expected', (
	pytest.param(curry(add, 1), (2,), 3, id='curryAdd1'),
	pytest.param(compose(str, abs), (-3,), '3', id='composeStrAbs'),
	pytest.param(juxt(abs, str), (-3,), (3, '-3'), id='juxtAbsStr'),
	pytest.param(complement(isEven), (3,), True, id='complementIsEven'),
	pytest.param(flip(pow), (2, 3), 9, id='flipPow'),
	pytest.param(curry(scaleSum, a=1), (2, 3), 5, id='curryScaleSumA1'),
))
def test_pickleRoundTrip(function: Callable[..., Any], args: Sequence[Any], protocol: int, expected: Any) -> None:
	assertEqualTo(pickle.loads(pickle.dumps(function, protocol))(*args), expected, 'pickle.loads(pickle.dumps(...))', function, protocol)

# Reference: upstream toolz's test suite: a module-level function that `curry` decorates unpickles as the same object.
@pytest.mark.parametrize('protocol', (0, 1, 2, 3, 4, 5))
def test_pickleCurriedDecorated(protocol: int) -> None:
	assert pickle.loads(pickle.dumps(addCurried, protocol)) is addCurried, messageTestFailure(pickle.loads(pickle.dumps(addCurried, protocol)), addCurried, 'pickle.loads(pickle.dumps(...))', addCurried, protocol)

# Reference: upstream toolz's test suite: `None` where a callable belongs raises `TypeError`, never `SystemError`.
@pytest.mark.parametrize('callNone, expected, match', (
	pytest.param(partial(apply, None), TypeError, "'NoneType' object is not callable", id='apply'),  # pyright: ignore[reportArgumentType] # ty: ignore[invalid-argument-type]
	pytest.param(complement(None), TypeError, "'NoneType' object is not callable", id='complement'),  # pyright: ignore[reportArgumentType] # ty: ignore[invalid-argument-type]
	pytest.param(compose(None, None), TypeError, "'NoneType' object is not callable", id='compose'),  # pyright: ignore[reportArgumentType, reportCallIssue, reportUnknownArgumentType] # ty: ignore[no-matching-overload]
	pytest.param(partial(curry, None), TypeError, 'Input must be callable', id='curry'),  # pyright: ignore[reportCallIssue, reportUnknownArgumentType]
	pytest.param(partial(do, None, 1), TypeError, "'NoneType' object is not callable", id='do'),  # pyright: ignore[reportArgumentType] # ty: ignore[invalid-argument-type]
	pytest.param(partial(juxt, None), TypeError, "'NoneType' object is not iterable", id='juxt'),  # pyright: ignore[reportCallIssue, reportUnknownArgumentType]
	pytest.param(partial(pipe, 1, None), TypeError, "'NoneType' object is not callable", id='pipe'),  # pyright: ignore[reportCallIssue, reportUnknownArgumentType] # ty: ignore[too-many-positional-arguments]
))
def test_functoolzNone(callNone: Callable[[], Any], expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		callNone()
