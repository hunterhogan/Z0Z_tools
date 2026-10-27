"""Test membership and ordering, filter sequences, and inspect mappings.

(AI generated docstring)

Contents
--------
Boolean antecedents
	between吗
		Test whether a value lies within inclusive bounds.
	consecutive吗
		Test whether integers are consecutive in ascending or descending order.
	thisHasThat吗
		Test whether a container contains a value.
	thisNotHaveThat吗
		Test whether a container does not contain a value.

Filtering functions
	exclude
		Obtain sequence items whose positions are not excluded.

Disaggregation and deconstruction functions
	DOTitems
		Obtain an iterator of mapping key-value pairs.
	DOTkeys
		Obtain an iterator of mapping keys.
	DOTvalues
		Obtain an iterator of mapping values.
	reverseLookup
		Find the first dictionary key associated with a value.
"""

from __future__ import annotations

from humpy_cytoolz import curry as syntacticCurry
from more_itertools import extract
from operator import eq
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from collections.abc import Container, Hashable, Iterable, Iterator, Mapping, Sequence
	from hunterMakesPy import Ordinals
	from typing import Any

#======== Boolean antecedents ================================================

@syntacticCurry
def between吗[小于: Ordinals](floor: 小于, ceiling: 小于, comparand: 小于) -> bool:
	"""Test the inclusive bounds `floor <= comparand <= ceiling`.

	(AI generated docstring)

	You can supply only `floor` and `ceiling` to obtain a predicate for values to compare.

	Parameters
	----------
	floor : 小于
		Inclusive lower bound.
	ceiling : 小于
		Inclusive upper bound.
	comparand : 小于
		Value to compare with the bounds. All three values must support ordered comparison.

	Returns
	-------
	withinBounds : bool
		`True` when `floor <= comparand <= ceiling`; otherwise, `False`.
	"""
	return floor <= comparand <= ceiling

def consecutive吗(flatContainer: Sequence[int]) -> bool:
	"""Test whether integers are consecutive in ascending or descending order.

	(AI generated docstring)

	Parameters
	----------
	flatContainer : Sequence[int]
		Integers in the order to test. Supply at least two integers with distinct endpoints.
		An empty sequence raises `IndexError`. Equal endpoints raise `ValueError`, including
		a sequence with only one integer.

	Returns
	-------
	consecutive : bool
		`True` when each integer differs from the previous integer by one and the direction
		remains the same; otherwise, `False`.
	"""
	difference: int = flatContainer[-1] - flatContainer[0]
	direction: int = (difference > 0) - (difference < 0)
	ImaRangeOfInt = range(flatContainer[0], flatContainer[-1] + direction, direction)
	return (abs(difference) == (len(flatContainer) - 1)) and (all(map(eq, flatContainer, ImaRangeOfInt)))

@syntacticCurry
def thisHasThat吗[个](this: Container[个], that: 个) -> bool:
	"""Test whether `that` is present in `this`.

	(AI generated docstring)

	You can use `thisHasThat吗` as a membership predicate. Supplying only `this` produces a
	predicate that tests each supplied value for membership in `this`.

	Parameters
	----------
	this : Container[个]
		Container to search.
	that : 个
		Value to find.

	Returns
	-------
	thatIsPresent : bool
		`True` if `that in this`.
	"""
	return that in this

@syntacticCurry
def thisNotHaveThat吗[个](this: Container[个], that: 个) -> bool:
	"""Test whether `that` is absent from `this`.

	(AI generated docstring)

	You can supply only `this` to obtain a predicate that tests each supplied value for
	absence from `this`.

	Parameters
	----------
	this : Container[个]
		Container to search.
	that : 个
		Value whose absence to test.

	Returns
	-------
	thatIsAbsent : bool
		`True` if `that not in this`.

	See Also
	--------
	`thisHasThat吗`
		Test for membership instead of absence.
	"""
	return not thisHasThat吗(this, that)

#======== Filtering functions ================================================

