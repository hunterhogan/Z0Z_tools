from Z0Z_tools import defineConcurrencyLimit, oopsieKwargsie, intInnit
from typing import Any, Callable, Dict, List, Optional, Sequence, Union, Tuple
from unittest.mock import patch
import pytest

def PytestFor_defineConcurrencyLimit(callableToTest: Callable[[Any], int] = defineConcurrencyLimit, cpuCount: int = 8) -> List[Tuple[str, Callable[[], None]]]:
    """Returns a list of test functions to validate concurrency limit behavior.

    This function provides a comprehensive test suite for validating concurrency limit parsing
    and computation, checking both valid and invalid input scenarios.

    Parameters
    ----------
    callableToTest (defineConcurrencyLimit):
        The function to test, which should accept various input types and return an integer
        representing the concurrency limit. Defaults to defineConcurrencyLimit.
    cpuCount (8):
        The number of CPUs to simulate in the test environment.

    Returns
    -------
    listOfTestFunctions:
        A list of tuples, each containing:
        - A string describing the test case
        - A callable test function that implements the test case

    Test Cases
    ----------
    - Default values (None, False, 0)
    - Direct integer inputs
    - Fractional float inputs
    - Minimum value enforcement
    - Boolean True variants
    - Invalid string inputs
    - String number parsing

    Example
    -------
    ```
    from Z0Z_tools.pytest_parseParameters import PytestFor_concurrencyLimit

    test_functions = PytestFor_concurrencyLimit(myFunction, cpuCount=4)
    for nameOfTest, callablePytest in test_functions:
        callablePytest()  # Runs each test case
    ```
    """
    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testDefaults(_mockCpu):
        for limitParameter in [None, False, 0]:
            assert callableToTest(limitParameter) == cpuCount

    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testDirectIntegers(_mockCpu):
        for limitParameter in [1, 4, 16]:
            assert callableToTest(limitParameter) == limitParameter

    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testFractionalFloats(_mockCpu):
        testCases = {
            0.5: cpuCount // 2,
            0.25: cpuCount // 4,
            0.75: int(cpuCount * 0.75)
        }
        for input, expected in testCases.items():
            assert callableToTest(input) == expected

    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testMinimumOne(_mockCpu):
        for limitParameter in [-10, -0.99, 0.1]:
            assert callableToTest(limitParameter) >= 1

    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testBooleanTrue(_mockCpu):
        assert callableToTest(True) == 1
        assert callableToTest('True') == 1
        assert callableToTest('TRUE') == 1
        assert callableToTest(' true ') == 1

    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testInvalidStrings(_mockCpu):
        for stringInput in ["invalid", "True but not quite", "None of the above"]:
            with pytest.raises(ValueError, match="must be a number, True, False, or None"):
                callableToTest(stringInput)

    @patch('multiprocessing.cpu_count', return_value=cpuCount)
    def testStringNumbers(_mockCpu):
        testCases = [
            ("1.5", 1),
            ("-2.5", 6),
            ("4", 4),
            ("0.5", 4),
            ("-0.5", 4),
        ]
        for stringNumber, expectedLimit in testCases:
            assert callableToTest(stringNumber) == expectedLimit

    return [
        ('testDefaults', testDefaults),
        ('testDirectIntegers', testDirectIntegers),
        ('testFractionalFloats', testFractionalFloats),
        ('testMinimumOne', testMinimumOne),
        ('testBooleanTrue', testBooleanTrue),
        ('testInvalidStrings', testInvalidStrings),
        ('testStringNumbers', testStringNumbers)
    ]

