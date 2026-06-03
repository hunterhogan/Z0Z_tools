from .utils import no_default
from _typeshed import SupportsRichComparison
from collections.abc import Callable, Hashable, Iterable, Iterator, Mapping, Sequence
from typing import Any, Literal, overload, Protocol, TypeGuard

type _NoDefaultType = Literal["__no__default__"]
type _NoPadType = Literal["__no__pad__"]

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

class _Randomable(Protocol):
	def random(self) -> float: ...

type _NonCallableKeySelector = Hashable | list[Any]

### Toolz itself

def remove[T]( predicate: Callable[[T], bool], seq: Iterable[T] ) -> Iterable[T]:
	...

@overload
def accumulate[T]( binop: Callable[[T, T], T], seq: Iterable[T] ) -> Iterator[T]: ...
@overload
def accumulate[T]( binop: Callable[[T, T], T], seq: Iterable[T], initial: T ) -> Iterator[T]: ...
def accumulate[T]( binop: Callable[[T, T], T], seq: Iterable[T], initial: T | _NoDefaultType = no_default ) -> Iterator[T]:
	...

@overload
def groupby[KT, T]( key: Callable[[T], KT], seq: Iterable[T] ) -> dict[KT, list[T]]: ...
@overload
def groupby[T]( key: list[Any], seq: Iterable[Sequence[T] | Mapping[Any, T]] ) -> dict[tuple[T, ...], list[Sequence[T] | Mapping[Any, T]]]: ...
@overload
def groupby[T]( key: Any, seq: Iterable[Sequence[T] | Mapping[Any, T]] ) -> dict[T, list[Sequence[T] | Mapping[Any, T]]]: ...
def groupby( key: Callable[[Any], Any] | list[Any] | Any, seq: Iterable[Any] ) -> dict[Any, list[Any]]:
	...

def merge_sorted[CT: SupportsRichComparison]( *seqs: Iterable[CT], key: Callable[[CT], CT] | None = None ) -> Iterator[CT]:
	...

def interleave[T]( seqs: Iterable[Iterable[T]] ) -> Iterator[T]:
	...

def unique[T]( seq: Iterable[T], key: Callable[[T], Any] | None = None ) -> Iterator[T]:
	...

def isiterable(x: Any) -> TypeGuard[Iterable[Any]]:
	...

def isdistinct(
	seq: Iterable[Any] | Sequence[Any],
) -> bool:
	...

def take[T](n: int, seq: Iterable[T]) -> Iterator[T]:
	...

@overload
def tail[S: Sequence[Any]](n: int, seq: S) -> S: ...
@overload
def tail[T](n: int, seq: Iterable[T]) -> tuple[T, ...]: ...
def tail[T](n: int, seq: Iterable[T]) -> Sequence[Any] | tuple[T, ...]:
	...

def drop[T](n: int, seq: Iterable[T]) -> Iterator[T]:
	...

def take_nth[T](n: int, seq: Iterable[T]) -> Iterator[T]:
	...

def first[T](seq: Iterable[T]) -> T:
	...

def second[T](seq: Iterable[T]) -> T:
	...

def nth[T](n: int, seq: Iterable[T]) -> T:
	...

def last[T](seq: Iterable[T]) -> T:
	...

def rest[T](seq: Iterable[T]) -> Iterable[T]:
	...
	# Warning - this function is not exposed via __all__ and should be considered private.

@overload
def get[T]( ind: list[Any], seq: Sequence[T] | Mapping[Any, T], default: T | _NoDefaultType = ..., ) -> tuple[T, ...]: ...
@overload
def get[T]( ind: Any, seq: Sequence[T] | Mapping[Any, T], default: T | _NoDefaultType = ..., ) -> T: ...
def get[T]( ind: Any | list[Any], seq: Sequence[T] | Mapping[Any, T], default: T | _NoDefaultType = no_default, ) -> T | tuple[T, ...]:
	...

def concat[T]( seqs: Iterable[Iterable[T]], ) -> Iterator[T]:
	...

def concatv[T](*seqs: Iterable[T]) -> Iterator[T]:
	...

def mapcat[T, R]( func: Callable[[T], Iterable[R]], seqs: Iterable[T], ) -> Iterator[R]:
	...

def cons[T](el: T, seq: Iterable[T]) -> Iterator[T]:
	...

def interpose[T]( el: T, seq: Iterable[T] ) -> Iterator[T]:
	...

def frequencies[T](seq: Iterable[T]) -> dict[T, int]:
	...

