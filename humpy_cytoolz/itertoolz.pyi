from collections.abc import Callable, Hashable, ItemsView, Iterable, Iterator, KeysView, Mapping, Sequence, ValuesView
from humpy_cytoolz._theTypes import K, L, R, Randomable, SupportsRichComparison, T, U
from humpy_cytoolz.utils import no_default
from typing import Any, Literal, overload, TypeAlias, TypeGuard

_NoDefaultType: TypeAlias = Literal["__no__default__"]
_NoPadType: TypeAlias = Literal["__no__pad__"]
_NonCallableKeySelector: TypeAlias = Hashable | list[Any]

__all__ = (
	"accumulate",
	"concat",
	"concatv",
	"cons",
	"count",
	"diff",
	"drop",
	"first",
	"frequencies",
	"get",
	"groupby",
	"interleave",
	"interpose",
	"isdistinct",
	"isiterable",
	"iterate",
	"join",
	"last",
	"mapcat",
	"merge_sorted",
	"nth",
	"partition",
	"partition_all",
	"peek",
	"peekn",
	"pluck",
	"random_sample",
	"reduceby",
	"remove",
	"second",
	"sliding_window",
	"tail",
	"take",
	"take_nth",
	"topk",
	"unique",
)

# Toolz itself

def remove(predicate: Callable[[T], bool], seq: Iterable[T]) -> Iterable[T]:
	...

@overload
def accumulate(binop: Callable[[T, T], T], seq: Iterable[T]) -> Iterator[T]: ...
@overload
def accumulate(binop: Callable[[T, T], T], seq: Iterable[T], initial: T) -> Iterator[T]: ...
def accumulate(binop: Callable[[T, T], T], seq: Iterable[T], initial: T | _NoDefaultType = no_default) -> Iterator[T]:
	...

@overload
def groupby(key: Callable[[T], K], seq: Iterable[T]) -> dict[K, list[T]]: ...
@overload
def groupby(key: list[Any], seq: Iterable[Sequence[T] | Mapping[Any, T]]) -> dict[tuple[T, ...], list[Sequence[T] | Mapping[Any, T]]]: ...
@overload
def groupby(key: Any, seq: Iterable[Sequence[T] | Mapping[Any, T]]) -> dict[T, list[Sequence[T] | Mapping[Any, T]]]: ...
def groupby(key: Callable[[Any], Any] | list[Any] | Any, seq: Iterable[Any]) -> dict[Any, list[Any]]:
	...

def merge_sorted(*seqs: Iterable[SupportsRichComparison], key: Callable[[SupportsRichComparison], SupportsRichComparison] | None = None) -> Iterator[SupportsRichComparison]:
	...

def interleave(seqs: Iterable[Iterable[T]]) -> Iterator[T]:
	...

def unique(seq: Iterable[T], key: Callable[[T], Any] | None = None) -> Iterator[T]:
	...

def isiterable(x: Any) -> TypeGuard[Iterable[Any]]:
	...

def isdistinct(
	seq: Iterable[Any] | Sequence[Any],
) -> bool:
	...

def take(n: int, seq: Iterable[T]) -> Iterator[T]:
	...

@overload
def tail(n: int, seq: Sequence[Any]) -> Sequence[Any]: ...
@overload
def tail(n: int, seq: Mapping[K, Any]) -> tuple[K, ...]: ...
@overload
def tail(n: int, seq: ItemsView[K, T]) -> tuple[tuple[K, T], ...]: ...
@overload
def tail(n: int, seq: KeysView[K]) -> tuple[K, ...]: ...
@overload
def tail(n: int, seq: ValuesView[T]) -> tuple[T, ...]: ...
@overload
def tail(n: int, seq: Iterable[T]) -> tuple[T, ...]: ...
def tail(n: int, seq: Iterable[T]) -> Sequence[Any] | tuple[T, ...] | tuple[tuple[Any, T], ...]:
	...

def drop(n: int, seq: Iterable[T]) -> Iterator[T]:
	...

def take_nth(n: int, seq: Iterable[T]) -> Iterator[T]:
	...

def first(seq: Iterable[T]) -> T:
	...

def second(seq: Iterable[T]) -> T:
	...

def nth(n: int, seq: Iterable[T]) -> T:
	...

def last(seq: Iterable[T]) -> T:
	...

def rest(seq: Iterable[T]) -> Iterable[T]:
	...
	# Warning - this function is not exposed via __all__ and should be considered private.

