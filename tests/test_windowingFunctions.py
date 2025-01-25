from numpy.typing import NDArray
from tests.conftest import *
from typing import Union
import numpy
import pytest
import scipy.signal.windows as SciPy
import torch

def prototypeArrayComparison(arrayExpected: NDArray | torch.Tensor, functionTarget: Callable, *arguments: Any, rtol: float = 1e-7, atol: float = 0, **keywordArguments: Any) -> None:
    try:
        arrayActual = functionTarget(*arguments, **keywordArguments)
    except Exception as actualError:
        raise type(actualError)(uniformTestFailureMessage(
            arrayExpected, type(actualError).__name__,
            functionTarget.__name__, *arguments, **keywordArguments
        )) from actualError

    compareMethod = torch if isinstance(arrayActual, torch.Tensor) else numpy

    assert compareMethod.allclose(arrayActual, arrayExpected, rtol=rtol, atol=atol), \
        uniformTestFailureMessage(arrayExpected, arrayActual, functionTarget.__name__,
                         *arguments, **keywordArguments)

def prototypeElephino(arrayTarget: NDArray | torch.Tensor, shapeExpected: tuple[int, ...] | None = None, minValue: float | None = None, maxValue: float | None = None, symmetryAxis: int | None = None) -> None:
    compareMethod = torch if isinstance(arrayTarget, torch.Tensor) else numpy

    if shapeExpected is not None:
        assert arrayTarget.shape == shapeExpected, \
            f"Shape mismatch\nExpected: {shapeExpected}\nGot: {arrayTarget.shape}"

    if minValue is not None:
        assert compareMethod.all(arrayTarget >= minValue), \
            f"Values below minimum {minValue}\nGot: {arrayTarget.min()}"

    if maxValue is not None:
        assert compareMethod.all(arrayTarget <= maxValue), \
            f"Values above maximum {maxValue}\nGot: {arrayTarget.max()}"

    if symmetryAxis is not None:
        midpoint = arrayTarget.shape[symmetryAxis] // 2
        sliceForward = [slice(None)] * arrayTarget.ndim
        sliceForward[symmetryAxis] = slice(0, midpoint)
        firstHalf = arrayTarget[tuple(sliceForward)]

        # Use flip instead of negative step for better compatibility
        if isinstance(arrayTarget, torch.Tensor):
            secondHalf = torch.flip(arrayTarget, [symmetryAxis])[tuple(sliceForward)]
        else:
            secondHalf = numpy.flip(arrayTarget, axis=symmetryAxis)[tuple(sliceForward)]

        assert compareMethod.allclose(firstHalf, secondHalf), \
            uniformTestFailureMessage(firstHalf, secondHalf, "symmetry check",
                            f"axis={symmetryAxis}")

def test_parameterized_windowing_functions(windowingFunctionsPair, lengthWindow: int, ratioTaper: float, device: str):
    """Test all windowing functions with their tensor counterparts."""
    deviceTarget = torch.device(device)

    for functionNumpy, functionTensor in windowingFunctionsPair:
        # Separate handling for functions with different parameters
        if functionNumpy in [halfsine]:  # Functions without taper parameter
            windowingFunction = functionNumpy(lengthWindow)
            windowingFunctionTensor = functionTensor(lengthWindow, device=deviceTarget)

            # Skip taper-specific tests for halfsine
            prototypeElephino(windowingFunction, shapeExpected=(lengthWindow,), minValue=0.0, maxValue=1.0, symmetryAxis=0)  # halfsine is always symmetric

            prototypeElephino(windowingFunctionTensor, shapeExpected=(lengthWindow,), minValue=0.0, maxValue=1.0, symmetryAxis=0)

        else:  # Functions that accept ratioTaper
            windowingFunction = functionNumpy(lengthWindow, ratioTaper=ratioTaper)
            windowingFunctionTensor = functionTensor(lengthWindow, ratioTaper=ratioTaper, device=deviceTarget)

            prototypeElephino(windowingFunction, shapeExpected=(lengthWindow,), minValue=0.0, maxValue=1.0, symmetryAxis=0 if ratioTaper > 0 else None)

            prototypeElephino(windowingFunctionTensor, shapeExpected=(lengthWindow,), minValue=0.0, maxValue=1.0, symmetryAxis=0 if ratioTaper > 0 else None)

            # Test special cases for taper-supporting functions only
            if ratioTaper == 0.0:
                prototypeArrayComparison(numpy.ones(lengthWindow), functionNumpy, lengthWindow, ratioTaper=ratioTaper)
                prototypeArrayComparison(torch.ones(lengthWindow, device=deviceTarget), functionTensor, lengthWindow, ratioTaper=ratioTaper, device=deviceTarget)

def test_halfsine_edge_value(lengthWindow: int):
    """Verify the edge value calculation for halfsine."""
    expectedValue = numpy.sin(numpy.pi * 0.5 / lengthWindow)
    windowingFunction = halfsine(lengthWindow)
    assert numpy.allclose(windowingFunction[0], expectedValue), \
        uniformTestFailureMessage(expectedValue, windowingFunction[0], "halfsine edge value")

def test_tukey_backward_compatibility():
    """Verify backward compatibility of tukey's alpha parameter."""
    arrayExpected = tukey(10, ratioTaper=0.5)
    prototypeArrayComparison(arrayExpected, tukey, 10, alpha=0.5)

def test_tukey_special_cases(lengthWindow: int):
    """Verify special cases of tukey windowing function."""
    # Test rectangular window case (ratioTaper = 0)
    prototypeArrayComparison(numpy.ones(lengthWindow), tukey, lengthWindow, ratioTaper=0.0)

    # Test Hann window case (ratioTaper = 1)
    prototypeArrayComparison(SciPy.hann(lengthWindow), tukey, lengthWindow, ratioTaper=1.0)

@pytest.mark.parametrize("functionWindowingInvalid", [cosineWings, equalPower])
def test_invalid_taper_ratio(functionWindowingInvalid):
    """Verify error handling for invalid taper ratios."""
    with pytest.raises(ValueError):
        functionWindowingInvalid(256, ratioTaper=-0.1)
    with pytest.raises(ValueError):
        functionWindowingInvalid(256, ratioTaper=1.1)
