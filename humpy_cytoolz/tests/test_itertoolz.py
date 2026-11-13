"""Expected values and exceptions come from the targets' docstrings, and expected types from `itertoolz.pyi`, unless a comment names another basis.

`no_default` is the documented default of every optional `default`, `initial`, and `init`, and `no_pad` of `pad`, so a parameter that passes
either one states the call without that argument.
"""
from __future__ import annotations

from collections import Counter, deque, UserList
from collections.abc import Iterator
from functools import partial, reduce
from humpy_cytoolz.dicttoolz import valmap
from humpy_cytoolz.functoolz import identity
from humpy_cytoolz.itertoolz import (
	accumulate, concat, concatv, cons, count, diff, drop, first, frequencies, get, groupby, interleave, interpose, isdistinct, isiterable,
	iterate, join, last, mapcat, merge_sorted, no_pad, nth, partition, partition_all, peek, peekn, pluck, random_sample, reduceby, remove,
	second, sliding_window, tail, take, take_nth, topk, unique)
from humpy_cytoolz.tests import assertEqualTo, messageTestFailure
from humpy_cytoolz.tests.dataSamples.callables import addToSet, isEven, pairAccumulated
from humpy_cytoolz.tests.dataSamples.equality import equalsEveryString
from humpy_cytoolz.tests.dataSamples.iterables import (
	boxOfIterablesPrimes, IterableNotSequence, IteratorRaises, messageSensorDisconnected, tuplePrimes)
from humpy_cytoolz.utils import no_default
from hypothesis import given, strategies
from operator import add, itemgetter, mul, neg, sub
from pickle import dumps, loads
from random import Random
from typing import TYPE_CHECKING
import heapq
import itertools
import more_itertools
import pytest

if TYPE_CHECKING:
	from collections.abc import Callable, Hashable, Iterable, Sequence
	from typing import Any

noDefaultUnpickled: str = loads(dumps(no_default))
"""Copy of the sentinel that is equal to `no_default` but is another object, as unpickling a curried signature produces."""

friends: list[tuple[str, str]] = [('Alice', 'Edith'), ('Alice', 'Zhao'), ('Edith', 'Alice'), ('Zhao', 'Alice'), ('Zhao', 'Edith')]
cities: list[tuple[str, str]] = [('Alice', 'NYC'), ('Alice', 'Chicago'), ('Dan', 'Sydney'), ('Edith', 'Paris'), ('Edith', 'Berlin'), ('Zhao', 'Shanghai')]
phonebook: dict[str, str] = {'Alice': '555-1234', 'Bob': '555-5678', 'Charlie': '555-9999'}

# Reference: the README states that functions with matching maintained implementations are aliases.
@pytest.mark.parametrize('alias, original', (
	pytest.param(concat, itertools.chain.from_iterable, id='concat'),
	pytest.param(concatv, itertools.chain, id='concatv'),
	pytest.param(count, more_itertools.ilen, id='count'),
	pytest.param(interpose, more_itertools.intersperse, id='interpose'),
	pytest.param(isdistinct, more_itertools.all_unique, id='isdistinct'),
	pytest.param(iterate, more_itertools.iterate, id='iterate'),
	pytest.param(merge_sorted, heapq.merge, id='merge_sorted'),
	pytest.param(remove, itertools.filterfalse, id='remove'),
	pytest.param(unique, more_itertools.unique_everseen, id='unique'),
))
def test_alias(alias: Callable[..., Any], original: Callable[..., Any]) -> None:
	assertEqualTo(alias, original, 'humpy_cytoolz.itertoolz', alias)

@pytest.mark.parametrize('binop, seq, initial, expected', (
	pytest.param(add, [1, 2, 3, 4, 5], no_default, [1, 3, 6, 10, 15], id='add-initialAbsent'),
	pytest.param(mul, [1, 2, 3, 4, 5], no_default, [1, 2, 6, 24, 120], id='mul-initialAbsent'),
	pytest.param(add, [1, 2, 3], -1, [-1, 0, 2, 5], id='add-initialNegative1'),
	pytest.param(add, [], 1, [1], id='add-seqEmpty-initial1'),
	pytest.param(add, [], no_default, [], id='add-seqEmpty-initialAbsent'),
	pytest.param(add, [1, 2, 3], noDefaultUnpickled, [1, 3, 6], id='add-noDefaultUnpickled'),
	pytest.param(pairAccumulated, [2, 3], equalsEveryString, [equalsEveryString, (equalsEveryString, 2), ((equalsEveryString, 2), 3)], id='pairAccumulated-equalsEveryString'),
))
def test_accumulate[T](binop: Callable[[T, T], T], seq: Iterable[T], initial: T, expected: list[T]) -> None:
	accumulated: Iterator[T] = accumulate(binop, seq, initial)
	assert isinstance(accumulated, Iterator), messageTestFailure(type(accumulated), Iterator, accumulate.__name__, binop, seq, initial)
	assertEqualTo([*accumulated], expected, accumulate.__name__, binop, seq, initial)

# Reference: `itertools.accumulate`, which the docstring names, with `initial` before the first item. `sub` is neither
# commutative nor associative, so agreement includes the order of the steps and of the arguments to `binop`.
@given(seq=strategies.lists(strategies.integers(-89, 89), max_size=13), initial=strategies.integers(-89, 89))
def test_accumulateGenerated(seq: list[int], initial: int) -> None:
	assertEqualTo([*accumulate(sub, seq, initial)], [*itertools.accumulate(seq, sub, initial=initial)], accumulate.__name__, sub, seq, initial)

