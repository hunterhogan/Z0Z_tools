from Z0Z_tools import defineConcurrencyLimit as defineConcurrencyLimit, intInnit as intInnit, oopsieKwargsie as oopsieKwargsie
from collections.abc import Callable as Callable, Iterable
from typing import Any

def PytestFor_defineConcurrencyLimit(callableToTest: Callable[[bool | float | int | None], int] = ..., cpuCount: int = 8) -> list[tuple[str, Callable[[], None]]]: ...
def PytestFor_intInnit(callableToTest: Callable[[Iterable[int], str | None, type[Any] | None], list[int]] = ...) -> list[tuple[str, Callable[[], None]]]: ...
def PytestFor_oopsieKwargsie(callableToTest: Callable[[str], bool | None | str] = ...) -> list[tuple[str, Callable[[], None]]]: ...