@overload
def reduceby[T, K]( key: Callable[[T], K], binop: Callable[[T, T], T], seq: Iterable[T], ) -> dict[K, T]: ...
@overload
def reduceby[T, K]( key: Callable[[T], K], binop: Callable[[T, T], T], seq: Iterable[T], init: T | Callable[[], T], ) -> dict[K, T]: ...
@overload
def reduceby[T]( key: Any, binop: Callable[[T, T], T], seq: Iterable[T], ) -> dict[T, T]: ...
@overload
def reduceby[T]( key: Any, binop: Callable[[T, T], T], seq: Iterable[T], init: T | Callable[[], T], ) -> dict[T, T]: ...
def reduceby[T, K]( key: Callable[[T], K] | Any, binop: Callable[[T, T], T], seq: Iterable[T], init: T | Callable[[], T] | _NoDefaultType = no_default, ) -> dict[K, T]:
	...

def iterate[T](func: Callable[[T], T], x: T) -> Iterator[T]:
	...

def sliding_window[T]( n: int, seq: Iterable[T] ) -> Iterator[tuple[T, ...]]:
	...

no_pad: _NoPadType = "__no__pad__"

@overload
def partition[T, P]( n: Literal[1], seq: Iterable[T], pad: Any = ... ) -> Iterator[tuple[T]]: ...
@overload
def partition[T]( n: int, seq: Iterable[T], pad: _NoPadType = ... ) -> Iterator[tuple[T, ...]]: ...
@overload
def partition[T, P]( n: int, seq: Iterable[T], pad: P ) -> Iterator[tuple[T | P, ...]]: ...
def partition[T, P]( n: int, seq: Iterable[T], pad: P | _NoPadType = no_pad ) -> Iterator[tuple[T | P, ...]]:
	...

@overload
def partition_all[T]( n: Literal[1], seq: Iterable[T] ) -> Iterator[tuple[T]]: ...
@overload
def partition_all[T]( n: int, seq: Iterable[T] ) -> Iterator[tuple[T, ...]]: ...
def partition_all[T]( n: int, seq: Iterable[T] ) -> Iterator[tuple[T, ...]]:
	...

def count(seq: Iterable[Any]) -> int:
	...

@overload
def pluck[T]( ind: list[Any], seqs: Iterable[ Sequence[T] | Mapping[Any, T] ], default: T | _NoDefaultType = ..., ) -> Iterator[tuple[T, ...]]: ...
@overload
def pluck[T]( ind: Any, seqs: Iterable[ Sequence[T] | Mapping[Any, T] ], default: T | _NoDefaultType = ..., ) -> Iterator[T]: ...
def pluck[T]( ind: Any | list[Any], seqs: Iterable[ Sequence[T] | Mapping[Any, T] ], default: T | _NoDefaultType = no_default, ) -> Iterator[T] | Iterator[tuple[T, ...]]:
	...

@overload
def getter[T]( index: list[Any], ) -> Callable[ [Sequence[T] | Mapping[Any, T]], tuple[T, ...], ]: ...
@overload
def getter[T]( index: Any, ) -> Callable[ [Sequence[T] | Mapping[Any, T]], T ]: ...
def getter[T]( index: Any | list[Any], ) -> Callable[ [Sequence[T] | Mapping[Any, T]], T | tuple[T, ...], ]:
	# Warning - this function is not exposed via __all__ and should be considered private.
	...

# === CALLABLE + CALLABLE (4 overloads) ===
@overload
def join[T, U](leftkey: Callable[[T], Hashable],leftseq: Iterable[T],rightkey: Callable[[U], Hashable],rightseq: Iterable[U],
) -> Iterator[tuple[T, U]]: ...
@overload
def join[T, U, L](leftkey: Callable[[T], Hashable],leftseq: Iterable[T],rightkey: Callable[[U], Hashable],rightseq: Iterable[U],left_default: L,
) -> Iterator[tuple[T | L, U]]: ...
@overload
def join[T, U, R](leftkey: Callable[[T], Hashable],leftseq: Iterable[T],rightkey: Callable[[U], Hashable],rightseq: Iterable[U],*,right_default: R,
) -> Iterator[tuple[T, U | R]]: ...
@overload
def join[T, U, L, R](leftkey: Callable[[T], Hashable],leftseq: Iterable[T],rightkey: Callable[[U], Hashable],rightseq: Iterable[U],left_default: L,right_default: R,
) -> Iterator[tuple[T | L, U | R]]: ...

# === HASHABLE + CALLABLE (4 overloads) ===
@overload
def join[T, U](leftkey: _NonCallableKeySelector,leftseq: Iterable[T],rightkey: Callable[[U], Hashable],rightseq: Iterable[U],
) -> Iterator[tuple[T, U]]: ...
@overload
def join[T, U, L](leftkey: _NonCallableKeySelector,leftseq: Iterable[T],rightkey: Callable[[U], Hashable],rightseq: Iterable[U],left_default: L,
) -> Iterator[tuple[T | L, U]]: ...
@overload
def join[T, U, R](leftkey: _NonCallableKeySelector,leftseq: Iterable[T],rightkey: Callable[[U], Hashable],rightseq: Iterable[U],*,right_default: R,
) -> Iterator[tuple[T, U | R]]: ...
@overload
def join[T, U, L, R](leftkey: _NonCallableKeySelector,leftseq: Iterable[T],rightkey: Callable[[U], Hashable],rightseq: Iterable[U],left_default: L,right_default: R,
) -> Iterator[tuple[T | L, U | R]]: ...

