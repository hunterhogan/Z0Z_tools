from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from functools import partial
from typing import Any, Concatenate, overload
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
def instanceproperty[Instance, T](fget: _Getter[Instance, T], fset: _Setter[Instance, T] | None=..., fdel: _Deleter[Instance] | None=..., doc: str | None=..., classval: T | None=...) -> InstanceProperty[Instance, T]:
    ...

@overload
def instanceproperty[Instance, T](fget: None=None, fset: _Setter[Instance, T] | None=..., fdel: _Deleter[Instance] | None=..., doc: str | None=..., classval: T | None=...) -> Callable[[_Getter[Instance, T]], InstanceProperty[Instance, T]]:
    ...

def instanceproperty[Instance, T](fget: _Getter[Instance, T] | None=None, fset: _Setter[Instance, T] | None=None, fdel: _Deleter[Instance] | None=None, doc: str | None=None, classval: T | None=None) -> InstanceProperty[Instance, T] | Callable[[_Getter[Instance, T]], InstanceProperty[Instance, T]]:
    ...

class InstanceProperty[Instance, T](property):

    def __init__(self, fget: _Getter[Instance, T] | None=None, fset: _Setter[Instance, T] | None=None, fdel: _Deleter[Instance] | None=None, doc: str | None=None, classval: T | None=None) -> None:
        ...

    @overload
    def __get__(self, obj: None, type: type | None=...) -> T | None:
        ...

    @overload
    def __get__(self, obj: Instance, type: type | None=...) -> T:
        ...

    def __get__(self, obj: Instance | None, type: type | None=None) -> T | None:
        ...

    def __reduce__(self) -> tuple[type[InstanceProperty[Any, Any]], InstancePropertyState[Callable[..., Any], Any]]:
        ...

class curry[**P, T]:

    @overload
    def __init__(self, func: curry[P, T] | partial[T], /, *args: Any, **kwargs: Any) -> None:
        ...

    @overload
    def __init__(self, func: Callable[P, T], /, *args: Any, **kwargs: Any) -> None:
        ...

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        ...

    @instanceproperty
    def func(self) -> Callable[P, T]:
        ...

    @instanceproperty
    def __signature__(self) -> inspect.Signature:
        ...

    @instanceproperty
    def args(self) -> tuple[Any, ...]:
        ...

    @instanceproperty
    def keywords(self) -> dict[str, Any]:
        ...

    @instanceproperty
    def func_name(self) -> str:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def __hash__(self) -> int:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __ne__(self, other: object) -> bool:
        ...

    @overload
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        ...

    @overload
    def __call__[First, **Remaining](self: curry[Concatenate[First, Remaining], T], first: First, /) -> curry[Remaining, T]:
        ...

    @overload
    def __call__[First, Second, **Remaining](self: curry[Concatenate[First, Second, Remaining], T], first: First, second: Second, /) -> curry[Remaining, T]:
        ...

    @overload
    def __call__(self, *args: Any, **kwargs: Any) -> curry[P, T]:
        ...

    def __call__(self, *args: Any, **kwargs: Any) -> T | curry[P, T]:
        ...

    def _should_curry(self, args: tuple[Any, ...], kwargs: dict[str, Any], exc: TypeError | None=None) -> bool:
        ...

    def bind(self, *args: Any, **kwargs: Any) -> curry[P, T]:
        ...

    def call(self, *args: Any, **kwargs: Any) -> T:
        ...

    def __get__(self, instance: object | None, owner: type | None) -> curry[P, T]:
        ...

    def __reduce__(self) -> tuple[Callable[..., T], CurryState]:
        ...

def _restore_curry[**P, T](cls: type[curry[P, T]], func: str | Callable[P, T], args: tuple[Any, ...], kwargs: Mapping[str, Any] | None, userdict: Iterable[tuple[str, Any]], is_decorated: bool | None) -> curry[P, T] | Callable[P, T]:
    ...

@curry
def memoize[T](func: Callable[..., T], cache: dict[Any, T] | None=None, key: Callable[[tuple[Any, ...], Mapping[str, Any]], Any] | None=None) -> Callable[..., T]:
    ...

class Compose:
    first: Callable[..., Any]
    funcs: tuple[Callable[..., Any], ...]

    def __init__(self, funcs: Iterable[Callable[..., Any]]) -> None:
        ...

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        ...

    def __getstate__(self) -> tuple[Callable[..., Any], tuple[Callable[..., Any], ...]]:
        ...

    def __setstate__(self, state: tuple[Callable[..., Any], tuple[Callable[..., Any], ...]]) -> None:
        ...

    @instanceproperty(classval=__doc__)
    def __doc__(self) -> str:
        ...

    @property
    def __name__(self) -> str:
        ...

    def __repr__(self) -> str:
        ...

    def __eq__(self, other: object) -> bool:
        ...

    def __ne__(self, other: object) -> bool:
        ...

    def __hash__(self) -> int:
        ...

    def __get__(self, obj: object | None, objtype: type | None=None) -> Compose:
        ...

    @instanceproperty
    def __signature__(self) -> inspect.Signature:
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
    funcs: tuple[Callable[..., Any], ...]

    def __init__(self, *funcs: Callable[..., Any] | Iterable[Callable[..., Any]]) -> None:
        ...

    def __call__(self, *args: Any, **kwargs: Any) -> tuple[Any, ...]:
        ...

    def __getstate__(self) -> tuple[Callable[..., Any], ...]:
        ...

    def __setstate__(self, state: tuple[Callable[..., Any], ...]) -> None:
        ...

def do[T](func: Callable[[T], Any], x: T) -> T:
    ...

@curry
def flip[T, U, R](func: Callable[[T, U], R], a: U, b: T) -> R:
    ...

def return_none(exc: Exception) -> None:
    ...

class excepts[**P, T]:

    def __init__(self, exc: type[Exception] | tuple[type[Exception], ...], func: Callable[P, T], handler: Callable[[Exception], T]=return_none) -> None:
        ...

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        ...

    @instanceproperty(classval=__doc__)
    def __doc__(self) -> str:
        ...

    @property
    def __name__(self) -> str:
        ...

def _check_sigspec[T](sigspec: inspect.Signature | None, func: Callable[..., Any], builtin_func: Callable[..., T], *builtin_args: Any) -> tuple[inspect.Signature | None, T | bool | None]:
    ...

def num_required_args(func: Callable[..., Any], sigspec: inspect.Signature | None=None) -> int | None:
    ...

def has_varargs(func: Callable[..., Any], sigspec: inspect.Signature | None=None) -> bool | None:
    ...

def has_keywords(func: Callable[..., Any], sigspec: inspect.Signature | None=None) -> bool | None:
    ...

def is_valid_args(func: Callable[..., Any], args: tuple[Any, ...], kwargs: Mapping[str, Any], sigspec: inspect.Signature | None=None) -> bool | None:
    ...

def is_partial_args(func: Callable[..., Any], args: tuple[Any, ...], kwargs: Mapping[str, Any], sigspec: inspect.Signature | None=None) -> bool | None:
    ...

def is_arity(n: int, func: Callable[..., Any], sigspec: inspect.Signature | None=None) -> bool | None:
    ...
