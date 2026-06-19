from collections.abc import Callable, Iterable, Iterator
from typing import Any, TypeVar

K = TypeVar('K')
T = TypeVar('T')


__all__ = ("countby", "partitionby")

def countby(
	key: Callable[[T], K], seq: Iterable[T]
) -> dict[K, int]:
	...

def partitionby(
	func: Callable[[T], Any], seq: Iterable[T]
) -> Iterator[tuple[T, ...]]:
	...
