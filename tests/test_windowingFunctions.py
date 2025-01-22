"""Tests for windowing functions.

Uses standardized test infrastructure from conftest.py.
Prefers semantically meaningful identifiers over technical terms.
"""
from numpy.typing import NDArray
import numpy
import pytest
import scipy.signal.windows as SciPy
import torch
from tests.conftest import *
from typing import Union

def test_parameterized_windowing_functions(windowingFunctionsPair, lengthWindow: int,
                                         ratioTaper: float, device: str):
    """Test all windowing functions with their tensor counterparts."""
    deviceTarget = torch.device(device)

    for functionNumpy, functionTensor in windowingFunctionsPair:
        # Separate handling for functions with different parameters
        if functionNumpy in [halfsine]:  # Functions without taper parameter
            windowingFunction = functionNumpy(lengthWindow)
            windowingFunctionTensor = functionTensor(lengthWindow, device=deviceTarget)

            # Skip taper-specific tests for halfsine
            verifyArrayProperties(windowingFunction,
                                shapeExpected=(lengthWindow,),
                                minValue=0.0,
                                maxValue=1.0,
                                symmetryAxis=0)  # halfsine is always symmetric

            verifyArrayProperties(windowingFunctionTensor,
                                shapeExpected=(lengthWindow,),
                                minValue=0.0,
                                maxValue=1.0,
                                symmetryAxis=0)

        else:  # Functions that accept ratioTaper
            windowingFunction = functionNumpy(lengthWindow, ratioTaper=ratioTaper)
            windowingFunctionTensor = functionTensor(lengthWindow, ratioTaper=ratioTaper,
                                                   device=deviceTarget)

            verifyArrayProperties(windowingFunction,
                                shapeExpected=(lengthWindow,),
                                minValue=0.0,
                                maxValue=1.0,
                                symmetryAxis=0 if ratioTaper > 0 else None)

            verifyArrayProperties(windowingFunctionTensor,
                                shapeExpected=(lengthWindow,),
                                minValue=0.0,
                                maxValue=1.0,
                                symmetryAxis=0 if ratioTaper > 0 else None)

            # Test special cases for taper-supporting functions only
            if ratioTaper == 0.0:
                standardArrayComparison(numpy.ones(lengthWindow),
                                     functionNumpy,
                                     lengthWindow,
                                     ratioTaper=ratioTaper)
                standardArrayComparison(torch.ones(lengthWindow, device=deviceTarget),
                                     functionTensor,
                                     lengthWindow,
                                     ratioTaper=ratioTaper,
                                     device=deviceTarget)

def test_halfsine_edge_value(lengthWindow: int):
    """Verify the edge value calculation for halfsine."""
    expectedValue = numpy.sin(numpy.pi * 0.5 / lengthWindow)
    windowingFunction = halfsine(lengthWindow)
    assert numpy.allclose(windowingFunction[0], expectedValue), \
        formatTestMessage(expectedValue, windowingFunction[0], "halfsine edge value")

def test_tukey_backward_compatibility():
    """Verify backward compatibility of tukey's alpha parameter."""
    arrayExpected = tukey(10, ratioTaper=0.5)
    standardArrayComparison(arrayExpected,
                          tukey,
                          10,
                          alpha=0.5)

def test_tukey_special_cases(lengthWindow: int):
    """Verify special cases of tukey windowing function."""
    # Test rectangular window case (ratioTaper = 0)
    standardArrayComparison(numpy.ones(lengthWindow),
                          tukey,
                          lengthWindow,
                          ratioTaper=0.0)

    # Test Hann window case (ratioTaper = 1)
    standardArrayComparison(SciPy.hann(lengthWindow),
                          tukey,
                          lengthWindow,
                          ratioTaper=1.0)

@pytest.mark.parametrize("functionWindowingInvalid", [cosineWings, equalPower])
def test_invalid_taper_ratio(functionWindowingInvalid):
    """Verify error handling for invalid taper ratios."""
    with pytest.raises(ValueError):
        functionWindowingInvalid(256, ratioTaper=-0.1)
    with pytest.raises(ValueError):
        functionWindowingInvalid(256, ratioTaper=1.1)
