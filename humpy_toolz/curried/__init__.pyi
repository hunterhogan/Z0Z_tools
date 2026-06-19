from .. import dicttoolz as _dicttoolz, itertoolz as _itertoolz, recipes as _recipes
from ..functoolz import (
	apply as apply, complement as complement, compose as comp, compose as compose, compose_left as compose_left, curry as curry,
	excepts as _excepts_class, flip as flip, identity as identity, juxt as juxt, memoize as memoize, pipe as pipe,
	thread_first as thread_first, thread_last as thread_last)
from ..itertoolz import (
	concat as concat, concatv as concatv, count as count, diff as diff, first as first, frequencies as frequencies, interleave as interleave,
	isdistinct as isdistinct, isiterable as isiterable, last as last, merge_sorted as merge_sorted, peek as peek, second as second)
# All functions from operator module are re-exported here.
# Binary and n-ary functions are curried; unary functions are not.
# From a typing perspective, curried functions have identical signatures.
from . import operator
from .exceptions import merge, merge_with
from _typeshed import SupportsRichComparison
from collections.abc import Callable, Hashable, Iterable, Iterator, Mapping, MutableMapping, Sequence
from typing import Any, Literal, overload, TypeGuard, ParamSpec, TypeVar
from typing_extensions import TypeIs
import functools

P = ParamSpec('P')
K = TypeVar('K')
K0 = TypeVar('K0')
K1 = TypeVar('K1')
KT = TypeVar('KT')
L = TypeVar('L')
PType = TypeVar('PType')
R = TypeVar('R')
S = TypeVar('S')
T = TypeVar('T')
T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')
T5 = TypeVar('T5')
U = TypeVar('U')
V = TypeVar('V')
V0 = TypeVar('V0')
V1 = TypeVar('V1')

__all__ = [
	# Curried functions (defined in this module)
	"accumulate",
	"assoc",
	"assoc_in",
	"cons",
	"countby",
	"dissoc",
	"do",
	"drop",
	"excepts",
	"filter",
	"get",
	"get_in",
	"groupby",
	"interpose",
	"itemfilter",
	"itemmap",
	"iterate",
	"join",
	"keyfilter",
	"keymap",
	"map",
	"mapcat",
	"nth",
	"partial",
	"partition",
	"partition_all",
	"partitionby",
	"peekn",
	"pluck",
	"random_sample",
	"reduce",
	"reduceby",
	"remove",
	"sliding_window",
	"sorted",
	"tail",
	"take",
	"take_nth",
	"topk",
	"unique",
	"update_in",
	"valfilter",
	"valmap",
	# Re-exported (not curried)
	"apply",
	"comp",
	"complement",
	"compose",
	"compose_left",
	"concat",
	"concatv",
	"count",
	"curry",
	"diff",
	"first",
	"flip",
	"frequencies",
	"identity",
	"interleave",
	"isdistinct",
	"isiterable",
	"juxt",
	"last",
	"memoize",
	"merge_sorted",
	"peek",
	"pipe",
	"second",
	"thread_first",
	"thread_last",
	# Re-exported from .exceptions
	"merge",
	"merge_with",
	# Submodule
	"operator",
]

# Curried accumulate with explicit overloads for type safety
# Stage 0: No arguments - returns a callable
@overload
def accumulate() -> Callable[..., Iterator[T]]: ...

# Stage 1: Just binop - returns callable waiting for seq (and optional initial)
@overload
def accumulate(
	binop: Callable[[T, T], T], /
) -> Callable[..., Iterator[T]]: ...

# Stage 2a: binop + seq (no initial) - executes immediately
@overload
def accumulate(
	binop: Callable[[T, T], T], seq: Iterable[T], /
) -> Iterator[T]: ...

# Stage 2b: binop + seq + initial - executes immediately
@overload
def accumulate(
	binop: Callable[[T, T], T],
	seq: Iterable[T],
	initial: T,
	/,
) -> Iterator[T]: ...
def accumulate(
	binop: Callable[[T, T], T] = ...,
	seq: Iterable[T] = ...,
	initial: T = ...,
) -> Iterator[T] | Callable[..., Iterator[T]]:
	...

@overload
def assoc() -> Callable[
	..., dict[K, V] | MutableMapping[K, V]
]: ...
@overload
def assoc(
	d: Mapping[K, V], /
) -> Callable[..., dict[K, V] | MutableMapping[K, V]]: ...
@overload
def assoc(
	d: Mapping[K, V], key: K, /
) -> Callable[[V], dict[K, V]]: ...
@overload
def assoc(
	d: Mapping[K, V],
	key: K,
	/,
	*,
	factory: Callable[[], MutableMapping[K, V]],
) -> Callable[[V], MutableMapping[K, V]]: ...
@overload
def assoc(
	d: Mapping[K, V], key: K, value: V, /
) -> dict[K, V]: ...
@overload
def assoc(
	d: Mapping[K, V],
	key: K,
	value: V,
	/,
	*,
	factory: Callable[[], MutableMapping[K, V]],
) -> MutableMapping[K, V]: ...
def assoc(
	d: Mapping[K, V] = ...,
	key: K = ...,
	value: V = ...,
	*,
	factory: Callable[[], MutableMapping[K, V]] = dict,
) -> (
	dict[K, V]
	| MutableMapping[K, V]
	| Callable[..., dict[K, V] | MutableMapping[K, V]]
):
	...

