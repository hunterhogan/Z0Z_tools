# ruff: noqa: RUF067
"""
Alternate namespace for toolz such that all functions are curried

Currying provides implicit partial evaluation of all functions

Example:

	Get usually requires two arguments, an index and a collection
	>>> from humpy_toolz.curried import get
	>>> get(0, ('a', 'b'))
	'a'

	When we use it in higher order functions we often want to pass a partially
	evaluated form
	>>> data = [(1, 2), (11, 22), (111, 222)]
	>>> list(map(lambda seq: get(0, seq), data))
	[1, 11, 111]

	The curried version allows simple expression of partial evaluation
	>>> list(map(get(0), data))
	[1, 11, 111]

See Also
--------
	humpy_toolz.functoolz.curry
"""

from __future__ import annotations

from typing import (
	cast as __cast, overload as _overload, ParamSpec as __ParamSpec, Protocol as __Protocol, TYPE_CHECKING, TypeVar as __TypeVar)

if TYPE_CHECKING:
	from _typeshed import SupportsRichComparison
	from collections.abc import Callable, Hashable, Iterable, Iterator, Mapping, MutableMapping, Sequence
	from humpy_toolz.functoolz import excepts as _excepts_class
	from typing import Any, Literal, TypeGuard
	from typing_extensions import TypeIs

from humpy_toolz import (
	apply as apply, comp as comp, complement as complement, compose as compose, compose_left as compose_left, concat as concat,
	concatv as concatv, count as count, curry as curry, diff as diff, first as first, flip as flip, frequencies as frequencies,
	identity as identity, interleave as interleave, isdistinct as isdistinct, isiterable as isiterable, juxt as juxt, last as last,
	memoize as memoize, merge_sorted as merge_sorted, peek as peek, pipe as pipe, second as second, thread_first as thread_first,
	thread_last as thread_last)
from humpy_toolz.curried import operator as operator
from humpy_toolz.curried.exceptions import merge as merge, merge_with as merge_with
import humpy_toolz

P = __ParamSpec('P')
K = __TypeVar('K')
K0 = __TypeVar('K0')
K1 = __TypeVar('K1')
KT = __TypeVar('KT')
L = __TypeVar('L')
PType = __TypeVar('PType')
R = __TypeVar('R')
S = __TypeVar('S')
T = __TypeVar('T')
T1 = __TypeVar('T1')
T2 = __TypeVar('T2')
T3 = __TypeVar('T3')
T4 = __TypeVar('T4')
T5 = __TypeVar('T5')
U = __TypeVar('U')
V = __TypeVar('V')
V0 = __TypeVar('V0')
V1 = __TypeVar('V1')

# Curried functions (defined in this module)
__all__ = [
	'accumulate',
	'assoc',
	'assoc_in',
	'cons',
	'countby',
	'dissoc',
	'do',
	'drop',
	'excepts',
	'filter',
	'get',
	'get_in',
	'groupby',
	'interpose',
	'itemfilter',
	'itemmap',
	'iterate',
	'join',
	'keyfilter',
	'keymap',
	'map',
	'mapcat',
	'nth',
	'partial',
	'partition',
	'partition_all',
	'partitionby',
	'peekn',
	'pluck',
	'random_sample',
	'reduce',
	'reduceby',
	'remove',
	'sliding_window',
	'sorted',
	'tail',
	'take',
	'take_nth',
	'topk',
	'unique',
	'update_in',
	'valfilter',
	'valmap',
]

# Re-exported, not curried
__all__ += [
	'apply',
	'comp',
	'complement',
	'compose',
	'compose_left',
	'concat',
	'concatv',
	'count',
	'curry',
	'diff',
	'first',
	'flip',
	'frequencies',
	'identity',
	'interleave',
	'isdistinct',
	'isiterable',
	'juxt',
	'last',
	'memoize',
	'merge_sorted',
	'peek',
	'pipe',
	'second',
	'thread_first',
	'thread_last']

# Re-exported from .exceptions
__all__ += [
	'merge',
	'merge_with',
	# Submodule
	'operator',
]

class __Accumulate(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., Iterator[T]]: ...

	# Stage 1: Just binop - returns callable waiting for seq (and optional initial)
	@_overload
	def __call__(self, binop: Callable[[T, T], T], /) -> Callable[..., Iterator[T]]: ...

	# Stage 2a: binop + seq (no initial) - executes immediately
	@_overload
	def __call__(self, binop: Callable[[T, T], T], seq: Iterable[T], /) -> Iterator[T]: ...

	# Stage 2b: binop + seq + initial - executes immediately
	@_overload
	def __call__(self, binop: Callable[[T, T], T], seq: Iterable[T], initial: T, /) -> Iterator[T]: ...

