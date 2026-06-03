from collections import defaultdict as _defaultdict
from collections.abc import Callable, ItemsView, Iterator, KeysView, Mapping, MutableMapping, ValuesView
from humpy_toolz.dicttoolz import (
	assoc, assoc_in, dissoc, get_in, itemfilter, itemmap, keyfilter, keymap, merge, merge_with, update_in, valfilter, valmap)
from humpy_toolz.functoolz import identity
from humpy_toolz.utils import raises
from typing import Any, ClassVar
import os
import pytest

def inc(x: int) -> int:
	return x + 1

def iseven(i: int) -> bool:
	return i % 2 == 0

def bucketKeyByParity(key: int) -> int:
	return key % 2

def swapItemKeyWithValue(item: tuple[int, int]) -> tuple[int, int]:
	return item[1], item[0]

def summarizeItemToParityAndTotal(item: tuple[int, int]) -> tuple[int, int]:
	return item[0] % 2, item[0] + item[1]

def valueExceedsThreeHundred(value: int) -> bool:
	return value > 300

def keyExceedsThreeHundred(key: int) -> bool:
	return key > 300

def itemHasEvenKeyAndOddValue(item: tuple[int, int]) -> bool:
	return item[0] % 2 == 0 and item[1] % 2 == 1

def itemHasLargeKeyAndLargeValue(item: tuple[int, int]) -> bool:
	return item[0] > 300 and item[1] > 300

def makeDefaultDictFactory(
	itemIterable: ItemsView[Any, Any] | Iterator[tuple[Any, Any]] | None = None,
) -> 'defaultdict[Any, Any]':
	if itemIterable is None:
		return defaultdict(int)
	return defaultdict(int, itemIterable)

def makeCustomMappingFactory(
	itemIterable: ItemsView[Any, Any] | Iterator[tuple[Any, Any]] | None = None,
) -> 'CustomMapping':
	if itemIterable is None:
		return CustomMapping()
	return CustomMapping(itemIterable)

