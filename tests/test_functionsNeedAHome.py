"""Expected values and exceptions come from the targets' docstrings unless a comment names another basis."""
from __future__ import annotations

from collections import UserDict
from collections.abc import Iterator
from hypothesis import given, strategies
from tests import assertEqualTo, messageTestFailure
from types import MappingProxyType
from typing import TYPE_CHECKING
from Z0Z_tools import between吗, consecutive吗, DOTitems, DOTkeys, DOTvalues, exclude, reverseLookup, thisHasThat吗, thisNotHaveThat吗
import pytest

if TYPE_CHECKING:
	from _pytest.mark.structures import ParameterSet
	from collections.abc import Container, Hashable, Iterable, Mapping, Sequence
	from hunterMakesPy import Ordinals
	from typing import Any

parametersBetween吗: tuple[ParameterSet, ...] = (
	pytest.param(5, 11, 3, False, id='comparandBelowFloor'),
	pytest.param(5, 11, 5, True, id='comparandEqualsFloor'),
	pytest.param(5, 11, 7, True, id='comparandBetween'),
	pytest.param(5, 11, 11, True, id='comparandEqualsCeiling'),
	pytest.param(5, 11, 13, False, id='comparandAboveCeiling'),
	pytest.param(-11, -5, -7, True, id='negativeBetween'),
	pytest.param(-11, -5, -13, False, id='negativeBelowFloor'),
	pytest.param(-11, -5, -3, False, id='negativeAboveCeiling'),
	pytest.param(7, 7, 7, True, id='floorEqualsCeilingMatch'),
	pytest.param(7, 7, 5, False, id='floorEqualsCeilingMiss'),
	pytest.param(11, 5, 7, False, id='floorAboveCeiling'),
	pytest.param(2.5, 7.5, 5.5, True, id='fractionsBetween'),
	pytest.param('delta', 'lambda', 'gamma', True, id='stringsBetween'),
	pytest.param('delta', 'lambda', 'omega', False, id='stringAboveCeiling'),
)

parametersThisHasThat吗: tuple[ParameterSet, ...] = (
	pytest.param((5, 7, 11), 7, True, id='tuplePrimes-7'),
	pytest.param((5, 7, 11), 13, False, id='tuplePrimes-13'),
	pytest.param((), 7, False, id='tupleEmpty-7'),
	pytest.param(['delta', 'lambda'], 'lambda', True, id='listGreek-lambda'),
	pytest.param(['delta', 'lambda'], 'omega', False, id='listGreek-omega'),
	pytest.param({5, 7, 11}, 7, True, id='setPrimes-7'),
	pytest.param(frozenset((5, 7, 11)), 13, False, id='frozensetPrimes-13'),
	pytest.param({'delta': 5, 'lambda': 7}, 'lambda', True, id='dictionaryGreekPrimes-lambda'),
	pytest.param({'delta': 5, 'lambda': 7}, 7, False, id='dictionaryGreekPrimes-7'),
	pytest.param('delta lambda', 'lambda', True, id='stringGreek-lambda'),
	pytest.param('delta lambda', '', True, id='stringGreek-stringEmpty'),
	pytest.param(range(5, 12, 2), 7, True, id='rangeOddFrom5-7'),
	pytest.param(range(5, 12, 2), 8, False, id='rangeOddFrom5-8'),
	pytest.param((None, 7), None, True, id='tupleNone7-None'),
)

@pytest.mark.parametrize('floor, ceiling, comparand, expected', parametersBetween吗)
def test_between吗[小于: Ordinals](floor: 小于, ceiling: 小于, comparand: 小于, expected: bool) -> None:
	assert between吗(floor, ceiling, comparand) is expected, messageTestFailure(between吗(floor, ceiling, comparand), expected, between吗.__name__, floor, ceiling, comparand)

# Relation: the predicate that `between吗(floor, ceiling)` returns answers what the complete call answers.
@pytest.mark.parametrize('floor, ceiling, comparand, expected', parametersBetween吗)
def test_between吗Curried[小于: Ordinals](floor: 小于, ceiling: 小于, comparand: 小于, expected: bool) -> None:
	assert between吗(floor, ceiling)(comparand) is expected, messageTestFailure(between吗(floor, ceiling)(comparand), expected, between吗.__name__, floor, ceiling)

