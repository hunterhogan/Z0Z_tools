# See #166: https://github.com/pytoolz/toolz/issues/166
# See #173: https://github.com/pytoolz/toolz/pull/173
from collections.abc import Callable, Hashable, Iterable, Iterator
from typing import overload, TypeVar
from typing_extensions import override
T = TypeVar('T')
T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')


class EqualityHashKey:
	def __init__(
		self, key: Callable[[T], Hashable] | int | None, item: T
	) -> None: ...
	@override
	def __hash__(self) -> int: ...
	@override
	def __eq__(self, other: object) -> bool: ...
	@override
	def __ne__(self, other: object) -> bool: ...

# See issue #293: https://github.com/pytoolz/toolz/issues/239
@overload
def unzip(seq: Iterable[tuple[()]]) -> tuple[()]: ...
@overload
def unzip(
	seq: Iterable[tuple[T1]],
) -> tuple[Iterator[T1]]: ...
@overload
def unzip(
	seq: Iterable[tuple[T1, T2]],
) -> tuple[Iterator[T1], Iterator[T2]]: ...
@overload
def unzip(
	seq: Iterable[tuple[T1, T2, T3]],
) -> tuple[
	Iterator[T1],
	Iterator[T2],
	Iterator[T3],
]: ...
@overload
def unzip(
	seq: Iterable[tuple[T1, T2, T3, T4]],
) -> tuple[
	Iterator[T1],
	Iterator[T2],
	Iterator[T3],
	Iterator[T4],
]: ...
@overload
def unzip(
	seq: Iterable[tuple[T, ...]],
) -> tuple[Iterator[T], ...]: ...

# Implementation signature
def unzip(
	seq: Iterable[tuple[T, ...]],
) -> tuple[Iterator[T], ...]:
	...
