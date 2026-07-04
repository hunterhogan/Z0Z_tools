from __future__ import annotations

from typing import overload as __overload, TYPE_CHECKING, TypeVar as __TypeVar
import humpy_toolz

if TYPE_CHECKING:
	from collections.abc import Callable, Mapping, MutableMapping

K = __TypeVar('K')
V = __TypeVar('V')

@__overload
def merge_with() -> Callable[..., dict[K, V] | MutableMapping[K, V]]: ...
@__overload
def merge_with(func: Callable[[list[V]], V], /) -> Callable[..., dict[K, V] | MutableMapping[K, V]]: ...
@__overload
def merge_with(func: Callable[[list[V]], V], d: Mapping[K, V], /) -> dict[K, V]: ...
@__overload
def merge_with(func: Callable[[list[V]], V], d: Mapping[K, V], d2: Mapping[K, V], /, *dicts: Mapping[K, V]) -> dict[K, V]: ...
@__overload
def merge_with(
	func: Callable[[list[V]], V], d: Mapping[K, V], d2: Mapping[K, V], /, *dicts: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]]
) -> MutableMapping[K, V]: ...
@__overload
def merge_with(func: Callable[[list[V]], V], /, *, factory: Callable[[], MutableMapping[K, V]]) -> Callable[..., MutableMapping[K, V]]: ...
@humpy_toolz.curry
def merge_with(
	func: Callable[[list[V]], V], d: Mapping[K, V], *dicts: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]] = dict
) -> MutableMapping[K, V]:
	return humpy_toolz.merge_with(func, d, *dicts, factory=factory)

@__overload
def merge() -> Callable[..., dict[K, V] | MutableMapping[K, V]]: ...
@__overload
def merge(d: Mapping[K, V], /) -> dict[K, V]: ...
@__overload
def merge(d: Mapping[K, V], d2: Mapping[K, V], /, *dicts: Mapping[K, V]) -> dict[K, V]: ...
@__overload
def merge(
	d: Mapping[K, V], d2: Mapping[K, V], /, *dicts: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]]
) -> MutableMapping[K, V]: ...
@__overload
def merge(*, factory: Callable[[], MutableMapping[K, V]]) -> Callable[..., MutableMapping[K, V]]: ...
@humpy_toolz.curry
def merge(d: Mapping[K, V], *dicts: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
	return humpy_toolz.merge(d, *dicts, factory=factory)

merge_with.__doc__ = humpy_toolz.merge_with.__doc__
merge.__doc__ = humpy_toolz.merge.__doc__
del __overload
del __TypeVar
