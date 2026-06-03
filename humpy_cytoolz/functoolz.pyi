from collections.abc import Callable, Iterable, Mapping
from typing import Any, overload, override, Protocol, TypeVar
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

### Internal type stubs
_T = TypeVar("_T")
_Instance = TypeVar("_Instance")
type _Getter[Instance, T] = Callable[[Instance], T]
type _Setter[Instance, T] = Callable[[Instance, T], None]
type _Deleter[Instance] = Callable[[Instance], None]
type _InstancePropertyState[Instance, T] = tuple[
	_Getter[Instance, T] | None,
	_Setter[Instance, T] | None,
	_Deleter[Instance] | None,
	str | None,
	T | None,
]

class _JuxtCallable[**P, R](Protocol):
	funcs: tuple[Callable[P, Any], ...]

	def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R: ...

### Toolz

def identity[T](x: T) -> T:
	...

def apply[**P, T](func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
	...

def thread_first[T, R](
	val: T, *forms: Callable[[T], R] | tuple[Callable[..., R], Any]
) -> R:
	...

def thread_last[T, U](
	val: T, *forms: Callable[[T], U] | tuple[Callable[..., U]]
) -> U:
	...

class InstanceProperty[Instance, T](property):
	...
	def __init__(
		self,
		fget: _Getter[_Instance, _T] | None = None,
		fset: _Setter[_Instance, _T] | None = None,
		fdel: _Deleter[_Instance] | None = None,
		doc: str | None = None,
		classval: _T | None = None,
	) -> None: ...
	@overload
	def __get__(self, obj: None, type: type | None = ...) -> _T | None: ...
	@overload
	def __get__(self, obj: _Instance, type: type | None = ...) -> _T: ...
	@override
	def __get__(self, obj: _Instance | None, type: type | None = None) -> _T | None: ...
	@override
	def __reduce__(
		self,
	) -> tuple[type[InstanceProperty], _InstancePropertyState]:
		# TODO figure out how to type this correctly
		...

@overload
def instanceproperty[Instance, T](
	fget: _Getter[Instance, T],
	fset: _Setter[Instance, T] | None = ...,
	fdel: _Deleter[Instance] | None = ...,
	doc: str | None = ...,
	classval: T | None = ...,
) -> InstanceProperty[Instance, T]: ...
@overload
def instanceproperty[Instance, T](
	fget: None = None,
	fset: _Setter[Instance, T] | None = ...,
	fdel: _Deleter[Instance] | None = ...,
	doc: str | None = ...,
	classval: T | None = ...,
) -> Callable[[_Getter[Instance, T]], InstanceProperty[Instance, T]]: ...
def instanceproperty[Instance, T](
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

class curry[**P, T]:
	...
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
def memoize[T](
	func: Callable[..., T],
	cache: dict[Any, T] | None = None,
	key: Callable[
		[tuple[Any, ...], Mapping[str, Any]], Any
	]
	| None = None,
) -> Callable[..., T]:
	...

@overload
def compose[**P, T](fn_0: Callable[P, T]) -> Callable[P, T]: ...
@overload
def compose[**P, T0, T1](
	fn_0: Callable[[T0], T1], fn_1: Callable[P, T0]
) -> Callable[P, T1]: ...
@overload
def compose[**P, T0, T1, T2](
	fn_0: Callable[[T1], T2],
	fn_1: Callable[[T0], T1],
	fn_2: Callable[P, T0],
) -> Callable[P, T2]: ...
@overload
def compose[**P, T0, T1, T2, T3](
	fn_0: Callable[[T2], T3],
	fn_1: Callable[[T1], T2],
	fn_2: Callable[[T0], T1],
	fn_3: Callable[P, T0],
) -> Callable[P, T3]: ...
@overload
def compose[**P, T0, T1, T2, T3, T4](
	fn_0: Callable[[T3], T4],
	fn_1: Callable[[T2], T3],
	fn_2: Callable[[T1], T2],
	fn_3: Callable[[T0], T1],
	fn_4: Callable[P, T0],
) -> Callable[P, T4]: ...
@overload
def compose[**P, T0, T1, T2, T3, T4, T5](
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
def compose_left[**P, T](fn_0: Callable[P, T]) -> Callable[P, T]: ...
@overload
def compose_left[**P, T0, T1](
	fn_0: Callable[P, T0], fn_1: Callable[[T0], T1]
) -> Callable[P, T1]: ...
@overload
def compose_left[**P, T0, T1, T2](
	fn_0: Callable[P, T0],
	fn_1: Callable[[T0], T1],
	fn_2: Callable[[T1], T2],
) -> Callable[P, T2]: ...
@overload
def compose_left[**P, T0, T1, T2, T3](
	fn_0: Callable[P, T0],
	fn_1: Callable[[T0], T1],
	fn_2: Callable[[T1], T2],
	fn_3: Callable[[T2], T3],
) -> Callable[P, T3]: ...
@overload
def compose_left[**P, T0, T1, T2, T3, T4](
	fn_0: Callable[P, T0],
	fn_1: Callable[[T0], T1],
	fn_2: Callable[[T1], T2],
	fn_3: Callable[[T2], T3],
	fn_4: Callable[[T3], T4],
) -> Callable[P, T4]: ...
@overload
def compose_left[**P, T0, T1, T2, T3, T4, T5](
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
def pipe[T0, T1](
	data: T0,
	fn_0: Callable[[T0], T1],
) -> T1: ...
@overload
def pipe[T0, T1, T2](
	data: T0,
	fn_0: Callable[[T0], T1],
	fn_1: Callable[[T1], T2],
) -> T2: ...
@overload
def pipe[T0, T1, T2, T3](
	data: T0,
	fn_0: Callable[[T0], T1],
	fn_1: Callable[[T1], T2],
	fn_2: Callable[[T2], T3],
) -> T3: ...
@overload
def pipe[T0, T1, T2, T3, T4](
	data: T0,
	fn_0: Callable[[T0], T1],
	fn_1: Callable[[T1], T2],
	fn_2: Callable[[T2], T3],
	fn_3: Callable[[T3], T4],
) -> T4: ...
@overload
def pipe[T0, T1, T2, T3, T4, T5](
	data: T0,
	fn_0: Callable[[T0], T1],
	fn_1: Callable[[T1], T2],
	fn_2: Callable[[T2], T3],
	fn_3: Callable[[T3], T4],
	fn_4: Callable[[T4], T5],
) -> T5: ...
@overload
def pipe[T0, T1, T2, T3, T4, T5, T6](
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

class complement[**P]:
	...
	def __init__(self, func: Callable[P, Any]) -> None: ...
	def __call__(self, *args: P.args, **kwargs: P.kwargs) -> bool: ...

@overload
def juxt() -> _JuxtCallable[..., tuple[()]]: ...
@overload
def juxt[**P, T0](
	fn_0: Callable[P, T0],
) -> _JuxtCallable[P, tuple[T0]]: ...
@overload
def juxt[**P, T0, T1](
	fn_0: Callable[P, T0],
	fn_1: Callable[P, T1],
) -> _JuxtCallable[P, tuple[T0, T1]]: ...
@overload
def juxt[**P, T0, T1, T2](
	fn_0: Callable[P, T0],
	fn_1: Callable[P, T1],
	fn_2: Callable[P, T2],
) -> _JuxtCallable[P, tuple[T0, T1, T2]]: ...
@overload
def juxt[**P, T0, T1, T2, T3](
	fn_0: Callable[P, T0],
	fn_1: Callable[P, T1],
	fn_2: Callable[P, T2],
	fn_3: Callable[P, T3],
) -> _JuxtCallable[P, tuple[T0, T1, T2, T3]]: ...
@overload
def juxt[**P, T0, T1, T2, T3, T4](
	fn_0: Callable[P, T0],
	fn_1: Callable[P, T1],
	fn_2: Callable[P, T2],
	fn_3: Callable[P, T3],
	fn_4: Callable[P, T4],
) -> _JuxtCallable[P, tuple[T0, T1, T2, T3, T4]]: ...
@overload
def juxt[**P, T0, T1, T2, T3, T4, T5](
	fn_0: Callable[P, T0],
	fn_1: Callable[P, T1],
	fn_2: Callable[P, T2],
	fn_3: Callable[P, T3],
	fn_4: Callable[P, T4],
	fn_5: Callable[P, T5],
) -> _JuxtCallable[P, tuple[T0, T1, T2, T3, T4, T5]]: ...
@overload
def juxt[**P, T](
	funcs: Iterable[Callable[P, T]],
) -> _JuxtCallable[P, tuple[T, ...]]: ...
@overload
def juxt[**P, T](
	*funcs: Callable[P, T],
) -> _JuxtCallable[P, tuple[T, ...]]: ...
def juxt[**P, T](
	*funcs: Callable[P, T] | Iterable[Callable[P, T]],
) -> _JuxtCallable[P, tuple[T, ...]]:
	...

def do[T](func: Callable[[T], Any], x: T) -> T:
	...

@curry
def flip[T, U, R](func: Callable[[T, U], R], a: U, b: T) -> R:
	...

def _flip[T, U, R](func: Callable[[T, U], R], a: U, b: T) -> R: ...

def return_none[T](exc: T) -> None: ...

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

class excepts[T, **P]:
	...
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
