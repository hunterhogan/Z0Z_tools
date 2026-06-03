from collections.abc import Callable, Iterable
from typing import Any

__all__ = ("consume", "include_dirs", "no_default", "raises")

def raises(err: type[Exception], lamda: Callable[[], Any]) -> bool: ...

no_default: Any = "__no__default__"

def include_dirs() -> tuple[str, str]: ...
def consume(seq: Iterable[Any]) -> None: ...
