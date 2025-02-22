"""
Pytest tests you can use in your package to test some Z0Z_tools functions.

Each function in this module returns a list of test functions that can be used with `pytest.parametrize`.
"""

from collections.abc import Callable, Iterable, Iterator
from typing import Any
from unittest.mock import patch, Mock
from Z0Z_tools import defineConcurrencyLimit, intInnit, oopsieKwargsie
import pytest

def PytestFor_defineConcurrencyLimit(callableToTest: Callable[[bool | float | int | None], int] = defineConcurrencyLimit, cpuCount: int = 8) -> list[tuple[str, Callable[[], None]]]:
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

	Examples
	--------
	Run each test on `Z0Z_tools.defineConcurrencyLimit`
	```
	from Z0Z_tools.pytest_parseParameters import PytestFor_concurrencyLimit

	listOfTests = PytestFor_concurrencyLimit()
	for nameOfTest, callablePytest in listOfTests:
		callablePytest()
	```

	Or, run each test on your function, '`functionLocal`', that has a compatible signature
	```
	from Z0Z_tools.pytest_parseParameters import PytestFor_defineConcurrencyLimit
	from packageLocal import functionLocal as YOUR_FUNCTION_HERE

	@pytest.mark.parametrize("nameOfTest,callablePytest", PytestFor_defineConcurrencyLimit(callableToTest = YOUR_FUNCTION_HERE))
	def test_functionLocal(nameOfTest, callablePytest):
		callablePytest()

	"""
	@patch('multiprocessing.cpu_count', return_value=cpuCount)
	def testDefaults(_mockCpu: Mock) -> None:
		listOfParameters: list[bool | int | None] = [None, False, 0]
		for limitParameter in listOfParameters:
			assert callableToTest(limitParameter) == cpuCount

	@patch('multiprocessing.cpu_count', return_value=cpuCount)
	def testDirectIntegers(_mockCpu: Mock) -> None:
		for limitParameter in [1, 4, 16]:
			assert callableToTest(limitParameter) == limitParameter

	@patch('multiprocessing.cpu_count', return_value=cpuCount)
	def testFractionalFloats(_mockCpu: Mock) -> None:
		testCases: dict[float, int] = {
			0.5: cpuCount // 2,
			0.25: cpuCount // 4,
			0.75: int(cpuCount * 0.75)
		}
		for input, expected in testCases.items():
			assert callableToTest(input) == expected

	@patch('multiprocessing.cpu_count', return_value=cpuCount)
	def testMinimumOne(_mockCpu: Mock) -> None:
		listOfParameters: list[float | int] = [-10, -0.99, 0.1]
		for limitParameter in listOfParameters:
			assert callableToTest(limitParameter) >= 1

	@patch('multiprocessing.cpu_count', return_value=cpuCount)
	def testBooleanTrue(_mockCpu: Mock) -> None:
		assert callableToTest(True) == 1
		assert callableToTest('True') == 1 # type: ignore
		assert callableToTest('TRUE') == 1 # type: ignore
		assert callableToTest(' true ') == 1 # type: ignore

	@patch('multiprocessing.cpu_count', return_value=cpuCount)
	def testInvalidStrings(_mockCpu: Mock) -> None:
		for stringInput in ["invalid", "True but not quite", "None of the above"]:
			with pytest.raises(ValueError, match="must be a number, True, False, or None"):
				callableToTest(stringInput) # type: ignore

	@patch('multiprocessing.cpu_count', return_value=cpuCount)
	def testStringNumbers(_mockCpu: Mock) -> None:
		testCases: list[tuple[str, int]] = [
			("1.51", 2),
			("-2.51", 5),
			("4", 4),
			("0.5", 4),
			("-0.25", 6),
		]
		for stringNumber, expectedLimit in testCases:
			assert callableToTest(stringNumber) == expectedLimit # type: ignore

	return [
		('testDefaults', testDefaults),
		('testDirectIntegers', testDirectIntegers),
		('testFractionalFloats', testFractionalFloats),
		('testMinimumOne', testMinimumOne),
		('testBooleanTrue', testBooleanTrue),
		('testInvalidStrings', testInvalidStrings),
		('testStringNumbers', testStringNumbers)
	]

def PytestFor_intInnit(callableToTest: Callable[[Iterable[int], str | None, type[Any] | None], list[int]] = intInnit) -> list[tuple[str, Callable[[], None]]]:
	"""Returns a list of test functions to validate integer initialization behavior.

	This function provides a comprehensive test suite for validating integer parsing
	and initialization, checking both valid and invalid input scenarios.

	Parameters
		callableToTest (intInnit): The function to test. Should accept:
			- A sequence of integer-compatible values
			- An optional parameter name string
			- An optional parameter type
			Returns a list of validated integers.

	Returns
		listOfTestFunctions: A list of tuples containing:
			- A string describing the test case
			- A callable test function implementing the test case

	Examples
		Run tests on `Z0Z_tools.intInnit`:
		```python
		from Z0Z_tools.pytest_parseParameters import PytestFor_intInnit

		listOfTests = PytestFor_intInnit()
		for nameOfTest, callablePytest in listOfTests:
			callablePytest()
		```

		Run tests on your compatible function:
		```python
		from Z0Z_tools.pytest_parseParameters import PytestFor_intInnit
		from packageLocal import functionLocal as YOUR_FUNCTION_HERE

		@pytest.mark.parametrize("nameOfTest,callablePytest",
			PytestFor_intInnit(callableToTest=YOUR_FUNCTION_HERE))
		def test_functionLocal(nameOfTest, callablePytest):
			callablePytest()
		```
	"""
	def testHandlesValidIntegers() -> None:
		assert callableToTest([2, 3, 5, 8], 'test', None) == [2, 3, 5, 8]
		assert callableToTest([13.0, 21.0, 34.0], 'test', None) == [13, 21, 34] # type: ignore
		assert callableToTest(['55', '89', '144'], 'test', None) == [55, 89, 144] # type: ignore
		assert callableToTest([' 233 ', '377', '-610'], 'test', None) == [233, 377, -610] # type: ignore

	def testRejectsNonWholeNumbers() -> None:
		listInvalidNumbers: list[float] = [13.7, 21.5, 34.8, -55.9]
		for invalidNumber in listInvalidNumbers:
			with pytest.raises(ValueError):
				callableToTest([invalidNumber], 'test', None) # type: ignore

	def testRejectsBooleans() -> None:
		with pytest.raises(TypeError):
			callableToTest([True, False], 'test', None)

	def testRejectsInvalidStrings() -> None:
		for invalidString in ['NW', '', ' ', 'SE.SW']:
			with pytest.raises(ValueError):
				callableToTest([invalidString], 'test', None) # type: ignore

	def testRejectsEmptyList() -> None:
		with pytest.raises(ValueError):
			callableToTest([], 'test', None)

	def testHandlesMixedValidTypes():
		assert callableToTest([13, '21', 34.0], 'test', None) == [13, 21, 34] # type: ignore

	def testHandlesBytes():
		validCases: list[tuple[list[bytes], str, list[int]]] = [
			([b'123'], '123', [123]),
		]
		for inputData, testName, expected in validCases:
			assert callableToTest(inputData, testName, None) == expected  # type: ignore

		extendedCases: list[tuple[list[bytes], str, list[int]]] = [
			([b'123456789'], '123456789', [123456789]),
		]
		for inputData, testName, expected in extendedCases:
			assert callableToTest(inputData, testName, None) == expected  # type: ignore

		invalidCases: list[list[bytes]] = [[b'\x00']]
		for inputData in invalidCases:
			with pytest.raises(ValueError):
				callableToTest(inputData, 'test', None) # type: ignore

	def testHandlesMemoryview():
		validCases: list[tuple[list[memoryview], str, list[int]]] = [
			([memoryview(b'123')], '123', [123]),
		]
		for inputData, testName, expected in validCases:
			assert callableToTest(inputData, testName, None) == expected # type: ignore

		largeMemoryviewCase: list[memoryview] = [memoryview(b'9999999999')]
		assert callableToTest(largeMemoryviewCase, 'test', None) == [9999999999]  # type: ignore

		invalidMemoryviewCases: list[list[memoryview]] = [[memoryview(b'\x00')]]
		for inputData in invalidMemoryviewCases:
			with pytest.raises(ValueError):
				callableToTest(inputData, 'test', None) # type: ignore

	def testRejectsMutableSequence():
		class MutableList(list[int]):
			def __iter__(self) -> Iterator[int]:
				self.append(89)
				return super().__iter__()
		with pytest.raises(RuntimeError, match=".*modified during iteration.*"):
			callableToTest(MutableList([13, 21, 34]), 'test', None)

	def testHandlesComplexIntegers() -> None:
		testCases: list[tuple[list[complex], list[int]]] = [
			([13+0j], [13]),
			([21+0j, 34+0j], [21, 34])
		]
		for inputData, expected in testCases:
			assert callableToTest(inputData, 'test', None) == expected # type: ignore

	def testRejectsInvalidComplex():
		for invalidComplex in [13+1j, 21+0.5j, 34.5+0j]:
			with pytest.raises(ValueError):
				callableToTest([invalidComplex], 'test', None) # type: ignore

	return [
		('testHandlesValidIntegers', testHandlesValidIntegers),
		('testRejectsNonWholeNumbers', testRejectsNonWholeNumbers),
		('testRejectsBooleans', testRejectsBooleans),
		('testRejectsInvalidStrings', testRejectsInvalidStrings),
		('testRejectsEmptyList', testRejectsEmptyList),
		('testHandlesMixedValidTypes', testHandlesMixedValidTypes),
		('testHandlesBytes', testHandlesBytes),
		('testHandlesMemoryview', testHandlesMemoryview),
		('testRejectsMutableSequence', testRejectsMutableSequence),
		('testHandlesComplexIntegers', testHandlesComplexIntegers),
		('testRejectsInvalidComplex', testRejectsInvalidComplex)
	]

def PytestFor_oopsieKwargsie(callableToTest: Callable[[str], bool | None | str] = oopsieKwargsie) -> list[tuple[str, Callable[[], None]]]:
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

	Examples
	--------
	Run each test on `Z0Z_tools.oopsieKwargsie`
	```
	from Z0Z_tools.pytest_parseParameters import PytestFor_oopsieKwargsie

	listOfTests = PytestFor_oopsieKwargsie()
	for nameOfTest, callablePytest in listOfTests:
		callablePytest()
	```

	Or, run each test on your function, '`functionLocal`', that has a compatible signature
	```
	from Z0Z_tools.pytest_parseParameters import PytestFor_oopsieKwargsie
	from packageLocal import functionLocal as YOUR_FUNCTION_HERE

	@pytest.mark.parametrize("nameOfTest,callablePytest", PytestFor_oopsieKwargsie(callableToTest = YOUR_FUNCTION_HERE))
	def test_functionLocal(nameOfTest, callablePytest):
		callablePytest()
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

		assert callableToTest(123) == "123" # type: ignore

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
