from numpy import ndarray, dtype, float64
from tests.conftest import prototype_numpyArrayEqual
from Z0Z_tools.optionalPyTorchAlternative import def_asTensor
import numpy
import pytest

def functionReturnsNDArray(arrayTarget: ndarray[tuple[int], dtype[float64]]) -> ndarray[tuple[int], dtype[float64]]:
    """Simple function that returns an NDArray."""
    return arrayTarget * 2

wrappedFunction = def_asTensor(functionReturnsNDArray)

def test_def_asTensor_returns_same_callable():
    """Test that def_asTensor returns the same callable without modification."""
    assert wrappedFunction is functionReturnsNDArray

@pytest.mark.parametrize("arrayInput,arrayExpected", [
    (numpy.array([3, 7, 11]), numpy.array([6, 14, 22])),
    (numpy.array([[1, 2], [3, 4]]), numpy.array([[2, 4], [6, 8]])),
    (numpy.zeros((3, 3)), numpy.zeros((3, 3))),
    (numpy.ones(5), numpy.full(5, 2)),
])
def test_def_asTensor_preserves_functionality(arrayInput: ndarray[tuple[int], dtype[float64]], arrayExpected: ndarray[tuple[int], dtype[float64]]):
    """Test that wrapped function maintains original behavior for various inputs."""
    prototype_numpyArrayEqual(arrayExpected, wrappedFunction, arrayInput)
