from collections.abc import Generator
from contextlib import contextmanager
from numpy import moveaxis
from typing import cast
from Z0Z_tools import ArrayType

@contextmanager
def moveToAxisOfOperation(arrayTarget: ArrayType, axisSource: int, axisOfOperation: int = -1) -> Generator[ArrayType, None, None]:
	"""
	Temporarily moves an axis of an array to a target position, typically to the last axis for easier operation.
	Yields the modified array and automatically reverts the axis position when exiting the context.

	Parameters
	----------
	arrayTarget : ArrayType
		The input array to modify.
	axisSource : int
		The current position of the axis to move.
	axisOfOperation : int, optional
		The target position for the axis. Defaults to -1 (last axis).

	Yields
	------
	ArrayType
		The array with the axis moved to the specified position.

	Notes
	-----
	This is a context manager that temporarily modifies array axis positions.
	The original axis positions are restored when exiting the context.
	"""
	arrayStandardized = cast(ArrayType, moveaxis(arrayTarget, axisSource, axisOfOperation))
	try:
		yield arrayStandardized
	finally:
		moveaxis(arrayStandardized, axisOfOperation, axisSource)
