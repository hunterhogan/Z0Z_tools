from collections.abc import Callable, Iterable, Mapping
from typing import Any, Literal, overload, override, TypeVar
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
type _Getter[_Instance, _T] = Callable[[_Instance], _T]
type _Setter[_Instance, _T] = Callable[[_Instance, _T], None]
type _Deleter[_Instance] = Callable[[_Instance], None]
type _InstancePropertyState[_Instance, _T] = tuple[
	_Getter[_Instance, _T] | None,
	_Setter[_Instance, _T] | None,
	_Deleter[_Instance] | None,
	str | None,
	_T | None,
]

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
def instanceproperty(
	fget: _Getter[_Instance, _T],
	fset: _Setter[_Instance, _T] | None = ...,
	fdel: _Deleter[_Instance] | None = ...,
	doc: str | None = ...,
	classval: _T | None = ...,
) -> InstanceProperty[_Instance, _T]: ...
@overload
def instanceproperty(
	fget: Literal[None] | None = None,
	fset: _Setter[_Instance, _T] | None = ...,
	fdel: _Deleter[_Instance] | None = ...,
	doc: str | None = ...,
	classval: _T | None = ...,
) -> Callable[[_Getter[_Instance, _T]], InstanceProperty[_Instance, _T]]: ...
def instanceproperty(
	fget: _Getter[_Instance, _T] | None = None,
	fset: _Setter[_Instance, _T] | None = None,
	fdel: _Deleter[_Instance] | None = None,
	doc: str | None = None,
	classval: _T | None = None,
) -> (
	InstanceProperty[_Instance, _T]
	| Callable[[_Getter[_Instance, _T]], InstanceProperty[_Instance, _T]]
):
	...

_CurryState = tuple

class curry[**P, T]:
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

def complement[**P](func: Callable[P, bool]) -> Callable[P, bool]:
	...

@overload
def juxt() -> Callable[..., tuple[()]]: ...
@overload
def juxt[**P, T0](
	fn_0: Callable[P, T0],
) -> Callable[P, tuple[T0]]: ...
@overload
def juxt[**P, T0, T1](
	fn_0: Callable[P, T0],
	fn_1: Callable[P, T1],
) -> Callable[P, tuple[T0, T1]]: ...
@overload
def juxt[**P, T0, T1, T2](
	fn_0: Callable[P, T0],
	fn_1: Callable[P, T1],
	fn_2: Callable[P, T2],
) -> Callable[P, tuple[T0, T1, T2]]: ...
@overload
def juxt[**P, T0, T1, T2, T3](
	fn_0: Callable[P, T0],
	fn_1: Callable[P, T1],
	fn_2: Callable[P, T2],
	fn_3: Callable[P, T3],
) -> Callable[P, tuple[T0, T1, T2, T3]]: ...
@overload
def juxt[**P, T0, T1, T2, T3, T4](
	fn_0: Callable[P, T0],
	fn_1: Callable[P, T1],
	fn_2: Callable[P, T2],
	fn_3: Callable[P, T3],
	fn_4: Callable[P, T4],
) -> Callable[P, tuple[T0, T1, T2, T3, T4]]: ...
@overload
def juxt[**P, T0, T1, T2, T3, T4, T5](
	fn_0: Callable[P, T0],
	fn_1: Callable[P, T1],
	fn_2: Callable[P, T2],
	fn_3: Callable[P, T3],
	fn_4: Callable[P, T4],
	fn_5: Callable[P, T5],
) -> Callable[P, tuple[T0, T1, T2, T3, T4, T5]]: ...
@overload
def juxt[**P, T](
	funcs: Iterable[Callable[P, T]],
) -> Callable[P, tuple[T, ...]]: ...
@overload
def juxt[**P, T](
	*funcs: Callable[P, T],
) -> Callable[P, tuple[T, ...]]: ...
def juxt[**P, T](
	*funcs: Callable[P, T] | Iterable[Callable[P, T]],
) -> Callable[P, tuple[T, ...]]:
	...

def do[T](func: Callable[[T], Any], x: T) -> T:
	...

@curry
def flip[T, U, R](func: Callable[[T, U], R], a: U, b: T) -> R:
	...

class excepts[T, **P]:
	def __init__(
		self,
		exc: type[Exception] | tuple[type[Exception], ...],
		func: Callable[P, T],
		handler: Callable[[Exception], T] | None = None,
	) -> None: ...
	def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T: ...
	@property
	def __name__(self) -> str: ...


def num_required_args(func: Callable[..., Any], sigspec: inspect.Signature | None = None) -> int | None:
	...

def has_varargs(func: Callable[..., Any], sigspec: inspect.Signature | None = None) -> bool | None:
    ...

def has_keywords(func: Callable[..., Any], sigspec: inspect.Signature | None = None) -> bool | None:
    ...

def is_partial_args(func: Callable[..., Any], args, kwargs, sigspec: inspect.Signature | None = None) -> bool | None:
    ...

def is_arity(n: int, func: Callable[..., Any], sigspec: inspect.Signature | None = None) -> bool | None:
	...
