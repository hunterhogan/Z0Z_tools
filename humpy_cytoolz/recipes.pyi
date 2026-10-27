from collections.abc import Callable, Hashable, Iterable, Iterator
from optype import CanGetitem
from typing import overload

__all__ = ('countby', 'partitionby')

@overload
def countby[T, Key: Hashable](key: Callable[[T], Key], seq: Iterable[T]) -> dict[Key, int]: ...
@overload
def countby[Key, Value: Hashable](key: list[Key], seq: Iterable[CanGetitem[Key, Value]]) -> dict[tuple[Value, ...], int]: ...
@overload
def countby[Key, Value: Hashable](key: Key, seq: Iterable[CanGetitem[Key, Value]]) -> dict[Value, int]: ...

def partitionby[T](func: Callable[[T], object], seq: Iterable[T]) -> Iterator[tuple[T, ...]]: ...