assoc_in = curry(_dicttoolz.assoc_in)

# Curried cons with explicit overloads for type safety
# Stage 0: No arguments - returns a callable
@overload
def cons() -> Callable[..., Iterator[T]]: ...

# Stage 1: Just el - returns callable waiting for seq
@overload
def cons(
	el: T, /
) -> Callable[[Iterable[T]], Iterator[T]]: ...

# Stage 2: Full application - executes immediately
@overload
def cons(
	el: T, seq: Iterable[T], /
) -> Iterator[T]: ...
def cons(
	el: T = ..., seq: Iterable[T] = ...
) -> (
	Iterator[T]
	| Callable[[Iterable[T]], Iterator[T]]
	| Callable[..., Iterator[T]]
):
	...

countby = curry(_recipes.countby)
dissoc = curry(_dicttoolz.dissoc)

# Curried do with explicit overloads for type safety
# Stage 0: No arguments - returns a callable
@overload
def do() -> Callable[..., T]: ...

# Stage 1: Just func - returns callable waiting for x
@overload
def do(func: Callable[[T], Any], /) -> Callable[[T], T]: ...

# Stage 2: Full application - executes immediately
@overload
def do(func: Callable[[T], Any], x: T, /) -> T: ...
def do(
	func: Callable[[T], Any] = ..., x: T = ...
) -> T | Callable[[T], T] | Callable[..., T]:
	...

@overload
def drop() -> Callable[..., Iterator[T]]: ...
@overload
def drop(
	n: int, /
) -> Callable[[Iterable[T]], Iterator[T]]: ...
@overload
def drop(
	n: int, seq: Iterable[T], /
) -> Iterator[T]: ...
def drop(
	n: int = ..., seq: Iterable[T] = ...
) -> (
	Iterator[T]
	| Callable[[Iterable[T]], Iterator[T]]
	| Callable[..., Iterator[T]]
):
	...

@overload
def excepts() -> Callable[..., _excepts_class[T, P]]: ...
@overload
def excepts(
	exc: type[Exception] | tuple[type[Exception], ...], /
) -> (
	Callable[[Callable[P, T]], _excepts_class[T, P]]
	| Callable[
		[Callable[P, T], Callable[[Exception], T]],
		_excepts_class[T, P],
	]
): ...
@overload
def excepts(
	exc: type[Exception] | tuple[type[Exception], ...],
	func: Callable[P, T],
	/,
) -> _excepts_class[T, P]: ...
@overload
def excepts(
	exc: type[Exception] | tuple[type[Exception], ...],
	func: Callable[P, T],
	handler: Callable[[Exception], T],
	/,
) -> _excepts_class[T, P]: ...
def excepts(
	exc: type[Exception] | tuple[type[Exception], ...] = ...,
	func: Callable[P, T] = ...,
	handler: Callable[[Exception], T] | None = ...,
) -> _excepts_class[T, P] | Callable[..., _excepts_class[T, P]]:
	...

@overload
def filter() -> Callable[  # noqa: A001
	..., Iterator[T] | Callable[..., Iterator[T]]
]: ...
@overload
def filter(  # noqa: A001
	function: None, /
) -> Callable[
	[Iterable[T | None]], Iterator[T]
]: ...
@overload
def filter(
	function: Callable[[S], TypeGuard[T]], /
) -> Callable[[Iterable[S]], Iterator[T]]: ...
@overload
def filter(
	function: Callable[[S], TypeIs[T]], /
) -> Callable[[Iterable[S]], Iterator[T]]: ...
@overload
def filter(
	function: Callable[[T], Any], /
) -> Callable[[Iterable[T]], Iterator[T]]: ...
@overload
def filter(
	function: None, iterable: Iterable[T | None], /
) -> Iterator[T]: ...
@overload
def filter(
	function: Callable[[S], TypeGuard[T]],
	iterable: Iterable[S],
	/,
) -> Iterator[T]: ...
@overload
def filter(
	function: Callable[[S], TypeIs[T]],
	iterable: Iterable[S],
	/,
) -> Iterator[T]: ...
@overload
def filter(
	function: Callable[[T], Any],
	iterable: Iterable[T],
	/,
) -> Iterator[T]: ...
def filter(
	function: Callable[[T], Any] | None = ...,
	iterable: Iterable[T] = ...,
) -> (
	Iterator[T]
	| Callable[[Iterable[T]], Iterator[T]]
	| Callable[
		...,
		Iterator[T] | Callable[..., Iterator[T]],
	]
):
	...

