"""Expected values and exceptions come from the targets' docstrings unless a comment names another basis."""
from __future__ import annotations

from collections import Counter
from collections.abc import Iterator
from functools import partial
from humpy_cytoolz.functoolz import identity
from humpy_cytoolz.itertoolz import concat
from humpy_cytoolz.recipes import countby, partitionby
from humpy_cytoolz.tests import assertEqualTo, messageTestFailure
from humpy_cytoolz.tests.dataSamples.callables import isEven
from humpy_cytoolz.tests.dataSamples.iterables import boxOfIterablesPrimes
from hypothesis import given, strategies
from operator import lt
from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
	from collections.abc import Callable, Hashable, Iterable
	from typing import Any

@pytest.mark.parametrize('key, seq, expected', (
	pytest.param(len, ['cat', 'mouse', 'dog'], {3: 2, 5: 1}, id='len-animals'),
	pytest.param(isEven, [1, 2, 3], {True: 1, False: 2}, id='isEven-1to3'),
	# Reference: upstream toolz's test suite: a key that is not callable indexes each item, as `groupby` does.
	pytest.param(0, ('ab', 'ac', 'bc'), {'a': 2, 'b': 1}, id='index0-strings'),
	pytest.param([0], ('ab', 'ac', 'bc'), {('a',): 2, ('b',): 1}, id='indices0-strings'),
))
def test_countby(key: Any, seq: Iterable[Any], expected: dict[Hashable, int]) -> None:
	assertEqualTo(countby(key, seq), expected, countby.__name__, key, seq)

# Reference: `isEven` holds for 2 alone among the primes.
@pytest.mark.parametrize('seq', boxOfIterablesPrimes)
def test_countbyPrimes(seq: Iterable[int]) -> None:
	assertEqualTo(countby(isEven, seq), {True: 1, False: 6}, countby.__name__, isEven, seq)

# Reference: `collections.Counter` counts the keys with its own `dict`; the docstring leaves the order of keys unspecified.
@given(seq=strategies.lists(strategies.integers(-8, 8), max_size=34), key=strategies.sampled_from((abs, isEven, identity)))
def test_countbyGenerated(key: Callable[[int], Hashable], seq: list[int]) -> None:
	assertEqualTo(countby(key, seq), dict(Counter(map(key, seq))), countby.__name__, key, seq)

@pytest.mark.parametrize('key, seq, expected, match', (
	pytest.param(list, [(13,), (17,)], TypeError, "unhashable type: 'list'", id='keysUnhashable'),
	pytest.param(isEven, None, TypeError, "'NoneType' object is not iterable", id='seqNone'),
))
def test_countbyError(key: Any, seq: Iterable[Any], expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		countby(key, seq)

@pytest.mark.parametrize('func, seq, expected', (
	pytest.param(str.isspace, 'I have space', [('I',), (' ',), ('h', 'a', 'v', 'e'), (' ',), ('s', 'p', 'a', 'c', 'e')], id='isspace-sentence'),
	pytest.param(partial(lt, 10), [1, 2, 1, 99, 88, 33, 99, -1, 5], [(1, 2, 1), (99, 88, 33, 99), (-1, 5)], id='moreThan10-integers'),
	# Reference: upstream toolz's test suite.
	pytest.param(identity, [], [], id='identity-listEmpty'),
	pytest.param('aeiou'.__contains__, 'abcdefghi', [('a',), ('b', 'c', 'd'), ('e',), ('f', 'g', 'h'), ('i',)], id='vowel-letters'),
	pytest.param(identity, 'Khhhaaaaannnnn!!!!', [('K',), ('h',) * 3, ('a',) * 5, ('n',) * 5, ('!',) * 4], id='identity-Khan'),
))
def test_partitionby(func: Callable[[Any], object], seq: Iterable[Any], expected: list[tuple[Any, ...]]) -> None:
	partitions: Iterator[tuple[Any, ...]] = partitionby(func, seq)
	assert isinstance(partitions, Iterator), messageTestFailure(type(partitions), Iterator, partitionby.__name__, func, seq)
	assertEqualTo([*partitions], expected, partitionby.__name__, func, seq)

# Relation: the partitions hold every item of `seq` in order, so concatenating them returns `seq`.
@given(seq=strategies.lists(strategies.integers(-8, 8), max_size=34), func=strategies.sampled_from((abs, isEven, identity)))
def test_partitionbyRoundTrip(func: Callable[[int], object], seq: list[int]) -> None:
	assertEqualTo([*concat(partitionby(func, seq))], seq, partitionby.__name__, func, seq)

@pytest.mark.parametrize('func, seq, expected, match', (
	pytest.param(isEven, None, TypeError, "'NoneType' object is not iterable", id='seqNone'),
))
def test_partitionbyError(func: Callable[[Any], object], seq: Iterable[Any], expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		list(partitionby(func, seq))