class TestDict:
	"""Test typical usage: dict inputs, no factory keyword.

	Class attributes:
		D: callable that inputs a dict and creates or returns a MutableMapping
		kw: kwargs dict to specify "factory" keyword (if applicable)
	"""
	D: ClassVar[Callable[..., Any]] = dict
	kw: ClassVar[dict[str, Any]] = {}

	def test_merge(self) -> None:
		D, kw = (self.D, self.kw)
		assert merge(D({1: 1, 2: 2}), D({3: 4}), **kw) == D({1: 1, 2: 2, 3: 4})

	def test_merge_iterable_arg(self) -> None:
		D, kw = (self.D, self.kw)
		assert merge([D({1: 1, 2: 2}), D({3: 4})], **kw) == D({1: 1, 2: 2, 3: 4})  # pyright: ignore[reportCallIssue, reportArgumentType]  # ty:ignore[no-matching-overload]

	def test_merge_three_dicts(self) -> None:
		D, kw = (self.D, self.kw)
		assert merge(D({2: 3}), D({5: 7}), D({11: 13}), **kw) == D({2: 3, 5: 7, 11: 13})
		assert merge(D({2: 3, 5: 7}), D({5: 11, 11: 13}), D({2: 17, 11: 19}), **kw) == D({2: 17, 5: 11, 11: 19})

	def test_merge_with(self) -> None:
		D, kw = (self.D, self.kw)
		dicts = (D({1: 1, 2: 2}), D({1: 10, 2: 20}))
		assert merge_with(sum, *dicts, **kw) == D({1: 11, 2: 22})
		assert merge_with(tuple, *dicts, **kw) == D({1: (1, 10), 2: (2, 20)})
		dicts = (D({1: 1, 2: 2, 3: 3}), D({1: 10, 2: 20}))
		assert merge_with(sum, *dicts, **kw) == D({1: 11, 2: 22, 3: 3})
		assert merge_with(tuple, *dicts, **kw) == D({1: (1, 10), 2: (2, 20), 3: (3,)})
		assert not merge_with(sum)  # pyright: ignore[reportArgumentType]

	def test_merge_with_iterable_arg(self) -> None:
		D, kw = (self.D, self.kw)
		dicts = (D({1: 1, 2: 2}), D({1: 10, 2: 20}))
		assert merge_with(sum, *dicts, **kw) == D({1: 11, 2: 22})
		assert merge_with(sum, dicts, **kw) == D({1: 11, 2: 22})  # pyright: ignore[reportCallIssue, reportArgumentType]  # ty:ignore[no-matching-overload]
		assert merge_with(sum, iter(dicts), **kw) == D({1: 11, 2: 22})  # pyright: ignore[reportCallIssue, reportArgumentType]  # ty:ignore[no-matching-overload]

	def test_merge_with_three_dicts(self) -> None:
		D, kw = (self.D, self.kw)
		dicts = (D({2: 3, 5: 7}), D({2: 11, 5: 13}), D({2: 17}))
		assert merge_with(sum, *dicts, **kw) == D({2: 31, 5: 20})
		assert merge_with(tuple, *dicts, **kw) == D({2: (3, 11, 17), 5: (7, 13)})

	@pytest.mark.parametrize(
		('functionUnderTest', 'sourceMappingDefinition', 'expectedMappingDefinition'),
		(
			pytest.param(
				inc,
				{13: 21, 34: 55},
				{13: 22, 34: 56},
				id='increments each value',
			),
			pytest.param(
				str,
				{13: 21, 34: 55},
				{13: '21', 34: '55'},
				id='converts each value to text',
			),
		),
	)
	def test_valmap(
		self,
		functionUnderTest: Callable[[Any], Any],
		sourceMappingDefinition: dict[int, Any],
		expectedMappingDefinition: dict[int, Any],
	) -> None:
		mappingFactory: Callable[[dict[Any, Any]], Any] = self.D
		factoryKeywordArguments: dict[str, Any] = self.kw
		sourceMapping: Any = mappingFactory(sourceMappingDefinition)
		expectedMapping: Any = mappingFactory(expectedMappingDefinition)

		resultMapping: Any = valmap(functionUnderTest, sourceMapping, **factoryKeywordArguments)

		assert resultMapping == expectedMapping, (
			f'valmap returned {resultMapping}, expected {expectedMapping} for source '
			f'{sourceMappingDefinition}.'
		)
		assert sourceMapping == mappingFactory(sourceMappingDefinition), (
			f'valmap mutated source mapping {sourceMapping}, expected {sourceMappingDefinition}.'
		)
		assert resultMapping is not sourceMapping, (
			f'valmap returned source mapping {sourceMapping} instead of a new mapping for '
			f'{sourceMappingDefinition}.'
		)
		assert isinstance(resultMapping, type(expectedMapping)), (
			f'valmap returned {type(resultMapping).__name__}, expected '
			f'{type(expectedMapping).__name__} for source {sourceMappingDefinition}.'
		)

	@pytest.mark.parametrize(
		('functionUnderTest', 'sourceMappingDefinition', 'expectedMappingDefinition'),
		(
			pytest.param(
				inc,
				{13: 21, 34: 55},
				{14: 21, 35: 55},
				id='increments each key',
			),
			pytest.param(
				bucketKeyByParity,
				{13: 21, 34: 55, 55: 89},
				{1: 89, 0: 55},
				id='keeps last value when transformed keys collide',
			),
		),
	)
	def test_keymap(
		self,
		functionUnderTest: Callable[[Any], Any],
		sourceMappingDefinition: dict[int, Any],
		expectedMappingDefinition: dict[int, Any],
	) -> None:
		mappingFactory: Callable[[dict[Any, Any]], Any] = self.D
		factoryKeywordArguments: dict[str, Any] = self.kw
		sourceMapping: Any = mappingFactory(sourceMappingDefinition)
		expectedMapping: Any = mappingFactory(expectedMappingDefinition)

		resultMapping: Any = keymap(functionUnderTest, sourceMapping, **factoryKeywordArguments)

		assert resultMapping == expectedMapping, (
			f'keymap returned {resultMapping}, expected {expectedMapping} for source '
			f'{sourceMappingDefinition}.'
		)
		assert sourceMapping == mappingFactory(sourceMappingDefinition), (
			f'keymap mutated source mapping {sourceMapping}, expected {sourceMappingDefinition}.'
		)
		assert resultMapping is not sourceMapping, (
			f'keymap returned source mapping {sourceMapping} instead of a new mapping for '
			f'{sourceMappingDefinition}.'
		)
		assert isinstance(resultMapping, type(expectedMapping)), (
			f'keymap returned {type(resultMapping).__name__}, expected '
			f'{type(expectedMapping).__name__} for source {sourceMappingDefinition}.'
		)

	@pytest.mark.parametrize(
		('functionUnderTest', 'sourceMappingDefinition', 'expectedMappingDefinition'),
		(
			pytest.param(
				swapItemKeyWithValue,
				{13: 21, 34: 55},
				{21: 13, 55: 34},
				id='swaps keys with values',
			),
			pytest.param(
				summarizeItemToParityAndTotal,
				{13: 21, 34: 55, 55: 89},
				{1: 144, 0: 89},
				id='keeps last transformed item when keys collide',
			),
		),
	)
	def test_itemmap(
		self,
		functionUnderTest: Callable[[tuple[Any, Any]], tuple[Any, Any]],
		sourceMappingDefinition: dict[int, Any],
		expectedMappingDefinition: dict[int, Any],
	) -> None:
		mappingFactory: Callable[[dict[Any, Any]], Any] = self.D
		factoryKeywordArguments: dict[str, Any] = self.kw
		sourceMapping: Any = mappingFactory(sourceMappingDefinition)
		expectedMapping: Any = mappingFactory(expectedMappingDefinition)

		resultMapping: Any = itemmap(functionUnderTest, sourceMapping, **factoryKeywordArguments)

		assert resultMapping == expectedMapping, (
			f'itemmap returned {resultMapping}, expected {expectedMapping} for source '
			f'{sourceMappingDefinition}.'
		)
		assert sourceMapping == mappingFactory(sourceMappingDefinition), (
			f'itemmap mutated source mapping {sourceMapping}, expected {sourceMappingDefinition}.'
		)
		assert resultMapping is not sourceMapping, (
			f'itemmap returned source mapping {sourceMapping} instead of a new mapping for '
			f'{sourceMappingDefinition}.'
		)
		assert isinstance(resultMapping, type(expectedMapping)), (
			f'itemmap returned {type(resultMapping).__name__}, expected '
			f'{type(expectedMapping).__name__} for source {sourceMappingDefinition}.'
		)

	@pytest.mark.parametrize(
		('predicateUnderTest', 'sourceMappingDefinition', 'expectedMappingDefinition'),
		(
			pytest.param(
				iseven,
				{13: 21, 34: 144, 55: 233},
				{34: 144},
				id='keeps matching values',
			),
			pytest.param(
				valueExceedsThreeHundred,
				{13: 21, 34: 144, 55: 233},
				{},
				id='returns empty mapping when nothing matches',
			),
		),
	)
	def test_valfilter(
		self,
		predicateUnderTest: Callable[[Any], bool],
		sourceMappingDefinition: dict[int, Any],
		expectedMappingDefinition: dict[int, Any],
	) -> None:
		mappingFactory: Callable[[dict[Any, Any]], Any] = self.D
		factoryKeywordArguments: dict[str, Any] = self.kw
		sourceMapping: Any = mappingFactory(sourceMappingDefinition)
		expectedMapping: Any = mappingFactory(expectedMappingDefinition)

		resultMapping: Any = valfilter(predicateUnderTest, sourceMapping, **factoryKeywordArguments)

		assert resultMapping == expectedMapping, (
			f'valfilter returned {resultMapping}, expected {expectedMapping} for source '
			f'{sourceMappingDefinition}.'
		)
		assert sourceMapping == mappingFactory(sourceMappingDefinition), (
			f'valfilter mutated source mapping {sourceMapping}, expected {sourceMappingDefinition}.'
		)
		assert resultMapping is not sourceMapping, (
			f'valfilter returned source mapping {sourceMapping} instead of a new mapping for '
			f'{sourceMappingDefinition}.'
		)
		assert isinstance(resultMapping, type(expectedMapping)), (
			f'valfilter returned {type(resultMapping).__name__}, expected '
			f'{type(expectedMapping).__name__} for source {sourceMappingDefinition}.'
		)

	@pytest.mark.parametrize(
		('predicateUnderTest', 'sourceMappingDefinition', 'expectedMappingDefinition'),
		(
			pytest.param(
				iseven,
				{13: 21, 34: 55, 55: 89, 144: 233},
				{34: 55, 144: 233},
				id='keeps matching keys',
			),
			pytest.param(
				keyExceedsThreeHundred,
				{13: 21, 34: 55, 55: 89},
				{},
				id='returns empty mapping when no keys match',
			),
		),
	)
	def test_keyfilter(
		self,
		predicateUnderTest: Callable[[Any], bool],
		sourceMappingDefinition: dict[int, Any],
		expectedMappingDefinition: dict[int, Any],
	) -> None:
		mappingFactory: Callable[[dict[Any, Any]], Any] = self.D
		factoryKeywordArguments: dict[str, Any] = self.kw
		sourceMapping: Any = mappingFactory(sourceMappingDefinition)
		expectedMapping: Any = mappingFactory(expectedMappingDefinition)

		resultMapping: Any = keyfilter(predicateUnderTest, sourceMapping, **factoryKeywordArguments)

		assert resultMapping == expectedMapping, (
			f'keyfilter returned {resultMapping}, expected {expectedMapping} for source '
			f'{sourceMappingDefinition}.'
		)
		assert sourceMapping == mappingFactory(sourceMappingDefinition), (
			f'keyfilter mutated source mapping {sourceMapping}, expected {sourceMappingDefinition}.'
		)
		assert resultMapping is not sourceMapping, (
			f'keyfilter returned source mapping {sourceMapping} instead of a new mapping for '
			f'{sourceMappingDefinition}.'
		)
		assert isinstance(resultMapping, type(expectedMapping)), (
			f'keyfilter returned {type(resultMapping).__name__}, expected '
			f'{type(expectedMapping).__name__} for source {sourceMappingDefinition}.'
		)

	@pytest.mark.parametrize(
		('predicateUnderTest', 'sourceMappingDefinition', 'expectedMappingDefinition'),
		(
			pytest.param(
				itemHasEvenKeyAndOddValue,
				{13: 21, 34: 55, 55: 144, 144: 233},
				{34: 55, 144: 233},
				id='filters on both key and value',
			),
			pytest.param(
				itemHasLargeKeyAndLargeValue,
				{13: 21, 34: 55, 55: 144},
				{},
				id='returns empty mapping when no items match',
			),
		),
	)
	def test_itemfilter(
		self,
		predicateUnderTest: Callable[[tuple[Any, Any]], bool],
		sourceMappingDefinition: dict[int, Any],
		expectedMappingDefinition: dict[int, Any],
	) -> None:
		mappingFactory: Callable[[dict[Any, Any]], Any] = self.D
		factoryKeywordArguments: dict[str, Any] = self.kw
		sourceMapping: Any = mappingFactory(sourceMappingDefinition)
		expectedMapping: Any = mappingFactory(expectedMappingDefinition)

		resultMapping: Any = itemfilter(predicateUnderTest, sourceMapping, **factoryKeywordArguments)

		assert resultMapping == expectedMapping, (
			f'itemfilter returned {resultMapping}, expected {expectedMapping} for source '
			f'{sourceMappingDefinition}.'
		)
		assert sourceMapping == mappingFactory(sourceMappingDefinition), (
			f'itemfilter mutated source mapping {sourceMapping}, expected {sourceMappingDefinition}.'
		)
		assert resultMapping is not sourceMapping, (
			f'itemfilter returned source mapping {sourceMapping} instead of a new mapping for '
			f'{sourceMappingDefinition}.'
		)
		assert isinstance(resultMapping, type(expectedMapping)), (
			f'itemfilter returned {type(resultMapping).__name__}, expected '
			f'{type(expectedMapping).__name__} for source {sourceMappingDefinition}.'
		)

	@pytest.mark.parametrize(
		('sourceMappingDefinition', 'keyToAssociate', 'valueToAssociate', 'expectedMappingDefinition'),
		(
			pytest.param(
				{},
				'alpha',
				13,
				{'alpha': 13},
				id='associates into empty mapping',
			),
			pytest.param(
				{'alpha': 13, 'beta': 21},
				'beta',
				34,
				{'alpha': 13, 'beta': 34},
				id='replaces existing value',
			),
			pytest.param(
				{'alpha': 13, 'beta': 21},
				'gamma',
				55,
				{'alpha': 13, 'beta': 21, 'gamma': 55},
				id='preserves siblings when inserting',
			),
		),
	)
	def test_assoc(
		self,
		sourceMappingDefinition: dict[str, int],
		keyToAssociate: str,
		valueToAssociate: int,
		expectedMappingDefinition: dict[str, int],
	) -> None:
		mappingFactory: Callable[[dict[Any, Any]], Any] = self.D
		factoryKeywordArguments: dict[str, Any] = self.kw
		sourceMapping: Any = mappingFactory(sourceMappingDefinition)
		expectedMapping: Any = mappingFactory(expectedMappingDefinition)

		resultMapping: Any = assoc(sourceMapping, keyToAssociate, valueToAssociate, **factoryKeywordArguments)

		assert resultMapping == expectedMapping, (
			f'assoc returned {resultMapping}, expected {expectedMapping} for source '
			f'{sourceMappingDefinition}, key {keyToAssociate}, and value {valueToAssociate}.'
		)
		assert sourceMapping == mappingFactory(sourceMappingDefinition), (
			f'assoc mutated source mapping {sourceMapping}, expected {sourceMappingDefinition}.'
		)
		assert resultMapping is not sourceMapping, (
			f'assoc returned source mapping {sourceMapping} instead of a new mapping for '
			f'{sourceMappingDefinition}.'
		)
		assert isinstance(resultMapping, type(expectedMapping)), (
			f'assoc returned {type(resultMapping).__name__}, expected '
			f'{type(expectedMapping).__name__} for source {sourceMappingDefinition}.'
		)

	@pytest.mark.parametrize(
		('sourceMappingDefinition', 'keysToRemove', 'expectedMappingDefinition'),
		(
			pytest.param(
				{'north': 13, 'south': 21, 'east': 34},
				('south',),
				{'north': 13, 'east': 34},
				id='removes single key',
			),
			pytest.param(
				{'north': 13, 'south': 21, 'east': 34, 'west': 55},
				('north', 'west'),
				{'south': 21, 'east': 34},
				id='removes multiple keys',
			),
			pytest.param(
				{'alpha': 13, 'beta': 21, 'gamma': 34},
				('beta', 'omega'),
				{'alpha': 13, 'gamma': 34},
				id='ignores missing keys',
			),
			pytest.param(
				{'alpha': 13, 'beta': 21, 'gamma': 34, 'delta': 55, 'epsilon': 89},
				('alpha', 'beta', 'gamma'),
				{'delta': 55, 'epsilon': 89},
				id='removes sixty percent boundary',
			),
			pytest.param(
				{'alpha': 13, 'beta': 21, 'gamma': 34},
				(),
				{'alpha': 13, 'beta': 21, 'gamma': 34},
				id='keeps mapping when no keys provided',
			),
			pytest.param(
				{'north': 13, 'south': 21, 'east': 34},
				('south', 'north', 'south', 'east'),
				{},
				id='removes all keys even with duplicates',
			),
		),
	)
	def test_dissocRemovesKeys(
		self,
		sourceMappingDefinition: dict[str, int],
		keysToRemove: tuple[str, ...],
		expectedMappingDefinition: dict[str, int],
	) -> None:
		mappingFactory = self.D
		factoryKeywordArguments: dict[str, Callable[[], MutableMapping[str, int]]] = self.kw
		sourceMapping = mappingFactory(sourceMappingDefinition)
		expectedMapping = mappingFactory(expectedMappingDefinition)

		resultMapping = dissoc(sourceMapping, *keysToRemove, **factoryKeywordArguments)

		assert resultMapping == expectedMapping, (
			f'dissoc returned {resultMapping}, expected {expectedMapping} for keys {keysToRemove} '
			f'and source {sourceMappingDefinition}.'
		)
		assert sourceMapping == mappingFactory(sourceMappingDefinition), (
			f'dissoc mutated source mapping {sourceMapping} for keys {keysToRemove}, '
			f'expected {sourceMappingDefinition}.'
		)
		assert resultMapping is not sourceMapping, (
			f'dissoc returned {resultMapping} which is the same object as {sourceMapping} '
			f'for keys {keysToRemove} and source {sourceMappingDefinition}, expected a new mapping.'
		)
		factoryCallable: Callable[[], MutableMapping[str, int]]
		if 'factory' in factoryKeywordArguments:
			factoryCallable = factoryKeywordArguments['factory']
		else:

			def defaultFactory() -> dict[str, int]:
				return {}

			factoryCallable = defaultFactory

		expectedMappingType = type(factoryCallable())
		assert isinstance(resultMapping, expectedMappingType), (
			f'dissoc returned {type(resultMapping).__name__}, expected {expectedMappingType.__name__} '
			f'for keys {keysToRemove} and source {sourceMappingDefinition}.'
		)

		repeatedResultMapping = dissoc(resultMapping, *keysToRemove, **factoryKeywordArguments)
		assert repeatedResultMapping == resultMapping, (
			f'dissoc was not idempotent for keys {keysToRemove} and source '
			f'{sourceMappingDefinition}, got {repeatedResultMapping}.'
		)

	def test_assoc_in(self) -> None:
		D, kw = (self.D, self.kw)
		assert assoc_in(D({'a': 1}), ['a'], 2, **kw) == D({'a': 2})
		assert assoc_in(D({'a': D({'b': 1})}), ['a', 'b'], 2, **kw) == D({'a': D({'b': 2})})
		assert assoc_in(D({}), ['a', 'b'], 1, **kw) == D({'a': D({'b': 1})})
		d = D({'x': 1})
		oldd = d
		d2 = assoc_in(d, ['x'], 2, **kw)
		assert d is oldd
		assert d2 is not oldd
		# Three-level nesting and new key creation
		assert assoc_in(D({}), ['a', 'b', 'c'], 42, **kw) == D({'a': D({'b': D({'c': 42})})})
		# Existing nested mapping is not mutated
		inner = D({'b': 1})
		d3 = D({'a': inner})
		d4 = assoc_in(d3, ['a', 'b'], 99, **kw)
		assert inner['b'] == 1
		assert d4['a']['b'] == 99
		# Sibling keys at outer level are preserved
		assert assoc_in(D({'a': 1, 'b': 2}), ['a'], 99, **kw) == D({'a': 99, 'b': 2})

	def test_get_in(self) -> None:
		transaction: Any = {
			'name': 'Alice',
			'purchase': {'items': ['Apple', 'Orange'], 'costs': [0.50, 1.25]},
			'credit card': '5555-1234-1234-1234',
		}
		assert get_in(['name'], transaction) == 'Alice'
		assert get_in(['purchase', 'items', 0], transaction) == 'Apple'  # ty:ignore[invalid-argument-type]
		assert get_in(['purchase', 'total'], transaction) is None
		assert get_in(['purchase', 'total'], transaction, 0) == 0
		assert get_in(['purchase', 'items', 'apple'], transaction) is None
		assert get_in(['purchase', 'items', 10], transaction) is None  # ty:ignore[invalid-argument-type]
		assert get_in([], transaction) is transaction
		assert get_in(['purchase'], transaction) == {'items': ['Apple', 'Orange'], 'costs': [0.50, 1.25]}

	def test_update_in(self) -> None:
		D, kw = (self.D, self.kw)
		assert update_in(D({'a': 0}), ['a'], inc, **kw) == D({'a': 1})
		assert update_in(D({'a': 0, 'b': 1}), ['b'], str, **kw) == D({'a': 0, 'b': '1'})
		assert update_in(D({'t': 1, 'v': D({'a': 0})}), ['v', 'a'], inc, **kw) == D({'t': 1, 'v': D({'a': 1})})
		assert update_in(D({}), ['z'], str, None, **kw) == D({'z': 'None'})
		assert update_in(D({}), ['z'], inc, 0, **kw) == D({'z': 1})
		assert update_in(D({}), ['z'], lambda x: x + 'ar', default='b', **kw) == D({'z': 'bar'})
		assert update_in(D({}), [0, 1], inc, default=-1, **kw) == D({0: D({1: 0})})
		assert update_in(D({}), [0, 1], str, default=100, **kw) == D({0: D({1: '100'})})
		assert update_in(D({'foo': 'bar', 1: 50}), ['d', 1, 0], str, 20, **kw) == D({'foo': 'bar', 1: 50, 'd': D({1: D({0: '20'})})})
		# Original mapping is not mutated
		d = D({'x': 1})
		oldd = d
		d2 = update_in(d, ['x'], inc, **kw)
		assert d is oldd
		assert d2 is not oldd
		# Sibling keys at outer level are preserved
		assert update_in(D({'a': 1, 'b': 2}), ['a'], inc, **kw) == D({'a': 2, 'b': 2})
		# Existing nested mapping is not mutated
		inner = D({'b': 1})
		d3 = D({'a': inner})
		d4 = update_in(d3, ['a', 'b'], inc, **kw)
		assert inner['b'] == 1
		assert d4['a']['b'] == 2

	@pytest.mark.parametrize(
		('dictsDefinition', 'expectedMappingDefinition'),
		(
			pytest.param(
				[{2: 'north', 5: 'south'}, {3: 'east', 7: 'west'}],
				{2: 'north', 3: 'east', 5: 'south', 7: 'west'},
				id='non-overlapping keys from both dicts are preserved',
			),
			pytest.param(
				[{2: 'north', 5: 'south'}, {5: 'southeast'}],
				{2: 'north', 5: 'southeast'},
				id='last dict value takes precedence for repeated key',
			),
			pytest.param(
				[{}, {3: 'east'}],
				{3: 'east'},
				id='leading empty dict does not alter result',
			),
			pytest.param(
				[{2: 'north'}, {}],
				{2: 'north'},
				id='trailing empty dict does not alter result',
			),
		),
	)
	def test_mergeProducesExpectedResult(
		self,
		dictsDefinition: list[dict[Any, Any]],
		expectedMappingDefinition: dict[Any, Any],
	) -> None:
		mappingFactory: Callable[[dict[Any, Any]], Any] = self.D
		factoryKeywordArguments: dict[str, Any] = self.kw
		sourceMappings: list[Any] = [mappingFactory(d) for d in dictsDefinition]
		expectedMapping: Any = mappingFactory(expectedMappingDefinition)

		resultMapping: Any = merge(*sourceMappings, **factoryKeywordArguments)

		assert resultMapping == expectedMapping, (
			f'merge returned {resultMapping}, expected {expectedMapping} for inputs {dictsDefinition}.'
		)
		assert resultMapping is not sourceMappings[0], (
			f'merge returned the first source mapping instead of a new mapping for {dictsDefinition}.'
		)
		for sourceMapping, originalDefinition in zip(sourceMappings, dictsDefinition, strict=True):
			assert sourceMapping == mappingFactory(originalDefinition), (
				f'merge mutated source mapping {sourceMapping}, expected {originalDefinition}.'
			)

	@pytest.mark.parametrize(
		('aggregationFunc', 'dictsDefinition', 'expectedMappingDefinition'),
		(
			pytest.param(
				max,
				[{2: 3, 5: 7}, {2: 11, 5: 2}],
				{2: 11, 5: 7},
				id='max selects largest value per key',
			),
			pytest.param(
				min,
				[{2: 3, 5: 7}, {2: 11, 5: 2}],
				{2: 3, 5: 2},
				id='min selects smallest value per key',
			),
			pytest.param(
				sum,
				[{2: 3, 5: 7}, {2: 11}, {5: 13}],
				{2: 14, 5: 20},
				id='sum adds values across three dicts including keys present in only a subset',
			),
		),
	)
	def test_mergeWithAggregatesValues(
		self,
		aggregationFunc: Callable[[list[Any]], Any],
		dictsDefinition: list[dict[Any, Any]],
		expectedMappingDefinition: dict[Any, Any],
	) -> None:
		mappingFactory: Callable[[dict[Any, Any]], Any] = self.D
		factoryKeywordArguments: dict[str, Any] = self.kw
		sourceMappings: list[Any] = [mappingFactory(d) for d in dictsDefinition]
		expectedMapping: Any = mappingFactory(expectedMappingDefinition)

		resultMapping: Any = merge_with(aggregationFunc, *sourceMappings, **factoryKeywordArguments)

		assert resultMapping == expectedMapping, (
			f'merge_with returned {resultMapping}, expected {expectedMapping} for inputs {dictsDefinition}.'
		)
		for sourceMapping, originalDefinition in zip(sourceMappings, dictsDefinition, strict=True):
			assert sourceMapping == mappingFactory(originalDefinition), (
				f'merge_with mutated source mapping {sourceMapping}, expected {originalDefinition}.'
			)

	@pytest.mark.parametrize(
		('sourceMappingDefinition', 'keysPath', 'valueToAssoc', 'expectedMappingDefinition'),
		(
			pytest.param(
				{'alpha': 13, 'beta': 21},
				['alpha'],
				34,
				{'alpha': 34, 'beta': 21},
				id='replaces value at single-key path while preserving siblings',
			),
			pytest.param(
				{'alpha': 21, 'gamma': 55},
				['beta'],
				34,
				{'alpha': 21, 'beta': 34, 'gamma': 55},
				id='inserts new key without altering existing keys',
			),
			pytest.param(
				{},
				['alpha'],
				144,
				{'alpha': 144},
				id='creates key in empty mapping',
			),
		),
	)
	def test_assocInUpdatesAtPath(
		self,
		sourceMappingDefinition: dict[str, Any],
		keysPath: list[str],
		valueToAssoc: Any,
		expectedMappingDefinition: dict[str, Any],
	) -> None:
		mappingFactory: Callable[[dict[Any, Any]], Any] = self.D
		factoryKeywordArguments: dict[str, Any] = self.kw
		sourceMapping: Any = mappingFactory(sourceMappingDefinition)
		expectedMapping: Any = mappingFactory(expectedMappingDefinition)

		resultMapping: Any = assoc_in(sourceMapping, keysPath, valueToAssoc, **factoryKeywordArguments)

		assert resultMapping == expectedMapping, (
			f'assoc_in returned {resultMapping}, expected {expectedMapping} '
			f'for keys={keysPath!r}, value={valueToAssoc!r}, source={sourceMappingDefinition}.'
		)
		assert sourceMapping == mappingFactory(sourceMappingDefinition), (
			f'assoc_in mutated source mapping for keys={keysPath!r}, value={valueToAssoc!r}.'
		)
		assert resultMapping is not sourceMapping, (
			f'assoc_in returned the source mapping instead of a new mapping for keys={keysPath!r}.'
		)

	@pytest.mark.parametrize(
		('sourceMappingDefinition', 'keysPath', 'funcToApply', 'defaultValue', 'expectedMappingDefinition'),
		(
			pytest.param(
				{'alpha': 13, 'beta': 21},
				['alpha'],
				inc,
				None,
				{'alpha': 14, 'beta': 21},
				id='applies func to existing value and preserves siblings',
			),
			pytest.param(
				{},
				['alpha'],
				inc,
				21,
				{'alpha': 22},
				id='applies func to default when key is absent',
			),
			pytest.param(
				{'alpha': 13, 'beta': 21},
				['beta'],
				str,
				None,
				{'alpha': 13, 'beta': '21'},
				id='applies str to value at named key',
			),
			pytest.param(
				{'alpha': 34},
				['gamma'],
				inc,
				55,
				{'alpha': 34, 'gamma': 56},
				id='applies func to default for absent key while preserving existing keys',
			),
		),
	)
	def test_updateInAppliesFuncAtPath(
		self,
		sourceMappingDefinition: dict[str, Any],
		keysPath: list[str],
		funcToApply: Callable[[Any], Any],
		defaultValue: Any,
		expectedMappingDefinition: dict[str, Any],
	) -> None:
		mappingFactory: Callable[[dict[Any, Any]], Any] = self.D
		factoryKeywordArguments: dict[str, Any] = self.kw
		sourceMapping: Any = mappingFactory(sourceMappingDefinition)
		expectedMapping: Any = mappingFactory(expectedMappingDefinition)

		resultMapping: Any = update_in(sourceMapping, keysPath, funcToApply, defaultValue, **factoryKeywordArguments) # pyright: ignore[reportUnknownVariableType]

		assert resultMapping == expectedMapping, (
			f'update_in returned {resultMapping}, expected {expectedMapping} '
			f'for keys={keysPath!r}, func={funcToApply.__name__!r}, default={defaultValue!r}, '  # ty:ignore[unresolved-attribute]
			f'source={sourceMappingDefinition}.'
		)
		assert sourceMapping == mappingFactory(sourceMappingDefinition), (
			f'update_in mutated source mapping for keys={keysPath!r}, func={funcToApply.__name__!r}.'  # ty:ignore[unresolved-attribute]
		)
		assert resultMapping is not sourceMapping, (
			f'update_in returned the source mapping instead of a new mapping for keys={keysPath!r}.'
		)

	def test_factory(self) -> None:
		D, _kw = (self.D, self.kw)
		assert merge(defaultdict(int, D({1: 2})), D({2: 3})) == {1: 2, 2: 3}
		assert merge(defaultdict(int, D({1: 2})), D({2: 3}), factory=lambda: defaultdict(int)) == defaultdict(int, D({1: 2, 2: 3}))
		assert not merge(defaultdict(int, D({1: 2})), D({2: 3}), factory=lambda: defaultdict(int)) == {1: 2, 2: 3}
		assert raises(TypeError, lambda: merge(D({1: 2}), D({2: 3}), factoryy=dict))  # pyright: ignore[reportCallIssue, reportUnknownLambdaType]  # ty:ignore[no-matching-overload]

