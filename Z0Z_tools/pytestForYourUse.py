"""Pytest tests you can use in your package to test some Z0Z_tools functions.

Each function in this module returns a list of test functions that can be used with `pytest.parametrize`.
"""
# ruff: noqa: S101
from collections.abc import Callable, Iterable, Iterator
from typing import Any, NoReturn
from unittest.mock import Mock, patch
from Z0Z_tools import defineConcurrencyLimit, intInnit, oopsieKwargsie
import pytest

def PytestFor_defineConcurrencyLimit(callableToTest: Callable[..., int] = defineConcurrencyLimit, cpuCount: int = 8) -> list[tuple[str, Callable[[], None]]]:  # noqa: C901
	"""Return a list of test functions to validate concurrency limit behavior.

	This function provides a comprehensive test suite for validating concurrency limit parsing
	and computation, checking both valid and invalid input scenarios.

	Parameters
	----------
	callableToTest : Callable[[bool | float | int | None, int], int] = defineConcurrencyLimit
		The function to test, which should accept various input types and return an integer
		representing the concurrency limit.
	cpuCount : int = 8
		The number of CPUs to simulate in the test environment.

	Returns
	-------
	listOfTestFunctions : list[tuple[str, Callable[[], None]]]
		A list of tuples, each containing a string describing the test case and a callable
		test function that implements the test case.

	Examples
	--------
	Run each test on `Z0Z_tools.defineConcurrencyLimit`:
	```python
	from Z0Z_tools.pytestForYourUse import PytestFor_defineConcurrencyLimit

	listOfTests = PytestFor_defineConcurrencyLimit()
	for nameOfTest, callablePytest in listOfTests:
		callablePytest()
	```

	Or, run each test on your function that has a compatible signature:
	```python
	from Z0Z_tools.pytestForYourUse import PytestFor_defineConcurrencyLimit
	from packageLocal import functionLocal

	@pytest.mark.parametrize("nameOfTest,callablePytest", PytestFor_defineConcurrencyLimit(callableToTest=functionLocal))
	def test_functionLocal(nameOfTest, callablePytest):
		callablePytest()
	```

	"""
	@patch('multiprocessing.cpu_count', return_value=cpuCount)
	def testDefaults(_mockCpu: Mock) -> None:
		listOfParameters: list[bool | int | None] = [None, False, 0]
		for limitParameter in listOfParameters:
			assert callableToTest(limit=limitParameter, cpuTotal=cpuCount) == cpuCount

	@patch('multiprocessing.cpu_count', return_value=cpuCount)
	def testDirectIntegers(_mockCpu: Mock) -> None:
		for limitParameter in [1, 4, 16]:
			assert callableToTest(limit=limitParameter, cpuTotal=cpuCount) == limitParameter

	@patch('multiprocessing.cpu_count', return_value=cpuCount)
	def testFractionalFloats(_mockCpu: Mock) -> None:
		testCases: dict[float, int] = {
			0.5: cpuCount // 2,
			0.25: cpuCount // 4,
			0.75: int(cpuCount * 0.75)
		}
		for limit, expected in testCases.items():
			assert callableToTest(limit=limit, cpuTotal=cpuCount) == expected

	@patch('multiprocessing.cpu_count', return_value=cpuCount)
	def testMinimumOne(_mockCpu: Mock) -> None:
		listOfParameters: list[float | int] = [-10, -0.99, 0.1]
		for limitParameter in listOfParameters:
			assert callableToTest(limit=limitParameter, cpuTotal=cpuCount) >= 1

	@patch('multiprocessing.cpu_count', return_value=cpuCount)
	def testBooleanTrue(_mockCpu: Mock) -> None:
		assert callableToTest(limit=True, cpuTotal=cpuCount) == 1
		assert callableToTest(limit='True', cpuTotal=cpuCount) == 1  # pyright: ignore[reportArgumentType]
		assert callableToTest(limit='TRUE', cpuTotal=cpuCount) == 1 # pyright: ignore[reportArgumentType]
		assert callableToTest(limit=' true ', cpuTotal=cpuCount) == 1 # pyright: ignore[reportArgumentType]

	@patch('multiprocessing.cpu_count', return_value=cpuCount)
	def testInvalidStrings(_mockCpu: Mock) -> None:
		for stringInput in ["invalid", "True but not quite", "None of the above"]:
			with pytest.raises(ValueError, match="must be a number, True, False, or None"):
				callableToTest(limit=stringInput, cpuTotal=cpuCount) # pyright: ignore[reportArgumentType]

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
			assert callableToTest(limit=stringNumber, cpuTotal=cpuCount) == expectedLimit # pyright: ignore[reportArgumentType]

	return [
		('testDefaults', testDefaults),
		('testDirectIntegers', testDirectIntegers),
		('testFractionalFloats', testFractionalFloats),
		('testMinimumOne', testMinimumOne),
		('testBooleanTrue', testBooleanTrue),
		('testInvalidStrings', testInvalidStrings),
		('testStringNumbers', testStringNumbers)
	]