@pytest.mark.parametrize('flatContainer, expected', (
	pytest.param((5, 6), True, id='ascendingPair'),
	pytest.param((6, 5), True, id='descendingPair'),
	pytest.param((5, 6, 7, 8), True, id='ascendingTuple'),
	pytest.param((8, 7, 6, 5), True, id='descendingTuple'),
	pytest.param([-7, -6, -5], True, id='negativeList'),
	pytest.param((-2, -1, 0, 1), True, id='acrossZero'),
	pytest.param(range(5, 9), True, id='ascendingRange'),
	pytest.param(range(8, 4, -1), True, id='descendingRange'),
	pytest.param((5, 7), False, id='pairGap'),
	pytest.param((5, 7, 9), False, id='ascendingGaps'),
	pytest.param((9, 7, 5), False, id='descendingGaps'),
	pytest.param((5, 7, 6, 8), False, id='interiorUnordered'),
	pytest.param((8, 6, 7, 5), False, id='interiorUnorderedDescending'),
	pytest.param((5, 5, 7), False, id='interiorRepeated'),
))
def test_consecutive吗(flatContainer: Sequence[int], expected: bool) -> None:
	assert consecutive吗(flatContainer) is expected, messageTestFailure(consecutive吗(flatContainer), expected, consecutive吗.__name__, flatContainer)

# Reference: a `range` with step 1 or -1 is consecutive by definition. The integers stay small because `consecutive吗` does no
# arithmetic whose behavior changes with magnitude; the length starts at 2 because shorter sequences raise.
@given(start=strategies.integers(-89, 89), length=strategies.integers(2, 89), step=strategies.sampled_from((1, -1)))
def test_consecutive吗Generated(start: int, length: int, step: int) -> None:
	assert consecutive吗(range(start, start + step * length, step)) is True, messageTestFailure(consecutive吗(range(start, start + step * length, step)), True, consecutive吗.__name__, range(start, start + step * length, step))

@pytest.mark.parametrize('flatContainer, expected', (
	pytest.param((), IndexError, id='tupleEmpty'),
	pytest.param([], IndexError, id='listEmpty'),
	pytest.param(range(7, 7), IndexError, id='rangeEmpty'),
	pytest.param((7,), ValueError, id='tupleSingleton'),
	pytest.param([7], ValueError, id='listSingleton'),
	pytest.param(range(7, 8), ValueError, id='rangeSingleton'),
	pytest.param((7, 7), ValueError, id='pairEqual'),
	pytest.param((7, 11, 7), ValueError, id='endpointsEqual'),
))
def test_consecutive吗Error(flatContainer: Sequence[int], expected: type[Exception]) -> None:
	with pytest.raises(expected):
		consecutive吗(flatContainer)

@pytest.mark.parametrize('this, that, expected', parametersThisHasThat吗)
def test_thisHasThat吗[个](this: Container[个], that: 个, expected: bool) -> None:
	assert thisHasThat吗(this, that) is expected, messageTestFailure(thisHasThat吗(this, that), expected, thisHasThat吗.__name__, this, that)

# Relation: the predicate that `thisHasThat吗(this)` returns answers what the complete call answers.
@pytest.mark.parametrize('this, that, expected', parametersThisHasThat吗)
def test_thisHasThat吗Curried[个](this: Container[个], that: 个, expected: bool) -> None:
	assert thisHasThat吗(this)(that) is expected, messageTestFailure(thisHasThat吗(this)(that), expected, thisHasThat吗.__name__, this)

# Relation: absence is the negation of the membership that `parametersThisHasThat吗` states.
@pytest.mark.parametrize('this, that, expected', parametersThisHasThat吗)
def test_thisNotHaveThat吗[个](this: Container[个], that: 个, expected: bool) -> None:
	assert thisNotHaveThat吗(this, that) is (not expected), messageTestFailure(thisNotHaveThat吗(this, that), not expected, thisNotHaveThat吗.__name__, this, that)

