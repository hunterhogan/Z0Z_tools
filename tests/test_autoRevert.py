from __future__ import annotations

from tests.conftest import uniformTestFailureMessage
from typing import TYPE_CHECKING
from Z0Z_tools import moveToAxisOfOperation
import numpy
import pytest

if TYPE_CHECKING:
	from numpy.typing import NDArray

@pytest.mark.parametrize("axisSource, axisOfOperation", [
	(0, -1),
	(1, -1),
	(2, 0),
	(-1, 1),
])
def test_moveToAxisOfOperation_movesAxisAndPreservesOriginalArray(
	arrayAxisOperation: NDArray[numpy.int64],
	axisSource: int,
	axisOfOperation: int
) -> None:
	arrayOriginal: NDArray[numpy.int64] = arrayAxisOperation.copy()
	shapeOriginal: tuple[int, ...] = arrayAxisOperation.shape
	arrayExpectedMoved: NDArray[numpy.int64] = numpy.moveaxis(arrayOriginal, axisSource, axisOfOperation)
	valueOffset: int = 13

	with moveToAxisOfOperation(arrayAxisOperation, axisSource, axisOfOperation) as arrayStandardized:
		assert arrayStandardized.shape == arrayExpectedMoved.shape, uniformTestFailureMessage(
			arrayExpectedMoved.shape,
			arrayStandardized.shape,
			moveToAxisOfOperation.__name__,
			axisSource=axisSource,
			axisOfOperation=axisOfOperation
		)
		assert numpy.array_equal(arrayStandardized, arrayExpectedMoved), uniformTestFailureMessage(
			arrayExpectedMoved,
			arrayStandardized,
			moveToAxisOfOperation.__name__,
			axisSource=axisSource,
			axisOfOperation=axisOfOperation
		)

		arrayStandardized += valueOffset

	assert arrayAxisOperation.shape == shapeOriginal, uniformTestFailureMessage(
		shapeOriginal,
		arrayAxisOperation.shape,
		moveToAxisOfOperation.__name__,
		axisSource=axisSource,
		axisOfOperation=axisOfOperation
	)
	assert numpy.array_equal(arrayAxisOperation, arrayOriginal + valueOffset), uniformTestFailureMessage(
		arrayOriginal + valueOffset,
		arrayAxisOperation,
		moveToAxisOfOperation.__name__,
		axisSource=axisSource,
		axisOfOperation=axisOfOperation
	)
