
from collections.abc import Callable, Collection, Hashable, ItemsView, Iterable, Iterator, KeysView, Mapping, Sequence, ValuesView
from humpy_toolz._theTypes import Randomable, SupportsDunderLT, SupportsGetItem, SupportsRichComparison
from humpy_toolz.utils import no_default
from typing import Any, Literal, overload
from typing_extensions import TypeIs

__all__ = ('accumulate', 'concat', 'concatv', 'cons', 'count', 'diff', 'drop', 'first', 'frequencies', 'get', 'groupby', 'interleave', 'interpose', 'isdistinct', 'isiterable', 'iterate', 'join', 'last', 'mapcat', 'merge_sorted', 'nth', 'partition', 'partition_all', 'peek', 'peekn', 'pluck', 'random_sample', 'reduceby', 'remove', 'second', 'sliding_window', 'tail', 'take', 'take_nth', 'topk', 'unique')
no_pad: Literal['__no__pad__']

def getter[T, V](index: T | Sequence[T]) -> Callable[[SupportsGetItem[T, V]], V | tuple[V, ...]]:
    ...

@overload
def accumulate[T](binop: Callable[[T, T], T], seq: Iterable[T], initial: Literal['__no__default__'] = no_default) -> Iterator[T]:
    ...

@overload
def accumulate[T, S](binop: Callable[[T, S], T], seq: Iterable[S], initial: T) -> Iterator[T]:
    ...

def accumulate[T, S](binop: Callable[[T, S], T], seq: Iterable[S], initial: T | Literal['__no__default__'] = no_default) -> Iterator[T]:
    ...

def concat[T](seqs: Iterable[Iterable[T]]) -> Iterator[T]:
    ...

def concatv[T](*seqs: Iterable[T]) -> Iterator[T]:
    ...

def cons[T](el: T, seq: Iterable[T]) -> Iterator[T]:
    ...

def count(seq: Iterable[Any]) -> int:
    ...

@overload
def diff[T](*seqs: Iterable[T], default: Literal['__no__default__'] = no_default, key: Callable[[T], Any] | None = None) -> Iterator[tuple[T | None, ...]]:
    ...

@overload
def diff[T, U](*seqs: Iterable[T], default: U, key: Callable[[T], Any] | None = None) -> Iterator[tuple[T | U, ...]]:
    ...

@overload
def diff[T](*seqs: Iterable[T], default: T, key: Callable[[T], Any] | None = None) -> Iterator[tuple[T, ...]]:
    ...

def diff[T, U](*seqs: Iterable[T], default: U | Literal['__no__default__'] = no_default, key: Callable[[T], Any] | None = None) -> Iterator[tuple[T | U | None, ...]]:
    ...

def drop[T](n: int, seq: Iterable[T]) -> Iterator[T]:
    ...

def first[T](seq: Iterable[T]) -> T:
    ...

def frequencies[T](seq: Iterable[T]) -> dict[T, int]:
    ...

def _get[T, V](ind: T, seq: SupportsGetItem[T, V], default: V) -> V:
    ...

@overload
def get[T, V](ind: Sequence[T], seq: SupportsGetItem[T, V], default: V | Literal['__no__default__'] = no_default) -> tuple[V, ...]:
    ...

@overload
def get[T, V](ind: T, seq: SupportsGetItem[T, V], default: V | Literal['__no__default__'] = no_default) -> V:
    ...

def get[T, V](ind: T | Sequence[T], seq: SupportsGetItem[T, V], default: V | Literal['__no__default__'] = no_default) -> V | tuple[V, ...]:
    ...

@overload
def groupby[T, K: Hashable](key: Callable[[T], K], seq: Iterable[T]) -> dict[K, list[T]]:
    ...

@overload
def groupby[K: Hashable, T](key: K, seq: Iterable[T]) -> dict[K, list[T]]:
    ...

def groupby[T, K: Hashable](key: Callable[[T], K] | K, seq: Iterable[T]) -> dict[K, list[T]]:
    ...

def interleave[T](seqs: Iterable[Iterable[T]]) -> Iterator[T]:
    ...

def interpose[T](el: T, seq: Iterable[T]) -> Iterator[T]:
    ...

def isdistinct(seq: Collection[Any]) -> bool:
    ...

@overload
def isiterable[TIterable: Iterable[Any]](x: TIterable) -> TypeIs[TIterable]:
    ...

@overload
def isiterable(x: object) -> bool:
    ...

def isiterable(x: Any) -> bool:
    ...

def iterate[T](func: Callable[[T], T], x: T) -> Iterator[T]:
    ...

@overload
def join[T, U](leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U]) -> Iterator[tuple[T, U]]:
    ...

@overload
def join[T, U, L](leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U], left_default: L) -> Iterator[tuple[T | L, U]]:
    ...

