import pytest
from unittest.mock import patch
from typing import Callable, Any, Optional, Union

def makeTestSuiteOopsieKwargsie(functionUnderTest: Callable[[str], Optional[Union[bool, str]]]):
    """
    Creates a test suite for oopsieKwargsie-like functions.
    
    Parameters:
        functionUnderTest: The function to test, must accept str and return bool|None|str

    Returns:
        dictionaryTests: Dictionary of test functions to run
    """
    def testHandlesTrueVariants():
        for variantTrue in ['True', 'TRUE', ' true ', 'TrUe']:
            assert functionUnderTest(variantTrue) is True

    def testHandlesFalseVariants():
        for variantFalse in ['False', 'FALSE', ' false ', 'FaLsE']:
            assert functionUnderTest(variantFalse) is False

    def testHandlesNoneVariants():
        for variantNone in ['None', 'NONE', ' none ', 'NoNe']:
            assert functionUnderTest(variantNone) is None

    def testReturnsOriginalString():
        for stringInput in ['hello', '123', 'True story', 'False alarm']:
            assert functionUnderTest(stringInput) == stringInput

    return {
        'testHandlesTrueVariants': testHandlesTrueVariants,
        'testHandlesFalseVariants': testHandlesFalseVariants,
        'testHandlesNoneVariants': testHandlesNoneVariants,
        'testReturnsOriginalString': testReturnsOriginalString
    }

def makeTestSuiteConcurrencyLimit(functionUnderTest: Callable[[Any], int], cpuCount: int = 8):
    """
    Creates a test suite for defineConcurrencyLimit-like functions.
    
    Parameters:
        functionUnderTest: The function to test, must return int
        cpuCount (8): Number of CPUs to simulate

    Returns:
        dictionaryTests: Dictionary of test functions to run
    """
    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testDefaults(_mockCpu):
        for limitParameter in [None, False, 0]:
            assert functionUnderTest(limitParameter) == cpuCount

    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testDirectIntegers(_mockCpu):
        for limitParameter in [1, 4, 16]:
            assert functionUnderTest(limitParameter) == limitParameter

    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testFractionalFloats(_mockCpu):
        testCases = {
            0.5: cpuCount // 2,
            0.25: cpuCount // 4,
            0.75: int(cpuCount * 0.75)
        }
        for input, expected in testCases.items():
            assert functionUnderTest(input) == expected

    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testMinimumOne(_mockCpu):
        for limitParameter in [-10, -0.99, 0.1]:
            assert functionUnderTest(limitParameter) >= 1

    return {
        'testDefaults': testDefaults,
        'testDirectIntegers': testDirectIntegers,
        'testFractionalFloats': testFractionalFloats,
        'testMinimumOne': testMinimumOne
    }

def makeTestSuiteIntInnit(functionUnderTest):
    """
    Creates a test suite for intInnit-like functions.
    
    Parameters:
        functionUnderTest: The function to test, must accept list and return list[int]

    Returns:
        dictionaryTests: Dictionary of test functions to run
    """
    def testHandlesValidIntegers():
        assert functionUnderTest([1, 2, 3], 'test') == [1, 2, 3]
        assert functionUnderTest([1.0, 2.0, 3.0], 'test') == [1, 2, 3]

    def testRejectsNonWholeNumbers():
        with pytest.raises(ValueError):
            functionUnderTest([1.5, 2, 3], 'test')

    def testRejectsBooleans():
        with pytest.raises(TypeError):
            functionUnderTest([True, False], 'test')

    def testRejectsNonNumerics():
        with pytest.raises(TypeError):
            functionUnderTest(['1', '2', '3'], 'test')

    def testRejectsEmptyList():
        with pytest.raises(ValueError):
            functionUnderTest([], 'test')

    def testHandlesMixedValidTypes():
        assert functionUnderTest([1, 2.0, 3], 'test') == [1, 2, 3]

    return {
        'testHandlesValidIntegers': testHandlesValidIntegers,
        'testRejectsNonWholeNumbers': testRejectsNonWholeNumbers,
        'testRejectsBooleans': testRejectsBooleans,
        'testRejectsNonNumerics': testRejectsNonNumerics,
        'testRejectsEmptyList': testRejectsEmptyList,
        'testHandlesMixedValidTypes': testHandlesMixedValidTypes
    }