class defaultdict[KeyType, ValueType](_defaultdict[KeyType, ValueType]):

	__hash__ = None  # pyright: ignore[reportAssignmentType]

	def __eq__(self, other: object) -> bool:
		return super().__eq__(other) and isinstance(other, _defaultdict) and (self.default_factory == other.default_factory)

class TestDefaultDict(TestDict):
	"""Test defaultdict as input and factory

	Class attributes:
		D: callable that inputs a dict and creates or returns a MutableMapping
		kw: kwargs dict to specify "factory" keyword (if applicable)
	"""

	@staticmethod
	def D(dict_: dict[Any, Any]) -> defaultdict[Any, Any]:
		return defaultdict(int, dict_)
	kw: ClassVar[dict[str, Callable[[], defaultdict[Any, Any]]]] = {'factory': makeDefaultDictFactory}

class CustomMapping:
	"""Define methods of the MutableMapping protocol required by dicttoolz"""

	__hash__ = None  # pyright: ignore[reportAssignmentType]

	def __init__(self, *args: Any, **kwargs: Any) -> None:
		self._d = dict(*args, **kwargs)

	def __getitem__(self, key: Any) -> Any:
		return self._d[key]

	def __setitem__(self, key: Any, val: Any) -> None:
		self._d[key] = val

	def __delitem__(self, key: Any) -> None:
		del self._d[key]

	def __iter__(self) -> Iterator[Any]:
		return iter(self._d)

	def __len__(self) -> int:
		return len(self._d)

	def __contains__(self, key: object) -> bool:
		return key in self._d

	def __eq__(self, other: object) -> bool:
		return isinstance(other, CustomMapping) and self._d == other._d

	def __ne__(self, other: object) -> bool:
		return not isinstance(other, CustomMapping) or self._d != other._d

	def keys(self) -> KeysView[Any]:
		return self._d.keys()

	def values(self) -> ValuesView[Any]:
		return self._d.values()

	def items(self) -> ItemsView[Any, Any]:
		return self._d.items()

	def update(self, *args: Any, **kwargs: Any) -> None:
		self._d.update(*args, **kwargs)

	def get(self, key, *args):
		return self._d.get(key, *args)