class __Assoc(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., dict[K, V] | MutableMapping[K, V]]: ...
	@_overload
	def __call__(self, d: Mapping[K, V], /) -> Callable[..., dict[K, V] | MutableMapping[K, V]]: ...
	@_overload
	def __call__(self, d: Mapping[K, V], key: K, /) -> Callable[[V], dict[K, V]]: ...
	@_overload
	def __call__(
		self, d: Mapping[K, V], key: K, /, *, factory: Callable[[], MutableMapping[K, V]]
	) -> Callable[[V], MutableMapping[K, V]]: ...
	@_overload
	def __call__(self, d: Mapping[K, V], key: K, value: V, /) -> dict[K, V]: ...
	@_overload
	def __call__(self, d: Mapping[K, V], key: K, value: V, /, *, factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...

class __Cons(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., Iterator[T]]: ...

	# Stage 1: Just el - returns callable waiting for seq
	@_overload
	def __call__(self, el: T, /) -> Callable[[Iterable[T]], Iterator[T]]: ...

	# Stage 2: Full application - executes immediately
	@_overload
	def __call__(self, el: T, seq: Iterable[T], /) -> Iterator[T]: ...

class __Do(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., T]: ...

	# Stage 1: Just func - returns callable waiting for x
	@_overload
	def __call__(self, func: Callable[[T], Any], /) -> Callable[[T], T]: ...

	# Stage 2: Full application - executes immediately
	@_overload
	def __call__(self, func: Callable[[T], Any], x: T, /) -> T: ...

class __Drop(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., Iterator[T]]: ...
	@_overload
	def __call__(self, n: int, /) -> Callable[[Iterable[T]], Iterator[T]]: ...
	@_overload
	def __call__(self, n: int, seq: Iterable[T], /) -> Iterator[T]: ...

class __Excepts(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., _excepts_class[T, P]]: ...
	@_overload
	def __call__(
		self, exc: type[Exception] | tuple[type[Exception], ...], /
	) -> Callable[[Callable[P, T]], _excepts_class[T, P]] | Callable[[Callable[P, T], Callable[[Exception], T]], _excepts_class[T, P]]: ...
	@_overload
	def __call__(self, exc: type[Exception] | tuple[type[Exception], ...], func: Callable[P, T], /) -> _excepts_class[T, P]: ...
	@_overload
	def __call__(
		self, exc: type[Exception] | tuple[type[Exception], ...], func: Callable[P, T], handler: Callable[[Exception], T], /
	) -> _excepts_class[T, P]: ...

class __Filter(__Protocol):
	@_overload
	def __call__(
		self,
	) -> Callable[
		..., Iterator[T] | Callable[..., Iterator[T]]
	]: ...
	@_overload
	def __call__(
		self,
		function: None,
		/,
	) -> Callable[[Iterable[T | None]], Iterator[T]]: ...
	@_overload
	def __call__(self, function: Callable[[S], TypeGuard[T]], /) -> Callable[[Iterable[S]], Iterator[T]]: ...
	@_overload
	def __call__(self, function: Callable[[S], TypeIs[T]], /) -> Callable[[Iterable[S]], Iterator[T]]: ...
	@_overload
	def __call__(self, function: Callable[[T], Any], /) -> Callable[[Iterable[T]], Iterator[T]]: ...
	@_overload
	def __call__(self, function: None, iterable: Iterable[T | None], /) -> Iterator[T]: ...
	@_overload
	def __call__(self, function: Callable[[S], TypeGuard[T]], iterable: Iterable[S], /) -> Iterator[T]: ...
	@_overload
	def __call__(self, function: Callable[[S], TypeIs[T]], iterable: Iterable[S], /) -> Iterator[T]: ...
	@_overload
	def __call__(self, function: Callable[[T], Any], iterable: Iterable[T], /) -> Iterator[T]: ...

class __Get(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., T | tuple[T, ...]]: ...
	@_overload
	def __call__(
		self, ind: Sequence[Any], /
	) -> Callable[[Sequence[T] | Mapping[Any, T]], tuple[T, ...]] | Callable[[Sequence[T] | Mapping[Any, T], T], tuple[T, ...]]: ...
	@_overload
	def __call__(self, ind: Any, /) -> Callable[[Sequence[T] | Mapping[Any, T]], T] | Callable[[Sequence[T] | Mapping[Any, T], T], T]: ...
	@_overload
	def __call__(self, ind: Sequence[Any], seq: Sequence[T] | Mapping[Any, T], /) -> tuple[T, ...]: ...
	@_overload
	def __call__(self, ind: Any, seq: Sequence[T] | Mapping[Any, T], /) -> T: ...
	@_overload
	def __call__(self, ind: Sequence[Any], seq: Sequence[T] | Mapping[Any, T], default: T, /) -> tuple[T, ...]: ...
	@_overload
	def __call__(self, ind: Any, seq: Sequence[T] | Mapping[Any, T], default: T, /) -> T: ...

class __Groupby(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., dict[KT, list[T]]]: ...
	@_overload
	def __call__(self, key: Callable[[T], KT], /) -> Callable[[Iterable[T]], dict[KT, list[T]]]: ...
	@_overload
	def __call__(self, key: Any, /) -> Callable[[Iterable[T]], dict[Any, list[T]]]: ...
	@_overload
	def __call__(self, key: Callable[[T], KT], seq: Iterable[T], /) -> dict[KT, list[T]]: ...
	@_overload
	def __call__(self, key: Any, seq: Iterable[T], /) -> dict[Any, list[T]]: ...

class __Interpose(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., Iterator[T]]: ...

	# Stage 1: Just el - returns callable waiting for seq
	@_overload
	def __call__(self, el: T, /) -> Callable[[Iterable[T]], Iterator[T]]: ...

	# Stage 2: Full application - executes immediately
	@_overload
	def __call__(self, el: T, seq: Iterable[T], /) -> Iterator[T]: ...

class __Itemfilter(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., dict[K, V] | MutableMapping[K, V]]: ...

	# Stage 1a: Just predicate (no factory) - returns callable waiting for dict
	@_overload
	def __call__(self, predicate: Callable[[tuple[K, V]], bool], /) -> Callable[[Mapping[K, V]], dict[K, V]]: ...

	# Stage 1b: Predicate with factory - returns callable waiting for dict
	@_overload
	def __call__(
		self, predicate: Callable[[tuple[K, V]], bool], /, *, factory: Callable[[], MutableMapping[K, V]]
	) -> Callable[[Mapping[K, V]], MutableMapping[K, V]]: ...

	# Stage 2a: Full application (no factory) - executes immediately
	@_overload
	def __call__(self, predicate: Callable[[tuple[K, V]], bool], d: Mapping[K, V], /) -> dict[K, V]: ...

	# Stage 2b: Full application (with factory) - executes immediately
	@_overload
	def __call__(
		self, predicate: Callable[[tuple[K, V]], bool], d: Mapping[K, V], /, *, factory: Callable[[], MutableMapping[K, V]]
	) -> MutableMapping[K, V]: ...

class __Itemmap(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., dict[K1, V1] | MutableMapping[K1, V1]]: ...

	# Stage 1a: Just func (no factory) - returns callable waiting for dict
	@_overload
	def __call__(self, func: Callable[[tuple[K0, V0]], tuple[K1, V1]], /) -> Callable[[Mapping[K0, V0]], dict[K1, V1]]: ...

	# Stage 1b: Func with factory - returns callable waiting for dict
	@_overload
	def __call__(
		self, func: Callable[[tuple[K0, V0]], tuple[K1, V1]], /, *, factory: Callable[[], MutableMapping[K1, V1]]
	) -> Callable[[Mapping[K0, V0]], MutableMapping[K1, V1]]: ...

	# Stage 2a: Full application (no factory) - executes immediately
	@_overload
	def __call__(self, func: Callable[[tuple[K0, V0]], tuple[K1, V1]], d: Mapping[K0, V0], /) -> dict[K1, V1]: ...

	# Stage 2b: Full application (with factory) - executes immediately
	@_overload
	def __call__(
		self, func: Callable[[tuple[K0, V0]], tuple[K1, V1]], d: Mapping[K0, V0], /, *, factory: Callable[[], MutableMapping[K1, V1]]
	) -> MutableMapping[K1, V1]: ...

class __Iterate(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., Iterator[T]]: ...

	# Stage 1: Just func - returns callable waiting for x
	@_overload
	def __call__(self, func: Callable[[T], T], /) -> Callable[[T], Iterator[T]]: ...

	# Stage 2: Full application - executes immediately
	@_overload
	def __call__(self, func: Callable[[T], T], x: T, /) -> Iterator[T]: ...

class __Join(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., Iterator[tuple[T, U]]]: ...

	# Stage 1: Just leftkey - returns a callable
	@_overload
	def __call__(self, leftkey: Callable[[T], Hashable], /) -> Callable[..., Iterator[tuple[T, U]]]: ...

	# Stage 2: leftkey + leftseq - returns a callable
	@_overload
	def __call__(self, leftkey: Callable[[T], Hashable], leftseq: Iterable[T], /) -> Callable[..., Iterator[tuple[T, U]]]: ...

	# Stage 3: leftkey + leftseq + rightkey - returns callable waiting for rightseq
	# This is the key overload for pipe usage!
	# Note: We use Any for U because U can't be inferred until rightseq is provided.
	# The callable will properly infer types when called with rightseq.
	@_overload
	def __call__(
		self, leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Callable[..., Hashable], /
	) -> Callable[[Iterable[Any]], Iterator[tuple[T, Any]]]: ...

	# Stage 4a: Full application (inner join) - executes immediately
	@_overload
	def __call__(
		self, leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U], /
	) -> Iterator[tuple[T, U]]: ...

	# Stage 4b: Full application with left_default only (right outer join)
	@_overload
	def __call__(
		self,
		leftkey: Callable[[T], Hashable],
		leftseq: Iterable[T],
		rightkey: Callable[[U], Hashable],
		rightseq: Iterable[U],
		/,
		left_default: L,
	) -> Iterator[tuple[T | L, U]]: ...

	# Stage 4c: Full application with right_default only (left outer join)
	@_overload
	def __call__(
		self,
		leftkey: Callable[[T], Hashable],
		leftseq: Iterable[T],
		rightkey: Callable[[U], Hashable],
		rightseq: Iterable[U],
		/,
		*,
		right_default: R,
	) -> Iterator[tuple[T, U | R]]: ...

	# Stage 4d: Full application with both defaults (full outer join)
	@_overload
	def __call__(
		self,
		leftkey: Callable[[T], Hashable],
		leftseq: Iterable[T],
		rightkey: Callable[[U], Hashable],
		rightseq: Iterable[U],
		/,
		left_default: L,
		right_default: R,
	) -> Iterator[tuple[T | L, U | R]]: ...

	# Stage 3 with defaults: leftkey + leftseq + rightkey + defaults - returns callable
	@_overload
	def __call__(
		self,
		leftkey: Callable[[T], Hashable],
		leftseq: Iterable[T],
		rightkey: Callable[[U], Hashable],
		/,
		left_default: L,
		right_default: R,
	) -> Callable[[Iterable[U]], Iterator[tuple[T | L, U | R]]]: ...