@pytest.mark.parametrize('binop, seq, expected, match', (
	pytest.param(None, [1, 2], TypeError, "'NoneType' object is not callable", id='binopNone'),
	pytest.param(add, None, TypeError, "'NoneType' object is not iterable", id='seqNone'),
))
def test_accumulateError(binop: Callable[[int, int], int], seq: Iterable[int], expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		list(accumulate(binop, seq))

@pytest.mark.parametrize('seq', boxOfIterablesPrimes)
def test_cons(seq: Iterable[int]) -> None:
	assertEqualTo(tuple(cons(1, seq)), (1, *tuplePrimes), cons.__name__, 1, seq)

# Reference: `cons` accepts a "possibly infinite" sequence.
def test_consInfinite() -> None:
	assertEqualTo(tuple(take(3, cons('N', itertools.count(13)))), ('N', 13, 14), cons.__name__, 'N', itertools.count(13))

@pytest.mark.parametrize('seqs, default, key, expected', (
	pytest.param(([1, 2, 3], [1, 2, 10, 100]), no_default, None, [(3, 10)], id='lists-defaultAbsent'),
	pytest.param(([1, 2, 3], [1, 2, 10, 100]), None, None, [(3, 10), (None, 100)], id='lists-defaultNone'),
	pytest.param((['apples', 'bananas'], ['Apples', 'Oranges']), no_default, str.lower, [('bananas', 'Oranges')], id='fruit-lower'),
	# Reference: upstream toolz's test suite, for three sequences of three kinds, and for one list of sequences.
	pytest.param(([1, 2, 3], (1, 10, 3), IterableNotSequence((1, 2, 10))), no_default, None, [(2, 10, 2), (3, 3, 10)], id='threeKinds'),
	pytest.param(([(1, 2), (1, 3)],), no_default, None, [(2, 3)], id='listOfSequences'),
	pytest.param(([1], [1, 2]), noDefaultUnpickled, None, [], id='lists-noDefaultUnpickled'),
	pytest.param(([1], [1, 2]), equalsEveryString, None, [(equalsEveryString, 2)], id='lists-equalsEveryString'),
))
def test_diff(seqs: tuple[Iterable[Any], ...], default: Any, key: Callable[[Any], Any] | None, expected: list[tuple[Any, ...]]) -> None:
	assertEqualTo([*diff(*seqs, default=default, key=key)], expected, diff.__name__, *seqs, default=default, key=key)

# Reference: upstream toolz's test suite: fewer than two sequences raise `TypeError`.
@pytest.mark.parametrize('seqs, expected, match', (
	pytest.param((), TypeError, 'Too few sequences', id='seqsAbsent'),
	pytest.param(([[1, 2]],), TypeError, 'Too few sequences', id='listOfOneSequence'),
	pytest.param((list[int](),), TypeError, 'Too few sequences', id='listEmpty'),
	pytest.param((None,), TypeError, 'Too few sequences', id='seqNone'),
	pytest.param(([None, None],), TypeError, "'NoneType' object is not iterable", id='listOfNone'),
))
def test_diffError(seqs: tuple[Iterable[Any], ...], expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		list(diff(*seqs))

@pytest.mark.parametrize('seq', boxOfIterablesPrimes)
@pytest.mark.parametrize('n, expected', (
	pytest.param(0, tuplePrimes, id='items0'),
	pytest.param(1, (3, 5, 7, 11, 13, 17), id='items1'),
	pytest.param(3, (7, 11, 13, 17), id='items3'),
	pytest.param(7, (), id='items7'),
	pytest.param(13, (), id='items13'),
))
def test_drop(n: int, seq: Iterable[int], expected: tuple[int, ...]) -> None:
	itemsRemaining: Iterator[int] = drop(n, seq)
	assert isinstance(itemsRemaining, Iterator), messageTestFailure(type(itemsRemaining), Iterator, drop.__name__, n, seq)
	assertEqualTo(tuple(itemsRemaining), expected, drop.__name__, n, seq)

@pytest.mark.parametrize('seq', boxOfIterablesPrimes)
def test_first(seq: Iterable[int]) -> None:
	assertEqualTo(first(seq), 2, first.__name__, seq)

@pytest.mark.parametrize('seq', boxOfIterablesPrimes)
def test_second(seq: Iterable[int]) -> None:
	assertEqualTo(second(seq), 3, second.__name__, seq)

@pytest.mark.parametrize('seq', boxOfIterablesPrimes)
def test_last(seq: Iterable[int]) -> None:
	assertEqualTo(last(seq), 17, last.__name__, seq)

@pytest.mark.parametrize('seq', (
	pytest.param((2, equalsEveryString), id='tuple'),
	pytest.param(IterableNotSequence((2, equalsEveryString)), id='IterableNotSequence'),
))
def test_lastEqualsEveryString(seq: Iterable[object]) -> None:
	assert last(seq) is equalsEveryString, messageTestFailure(last(seq), equalsEveryString, last.__name__, seq)

# Reference: an empty sequence raises `IndexError` from `[-1]`; `last` raises it for every other empty iterable as well.
@pytest.mark.parametrize('seq, expected, match', (
	pytest.param((), IndexError, 'index out of range', id='tupleEmpty'),
	pytest.param(IterableNotSequence(()), IndexError, 'index out of range', id='IterableNotSequenceEmpty'),
	pytest.param(None, TypeError, "'NoneType' object is not iterable", id='seqNone'),
))
def test_lastError(seq: Iterable[int], expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		last(seq)

@pytest.mark.parametrize('seq, expected', (
	pytest.param(['cat', 'cat', 'ox', 'pig', 'pig', 'cat'], {'cat': 3, 'ox': 1, 'pig': 2}, id='animals'),
	pytest.param([], {}, id='listEmpty'),
))
def test_frequencies[T: Hashable](seq: Iterable[T], expected: dict[T, int]) -> None:
	assertEqualTo(frequencies(seq), expected, frequencies.__name__, seq)

# Reference: `collections.Counter`, which counts with its own `dict`. The docstring leaves the order of keys unspecified.
@given(seq=strategies.lists(strategies.integers(-8, 8), max_size=34))
def test_frequenciesGenerated(seq: list[int]) -> None:
	assertEqualTo(frequencies(seq), dict(Counter(seq)), frequencies.__name__, seq)

@pytest.mark.parametrize('seq, expected, match', (
	pytest.param([[13], [13]], TypeError, "unhashable type: 'list'", id='itemsUnhashable'),
	pytest.param(None, TypeError, "'NoneType' object is not iterable", id='seqNone'),
))
def test_frequenciesError(seq: Iterable[Any], expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		frequencies(seq)

@pytest.mark.parametrize('ind, seq, default, expected', (
	pytest.param(1, 'ABC', no_default, 'B', id='index1-string'),
	pytest.param([1, 2], 'ABC', no_default, ('B', 'C'), id='indices1and2-string'),
	pytest.param('Alice', phonebook, no_default, '555-1234', id='Alice-phonebook'),
	pytest.param(['Alice', 'Bob'], phonebook, no_default, ('555-1234', '555-5678'), id='AliceBob-phonebook'),
	pytest.param(['Alice', 'Dennis'], phonebook, None, ('555-1234', None), id='AliceDennis-phonebook-defaultNone'),
	# Reference: upstream toolz's test suite.
	pytest.param('foo', {}, 'bar', 'bar', id='keyAbsent-defaultBar'),
	pytest.param({}, [1, 2, 3], 'bar', 'bar', id='indexUnhashable-defaultBar'),
	pytest.param([0, 2], 'AB', 'C', ('A', 'C'), id='indices0and2-defaultC'),
	pytest.param([0], 'AB', no_default, ('A',), id='indices0'),
	pytest.param([], 'AB', no_default, (), id='indicesEmpty'),
	pytest.param(5, (), equalsEveryString, equalsEveryString, id='index5-equalsEveryString'),
	pytest.param([5], (), equalsEveryString, (equalsEveryString,), id='indices5-equalsEveryString'),
))
def test_get(ind: Any, seq: Any, default: Any, expected: Any) -> None:
	assertEqualTo(get(ind, seq, default), expected, get.__name__, ind, seq, default)

# Reference: upstream toolz's test suite: without a default, `get` raises the exception that indexing raises, message included.
@pytest.mark.parametrize('ind, seq, default, expected, match', (
	pytest.param(10, 'ABC', no_default, IndexError, 'string index out of range', id='index10-string'),
	pytest.param('Dennis', phonebook, no_default, KeyError, "'Dennis'", id='Dennis-phonebook'),
	pytest.param({}, [1, 2, 3], no_default, TypeError, 'list indices must be integers or slices, not dict', id='indexUnhashable'),
	pytest.param([1, 2, 3], 1, None, TypeError, "'int' object is not subscriptable", id='seqNotIndexable-defaultNone'),
	pytest.param('foo', {}, noDefaultUnpickled, KeyError, "'foo'", id='keyAbsent-noDefaultUnpickled'),
	pytest.param(1, None, no_default, TypeError, "'NoneType' object is not subscriptable", id='seqNone'),
	pytest.param([1, 2], None, no_default, TypeError, "'NoneType' object is not subscriptable", id='indices-seqNone'),
))
def test_getError(ind: Any, seq: Any, default: Any, expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		get(ind, seq, default)

@pytest.mark.parametrize('key, seq, expected', (
	pytest.param(len, ['Alice', 'Bob', 'Charlie', 'Dan', 'Edith', 'Frank'], {3: ['Bob', 'Dan'], 5: ['Alice', 'Edith', 'Frank'], 7: ['Charlie']}, id='len-names'),
	pytest.param(isEven, [1, 2, 3, 4, 5, 6, 7, 8], {False: [1, 3, 5, 7], True: [2, 4, 6, 8]}, id='isEven-1to8'),
	pytest.param('gender', [{'name': 'Alice', 'gender': 'F'}, {'name': 'Bob', 'gender': 'M'}, {'name': 'Charlie', 'gender': 'M'}]
		, {'F': [{'gender': 'F', 'name': 'Alice'}], 'M': [{'gender': 'M', 'name': 'Bob'}, {'gender': 'M', 'name': 'Charlie'}]}, id='gender-people'),
	# Reference: upstream toolz's test suite, for an index and a list of indices.
	pytest.param(0, [(1, 2), (1, 3), (2, 2), (2, 4)], {1: [(1, 2), (1, 3)], 2: [(2, 2), (2, 4)]}, id='index0-pairs'),
	pytest.param([0], [(1, 2), (1, 3), (2, 2), (2, 4)], {(1,): [(1, 2), (1, 3)], (2,): [(2, 2), (2, 4)]}, id='indices0-pairs'),
	pytest.param([0, 0], [(1, 2), (1, 3), (2, 2), (2, 4)], {(1, 1): [(1, 2), (1, 3)], (2, 2): [(2, 2), (2, 4)]}, id='indices0and0-pairs'),
))
def test_groupby(key: Any, seq: Iterable[Any], expected: dict[Any, list[Any]]) -> None:
	assertEqualTo(groupby(key, seq), expected, groupby.__name__, key, seq)

@pytest.mark.parametrize('key, seq, expected, match', (
	pytest.param(list, [(13,), (17,)], TypeError, "unhashable type: 'list'", id='keysUnhashable'),
	pytest.param(None, [1, 2], TypeError, "'int' object is not subscriptable", id='keyNone'),
	pytest.param(isEven, None, TypeError, "'NoneType' object is not iterable", id='seqNone'),
))
def test_groupbyError(key: Any, seq: Iterable[Any], expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		groupby(key, seq)

@pytest.mark.parametrize('seqs, expected', (
	pytest.param([[1, 2], [3, 4]], [1, 3, 2, 4], id='lists'),
	pytest.param(('ABC', 'XY'), ['A', 'X', 'B', 'Y', 'C'], id='stringsUnequal'),
	# Reference: upstream toolz's test suite.
	pytest.param(((), (13, 17), (), (19,)), [13, 19, 17], id='tuplesEmptyAmong'),
	pytest.param((), [], id='seqsEmpty'),
))
def test_interleave(seqs: Iterable[Iterable[Any]], expected: list[Any]) -> None:
	assertEqualTo([*interleave(seqs)], expected, interleave.__name__, seqs)

# Reference: "Both the individual sequences and the sequence of sequences may be infinite".
def test_interleaveInfinite() -> None:
	assertEqualTo(tuple(take(5, interleave((itertools.count(13), itertools.repeat('N'))))), (13, 'N', 14, 'N', 15), interleave.__name__, (itertools.count(13), itertools.repeat('N')))

# Relation: an exception from one of the sequences propagates unchanged, message included.
@pytest.mark.parametrize('seqs, expected, match', (
	pytest.param(None, TypeError, "'NoneType' object is not iterable", id='seqsNone'),
	pytest.param([None, None], TypeError, "'NoneType' object is not iterable", id='listOfNone'),
	pytest.param([[1, 2], IteratorRaises()], ValueError, f'^{messageSensorDisconnected}$', id='IteratorRaises'),
))
def test_interleaveError(seqs: Iterable[Iterable[Any]], expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		list(interleave(seqs))

@pytest.mark.parametrize('x, expected', (
	pytest.param([1, 2, 3], True, id='list'),
	pytest.param('abc', True, id='string'),
	pytest.param(5, False, id='5'),
	pytest.param(None, False, id='None'),
	pytest.param(IterableNotSequence(tuplePrimes), True, id='IterableNotSequencePrimes'),
))
def test_isiterable(x: object, expected: bool) -> None:
	assert isiterable(x) is expected, messageTestFailure(isiterable(x), expected, isiterable.__name__, x)

@pytest.mark.parametrize('leftkey, leftseq, rightkey, rightseq, left_default, right_default, expected', (
	pytest.param(second, friends, first, cities, no_default, no_default, Counter({
		(('Edith', 'Alice'), ('Alice', 'NYC')): 1, (('Zhao', 'Alice'), ('Alice', 'NYC')): 1
		, (('Edith', 'Alice'), ('Alice', 'Chicago')): 1, (('Zhao', 'Alice'), ('Alice', 'Chicago')): 1
		, (('Alice', 'Edith'), ('Edith', 'Paris')): 1, (('Zhao', 'Edith'), ('Edith', 'Paris')): 1
		, (('Alice', 'Edith'), ('Edith', 'Berlin')): 1, (('Zhao', 'Edith'), ('Edith', 'Berlin')): 1
		, (('Alice', 'Zhao'), ('Zhao', 'Shanghai')): 1,
	}), id='second-friends-first-cities'),
))
def test_join(leftkey: Any, leftseq: Iterable[Any], rightkey: Any, rightseq: Iterable[Any], left_default: Any, right_default: Any, expected: Counter[tuple[Any, Any]]) -> None:
	assertEqualTo(Counter(join(leftkey, leftseq, rightkey, rightseq, left_default, right_default)), expected, join.__name__, leftkey, leftseq, rightkey, rightseq, left_default, right_default)

@pytest.mark.parametrize('leftseq, rightseq, left_default, right_default, expected', (
	pytest.param([1, 2, 3], [2, 3, 4], None, None, [(2, 2), (3, 3), (None, 4), (1, None)], id='outer-defaultsNone'),
	# Reference: the docstring's outer join, with each default alone.
	pytest.param([1, 2, 3], [2, 3, 4], None, no_default, [(2, 2), (3, 3), (None, 4)], id='rightOuter-leftDefaultNone'),
	pytest.param([1, 2, 3], [2, 3, 4], no_default, None, [(2, 2), (3, 3), (1, None)], id='leftOuter-rightDefaultNone'),
	pytest.param([1, 2, 3], [2, 3, 4], no_default, no_default, [(2, 2), (3, 3)], id='inner'),
	pytest.param([1, 2, 3], [2, 3, 4], noDefaultUnpickled, noDefaultUnpickled, [(2, 2), (3, 3)], id='inner-noDefaultUnpickled'),
	pytest.param([1], [2], equalsEveryString, no_default, [(equalsEveryString, 2)], id='rightOuter-equalsEveryString'),
	pytest.param([1], [2], no_default, equalsEveryString, [(1, equalsEveryString)], id='leftOuter-equalsEveryString'),
))
def test_joinOuter(leftseq: Iterable[int], rightseq: Iterable[int], left_default: Any, right_default: Any, expected: list[tuple[Any, Any]]) -> None:
	assertEqualTo([*join(identity, leftseq, identity, rightseq, left_default, right_default)], expected, join.__name__, identity, leftseq, identity, rightseq, left_default, right_default)

# Relation: "If the keys are not obviously callable then it is assumed that indexing was intended", so index keys and list keys
# join what the corresponding `getter` callables join.
@pytest.mark.parametrize('leftkey, rightkey', (
	pytest.param(1, 0, id='index1-index0'),
	pytest.param([1], [0], id='indices1-indices0'),
))
def test_joinIndex(leftkey: Any, rightkey: Any) -> None:
	assertEqualTo(Counter(map(itemgetter(0, 1), join(leftkey, friends, rightkey, cities))), Counter(join(second, friends, first, cities))
		, join.__name__, leftkey, friends, rightkey, cities)

# Reference: the docstring states that `join` evaluates the right sequence lazily, so it can be arbitrarily large.
def test_joinInfinite() -> None:
	assertEqualTo(tuple(take(2, join(identity, [13, 17], identity, itertools.count()))), ((13, 13), (17, 17)), join.__name__, identity, [13, 17], identity, itertools.count())

# Reference: a hash join looks up each right key, so an unhashable right key raises `TypeError`, as in upstream toolz.
@pytest.mark.parametrize('leftseq, rightseq, expected, match', (
	pytest.param(None, (1, 2, 3), TypeError, "'NoneType' object is not iterable", id='leftseqNone'),
	pytest.param((1, 2, 3), None, TypeError, "'NoneType' object is not iterable", id='rightseqNone'),
	pytest.param([1], [[1]], TypeError, "unhashable type: 'list'", id='rightKeysUnhashable'),
))
def test_joinError(leftseq: Iterable[Any], rightseq: Iterable[Any], expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		list(join(identity, leftseq, identity, rightseq))

def test_mapcat() -> None:
	assertEqualTo([*mapcat(partial(map, str.upper), [['a', 'b'], ['c', 'd', 'e']])], ['A', 'B', 'C', 'D', 'E'], mapcat.__name__, partial(map, str.upper), [['a', 'b'], ['c', 'd', 'e']])

@pytest.mark.parametrize('seq', boxOfIterablesPrimes)
@pytest.mark.parametrize('n, expected', (
	pytest.param(0, 2, id='index0'),
	pytest.param(3, 7, id='index3'),
	pytest.param(6, 17, id='index6'),
))
def test_nth(n: int, seq: Iterable[int], expected: int) -> None:
	assertEqualTo(nth(n, seq), expected, nth.__name__, n, seq)

# Reference: upstream toolz's test suite: a sequence accepts a negative index.
@pytest.mark.parametrize('n, seq, expected', (
	pytest.param(-2, 'ABCDE', 'D', id='indexNegative2-string'),
	pytest.param(-1, [2, 3, 5, 7, 11, 13, 17], 17, id='indexNegative1-listPrimes'),
	pytest.param(-7, deque(tuplePrimes), 2, id='indexNegative7-dequePrimes'),
))
def test_nthNegative(n: int, seq: Sequence[Any], expected: Any) -> None:
	assertEqualTo(nth(n, seq), expected, nth.__name__, n, seq)

# Reference: upstream toolz's test suite: an iterator refuses a negative index, and an index past the end of an iterator
# raises `StopIteration`.
@pytest.mark.parametrize('n, seq, expected, match', (
	pytest.param(-2, IterableNotSequence(tuplePrimes), ValueError, 'must be positive when indexing an iterator', id='indexNegative2-IterableNotSequencePrimes'),
	pytest.param(-1, dict.fromkeys(tuplePrimes), ValueError, 'must be positive when indexing an iterator', id='indexNegative1-dictionaryKeysPrimes'),
	pytest.param(7, IterableNotSequence(tuplePrimes), StopIteration, '^$', id='index7-IterableNotSequencePrimes'),
	pytest.param(7, tuplePrimes, IndexError, 'tuple index out of range', id='index7-tuplePrimes'),
	pytest.param(0, None, TypeError, "'NoneType' object is not iterable", id='index0-seqNone'),
	pytest.param(None, tuplePrimes, TypeError, "'NoneType' object cannot be interpreted as an integer", id='indexNone-tuplePrimes'),
))
def test_nthError(n: int, seq: Iterable[int], expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		nth(n, seq)

@pytest.mark.parametrize('seq', boxOfIterablesPrimes)
@pytest.mark.parametrize('n, pad, expected', (
	pytest.param(2, no_pad, ((2, 3), (5, 7), (11, 13)), id='size2-padAbsent'),
	pytest.param(2, None, ((2, 3), (5, 7), (11, 13), (17, None)), id='size2-padNone'),
	pytest.param(3, 0, ((2, 3, 5), (7, 11, 13), (17, 0, 0)), id='size3-pad0'),
	pytest.param(7, no_pad, (tuplePrimes,), id='size7-padAbsent'),
	pytest.param(13, no_pad, (), id='size13-padAbsent'),
	pytest.param(2, equalsEveryString, ((2, 3), (5, 7), (11, 13), (17, equalsEveryString)), id='size2-equalsEveryString'),
))
def test_partition(n: int, seq: Iterable[int], pad: Any, expected: tuple[tuple[Any, ...], ...]) -> None:
	partitions: Iterator[tuple[Any, ...]] = partition(n, seq, pad)
	assert isinstance(partitions, Iterator), messageTestFailure(type(partitions), Iterator, partition.__name__, n, seq, pad)
	assertEqualTo(tuple(partitions), expected, partition.__name__, n, seq, pad)

@pytest.mark.parametrize('seq', boxOfIterablesPrimes)
@pytest.mark.parametrize('n, expected', (
	pytest.param(2, ((2, 3), (5, 7), (11, 13), (17,)), id='size2'),
	pytest.param(3, ((2, 3, 5), (7, 11, 13), (17,)), id='size3'),
	pytest.param(7, (tuplePrimes,), id='size7'),
	pytest.param(13, (tuplePrimes,), id='size13'),
))
def test_partition_all(n: int, seq: Iterable[int], expected: tuple[tuple[int, ...], ...]) -> None:
	partitions: Iterator[tuple[int, ...]] = partition_all(n, seq)
	assert isinstance(partitions, Iterator), messageTestFailure(type(partitions), Iterator, partition_all.__name__, n, seq)
	assertEqualTo(tuple(partitions), expected, partition_all.__name__, n, seq)

@pytest.mark.parametrize('n, seq, expected, match', (
	pytest.param(None, [1, 2, 3], TypeError, "'NoneType' object cannot be interpreted as an integer", id='sizeNone'),
	pytest.param(1, None, TypeError, "'NoneType' object is not iterable", id='seqNone'),
))
def test_partitionError(n: int, seq: Iterable[int], expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		list(partition(n, seq))

@pytest.mark.parametrize('seq', boxOfIterablesPrimes)
def test_peek(seq: Iterable[int]) -> None:
	item, seqPeeked = peek(seq)
	assertEqualTo((item, tuple(seqPeeked)), (2, tuplePrimes), peek.__name__, seq)

@pytest.mark.parametrize('seq', boxOfIterablesPrimes)
@pytest.mark.parametrize('n, expected', (
	pytest.param(2, (2, 3), id='items2'),
	pytest.param(13, tuplePrimes, id='items13'),
))
def test_peekn(n: int, seq: Iterable[int], expected: tuple[int, ...]) -> None:
	items, seqPeeked = peekn(n, seq)
	assertEqualTo((items, tuple(seqPeeked)), (expected, tuplePrimes), peekn.__name__, n, seq)

# Reference: upstream toolz's test suite: an empty sequence has nothing to peek.
@pytest.mark.parametrize('seq, expected, match', (
	pytest.param((), StopIteration, '^$', id='tupleEmpty'),
	pytest.param(None, TypeError, "'NoneType' object is not iterable", id='seqNone'),
))
def test_peekError(seq: Iterable[int], expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		peek(seq)

@pytest.mark.parametrize('ind, seqs, default, expected', (
	pytest.param('name', [{'id': 1, 'name': 'Cheese'}, {'id': 2, 'name': 'Pies'}], no_default, ['Cheese', 'Pies'], id='name-food'),
	pytest.param([0, 1], [[1, 2, 3], [4, 5, 7]], no_default, [(1, 2), (4, 5)], id='indices0and1-lists'),
	# Reference: upstream toolz's test suite.
	pytest.param(1, [[0], [0, 1]], None, [None, 1], id='index1-defaultNone'),
	pytest.param('price', [{'id': 1}, {'id': 2, 'price': 1}], 0, [0, 1], id='price-default0'),
	pytest.param(['price', 'other'], [{'id': 1}, {'id': 2, 'price': 1}], 0, [(0, 0), (1, 0)], id='keysAbsent-default0'),
	pytest.param(0, [[0, 1], [2, 3], [4, 5]], noDefaultUnpickled, [0, 2, 4], id='index0-noDefaultUnpickled'),
	# Reference: `get` with a list of indices; ten indices or more take `operator.itemgetter` instead of `_pluck_list`.
	pytest.param([*range(10)], [[*range(13)]], no_default, [tuple(range(10))], id='indices0to9'),
	pytest.param(5, [[1]], equalsEveryString, [equalsEveryString], id='index5-equalsEveryString'),
	pytest.param([5], [[1]], equalsEveryString, [(equalsEveryString,)], id='indices5-equalsEveryString'),
))
def test_pluck(ind: Any, seqs: Iterable[Any], default: Any, expected: list[Any]) -> None:
	itemsPlucked: Iterator[Any] = pluck(ind, seqs, default)
	assert isinstance(itemsPlucked, Iterator), messageTestFailure(type(itemsPlucked), Iterator, pluck.__name__, ind, seqs, default)
	assertEqualTo([*itemsPlucked], expected, pluck.__name__, ind, seqs, default)

# Reference: upstream toolz's test suite: `pluck` raises the exception that indexing raises, message included, unless a
# default replaces a missing item.
@pytest.mark.parametrize('ind, seqs, default, expected, match', (
	pytest.param(1, [[0]], no_default, IndexError, 'list index out of range', id='index1-listsShort'),
	pytest.param('name', [{'id': 1}], no_default, KeyError, "'name'", id='keyAbsent'),
	pytest.param(1, [[0]], noDefaultUnpickled, IndexError, 'list index out of range', id='index1-noDefaultUnpickled'),
	pytest.param([0], [5], None, TypeError, "'int' object is not subscriptable", id='indices0-itemNotIndexable-defaultNone'),
	pytest.param(0, None, no_default, TypeError, "'NoneType' object is not iterable", id='seqsNone'),
	pytest.param(0, [None, [2]], no_default, TypeError, "'NoneType' object is not subscriptable", id='itemNone'),
))
def test_pluckError(ind: Any, seqs: Iterable[Any], default: Any, expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		list(pluck(ind, seqs, default))

@pytest.mark.parametrize('prob, seq, random_state, expected', (
	pytest.param(0.1, [*range(100)], 2016, [7, 9, 19, 25, 30, 32, 34, 48, 59, 60, 81, 98], id='fraction1Tenth-range100-seed2016'),
	pytest.param(0.1, [*range(100)], Random(2016), [7, 9, 19, 25, 30, 32, 34, 48, 59, 60, 81, 98], id='fraction1Tenth-range100-Random2016'),
	# Reference: upstream toolz's test suite: a probability of 1 keeps every item.
	pytest.param(1, [*range(100)], 2016, [*range(100)], id='probability1-range100-seed2016'),
))
def test_random_sample(prob: float, seq: Iterable[int], random_state: Any, expected: list[int]) -> None:
	assertEqualTo([*random_sample(prob, seq, random_state)], expected, random_sample.__name__, prob, seq, random_state)

@pytest.mark.parametrize('key, binop, seq, init, expected', (
	pytest.param(isEven, add, [1, 2, 3, 4, 5], no_default, {False: 9, True: 6}, id='isEven-add-initAbsent'),
	pytest.param(isEven, mul, [1, 2, 3, 4, 5], no_default, {False: 15, True: 8}, id='isEven-mul-initAbsent'),
	pytest.param(isEven, addToSet, [1, 2, 3, 4, 1, 2, 3], set, {True: {2, 4}, False: {1, 3}}, id='isEven-addToSet-initSet'),
	# Reference: upstream toolz's test suite.
	pytest.param(isEven, add, [1, 2, 3, 4], noDefaultUnpickled, {True: 6, False: 4}, id='isEven-add-noDefaultUnpickled'),
	pytest.param(isEven, add, [1, 2, 3, 4], 0, {True: 6, False: 4}, id='isEven-add-init0'),
	pytest.param(0, add, [(1, 2), (1, 3), (2, 5)], (), {1: (1, 2, 1, 3), 2: (2, 5)}, id='index0-add-initTupleEmpty'),
	pytest.param(isEven, pairAccumulated, [2, 4], equalsEveryString, {True: ((equalsEveryString, 2), 4)}, id='isEven-pairAccumulated-equalsEveryString'),
))
def test_reduceby(key: Any, binop: Callable[[Any, Any], Any], seq: Iterable[Any], init: Any, expected: dict[Any, Any]) -> None:
	assertEqualTo(reduceby(key, binop, seq, init), expected, reduceby.__name__, key, binop, seq, init)

# Relation: the docstring states that `reduceby(key, binop, seq)` equals `valmap(reduction, groupby(key, seq))` with
# `reduce(binop, group)` as the reduction. `sub` is neither commutative nor associative, so agreement includes order.
@given(seq=strategies.lists(strategies.integers(-89, 89), max_size=21))
def test_reducebyGenerated(seq: list[int]) -> None:
	assertEqualTo(reduceby(isEven, sub, seq), valmap(partial[int](reduce, sub), groupby(isEven, seq)), reduceby.__name__, isEven, sub, seq)  # pyright: ignore[reportArgumentType]

@pytest.mark.parametrize('key, binop, seq, expected, match', (
	pytest.param(list, add, [(13,), (17,)], TypeError, "unhashable type: 'list'", id='keysUnhashable'),
	pytest.param(None, add, [1, 2, 3], TypeError, "'int' object is not subscriptable", id='keyNone'),
	pytest.param(isEven, None, [1, 2, 3], TypeError, "'NoneType' object is not callable", id='binopNone'),
	pytest.param(isEven, add, None, TypeError, "'NoneType' object is not iterable", id='seqNone'),
))
def test_reducebyError(key: Any, binop: Callable[[Any, Any], Any], seq: Iterable[Any], expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		reduceby(key, binop, seq, 0)

@pytest.mark.parametrize('seq', boxOfIterablesPrimes)
@pytest.mark.parametrize('n, expected', (
	pytest.param(1, ((2,), (3,), (5,), (7,), (11,), (13,), (17,)), id='size1'),
	pytest.param(2, ((2, 3), (3, 5), (5, 7), (7, 11), (11, 13), (13, 17)), id='size2'),
	pytest.param(7, (tuplePrimes,), id='size7'),
	# Reference: upstream toolz's test suite: a window longer than the sequence yields nothing.
	pytest.param(13, (), id='size13'),
))
def test_sliding_window(n: int, seq: Iterable[int], expected: tuple[tuple[int, ...], ...]) -> None:
	windows: Iterator[tuple[int, ...]] = sliding_window(n, seq)
	assert isinstance(windows, Iterator), messageTestFailure(type(windows), Iterator, sliding_window.__name__, n, seq)
	assertEqualTo(tuple(windows), expected, sliding_window.__name__, n, seq)

@pytest.mark.parametrize('seq', boxOfIterablesPrimes)
@pytest.mark.parametrize('n, expected', (
	pytest.param(0, (), id='items0'),
	pytest.param(1, (17,), id='items1'),
	pytest.param(3, (11, 13, 17), id='items3'),
	pytest.param(7, tuplePrimes, id='items7'),
	pytest.param(13, tuplePrimes, id='items13'),
))
def test_tail(n: int, seq: Iterable[int], expected: tuple[int, ...]) -> None:
	assertEqualTo(tuple(tail(n, seq)), expected, tail.__name__, n, seq)

@pytest.mark.parametrize('seq, expected', (
	pytest.param([2, 3, 5, 7], [5, 7], id='listPrimes'),
	pytest.param((2, 3, 5, 7), (5, 7), id='tuplePrimes'),
	pytest.param('NESW', 'SW', id='stringCompass'),
	pytest.param(b'NESW', b'SW', id='bytesCompass'),
	pytest.param(bytearray(b'NESW'), bytearray(b'SW'), id='bytearrayCompass'),
	pytest.param(range(2, 7), range(5, 7), id='range2to6'),
	pytest.param({'N': 0, 'E': 1, 'S': 2, 'W': 3}, ('S', 'W'), id='dictionaryCompass'),
	pytest.param(UserList((2, 3, 5, 7)), UserList((5, 7)), id='UserListPrimes'),
))
def test_tailType(seq: Iterable[Any], expected: Sequence[Any]) -> None:
	itemsLast: Sequence[Any] = tail(2, seq)
	assertEqualTo((itemsLast, type(itemsLast)), (expected, type(expected)), tail.__name__, 2, seq)

@pytest.mark.parametrize('seq', boxOfIterablesPrimes)
@pytest.mark.parametrize('n, expected', (
	pytest.param(0, (), id='items0'),
	pytest.param(1, (2,), id='items1'),
	pytest.param(3, (2, 3, 5), id='items3'),
	pytest.param(7, tuplePrimes, id='items7'),
	pytest.param(13, tuplePrimes, id='items13'),
))
def test_take(n: int, seq: Iterable[int], expected: tuple[int, ...]) -> None:
	itemsFirst: Iterator[int] = take(n, seq)
	assert isinstance(itemsFirst, Iterator), messageTestFailure(type(itemsFirst), Iterator, take.__name__, n, seq)
	assertEqualTo(tuple(itemsFirst), expected, take.__name__, n, seq)

@pytest.mark.parametrize('seq', boxOfIterablesPrimes)
@pytest.mark.parametrize('n, expected', (
	pytest.param(1, tuplePrimes, id='every1'),
	pytest.param(2, (2, 5, 11, 17), id='every2'),
	pytest.param(3, (2, 7, 17), id='every3'),
	pytest.param(13, (2,), id='every13'),
))
def test_take_nth(n: int, seq: Iterable[int], expected: tuple[int, ...]) -> None:
	itemsTaken: Iterator[int] = take_nth(n, seq)
	assert isinstance(itemsTaken, Iterator), messageTestFailure(type(itemsTaken), Iterator, take_nth.__name__, n, seq)
	assertEqualTo(tuple(itemsTaken), expected, take_nth.__name__, n, seq)

@pytest.mark.parametrize('function', (drop, tail, take, take_nth))
@pytest.mark.parametrize('n, seq, expected, match', (
	pytest.param(None, tuplePrimes, TypeError, "'NoneType' object cannot be interpreted as an integer", id='countNone'),
	pytest.param(1, None, TypeError, "'NoneType' object is not iterable", id='seqNone'),
))
def test_positionalError(function: Callable[[int, Iterable[int]], Iterable[int]], n: int, seq: Iterable[int], expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		list(function(n, seq))

@pytest.mark.parametrize('seq', boxOfIterablesPrimes)
@pytest.mark.parametrize('k, key, expected', (
	pytest.param(0, None, (), id='largest0'),
	pytest.param(1, None, (17,), id='largest1'),
	pytest.param(2, None, (17, 13), id='largest2'),
	pytest.param(13, None, (17, 13, 11, 7, 5, 3, 2), id='largest13'),
	pytest.param(2, neg, (2, 3), id='largest2-neg'),
))
def test_topk(k: int, seq: Iterable[int], key: Callable[[int], int] | None, expected: tuple[int, ...]) -> None:
	assertEqualTo(topk(k, seq, key), expected, topk.__name__, k, seq, key)

@pytest.mark.parametrize('k, seq, key, expected', (
	pytest.param(2, [1, 100, 10, 1000], None, (1000, 100), id='largest2-powersOf10'),
	pytest.param(2, ['Alice', 'Bob', 'Charlie', 'Dan'], len, ('Charlie', 'Alice'), id='largest2-names-len'),
	# Reference: upstream toolz's test suite, for keys that index each item, and for stability among equal keys.
	pytest.param(2, [{'a': 1, 'b': 10}, {'a': 2, 'b': 9}, {'a': 10, 'b': 1}, {'a': 9, 'b': 2}], 'a', ({'a': 10, 'b': 1}, {'a': 9, 'b': 2}), id='largest2-keyA'),
	pytest.param(2, [(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)], 0, ((4, 0), (3, 1)), id='largest2-index0'),
	pytest.param(4, [5, 9, 2, 1, 5, 3], bool, (5, 9, 2, 1), id='largest4-keysEqual'),
))
def test_topkKey(k: int, seq: Iterable[Any], key: Any, expected: tuple[Any, ...]) -> None:
	assertEqualTo(topk(k, seq, key), expected, topk.__name__, k, seq, key)

# Reference: `sorted(seq, key=key, reverse=True)[:k]`, which `heapq.nlargest`, named in the docstring, documents as its
# equivalent; `sorted` is stable, so items with equal keys keep their order. Small integers produce equal keys.
@given(k=strategies.integers(0, 13), seq=strategies.lists(strategies.integers(-5, 5), max_size=21), key=strategies.sampled_from((None, abs, isEven)))
def test_topkGenerated(k: int, seq: list[int], key: Callable[[int], Any] | None) -> None:
	assertEqualTo(topk(k, seq, key), tuple(sorted(seq, key=key, reverse=True)[0:k]), topk.__name__, k, seq, key)

@pytest.mark.parametrize('k, seq, expected, match', (
	pytest.param(None, [1, 2, 3], TypeError, "'NoneType' object cannot be interpreted as an integer", id='largestNone'),
	pytest.param(3, None, TypeError, "'NoneType' object is not iterable", id='seqNone'),
))
def test_topkError(k: int, seq: Iterable[int], expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		topk(k, seq)

# Reference: `collections.Counter` counts the keys whose groups `groupby` collects.
@given(seq=strategies.lists(strategies.integers(-8, 8), max_size=34))
def test_groupbyGenerated(seq: list[int]) -> None:
	assertEqualTo(valmap(len, groupby(isEven, seq)), dict(Counter(map(isEven, seq))), groupby.__name__, isEven, seq)
