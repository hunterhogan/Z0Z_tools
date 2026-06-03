from collections.abc import Callable, Iterable
from typing import Literal

type _MapFunction[T] = Callable[
	[
		Callable[[Iterable[T]], T],
		Iterable[Iterable[T]],
	],
	Iterable[T],
]

def fold[T](
	binop: Callable[[T, T], T],
	seq: Iterable[T],
	default: Literal[__no__default__] | T = "__no_default__",
	map: _MapFunction[T] = map,
	chunksize: int = 128,
	combine: Callable[[T, T], T] | None = None,
) -> T:
	...
