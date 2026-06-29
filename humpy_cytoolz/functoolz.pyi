from humpy_cytoolz._theTypes import Instance, T, R, P, U, Instance_, T0, T1, T2, T3, T4, T5, T6, T_
from typing_extensions import override

from collections.abc import Callable, Iterable, Mapping
from typing import Any, Generic, overload, Protocol, TypeAlias
import functools
import inspect

__all__ = (
	"apply",
	"complement",
	"compose",
	"compose_left",
	"curry",
	"do",
	"excepts",
	"flip",
	"identity",
	"juxt",
	"memoize",
	"pipe",
	"thread_first",
	"thread_last",
)
PYPY = bool


_Getter: TypeAlias = Callable[[Instance, T], T]
_Setter: TypeAlias = Callable[[Instance, T], None]
_Deleter: TypeAlias = Callable[[Instance], None]
_InstancePropertyState: TypeAlias = tuple[
	Callable[[Instance, T], T] | None,
	Callable[[Instance, T], None] | None,
	Callable[[Instance], None] | None,
	str | None,
	T | None,
]

class _JuxtCallable(Protocol, Generic[P, R]):
	funcs: tuple[Callable[P, Any], ...]

	def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R: ...

# Toolz

def identity(x: T) -> T:
	...

def apply(func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
	...

def thread_first(
	val: T, *forms: Callable[[T], R] | tuple[Callable[..., R], Any]
) -> R:
	...

def thread_last(
	val: T, *forms: Callable[[T], U] | tuple[Callable[..., U]]
) -> U:
	...

class InstanceProperty(property, Generic[Instance, T]):
	def __init__(
		self,
		fget: _Getter[Instance_, T_] | None = None,
		fset: _Setter[Instance_, T_] | None = None,
		fdel: _Deleter[Instance_] | None = None,
		doc: str | None = None,
		classval: T_ | None = None,
	) -> None: ...
	@overload
	def __get__(self, obj: None, type: type | None = ...) -> T_ | None: ...
	@overload
	def __get__(self, obj: Instance_, type: type | None = ...) -> T_: ...
	@override
	def __get__(self, obj: Instance_ | None, type: type | None = None) -> T_ | None: ...
	@override
	def __reduce__(
		self,
	) -> tuple[type[InstanceProperty], _InstancePropertyState]:
		# TODO figure out how to type this correctly
		...

@overload
def instanceproperty(
	fget: _Getter[Instance, T],
	fset: _Setter[Instance, T] | None = ...,
	fdel: _Deleter[Instance] | None = ...,
	doc: str | None = ...,
	classval: T | None = ...,
) -> InstanceProperty[Instance, T]: ...
@overload
def instanceproperty(
	fget: None = None,
	fset: _Setter[Instance, T] | None = ...,
	fdel: _Deleter[Instance] | None = ...,
	doc: str | None = ...,
	classval: T | None = ...,
) -> Callable[[_Getter[Instance, T]], InstanceProperty[Instance, T]]: ...
def instanceproperty(
	fget: _Getter[Instance, T] | None = None,
	fset: _Setter[Instance, T] | None = None,
	fdel: _Deleter[Instance] | None = None,
	doc: str | None = None,
	classval: T | None = None,
) -> (
	InstanceProperty[Instance, T]
	| Callable[[_Getter[Instance, T]], InstanceProperty[Instance, T]]
):
	...

_CurryState = tuple

class curry(Generic[P, T]):
	def __init__(
		self,
		func: curry[P, T] | functools.partial[T] | Callable[P, T],
		/,  # Must be positional-only
		*args: Any,
		**kwargs: Any,
	) -> None: ...
	@instanceproperty
	def func(self) -> Callable[P, T]: ...
	@instanceproperty
	def __signature__(self) -> inspect.Signature: ...
	@instanceproperty
	def args(self) -> tuple[Any, ...]: ...
	@instanceproperty
	def keywords(self) -> dict[str, Any]: ...
	@instanceproperty
	def func_name(self) -> str: ...
	@override
	def __hash__(self) -> int: ...
	@override
	def __eq__(self, other: object) -> bool: ...
	@override
	def __ne__(self, other: object) -> bool: ...
	@overload
	def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T: ...
	@overload
	def __call__(
		self, *args: Any, **kwargs: Any
	) -> functools.partial[T]: ...
	def bind(self, *args: Any, **kwargs: Any) -> curry[P, T]: ...
	def call(self, *args: Any, **kwargs: Any) -> T: ...
	def __get__(self, instance: object, owner: type) -> curry[P, T]: ...
	@override
	def __reduce__(
		self,
	) -> tuple[Callable[..., T], _CurryState]: ...

@curry
def memoize(
	func: Callable[..., T],
	cache: dict[Any, T] | None = None,
	key: Callable[
		[tuple[Any, ...], Mapping[str, Any]], Any
	]
	| None = None,
) -> Callable[..., T]:
	...

@overload
def compose(fn_0: Callable[P, T]) -> Callable[P, T]: ...
@overload
def compose(
	fn_0: Callable[[T0], T1], fn_1: Callable[P, T0]
) -> Callable[P, T1]: ...
@overload
def compose(
	fn_0: Callable[[T1], T2],
	fn_1: Callable[[T0], T1],
	fn_2: Callable[P, T0],
) -> Callable[P, T2]: ...
@overload
def compose(
	fn_0: Callable[[T2], T3],
	fn_1: Callable[[T1], T2],
	fn_2: Callable[[T0], T1],
	fn_3: Callable[P, T0],
) -> Callable[P, T3]: ...
@overload
def compose(
	fn_0: Callable[[T3], T4],
	fn_1: Callable[[T2], T3],
	fn_2: Callable[[T1], T2],
	fn_3: Callable[[T0], T1],
	fn_4: Callable[P, T0],
) -> Callable[P, T4]: ...
@overload
def compose(
	fn_0: Callable[[T4], T5],
	fn_1: Callable[[T3], T4],
	fn_2: Callable[[T2], T3],
	fn_3: Callable[[T1], T2],
	fn_4: Callable[[T0], T1],
	fn_5: Callable[P, T0],
) -> Callable[P, T5]: ...
@overload
def compose(
	*funcs: Callable[..., Any],
) -> Callable[..., Any]: ...
def compose(
	*funcs: Callable[..., Any],
) -> Callable[..., Any]:
	...

@overload
def compose_left(fn_0: Callable[P, T]) -> Callable[P, T]: ...
@overload
def compose_left(
	fn_0: Callable[P, T0], fn_1: Callable[[T0], T1]
) -> Callable[P, T1]: ...
@overload
def compose_left(
	fn_0: Callable[P, T0],
	fn_1: Callable[[T0], T1],
	fn_2: Callable[[T1], T2],
) -> Callable[P, T2]: ...
@overload
def compose_left(
	fn_0: Callable[P, T0],
	fn_1: Callable[[T0], T1],
	fn_2: Callable[[T1], T2],
	fn_3: Callable[[T2], T3],
) -> Callable[P, T3]: ...
@overload
def compose_left(
	fn_0: Callable[P, T0],
	fn_1: Callable[[T0], T1],
	fn_2: Callable[[T1], T2],
	fn_3: Callable[[T2], T3],
	fn_4: Callable[[T3], T4],
) -> Callable[P, T4]: ...
@overload
def compose_left(
	fn_0: Callable[P, T0],
	fn_1: Callable[[T0], T1],
	fn_2: Callable[[T1], T2],
	fn_3: Callable[[T2], T3],
	fn_4: Callable[[T3], T4],
	fn_5: Callable[[T4], T5],
) -> Callable[P, T5]: ...
@overload
def compose_left(
	*funcs: Callable[..., Any],
) -> Callable[..., Any]: ...
def compose_left(
	*funcs: Callable[..., Any],
) -> Callable[..., Any]:
	...

@overload
def pipe(
	data: T0,
	fn_0: Callable[[T0], T1],
) -> T1: ...
@overload
def pipe(
	data: T0,
	fn_0: Callable[[T0], T1],
	fn_1: Callable[[T1], T2],
) -> T2: ...
@overload
def pipe(
	data: T0,
	fn_0: Callable[[T0], T1],
	fn_1: Callable[[T1], T2],
	fn_2: Callable[[T2], T3],
) -> T3: ...
@overload
def pipe(
	data: T0,
	fn_0: Callable[[T0], T1],
	fn_1: Callable[[T1], T2],
	fn_2: Callable[[T2], T3],
	fn_3: Callable[[T3], T4],
) -> T4: ...
@overload
def pipe(
	data: T0,
	fn_0: Callable[[T0], T1],
	fn_1: Callable[[T1], T2],
	fn_2: Callable[[T2], T3],
	fn_3: Callable[[T3], T4],
	fn_4: Callable[[T4], T5],
) -> T5: ...
@overload
def pipe(
	data: T0,
	fn_0: Callable[[T0], T1],
	fn_1: Callable[[T1], T2],
	fn_2: Callable[[T2], T3],
	fn_3: Callable[[T3], T4],
	fn_4: Callable[[T4], T5],
	fn_5: Callable[[T5], T6],
) -> T6: ...
@overload
def pipe(data: Any, *funcs: Callable[..., Any]) -> Any: ...
def pipe(data: Any, *funcs: Callable[..., Any]) -> Any:
	...

class complement(Generic[P]):
	def __init__(self, func: Callable[P, Any]) -> None: ...
	def __call__(self, *args: P.args, **kwargs: P.kwargs) -> bool: ...

@overload
def juxt() -> _JuxtCallable[..., tuple[()]]: ...
@overload
def juxt(
	fn_0: Callable[P, T0],
) -> _JuxtCallable[P, tuple[T0]]: ...
@overload
def juxt(
	fn_0: Callable[P, T0],
	fn_1: Callable[P, T1],
) -> _JuxtCallable[P, tuple[T0, T1]]: ...
@overload
def juxt(
	fn_0: Callable[P, T0],
	fn_1: Callable[P, T1],
	fn_2: Callable[P, T2],
) -> _JuxtCallable[P, tuple[T0, T1, T2]]: ...
@overload
def juxt(
	fn_0: Callable[P, T0],
	fn_1: Callable[P, T1],
	fn_2: Callable[P, T2],
	fn_3: Callable[P, T3],
) -> _JuxtCallable[P, tuple[T0, T1, T2, T3]]: ...
@overload
def juxt(
	fn_0: Callable[P, T0],
	fn_1: Callable[P, T1],
	fn_2: Callable[P, T2],
	fn_3: Callable[P, T3],
	fn_4: Callable[P, T4],
) -> _JuxtCallable[P, tuple[T0, T1, T2, T3, T4]]: ...
@overload
def juxt(
	fn_0: Callable[P, T0],
	fn_1: Callable[P, T1],
	fn_2: Callable[P, T2],
	fn_3: Callable[P, T3],
	fn_4: Callable[P, T4],
	fn_5: Callable[P, T5],
) -> _JuxtCallable[P, tuple[T0, T1, T2, T3, T4, T5]]: ...
@overload
def juxt(
	funcs: Iterable[Callable[P, T]],
) -> _JuxtCallable[P, tuple[T, ...]]: ...
@overload
def juxt(
	*funcs: Callable[P, T],
) -> _JuxtCallable[P, tuple[T, ...]]: ...
def juxt(
	*funcs: Callable[P, T] | Iterable[Callable[P, T]],
) -> _JuxtCallable[P, tuple[T, ...]]:
	...

def do(func: Callable[[T], Any], x: T) -> T:
	...

@curry
def flip(func: Callable[[T, U], R], a: U, b: T) -> R:
	...

def _flip(func: Callable[[T, U], R], a: U, b: T) -> R: ...

def return_none(exc: T) -> None: ...

class Compose:
	first: Callable[..., Any]
	funcs: tuple[Callable[..., Any], ...]
	def __init__(self, *funcs: Callable[..., Any]) -> None: ...
	def __call__(self, *args: Any, **kwargs: Any) -> Any: ...
	@property
	def __wrapped__(self) -> Callable[..., Any]: ...
	@property
	def __signature__(self) -> inspect.Signature: ...
	@property
	def __name__(self) -> str: ...

class excepts(Generic[T, P]):
	def __init__(
		self,
		exc: type[Exception] | tuple[type[Exception], ...],
		func: Callable[P, T],
		handler: Callable[[Exception], T | None] = ...,
	) -> None: ...
	@property
	def exc(self) -> type[Exception] | tuple[type[Exception], ...]: ...
	@property
	def func(self) -> Callable[P, T]: ...
	@property
	def handler(self) -> Callable[[Exception], T | None]: ...
	def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T | None: ...
	@property
	def __name__(self) -> str: ...