class TestCustomMapping(TestDict):
	"""Test CustomMapping as input and factory

	Class attributes:
		D: callable that inputs a dict and creates or returns a MutableMapping
		kw: kwargs dict to specify "factory" keyword (if applicable)
	"""
	D: ClassVar[Callable[..., Any]] = CustomMapping
	kw: ClassVar[dict[str, Any]] = {'factory': makeCustomMappingFactory}

@pytest.mark.parametrize(
	('keys', 'coll', 'expectedValue'),
	(
		pytest.param(
			['alpha'],
			{'alpha': 13, 'beta': 21},
			13,
			id='retrieves value at single-key path',
		),
		pytest.param(
			['alpha', 'beta'],
			{'alpha': {'beta': 34}, 'gamma': 55},
			34,
			id='retrieves value at two-key nested path',
		),
		pytest.param(
			['alpha', 'beta', 'gamma'],
			{'alpha': {'beta': {'gamma': 89}, 'delta': 144}, 'epsilon': 233},
			89,
			id='retrieves value at three-key nested path',
		),
		pytest.param(
			[2],
			[3, 5, 7, 11, 13],
			7,
			id='retrieves value at integer index in list',
		),
	),
)
def test_get_in_retrieves_value_at_path(
	keys: list[Any],
	coll: Any,
	expectedValue: Any,
) -> None:
	result: Any = get_in(keys, coll)
	assert result == expectedValue, (
		f'get_in returned {result!r}, expected {expectedValue!r} for keys={keys!r}.'
	)

