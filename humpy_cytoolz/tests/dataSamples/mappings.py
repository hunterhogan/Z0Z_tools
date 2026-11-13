"""Kinds of mapping that take each branch `dicttoolz` has for its input, and factories that create its results.

`dicttoolz` reads an exact `dict` with `PyDict_Next` and every other mapping through `items()`, and it fills a result
that is an exact `dict` with `PyDict_Update` and every other result through `update` and item assignment. Each member of
`boxOfMappingKinds` builds a mapping of its kind from a `dict`; each member of `boxOfFactories` creates an empty result.
"""
from __future__ import annotations

from collections import defaultdict, OrderedDict, UserDict
from collections.abc import MutableMapping
from functools import partial
from types import MappingProxyType
from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
	from _pytest.mark.structures import ParameterSet
	from collections.abc import ItemsView, Iterator, KeysView, Mapping, ValuesView

class CustomMapping[文件, 文义]:
	"""Mapping that implements only the methods `dicttoolz` calls, inherits from nothing, and equals what its items equal.

	`MutableMapping.register` makes it a `MutableMapping` by `isinstance`, as `merge` requires of a single argument.
	"""

	__hash__ = None  # pyright: ignore[reportAssignmentType]

	def __init__(self, *args: Mapping[文件, 文义]) -> None:
		self.dictionary: dict[文件, 文义] = dict(*args)

	def __getitem__(self, key: 文件) -> 文义:
		return self.dictionary[key]

	def __setitem__(self, key: 文件, value: 文义) -> None:
		self.dictionary[key] = value

	def __delitem__(self, key: 文件) -> None:
		del self.dictionary[key]

	def __iter__(self) -> Iterator[文件]:
		return iter(self.dictionary)

	def __len__(self) -> int:
		return len(self.dictionary)

	def __contains__(self, key: object) -> bool:
		return key in self.dictionary

	def __eq__(self, other: object) -> bool:
		return self.dictionary == other

	def __repr__(self) -> str:
		return f'{type(self).__name__}({self.dictionary!r})'

	def keys(self) -> KeysView[文件]:
		return self.dictionary.keys()

	def values(self) -> ValuesView[文义]:
		return self.dictionary.values()

	def items(self) -> ItemsView[文件, 文义]:
		return self.dictionary.items()

	def update(self, other: Mapping[文件, 文义]) -> None:
		self.dictionary.update(other)

	def get(self, key: 文件, default: 文义 | None = None) -> 文义 | None:
		return self.dictionary.get(key, default)

MutableMapping.register(CustomMapping)  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]

boxOfMappingKinds: tuple[ParameterSet, ...] = (
	pytest.param(dict, id='dict'),
	pytest.param(OrderedDict, id='OrderedDict'),
	pytest.param(partial(defaultdict[object, int], int), id='defaultdictInt'),
	pytest.param(MappingProxyType, id='MappingProxyType'),
	pytest.param(UserDict, id='UserDict'),
	pytest.param(CustomMapping, id='CustomMapping'),
)

boxOfFactories: tuple[ParameterSet, ...] = (
	pytest.param(dict, id='factoryDict'),
	pytest.param(OrderedDict, id='factoryOrderedDict'),
	pytest.param(partial(defaultdict[object, int], int), id='factoryDefaultdictInt'),
	pytest.param(UserDict, id='factoryUserDict'),
	pytest.param(CustomMapping, id='factoryCustomMapping'),
)
