"""Expected values come from `humpy_cytoolz/curried/__init__.py`, which declares each name, unless a comment names another basis.

The namespace curries each function that takes more than one argument and re-exports each other function unchanged.
"""
from __future__ import annotations

from collections import defaultdict
from functools import partial
from humpy_cytoolz.functoolz import complement, curry
from humpy_cytoolz.tests import assertEqualTo, messageTestFailure
from operator import methodcaller
import humpy_cytoolz
import humpy_cytoolz.curried
import operator
import pytest

boxOfIdentifiersCurried: tuple[str, ...] = (
	'accumulate', 'assoc', 'assoc_in', 'cons', 'countby', 'dissoc', 'do', 'drop', 'excepts', 'filter', 'get', 'get_in', 'groupby',
	'interpose', 'isdistinct', 'itemfilter', 'itemmap', 'iterate', 'join', 'keyfilter', 'keymap', 'map', 'mapcat', 'nth', 'partial',
	'partition', 'partition_all', 'partitionby', 'peekn', 'pluck', 'random_sample', 'reduce', 'reduceby', 'remove', 'sliding_window',
	'sorted', 'tail', 'take', 'take_nth', 'topk', 'unique', 'update_in', 'valfilter', 'valmap')

boxOfIdentifiersUnchanged: tuple[str, ...] = (
	'apply', 'comp', 'complement', 'compose', 'compose_left', 'concat', 'concatv', 'count', 'curry', 'diff', 'first', 'flip',
	'frequencies', 'identity', 'interleave', 'isiterable', 'juxt', 'last', 'memoize', 'merge_sorted', 'peek', 'pipe', 'second',
	'thread_first', 'thread_last')

boxOfIdentifiersExceptions: tuple[str, ...] = ('merge', 'merge_with')
"""Functions that `humpy_cytoolz.curried.exceptions` curries through a wrapper, because their variadic signatures defeat `curry`."""

@pytest.mark.parametrize('identifier', boxOfIdentifiersCurried)
def test_curriedCurried(identifier: str) -> None:
	assertEqualTo(getattr(humpy_cytoolz.curried, identifier), curry(getattr(humpy_cytoolz, identifier)), 'humpy_cytoolz.curried', identifier)

@pytest.mark.parametrize('identifier', boxOfIdentifiersUnchanged)
def test_curriedUnchanged(identifier: str) -> None:
	assert getattr(humpy_cytoolz.curried, identifier) is getattr(humpy_cytoolz, identifier), messageTestFailure(
		getattr(humpy_cytoolz.curried, identifier), getattr(humpy_cytoolz, identifier), 'humpy_cytoolz.curried', identifier)

# Relation: the declared identifiers are every public callable in the namespace, so a new function must be declared.
def test_curriedComplete() -> None:
	assertEqualTo(sorted(humpy_cytoolz.keyfilter(complement(methodcaller('startswith', '_')), humpy_cytoolz.valfilter(callable, vars(humpy_cytoolz.curried))))
		, sorted((*boxOfIdentifiersCurried, *boxOfIdentifiersUnchanged, *boxOfIdentifiersExceptions)), 'humpy_cytoolz.curried')

# Reference: upstream toolz's test suite: the wrapped `merge` and `merge_with` curry, including through `factory` alone.
@pytest.mark.parametrize('callCurried, expected', (
	pytest.param(partial(humpy_cytoolz.curried.merge(factory=partial(defaultdict[int, int], int)), {1: 1}), defaultdict(int, {1: 1}), id='merge-factoryThenDicts'),
	pytest.param(partial(humpy_cytoolz.curried.merge, {1: 1}), {1: 1}, id='merge-dict'),
	pytest.param(partial(humpy_cytoolz.curried.merge_with(sum), {1: 1}, {1: 2}), {1: 3}, id='merge_with-sumThenDicts'),  # pyright: ignore[reportArgumentType, reportCallIssue]
	pytest.param(partial(humpy_cytoolz.curried.merge_with, sum, [{'a': 1}, {'a': 2}]), {'a': 3}, id='merge_with-sum-listOfDicts'),  # pyright: ignore[reportCallIssue] # ty: ignore[too-many-positional-arguments]
))
def test_curriedExceptions(callCurried: partial[object], expected: object) -> None:
	assertEqualTo(callCurried(), expected, 'humpy_cytoolz.curried', callCurried)

# Reference: `humpy_cytoolz/curried/operator.py` curries every callable of `operator` except the unary ones it names.
@pytest.mark.parametrize('identifier', ('add', 'contains', 'getitem', 'mul', 'pow', 'sub'))
def test_curriedOperatorCurried(identifier: str) -> None:
	assertEqualTo(getattr(humpy_cytoolz.curried.operator, identifier), curry(getattr(operator, identifier)), 'humpy_cytoolz.curried.operator', identifier)

@pytest.mark.parametrize('identifier', ('abs', 'attrgetter', 'index', 'itemgetter', 'neg', 'not_', 'truth'))
def test_curriedOperatorUnchanged(identifier: str) -> None:
	assert getattr(humpy_cytoolz.curried.operator, identifier) is getattr(operator, identifier), messageTestFailure(
		getattr(humpy_cytoolz.curried.operator, identifier), getattr(operator, identifier), 'humpy_cytoolz.curried.operator', identifier)

# Relation: a curried operator applied in two calls answers what the operator answers in one.
@pytest.mark.parametrize('identifier', ('add', 'pow', 'sub'))
def test_curriedOperatorPartial(identifier: str) -> None:
	assertEqualTo(getattr(humpy_cytoolz.curried.operator, identifier)(13)(2), getattr(operator, identifier)(13, 2), 'humpy_cytoolz.curried.operator', identifier)