class __Keyfilter(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., dict[K, V] | MutableMapping[K, V]]: ...

	# Stage 1a: Just predicate (no factory) - returns callable waiting for dict
	@_overload
	def __call__(self, predicate: Callable[[K], bool], /) -> Callable[[Mapping[K, V]], dict[K, V]]: ...

	# Stage 1b: Predicate with factory - returns callable waiting for dict
	@_overload
	def __call__(
		self, predicate: Callable[[K], bool], /, *, factory: Callable[[], MutableMapping[K, V]]
	) -> Callable[[Mapping[K, V]], MutableMapping[K, V]]: ...

	# Stage 2a: Full application (no factory) - executes immediately
	@_overload
	def __call__(self, predicate: Callable[[K], bool], d: Mapping[K, V], /) -> dict[K, V]: ...

	# Stage 2b: Full application (with factory) - executes immediately
	@_overload
	def __call__(
		self, predicate: Callable[[K], bool], d: Mapping[K, V], /, *, factory: Callable[[], MutableMapping[K, V]]
	) -> MutableMapping[K, V]: ...

class __Keymap(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., dict[K1, V] | MutableMapping[K1, V]]: ...

	# Stage 1a: Just func (no factory) - returns callable waiting for dict
	@_overload
	def __call__(self, func: Callable[[K0], K1], /) -> Callable[[Mapping[K0, V]], dict[K1, V]]: ...

	# Stage 1b: Func with factory - returns callable waiting for dict
	@_overload
	def __call__(
		self, func: Callable[[K0], K1], /, *, factory: Callable[[], MutableMapping[K1, V]]
	) -> Callable[[Mapping[K0, V]], MutableMapping[K1, V]]: ...

	# Stage 2a: Full application (no factory) - executes immediately
	@_overload
	def __call__(self, func: Callable[[K0], K1], d: Mapping[K0, V], /) -> dict[K1, V]: ...

	# Stage 2b: Full application (with factory) - executes immediately
	@_overload
	def __call__(
		self, func: Callable[[K0], K1], d: Mapping[K0, V], /, *, factory: Callable[[], MutableMapping[K1, V]]
	) -> MutableMapping[K1, V]: ...

