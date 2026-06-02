"""Temporarily reposition array axes and restore the original axis order on context exit.

Contents
--------
Functions
	moveToAxisOfOperation
		Move an array axis to an operation position, then automatically restore the original axis order on exit.

"""
from __future__ import annotations

from contextlib import contextmanager
from numpy import moveaxis
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from collections.abc import Generator
	from Z0Z_tools import ArrayType

@contextmanager
def moveToAxisOfOperation(arrayTarget: ArrayType, axisSource: int, axisOfOperation: int = -1) -> Generator[ArrayType, None, None]:
	"""Move an array axis to an operation position, then automatically restore the original axis order on exit.

	You can use `moveToAxisOfOperation` as a context manager to temporarily rearrange the axes of
	`arrayTarget`. The context yields `arrayStandardized`, a `numpy.moveaxis` [1] view of `arrayTarget`
	with `axisSource` moved to `axisOfOperation`. Because `arrayStandardized` shares memory with
	`arrayTarget`, modifications to `arrayStandardized` inside the context are reflected in `arrayTarget`.
	When the context exits, `arrayTarget` retains its original axis order.

	Parameters
	----------
	arrayTarget : ArrayType
		The array whose axis to move.
	axisSource : int
		The source axis position to move. Negative values count from the last axis.
	axisOfOperation : int = -1
		The destination axis position for `axisSource`. Negative values count from the last axis.

	Yields
	------
	arrayStandardized : ArrayType
		A view of `arrayTarget` with `axisSource` at position `axisOfOperation`.

	Examples
	--------
	Move axis 0 to the last position and modify values inside the context:

		```python
		import numpy
		from Z0Z_tools import moveToAxisOfOperation

		arrayAxisOperation = numpy.arange(24).reshape(2, 3, 4)
		with moveToAxisOfOperation(arrayAxisOperation, axisSource=0, axisOfOperation=-1) as arrayStandardized:
			arrayStandardized += 10
		```

	References
	----------
	[1] numpy.moveaxis
		https://numpy.org/doc/stable/reference/generated/numpy.moveaxis.html

	"""
	arrayStandardized: ArrayType = moveaxis(arrayTarget, axisSource, axisOfOperation)
	try:
		yield arrayStandardized
	finally:
		moveaxis(arrayStandardized, axisOfOperation, axisSource)