# Relation: absence is the negation of membership, and the predicate that `thisNotHaveThat吗(this)` returns answers it.
@pytest.mark.parametrize('this, that, expected', parametersThisHasThat吗)
def test_thisNotHaveThat吗Curried[个](this: Container[个], that: 个, expected: bool) -> None:
	assert thisNotHaveThat吗(this)(that) is (not expected), messageTestFailure(thisNotHaveThat吗(this)(that), not expected, thisNotHaveThat吗.__name__, this)

@pytest.mark.parametrize('flatContainer', (
	pytest.param((5, 6, 7, 8, 9), id='tuple5to9'),
	pytest.param([5, 6, 7, 8, 9], id='list5to9'),
	pytest.param(range(5, 10), id='range5to9'),
))
@pytest.mark.parametrize('indices, expected', (
	pytest.param((), (5, 6, 7, 8, 9), id='indicesEmpty'),
	pytest.param((0,), (6, 7, 8, 9), id='index0'),
	pytest.param((4,), (5, 6, 7, 8), id='index4'),
	pytest.param((3, 1), (5, 7, 9), id='indicesUnordered'),
	pytest.param((3, 1, 3), (5, 7, 9), id='indicesRepeated'),
	pytest.param((-1,), (5, 6, 7, 8), id='indexNegative1'),
	pytest.param((-5,), (6, 7, 8, 9), id='indexNegative5'),
	pytest.param((-6,), (5, 6, 7, 8), id='indexNegative6'),
	pytest.param((0, -5, 4, -1), (6, 7, 8), id='indicesEquivalent'),
	pytest.param((5, 13), (5, 6, 7, 8, 9), id='indicesOutside'),
	pytest.param([0, 1, 2, 3, 4], (), id='indicesAll'),
))
def test_exclude[个](flatContainer: Sequence[个], indices: Iterable[int], expected: tuple[个, ...]) -> None:
	itemsIncluded: Iterator[个] = exclude(flatContainer, indices)
	assert isinstance(itemsIncluded, Iterator), messageTestFailure(type(itemsIncluded), Iterator, exclude.__name__, flatContainer, indices)
	assertEqualTo(tuple(itemsIncluded), expected, exclude.__name__, flatContainer, indices)

@pytest.mark.parametrize('flatContainer, indices, expected', (
	pytest.param((), (-1,), ZeroDivisionError, id='tupleEmpty-indexNegative1'),
	pytest.param([], (-7,), ZeroDivisionError, id='listEmpty-indexNegative7'),
))
def test_excludeError[个](flatContainer: Sequence[个], indices: Iterable[int], expected: type[Exception]) -> None:
	with pytest.raises(expected):
		exclude(flatContainer, indices)

@pytest.mark.parametrize('dictionary, expected', (
	pytest.param({}, (), id='dictionaryEmpty'),
	pytest.param({'lambda': 7, 'delta': 5}, (('lambda', 7), ('delta', 5)), id='dictionaryGreekPrimes'),
	pytest.param({'lambda': 7, 'delta': 7}, (('lambda', 7), ('delta', 7)), id='dictionaryValuesRepeated'),
	pytest.param(UserDict({'lambda': 7, 'delta': 5}), (('lambda', 7), ('delta', 5)), id='UserDictGreekPrimes'),
	pytest.param(MappingProxyType({'lambda': 7, 'delta': 5}), (('lambda', 7), ('delta', 5)), id='MappingProxyGreekPrimes'),
	pytest.param({(5, 7): None}, (((5, 7), None),), id='dictionaryKeyTupleValueNone'),
))
def test_DOTitems[文件: Hashable, 文义](dictionary: Mapping[文件, 文义], expected: tuple[tuple[文件, 文义], ...]) -> None:
	aRiverOfItems: Iterator[tuple[文件, 文义]] = DOTitems(dictionary)
	assert isinstance(aRiverOfItems, Iterator), messageTestFailure(type(aRiverOfItems), Iterator, DOTitems.__name__, dictionary)
	assertEqualTo(tuple(aRiverOfItems), expected, DOTitems.__name__, dictionary)