@overload
def join[T, U, R](leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U], *, right_default: R) -> Iterator[tuple[T, U | R]]:
    ...

@overload
def join[T, U, L, R](leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U], left_default: L, right_default: R) -> Iterator[tuple[T | L, U | R]]:
    ...

@overload
def join[T, U](leftkey: Hashable, leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U]) -> Iterator[tuple[T, U]]:
    ...

@overload
def join[T, U, L](leftkey: Hashable, leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U], left_default: L) -> Iterator[tuple[T | L, U]]:
    ...

@overload
def join[T, U, R](leftkey: Hashable, leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U], *, right_default: R) -> Iterator[tuple[T, U | R]]:
    ...

@overload
def join[T, U, L, R](leftkey: Hashable, leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U], left_default: L, right_default: R) -> Iterator[tuple[T | L, U | R]]:
    ...

@overload
def join[T, U](leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Hashable, rightseq: Iterable[U]) -> Iterator[tuple[T, U]]:
    ...

@overload
def join[T, U, L](leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Hashable, rightseq: Iterable[U], left_default: L) -> Iterator[tuple[T | L, U]]:
    ...

@overload
def join[T, U, R](leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Hashable, rightseq: Iterable[U], *, right_default: R) -> Iterator[tuple[T, U | R]]:
    ...

@overload
def join[T, U, L, R](leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Hashable, rightseq: Iterable[U], left_default: L, right_default: R) -> Iterator[tuple[T | L, U | R]]:
    ...

@overload
def join[T, U](leftkey: Hashable, leftseq: Iterable[T], rightkey: Hashable, rightseq: Iterable[U]) -> Iterator[tuple[T, U]]:
    ...

@overload
def join[T, U, L](leftkey: Hashable, leftseq: Iterable[T], rightkey: Hashable, rightseq: Iterable[U], left_default: L) -> Iterator[tuple[T | L, U]]:
    ...

@overload
def join[T, U, R](leftkey: Hashable, leftseq: Iterable[T], rightkey: Hashable, rightseq: Iterable[U], *, right_default: R) -> Iterator[tuple[T, U | R]]:
    ...

@overload
def join[T, U, L, R](leftkey: Hashable, leftseq: Iterable[T], rightkey: Hashable, rightseq: Iterable[U], left_default: L, right_default: R) -> Iterator[tuple[T | L, U | R]]:
    ...

def join[T, U, L, R](leftkey: Callable[[T], Hashable] | Hashable, leftseq: Iterable[T], rightkey: Callable[[U], Hashable] | Hashable, rightseq: Iterable[U], left_default: L | Literal['__no__default__'] = no_default, right_default: R | Literal['__no__default__'] = no_default) -> Iterator[tuple[T | L, U | R]]:
    ...

def last[T](seq: Iterable[T]) -> T:
    ...

def mapcat[T, R](func: Callable[[T], Iterable[R]], seqs: Iterable[T]) -> Iterator[R]:
    ...

def _merge_sorted_binary(seqs: Sequence[Iterable[SupportsDunderLT[Any]]]) -> Iterator[SupportsDunderLT[Any]]:
    ...

def _merge_sorted_binary_key[T](seqs: Sequence[Iterable[T]], key: Callable[[T], SupportsDunderLT[Any]]) -> Iterator[T]:
    ...

@overload
def merge_sorted[TSupportsRichComparison: SupportsRichComparison](*seqs: Iterable[TSupportsRichComparison], key: None = None) -> Iterator[TSupportsRichComparison]:
    ...

@overload
def merge_sorted[T](*seqs: Iterable[T], key: Callable[[T], SupportsDunderLT[Any]]) -> Iterator[T]:
    ...

def merge_sorted[T](*seqs: Iterable[T], key: Callable[[T], SupportsDunderLT[Any]] | None = None) -> Iterator[T]:
    ...

def nth[T](n: int, seq: Iterable[T]) -> T:
    ...

def partition[T, L](n: int, seq: Iterable[T], pad: L | Literal['__no__pad__'] = no_pad) -> Iterator[tuple[T, ...]] | Iterator[tuple[T | L, ...]]:
    ...

def partition_all[T](n: int, seq: Iterable[T]) -> Iterator[tuple[T, ...]]:
    ...

def peek[T](seq: Iterable[T]) -> tuple[T, Iterator[T]]:
    ...

def peekn[T](n: int, seq: Iterable[T]) -> tuple[tuple[T, ...], Iterator[T]]:
    ...

@overload
def pluck[T](ind: list[Any], seqs: Iterable[Sequence[T] | Mapping[Any, T]], default: T | Literal['__no__default__'] = ...) -> Iterator[tuple[T, ...]]:
    ...

@overload
def pluck[T](ind: Any, seqs: Iterable[Sequence[T] | Mapping[Any, T]], default: T | Literal['__no__default__'] = ...) -> Iterator[T]:
    ...

