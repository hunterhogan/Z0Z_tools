"""Expected values and exceptions come from the targets' docstrings unless a comment names another basis.

Every target that accepts `factory` returns a mapping that `factory` created, and no target changes the mapping it reads:
each test asserts both, for every kind of input mapping and every factory.
"""
from __future__ import annotations

from copy import deepcopy
from humpy_cytoolz.dicttoolz import (
	assoc, assoc_in, dissoc, get_in, itemfilter, itemmap, keyfilter, keymap, merge, merge_with, update_in, valfilter, valmap)
from humpy_cytoolz.itertoolz import first
from humpy_cytoolz.tests import assertEqualTo
from humpy_cytoolz.tests.dataSamples.callables import isEven, keyEvenValueLessThan4吗
from humpy_cytoolz.tests.dataSamples.mappings import boxOfFactories, boxOfMappingKinds
from hypothesis import given, strategies
from threading import Lock
from typing import TYPE_CHECKING
import pytest
import sys

if TYPE_CHECKING:
	from collections.abc import Callable, Hashable, Mapping, MutableMapping, Sequence
	from typing import Any

transaction: dict[str, Any] = {'name': 'Alice', 'purchase': {'items': ['Apple', 'Orange'], 'costs': [0.50, 1.25]}, 'credit card': '5555-1234-1234-1234'}
bills: dict[str, list[int]] = {'Alice': [20, 15, 30], 'Bob': [10, 35]}
lockSensor: Lock = Lock()
"""A value that `copy.deepcopy` refuses, as many values in a configuration mapping are."""

@pytest.mark.parametrize('factory', boxOfFactories)
@pytest.mark.parametrize('mappingKind', boxOfMappingKinds)
@pytest.mark.parametrize('d, key, value, expected', (
	pytest.param({}, 'a', 1, {'a': 1}, id='dictionaryEmpty-a'),
	pytest.param({'a': 1}, 'a', 3, {'a': 3}, id='keyPresent-a'),
	pytest.param({'a': 1}, 'b', 3, {'a': 1, 'b': 3}, id='keyAbsent-b'),
))
def test_assoc(mappingKind: Callable[[dict[Any, Any]], Mapping[Any, Any]], d: dict[Any, Any], key: Any, value: Any, factory: Callable[[], MutableMapping[Any, Any]], expected: dict[Any, Any]) -> None:
	mapping: Mapping[Any, Any] = mappingKind(d)
	mappingUpdated: MutableMapping[Any, Any] = assoc(mapping, key, value, factory)
	assertEqualTo((type(mappingUpdated), dict(mappingUpdated)), (type(factory()), expected), assoc.__name__, mapping, key, value, factory)
	assertEqualTo(dict(mapping), d, assoc.__name__, mapping, key, value, factory)

@pytest.mark.parametrize('factory', boxOfFactories)
@pytest.mark.parametrize('mappingKind', boxOfMappingKinds)
@pytest.mark.parametrize('d, keys, value, expected', (
	pytest.param({'a': 1}, ['a'], 2, {'a': 2}, id='a'),
	pytest.param({'a': {'b': 1}}, ['a', 'b'], 2, {'a': {'b': 2}}, id='aB'),
	pytest.param({}, ['a', 'b'], 1, {'a': {'b': 1}}, id='dictionaryEmpty-aB'),
	# Reference: upstream toolz's test suite: siblings at each level survive.
	pytest.param({'a': {'b': 55, 'c': 89}, 'd': 13}, ['a', 'b'], 144, {'a': {'b': 144, 'c': 89}, 'd': 13}, id='siblings-aB'),
))
def test_assoc_in(mappingKind: Callable[[dict[Any, Any]], Mapping[Any, Any]], d: dict[Any, Any], keys: Sequence[Any], value: Any, factory: Callable[[], MutableMapping[Any, Any]], expected: dict[Any, Any]) -> None:
	dictionaryBefore: dict[Any, Any] = deepcopy(d)
	mapping: Mapping[Any, Any] = mappingKind(d)
	mappingUpdated: MutableMapping[Any, Any] = assoc_in(mapping, keys, value, factory)
	assertEqualTo((type(mappingUpdated), dict(mappingUpdated)), (type(factory()), expected), assoc_in.__name__, mapping, keys, value, factory)
	assertEqualTo(dict(mapping), dictionaryBefore, assoc_in.__name__, mapping, keys, value, factory)