@overload
def get() -> Callable[..., T | tuple[T, ...]]: ...
@overload
def get(
	ind: Sequence[Any], /
) -> (
	Callable[
		[Sequence[T] | Mapping[Any, T]],
		tuple[T, ...],
	]
	| Callable[
		[Sequence[T] | Mapping[Any, T], T],
		tuple[T, ...],
	]
): ...
@overload
def get(
	ind: Any, /
) -> (
	Callable[
		[Sequence[T] | Mapping[Any, T]], T
	]
	| Callable[
		[Sequence[T] | Mapping[Any, T], T], T
	]
): ...
@overload
def get(
	ind: Sequence[Any],
	seq: Sequence[T] | Mapping[Any, T],
	/,
) -> tuple[T, ...]: ...
@overload
def get(
	ind: Any,
	seq: Sequence[T] | Mapping[Any, T],
	/,
) -> T: ...
@overload
def get(
	ind: Sequence[Any],
	seq: Sequence[T] | Mapping[Any, T],
	default: T,
	/,
) -> tuple[T, ...]: ...
@overload
def get(
	ind: Any,
	seq: Sequence[T] | Mapping[Any, T],
	default: T,
	/,
) -> T: ...
def get(
	ind: Any | Sequence[Any] = ...,
	seq: Sequence[T] | Mapping[Any, T] = ...,
	default: T = ...,
) -> T | tuple[T, ...] | Callable[..., T | tuple[T, ...]]:
	...

get_in = curry(_dicttoolz.get_in)

@overload
def groupby() -> Callable[..., dict[KT, list[T]]]: ...
@overload
def groupby(
	key: Callable[[T], KT], /
) -> Callable[[Iterable[T]], dict[KT, list[T]]]: ...
@overload
def groupby(
	key: Any, /
) -> Callable[[Iterable[T]], dict[Any, list[T]]]: ...
@overload
def groupby(
	key: Callable[[T], KT], seq: Iterable[T], /
) -> dict[KT, list[T]]: ...
@overload
def groupby(
	key: Any, seq: Iterable[T], /
) -> dict[Any, list[T]]: ...
def groupby(
	key: Callable[[T], KT] | Any = ...,
	seq: Iterable[T] = ...,
) -> (
	dict[KT, list[T]]
	| dict[Any, list[T]]
	| Callable[..., dict[KT, list[T]] | dict[Any, list[T]]]
):
	...

# Curried interpose with explicit overloads for type safety
# Stage 0: No arguments - returns a callable
@overload
def interpose() -> Callable[..., Iterator[T]]: ...

# Stage 1: Just el - returns callable waiting for seq
@overload
def interpose(
	el: T, /
) -> Callable[[Iterable[T]], Iterator[T]]: ...

# Stage 2: Full application - executes immediately
@overload
def interpose(
	el: T, seq: Iterable[T], /
) -> Iterator[T]: ...
def interpose(
	el: T = ..., seq: Iterable[T] = ...
) -> (
	Iterator[T]
	| Callable[[Iterable[T]], Iterator[T]]
	| Callable[..., Iterator[T]]
):
	...

@overload
def itemfilter() -> Callable[
	..., dict[K, V] | MutableMapping[K, V]
]: ...

# Stage 1a: Just predicate (no factory) - returns callable waiting for dict
@overload
def itemfilter(
	predicate: Callable[[tuple[K, V]], bool], /
) -> Callable[[Mapping[K, V]], dict[K, V]]: ...

# Stage 1b: Predicate with factory - returns callable waiting for dict
@overload
def itemfilter(
	predicate: Callable[[tuple[K, V]], bool],
	/,
	*,
	factory: Callable[[], MutableMapping[K, V]],
) -> Callable[
	[Mapping[K, V]], MutableMapping[K, V]
]: ...

# Stage 2a: Full application (no factory) - executes immediately
@overload
def itemfilter(
	predicate: Callable[[tuple[K, V]], bool],
	d: Mapping[K, V],
	/,
) -> dict[K, V]: ...

# Stage 2b: Full application (with factory) - executes immediately
@overload
def itemfilter(
	predicate: Callable[[tuple[K, V]], bool],
	d: Mapping[K, V],
	/,
	*,
	factory: Callable[[], MutableMapping[K, V]],
) -> MutableMapping[K, V]: ...
def itemfilter(
	predicate: Callable[[tuple[K, V]], bool] = ...,
	d: Mapping[K, V] = ...,
	*,
	factory: Callable[[], MutableMapping[K, V]] = dict,
) -> (
	dict[K, V]
	| MutableMapping[K, V]
	| Callable[..., dict[K, V] | MutableMapping[K, V]]
):
	...

@overload
def itemmap() -> Callable[
	..., dict[K1, V1] | MutableMapping[K1, V1]
]: ...

# Stage 1a: Just func (no factory) - returns callable waiting for dict
@overload
def itemmap(
	func: Callable[[tuple[K0, V0]], tuple[K1, V1]], /
) -> Callable[[Mapping[K0, V0]], dict[K1, V1]]: ...

# Stage 1b: Func with factory - returns callable waiting for dict
@overload
def itemmap(
	func: Callable[[tuple[K0, V0]], tuple[K1, V1]],
	/,
	*,
	factory: Callable[[], MutableMapping[K1, V1]],
) -> Callable[
	[Mapping[K0, V0]], MutableMapping[K1, V1]
]: ...

# Stage 2a: Full application (no factory) - executes immediately
@overload
def itemmap(
	func: Callable[[tuple[K0, V0]], tuple[K1, V1]],
	d: Mapping[K0, V0],
	/,
) -> dict[K1, V1]: ...

