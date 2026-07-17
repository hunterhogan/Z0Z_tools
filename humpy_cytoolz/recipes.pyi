
from collections.abc import Callable, Hashable, Iterable, Iterator
from typing import Any

__all__ = ('countby', 'partitionby')

def countby[T, K: Hashable](key: Callable[[T], K] | K, seq: Iterable[T]) -> dict[K, int]:
    ...

def partitionby[T](func: Callable[[T], Any], seq: Iterable[T]) -> Iterator[tuple[T, ...]]:
    ...
