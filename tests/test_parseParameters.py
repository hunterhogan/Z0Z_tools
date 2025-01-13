import pytest
from unittest.mock import patch
from Z0Z_tools.parseParameters import defineConcurrencyLimit, oopsieKwargsie, intInnit
from Z0Z_tools.pytest_parseParameters import (
    makeTestSuiteOopsieKwargsie,
    makeTestSuiteConcurrencyLimit,
    makeTestSuiteIntInnit
)

# Fixtures
@pytest.fixture
def mockCpuCount8():
    """Fixture to mock multiprocessing.cpu_count(). Returns 8."""
    with patch('multiprocessing.cpu_count', return_value=8) as mock:
        yield mock

def testOopsieKwargsie():
    dictionaryTests = makeTestSuiteOopsieKwargsie(oopsieKwargsie)
    for testName, testFunction in dictionaryTests.items():
        testFunction()

@pytest.mark.usefixtures("mockCpuCount8")
def testConcurrencyLimitGenerated():
    dictionaryTests = makeTestSuiteConcurrencyLimit(defineConcurrencyLimit)
    for testName, testFunction in dictionaryTests.items():
        testFunction()

@pytest.mark.usefixtures("mockCpuCount8")
@pytest.mark.parametrize("stringInput", ["invalid", "True but not quite", "None of the above"])
def testInvalidStrings(stringInput):
    with pytest.raises(ValueError, match="must be a number, True, False, or None"):
        defineConcurrencyLimit(stringInput)

@pytest.mark.usefixtures("mockCpuCount8")
@pytest.mark.parametrize("stringNumber, expectedLimit", [
    ("1.5", 1),
    ("-2.5", 6),
    ("4", 4),
    ("0.5", 4),
    ("-0.5", 4),
])
def testStringNumbers(stringNumber, expectedLimit):
    assert defineConcurrencyLimit(stringNumber) == expectedLimit

def testIntInnitGenerated():
    dictionaryTests = makeTestSuiteIntInnit(intInnit)
    for testName, testFunction in dictionaryTests.items():
        testFunction()

@pytest.mark.parametrize("input_bytes,expected", [
    (b'\x01', [1]),
    (b'\xff', [255]),
    (bytearray(b'\x02'), [2]),
    (memoryview(b'\x01'), [1]),
    (memoryview(b'\xff'), [255]),
])
def testBytesTypes(input_bytes, expected):
    assert intInnit([input_bytes], 'test') == expected

@pytest.mark.parametrize("invalid_sequence", [
    b'\x01\x02',  # Too long
    bytearray(b'\x01\x02'),  # Too long
    memoryview(b'\x01\x02'),  # Too long
])
def testRejectsMultiByteSequences(invalid_sequence):
    with pytest.raises(ValueError):
        intInnit([invalid_sequence], 'test')

def testMutableSequence():
    class MutableList(list):
        def __iter__(self):
            self.append(4)
            return super().__iter__()

    with pytest.raises(RuntimeError, match=".*modified during iteration.*"):
        intInnit(MutableList([1, 2, 3]), 'test')

@pytest.mark.parametrize("complex_input,expected", [
    ([1+0j], [1]),
    ([2+0j, 3+0j], [2, 3]),
])
def testHandlesComplexIntegers(complex_input, expected):
    assert intInnit(complex_input, 'test') == expected

@pytest.mark.parametrize("invalid_complex", [
    1+1j,
    2+0.5j,
    3.5+0j,
])
def testRejectsInvalidComplex(invalid_complex):
    with pytest.raises(ValueError):
        intInnit([invalid_complex], 'test')
