# ruff:file-ignore[undocumented-public-module, undocumented-public-function]
from __future__ import annotations

from typing import overload, TYPE_CHECKING
import humpy_toolz

if TYPE_CHECKING:
	from collections.abc import Callable, Hashable, Mapping, MutableMapping

@overload
def merge_with[K: Hashable, V]() -> Callable[..., dict[K, V] | MutableMapping[K, V]]: ...
@overload
def merge_with[K: Hashable, V](func: Callable[[list[V]], V], /) -> Callable[..., dict[K, V] | MutableMapping[K, V]]: ...
@overload
def merge_with[V, K](func: Callable[[list[V]], V], d: Mapping[K, V], /) -> dict[K, V]: ...
@overload
def merge_with[V, K](func: Callable[[list[V]], V], d: Mapping[K, V], d2: Mapping[K, V], /, *dicts: Mapping[K, V]) -> dict[K, V]: ...
@overload
def merge_with[V, K](
	func: Callable[[list[V]], V], d: Mapping[K, V], d2: Mapping[K, V], /, *dicts: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]]
) -> MutableMapping[K, V]: ...
@overload
def merge_with[V, K](func: Callable[[list[V]], V], /, *, factory: Callable[[], MutableMapping[K, V]]) -> Callable[..., MutableMapping[K, V]]: ...
@humpy_toolz.functoolz.curry
def merge_with[V, K](
	func: Callable[[list[V]], V], d: Mapping[K, V], *dicts: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]] = dict
) -> MutableMapping[K, V]:
	return humpy_toolz.merge_with(func, d, *dicts, factory=factory)

@overload
def merge[K: Hashable, V]() -> Callable[..., dict[K, V] | MutableMapping[K, V]]: ...
@overload
def merge[K: Hashable, V](d: Mapping[K, V], /) -> dict[K, V]: ...
@overload
def merge[K: Hashable, V](d: Mapping[K, V], d2: Mapping[K, V], /, *dicts: Mapping[K, V]) -> dict[K, V]: ...
@overload
def merge[K: Hashable, V](
	d: Mapping[K, V], d2: Mapping[K, V], /, *dicts: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]]
) -> MutableMapping[K, V]: ...
@overload
def merge[K: Hashable, V](*, factory: Callable[[], MutableMapping[K, V]]) -> Callable[..., MutableMapping[K, V]]: ...
@humpy_toolz.functoolz.curry
def merge[K: Hashable, V](d: Mapping[K, V], *dicts: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
	return humpy_toolz.merge(d, *dicts, factory=factory)

merge_with.__doc__ = humpy_toolz.merge_with.__doc__
merge.__doc__ = humpy_toolz.merge.__doc__
del overload