# Stage 2b: Full application (with factory) - executes immediately
@overload
def itemmap(
	func: Callable[[tuple[K0, V0]], tuple[K1, V1]],
	d: Mapping[K0, V0],
	/,
	*,
	factory: Callable[[], MutableMapping[K1, V1]],
) -> MutableMapping[K1, V1]: ...
def itemmap(
	func: Callable[[tuple[K0, V0]], tuple[K1, V1]] = ...,
	d: Mapping[K0, V0] = ...,
	*,
	factory: Callable[[], MutableMapping[K1, V1]] = dict,
) -> (
	dict[K1, V1]
	| MutableMapping[K1, V1]
	| Callable[..., dict[K1, V1] | MutableMapping[K1, V1]]
):
	...

# Curried iterate with explicit overloads for type safety
# Stage 0: No arguments - returns a callable
@overload
def iterate() -> Callable[..., Iterator[T]]: ...

# Stage 1: Just func - returns callable waiting for x
@overload
def iterate(
	func: Callable[[T], T], /
) -> Callable[[T], Iterator[T]]: ...

# Stage 2: Full application - executes immediately
@overload
def iterate(
	func: Callable[[T], T], x: T, /
) -> Iterator[T]: ...
def iterate(
	func: Callable[[T], T] = ..., x: T = ...
) -> (
	Iterator[T]
	| Callable[[T], Iterator[T]]
	| Callable[..., Iterator[T]]
):
	...

# Curried join with explicit overloads for type safety
# Stage 0: No arguments - returns a callable
@overload
def join() -> Callable[..., Iterator[tuple[T, U]]]: ...

# Stage 1: Just leftkey - returns a callable
@overload
def join(
	leftkey: Callable[[T], Hashable], /
) -> Callable[..., Iterator[tuple[T, U]]]: ...

# Stage 2: leftkey + leftseq - returns a callable
@overload
def join(
	leftkey: Callable[[T], Hashable],
	leftseq: Iterable[T],
	/,
) -> Callable[..., Iterator[tuple[T, U]]]: ...

# Stage 3: leftkey + leftseq + rightkey - returns callable waiting for rightseq
# This is the key overload for pipe usage!
# Note: We use Any for U because U can't be inferred until rightseq is provided.
# The callable will properly infer types when called with rightseq.
@overload
def join(
	leftkey: Callable[[T], Hashable],
	leftseq: Iterable[T],
	rightkey: Callable[..., Hashable],
	/,
) -> Callable[
	[Iterable[Any]],
	Iterator[tuple[T, Any]],
]: ...

# Stage 4a: Full application (inner join) - executes immediately
@overload
def join(
	leftkey: Callable[[T], Hashable],
	leftseq: Iterable[T],
	rightkey: Callable[[U], Hashable],
	rightseq: Iterable[U],
	/,
) -> Iterator[tuple[T, U]]: ...

# Stage 4b: Full application with left_default only (right outer join)
@overload
def join(
	leftkey: Callable[[T], Hashable],
	leftseq: Iterable[T],
	rightkey: Callable[[U], Hashable],
	rightseq: Iterable[U],
	/,
	left_default: L,
) -> Iterator[tuple[T | L, U]]: ...

# Stage 4c: Full application with right_default only (left outer join)
@overload
def join(
	leftkey: Callable[[T], Hashable],
	leftseq: Iterable[T],
	rightkey: Callable[[U], Hashable],
	rightseq: Iterable[U],
	/,
	*,
	right_default: R,
) -> Iterator[tuple[T, U | R]]: ...

# Stage 4d: Full application with both defaults (full outer join)
@overload
def join(
	leftkey: Callable[[T], Hashable],
	leftseq: Iterable[T],
	rightkey: Callable[[U], Hashable],
	rightseq: Iterable[U],
	/,
	left_default: L,
	right_default: R,
) -> Iterator[tuple[T | L, U | R]]: ...

# Stage 3 with defaults: leftkey + leftseq + rightkey + defaults - returns callable
@overload
def join(
	leftkey: Callable[[T], Hashable],
	leftseq: Iterable[T],
	rightkey: Callable[[U], Hashable],
	/,
	left_default: L,
	right_default: R,
) -> Callable[
	[Iterable[U]], Iterator[tuple[T | L, U | R]]
]: ...

# Implementation signature
def join(
	leftkey: Callable[[T], Hashable] | Hashable = ...,
	leftseq: Iterable[T] = ...,
	rightkey: Callable[[U], Hashable] | Hashable = ...,
	rightseq: Iterable[U] = ...,
	left_default: L = ...,
	right_default: R = ...,
) -> (
	Iterator[tuple[T | L, U | R]]
	| Callable[..., Iterator[tuple[T | L, U | R]]]
):
	...

# Curried keyfilter with explicit overloads for type safety
# Stage 0: No arguments - returns a callable
@overload
def keyfilter() -> Callable[
	..., dict[K, V] | MutableMapping[K, V]
]: ...

# Stage 1a: Just predicate (no factory) - returns callable waiting for dict
@overload
def keyfilter(
	predicate: Callable[[K], bool], /
) -> Callable[[Mapping[K, V]], dict[K, V]]: ...