class __Map(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., Iterator[S] | Callable[..., Iterator[S]]]: ...
	@_overload
	def __call__(self, func: Callable[[T1], S], /) -> Callable[[Iterable[T1]], Iterator[S]]: ...
	@_overload
	def __call__(self, func: Callable[[T1, T2], S], /) -> Callable[[Iterable[T1], Iterable[T2]], Iterator[S]]: ...
	@_overload
	def __call__(self, func: Callable[[T1, T2, T3], S], /) -> Callable[[Iterable[T1], Iterable[T2], Iterable[T3]], Iterator[S]]: ...
	@_overload
	def __call__(
		self, func: Callable[[T1, T2, T3, T4], S], /
	) -> Callable[[Iterable[T1], Iterable[T2], Iterable[T3], Iterable[T4]], Iterator[S]]: ...
	@_overload
	def __call__(
		self, func: Callable[[T1, T2, T3, T4, T5], S], /
	) -> Callable[[Iterable[T1], Iterable[T2], Iterable[T3], Iterable[T4], Iterable[T5]], Iterator[S]]: ...
	@_overload
	def __call__(self, func: Callable[[T1], S], iterable: Iterable[T1], /) -> Iterator[S]: ...
	@_overload
	def __call__(self, func: Callable[[T1, T2], S], iterable: Iterable[T1], iter2: Iterable[T2], /) -> Iterator[S]: ...
	@_overload
	def __call__(
		self, func: Callable[[T1, T2, T3], S], iterable: Iterable[T1], iter2: Iterable[T2], iter3: Iterable[T3], /
	) -> Iterator[S]: ...
	@_overload
	def __call__(
		self, func: Callable[[T1, T2, T3, T4], S], iterable: Iterable[T1], iter2: Iterable[T2], iter3: Iterable[T3], iter4: Iterable[T4], /
	) -> Iterator[S]: ...
	@_overload
	def __call__(
		self,
		func: Callable[[T1, T2, T3, T4, T5], S],
		iterable: Iterable[T1],
		iter2: Iterable[T2],
		iter3: Iterable[T3],
		iter4: Iterable[T4],
		iter5: Iterable[T5],
		/,
	) -> Iterator[S]: ...
	@_overload
	def __call__(
		self,
		func: Callable[..., S],
		iterable: Iterable[Any],
		iter2: Iterable[Any],
		iter3: Iterable[Any],
		iter4: Iterable[Any],
		iter5: Iterable[Any],
		iter6: Iterable[Any],
		/,
		*iterables: Iterable[Any],
	) -> Iterator[S]: ...