# === CALLABLE + HASHABLE (4 overloads) ===
@overload
def join[T, U](leftkey: Callable[[T], Hashable],leftseq: Iterable[T],rightkey: _NonCallableKeySelector,rightseq: Iterable[U],
) -> Iterator[tuple[T, U]]: ...
@overload
def join[T, U, L](leftkey: Callable[[T], Hashable],leftseq: Iterable[T],rightkey: _NonCallableKeySelector,rightseq: Iterable[U],left_default: L,
) -> Iterator[tuple[T | L, U]]: ...
@overload
def join[T, U, R](leftkey: Callable[[T], Hashable],leftseq: Iterable[T],rightkey: _NonCallableKeySelector,rightseq: Iterable[U],*,right_default: R,
) -> Iterator[tuple[T, U | R]]: ...
@overload
def join[T, U, L, R](leftkey: Callable[[T], Hashable],leftseq: Iterable[T],rightkey: _NonCallableKeySelector,rightseq: Iterable[U],left_default: L,right_default: R,
) -> Iterator[tuple[T | L, U | R]]: ...

# === HASHABLE + HASHABLE (4 overloads) ===
@overload
def join[T, U](leftkey: _NonCallableKeySelector,leftseq: Iterable[T],rightkey: _NonCallableKeySelector,rightseq: Iterable[U],
) -> Iterator[tuple[T, U]]: ...
@overload
def join[T, U, L](leftkey: _NonCallableKeySelector,leftseq: Iterable[T],rightkey: _NonCallableKeySelector,rightseq: Iterable[U],left_default: L,
) -> Iterator[tuple[T | L, U]]: ...
@overload
def join[T, U, R](leftkey: _NonCallableKeySelector,leftseq: Iterable[T],rightkey: _NonCallableKeySelector,rightseq: Iterable[U],*,right_default: R,
) -> Iterator[tuple[T, U | R]]: ...
@overload
def join[T, U, L, R](leftkey: _NonCallableKeySelector,leftseq: Iterable[T],rightkey: _NonCallableKeySelector,rightseq: Iterable[U],left_default: L,right_default: R,
) -> Iterator[tuple[T | L, U | R]]: ...

# Implementation signature
def join[T, U, L, R](leftkey: Callable[[T], Hashable] | _NonCallableKeySelector,leftseq: Iterable[T],rightkey: Callable[[U], Hashable] | _NonCallableKeySelector,rightseq: Iterable[U],left_default: L | _NoDefaultType = no_default,right_default: R | _NoDefaultType = no_default,
) -> Iterator[tuple[T | L, U | R]]:
	...

@overload
def diff[T](seqs: list[Iterable[T]],*,key: Callable[[T], Any] | None = None,
) -> Iterator[tuple[T, ...]]: ...
@overload
def diff[T](seqs: list[Iterable[T]],*,default: None,key: Callable[[T], Any] | None = None,
) -> Iterator[tuple[T | None, ...]]: ...
@overload
def diff[T, D](seqs: list[Iterable[T]],*,default: D,key: Callable[[T], Any] | None = None,
) -> Iterator[tuple[T | D, ...]]: ...
@overload
def diff[T](*seqs: Iterable[T],key: Callable[[T], Any] | None = None,
) -> Iterator[tuple[T, ...]]: ...
@overload
def diff[T](*seqs: Iterable[T],default: None,key: Callable[[T], Any] | None = None,
) -> Iterator[tuple[T | None, ...]]: ...
@overload
def diff[T, D](*seqs: Iterable[T],default: D,key: Callable[[T], Any] | None = None,
) -> Iterator[tuple[T | D, ...]]: ...
@overload
def diff[T](*seqs: Iterable[T],default: T,key: Callable[[T], Any] | None = None,
) -> Iterator[tuple[T, ...]]: ...
def diff[T, D](*seqs: Iterable[T] | list[Iterable[T]],default: T | D | _NoDefaultType = no_default,key: Callable[[T], Any] | None = None,
) -> Iterator[tuple[T, ...]] | Iterator[tuple[T | D, ...]]:
	...

def topk[T](k: int,seq: Iterable[T],key: Callable[[T], SupportsRichComparison] | Any | None = None,
) -> tuple[T, ...]:
	...

def peek[T](seq: Iterable[T]) -> tuple[T, Iterator[T]]:
	...

def peekn[T]( n: int, seq: Iterable[T] ) -> tuple[tuple[T, ...], Iterator[T]]:
	...

def random_sample[T]( prob: float, seq: Iterable[T], random_state: int | float | str | bytes | bytearray | _Randomable | None = None, ) -> Iterator[T]:
	...