@pytest.mark.parametrize(
	('keys', 'coll', 'defaultValue', 'expectedValue'),
	(
		pytest.param(
			['alpha'],
			{},
			13,
			13,
			id='returns default for missing single key',
		),
		pytest.param(
			['alpha', 'beta'],
			{'alpha': {}},
			21,
			21,
			id='returns default when intermediate mapping lacks final key',
		),
		pytest.param(
			['alpha', 'beta'],
			{},
			34,
			34,
			id='returns default when first key absent in two-key path',
		),
		pytest.param(
			['alpha'],
			{'beta': 55},
			None,
			None,
			id='returns None when key absent and no default provided',
		),
	),
)
def test_get_in_returns_default_for_missing_path(
	keys: list[Any],
	coll: dict[str, Any],
	defaultValue: Any,
	expectedValue: Any,
) -> None:
	result: Any = get_in(keys, coll, defaultValue)
	assert result == expectedValue, (
		f'get_in returned {result!r}, expected {expectedValue!r} '
		f'for keys={keys!r} with default={defaultValue!r}.'
	)

@pytest.mark.parametrize(
	('sourceMappingDefinition', 'keysPath', 'valueToAssoc', 'expectedMappingDefinition'),
	(
		pytest.param(
			{},
			['alpha', 'beta'],
			21,
			{'alpha': {'beta': 21}},
			id='creates two-level nested path in empty mapping',
		),
		pytest.param(
			{},
			['alpha', 'beta', 'gamma'],
			34,
			{'alpha': {'beta': {'gamma': 34}}},
			id='creates three-level nested path in empty mapping',
		),
		pytest.param(
			{'alpha': {'beta': 55, 'gamma': 89}},
			['alpha', 'beta'],
			144,
			{'alpha': {'beta': 144, 'gamma': 89}},
			id='replaces value at two-key path while preserving nested siblings',
		),
	),
)
def test_assoc_in_nested_paths(
	sourceMappingDefinition: dict[str, Any],
	keysPath: list[str],
	valueToAssoc: Any,
	expectedMappingDefinition: dict[str, Any],
) -> None:
	result: Any = assoc_in(sourceMappingDefinition, keysPath, valueToAssoc)
	assert result == expectedMappingDefinition, (
		f'assoc_in returned {result}, expected {expectedMappingDefinition} '
		f'for keys={keysPath!r}, value={valueToAssoc!r}, source={sourceMappingDefinition}.'
	)
	assert result is not sourceMappingDefinition, (
		f'assoc_in returned the source mapping instead of a new mapping for keys={keysPath!r}.'
	)