class __Mapcat(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., Iterator[R] | Callable[..., Iterator[R]]]: ...
	@_overload
	def __call__(self, func: Callable[[T], Iterable[R]], /) -> Callable[[Iterable[T]], Iterator[R]]: ...
	@_overload
	def __call__(self, func: Callable[[T], Iterable[R]], seqs: Iterable[T], /) -> Iterator[R]: ...

class __Nth(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., T]: ...

	# Stage 1: Just n - returns callable waiting for seq
	@_overload
	def __call__(self, n: int, /) -> Callable[[Iterable[T]], T]: ...

	# Stage 2: Full application - executes immediately
	@_overload
	def __call__(self, n: int, seq: Iterable[T], /) -> T: ...

class __Partition(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., Iterator[tuple[T, ...]]]: ...
	@_overload
	def __call__(self, n: int, /) -> Callable[..., Iterator[tuple[T, ...]]]: ...
	@_overload
	def __call__(self, n: Literal[1], seq: Iterable[T], /) -> Iterator[tuple[T]]: ...
	@_overload
	def __call__(self, n: int, seq: Iterable[T], /) -> Iterator[tuple[T, ...]]: ...
	@_overload
	def __call__(self, n: Literal[1], seq: Iterable[T], pad: Any, /) -> Iterator[tuple[T]]:
		# Note: With n=1, tuples always have exactly 1 element, so pad is never used
		...

	@_overload
	def __call__(self, n: int, seq: Iterable[T], pad: PType, /) -> Iterator[tuple[T | PType, ...]]: ...

