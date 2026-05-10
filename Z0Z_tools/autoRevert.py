"""Array axis manipulation utilities with automatic reversion.

This module provides context managers for temporarily manipulating array axes with automatic
restoration of the original configuration when exiting the context.

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
	"""Temporarily move an axis of an array to a target position with automatic reversion.

	Moves an axis of an array to a specified position, typically to the last axis for easier operation.
	Yields the modified array and automatically reverts the axis position when exiting the context.

	Parameters
	----------
	arrayTarget : ArrayType
		The input array to modify.
	axisSource : int
		The current position of the axis to move.
	axisOfOperation : int = -1
		The target position for the axis.

	Yields
	------
	arrayStandardized : ArrayType
		The array with the axis moved to the specified position.

	Example
	-------
	```python
	with moveToAxisOfOperation(arrayWaveforms, axes['time']):
		arrayWaveforms = arrayWaveforms[..., COUNTsamplesPadding : -COUNTsamplesPadding]
	```
	"""
	arrayStandardized: ArrayType = moveaxis(arrayTarget, axisSource, axisOfOperation)
	try:
		yield arrayStandardized
	finally:
		moveaxis(arrayStandardized, axisOfOperation, axisSource)