def pluck[T](ind: Any | list[Any], seqs: Iterable[Sequence[T] | Mapping[Any, T]], default: T | Literal['__no__default__'] = no_default) -> Iterator[T] | Iterator[tuple[T, ...]]:
    ...

def random_sample[T](prob: float, seq: Iterable[T], random_state: Randomable | int | float | str | bytes | bytearray | None = None) -> Iterator[T]:
    ...

@overload
def reduceby[T, K: Hashable](key: Callable[[T], K], binop: Callable[[T, T], T], seq: Iterable[T]) -> dict[K, T]:
    ...

@overload
def reduceby[T, K: Hashable](key: Callable[[T], K], binop: Callable[[T, T], T], seq: Iterable[T], init: T | Callable[[], T]) -> dict[K, T]:
    ...

@overload
def reduceby[T](key: Any, binop: Callable[[T, T], T], seq: Iterable[T]) -> dict[T, T]:
    ...

@overload
def reduceby[T](key: Any, binop: Callable[[T, T], T], seq: Iterable[T], init: T | Callable[[], T]) -> dict[T, T]:
    ...

def reduceby[T, K: Hashable](key: Callable[[T], K] | Any, binop: Callable[[T, T], T], seq: Iterable[T], init: T | Callable[[], T] | Literal['__no__default__'] = no_default) -> dict[K, T]:
    ...

def remove[T](predicate: Callable[[T], bool], seq: Iterable[T]) -> Iterable[T]:
    ...

def second[T](seq: Iterable[T]) -> T:
    ...

@overload
def sliding_window[T](n: Literal[1], seq: Iterable[T]) -> Iterator[tuple[T]]:
    ...

@overload
def sliding_window[T](n: Literal[2], seq: Iterable[T]) -> Iterator[tuple[T, T]]:
    ...

@overload
def sliding_window[T](n: Literal[3], seq: Iterable[T]) -> Iterator[tuple[T, T, T]]:
    ...

@overload
def sliding_window[T](n: Literal[4], seq: Iterable[T]) -> Iterator[tuple[T, T, T, T]]:
    ...

@overload
def sliding_window[T](n: Literal[5], seq: Iterable[T]) -> Iterator[tuple[T, T, T, T, T]]:
    ...

@overload
def sliding_window[T](n: int, seq: Iterable[T]) -> Iterator[tuple[T, ...]]:
    ...

def sliding_window(n: int, seq: Iterable[Any]) -> Iterator[tuple[Any, ...]]:
    ...

@overload
def tail[SSequence: Sequence[Any]](n: int, seq: SSequence) -> SSequence:
    ...

@overload
def tail[K: Hashable](n: int, seq: Mapping[K, Any]) -> tuple[K, ...]:
    ...

@overload
def tail[K: Hashable, T](n: int, seq: ItemsView[K, T]) -> tuple[tuple[K, T], ...]:
    ...

@overload
def tail[K: Hashable](n: int, seq: KeysView[K]) -> tuple[K, ...]:
    ...

@overload
def tail[T](n: int, seq: ValuesView[T]) -> tuple[T, ...]:
    ...

def tail[SSequence: Sequence[Any], K: Hashable, T](n: int, seq: SSequence | Mapping[K, Any] | ItemsView[K, T] | KeysView[K] | ValuesView[T]) -> SSequence | tuple[K, ...] | tuple[tuple[K, T], ...] | tuple[T, ...]:
    ...

def take[T](n: int, seq: Iterable[T]) -> Iterator[T]:
    ...

def take_nth[T](n: int, seq: Iterable[T]) -> Iterator[T]:
    ...

@overload
def topk[T](k: Literal[1], seq: Iterable[T], key: Callable[[T], Any] | None = ...) -> tuple[T]:
    ...

@overload
def topk[T](k: Literal[2], seq: Iterable[T], key: Callable[[T], Any] | None = ...) -> tuple[T, T]:
    ...

@overload
def topk[T](k: Literal[3], seq: Iterable[T], key: Callable[[T], Any] | None = ...) -> tuple[T, T, T]:
    ...

@overload
def topk[T](k: Literal[4], seq: Iterable[T], key: Callable[[T], Any] | None = ...) -> tuple[T, T, T, T]:
    ...

@overload
def topk[T](k: Literal[5], seq: Iterable[T], key: Callable[[T], Any] | None = ...) -> tuple[T, T, T, T, T]:
    ...

@overload
def topk[T](k: int, seq: Iterable[T], key: Callable[[T], Any] | None = None) -> tuple[T, ...]:
    ...

def topk(k: int, seq: Iterable[Any], key: Callable[[Any], Any] | None = None) -> tuple[Any, ...]:
    ...

def unique[T](seq: Iterable[T], key: Callable[[T], Any] | None = None) -> Iterator[T]:
    ...
