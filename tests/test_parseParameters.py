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

# Test Suites from pytest_parseParameters.py
class TestOopsieKwargsie:
    """Test suite for oopsieKwargsie using both direct tests and generated tests."""
    dictionaryTestsGenerated = makeTestSuiteOopsieKwargsie(oopsieKwargsie)
    
    def testHandlesTrueVariants(self):
        self.dictionaryTestsGenerated['testHandlesTrueVariants']()
    
    def testHandlesFalseVariants(self):
        self.dictionaryTestsGenerated['testHandlesFalseVariants']()
    
    def testHandlesNoneVariants(self):
        self.dictionaryTestsGenerated['testHandlesNoneVariants']()
    
    def testReturnsOriginalString(self):
        self.dictionaryTestsGenerated['testReturnsOriginalString']()

class TestDefineConcurrencyLimit:
    """Test suite for defineConcurrencyLimit using both direct tests and generated tests."""
    @pytest.mark.usefixtures("mockCpuCount8")
    def testGeneratedTests(self):
        dictionaryTests = makeTestSuiteConcurrencyLimit(defineConcurrencyLimit)
        for testFunction in dictionaryTests.values():
            testFunction()
    
    @pytest.mark.usefixtures("mockCpuCount8")
    @pytest.mark.parametrize("stringInput", ["invalid", "True but not quite", "None of the above"])
    def testInvalidStrings(self, stringInput):
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
    def testStringNumbers(self, stringNumber, expectedLimit):
        assert defineConcurrencyLimit(stringNumber) == expectedLimit

class TestIntInnit:
    """Test suite for intInnit using both direct tests and generated tests."""
    dictionaryTestsGenerated = makeTestSuiteIntInnit(intInnit)

    def testGeneratedTests(self):
        for testFunction in self.dictionaryTestsGenerated.values():
            testFunction()

    @pytest.mark.parametrize("input_bytes,expected", [
        (b'\x01', [1]),
        (b'\xff', [255]),
        (bytearray(b'\x02'), [2]),
        (memoryview(b'\x01'), [1]),
        (memoryview(b'\xff'), [255]),
    ])
    def testBytesTypes(self, input_bytes, expected):
        assert intInnit([input_bytes], 'test') == expected

    @pytest.mark.parametrize("invalid_sequence", [
        b'\x01\x02',  # Too long
        bytearray(b'\x01\x02'),  # Too long
        memoryview(b'\x01\x02'),  # Too long
    ])
    def testRejectsMultiByteSequences(self, invalid_sequence):
        with pytest.raises(ValueError):
            intInnit([invalid_sequence], 'test')

    def testMutableSequence(self):
        class MutableList(list):
            def __iter__(self):
                self.append(4)
                return super().__iter__()
        
        with pytest.raises(RuntimeError, match="Input sequence was modified during iteration"):
            intInnit(MutableList([1, 2, 3]), 'test')

    @pytest.mark.parametrize("complex_input,expected", [
        ([1+0j], [1]),
        ([2+0j, 3+0j], [2, 3]),
    ])
    def testHandlesComplexIntegers(self, complex_input, expected):
        assert intInnit(complex_input, 'test') == expected

    @pytest.mark.parametrize("invalid_complex", [
        1+1j,
        2+0.5j,
        3.5+0j,
    ])
    def testRejectsInvalidComplex(self, invalid_complex):
        with pytest.raises(ValueError):
            intInnit([invalid_complex], 'test')
