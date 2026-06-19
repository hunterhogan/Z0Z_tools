from collections.abc import Callable, Mapping, MutableMapping
from typing import overload, TypeVar
K = TypeVar('K')
V = TypeVar('V')


__all__ = ["merge", "merge_with"]

@overload
def merge_with() -> Callable[
	..., dict[K, V] | MutableMapping[K, V]
]: ...
@overload
def merge_with(
	func: Callable[[list[V]], V], /
) -> Callable[..., dict[K, V] | MutableMapping[K, V]]: ...
@overload
def merge_with(
	func: Callable[[list[V]], V],
	d: Mapping[K, V],
	/,
) -> dict[K, V]: ...
@overload
def merge_with(
	func: Callable[[list[V]], V],
	d: Mapping[K, V],
	d2: Mapping[K, V],
	/,
	*dicts: Mapping[K, V],
) -> dict[K, V]: ...
@overload
def merge_with(
	func: Callable[[list[V]], V],
	d: Mapping[K, V],
	d2: Mapping[K, V],
	/,
	*dicts: Mapping[K, V],
	factory: Callable[[], MutableMapping[K, V]],
) -> MutableMapping[K, V]: ...
@overload
def merge_with(
	func: Callable[[list[V]], V],
	/,
	*,
	factory: Callable[[], MutableMapping[K, V]],
) -> Callable[..., MutableMapping[K, V]]: ...
def merge_with(
	func: Callable[[list[V]], V] = ...,
	d: Mapping[K, V] = ...,
	*dicts: Mapping[K, V],
	factory: Callable[[], MutableMapping[K, V]] = ...,
) -> (
	dict[K, V]
	| MutableMapping[K, V]
	| Callable[..., dict[K, V] | MutableMapping[K, V]]
):
	...

@overload
def merge() -> Callable[
	..., dict[K, V] | MutableMapping[K, V]
]: ...
@overload
def merge(d: Mapping[K, V], /) -> dict[K, V]: ...
@overload
def merge(
	d: Mapping[K, V],
	d2: Mapping[K, V],
	/,
	*dicts: Mapping[K, V],
) -> dict[K, V]: ...
@overload
def merge(
	d: Mapping[K, V],
	d2: Mapping[K, V],
	/,
	*dicts: Mapping[K, V],
	factory: Callable[[], MutableMapping[K, V]],
) -> MutableMapping[K, V]: ...
@overload
def merge(
	*,
	factory: Callable[[], MutableMapping[K, V]],
) -> Callable[..., MutableMapping[K, V]]: ...
def merge(
	d: Mapping[K, V] = ...,
	*dicts: Mapping[K, V],
	factory: Callable[[], MutableMapping[K, V]] = ...,
) -> (
	dict[K, V]
	| MutableMapping[K, V]
	| Callable[..., dict[K, V] | MutableMapping[K, V]]
):
	...
