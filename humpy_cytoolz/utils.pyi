
from collections.abc import Callable
from typing import Literal

no_default: Literal['__no__default__']

def raises(err: type[Exception], lamda: Callable[[], None]) -> bool:
    ...