@pytest.mark.parametrize('dictionary, expected', (
	pytest.param({}, (), id='dictionaryEmpty'),
	pytest.param({'lambda': 7, 'delta': 5}, ('lambda', 'delta'), id='dictionaryGreekPrimes'),
	pytest.param({'lambda': 7, 'delta': 7}, ('lambda', 'delta'), id='dictionaryValuesRepeated'),
	pytest.param(UserDict({'lambda': 7, 'delta': 5}), ('lambda', 'delta'), id='UserDictGreekPrimes'),
	pytest.param(MappingProxyType({'lambda': 7, 'delta': 5}), ('lambda', 'delta'), id='MappingProxyGreekPrimes'),
	pytest.param({(5, 7): None}, ((5, 7),), id='dictionaryKeyTupleValueNone'),
))
def test_DOTkeys[个](dictionary: Mapping[个, Any], expected: tuple[个, ...]) -> None:
	aRiverOfKeys: Iterator[个] = DOTkeys(dictionary)
	assert isinstance(aRiverOfKeys, Iterator), messageTestFailure(type(aRiverOfKeys), Iterator, DOTkeys.__name__, dictionary)
	assertEqualTo(tuple(aRiverOfKeys), expected, DOTkeys.__name__, dictionary)

@pytest.mark.parametrize('dictionary, expected', (
	pytest.param({}, (), id='dictionaryEmpty'),
	pytest.param({'lambda': 7, 'delta': 5}, (7, 5), id='dictionaryGreekPrimes'),
	pytest.param({'lambda': 7, 'delta': 7}, (7, 7), id='dictionaryValuesRepeated'),
	pytest.param(UserDict({'lambda': 7, 'delta': 5}), (7, 5), id='UserDictGreekPrimes'),
	pytest.param(MappingProxyType({'lambda': 7, 'delta': 5}), (7, 5), id='MappingProxyGreekPrimes'),
	pytest.param({(5, 7): None}, (None,), id='dictionaryKeyTupleValueNone'),
))
def test_DOTvalues[个](dictionary: Mapping[Any, 个], expected: tuple[个, ...]) -> None:
	aRiverOfValues: Iterator[个] = DOTvalues(dictionary)
	assert isinstance(aRiverOfValues, Iterator), messageTestFailure(type(aRiverOfValues), Iterator, DOTvalues.__name__, dictionary)
	assertEqualTo(tuple(aRiverOfValues), expected, DOTvalues.__name__, dictionary)

@pytest.mark.parametrize('dictionary, keyValue, expected', (
	pytest.param({}, 7, None, id='dictionaryEmpty-7'),
	pytest.param({'lambda': 7, 'delta': 5}, 7, 'lambda', id='dictionaryGreekPrimes-7'),
	pytest.param({'lambda': 7, 'delta': 5}, 5, 'delta', id='dictionaryGreekPrimes-5'),
	pytest.param({'lambda': 7, 'delta': 5}, 13, None, id='dictionaryGreekPrimes-13'),
	pytest.param({'lambda': 7, 'delta': 7}, 7, 'lambda', id='dictionaryValuesRepeated-7'),
	pytest.param({'delta': 7, 'lambda': 7}, 7, 'delta', id='dictionaryValuesRepeatedReordered-7'),
	pytest.param({0: 7, 5: 11}, 7, 0, id='dictionaryKeyZero-7'),
	pytest.param({'': 7, 'delta': 5}, 7, '', id='dictionaryKeyStringEmpty-7'),
	pytest.param({None: 7, 'delta': 5}, 7, None, id='dictionaryKeyNone-7'),
	pytest.param({'lambda': None, 'delta': 5}, None, 'lambda', id='dictionaryValueNone-None'),
	pytest.param({'lambda': [5, 7], 'delta': [11, 13]}, [5, 7], 'lambda', id='dictionaryValuesUnhashable-list5and7'),
	pytest.param({(5, 7): 11}, 11, (5, 7), id='dictionaryKeyTuple-11'),
))
def test_reverseLookup[文件: Hashable, 文义](dictionary: dict[文件, 文义], keyValue: 文义, expected: 文件 | None) -> None:
	keyOrNone: 文件 | None = reverseLookup(dictionary, keyValue)
	assertEqualTo((keyOrNone, type(keyOrNone)), (expected, type(expected)), reverseLookup.__name__, dictionary, keyValue)
