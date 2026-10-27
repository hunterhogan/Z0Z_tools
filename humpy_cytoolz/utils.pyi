from collections.abc import Callable
from more_itertools import consume as consume
from typing import Literal

no_default: Literal['__no__default__']

def raises[Result](err: type[BaseException] | tuple[type[BaseException], ...], lamda: Callable[[], Result]) -> bool:
    ...

def include_dirs() -> tuple[str, str]: ...