@pytest.mark.parametrize(
	('sourceMappingDefinition', 'keysPath', 'funcToApply', 'defaultValue', 'expectedMappingDefinition'),
	(
		pytest.param(
			{'alpha': {'beta': 34}},
			['alpha', 'beta'],
			inc,
			None,
			{'alpha': {'beta': 35}},
			id='applies func at two-level nested path to existing value',
		),
		pytest.param(
			{},
			['alpha', 'beta'],
			inc,
			21,
			{'alpha': {'beta': 22}},
			id='creates two-level nested path and applies func to default',
		),
		pytest.param(
			{'alpha': {'beta': 55, 'gamma': 89}},
			['alpha', 'beta'],
			str,
			None,
			{'alpha': {'beta': '55', 'gamma': 89}},
			id='applies func at two-level path while preserving nested siblings',
		),
	),
)
def test_update_in_nested_paths(
	sourceMappingDefinition: dict[str, Any],
	keysPath: list[str],
	funcToApply: Callable[[Any], Any],
	defaultValue: Any,
	expectedMappingDefinition: dict[str, Any],
) -> None:
	result: Any = update_in(sourceMappingDefinition, keysPath, funcToApply, defaultValue)
	assert result == expectedMappingDefinition, (
		f'update_in returned {result}, expected {expectedMappingDefinition} '
		f'for keys={keysPath!r}, func={funcToApply.__name__!r}, default={defaultValue!r}, '  # ty:ignore[unresolved-attribute]
		f'source={sourceMappingDefinition}.'
	)
	assert result is not sourceMappingDefinition, (
		f'update_in returned the source dict instead of a new mapping for keys={keysPath!r}.'
	)