def exclude[个](flatContainer: Sequence[个], indices: Iterable[int]) -> Iterator[个]:
	"""Obtain items from `flatContainer` whose positions are not in `indices`.

	(AI generated docstring)

	Parameters
	----------
	flatContainer : Sequence[个]
		Sequence from which to select items.
	indices : Iterable[int]
		Zero-based positions to exclude. Negative positions wrap modulo the sequence length,
		so `-1` excludes the last item. Repeated positions have no additional effect.
		Nonnegative positions outside the sequence are ignored. A negative position with an
		empty `flatContainer` raises `ZeroDivisionError`.

	Returns
	-------
	itemsIncluded : Iterator[个]
		Items at the remaining positions, in their original sequence order.
	"""
	lengthIterable: int = len(flatContainer)

	def normalizeIndex(index: int) -> int:
		"""I use this to wrap a negative position modulo the sequence length.

		(AI generated docstring)

		Parameters
		----------
		index : int
			Position to normalize for `flatContainer`.

		Returns
		-------
		index : int
			Position modulo the sequence length if negative; otherwise, the supplied position.
		"""
		if index < 0:
			index = (index + lengthIterable) % lengthIterable
		return index
	indicesInclude: list[int] = sorted(set(range(lengthIterable)).difference(map(normalizeIndex, indices)))
	return extract(flatContainer, indicesInclude)

#======== Disaggregation and deconstruction functions ================================================

def DOTitems[文件: Hashable, 文义](dictionary: Mapping[文件, 文义], /) -> Iterator[tuple[文件, 文义]]:
	"""Create an `Iterator` of key-value pairs from a mapping.

	(AI generated docstring)

	You can pass the result to functions requiring iterators rather than mapping views.

	Parameters
	----------
	dictionary : Mapping[文件, 文义]
		Source mapping from which to extract key-value pairs.

	Returns
	-------
	aRiverOfItems : Iterator[tuple[文件, 文义]]
		`Iterator` yielding each `(key, value)` pair in the order provided by `dictionary`.
	"""
	return iter(dictionary.items())

def DOTkeys[个](dictionary: Mapping[个, Any], /) -> Iterator[个]:
	"""Create an `Iterator` of keys from a mapping.

	(AI generated docstring)

	You can pass the result to functions requiring iterators rather than mapping views.

	Parameters
	----------
	dictionary : Mapping[个, Any]
		Source mapping from which to extract keys.

	Returns
	-------
	aRiverOfKeys : Iterator[个]
		`Iterator` yielding each key in the order provided by `dictionary`.
	"""
	return iter(dictionary.keys())

def DOTvalues[个](dictionary: Mapping[Any, 个], /) -> Iterator[个]:
	"""Create an `Iterator` of values from a mapping.

	(AI generated docstring)

	You can pass the result to functions requiring iterators rather than mapping views.

	Parameters
	----------
	dictionary : Mapping[Any, 个]
		Source mapping from which to extract values.

	Returns
	-------
	aRiverOfValues : Iterator[个]
		`Iterator` yielding each value in the order provided by `dictionary`.
	"""
	return iter(dictionary.values())

def reverseLookup[文件: Hashable, 文义](dictionary: dict[文件, 文义], keyValue: 文义) -> 文件 | None:
	"""Find the key in a dictionary that maps to a specified value.

	(AI generated docstring)

	You can find the first key where `dictionary[key] == keyValue`, in dictionary insertion
	order. When no matching key exists, the result is `None`. Values need not be distinct.
	To test only whether a value is present, use `keyValue in dictionary.values()`.

	Parameters
	----------
	dictionary : dict[文件, 文义]
		Dictionary to search for `keyValue`.
	keyValue : 文义
		Value to locate in `dictionary.values()`.

	Returns
	-------
	keyOrNone : 文件 | None
		The first key that maps to `keyValue`, or `None` when no key maps to `keyValue`. A result
		of `None` can also be a matching key when `dictionary` contains the key `None`.
	"""
	for key, value in dictionary.items():
		if value == keyValue:
			return key
	return None