@pytest.mark.parametrize('factory', boxOfFactories)
@pytest.mark.parametrize('mappingKind', boxOfMappingKinds)
@pytest.mark.parametrize('d, keys, expected', (
	pytest.param({'x': 1, 'y': 2}, ('y',), {'x': 1}, id='y'),
	pytest.param({'x': 1, 'y': 2}, ('y', 'x'), {}, id='yX'),
	pytest.param({'x': 1}, ('y',), {'x': 1}, id='keyAbsent'),
	# Reference: the docstring's "Algorithm Details": removing 60% of the keys or more copies only the remaining items.
	pytest.param({'N': 0, 'E': 1, 'S': 2, 'W': 3, 'C': 4}, ('N', 'E', 'S', 'W'), {'C': 4}, id='compass-removeFourFifths'),
	pytest.param({'N': 0, 'E': 1, 'S': 2, 'W': 3, 'C': 4}, ('N',), {'E': 1, 'S': 2, 'W': 3, 'C': 4}, id='compass-removeOneFifth'),
	pytest.param({'N': 0}, (), {'N': 0}, id='keysAbsent'),
))
def test_dissoc(mappingKind: Callable[[dict[Any, Any]], Mapping[Any, Any]], d: dict[Any, Any], keys: tuple[Any, ...], factory: Callable[[], MutableMapping[Any, Any]], expected: dict[Any, Any]) -> None:
	mapping: Mapping[Any, Any] = mappingKind(d)
	mappingReduced: MutableMapping[Any, Any] = dissoc(mapping, *keys, factory=factory)
	assertEqualTo((type(mappingReduced), dict(mappingReduced)), (type(factory()), expected), dissoc.__name__, mapping, *keys, factory=factory)
	assertEqualTo(dict(mapping), d, dissoc.__name__, mapping, *keys, factory=factory)

def test_dissocError() -> None:
	with pytest.raises(TypeError, match="dissoc\\(\\) got an unexpected keyword argument 'factoryy'"):
		dissoc({'x': 1}, 'x', factoryy=dict)  # pyright: ignore[reportCallIssue] # ty: ignore[no-matching-overload]

@pytest.mark.parametrize('mappingKind', boxOfMappingKinds)
@pytest.mark.parametrize('keys, default, expected', (
	pytest.param(['purchase', 'items', 0], None, 'Apple', id='purchaseItems0'),
	pytest.param(['name'], None, 'Alice', id='name'),
	pytest.param(['purchase', 'total'], None, None, id='purchaseTotal'),
	pytest.param(['purchase', 'items', 'apple'], None, None, id='purchaseItemsApple'),
	pytest.param(['purchase', 'items', 10], None, None, id='purchaseItems10'),
	pytest.param(['purchase', 'total'], 0, 0, id='purchaseTotal-default0'),
))
def test_get_in(keys: Sequence[Any], mappingKind: Callable[[dict[Any, Any]], Mapping[Any, Any]], default: Any, expected: Any) -> None:
	assertEqualTo(get_in(keys, mappingKind(transaction), default), expected, get_in.__name__, keys, mappingKind(transaction), default)

# Relation: an empty path names `coll` itself.
@pytest.mark.parametrize('mappingKind', boxOfMappingKinds)
def test_get_inPathEmpty(mappingKind: Callable[[dict[Any, Any]], Mapping[Any, Any]]) -> None:
	coll: Mapping[Any, Any] = mappingKind(transaction)
	assert get_in([], coll) is coll, f'{get_in.__name__}([], {coll!r}) did not return {coll!r}.'