# Stage 1b: Predicate with factory - returns callable waiting for dict
@overload
def keyfilter(
	predicate: Callable[[K], bool],
	/,
	*,
	factory: Callable[[], MutableMapping[K, V]],
) -> Callable[
	[Mapping[K, V]], MutableMapping[K, V]
]: ...

# Stage 2a: Full application (no factory) - executes immediately
@overload
def keyfilter(
	predicate: Callable[[K], bool],
	d: Mapping[K, V],
	/,
) -> dict[K, V]: ...

# Stage 2b: Full application (with factory) - executes immediately
@overload
def keyfilter(
	predicate: Callable[[K], bool],
	d: Mapping[K, V],
	/,
	*,
	factory: Callable[[], MutableMapping[K, V]],
) -> MutableMapping[K, V]: ...
def keyfilter(
	predicate: Callable[[K], bool] = ...,
	d: Mapping[K, V] = ...,
	*,
	factory: Callable[[], MutableMapping[K, V]] = dict,
) -> (
	dict[K, V]
	| MutableMapping[K, V]
	| Callable[..., dict[K, V] | MutableMapping[K, V]]
):
	...

@overload
def keymap() -> Callable[
	..., dict[K1, V] | MutableMapping[K1, V]
]: ...

# Stage 1a: Just func (no factory) - returns callable waiting for dict
@overload
def keymap(
	func: Callable[[K0], K1], /
) -> Callable[[Mapping[K0, V]], dict[K1, V]]: ...

# Stage 1b: Func with factory - returns callable waiting for dict
@overload
def keymap(
	func: Callable[[K0], K1],
	/,
	*,
	factory: Callable[[], MutableMapping[K1, V]],
) -> Callable[
	[Mapping[K0, V]], MutableMapping[K1, V]
]: ...

# Stage 2a: Full application (no factory) - executes immediately
@overload
def keymap(
	func: Callable[[K0], K1],
	d: Mapping[K0, V],
	/,
) -> dict[K1, V]: ...

# Stage 2b: Full application (with factory) - executes immediately
@overload
def keymap(
	func: Callable[[K0], K1],
	d: Mapping[K0, V],
	/,
	*,
	factory: Callable[[], MutableMapping[K1, V]],
) -> MutableMapping[K1, V]: ...
def keymap(
	func: Callable[[K0], K1] = ...,
	d: Mapping[K0, V] = ...,
	*,
	factory: Callable[[], MutableMapping[K1, V]] = dict,
) -> (
	dict[K1, V]
	| MutableMapping[K1, V]
	| Callable[..., dict[K1, V] | MutableMapping[K1, V]]
):
	...