@overload
def get(ind: list[Any], seq: Sequence[T] | Mapping[Any, T], default: T | _NoDefaultType = ...) -> tuple[T, ...]: ...
@overload
def get(ind: Any, seq: Sequence[T] | Mapping[Any, T], default: T | _NoDefaultType = ...) -> T: ...
def get(ind: Any | list[Any], seq: Sequence[T] | Mapping[Any, T], default: T | _NoDefaultType = no_default) -> T | tuple[T, ...]:
	...

def concat(seqs: Iterable[Iterable[T]]) -> Iterator[T]:
	...

def concatv(*seqs: Iterable[T]) -> Iterator[T]:
	...

def mapcat(func: Callable[[T], Iterable[R]], seqs: Iterable[T]) -> Iterator[R]:
	...

def cons(el: T, seq: Iterable[T]) -> Iterator[T]:
	...

def interpose(el: T, seq: Iterable[T]) -> Iterator[T]:
	...

def frequencies(seq: Iterable[T]) -> dict[T, int]:
	...

@overload
def reduceby(key: Callable[[T], K], binop: Callable[[T, T], T], seq: Iterable[T]) -> dict[K, T]: ...
@overload
def reduceby(key: Callable[[T], K], binop: Callable[[T, T], T], seq: Iterable[T], init: T | Callable[[], T]) -> dict[K, T]: ...
@overload
def reduceby(key: Any, binop: Callable[[T, T], T], seq: Iterable[T]) -> dict[T, T]: ...
@overload
def reduceby(key: Any, binop: Callable[[T, T], T], seq: Iterable[T], init: T | Callable[[], T]) -> dict[T, T]: ...
def reduceby(key: Callable[[T], K] | Any, binop: Callable[[T, T], T], seq: Iterable[T], init: T | Callable[[], T] | _NoDefaultType = no_default) -> dict[K, T]:
	...

def iterate(func: Callable[[T], T], x: T) -> Iterator[T]:
	...

def sliding_window(n: int, seq: Iterable[T]) -> Iterator[tuple[T, ...]]:
	...

no_pad: _NoPadType = "__no__pad__"

@overload
def partition(n: Literal[1], seq: Iterable[T], pad: Any = ...) -> Iterator[tuple[T]]: ...
@overload
def partition(n: int, seq: Iterable[T], pad: _NoPadType = ...) -> Iterator[tuple[T, ...]]: ...
@overload
def partition(n: int, seq: Iterable[T], pad: U) -> Iterator[tuple[T | U, ...]]: ...
def partition(n: int, seq: Iterable[T], pad: U | _NoPadType = no_pad) -> Iterator[tuple[T | U, ...]]:
	...

@overload
def partition_all(n: Literal[1], seq: Iterable[T]) -> Iterator[tuple[T]]: ...
@overload
def partition_all(n: int, seq: Iterable[T]) -> Iterator[tuple[T, ...]]: ...
def partition_all(n: int, seq: Iterable[T]) -> Iterator[tuple[T, ...]]:
	...

def count(seq: Iterable[Any]) -> int:
	...

@overload
def pluck(ind: list[Any], seqs: Iterable[Sequence[T] | Mapping[Any, T]], default: T | _NoDefaultType = ...) -> Iterator[tuple[T, ...]]: ...
@overload
def pluck(ind: Any, seqs: Iterable[Sequence[T] | Mapping[Any, T]], default: T | _NoDefaultType = ...) -> Iterator[T]: ...
def pluck(ind: Any | list[Any], seqs: Iterable[Sequence[T] | Mapping[Any, T]], default: T | _NoDefaultType = no_default) -> Iterator[T] | Iterator[tuple[T, ...]]:
	...

@overload
def getter(index: list[Any]) -> Callable[[Sequence[T] | Mapping[Any, T]], tuple[T, ...]]: ...
@overload
def getter(index: Any) -> Callable[[Sequence[T] | Mapping[Any, T]], T]: ...
def getter(index: Any | list[Any]) -> Callable[[Sequence[T] | Mapping[Any, T]], T | tuple[T, ...]]:
	# Warning - this function is not exposed via __all__ and should be considered private.
	...

# === CALLABLE + CALLABLE (4 overloads) ===
@overload
def join(leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U],
) -> Iterator[tuple[T, U]]: ...
@overload
def join(leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U], left_default: L,
) -> Iterator[tuple[T | L, U]]: ...
@overload
def join(leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U], *, right_default: R,
) -> Iterator[tuple[T, U | R]]: ...
@overload
def join(leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U], left_default: L, right_default: R,
) -> Iterator[tuple[T | L, U | R]]: ...

