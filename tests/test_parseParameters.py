from typing import Optional, Union, Callable, Any
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
@pytest.mark.parametrize("input_list,expected", [
    ([1, 2, 3], [1, 2, 3]),
    ([1.0, 2.0, 3.0], [1, 2, 3]),
    ([1, 2.0, 3], [1, 2, 3]),
])
def testIntInnitValidCases(input_list, expected):
    """Test intInnit with valid inputs."""
    from Z0Z_tools import intInnit
    assert intInnit(input_list, 'test') == expected

@pytest.mark.parametrize("invalid_input,expected_error", [
    ([1.5, 2, 3], ValueError),
    ([True, False], TypeError),
    ([], ValueError),
])
def testIntInnitInvalidCases(invalid_input, expected_error):
    """Test intInnit with invalid inputs."""
    from Z0Z_tools import intInnit
    with pytest.raises(expected_error):
        intInnit(invalid_input, 'test')

@pytest.mark.parametrize("input_bytes,expected", [
    (b'\x01', [1]),
    (b'\xff', [255]),
    (bytearray(b'\x02'), [2]),
])
def testIntInnitBytesTypes(input_bytes, expected):
    """Test intInnit with bytes and bytearray inputs."""
    from Z0Z_tools import intInnit
    assert intInnit([input_bytes], 'test') == expected

@pytest.mark.parametrize("input_complex,expected", [
    ([1+0j], [1]),
    ([2+0j, 3+0j], [2, 3]),
])
def testIntInnitComplexNumbers(input_complex, expected):
    """Test intInnit with complex numbers having zero imaginary part."""
    from Z0Z_tools import intInnit
    assert intInnit(input_complex, 'test') == expected

@pytest.mark.parametrize("invalid_complex", [
    [1+1j],
    [2+0.5j],
])
def testIntInnitInvalidComplexNumbers(invalid_complex):
    """Test intInnit with complex numbers having non-zero imaginary part."""
    from Z0Z_tools import intInnit
    with pytest.raises(ValueError):
        intInnit(invalid_complex, 'test')

@pytest.mark.parametrize("input_str,expected", [
    (["123"], [123]),
    (["456", "789"], [456, 789]),
])
def testIntInnitStringNumbers(input_str, expected):
    """Test intInnit with string representations of numbers."""
    from Z0Z_tools import intInnit
    assert intInnit(input_str, 'test') == expected

@pytest.mark.parametrize("invalid_str", [
    ["abc"],
    ["12.3"],
    [""],
    [" "],
])
def testIntInnitInvalidStrings(invalid_str):
    """Test intInnit with invalid string inputs."""
    from Z0Z_tools import intInnit
    with pytest.raises(ValueError):
        intInnit(invalid_str, 'test')

def testIntInnitMutableSequence():
    """Test intInnit's behavior when input sequence is modified during iteration."""
    from Z0Z_tools import intInnit
    class MutableList(list):
        def __iter__(self):
            self.append(4)  # Modify list during iteration
            return super().__iter__()
    
    with pytest.raises(RuntimeError, match="Input sequence was modified during iteration"):
        intInnit(MutableList([1, 2, 3]), 'test')

def testIntInnitNonIterable():
    """Test intInnit with non-iterable input."""
    from Z0Z_tools import intInnit
    with pytest.raises(TypeError, match="does not have the '__iter__' attribute"):
        intInnit(42, 'test') # type: ignore

@pytest.mark.parametrize("input_memview,expected", [
    (memoryview(b'\x01'), [1]),
    (memoryview(b'\xff'), [255]),
])
def testIntInnitMemoryView(input_memview, expected):
    """Test intInnit with memoryview inputs."""
    from Z0Z_tools import intInnit
    assert intInnit([input_memview], 'test') == expected

def testIntInnitLargeMemoryView():
    """Test intInnit with invalid memoryview size."""
    from Z0Z_tools import intInnit
    with pytest.raises(ValueError):
        intInnit([memoryview(b'\x01\x02')], 'test') # type: ignore

@pytest.mark.parametrize("mixed_input,expected", [
    ([1, 2.0, "3", b'\x04'], [1, 2, 3, 4]),
    ([True, 1, 0], TypeError),  # Should fail on boolean
    ([1, None, 3], TypeError),   # Should fail on None
])
def testIntInnitMixedTypes(mixed_input, expected):
    """Test intInnit with mixed type inputs."""
    from Z0Z_tools import intInnit
    if isinstance(expected, list):
        assert intInnit(mixed_input, 'test') == expected
    else:
        with pytest.raises(expected):
            intInnit(mixed_input, 'test')

@pytest.mark.parametrize("empty_input", [
    None,
    [],
    (),
])
def testIntInnitEmptyInput(empty_input):
    """Test intInnit with empty or None input."""
    from Z0Z_tools import intInnit
    with pytest.raises(ValueError, match="I did not receive a value for test, but it is required."):
        intInnit(empty_input, 'test')

@pytest.mark.usefixtures("mockCpuCount")
@pytest.mark.parametrize("stringInput", [
    "invalid",
    "True but not quite",
    "None of the above",
])
def testDefineConcurrencyLimitInvalidStrings(stringInput):
    """Test defineConcurrencyLimit with invalid string inputs."""
    with pytest.raises(ValueError, match="must be a number, True, False, or None"):
        defineConcurrencyLimit(stringInput)

@pytest.mark.usefixtures("mockCpuCount")
@pytest.mark.parametrize("stringNumber, expectedLimit", [
    ("1.5", 1),
    ("-2.5", 6),
    ("4", 4),
    ("0.5", 4),  # 0.5 * 8 CPUs = 4
    ("-0.5", 4), # 8 CPUs - (0.5 * 8) = 4
])
def testDefineConcurrencyLimitStringNumbers(stringNumber, expectedLimit):
    """Test defineConcurrencyLimit handles valid numeric strings."""
    resultLimit = defineConcurrencyLimit(stringNumber)
    assert resultLimit == expectedLimit