class __PartitionAll(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., Iterator[tuple[T, ...]]]: ...

	# Stage 1: Just n - returns callable waiting for seq
	@_overload
	def __call__(self, n: Literal[1], /) -> Callable[[Iterable[T]], Iterator[tuple[T]]]: ...
	@_overload
	def __call__(self, n: int, /) -> Callable[[Iterable[T]], Iterator[tuple[T, ...]]]: ...

	# Stage 2: Full application - executes immediately
	@_overload
	def __call__(self, n: Literal[1], seq: Iterable[T], /) -> Iterator[tuple[T]]: ...
	@_overload
	def __call__(self, n: int, seq: Iterable[T], /) -> Iterator[tuple[T, ...]]: ...

class __Pluck(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., Iterator[T] | Iterator[tuple[T, ...]]]: ...
	@_overload
	def __call__(
		self, ind: Sequence[Any], /
	) -> (
		Callable[[Iterable[Sequence[T] | Mapping[Any, T]]], Iterator[tuple[T, ...]]]
		| Callable[[Iterable[Sequence[T] | Mapping[Any, T]], T], Iterator[tuple[T, ...]]]
	): ...
	@_overload
	def __call__(
		self, ind: Any, /
	) -> (
		Callable[[Iterable[Sequence[T] | Mapping[Any, T]]], Iterator[T]]
		| Callable[[Iterable[Sequence[T] | Mapping[Any, T]], T], Iterator[T]]
	): ...
	@_overload
	def __call__(self, ind: Sequence[Any], seqs: Iterable[Sequence[T] | Mapping[Any, T]], /) -> Iterator[tuple[T, ...]]: ...
	@_overload
	def __call__(self, ind: Any, seqs: Iterable[Sequence[T] | Mapping[Any, T]], /) -> Iterator[T]: ...
	@_overload
	def __call__(self, ind: Sequence[Any], seqs: Iterable[Sequence[T] | Mapping[Any, T]], default: T, /) -> Iterator[tuple[T, ...]]: ...
	@_overload
	def __call__(self, ind: Any, seqs: Iterable[Sequence[T] | Mapping[Any, T]], default: T, /) -> Iterator[T]: ...

class __Reduce(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., T]: ...
	@_overload
	def __call__(self, function: Callable[[T, T], T], /) -> Callable[[Iterable[T]], T]: ...
	@_overload
	def __call__(self, function: Callable[[T, S], T], /) -> Callable[..., T]: ...
	@_overload
	def __call__(self, function: Callable[[T, T], T], iterable: Iterable[T], /) -> T: ...
	@_overload
	def __call__(self, function: Callable[[T, S], T], iterable: Iterable[S], initial: T, /) -> T: ...

class __Remove(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., Iterable[T]]: ...

	# Stage 1: Just predicate - returns callable waiting for seq
	@_overload
	def __call__(self, predicate: Callable[[T], bool], /) -> Callable[[Iterable[T]], Iterable[T]]: ...

	# Stage 2: Full application - executes immediately
	@_overload
	def __call__(self, predicate: Callable[[T], bool], seq: Iterable[T], /) -> Iterable[T]: ...

class __SlidingWindow(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., Iterator[tuple[T, ...]]]: ...

	# Stage 1a: Just n=1 - returns callable waiting for seq
	@_overload
	def __call__(self, n: Literal[1], /) -> Callable[[Iterable[T]], Iterator[tuple[T]]]: ...

	# Stage 1b: Just n=2 - returns callable waiting for seq
	@_overload
	def __call__(self, n: Literal[2], /) -> Callable[[Iterable[T]], Iterator[tuple[T, T]]]: ...

	# Stage 1c: Just n=3 - returns callable waiting for seq
	@_overload
	def __call__(self, n: Literal[3], /) -> Callable[[Iterable[T]], Iterator[tuple[T, T, T]]]: ...

	# Stage 1d: Just n (general) - returns callable waiting for seq
	@_overload
	def __call__(self, n: int, /) -> Callable[[Iterable[T]], Iterator[tuple[T, ...]]]: ...

	# Stage 2a: Full application with n=1 - executes immediately
	@_overload
	def __call__(self, n: Literal[1], seq: Iterable[T], /) -> Iterator[tuple[T]]: ...

	# Stage 2b: Full application with n=2 - executes immediately
	@_overload
	def __call__(self, n: Literal[2], seq: Iterable[T], /) -> Iterator[tuple[T, T]]: ...

	# Stage 2c: Full application with n=3 - executes immediately
	@_overload
	def __call__(self, n: Literal[3], seq: Iterable[T], /) -> Iterator[tuple[T, T, T]]: ...

	# Stage 2d: Full application (general) - executes immediately
	@_overload
	def __call__(self, n: int, seq: Iterable[T], /) -> Iterator[tuple[T, ...]]: ...