def PytestFor_intInnit(callableToTest: Callable[[Iterable[int], str | None, type[Any] | None], list[int]] = intInnit) -> list[tuple[str, Callable[[], None]]]:  # noqa: C901
	"""Return a list of test functions to validate integer initialization behavior.

	This function provides a comprehensive test suite for validating integer parsing
	and initialization, checking both valid and invalid input scenarios.

	Parameters
	----------
	callableToTest : Callable[[Iterable[int], str | None, type[Any] | None], list[int]] = intInnit
		The function to test. Should accept a sequence of integer-compatible values,
		an optional parameter name string, and an optional parameter type.
		Returns a list of validated integers.

	Returns
	-------
	listOfTestFunctions : list[tuple[str, Callable[[], None]]]
		A list of tuples containing a string describing the test case and a callable
		test function implementing the test case.

	Examples
	--------
	Run tests on `Z0Z_tools.intInnit`:
	```python
	from Z0Z_tools.pytestForYourUse import PytestFor_intInnit

	listOfTests = PytestFor_intInnit()
	for nameOfTest, callablePytest in listOfTests:
		callablePytest()
	```

	Run tests on your compatible function:
	```python
	from Z0Z_tools.pytestForYourUse import PytestFor_intInnit
	from packageLocal import functionLocal

	@pytest.mark.parametrize("nameOfTest,callablePytest",
		PytestFor_intInnit(callableToTest=functionLocal))
	def test_functionLocal(nameOfTest, callablePytest):
		callablePytest()
	```

	"""
	def testHandlesValidIntegers() -> None:
		assert callableToTest([2, 3, 5, 8], 'test', None) == [2, 3, 5, 8]
		assert callableToTest([13.0, 21.0, 34.0], 'test', None) == [13, 21, 34] # pyright: ignore[reportArgumentType]
		assert callableToTest(['55', '89', '144'], 'test', None) == [55, 89, 144] # pyright: ignore[reportArgumentType]
		assert callableToTest([' 233 ', '377', '-610'], 'test', None) == [233, 377, -610] # pyright: ignore[reportArgumentType]

	def testRejectsNonWholeNumbers() -> None:
		listInvalidNumbers: list[float] = [13.7, 21.5, 34.8, -55.9]
		for invalidNumber in listInvalidNumbers:
			with pytest.raises(ValueError):  # noqa: PT011
				callableToTest([invalidNumber], 'test', None) # pyright: ignore[reportArgumentType]

	def testRejectsBooleans() -> None:
		with pytest.raises(TypeError):
			callableToTest([True, False], 'test', None)

	def testRejectsInvalidStrings() -> None:
		for invalidString in ['NW', '', ' ', 'SE.SW']:
			with pytest.raises(ValueError):  # noqa: PT011
				callableToTest([invalidString], 'test', None) # pyright: ignore[reportArgumentType]

	def testRejectsEmptyList() -> None:
		with pytest.raises(ValueError):  # noqa: PT011
			callableToTest([], 'test', None)

	def testHandlesMixedValidTypes() -> None:
		assert callableToTest([13, '21', 34.0], 'test', None) == [13, 21, 34] # pyright: ignore[reportArgumentType]

	def testHandlesBytes() -> None:
		validCases: list[tuple[list[bytes], str, list[int]]] = [
			([b'123'], '123', [123]),
		]
		for inputData, testName, expected in validCases:
			assert callableToTest(inputData, testName, None) == expected # pyright: ignore[reportArgumentType]

		extendedCases: list[tuple[list[bytes], str, list[int]]] = [
			([b'123456789'], '123456789', [123456789]),
		]
		for inputData, testName, expected in extendedCases:
			assert callableToTest(inputData, testName, None) == expected # pyright: ignore[reportArgumentType]

		invalidCases: list[list[bytes]] = [[b'\x00']]
		for inputData in invalidCases:
			with pytest.raises(ValueError):  # noqa: PT011
				callableToTest(inputData, 'test', None) # pyright: ignore[reportArgumentType]

	def testHandlesMemoryview() -> None:
		validCases: list[tuple[list[memoryview], str, list[int]]] = [
			([memoryview(b'123')], '123', [123]),
		]
		for inputData, testName, expected in validCases:
			assert callableToTest(inputData, testName, None) == expected # pyright: ignore[reportArgumentType]

		largeMemoryviewCase: list[memoryview] = [memoryview(b'9999999999')]
		assert callableToTest(largeMemoryviewCase, 'test', None) == [9999999999] # pyright: ignore[reportArgumentType]

		invalidMemoryviewCases: list[list[memoryview]] = [[memoryview(b'\x00')]]
		for inputData in invalidMemoryviewCases:
			with pytest.raises(ValueError):  # noqa: PT011
				callableToTest(inputData, 'test', None) # pyright: ignore[reportArgumentType]

	def testRejectsMutableSequence() -> None:
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
			assert callableToTest(inputData, 'test', None) == expected # pyright: ignore[reportArgumentType]

	def testRejectsInvalidComplex() -> None:
		for invalidComplex in [13+1j, 21+0.5j, 34.5+0j]:
			with pytest.raises(ValueError):  # noqa: PT011
				callableToTest([invalidComplex], 'test', None) # pyright: ignore[reportArgumentType]

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

