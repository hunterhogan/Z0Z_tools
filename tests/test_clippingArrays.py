from typing import Literal
from numpy._core._exceptions import UFuncTypeError, _UFuncNoLoopError
from numpy._typing._array_like import NDArray
from tests.conftest import *
import numpy
import pytest

@pytest.mark.parametrize("description,expected,arrayTarget,comparand", [
	("Simple array under limit", numpy.array([0.5, -0.5]), numpy.array([0.5, -0.5]), 1.0),
	("Simple array at limit", numpy.array([1.0, -1.0]), numpy.array([1.0, -1.0]), 1.0),
	# ("Simple array over limit", numpy.array([1.0, -1.0]), numpy.array([2.0, -2.0]), 1.0),
	("Array comparand under limit", numpy.array([0.5, -0.5]), numpy.array([0.5, -0.5]), numpy.array([1.0, 1.0])),
	# ("Array comparand mixed limits", numpy.array([0.3, 1.0, -1.0]), numpy.array([0.5, 2.0, -1.5]), numpy.array([0.3, 1.0, 1.0])),
	("Zero array", numpy.zeros(5), numpy.zeros(5), 1.0),
	# ("Zero comparand", numpy.zeros(2), numpy.array([0.5, -0.5]), 0.0),
	("2D array under limit", numpy.array([[0.5, -0.5], [0.3, -0.3]]), numpy.array([[0.5, -0.5], [0.3, -0.3]]), 1.0),
	# ("2D array over limit", numpy.array([[1.0, -1.0], [1.0, -0.8]]), numpy.array([[2.0, -1.5], [1.2, -0.8]]), 1.0),
	("Non-array input", TypeError, 5.0, 1.0),
	("Mismatched shapes", IndexError, numpy.array([1.0, 2.0]), numpy.array([[1.0]])),
	("Invalid dtype", _UFuncNoLoopError, numpy.array(['a', 'b']), 1.0),
	# ("Invalid dtype", UFuncTypeError, numpy.array(['a', 'b']), 1.0),
], ids=lambda x: x if isinstance(x, str) else "")
def testApplyHardLimit(description: Literal['Simple array under limit'] | Literal['Simple array at limit'] | Literal['Array comparand under limit'] | Literal['Zero array'] | Literal['2D array under limit'] | Literal['Non-array input'] | Literal['Mismatched shapes'] | Literal['Invalid dtype'], expected: Any, arrayTarget: NDArray[Any] | NDArray[float64] | float, comparand: float | NDArray[Any]) -> None:
	"""Test applyHardLimit with various inputs."""
	prototype_numpyAllClose(expected, None, None, applyHardLimit, arrayTarget, comparand)

@pytest.mark.parametrize("description,expected,arrayTarget,comparand,penalty", [
	("Simple complex under limit", numpy.array([1+1j, -1-1j]), numpy.array([1+1j, -1-1j]), numpy.array([2.0, 2.0]), 1.0),
	("Simple complex at limit", numpy.array([1+1j, -1-1j]), numpy.array([1+1j, -1-1j]), numpy.array([numpy.sqrt(2), numpy.sqrt(2)]), 1.0),
	("Simple complex over limit", numpy.array([(1+1j)*numpy.sqrt(2), (-1-1j)*numpy.sqrt(2)]), numpy.array([2+2j, -2-2j]), numpy.array([2.0, 2.0]), 1.0),
	# ("Over limit with penalty=2", numpy.array([(1+1j)*2/numpy.sqrt(8), (-1-1j)*2/numpy.sqrt(8)]), numpy.array([2+2j, -2-2j]), numpy.array([2.0, 2.0]), 2.0),
	# ("Complex comparand", numpy.array([(1+1j)*numpy.sqrt(2), (-1-1j)*numpy.sqrt(2)]), numpy.array([2+2j, -2-2j]), numpy.array([1+1j, 1-1j]), 1.0),
	("2D complex array", numpy.array([[1+1j, (1+1j)*numpy.sqrt(2)], [-1-1j, (-1-1j)*numpy.sqrt(2)]]), numpy.array([[1+1j, 2+2j], [-1-1j, -2-2j]]), numpy.array([[2.0, 2.0], [2.0, 2.0]]), 1.0),
	("Zero complex array", numpy.zeros(5, dtype=complex), numpy.zeros(5, dtype=complex), numpy.ones(5), 1.0),
	("Non-complex array", numpy.array([1.0, 1.0]), numpy.array([1.0, 2.0]), numpy.array([1.0, 1.0]), 1.0),
	("Invalid penalty", TypeError, numpy.array([1+1j, 2+2j]), numpy.array([1.0, 1.0]), "invalid"),
	("Mismatched shapes", IndexError, numpy.array([1+1j, 2+2j]), numpy.array([[1.0]]), 1.0),
], ids=lambda x: x if isinstance(x, str) else "")
def testApplyHardLimitComplexValued(description: Literal['Simple complex under limit'] | Literal['Simple complex at limit'] | Literal['Simple complex over limit'] | Literal['2D complex array'] | Literal['Zero complex array'] | Literal['Non-complex array'] | Literal['Invalid penalty'] | Literal['Mismatched shapes'], expected: Any, arrayTarget: NDArray[Any], comparand: NDArray[Any] | NDArray[float64], penalty: float | Literal['invalid']) -> None:
	"""Test applyHardLimitComplexValued with various inputs."""
	prototype_numpyAllClose(expected, None, None, applyHardLimitComplexValued, arrayTarget, comparand, penalty)
