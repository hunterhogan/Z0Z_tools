
from collections.abc import Callable, Iterable, Mapping
from typing import Any, overload
import inspect

type CurryState = tuple[Any, ...]
type _Getter[_Instance, _T] = Callable[[_Instance], _T]
type _Setter[_Instance, _T] = Callable[[_Instance, _T], None]
type _Deleter[_Instance] = Callable[[_Instance], None]
type InstancePropertyState[_Instance, _T] = tuple[_Getter[_Instance, _T] | None, _Setter[_Instance, _T] | None, _Deleter[_Instance] | None, str | None, _T | None]
PYPY: bool
__all__: tuple[str, ...] = ('apply', 'complement', 'compose', 'compose_left', 'curry', 'do', 'excepts', 'flip', 'identity', 'juxt', 'memoize', 'pipe', 'thread_first', 'thread_last')

def identity[T](x: T) -> T:
	...

@overload
def apply[**P, T](func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
	...

@overload
def apply(*func_and_args: Any, **kwargs: Any) -> Any:
	...

def apply(*func_and_args: Any, **kwargs: Any) -> Any:
	...

def thread_first[T, R](val: T, *forms: Callable[[T], R] | tuple[Callable[..., R], Any]) -> R:
	...

def thread_last[T, U](val: T, *forms: Callable[[T], U] | tuple[Callable[..., U], ...]) -> U:
	...

@overload
def instanceproperty[Instance, T](fget: _Getter[Instance, T], fset: _Setter[Instance, T] | None = ..., fdel: _Deleter[Instance] | None = ..., doc: str | None = ..., classval: T | None = ...) -> InstanceProperty[Instance, T]:
	...

@overload
def instanceproperty[Instance, T](fget: None = None, fset: _Setter[Instance, T] | None = ..., fdel: _Deleter[Instance] | None = ..., doc: str | None = ..., classval: T | None = ...) -> Callable[[_Getter[Instance, T]], InstanceProperty[Instance, T]]:
	...

def instanceproperty[Instance, T](fget: _Getter[Instance, T] | None = None, fset: _Setter[Instance, T] | None = None, fdel: _Deleter[Instance] | None = None, doc: str | None = None, classval: T | None = None) -> InstanceProperty[Instance, T] | Callable[[_Getter[Instance, T]], InstanceProperty[Instance, T]]:
	...

class InstanceProperty[Instance, T](property):
	...

class curry[**P, T]:
	...

def _restore_curry[**P, T](cls: type[curry[P, T]], func: str | Callable[P, T], args: tuple[Any, ...], kwargs: Mapping[str, Any] | None, userdict: Iterable[tuple[str, Any]], is_decorated: bool | None) -> curry[P, T] | Callable[P, T]:
	...

@curry
def memoize[T](func: Callable[..., T], cache: dict[Any, T] | None = None, key: Callable[[tuple[Any, ...], Mapping[str, Any]], Any] | None = None) -> Callable[..., T]:
	...

class Compose:
	...

@overload
def compose[**P, T](fn_0: Callable[P, T]) -> Callable[P, T]:
	...

@overload
def compose[**P, T0, T1](fn_0: Callable[[T0], T1], fn_1: Callable[P, T0]) -> Callable[P, T1]:
	...

@overload
def compose[**P, T0, T1, T2](fn_0: Callable[[T1], T2], fn_1: Callable[[T0], T1], fn_2: Callable[P, T0]) -> Callable[P, T2]:
	...

@overload
def compose[**P, T0, T1, T2, T3](fn_0: Callable[[T2], T3], fn_1: Callable[[T1], T2], fn_2: Callable[[T0], T1], fn_3: Callable[P, T0]) -> Callable[P, T3]:
	...

@overload
def compose[**P, T0, T1, T2, T3, T4](fn_0: Callable[[T3], T4], fn_1: Callable[[T2], T3], fn_2: Callable[[T1], T2], fn_3: Callable[[T0], T1], fn_4: Callable[P, T0]) -> Callable[P, T4]:
	...

@overload
def compose[**P, T0, T1, T2, T3, T4, T5](fn_0: Callable[[T4], T5], fn_1: Callable[[T3], T4], fn_2: Callable[[T2], T3], fn_3: Callable[[T1], T2], fn_4: Callable[[T0], T1], fn_5: Callable[P, T0]) -> Callable[P, T5]:
	...

@overload
def compose(*funcs: Callable[..., Any]) -> Callable[..., Any]:
	...

def compose(*funcs: Callable[..., Any]) -> Callable[..., Any]:
	...

@overload
def compose_left[**P, T](fn_0: Callable[P, T]) -> Callable[P, T]:
	...

@overload
def compose_left[**P, T0, T1](fn_0: Callable[P, T0], fn_1: Callable[[T0], T1]) -> Callable[P, T1]:
	...

@overload
def compose_left[**P, T0, T1, T2](fn_0: Callable[P, T0], fn_1: Callable[[T0], T1], fn_2: Callable[[T1], T2]) -> Callable[P, T2]:
	...

@overload
def compose_left[**P, T0, T1, T2, T3](fn_0: Callable[P, T0], fn_1: Callable[[T0], T1], fn_2: Callable[[T1], T2], fn_3: Callable[[T2], T3]) -> Callable[P, T3]:
	...

@overload
def compose_left[**P, T0, T1, T2, T3, T4](fn_0: Callable[P, T0], fn_1: Callable[[T0], T1], fn_2: Callable[[T1], T2], fn_3: Callable[[T2], T3], fn_4: Callable[[T3], T4]) -> Callable[P, T4]:
	...

@overload
def compose_left[**P, T0, T1, T2, T3, T4, T5](fn_0: Callable[P, T0], fn_1: Callable[[T0], T1], fn_2: Callable[[T1], T2], fn_3: Callable[[T2], T3], fn_4: Callable[[T3], T4], fn_5: Callable[[T4], T5]) -> Callable[P, T5]:
	...

@overload
def compose_left(*funcs: Callable[..., Any]) -> Callable[..., Any]:
	...

def compose_left(*funcs: Callable[..., Any]) -> Callable[..., Any]:
	...

@overload
def pipe[T0, T1](data: T0, fn_0: Callable[[T0], T1]) -> T1:
	...

@overload
def pipe[T0, T1, T2](data: T0, fn_0: Callable[[T0], T1], fn_1: Callable[[T1], T2]) -> T2:
	...

@overload
def pipe[T0, T1, T2, T3](data: T0, fn_0: Callable[[T0], T1], fn_1: Callable[[T1], T2], fn_2: Callable[[T2], T3]) -> T3:
	...

@overload
def pipe[T0, T1, T2, T3, T4](data: T0, fn_0: Callable[[T0], T1], fn_1: Callable[[T1], T2], fn_2: Callable[[T2], T3], fn_3: Callable[[T3], T4]) -> T4:
	...

@overload
def pipe[T0, T1, T2, T3, T4, T5](data: T0, fn_0: Callable[[T0], T1], fn_1: Callable[[T1], T2], fn_2: Callable[[T2], T3], fn_3: Callable[[T3], T4], fn_4: Callable[[T4], T5]) -> T5:
	...

@overload
def pipe[T0, T1, T2, T3, T4, T5, T6](data: T0, fn_0: Callable[[T0], T1], fn_1: Callable[[T1], T2], fn_2: Callable[[T2], T3], fn_3: Callable[[T3], T4], fn_4: Callable[[T4], T5], fn_5: Callable[[T5], T6]) -> T6:
	...

@overload
def pipe(data: Any, *funcs: Callable[..., Any]) -> Any:
	...

def pipe(data: Any, *funcs: Callable[..., Any]) -> Any:
	...

def complement[**P](func: Callable[P, bool]) -> Callable[P, bool]:
	...

class juxt[**P, T]:
	...

def do[T](func: Callable[[T], Any], x: T) -> T:
	...

@curry
def flip[T, U, R](func: Callable[[T, U], R], a: U, b: T) -> R:
	...

def return_none(exc: Exception) -> None:
	...

class excepts[**P, T]:
	...

def _check_sigspec[T](sigspec: inspect.Signature | None, func: Callable[..., Any], builtin_func: Callable[..., T], *builtin_args: Any) -> tuple[inspect.Signature | None, T | bool | None]:
	...

def num_required_args(func: Callable[..., Any], sigspec: inspect.Signature | None = None) -> int | None:
	...

def has_varargs(func: Callable[..., Any], sigspec: inspect.Signature | None = None) -> bool | None:
	...

def has_keywords(func: Callable[..., Any], sigspec: inspect.Signature | None = None) -> bool | None:
	...

def is_valid_args(func: Callable[..., Any], args: tuple[Any, ...], kwargs: Mapping[str, Any], sigspec: inspect.Signature | None = None) -> bool | None:
	...

def is_partial_args(func: Callable[..., Any], args: tuple[Any, ...], kwargs: Mapping[str, Any], sigspec: inspect.Signature | None = None) -> bool | None:
	...

def is_arity(n: int, func: Callable[..., Any], sigspec: inspect.Signature | None = None) -> bool | None:
	...
