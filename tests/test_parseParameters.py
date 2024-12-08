
from typing import Optional, Union
import pytest
from unittest.mock import patch
from Z0Z_tools import defineConcurrencyLimit, oopsieKwargsie

@pytest.fixture
def mockCpuCount():
    """Fixture to mock multiprocessing.cpu_count(). Always returns 8."""
    with patch('multiprocessing.cpu_count', return_value=8):
        yield

@pytest.mark.parametrize("variantTrue", ['True', 'TRUE', ' true ', 'TrUe'])
def testOopsieKwargsieHandlesTrueVariants(variantTrue):
    """Test oopsieKwargsie handles various string representations of True."""
    assert oopsieKwargsie(variantTrue) is True

@pytest.mark.parametrize("variantFalse", ['False', 'FALSE', ' false ', 'FaLsE'])
def testOopsieKwargsieHandlesFalseVariants(variantFalse):
    """Test oopsieKwargsie handles various string representations of False."""
    assert oopsieKwargsie(variantFalse) is False

@pytest.mark.parametrize("variantNone", ['None', 'NONE', ' none ', 'NoNe'])
def testOopsieKwargsieHandlesNoneVariants(variantNone):
    """Test oopsieKwargsie handles various string representations of None."""
    assert oopsieKwargsie(variantNone) is None

@pytest.mark.parametrize("stringInput", ['hello', '123', 'True story', 'False alarm'])
def testOopsieKwargsieReturnsOriginalString(stringInput):
    """Test oopsieKwargsie returns the original string when input is unrecognized."""
    assert oopsieKwargsie(stringInput) == stringInput

@pytest.mark.usefixtures("mockCpuCount")
@pytest.mark.parametrize("limitParameter, expectedLimit", [
    (None, 8),
    (False, 8),
    (0, 8),
])
def testDefineConcurrencyLimitDefaults(limitParameter, expectedLimit):
    """Test defineConcurrencyLimit with default parameters."""
    resultLimit = defineConcurrencyLimit(limitParameter)
    assert resultLimit == expectedLimit

@pytest.mark.usefixtures("mockCpuCount")
@pytest.mark.parametrize("limitParameter, expectedLimit", [
    (1, 1),
    (4, 4),
    (16, 16),
])
def testDefineConcurrencyLimitDirectIntegers(limitParameter, expectedLimit):
    """Test defineConcurrencyLimit with direct integer values ≥ 1."""
    resultLimit = defineConcurrencyLimit(limitParameter)
    assert resultLimit == expectedLimit

@pytest.mark.usefixtures("mockCpuCount")
@pytest.mark.parametrize("limitParameter, expectedLimit", [
    (0.5, 4),
    (0.25, 2),
    (0.75, 6),
])
def testDefineConcurrencyLimitFractionalFloats(limitParameter, expectedLimit):
    """Test defineConcurrencyLimit with float values between 0 and 1."""
    resultLimit = defineConcurrencyLimit(limitParameter)
    assert resultLimit == expectedLimit

@pytest.mark.usefixtures("mockCpuCount")
@pytest.mark.parametrize("limitParameter, expectedLimit", [
    (-0.5, 4),
    (-0.25, 6),
    (-0.75, 2),
])
def testDefineConcurrencyLimitNegativeFractions(limitParameter, expectedLimit):
    """Test defineConcurrencyLimit with float values between -1 and 0."""
    resultLimit = defineConcurrencyLimit(limitParameter)
    assert resultLimit == expectedLimit

@pytest.mark.usefixtures("mockCpuCount")
@pytest.mark.parametrize("limitParameter, expectedLimit", [
    (-1, 7),
    (-3, 5),
    (-7, 1),
])
def testDefineConcurrencyLimitNegativeIntegers(limitParameter, expectedLimit):
    """Test defineConcurrencyLimit with integer values ≤ -1."""
    resultLimit = defineConcurrencyLimit(limitParameter)
    assert resultLimit == expectedLimit

@pytest.mark.usefixtures("mockCpuCount")
def testDefineConcurrencyLimitBooleanTrue():
    """Test defineConcurrencyLimit with boolean True."""
    resultLimit = defineConcurrencyLimit(True)
    assert resultLimit == 1

@pytest.mark.usefixtures("mockCpuCount")
def testDefineConcurrencyLimitSpecificTrueCase():
    """Ensure defineConcurrencyLimit(True) specifically returns 1."""
    resultTrue = defineConcurrencyLimit(True)
    resultNone = defineConcurrencyLimit(None)
    assert resultTrue == 1
    assert resultNone != 1

@pytest.mark.usefixtures("mockCpuCount")
@patch('Z0Z_tools.parseParameters.oopsieKwargsie')
@pytest.mark.parametrize("stringInput, mockedReturn, expectedLimit", [
    ("true", True, 1),
    ("false", False, 8),
    ("none", None, 8),
    ("4", 4, 4),
])
def testDefineConcurrencyLimitStringValues(mockOopsieKwargsie, stringInput, mockedReturn, expectedLimit):
    """Test defineConcurrencyLimit handling of string inputs via oopsieKwargsie."""
    mockOopsieKwargsie.return_value = mockedReturn
    resultLimit = defineConcurrencyLimit(stringInput)
    assert resultLimit == expectedLimit

@pytest.mark.usefixtures("mockCpuCount")
@pytest.mark.parametrize("limitParameter, expectedLimit", [
    (-10, 1),
    (-0.99, 1),
    (0.1, 1),
])
def testDefineConcurrencyLimitEnsuresMinimumOne(limitParameter, expectedLimit):
    """Test defineConcurrencyLimit ensures the minimum return value is 1."""
    resultLimit = defineConcurrencyLimit(limitParameter)
    assert resultLimit == expectedLimit