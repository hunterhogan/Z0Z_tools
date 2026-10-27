from __future__ import annotations

from collections import UserDict
from tests import assertEqualTo
from tests.dataSamples.predicates import (
	parametersAbsence, parametersAbsentFilter, parametersBounds, parametersBoundsFilter, parametersMemberFilter, parametersMembership)
from types import MappingProxyType
from typing import TYPE_CHECKING
from Z0Z_tools import between吗, consecutive吗, DOTitems, DOTkeys, DOTvalues, exclude, reverseLookup, thisHasThat吗, thisNotHaveThat吗
import pytest

if TYPE_CHECKING:
	from collections.abc import Container, Hashable, Iterable, Iterator, Mapping, Sequence
	from hunterMakesPy import Ordinals
	from typing import Any

@pytest.mark.parametrize(('floor', 'ceiling', 'comparand', 'expected'), parametersBounds)
def test_between吗[小于: Ordinals](floor: 小于, ceiling: 小于, comparand: 小于, expected: bool) -> None:
	actual: bool = between吗(floor, ceiling, comparand)
	assertEqualTo(actual, expected, 'between吗', floor, ceiling, comparand)

@pytest.mark.parametrize(('floor', 'ceiling', 'flatContainer', 'expected'), parametersBoundsFilter)
def test_between吗Curried[小于: Ordinals](floor: 小于, ceiling: 小于, flatContainer: Iterable[小于], expected: tuple[小于, ...]) -> None:
	actual: tuple[小于, ...] = tuple(filter(between吗(floor, ceiling), flatContainer))
	assertEqualTo(actual, expected, 'between吗', floor, ceiling, flatContainer)

@pytest.mark.parametrize(('flatContainer', 'expected'), (
	pytest.param((5, 6), True, id='ascending-pair'),
	pytest.param((6, 5), True, id='descending-pair'),
	pytest.param((5, 6, 7, 8), True, id='ascending-tuple'),
	pytest.param((8, 7, 6, 5), True, id='descending-tuple'),
	pytest.param([-7, -6, -5], True, id='negative-list'),
	pytest.param((-2, -1, 0, 1), True, id='cross-zero'),
	pytest.param(range(5, 9), True, id='ascending-range'),
	pytest.param(range(8, 4, -1), True, id='descending-range'),
	pytest.param((5, 7), False, id='pair-gap'),
	pytest.param((5, 7, 9), False, id='ascending-gaps'),
	pytest.param((9, 7, 5), False, id='descending-gaps'),
	pytest.param((5, 7, 6, 8), False, id='unordered-interior'),
	pytest.param((8, 6, 7, 5), False, id='unordered-descending-interior'),
	pytest.param((5, 5, 7), False, id='repeated-interior'),
))
def test_consecutive吗(flatContainer: Sequence[int], expected: bool) -> None:
	actual: bool = consecutive吗(flatContainer)
	assertEqualTo(actual, expected, 'consecutive吗', flatContainer)

@pytest.mark.parametrize(('flatContainer', 'expected'), (
	pytest.param((), IndexError, id='empty-tuple'),
	pytest.param([], IndexError, id='empty-list'),
	pytest.param(range(7, 7), IndexError, id='empty-range'),
	pytest.param((7,), ValueError, id='singleton-tuple'),
	pytest.param([7], ValueError, id='singleton-list'),
	pytest.param(range(7, 8), ValueError, id='singleton-range'),
	pytest.param((7, 7), ValueError, id='equal-pair'),
	pytest.param((7, 11, 7), ValueError, id='equal-endpoints'),
))
def test_consecutive吗Error(flatContainer: Sequence[int], expected: type[Exception]) -> None:
	with pytest.raises(expected):
		consecutive吗(flatContainer)

@pytest.mark.parametrize(('this', 'that', 'expected'), parametersMembership)
def test_thisHasThat吗[个](this: Container[个], that: 个, expected: bool) -> None:
	actual: bool = thisHasThat吗(this, that)
	assertEqualTo(actual, expected, 'thisHasThat吗', this, that)