@overload
def map() -> Callable[
	..., Iterator[S] | Callable[..., Iterator[S]]
]: ...
@overload
def map(
	func: Callable[[T1], S], /
) -> Callable[[Iterable[T1]], Iterator[S]]: ...
@overload
def map(
	func: Callable[[T1, T2], S], /
) -> Callable[
	[Iterable[T1], Iterable[T2]],
	Iterator[S],
]: ...
@overload
def map(
	func: Callable[[T1, T2, T3], S], /
) -> Callable[
	[
		Iterable[T1],
		Iterable[T2],
		Iterable[T3],
	],
	Iterator[S],
]: ...
@overload
def map(
	func: Callable[[T1, T2, T3, T4], S], /
) -> Callable[
	[
		Iterable[T1],
		Iterable[T2],
		Iterable[T3],
		Iterable[T4],
	],
	Iterator[S],
]: ...
@overload
def map(
	func: Callable[[T1, T2, T3, T4, T5], S], /
) -> Callable[
	[
		Iterable[T1],
		Iterable[T2],
		Iterable[T3],
		Iterable[T4],
		Iterable[T5],
	],
	Iterator[S],
]: ...
@overload
def map(
	func: Callable[[T1], S], iterable: Iterable[T1], /
) -> Iterator[S]: ...
@overload
def map(
	func: Callable[[T1, T2], S],
	iterable: Iterable[T1],
	iter2: Iterable[T2],
	/,
) -> Iterator[S]: ...
@overload
def map(
	func: Callable[[T1, T2, T3], S],
	iterable: Iterable[T1],
	iter2: Iterable[T2],
	iter3: Iterable[T3],
	/,
) -> Iterator[S]: ...
@overload
def map(
	func: Callable[[T1, T2, T3, T4], S],
	iterable: Iterable[T1],
	iter2: Iterable[T2],
	iter3: Iterable[T3],
	iter4: Iterable[T4],
	/,
) -> Iterator[S]: ...
@overload
def map(
	func: Callable[[T1, T2, T3, T4, T5], S],
	iterable: Iterable[T1],
	iter2: Iterable[T2],
	iter3: Iterable[T3],
	iter4: Iterable[T4],
	iter5: Iterable[T5],
	/,
) -> Iterator[S]: ...
@overload
def map(
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
def map(
	func: Callable[..., S] = ...,
	*iterables: Iterable[Any],
) -> (
	Iterator[S]
	| Callable[..., Iterator[S]]
	| Callable[
		...,
		Iterator[S] | Callable[..., Iterator[S]],
	]
):
	...

@overload
def mapcat() -> Callable[
	..., Iterator[R] | Callable[..., Iterator[R]]
]: ...
@overload
def mapcat(
	func: Callable[[T], Iterable[R]], /
) -> Callable[[Iterable[T]], Iterator[R]]: ...
@overload
def mapcat(
	func: Callable[[T], Iterable[R]],
	seqs: Iterable[T],
	/,
) -> Iterator[R]: ...
def mapcat(
	func: Callable[[T], Iterable[R]] = ...,
	seqs: Iterable[T] = ...,
) -> (
	Iterator[R]
	| Callable[[Iterable[T]], Iterator[R]]
	| Callable[
		...,
		Iterator[R] | Callable[..., Iterator[R]],
	]
):
	...

# Curried nth with explicit overloads for type safety
# Stage 0: No arguments - returns a callable
@overload
def nth() -> Callable[..., T]: ...

# Stage 1: Just n - returns callable waiting for seq
@overload
def nth(n: int, /) -> Callable[[Iterable[T]], T]: ...

# Stage 2: Full application - executes immediately
@overload
def nth(n: int, seq: Iterable[T], /) -> T: ...
def nth(
	n: int = ..., seq: Iterable[T] = ...
) -> T | Callable[[Iterable[T]], T] | Callable[..., T]:
	...

partial = curry(functools.partial)

@overload
def partition() -> Callable[..., Iterator[tuple[T, ...]]]: ...
@overload
def partition(
	n: int, /
) -> Callable[..., Iterator[tuple[T, ...]]]: ...
@overload
def partition(
	n: Literal[1], seq: Iterable[T], /
) -> Iterator[tuple[T]]: ...
@overload
def partition(
	n: int, seq: Iterable[T], /
) -> Iterator[tuple[T, ...]]: ...
@overload
def partition(
	n: Literal[1], seq: Iterable[T], pad: Any, /
) -> Iterator[tuple[T]]:
	# Note: With n=1, tuples always have exactly 1 element, so pad is never used
	...

@overload
def partition(
	n: int, seq: Iterable[T], pad: PType, /
) -> Iterator[tuple[T | PType, ...]]: ...
def partition(
	n: int = ...,
	seq: Iterable[T] = ...,
	pad: PType = ...,
) -> (
	Iterator[tuple[T, ...]]
	| Iterator[tuple[T | PType, ...]]
	| Callable[..., Iterator[tuple[T | PType, ...]]]
):
	...

# Curried partition_all with explicit overloads for type safety
# Stage 0: No arguments - returns a callable
@overload
def partition_all() -> Callable[
	..., Iterator[tuple[T, ...]]
]: ...

# Stage 1: Just n - returns callable waiting for seq
@overload
def partition_all(
	n: Literal[1], /
) -> Callable[
	[Iterable[T]], Iterator[tuple[T]]
]: ...
@overload
def partition_all(
	n: int, /
) -> Callable[
	[Iterable[T]], Iterator[tuple[T, ...]]
]: ...

# Stage 2: Full application - executes immediately
@overload
def partition_all(
	n: Literal[1], seq: Iterable[T], /
) -> Iterator[tuple[T]]: ...
@overload
def partition_all(
	n: int, seq: Iterable[T], /
) -> Iterator[tuple[T, ...]]: ...
def partition_all(
	n: int = ..., seq: Iterable[T] = ...
) -> (
	Iterator[tuple[T, ...]]
	| Callable[
		[Iterable[T]],
		Iterator[tuple[T, ...]] | Iterator[tuple[T]],
	]
	| Callable[..., Iterator[tuple[T, ...]]]
):
	...

partitionby = curry(_recipes.partitionby)
peekn = curry(_itertoolz.peekn)

@overload
def pluck() -> Callable[
	..., Iterator[T] | Iterator[tuple[T, ...]]
]: ...
@overload
def pluck(
	ind: Sequence[Any], /
) -> (
	Callable[
		[
			Iterable[
				Sequence[T] | Mapping[Any, T]
			]
		],
		Iterator[tuple[T, ...]],
	]
	| Callable[
		[
			Iterable[
				Sequence[T] | Mapping[Any, T]
			],
			T,
		],
		Iterator[tuple[T, ...]],
	]
): ...
@overload
def pluck(
	ind: Any, /
) -> (
	Callable[
		[
			Iterable[
				Sequence[T] | Mapping[Any, T]
			]
		],
		Iterator[T],
	]
	| Callable[
		[
			Iterable[
				Sequence[T] | Mapping[Any, T]
			],
			T,
		],
		Iterator[T],
	]
): ...
@overload
def pluck(
	ind: Sequence[Any],
	seqs: Iterable[
		Sequence[T] | Mapping[Any, T]
	],
	/,
) -> Iterator[tuple[T, ...]]: ...
@overload
def pluck(
	ind: Any,
	seqs: Iterable[
		Sequence[T] | Mapping[Any, T]
	],
	/,
) -> Iterator[T]: ...
@overload
def pluck(
	ind: Sequence[Any],
	seqs: Iterable[
		Sequence[T] | Mapping[Any, T]
	],
	default: T,
	/,
) -> Iterator[tuple[T, ...]]: ...
@overload
def pluck(
	ind: Any,
	seqs: Iterable[
		Sequence[T] | Mapping[Any, T]
	],
	default: T,
	/,
) -> Iterator[T]: ...
def pluck(
	ind: Any | Sequence[Any] = ...,
	seqs: Iterable[
		Sequence[T] | Mapping[Any, T]
	] = ...,
	default: T = ...,
) -> (
	Iterator[T]
	| Iterator[tuple[T, ...]]
	| Callable[
		..., Iterator[T] | Iterator[tuple[T, ...]]
	]
):
	...

random_sample = curry(_itertoolz.random_sample)

@overload
def reduce() -> Callable[..., T]: ...
@overload
def reduce(
	function: Callable[[T, T], T], /
) -> Callable[[Iterable[T]], T]: ...
@overload
def reduce(
	function: Callable[[T, S], T], /
) -> Callable[..., T]: ...
@overload
def reduce(
	function: Callable[[T, T], T],
	iterable: Iterable[T],
	/,
) -> T: ...
@overload
def reduce(
	function: Callable[[T, S], T],
	iterable: Iterable[S],
	initial: T,
	/,
) -> T: ...
def reduce(
	function: Callable[[T, S], T] = ...,
	iterable: Iterable[S] = ...,
	initial: T = ...,
) -> T | Callable[..., T]:
	...

reduceby = curry(_itertoolz.reduceby)

# Curried remove with explicit overloads for type safety
# Stage 0: No arguments - returns a callable
@overload
def remove() -> Callable[..., Iterable[T]]: ...

# Stage 1: Just predicate - returns callable waiting for seq
@overload
def remove(
	predicate: Callable[[T], bool], /
) -> Callable[[Iterable[T]], Iterable[T]]: ...

# Stage 2: Full application - executes immediately
@overload
def remove(
	predicate: Callable[[T], bool], seq: Iterable[T], /
) -> Iterable[T]: ...
def remove(
	predicate: Callable[[T], bool] = ..., seq: Iterable[T] = ...
) -> (
	Iterable[T]
	| Callable[[Iterable[T]], Iterable[T]]
	| Callable[..., Iterable[T]]
):
	...

# Curried sliding_window with explicit overloads for type safety
# Stage 0: No arguments - returns a callable
@overload
def sliding_window() -> Callable[
	..., Iterator[tuple[T, ...]]
]: ...

# Stage 1a: Just n=1 - returns callable waiting for seq
@overload
def sliding_window(
	n: Literal[1], /
) -> Callable[
	[Iterable[T]], Iterator[tuple[T]]
]: ...

# Stage 1b: Just n=2 - returns callable waiting for seq
@overload
def sliding_window(
	n: Literal[2], /
) -> Callable[
	[Iterable[T]], Iterator[tuple[T, T]]
]: ...

# Stage 1c: Just n=3 - returns callable waiting for seq
@overload
def sliding_window(
	n: Literal[3], /
) -> Callable[
	[Iterable[T]], Iterator[tuple[T, T, T]]
]: ...

# Stage 1d: Just n (general) - returns callable waiting for seq
@overload
def sliding_window(
	n: int, /
) -> Callable[
	[Iterable[T]], Iterator[tuple[T, ...]]
]: ...

# Stage 2a: Full application with n=1 - executes immediately
@overload
def sliding_window(
	n: Literal[1], seq: Iterable[T], /
) -> Iterator[tuple[T]]: ...

# Stage 2b: Full application with n=2 - executes immediately
@overload
def sliding_window(
	n: Literal[2], seq: Iterable[T], /
) -> Iterator[tuple[T, T]]: ...

# Stage 2c: Full application with n=3 - executes immediately
@overload
def sliding_window(
	n: Literal[3], seq: Iterable[T], /
) -> Iterator[tuple[T, T, T]]: ...

# Stage 2d: Full application (general) - executes immediately
@overload
def sliding_window(
	n: int, seq: Iterable[T], /
) -> Iterator[tuple[T, ...]]: ...
def sliding_window(
	n: int = ..., seq: Iterable[T] = ...
) -> (
	Iterator[tuple[T, ...]]
	| Callable[
		[Iterable[T]], Iterator[tuple[T, ...]]
	]
	| Callable[..., Iterator[tuple[T, ...]]]
):
	...

# Curried sorted with explicit overloads for type safety
# Note: key and reverse are keyword-only parameters in builtin sorted
# Stage 0: No arguments - returns a callable
@overload
def sorted() -> Callable[..., list[T]]: ...

# Stage 1a: Partial application with keyword args only (no key) - returns callable
@overload
def sorted(
	*,
	key: None = None,
	reverse: bool = False,
) -> Callable[[Iterable[T]], list[T]]: ...

# Stage 1b: Partial application with keyword args only (with key) - returns callable
@overload
def sorted(
	*,
	key: Callable[[T], SupportsRichComparison],
	reverse: bool = False,
) -> Callable[[Iterable[T]], list[T]]: ...

# Stage 2a: Full application (no key) - executes immediately
@overload
def sorted(
	iterable: Iterable[T],
	/,
	*,
	key: None = None,
	reverse: bool = False,
) -> list[T]: ...

# Stage 2b: Full application (with key function) - executes immediately
@overload
def sorted(
	iterable: Iterable[T],
	/,
	*,
	key: Callable[[T], SupportsRichComparison],
	reverse: bool = False,
) -> list[T]: ...

# Implementation signature (catch-all)
def sorted(
	iterable: Iterable[T] = ...,
	/,
	*,
	key: Callable[[T], SupportsRichComparison] | None = None,
	reverse: bool = False,
) -> list[T] | Callable[..., list[T]]:
	...

# Curried tail with explicit overloads for type safety
# Stage 0: No arguments - returns a callable
@overload
def tail() -> Callable[..., Iterator[T]]: ...

# Stage 1: Just n - returns callable waiting for seq
@overload
def tail(
	n: int, /
) -> Callable[[Iterable[T]], Iterator[T]]: ...

# Stage 2: Full application - executes immediately
@overload
def tail(
	n: int, seq: Iterable[T], /
) -> Iterator[T]: ...
def tail(
	n: int = ..., seq: Iterable[T] = ...
) -> (
	Iterator[T]
	| Callable[[Iterable[T]], Iterator[T]]
	| Callable[..., Iterator[T]]
):
	...

@overload
def take() -> Callable[..., Iterator[T]]: ...
@overload
def take(
	n: int, /
) -> Callable[[Iterable[T]], Iterator[T]]: ...
@overload
def take(
	n: int, seq: Iterable[T], /
) -> Iterator[T]: ...
def take(
	n: int = ..., seq: Iterable[T] = ...
) -> (
	Iterator[T]
	| Callable[[Iterable[T]], Iterator[T]]
	| Callable[..., Iterator[T]]
):
	...

# Curried take_nth with explicit overloads for type safety
# Stage 0: No arguments - returns a callable
@overload
def take_nth() -> Callable[..., Iterator[T]]: ...

# Stage 1: Just n - returns callable waiting for seq
@overload
def take_nth(
	n: int, /
) -> Callable[[Iterable[T]], Iterator[T]]: ...

# Stage 2: Full application - executes immediately
@overload
def take_nth(
	n: int, seq: Iterable[T], /
) -> Iterator[T]: ...
def take_nth(
	n: int = ..., seq: Iterable[T] = ...
) -> (
	Iterator[T]
	| Callable[[Iterable[T]], Iterator[T]]
	| Callable[..., Iterator[T]]
):
	...

topk = curry(_itertoolz.topk)
unique = curry(_itertoolz.unique)
update_in = curry(_dicttoolz.update_in)

@overload
def valfilter() -> Callable[
	..., dict[K, V] | MutableMapping[K, V]
]: ...

# Stage 1a: Just predicate (no factory) - returns callable waiting for dict
@overload
def valfilter(
	predicate: Callable[[V], bool], /
) -> Callable[[Mapping[K, V]], dict[K, V]]: ...

# Stage 1b: Predicate with factory - returns callable waiting for dict
@overload
def valfilter(
	predicate: Callable[[V], bool],
	/,
	*,
	factory: Callable[[], MutableMapping[K, V]],
) -> Callable[
	[Mapping[K, V]], MutableMapping[K, V]
]: ...

# Stage 2a: Full application (no factory) - executes immediately
@overload
def valfilter(
	predicate: Callable[[V], bool],
	d: Mapping[K, V],
	/,
) -> dict[K, V]: ...

# Stage 2b: Full application (with factory) - executes immediately
@overload
def valfilter(
	predicate: Callable[[V], bool],
	d: Mapping[K, V],
	/,
	*,
	factory: Callable[[], MutableMapping[K, V]],
) -> MutableMapping[K, V]: ...
def valfilter(
	predicate: Callable[[V], bool] = ...,
	d: Mapping[K, V] = ...,
	*,
	factory: Callable[[], MutableMapping[K, V]] = dict,
) -> (
	dict[K, V]
	| MutableMapping[K, V]
	| Callable[..., dict[K, V] | MutableMapping[K, V]]
):
	...

@overload
def valmap() -> Callable[
	..., dict[K, V1] | MutableMapping[K, V1]
]: ...

# Stage 1a: Just func (no factory) - returns callable waiting for dict
@overload
def valmap(
	func: Callable[[V0], V1], /
) -> Callable[[Mapping[K, V0]], dict[K, V1]]: ...

# Stage 1b: Func with factory - returns callable waiting for dict
@overload
def valmap(
	func: Callable[[V0], V1],
	/,
	*,
	factory: Callable[[], MutableMapping[K, V1]],
) -> Callable[
	[Mapping[K, V0]], MutableMapping[K, V1]
]: ...

# Stage 2a: Full application (no factory) - executes immediately
@overload
def valmap(
	func: Callable[[V0], V1],
	d: Mapping[K, V0],
	/,
) -> dict[K, V1]: ...

# Stage 2b: Full application (with factory) - executes immediately
@overload
def valmap(
	func: Callable[[V0], V1],
	d: Mapping[K, V0],
	/,
	*,
	factory: Callable[[], MutableMapping[K, V1]],
) -> MutableMapping[K, V1]: ...
def valmap(
	func: Callable[[V0], V1] = ...,
	d: Mapping[K, V0] = ...,
	*,
	factory: Callable[[], MutableMapping[K, V1]] = dict,
) -> (
	dict[K, V1]
	| MutableMapping[K, V1]
	| Callable[..., dict[K, V1] | MutableMapping[K, V1]]
):
	...
