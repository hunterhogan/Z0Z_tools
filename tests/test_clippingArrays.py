from numpy._core._exceptions import _UFuncNoLoopError, UFuncTypeError
from tests.conftest import *
import numpy
import pytest
from typing import Any

@pytest.mark.parametrize("description,expected,arrayTarget,comparand", [
    ("Simple array under limit", numpy.array([0.3, -0.5]), numpy.array([0.3, -0.5]), 0.8),
    ("Simple array at limit", numpy.array([1.3, -1.3]), numpy.array([1.3, -1.3]), 1.3),
    # ("Simple array over limit", numpy.array([2.1, -2.1]), numpy.array([3.4, -3.4]), 2.1),
    ("Array comparand under limit", numpy.array([0.5, -0.8]), numpy.array([0.5, -0.8]), numpy.array([1.3, 2.1])),
    ("Array comparand mixed limits", numpy.array([0.3, 2.1, -3.4]), numpy.array([0.3, 5.5, -3.4]), numpy.array([0.5, 2.1, 3.4])),
    ("Zero array", numpy.zeros(3), numpy.zeros(3), 1.3),
    # ("Zero comparand", numpy.zeros(2), numpy.array([0.8, -1.3]), 0.0),
    ("2D array under limit", numpy.array([[0.3, -0.8], [1.3, -2.1]]), numpy.array([[0.3, -0.8], [1.3, -2.1]]), 3.4),
    ("2D array over limit", numpy.array([[2.1, -3.4], [5.5, -0.8]]), numpy.array([[2.1, -3.4], [5.5, -0.8]]), 5.5),
    ("Non-array input", TypeError, 0.5, 0.8),
    ("Mismatched shapes", IndexError, numpy.array([1.3, 2.1]), numpy.array([[3.4]])),
    ("Invalid dtype", _UFuncNoLoopError, numpy.array(['N', 'E']), 1.3),
    # ("Invalid dtype", type[UFuncTypeError], numpy.array(['S', 'W']), 2.1),
], ids=lambda x: x if isinstance(x, str) else "")
def testApplyHardLimit(description: str, expected: NDArray[Any] | type[Exception], arrayTarget: NDArray[Any] | float, comparand: float | NDArray[Any]) -> None:
    """Test applyHardLimit with various inputs."""
    prototype_numpyAllClose(expected, None, None, applyHardLimit, arrayTarget, comparand)

@pytest.mark.parametrize("description,expected,arrayTarget,comparand,penalty", [
    ("Simple complex under limit", numpy.array([0.3+0.5j, -0.8-1.3j]), numpy.array([0.3+0.5j, -0.8-1.3j]), numpy.array([2.1, 3.4]), 0.5),
    ("Simple complex at limit", numpy.array([0.8+1.3j, -2.1-3.4j]), numpy.array([0.8+1.3j, -2.1-3.4j]), numpy.array([3.4, 5.5]), 0.8),
    # ("Simple complex over limit", numpy.array([(1.3+2.1j)*numpy.sqrt(2), (-3.4-5.5j)*numpy.sqrt(2)]), numpy.array([2.1+3.4j, -5.5-0.8j]), numpy.array([0.3, 0.5]), 1.3),
    # ("Non-complex array", numpy.array([0.3, 0.8]), numpy.array([1.3, 2.1]), numpy.array([3.4, 5.5]), 2.1),
    ("Invalid penalty", TypeError, numpy.array([0.5+0.8j, 1.3+2.1j]), numpy.array([3.4, 5.5]), "invalid"),
    ("Zero complex array", numpy.zeros(3, dtype=complex), numpy.zeros(3, dtype=complex), numpy.array([0.3, 0.5, 0.8])*1.3, 3.4),
    ("Mismatched shapes", IndexError, numpy.array([0.3+0.5j, 0.8+1.3j]), numpy.array([[2.1]]), 5.5),
    # ("2D complex array", numpy.array([[0.3+0.5j, (0.8+1.3j)*numpy.sqrt(2)], [-2.1-3.4j, (-5.5-0.8j)*numpy.sqrt(2)]], dtype=numpy.complex128),
    #                     numpy.array([[0.3+0.5j, 1.3+2.1j], [-3.4-5.5j, -0.8-0.3j]], dtype=numpy.complex128),
    #                     numpy.array([[0.5, 0.8], [1.3, 2.1]], dtype=numpy.float64), 3.4),
    # ("Over limit with penalty=2", numpy.array([(0.3+0.5j)*2/numpy.sqrt(8), (-0.8-1.3j)*2/numpy.sqrt(8)]),
    #                             numpy.array([2.1+3.4j, -5.5-0.8j]), numpy.array([0.3, 0.5]), 2.0),
    # ("Complex comparand", numpy.array([(1.3+2.1j)*numpy.sqrt(2), (-3.4-5.5j)*numpy.sqrt(2)]),
    #                     numpy.array([0.3+0.5j, -0.8-1.3j]), numpy.array([2.1+3.4j, 5.5+0.8j]), 0.5),
], ids=lambda x: x if isinstance(x, str) else "")
def testApplyHardLimitComplexValued(description: str
, expected: Any
, arrayTarget: NDArray[Any]
, comparand: NDArray[Any] | NDArray[float64]
, penalty: float | str
) -> None:
    prototype_numpyAllClose(expected, None, None, applyHardLimitComplexValued, arrayTarget, comparand, penalty)