@pytest.mark.parametrize(('this', 'flatContainer', 'expected'), parametersMemberFilter)
def test_thisHasThat吗Curried[个](this: Container[个], flatContainer: Iterable[个], expected: tuple[个, ...]) -> None:
	actual: tuple[个, ...] = tuple(filter(thisHasThat吗(this), flatContainer))
	assertEqualTo(actual, expected, 'thisHasThat吗', this, flatContainer)

@pytest.mark.parametrize(('this', 'that', 'expected'), parametersAbsence)
def test_thisNotHaveThat吗[个](this: Container[个], that: 个, expected: bool) -> None:
	actual: bool = thisNotHaveThat吗(this, that)
	assertEqualTo(actual, expected, 'thisNotHaveThat吗', this, that)

@pytest.mark.parametrize(('this', 'flatContainer', 'expected'), parametersAbsentFilter)
def test_thisNotHaveThat吗Curried[个](this: Container[个], flatContainer: Iterable[个], expected: tuple[个, ...]) -> None:
	actual: tuple[个, ...] = tuple(filter(thisNotHaveThat吗(this), flatContainer))
	assertEqualTo(actual, expected, 'thisNotHaveThat吗', this, flatContainer)

@pytest.mark.parametrize('flatContainer', (
	pytest.param((5, 6, 7, 8, 9), id='tuple'),
	pytest.param([5, 6, 7, 8, 9], id='list'),
	pytest.param(range(5, 10), id='range'),
))
@pytest.mark.parametrize(('indices', 'expected'), (
	pytest.param((), (5, 6, 7, 8, 9), id='exclude-none'),
	pytest.param((0,), (6, 7, 8, 9), id='exclude-first'),
	pytest.param((4,), (5, 6, 7, 8), id='exclude-last'),
	pytest.param((3, 1), (5, 7, 9), id='unordered-indices'),
	pytest.param((3, 1, 3), (5, 7, 9), id='duplicate-indices'),
	pytest.param((-1,), (5, 6, 7, 8), id='negative-last'),
	pytest.param((-5,), (6, 7, 8, 9), id='negative-first'),
	pytest.param((-6,), (5, 6, 7, 8), id='negative-wrap'),
	pytest.param((0, -5, 4, -1), (6, 7, 8), id='equivalent-indices'),
	pytest.param((5, 13), (5, 6, 7, 8, 9), id='outside-sequence'),
	pytest.param([0, 1, 2, 3, 4], (), id='exclude-all'),
))
def test_exclude[个](flatContainer: Sequence[个], indices: Iterable[int], expected: tuple[个, ...]) -> None:
	actual: Iterator[个] = exclude(flatContainer, indices)
	assertEqualTo(tuple(actual), expected, 'exclude', flatContainer, indices)
	assertEqualTo(tuple(actual), (), 'exclude', flatContainer, indices)

@pytest.mark.parametrize(('flatContainer', 'indices', 'expected'), (
	pytest.param((), (-1,), ZeroDivisionError, id='empty-tuple-negative-index'),
	pytest.param([], (-7,), ZeroDivisionError, id='empty-list-negative-index'),
))
def test_excludeError[个](flatContainer: Sequence[个], indices: Iterable[int], expected: type[Exception]) -> None:
	with pytest.raises(expected):
		exclude(flatContainer, indices)

@pytest.mark.parametrize(('dictionary', 'expected'), (
	pytest.param({}, (), id='empty'),
	pytest.param({'lambda': 7, 'delta': 5}, (('lambda', 7), ('delta', 5)), id='insertion-order'),
	pytest.param({'lambda': 7, 'delta': 7}, (('lambda', 7), ('delta', 7)), id='repeated-values'),
	pytest.param(UserDict({'lambda': 7, 'delta': 5}), (('lambda', 7), ('delta', 5)), id='user-dictionary'),
	pytest.param(MappingProxyType({'lambda': 7, 'delta': 5}), (('lambda', 7), ('delta', 5)), id='mapping-proxy'),
	pytest.param({(5, 7): None}, (((5, 7), None),), id='tuple-key-none-value'),
))
def test_DOTitems[文件: Hashable, 文义](dictionary: Mapping[文件, 文义], expected: tuple[tuple[文件, 文义], ...]) -> None:
	actual: Iterator[tuple[文件, 文义]] = DOTitems(dictionary)
	assertEqualTo(tuple(actual), expected, 'DOTitems', dictionary)
	assertEqualTo(tuple(actual), (), 'DOTitems', dictionary)

