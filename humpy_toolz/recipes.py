# ruff:file-ignore[undocumented-public-module]
from __future__ import annotations

from humpy_toolz.itertoolz import frequencies, getter, pluck
from typing import TYPE_CHECKING
import itertools

if TYPE_CHECKING:
	from collections.abc import Callable, Hashable, Iterable, Iterator
	from typing import Any

__all__ = ('countby', 'partitionby')

def countby[T, K: Hashable](key: Callable[[T], K] | K, seq: Iterable[T]) -> dict[K, int]:
	"""Count elements of a collection by a key function.

	Returns
	-------
	countBy : dict[K, int]
		A dictionary mapping keys to the number of times they occur in `seq`.

	>>> countby(len, ['cat', 'mouse', 'dog'])
	{3: 2, 5: 1}

	>>> def iseven(x):
	...     return x % 2 == 0
	>>> countby(iseven, [1, 2, 3])  # doctest:+SKIP
	{True: 1, False: 2}

	See Also
	--------
		groupby
	"""
	if not callable(key):
		key = getter(key)
	return frequencies(map(key, seq))

def partitionby[T](func: Callable[[T], Any], seq: Iterable[T]) -> Iterator[tuple[T, ...]]:
	"""Partition a sequence according to a function.

	Partition `s` into a sequence of lists such that, when traversing
	`s`, every time the output of `func` changes a new list is started
	and that and subsequent items are collected into that list.

	Returns
	-------
	partitionBy : Iterator[tuple[T, ...]]
	An iterator of tuples, each containing a partition of `seq`.

	>>> is_space = lambda c: c == ' '
	>>> list(partitionby(is_space, 'I have space'))
	[('I',), (' ',), ('h', 'a', 'v', 'e'), (' ',), ('s', 'p', 'a', 'c', 'e')]

	>>> is_large = lambda x: x > 10
	>>> list(partitionby(is_large, [1, 2, 1, 99, 88, 33, 99, -1, 5]))
	[(1, 2, 1), (99, 88, 33, 99), (-1, 5)]

	See Also
	--------
		partition
		groupby
		itertools.groupby
	"""
	return map(tuple, pluck(1, itertools.groupby(seq, key=func)))