def PytestFor_intInnit(callableToTest: Callable[[Sequence, str], List] = intInnit) -> List[Tuple[str, Callable[[], None]]]:
    """Returns a list of test functions to validate integer initialization behavior.

    This function provides a comprehensive test suite for validating integer parsing and initialization,
    checking both valid and invalid input scenarios.

    Parameters
    ----------
    callableToTest (intInnit):
        The function to test, which should take a sequence and a string parameter and return a list of integers.
        Defaults to intInnit.

    Returns
    -------
    listOfTestFunctions:
        A list of tuples, each containing:
        - A string describing the test case
        - A callable test function that implements the test case

    Test Cases
    ----------
    - Handling of valid integers (including floats and strings representing integers)
    - Rejection of non-whole numbers
    - Rejection of boolean values
    - Rejection of invalid string formats
    - Rejection of empty lists
    - Handling of mixed valid types
    - Handling of single bytes and byte-like objects
    - Protection against mutable sequence modification during iteration
    - Handling of complex numbers with zero imaginary parts
    - Rejection of invalid complex numbers

    Example
    -------
    ```
    from Z0Z_tools.pytest_parseParameters import PytestFor_intInnit

    test_functions = PytestFor_intInnit(Z0Z_tools.intInnit)
    for nameOfTest, callablePytest in test_functions:
        callablePytest()  # Runs each test case
    ```
    """
    def testHandlesValidIntegers():
        assert callableToTest([1, 2, 3], 'test') == [1, 2, 3]
        assert callableToTest([1.0, 2.0, 3.0], 'test') == [1, 2, 3]
        assert callableToTest(['1', '2', '3'], 'test') == [1, 2, 3]
        assert callableToTest([' 42 ', '0', '-1'], 'test') == [42, 0, -1]

    def testRejectsNonWholeNumbers():
        for invalidNumber in [1.5, '1.5', ' 1.5 ', -2.7]:
            with pytest.raises(ValueError):
                callableToTest([invalidNumber], 'test')

    def testRejectsBooleans():
        with pytest.raises(TypeError):
            callableToTest([True, False], 'test')

    def testRejectsInvalidStrings():
        for invalidString in ['abc', '', ' ', '1.2.3']:
            with pytest.raises(ValueError):
                callableToTest([invalidString], 'test')

    def testRejectsEmptyList():
        with pytest.raises(ValueError):
            callableToTest([], 'test')

    def testHandlesMixedValidTypes():
        assert callableToTest([1, '2', 3.0], 'test') == [1, 2, 3]

    def testHandlesSingleBytes():
        testCases = [
            ([b'\x01'], [1]),
            ([b'\xff'], [255]),
            ([bytearray(b'\x02')], [2]),
            ([memoryview(b'\x01')], [1]),
            ([memoryview(b'\xff')], [255]),
        ]
        for inputData, expected in testCases:
            assert callableToTest(inputData, 'test') == expected
        with pytest.raises(ValueError):
            callableToTest([b'\x01\x02'], 'test')

    def testRejectsMutableSequence():
        class MutableList(list):
            def __iter__(self):
                self.append(4)
                return super().__iter__()
        with pytest.raises(RuntimeError, match=".*modified during iteration.*"):
            callableToTest(MutableList([1, 2, 3]), 'test')

    def testHandlesComplexIntegers():
        testCases = [
            ([1+0j], [1]),
            ([2+0j, 3+0j], [2, 3])
        ]
        for inputData, expectedList in testCases:
            assert callableToTest(inputData, 'test') == expectedList

    def testRejectsInvalidComplex():
        for invalidComplex in [1+1j, 2+0.5j, 3.5+0j]:
            with pytest.raises(ValueError):
                callableToTest([invalidComplex], 'test')

    return [
        ('testHandlesValidIntegers', testHandlesValidIntegers),
        ('testRejectsNonWholeNumbers', testRejectsNonWholeNumbers),
        ('testRejectsBooleans', testRejectsBooleans),
        ('testRejectsInvalidStrings', testRejectsInvalidStrings),
        ('testRejectsEmptyList', testRejectsEmptyList),
        ('testHandlesMixedValidTypes', testHandlesMixedValidTypes),
        ('testHandlesSingleBytes', testHandlesSingleBytes),
        ('testRejectsMutableSequence', testRejectsMutableSequence),
        ('testHandlesComplexIntegers', testHandlesComplexIntegers),
        ('testRejectsInvalidComplex', testRejectsInvalidComplex)
    ]

def PytestFor_oopsieKwargsie(callableToTest: Callable[[str], Optional[Union[bool, str]]] = oopsieKwargsie) -> List[Tuple[str, Callable[[], None]]]:
    """Returns a list of test functions to validate string-to-boolean/None conversion behavior.

    This function provides a comprehensive test suite for validating string parsing and conversion
    to boolean or None values, with fallback to the original string when appropriate.

    Parameters
    ----------
    callableToTest (oopsieKwargsie):
        The function to test, which should accept a string and return either a boolean, None,
        or the original input. Defaults to oopsieKwargsie.

    Returns
    -------
    listOfTestFunctions:
        A list of tuples, each containing:
        - A string describing the test case
        - A callable test function that implements the test case

    Test Cases
    ----------
    - True string variants (case-insensitive)
    - False string variants (case-insensitive)
    - None string variants (case-insensitive)
    - Non-convertible strings (returned as-is)
    - Non-string object handling
        - Numbers (converted to strings)
        - Objects with failed str() conversion (returned as-is)

    Example
    -------
    ```
    from Z0Z_tools.pytest_parseParameters import PytestFor_oopsieKwargsie

    test_functions = PytestFor_oopsieKwargsie(myFunction)
    for nameOfTest, callablePytest in test_functions:
        callablePytest()  # Runs each test case
    ```
    """
    def testHandlesTrueVariants():
        for variantTrue in ['True', 'TRUE', ' true ', 'TrUe']:
            assert callableToTest(variantTrue) is True

    def testHandlesFalseVariants():
        for variantFalse in ['False', 'FALSE', ' false ', 'FaLsE']:
            assert callableToTest(variantFalse) is False

    def testHandlesNoneVariants():
        for variantNone in ['None', 'NONE', ' none ', 'NoNe']:
            assert callableToTest(variantNone) is None

    def testReturnsOriginalString():
        for stringInput in ['hello', '123', 'True story', 'False alarm']:
            assert callableToTest(stringInput) == stringInput

    def testHandlesNonStringObjects():
        class UnStringable:
            def __str__(self):
                raise TypeError("Cannot be stringified")

        # This integer should get converted to string
        assert callableToTest(123) == "123" # type: ignore

        # This custom object should be returned as-is (same object) if str() fails
        unStringableObject = UnStringable()
        result = callableToTest(unStringableObject) # type: ignore
        assert result is unStringableObject

    return [
        ('testHandlesTrueVariants', testHandlesTrueVariants),
        ('testHandlesFalseVariants', testHandlesFalseVariants),
        ('testHandlesNoneVariants', testHandlesNoneVariants),
        ('testReturnsOriginalString', testReturnsOriginalString),
        ('testHandlesNonStringObjects', testHandlesNonStringObjects)
    ]