@pytest.mark.parametrize(('dictionary', 'expected'), (
	pytest.param({}, (), id='empty'),
	pytest.param({'lambda': 7, 'delta': 5}, ('lambda', 'delta'), id='insertion-order'),
	pytest.param({'lambda': 7, 'delta': 7}, ('lambda', 'delta'), id='repeated-values'),
	pytest.param(UserDict({'lambda': 7, 'delta': 5}), ('lambda', 'delta'), id='user-dictionary'),
	pytest.param(MappingProxyType({'lambda': 7, 'delta': 5}), ('lambda', 'delta'), id='mapping-proxy'),
	pytest.param({(5, 7): None}, ((5, 7),), id='tuple-key'),
))
def test_DOTkeys[个](dictionary: Mapping[个, Any], expected: tuple[个, ...]) -> None:
	actual: Iterator[个] = DOTkeys(dictionary)
	assertEqualTo(tuple(actual), expected, 'DOTkeys', dictionary)
	assertEqualTo(tuple(actual), (), 'DOTkeys', dictionary)

@pytest.mark.parametrize(('dictionary', 'expected'), (
	pytest.param({}, (), id='empty'),
	pytest.param({'lambda': 7, 'delta': 5}, (7, 5), id='insertion-order'),
	pytest.param({'lambda': 7, 'delta': 7}, (7, 7), id='repeated-values'),
	pytest.param(UserDict({'lambda': 7, 'delta': 5}), (7, 5), id='user-dictionary'),
	pytest.param(MappingProxyType({'lambda': 7, 'delta': 5}), (7, 5), id='mapping-proxy'),
	pytest.param({(5, 7): None}, (None,), id='none-value'),
))
def test_DOTvalues[个](dictionary: Mapping[Any, 个], expected: tuple[个, ...]) -> None:
	actual: Iterator[个] = DOTvalues(dictionary)
	assertEqualTo(tuple(actual), expected, 'DOTvalues', dictionary)
	assertEqualTo(tuple(actual), (), 'DOTvalues', dictionary)

@pytest.mark.parametrize(('dictionary', 'keyValue', 'expected'), (
	pytest.param({}, 7, None, id='empty'),
	pytest.param({'lambda': 7, 'delta': 5}, 7, 'lambda', id='first-value'),
	pytest.param({'lambda': 7, 'delta': 5}, 5, 'delta', id='later-value'),
	pytest.param({'lambda': 7, 'delta': 5}, 13, None, id='missing-value'),
	pytest.param({'lambda': 7, 'delta': 7}, 7, 'lambda', id='first-duplicate-value'),
	pytest.param({'delta': 7, 'lambda': 7}, 7, 'delta', id='reversed-duplicate-values'),
	pytest.param({0: 7, 5: 11}, 7, 0, id='zero-key'),
	pytest.param({'': 7, 'delta': 5}, 7, '', id='empty-text-key'),
	pytest.param({None: 7, 'delta': 5}, 7, None, id='none-key'),
	pytest.param({'lambda': None, 'delta': 5}, None, 'lambda', id='none-value'),
	pytest.param({'lambda': [5, 7], 'delta': [11, 13]}, [5, 7], 'lambda', id='unhashable-equal-value'),
	pytest.param({(5, 7): 11}, 11, (5, 7), id='tuple-key'),
))
def test_reverseLookup[文件: Hashable, 文义](dictionary: dict[文件, 文义], keyValue: 文义, expected: 文件 | None) -> None:
	actual: 文件 | None = reverseLookup(dictionary, keyValue)
	assertEqualTo(actual, expected, 'reverseLookup', dictionary, keyValue)