# === HASHABLE + CALLABLE (4 overloads) ===
@overload
def join(leftkey: _NonCallableKeySelector, leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U],
) -> Iterator[tuple[T, U]]: ...
@overload
def join(leftkey: _NonCallableKeySelector, leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U], left_default: L,
) -> Iterator[tuple[T | L, U]]: ...
@overload
def join(leftkey: _NonCallableKeySelector, leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U], *, right_default: R,
) -> Iterator[tuple[T, U | R]]: ...
@overload
def join(leftkey: _NonCallableKeySelector, leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U], left_default: L, right_default: R,
) -> Iterator[tuple[T | L, U | R]]: ...

# === CALLABLE + HASHABLE (4 overloads) ===
@overload
def join(leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: _NonCallableKeySelector, rightseq: Iterable[U],
) -> Iterator[tuple[T, U]]: ...
@overload
def join(leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: _NonCallableKeySelector, rightseq: Iterable[U], left_default: L,
) -> Iterator[tuple[T | L, U]]: ...
@overload
def join(leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: _NonCallableKeySelector, rightseq: Iterable[U], *, right_default: R,
) -> Iterator[tuple[T, U | R]]: ...
@overload
def join(leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: _NonCallableKeySelector, rightseq: Iterable[U], left_default: L, right_default: R,
) -> Iterator[tuple[T | L, U | R]]: ...

# === HASHABLE + HASHABLE (4 overloads) ===
@overload
def join(leftkey: _NonCallableKeySelector, leftseq: Iterable[T], rightkey: _NonCallableKeySelector, rightseq: Iterable[U],
) -> Iterator[tuple[T, U]]: ...
@overload
def join(leftkey: _NonCallableKeySelector, leftseq: Iterable[T], rightkey: _NonCallableKeySelector, rightseq: Iterable[U], left_default: L,
) -> Iterator[tuple[T | L, U]]: ...
@overload
def join(leftkey: _NonCallableKeySelector, leftseq: Iterable[T], rightkey: _NonCallableKeySelector, rightseq: Iterable[U], *, right_default: R,
) -> Iterator[tuple[T, U | R]]: ...
@overload
def join(leftkey: _NonCallableKeySelector, leftseq: Iterable[T], rightkey: _NonCallableKeySelector, rightseq: Iterable[U], left_default: L, right_default: R,
) -> Iterator[tuple[T | L, U | R]]: ...

# Implementation signature
def join(leftkey: Callable[[T], Hashable] | _NonCallableKeySelector, leftseq: Iterable[T], rightkey: Callable[[U], Hashable] | _NonCallableKeySelector, rightseq: Iterable[U], left_default: L | _NoDefaultType = no_default, right_default: R | _NoDefaultType = no_default,
) -> Iterator[tuple[T | L, U | R]]:
	...

@overload
def diff(seqs: list[Iterable[T]], *, key: Callable[[T], Any] | None = None,
) -> Iterator[tuple[T, ...]]: ...
@overload
def diff(seqs: list[Iterable[T]], *, default: None, key: Callable[[T], Any] | None = None,
) -> Iterator[tuple[T | None, ...]]: ...
@overload
def diff(seqs: list[Iterable[T]], *, default: Any, key: Callable[[T], Any] | None = None,
) -> Iterator[tuple[T | Any, ...]]: ...
@overload
def diff(*seqs: Iterable[T], key: Callable[[T], Any] | None = None,
) -> Iterator[tuple[T, ...]]: ...
@overload
def diff(*seqs: Iterable[T], default: None, key: Callable[[T], Any] | None = None,
) -> Iterator[tuple[T | None, ...]]: ...
@overload
def diff(*seqs: Iterable[T], default: Any, key: Callable[[T], Any] | None = None,
) -> Iterator[tuple[T | Any, ...]]: ...
@overload
def diff(*seqs: Iterable[T], default: T, key: Callable[[T], Any] | None = None,
) -> Iterator[tuple[T, ...]]: ...
def diff(*seqs: Iterable[T] | list[Iterable[T]], default: T | Any | _NoDefaultType = no_default, key: Callable[[T], Any] | None = None,
) -> Iterator[tuple[T, ...]] | Iterator[tuple[T | Any, ...]]:
	...

def topk(k: int, seq: Iterable[T], key: Callable[[T], SupportsRichComparison] | Any | None = None,
) -> tuple[T, ...]:
	...

def peek(seq: Iterable[T]) -> tuple[T, Iterator[T]]:
	...

def peekn(n: int, seq: Iterable[T]) -> tuple[tuple[T, ...], Iterator[T]]:
	...

def random_sample(prob: float, seq: Iterable[T], random_state: int | float | str | bytes | bytearray | Randomable | None = None) -> Iterator[T]:
	...
