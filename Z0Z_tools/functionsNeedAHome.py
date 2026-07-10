# ruff: noqa: DOC201, D100, D103
from __future__ import annotations

from collections.abc import Sequence
from humpy_cytoolz import curry as syntacticCurry
from more_itertools import extract
from operator import eq
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from collections.abc import Container, Iterable, Iterator, Mapping
	from hunterMakesPy import Ordinals
	from typing import Any

#======== Boolean antecedents ================================================

@syntacticCurry
def between吗[小于: Ordinals](floor: 小于, ceiling: 小于, comparand: 小于) -> bool:
	"""Inclusive `floor <= comparand <= ceiling`."""
	return floor <= comparand <= ceiling

# NOTE `个` TypeVar exists to help ty with static type checking. See https://github.com/astral-sh/ty/issues/2799.
def consecutive吗[个: Sequence[int]](flatContainer: 个) -> bool:
	"""Are the integers in `flatContainer` consecutive, either ascending or descending?"""
	difference: int = flatContainer[-1] - flatContainer[0]
	direction: int = (difference > 0) - (difference < 0)
	ImaRangeOfInt = range(flatContainer[0], flatContainer[-1] + direction, direction)
	return (abs(difference) == (len(flatContainer) - 1)) and (all(map(eq, flatContainer, ImaRangeOfInt)))

@syntacticCurry
def thisHasThat吗[个](this: Container[个], that: 个) -> bool:
	"""You can test whether `that` is present in `this`.

	You can use `thisHasThat` in an `if` statement, or you can pass `thisHasThat` as a
	predicate to a filtering utility described in the module docstring.

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

	References
	----------
	[1] `operator.contains` (Python documentation)
		https://docs.python.org/3/library/operator.html#operator.contains

	"""
	return that in this

@syntacticCurry
def thisNotHaveThat吗[个](this: Container[个], that: 个) -> bool:
	return not thisHasThat吗(this, that)

#======== Filtering functions ================================================

def exclude[个](flatContainer: Sequence[个], indices: Iterable[int]) -> Iterator[个]:
	"""Yield items from `flatContainer` whose positions are not in `indices`."""
	lengthIterable: int = len(flatContainer)

	def normalizeIndex(index: int) -> int:
		if index < 0:
			index = (index + lengthIterable) % lengthIterable
		return index
	indicesInclude: list[int] = sorted(set(range(lengthIterable)).difference(map(normalizeIndex, indices)))
	return extract(flatContainer, indicesInclude)

#======== Disaggregation and deconstruction functions ================================================

def DOTitems[文件, 文义](dictionary: Mapping[文件, 文义], /) -> Iterator[tuple[文件, 文义]]:
	"""Create an `Iterator` of key-value pairs from a mapping.

	You can use this function to convert `dictionary.items()` into an `Iterator` that you can
	pass to functions requiring iterators rather than views. The function is analogous to
	`dict.items()` [1] but returns an `Iterator` instead of a dictionary view.

	Parameters
	----------
	dictionary : Mapping[文件, 文义]
		Source mapping from which to extract key-value pairs.

	Returns
	-------
	aRiverOfItems : Iterator[tuple[文件, 文义]]
		`Iterator` yielding each `(key, value)` pair from `dictionary`.

	Examples
	--------
	The function is used to initialize iteration queues from filtered dictionaries.

		dequePileLeaf: deque[tuple[Pile, Leaf]] = deque(sorted(DOTitems(valfilter(mappingHasKey(dictionaryConditionalLeafPredecessors),
			leavesPinned))))

	The function is used to create sorted item sequences for triple-wise processing.

		piles3consecutive: deque[tuple[tuple[Pile, LeafSpace], tuple[Pile, LeafSpace], tuple[Pile, LeafSpace]]] = deque(triplewise(sorted(DOTitems(permutationSpace))))

	References
	----------
	[1] Mapping.items() - Python documentation
		https://docs.python.org/3/library/stdtypes.html#dict.items

	"""
	return iter(dictionary.items())