class __Sorted(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., list[T]]: ...

	# Stage 1a: Partial application with keyword args only (no key) - returns callable
	@_overload
	def __call__(self, *, key: None = None, reverse: bool = False) -> Callable[[Iterable[T]], list[T]]: ...

	# Stage 1b: Partial application with keyword args only (with key) - returns callable
	@_overload
	def __call__(self, *, key: Callable[[T], SupportsRichComparison], reverse: bool = False) -> Callable[[Iterable[T]], list[T]]: ...

	# Stage 2a: Full application (no key) - executes immediately
	@_overload
	def __call__(self, iterable: Iterable[T], /, *, key: None = None, reverse: bool = False) -> list[T]: ...

	# Stage 2b: Full application (with key function) - executes immediately
	@_overload
	def __call__(self, iterable: Iterable[T], /, *, key: Callable[[T], SupportsRichComparison], reverse: bool = False) -> list[T]: ...

class __Tail(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., Iterator[T]]: ...

	# Stage 1: Just n - returns callable waiting for seq
	@_overload
	def __call__(self, n: int, /) -> Callable[[Iterable[T]], Iterator[T]]: ...

	# Stage 2: Full application - executes immediately
	@_overload
	def __call__(self, n: int, seq: Iterable[T], /) -> Iterator[T]: ...

class __Take(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., Iterator[T]]: ...
	@_overload
	def __call__(self, n: int, /) -> Callable[[Iterable[T]], Iterator[T]]: ...
	@_overload
	def __call__(self, n: int, seq: Iterable[T], /) -> Iterator[T]: ...

class __TakeNth(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., Iterator[T]]: ...

	# Stage 1: Just n - returns callable waiting for seq
	@_overload
	def __call__(self, n: int, /) -> Callable[[Iterable[T]], Iterator[T]]: ...

	# Stage 2: Full application - executes immediately
	@_overload
	def __call__(self, n: int, seq: Iterable[T], /) -> Iterator[T]: ...

class __Valfilter(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., dict[K, V] | MutableMapping[K, V]]: ...

	# Stage 1a: Just predicate (no factory) - returns callable waiting for dict
	@_overload
	def __call__(self, predicate: Callable[[V], bool], /) -> Callable[[Mapping[K, V]], dict[K, V]]: ...

	# Stage 1b: Predicate with factory - returns callable waiting for dict
	@_overload
	def __call__(
		self, predicate: Callable[[V], bool], /, *, factory: Callable[[], MutableMapping[K, V]]
	) -> Callable[[Mapping[K, V]], MutableMapping[K, V]]: ...

	# Stage 2a: Full application (no factory) - executes immediately
	@_overload
	def __call__(self, predicate: Callable[[V], bool], d: Mapping[K, V], /) -> dict[K, V]: ...

	# Stage 2b: Full application (with factory) - executes immediately
	@_overload
	def __call__(
		self, predicate: Callable[[V], bool], d: Mapping[K, V], /, *, factory: Callable[[], MutableMapping[K, V]]
	) -> MutableMapping[K, V]: ...

class __Valmap(__Protocol):
	@_overload
	def __call__(self) -> Callable[..., dict[K, V1] | MutableMapping[K, V1]]: ...

	# Stage 1a: Just func (no factory) - returns callable waiting for dict
	@_overload
	def __call__(self, func: Callable[[V0], V1], /) -> Callable[[Mapping[K, V0]], dict[K, V1]]: ...

	# Stage 1b: Func with factory - returns callable waiting for dict
	@_overload
	def __call__(
		self, func: Callable[[V0], V1], /, *, factory: Callable[[], MutableMapping[K, V1]]
	) -> Callable[[Mapping[K, V0]], MutableMapping[K, V1]]: ...

	# Stage 2a: Full application (no factory) - executes immediately
	@_overload
	def __call__(self, func: Callable[[V0], V1], d: Mapping[K, V0], /) -> dict[K, V1]: ...

	# Stage 2b: Full application (with factory) - executes immediately
	@_overload
	def __call__(
		self, func: Callable[[V0], V1], d: Mapping[K, V0], /, *, factory: Callable[[], MutableMapping[K, V1]]
	) -> MutableMapping[K, V1]: ...

