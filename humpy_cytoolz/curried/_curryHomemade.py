from __future__ import annotations

from typing import TYPE_CHECKING
import humpy_cytoolz

if TYPE_CHECKING:
	from collections.abc import Callable, Mapping, MutableMapping
	from optype import CanHash

__all__ = ['merge', 'merge_with']

@humpy_cytoolz.curry
def merge[Key: CanHash, Value](
	d: Mapping[Key, Value], *dicts: Mapping[Key, Value], factory: Callable[[], MutableMapping[Key, Value]] = dict
) -> MutableMapping[Key, Value]:
	return humpy_cytoolz.merge(d, *dicts, factory=factory)

@humpy_cytoolz.curry
def merge_with[Key: CanHash, Value, ValueResult](
	func: Callable[[list[Value]], ValueResult], d: Mapping[Key, Value], *dicts: Mapping[Key, Value]
	, factory: Callable[[], MutableMapping[Key, ValueResult]] = dict
) -> MutableMapping[Key, ValueResult]:
	return humpy_cytoolz.merge_with(func, d, *dicts, factory=factory)
merge.__doc__ = humpy_cytoolz.merge.__doc__
merge_with.__doc__ = humpy_cytoolz.merge_with.__doc__