def DOTkeys[个](dictionary: Mapping[个, Any], /) -> Iterator[个]:
	"""Create an `Iterator` of keys from a mapping.

	You can use this function to convert `dictionary.keys()` into an `Iterator` that you can
	pass to functions requiring iterators rather than views. The function is analogous to
	`dict.keys()` [1] but returns an `Iterator` instead of a dictionary view.

	Parameters
	----------
	dictionary : Mapping[个, Any]
		Source mapping from which to extract keys.

	Returns
	-------
	aRiverOfKeys : Iterator[个]
		`Iterator` yielding each key from `dictionary`.

	Examples
	--------
	The function is used to extract keys for dictionary dissociation.

		return (leavesPinned, dissociatePiles(permutationSpace, *DOTkeys(leavesPinned)))

	The function is used to identify leaves with singleton domains.

		leavesWithDomainOf1: set[Leaf] = set(DOTkeys(valfilter((1).__eq__, leafAndItsDomainSize))).difference(leavesPinned.values()).difference([state.leavesTotal])

	References
	----------
	[1] Mapping.keys() - Python documentation
		https://docs.python.org/3/library/stdtypes.html#dict.keys

	"""
	return iter(dictionary.keys())

def DOTvalues[个](dictionary: Mapping[Any, 个], /) -> Iterator[个]:
	"""Create an `Iterator` of values from a mapping.

	You can use this function to convert `dictionary.values()` into an `Iterator` that you can
	pass to functions requiring iterators rather than views. The function is analogous to
	`dict.values()` [1] but returns an `Iterator` instead of a dictionary view.

	Parameters
	----------
	dictionary : Mapping[Any, 个]
		Source mapping from which to extract values.

	Returns
	-------
	aRiverOfValues : Iterator[个]
		`Iterator` yielding each value from `dictionary`.

	Examples
	--------
	The function is used to extract leaf domains for anti-option computation.

		if not (permutationSpace := _reducePileRangesOfLeaves(state, permutationSpace, deque(pilesUndetermined.items()), makeLeafAntiOptions(state.leavesTotal, DOTvalues(leavesPinned)))):

	The function is used to count leaf occurrences across domains.

		leafAndItsDomainSize: Counter[Leaf] = Counter(chain(chain.from_iterable(map(getIteratorOfLeaves, DOTvalues(pilesUndetermined))), DOTvalues(leavesPinned)))

	The function is used to extract folding sequences from pinned leaves.

		folding = tuple(DOTvalues(extractPinnedLeaves(permutationSpace)))

	References
	----------
	[1] Mapping.values() - Python documentation
		https://docs.python.org/3/library/stdtypes.html#dict.values

	"""
	return iter(dictionary.values())

def reverseLookup[文件, 文义](dictionary: dict[文件, 文义], keyValue: 文义) -> 文件 | None:
	"""Find the key in a dictionary that maps to a specified value.

	You can use this function to perform reverse dictionary lookup: given a value, find the
	key that maps to that value. The function iterates through `dictionary.items()` [1] and
	returns the first key where `dictionary[key] == keyValue`. When no matching key exists,
	the function returns `None`.

	Parameters
	----------
	dictionary : dict[文件, 文义]
		Dictionary to search for `keyValue`.
	keyValue : 文义
		Value to locate in `dictionary.values()`.

	Returns
	-------
	keyOrNone : 文件 | None
		The key that maps to `keyValue`, or `None` when no key maps to `keyValue`.

	Examples
	--------
	The function is used to find which pile contains a specific leaf.

		pileOfLeaf一零: Pile = raiseIfNone(reverseLookup(state.permutationSpace, leaf一零))
		pileOfLeaf首零一: Pile = raiseIfNone(reverseLookup(state.permutationSpace, leaf首零一))

	Important
	---------
	The function assumes all values in `dictionary` are distinct. When multiple keys map to
	`keyValue`, the function returns an arbitrary matching key (whichever appears first during
	iteration). The function is not efficient for membership testing: use `keyValue in dictionary.values()`
	instead. When you expect a key to exist, combine with `raiseIfNone` [2] rather than checking
	for `None`.

	References
	----------
	[1] dict.items() - Python documentation
		https://docs.python.org/3/library/stdtypes.html#dict.items
	[2] hunterMakesPy.raiseIfNone - Context7
		https://context7.com/hunterhogan/huntermakespy

	"""
	for key, value in dictionary.items():
		if value == keyValue:
			return key
	return None