accumulate = __cast('__Accumulate', humpy_toolz.curry(humpy_toolz.accumulate))
assoc = __cast('__Assoc', humpy_toolz.curry(humpy_toolz.assoc))
assoc_in = humpy_toolz.curry(humpy_toolz.assoc_in)
cons = __cast('__Cons', humpy_toolz.curry(humpy_toolz.cons))
countby = humpy_toolz.curry(humpy_toolz.countby)
dissoc = humpy_toolz.curry(humpy_toolz.dissoc)
do = __cast('__Do', humpy_toolz.curry(humpy_toolz.do))
drop = __cast('__Drop', humpy_toolz.curry(humpy_toolz.drop))
excepts = __cast('__Excepts', humpy_toolz.curry(humpy_toolz.excepts))
filter = __cast('__Filter', humpy_toolz.curry(humpy_toolz.filter))
get = __cast('__Get', humpy_toolz.curry(humpy_toolz.get))
get_in = humpy_toolz.curry(humpy_toolz.get_in)
groupby = __cast('__Groupby', humpy_toolz.curry(humpy_toolz.groupby))
interpose = __cast('__Interpose', humpy_toolz.curry(humpy_toolz.interpose))
itemfilter = __cast('__Itemfilter', humpy_toolz.curry(humpy_toolz.itemfilter))
itemmap = __cast('__Itemmap', humpy_toolz.curry(humpy_toolz.itemmap))
iterate = __cast('__Iterate', humpy_toolz.curry(humpy_toolz.iterate))
join = __cast('__Join', humpy_toolz.curry(humpy_toolz.join))
keyfilter = __cast('__Keyfilter', humpy_toolz.curry(humpy_toolz.keyfilter))
keymap = __cast('__Keymap', humpy_toolz.curry(humpy_toolz.keymap))
map = __cast('__Map', humpy_toolz.curry(humpy_toolz.map))
mapcat = __cast('__Mapcat', humpy_toolz.curry(humpy_toolz.mapcat))
nth = __cast('__Nth', humpy_toolz.curry(humpy_toolz.nth))
partial = humpy_toolz.curry(humpy_toolz.partial)
partition = __cast('__Partition', humpy_toolz.curry(humpy_toolz.partition))
partition_all = __cast('__PartitionAll', humpy_toolz.curry(humpy_toolz.partition_all))
partitionby = humpy_toolz.curry(humpy_toolz.partitionby)
peekn = humpy_toolz.curry(humpy_toolz.peekn)
pluck = __cast('__Pluck', humpy_toolz.curry(humpy_toolz.pluck))
random_sample = humpy_toolz.curry(humpy_toolz.random_sample)
reduce = __cast('__Reduce', humpy_toolz.curry(humpy_toolz.reduce))
reduceby = humpy_toolz.curry(humpy_toolz.reduceby)
remove = __cast('__Remove', humpy_toolz.curry(humpy_toolz.remove))
sliding_window = __cast('__SlidingWindow', humpy_toolz.curry(humpy_toolz.sliding_window))
sorted = __cast('__Sorted', humpy_toolz.curry(humpy_toolz.sorted))
tail = __cast('__Tail', humpy_toolz.curry(humpy_toolz.tail))
take = __cast('__Take', humpy_toolz.curry(humpy_toolz.take))
take_nth = __cast('__TakeNth', humpy_toolz.curry(humpy_toolz.take_nth))
topk = humpy_toolz.curry(humpy_toolz.topk)
unique = humpy_toolz.curry(humpy_toolz.unique)
update_in = humpy_toolz.curry(humpy_toolz.update_in)
valfilter = __cast('__Valfilter', humpy_toolz.curry(humpy_toolz.valfilter))
valmap = __cast('__Valmap', humpy_toolz.curry(humpy_toolz.valmap))
del __Accumulate
del __Assoc
del __Cons
del __Do
del __Drop
del __Excepts
del __Filter
del __Get
del __Groupby
del __Interpose
del __Itemfilter
del __Itemmap
del __Iterate
del __Join
del __Keyfilter
del __Keymap
del __Map
del __Mapcat
del __Nth
del __Partition
del __PartitionAll
del __Pluck
del __Reduce
del __Remove
del __SlidingWindow
del __Sorted
del __Tail
del __Take
del __TakeNth
del __Valfilter
del __Valmap
del __cast
del _overload
del __ParamSpec
del __Protocol
del __TypeVar
del humpy_toolz