def PytestFor_oopsieKwargsie(callableToTest: Callable[[str], bool | None | str] = oopsieKwargsie) -> list[tuple[str, Callable[[], None]]]:  # noqa: C901
	"""Return a list of test functions to validate string-to-boolean/None conversion behavior.

	This function provides a comprehensive test suite for validating string parsing and conversion
	to boolean or None values, with fallback to the original string when appropriate.

	Parameters
	----------
	callableToTest : Callable[[str], bool | None | str] = oopsieKwargsie
		The function to test, which should accept a string and return either a boolean, None,
		or the original input.

	Returns
	-------
	listOfTestFunctions : list[tuple[str, Callable[[], None]]]
		A list of tuples, each containing a string describing the test case and a callable
		test function that implements the test case.

	Examples
	--------
	Run each test on `Z0Z_tools.oopsieKwargsie`:
	```python
	from Z0Z_tools.pytestForYourUse import PytestFor_oopsieKwargsie

	listOfTests = PytestFor_oopsieKwargsie()
	for nameOfTest, callablePytest in listOfTests:
		callablePytest()
	```

	Or, run each test on your function that has a compatible signature:
	```python
	from Z0Z_tools.pytestForYourUse import PytestFor_oopsieKwargsie
	from packageLocal import functionLocal

	@pytest.mark.parametrize("nameOfTest,callablePytest", PytestFor_oopsieKwargsie(callableToTest=functionLocal))
	def test_functionLocal(nameOfTest, callablePytest):
		callablePytest()
	```

	"""
	def testHandlesTrueVariants() -> None:
		for variantTrue in ['True', 'TRUE', ' true ', 'TrUe']:
			assert callableToTest(variantTrue) is True

	def testHandlesFalseVariants() -> None:
		for variantFalse in ['False', 'FALSE', ' false ', 'FaLsE']:
			assert callableToTest(variantFalse) is False

	def testHandlesNoneVariants() -> None:
		for variantNone in ['None', 'NONE', ' none ', 'NoNe']:
			assert callableToTest(variantNone) is None

	def testReturnsOriginalString() -> None:
		for stringInput in ['hello', '123', 'True story', 'False alarm']:
			assert callableToTest(stringInput) == stringInput

	def testHandlesNonStringObjects() -> None:
		class UnStringable:
			def __str__(self) -> NoReturn:
				message = "Cannot be stringified"
				raise TypeError(message)

		assert callableToTest(123) == "123" # pyright: ignore[reportArgumentType]

		unStringableObject = UnStringable()
		result = callableToTest(unStringableObject) # pyright: ignore[reportArgumentType]
		assert result is unStringableObject

	return [
		('testHandlesTrueVariants', testHandlesTrueVariants),
		('testHandlesFalseVariants', testHandlesFalseVariants),
		('testHandlesNoneVariants', testHandlesNoneVariants),
		('testReturnsOriginalString', testReturnsOriginalString),
		('testHandlesNonStringObjects', testHandlesNonStringObjects)
	]