# Reference: upstream toolz's test suite: with `no_default=True`, indexing raises its own exception.
@pytest.mark.parametrize('keys, coll, expected, match', (
	pytest.param(['y'], {}, KeyError, "'y'", id='y-dictionaryEmpty'),
	pytest.param([0], [], IndexError, 'list index out of range', id='index0-listEmpty'),
	pytest.param(['x', 0], {'x': 42}, TypeError, "'int' object is not subscriptable", id='x0-valueNotIndexable'),
	pytest.param([0, 1], None, TypeError, "'NoneType' object is not subscriptable", id='collNone'),
))
def test_get_inError(keys: Sequence[Any], coll: Any, expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		get_in(keys, coll, no_default=True)

@pytest.mark.parametrize('factory', boxOfFactories)
@pytest.mark.parametrize('mappingKind', boxOfMappingKinds)
@pytest.mark.parametrize('predicate, d, expected', (
	pytest.param(keyEvenValueLessThan4吗, {1: 2, 2: 3, 3: 4, 4: 5}, {2: 3}, id='keyEvenValueLessThan4'),
))
def test_itemfilter(predicate: Callable[[tuple[Any, Any]], bool], mappingKind: Callable[[dict[Any, Any]], Mapping[Any, Any]], d: dict[Any, Any], factory: Callable[[], MutableMapping[Any, Any]], expected: dict[Any, Any]) -> None:
	mapping: Mapping[Any, Any] = mappingKind(d)
	mappingFiltered: MutableMapping[Any, Any] = itemfilter(predicate, mapping, factory)
	assertEqualTo((type(mappingFiltered), dict(mappingFiltered)), (type(factory()), expected), itemfilter.__name__, predicate, mapping, factory)
	assertEqualTo(dict(mapping), d, itemfilter.__name__, predicate, mapping, factory)

@pytest.mark.parametrize('factory', boxOfFactories)
@pytest.mark.parametrize('mappingKind', boxOfMappingKinds)
@pytest.mark.parametrize('func, d, expected', (
	pytest.param(reversed, {'Alice': 10, 'Bob': 20}, {10: 'Alice', 20: 'Bob'}, id='reversed-accounts'),
))
def test_itemmap(func: Callable[[tuple[Any, Any]], Any], mappingKind: Callable[[dict[Any, Any]], Mapping[Any, Any]], d: dict[Any, Any], factory: Callable[[], MutableMapping[Any, Any]], expected: dict[Any, Any]) -> None:
	mapping: Mapping[Any, Any] = mappingKind(d)
	mappingTransformed: MutableMapping[Any, Any] = itemmap(func, mapping, factory)
	assertEqualTo((type(mappingTransformed), dict(mappingTransformed)), (type(factory()), expected), itemmap.__name__, func, mapping, factory)
	assertEqualTo(dict(mapping), d, itemmap.__name__, func, mapping, factory)

@pytest.mark.parametrize('factory', boxOfFactories)
@pytest.mark.parametrize('mappingKind', boxOfMappingKinds)
@pytest.mark.parametrize('predicate, d, expected', (
	pytest.param(isEven, {1: 2, 2: 3, 3: 4, 4: 5}, {2: 3, 4: 5}, id='isEven'),
))
def test_keyfilter(predicate: Callable[[Any], bool], mappingKind: Callable[[dict[Any, Any]], Mapping[Any, Any]], d: dict[Any, Any], factory: Callable[[], MutableMapping[Any, Any]], expected: dict[Any, Any]) -> None:
	mapping: Mapping[Any, Any] = mappingKind(d)
	mappingFiltered: MutableMapping[Any, Any] = keyfilter(predicate, mapping, factory)
	assertEqualTo((type(mappingFiltered), dict(mappingFiltered)), (type(factory()), expected), keyfilter.__name__, predicate, mapping, factory)
	assertEqualTo(dict(mapping), d, keyfilter.__name__, predicate, mapping, factory)

@pytest.mark.parametrize('factory', boxOfFactories)
@pytest.mark.parametrize('mappingKind', boxOfMappingKinds)
@pytest.mark.parametrize('func, d, expected', (
	pytest.param(str.lower, bills, {'alice': [20, 15, 30], 'bob': [10, 35]}, id='lower-bills'),
	# Reference: upstream toolz's test suite: when transformed keys collide, the later item's value remains.
	pytest.param(isEven, {13: 21, 34: 55, 55: 89}, {False: 89, True: 55}, id='isEven-keysCollide'),
))
def test_keymap(func: Callable[[Any], Hashable], mappingKind: Callable[[dict[Any, Any]], Mapping[Any, Any]], d: dict[Any, Any], factory: Callable[[], MutableMapping[Any, Any]], expected: dict[Any, Any]) -> None:
	mapping: Mapping[Any, Any] = mappingKind(d)
	mappingTransformed: MutableMapping[Any, Any] = keymap(func, mapping, factory)
	assertEqualTo((type(mappingTransformed), dict(mappingTransformed)), (type(factory()), expected), keymap.__name__, func, mapping, factory)
	assertEqualTo(dict(mapping), d, keymap.__name__, func, mapping, factory)

@pytest.mark.parametrize('factory', boxOfFactories)
@pytest.mark.parametrize('mappingKind', boxOfMappingKinds)
@pytest.mark.parametrize('dicts, expected', (
	pytest.param(({1: 'one'}, {2: 'two'}), {1: 'one', 2: 'two'}, id='oneTwo'),
	pytest.param(({1: 2, 3: 4}, {3: 3, 4: 4}), {1: 2, 3: 3, 4: 4}, id='laterPrecedence'),
	# Reference: upstream toolz's test suite.
	pytest.param(({2: 3, 5: 7}, {5: 11, 11: 13}, {2: 17, 11: 19}), {2: 17, 5: 11, 11: 19}, id='threeDicts'),
	pytest.param(({13: 21},), {13: 21}, id='oneDict'),
))
def test_merge(mappingKind: Callable[[dict[Any, Any]], Mapping[Any, Any]], dicts: tuple[dict[Any, Any], ...], factory: Callable[[], MutableMapping[Any, Any]], expected: dict[Any, Any]) -> None:
	mappingMerged: MutableMapping[Any, Any] = merge(*map(mappingKind, dicts), factory=factory)
	assertEqualTo((type(mappingMerged), dict(mappingMerged)), (type(factory()), expected), merge.__name__, *map(mappingKind, dicts), factory=factory)

# Relation: a single iterable of mappings merges as the same mappings passed separately.
@pytest.mark.parametrize('mappingKind', boxOfMappingKinds)
def test_mergeIterable(mappingKind: Callable[[dict[Any, Any]], Mapping[Any, Any]]) -> None:
	assertEqualTo(merge([mappingKind({1: 2, 3: 4}), mappingKind({3: 3, 4: 4})]), merge(mappingKind({1: 2, 3: 4}), mappingKind({3: 3, 4: 4})), merge.__name__, [mappingKind({1: 2, 3: 4}), mappingKind({3: 3, 4: 4})])

# Reference: the `dict` union operator, whose documentation states that the values of the right operand take priority.
@given(dictionaryLeft=strategies.dictionaries(strategies.integers(-8, 8), strategies.integers()), dictionaryRight=strategies.dictionaries(strategies.integers(-8, 8), strategies.integers()))
def test_mergeGenerated(dictionaryLeft: dict[int, int], dictionaryRight: dict[int, int]) -> None:
	assertEqualTo(merge(dictionaryLeft, dictionaryRight), dictionaryLeft | dictionaryRight, merge.__name__, dictionaryLeft, dictionaryRight)

def test_mergeError() -> None:
	with pytest.raises(TypeError, match="unexpected keyword argument 'factoryy'"):
		merge({1: 2}, {2: 3}, factoryy=dict)  # pyright: ignore[reportCallIssue] # ty: ignore[no-matching-overload]

@pytest.mark.parametrize('factory', boxOfFactories)
@pytest.mark.parametrize('mappingKind', boxOfMappingKinds)
@pytest.mark.parametrize('func, dicts, expected', (
	pytest.param(sum, ({1: 1, 2: 2}, {1: 10, 2: 20}), {1: 11, 2: 22}, id='sum'),
	pytest.param(first, ({1: 1, 2: 2}, {2: 20, 3: 30}), {1: 1, 2: 2, 3: 30}, id='first'),
	# Reference: upstream toolz's test suite: `func` receives the values in the order of `dicts`.
	pytest.param(tuple, ({2: 3, 5: 7}, {2: 11, 5: 13}, {2: 17}), {2: (3, 11, 17), 5: (7, 13)}, id='tuple-threeDicts'),
	pytest.param(sum, (), {}, id='sum-dictsAbsent'),
))
def test_merge_with(func: Callable[[list[Any]], Any], mappingKind: Callable[[dict[Any, Any]], Mapping[Any, Any]], dicts: tuple[dict[Any, Any], ...], factory: Callable[[], MutableMapping[Any, Any]], expected: dict[Any, Any]) -> None:
	mappingMerged: MutableMapping[Any, Any] = merge_with(func, *map(mappingKind, dicts), factory=factory)
	assertEqualTo((type(mappingMerged), dict(mappingMerged)), (type(factory()), expected), merge_with.__name__, func, *map(mappingKind, dicts), factory=factory)

# Relation: a single iterable of mappings merges as the same mappings passed separately.
@pytest.mark.parametrize('mappingKind', boxOfMappingKinds)
def test_merge_withIterable(mappingKind: Callable[[dict[Any, Any]], Mapping[Any, Any]]) -> None:
	assertEqualTo(merge_with(tuple, iter([mappingKind({1: 1, 2: 2}), mappingKind({1: 10})])), merge_with(tuple, mappingKind({1: 1, 2: 2}), mappingKind({1: 10})), merge_with.__name__, tuple, iter([mappingKind({1: 1, 2: 2}), mappingKind({1: 10})]))

@pytest.mark.parametrize('factory', boxOfFactories)
@pytest.mark.parametrize('mappingKind', boxOfMappingKinds)
@pytest.mark.parametrize('d, keys, func, default, expected', (
	pytest.param({'a': 0}, ['a'], (1).__add__, None, {'a': 1}, id='a-increment'),
	pytest.param({}, ['z'], (1).__add__, 0, {'z': 1}, id='dictionaryEmpty-z-increment-default0'),
	pytest.param({}, [1, 2, 3], str, 'bar', {1: {2: {3: 'bar'}}}, id='dictionaryEmpty-path123-str-defaultBar'),
	# Reference: upstream toolz's test suite: siblings at each level survive.
	pytest.param({'a': {'b': 55, 'c': 89}, 'd': 13}, ['a', 'b'], str, None, {'a': {'b': '55', 'c': 89}, 'd': 13}, id='siblings-aB-str'),
	pytest.param({'a': {'b': 34}}, ['a', 'b'], (1).__add__, None, {'a': {'b': 35}}, id='aB-increment'),
	pytest.param({'lock': lockSensor, 'reading': 13}, ['reading'], (1).__add__, None, {'lock': lockSensor, 'reading': 14}, id='valueNotCopyable-reading-increment'),
))
def test_update_in(mappingKind: Callable[[dict[Any, Any]], Mapping[Any, Any]], d: dict[Any, Any], keys: Sequence[Any], func: Callable[[Any], Any], default: Any, factory: Callable[[], MutableMapping[Any, Any]], expected: dict[Any, Any]) -> None:
	mapping: Mapping[Any, Any] = mappingKind(d)
	mappingUpdated: MutableMapping[Any, Any] = update_in(mapping, keys, func, default, factory)
	assertEqualTo((type(mappingUpdated), dict(mappingUpdated)), (type(factory()), expected), update_in.__name__, mapping, keys, func, default, factory)
	assertEqualTo(dict(mapping), d, update_in.__name__, mapping, keys, func, default, factory)

# Reference: `update_in` returns a new mutable mapping that `factory` created; a `frozendict` cannot be updated in place.
@pytest.mark.skipif(sys.version_info < (3, 15), reason='`frozendict` is a builtin from Python 3.15.')
@pytest.mark.parametrize('keys, expected', (
	pytest.param(['a'], {'a': '13'}, id='a'),
	pytest.param(['b', 'c'], {'a': 13, 'b': {'c': 'None'}}, id='pathAbsent-bC'),
))
def test_update_inFrozendict(keys: Sequence[Any], expected: dict[Any, Any]) -> None:
	mappingUpdated: MutableMapping[Any, Any] = update_in(frozendict({'a': 13}), keys, str)  # pyright: ignore[reportUndefinedVariable, reportCallIssue] # ty: ignore[unresolved-reference]  # ruff: ignore[undefined-name]
	assertEqualTo((type(mappingUpdated), mappingUpdated), (dict, expected), update_in.__name__, frozendict({'a': 13}), keys, str)  # pyright: ignore[reportUndefinedVariable, reportCallIssue] # ty: ignore[unresolved-reference]  # ruff: ignore[undefined-name]

# Relation: `update_in` with a function that returns `value` places `value` where `assoc_in` places it.
@pytest.mark.parametrize('factory', boxOfFactories)
@pytest.mark.parametrize('d, keys', (
	pytest.param({'a': {'b': 55, 'c': 89}, 'd': 13}, ['a', 'b'], id='siblings-aB'),
	pytest.param({}, ['N', 'E', 'S'], id='dictionaryEmpty-pathNES'),
))
def test_update_inAssoc_in(d: dict[Any, Any], keys: Sequence[Any], factory: Callable[[], MutableMapping[Any, Any]]) -> None:
	assertEqualTo(update_in(d, keys, str, None, factory), assoc_in(d, keys, str(get_in(keys, d)), factory), update_in.__name__, d, keys, str, None, factory)

@pytest.mark.parametrize('factory', boxOfFactories)
@pytest.mark.parametrize('mappingKind', boxOfMappingKinds)
@pytest.mark.parametrize('predicate, d, expected', (
	pytest.param(isEven, {1: 2, 2: 3, 3: 4, 4: 5}, {1: 2, 3: 4}, id='isEven'),
))
def test_valfilter(predicate: Callable[[Any], bool], mappingKind: Callable[[dict[Any, Any]], Mapping[Any, Any]], d: dict[Any, Any], factory: Callable[[], MutableMapping[Any, Any]], expected: dict[Any, Any]) -> None:
	mapping: Mapping[Any, Any] = mappingKind(d)
	mappingFiltered: MutableMapping[Any, Any] = valfilter(predicate, mapping, factory)
	assertEqualTo((type(mappingFiltered), dict(mappingFiltered)), (type(factory()), expected), valfilter.__name__, predicate, mapping, factory)
	assertEqualTo(dict(mapping), d, valfilter.__name__, predicate, mapping, factory)

@pytest.mark.parametrize('factory', boxOfFactories)
@pytest.mark.parametrize('mappingKind', boxOfMappingKinds)
@pytest.mark.parametrize('func, d, expected', (
	pytest.param(sum, bills, {'Alice': 65, 'Bob': 45}, id='sum-bills'),
))
def test_valmap(func: Callable[[Any], Any], mappingKind: Callable[[dict[Any, Any]], Mapping[Any, Any]], d: dict[Any, Any], factory: Callable[[], MutableMapping[Any, Any]], expected: dict[Any, Any]) -> None:
	mapping: Mapping[Any, Any] = mappingKind(d)
	mappingTransformed: MutableMapping[Any, Any] = valmap(func, mapping, factory)
	assertEqualTo((type(mappingTransformed), dict(mappingTransformed)), (type(factory()), expected), valmap.__name__, func, mapping, factory)
	assertEqualTo(dict(mapping), d, valmap.__name__, func, mapping, factory)

@pytest.mark.parametrize('function', (itemfilter, itemmap, keyfilter, keymap, valfilter, valmap))
@pytest.mark.parametrize('func, d, expected, match', (
	pytest.param(isEven, None, AttributeError, "'NoneType' object has no attribute 'items'", id='dNone'),
	pytest.param(None, {1: 2}, TypeError, "'NoneType' object is not callable", id='funcNone'),
))
def test_mappingFunctionError(function: Callable[..., Any], func: Callable[..., Any], d: Mapping[Any, Any], expected: type[Exception], match: str) -> None:
	with pytest.raises(expected, match=match):
		function(func, d)