def test_get_in_no_default() -> None:
	with pytest.raises(KeyError):
		get_in(['y'], {}, no_default=True)
	with pytest.raises(IndexError):
		get_in([0], [], no_default=True)  # pyright: ignore[reportArgumentType]  # ty:ignore[no-matching-overload]
	with pytest.raises(TypeError):
		get_in(['x', 0], {'x': 42}, no_default=True)  # ty:ignore[no-matching-overload]

def test_get_in_empty_keys() -> None:
	coll: dict[str, int] = {'a': 1}
	assert get_in([], coll) is coll

def test_environ() -> None:
	assert keymap(identity, os.environ) == os.environ
	assert valmap(identity, os.environ) == os.environ
	assert itemmap(identity, os.environ) == os.environ

def test_merge_with_non_dict_mappings() -> None:

	class Foo(Mapping[int, int]):

		def __init__(self, d: dict[int, int]) -> None:
			self.d: dict[int, int] = d

		def __iter__(self) -> Iterator[int]:
			return iter(self.d)

		def __getitem__(self, key: int) -> int:
			return self.d[key]

		def __len__(self) -> int:
			return len(self.d)

	d = Foo({1: 1})
	assert merge(d) is d or merge(d) == {1: 1}
	assert merge_with(sum, d) == {1: 1}
