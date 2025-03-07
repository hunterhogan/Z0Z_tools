from collections.abc import Generator
from contextlib import contextmanager
from numpy import moveaxis
from numpy.typing import NDArray
from typing import Any, cast, TypeVar

ArrayType = TypeVar('ArrayType', bound=NDArray[Any])

@contextmanager
def moveToAxisOfOperation(arrayTarget: ArrayType, axisSource: int, axisOfOperation: int = -1) -> Generator[ArrayType, None, None]:
	arrayStandardized = cast(ArrayType, moveaxis(arrayTarget, axisSource, axisOfOperation))
	try:
		yield arrayStandardized
	finally:
		moveaxis(arrayStandardized, axisOfOperation, axisSource)
