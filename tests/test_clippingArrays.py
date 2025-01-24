# from Z0Z_tools.clippingArrays import applyHardLimit, applyHardLimitComplexValued
# from numpy._core._exceptions import UFuncTypeError, _UFuncNoLoopError
# from tests.conftest import *
# import numpy
# import pytest

# def prototype_numpyAllClose(expected: NDArray[Any], functionTarget: Callable, *arguments: Any, **keywordArguments: Any) -> None:
#     """Template for tests using numpy.allclose comparison."""
#     try:
#         actual = functionTarget(*arguments, **keywordArguments)
#     except Exception as actualError:
#         messageActual = type(actualError).__name__
#         actual = type(actualError)
#         messageExpected = expected if isinstance(expected, type) else "array-like result"
#         assert actual == expected, formatTestMessage(messageExpected, messageActual, functionTarget.__name__, *arguments, **keywordArguments)
#     else:
#         assert numpy.allclose(actual, expected), formatTestMessage(expected, actual, functionTarget.__name__, *arguments, **keywordArguments)

# def prototype_numpyArrayEqual(expected: NDArray[Any], functionTarget: Callable, *arguments: Any, **keywordArguments: Any) -> None:
#     """Template for tests using numpy.array_equal comparison."""
#     try:
#         actual = functionTarget(*arguments, **keywordArguments)
#     except Exception as actualError:
#         messageActual = type(actualError).__name__
#         actual = type(actualError)
#         messageExpected = expected if isinstance(expected, type) else "array-like result"
#         assert actual == expected, formatTestMessage(messageExpected, messageActual, functionTarget.__name__, *arguments, **keywordArguments)
#     else:
#         assert numpy.array_equal(actual, expected), formatTestMessage(expected, actual, functionTarget.__name__, *arguments, **keywordArguments)

# @pytest.mark.parametrize("description,expected,arrayTarget,comparand", [
#     ("Simple array under limit", numpy.array([0.5, -0.5]), numpy.array([0.5, -0.5]), 1.0),
#     ("Simple array at limit", numpy.array([1.0, -1.0]), numpy.array([1.0, -1.0]), 1.0),
#     ("Simple array over limit", numpy.array([1.0, -1.0]), numpy.array([2.0, -2.0]), 1.0),
#     ("Array comparand under limit", numpy.array([0.5, -0.5]), numpy.array([0.5, -0.5]), numpy.array([1.0, 1.0])),
#     ("Array comparand mixed limits", numpy.array([0.3, 1.0, -1.0]), numpy.array([0.5, 2.0, -1.5]), numpy.array([0.3, 1.0, 1.0])),
#     ("Zero array", numpy.zeros(5), numpy.zeros(5), 1.0),
#     ("Zero comparand", numpy.zeros(2), numpy.array([0.5, -0.5]), 0.0),
#     ("2D array under limit", numpy.array([[0.5, -0.5], [0.3, -0.3]]), numpy.array([[0.5, -0.5], [0.3, -0.3]]), 1.0),
#     ("2D array over limit", numpy.array([[1.0, -1.0], [1.0, -0.8]]), numpy.array([[2.0, -1.5], [1.2, -0.8]]), 1.0),
#     ("Non-array input", TypeError, 5.0, 1.0),
#     ("Mismatched shapes", IndexError, numpy.array([1.0, 2.0]), numpy.array([[1.0]])),
#     ("Invalid dtype", _UFuncNoLoopError, numpy.array(['a', 'b']), 1.0),
#     # ("Invalid dtype", UFuncTypeError, numpy.array(['a', 'b']), 1.0),
# ], ids=lambda x: x if isinstance(x, str) else "")
# def testApplyHardLimit(description, expected, arrayTarget, comparand):
#     """Test applyHardLimit with various inputs."""
#     prototype_numpyAllClose(expected, applyHardLimit, arrayTarget, comparand)

# @pytest.mark.parametrize("description,expected,arrayTarget,comparand,penalty", [
#     ("Simple complex under limit", numpy.array([1+1j, -1-1j]), numpy.array([1+1j, -1-1j]), numpy.array([2.0, 2.0]), 1.0),
#     ("Simple complex at limit", numpy.array([1+1j, -1-1j]), numpy.array([1+1j, -1-1j]), numpy.array([numpy.sqrt(2), numpy.sqrt(2)]), 1.0),
#     ("Simple complex over limit", numpy.array([(1+1j)*numpy.sqrt(2), (-1-1j)*numpy.sqrt(2)]), numpy.array([2+2j, -2-2j]), numpy.array([2.0, 2.0]), 1.0),
#     ("Over limit with penalty=2", numpy.array([(1+1j)*2/numpy.sqrt(8), (-1-1j)*2/numpy.sqrt(8)]), numpy.array([2+2j, -2-2j]), numpy.array([2.0, 2.0]), 2.0),
#     ("Complex comparand", numpy.array([(1+1j)*numpy.sqrt(2), (-1-1j)*numpy.sqrt(2)]), numpy.array([2+2j, -2-2j]), numpy.array([1+1j, 1-1j]), 1.0),
#     ("2D complex array", numpy.array([[1+1j, (1+1j)*numpy.sqrt(2)], [-1-1j, (-1-1j)*numpy.sqrt(2)]]), numpy.array([[1+1j, 2+2j], [-1-1j, -2-2j]]), numpy.array([[2.0, 2.0], [2.0, 2.0]]), 1.0),
#     ("Zero complex array", numpy.zeros(5, dtype=complex), numpy.zeros(5, dtype=complex), numpy.ones(5), 1.0),
#     ("Non-complex array", numpy.array([1.0, 1.0]), numpy.array([1.0, 2.0]), numpy.array([1.0, 1.0]), 1.0),
#     ("Invalid penalty", TypeError, numpy.array([1+1j, 2+2j]), numpy.array([1.0, 1.0]), "invalid"),
#     ("Mismatched shapes", IndexError, numpy.array([1+1j, 2+2j]), numpy.array([[1.0]]), 1.0),
# ], ids=lambda x: x if isinstance(x, str) else "")
# def testApplyHardLimitComplexValued(description, expected, arrayTarget, comparand, penalty):
#     """Test applyHardLimitComplexValued with various inputs."""
#     prototype_numpyAllClose(expected, applyHardLimitComplexValued, arrayTarget, comparand, penalty)
