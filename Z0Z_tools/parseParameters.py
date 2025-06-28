"""Provides parameter and input validation, integer parsing, and concurrency handling utilities."""
from collections.abc import Iterable, Sized
from dataclasses import dataclass
from typing import Any
import charset_normalizer
import multiprocessing

@dataclass
class ErrorMessageContext:
	"""Context information for constructing error messages.

	(AI generated docstring)

	Parameters
	----------
	parameterValue : Any = None
		(parameter2value) The value that caused the error.
	parameterValueType : str | None = None
		(parameter2value2type) The type name of the parameter value.
	containerType : str | None = None
		(container2type) The type name of the container holding the parameter.
	isElement : bool = False
		(is2element) Whether the parameter is an element within a container.

	"""

	parameterValue: Any = None
	parameterValueType: str | None = None
	containerType: str | None = None
	isElement: bool = False

def _constructErrorMessage(context: ErrorMessageContext, parameterName: str, parameterType: type[Any] | None) -> str:
	"""Construct error message from available context using template.

	I received ["value" | a value | `None`] [of type `type` | `None`] [as an element in | `None`] [a `containerType` type | `None`] but `parameterName` must have integers [in type(s) `parameterType` | `None`].

	Hypothetically, this is a prototype that can be generalized to other functions. In this package and a few of my other
	packages, I have developed standardized error messages, but those are quite different from this. I will certainly continue to
	develop this kind of functionality, and this function will influence things.

	Parameters
	----------
	context : ErrorMessageContext
		(context) The error context containing parameter value, type, and container information.
	parameterName : str
		(parameter2name) The name of the parameter that caused the error.
	parameterType : type[Any] | None
		(parameter2type) The expected type of the parameter, used in error messages.

	Returns
	-------
	errorMessage : str
		(error2message) The constructed error message string.

	"""
	messageParts = ["I received "]

	if context.parameterValue is not None and not isinstance(context.parameterValue, (bytes, bytearray, memoryview)):
		messageParts.append(f'"{context.parameterValue}"')
	else:
		messageParts.append("a value")

	if context.parameterValueType:
		messageParts.append(f" of type `{context.parameterValueType}`")

	if context.isElement:
		messageParts.append(" as an element in")

	if context.containerType:
		messageParts.append(f" a `{context.containerType}` type")

	messageParts.append(f" but {parameterName} must have integers")

	if parameterType:
		messageParts.append(f" in type(s) `{parameterType}`")

	return "".join(messageParts)

def defineConcurrencyLimit(*, limit: bool | float | int | None, cpuTotal: int = multiprocessing.cpu_count()) -> int:  # noqa: C901, PYI041
	"""Determine the concurrency limit based on the provided parameter.

	This package has Pytest tests you can import and run on this function. `from Z0Z_tools.pytest_parseParameters import makeTestSuiteConcurrencyLimit`

	Parameters
	----------
	limit : bool | float | int | None
		Whether and how to limit CPU usage. Accepts `True`/`False`, an integer count, or a fraction of total CPUs. Positive and
		negative values have different behaviors, see code for details.
	cpuTotal : int = multiprocessing.cpu_count()
		The total number of CPUs available in the system. Default is `multiprocessing.cpu_count()`.

	Returns
	-------
	concurrencyLimit : int
		(concurrency2limit) The calculated concurrency limit, ensuring it is at least 1.

	Notes
	-----
	If you want to be extra nice to your users, consider using `Z0Z_tools.oopsieKwargsie()` to handle
	malformed inputs. For example:

	```
	if not (CPUlimit is None or isinstance(CPUlimit, (bool, int, float))):
		CPUlimit = oopsieKwargsie(CPUlimit)
	```

	Examples
	--------
	Example parameters:
		CPUlimit: bool | float | int | None
		CPUlimit: bool | float | int | None = None

	Example docstring:
		```python

		Arguments:
			CPUlimit: bool | float | int | None
				whether and how to limit the CPU usage. See notes for details.

		Limits on CPU usage `CPUlimit`:
			- `False`, `None`, or `0`: No limits on CPU usage; uses all available CPUs. All other values will potentially limit CPU usage.
			- `True`: Yes, limit the CPU usage; limits to 1 CPU.
			- Integer `>= 1`: Limits usage to the specified number of CPUs.
			- Decimal value (`float`) between 0 and 1: Fraction of total CPUs to use.
			- Decimal value (`float`) between -1 and 0: Fraction of CPUs to *not* use.
			- Integer `<= -1`: Subtract the absolute value from total CPUs.
		```

	"""
	concurrencyLimit = cpuTotal

	if isinstance(limit, str):
		limitFromString = oopsieKwargsie(limit)
		if isinstance(limitFromString, str):
			try:
				limit = float(limitFromString)
			except ValueError:
				message = f"I received '{limitFromString}', but it must be a number, True, False, or None."
				raise ValueError(message)
		else:
			limit = limitFromString
	if isinstance(limit, float) and abs(limit) >= 1:
		limit = round(limit)
	match limit:
		case None | False | 0:
			pass
		case True:
			concurrencyLimit = 1
		case _ if limit >= 1:
			concurrencyLimit = int(limit)
		case _ if 0 < limit < 1:
			concurrencyLimit = round(limit * cpuTotal)
		case _ if -1 < limit < 0:
			concurrencyLimit = cpuTotal - abs(round(limit * cpuTotal))
		case _ if limit <= -1:
			concurrencyLimit = cpuTotal - abs(int(limit))
		case _:
			pass

	return max(int(concurrencyLimit), 1)

def intInnit(listInt_Allegedly: Iterable[Any], parameterName: str | None = None, parameterType: type[Any] | None = None) -> list[int]:  # noqa: C901, PLR0912, PLR0915
	"""Validate and convert input values to a `list` of integers.

	Accepts various numeric types and attempts to convert them into integers while providing descriptive error messages.

	Parameters
	----------
	listInt_Allegedly : Iterable[Any]
		(list2int2allegedly) The input sequence that should contain integer-compatible values.
		Accepts integers, strings, floats, complex numbers, and binary data.
		Rejects boolean values and non-integer numeric values.
	parameterName : str | None = None
		(parameter2name) Name of the parameter from your function for which this function is validating the input validated. If there is an error message, it provides context to your user. Defaults to 'the parameter'.
	parameterType : type[Any] | None = None
		(parameter2type) Expected type(s) of the parameter, used in error messages.

	Returns
	-------
	listValidated : list[int]
		(list2validated) A `list` containing validated integers.

	Raises
	------
	ValueError
		When the input is empty or contains non-integer compatible values.
	TypeError
		When an element is a boolean or incompatible type.
	RuntimeError
		If the input sequence length changes during iteration.

	Notes
	-----
	This package includes Pytest tests that can be imported and run:
	`from Z0Z_tools.pytest_parseParameters import makeTestSuiteIntInnit`

	The function performs strict validation and follows fail-early principles to catch potential issues before they become catastrophic.

	"""
	parameterName = parameterName or 'the parameter'
	parameterType = parameterType or list

	if not listInt_Allegedly:
		message = f"I did not receive a value for {parameterName}, but it is required."
		raise ValueError(message)

	# Be nice: assume the input container is valid and every element is valid.  # noqa: ERA001
	# Nevertheless, this is a "fail-early" step, so reject ambiguity and try to induce errors now that could be catastrophic later.
	try:
		iter(listInt_Allegedly)
		lengthInitial = None
		if isinstance(listInt_Allegedly, Sized):
			lengthInitial = len(listInt_Allegedly)

		listValidated: list[int] = []

		for allegedInt in listInt_Allegedly:
# ruff: noqa: PLW2901
			errorMessageContext = ErrorMessageContext(
				parameterValue = allegedInt,
				parameterValueType = type(allegedInt).__name__,
				isElement = True
			)

			# Always rejected as ambiguous
			if isinstance(allegedInt, bool):
				raise TypeError(errorMessageContext)

			# In this section, we know the Python type is not `int`, but maybe the value is clearly an integer.
			# Through a series of conversions, allow data to cascade down into either an `int` or a meaningful error message.

			if isinstance(allegedInt, (bytes, bytearray, memoryview)):
				errorMessageContext.parameterValue = None  # Don't expose potentially garbled binary data in error messages
				if isinstance(allegedInt, memoryview):
					allegedInt = allegedInt.tobytes()
				decodedString = charset_normalizer.from_bytes(allegedInt).best()
				if not decodedString:
					raise ValueError(errorMessageContext)
				allegedInt = errorMessageContext.parameterValue = str(decodedString)

			if isinstance(allegedInt, complex):
				if allegedInt.imag != 0:
					raise ValueError(errorMessageContext)
				allegedInt = float(allegedInt.real)
			elif isinstance(allegedInt, str):
				allegedInt = float(allegedInt.strip())

			if isinstance(allegedInt, float):
				if not float(allegedInt).is_integer():
					raise ValueError(errorMessageContext)
				allegedInt = int(allegedInt)
			else:
				allegedInt = int(allegedInt)

			listValidated.append(allegedInt)

			if lengthInitial is not None and isinstance(listInt_Allegedly, Sized) and len(listInt_Allegedly) != lengthInitial:
				raise RuntimeError((lengthInitial, len(listInt_Allegedly)))

		return listValidated

	except (TypeError, ValueError) as ERRORmessage:
		if isinstance(ERRORmessage.args[0], ErrorMessageContext):
			context = ERRORmessage.args[0]
			if not context.containerType:
				context.containerType = type(listInt_Allegedly).__name__
			message = _constructErrorMessage(context, parameterName, parameterType)
			raise type(ERRORmessage)(message) from None
		# If it's not our Exception, don't molest it
		raise

	except RuntimeError as ERRORruntime:
		lengthInitial, lengthCurrent = ERRORruntime.args[0]
		ERRORmessage = (
			f"The input sequence {parameterName} was modified during iteration. "
			f"Initial length {lengthInitial}, current length {lengthCurrent}."
		)
		raise RuntimeError(
			ERRORmessage
		) from None

def oopsieKwargsie(huh: Any) -> bool | None | str:
	"""Interpret a `str` as `True`, `False`, or `None` to avoid an `Exception`.

	If a calling function passes a `str` to a parameter that shouldn't receive a `str`, `oopsieKwargsie()` might help you avoid an `Exception`. It tries to interpret the string as `True`, `False`, or `None`. This package has Pytest tests you can import and run on this function.
	`from Z0Z_tools.pytest_parseParameters import makeTestSuiteOopsieKwargsie`

	Parameters
	----------
	huh : Any
		(huh) The input string to be parsed.

	Returns
	-------
	interpretedValue : bool | None | str
		(interpreted2value) The reserved keyword `True`, `False`, or `None` or the original string, `huh`.

	"""
	if not isinstance(huh, str):
		try:
			huh = str(huh)
		except BaseException:  # noqa: BLE001
			return huh
	formatted = huh.strip().title()
	if formatted == str(True):
		return True
	if formatted == str(False):
		return False
	if formatted == str(None):
		return None
	return huh

if __name__ == '__main__':
	# Frankly, I cannot remember the precise reason I put this in some modules. It solved a concurrency problem I was having at the time,
	# but it felt like a hack at the time and it feels even more like a hack now. I suspect I will eventually learn enough so that I can
	# come full circle: know why I added it, know how I already fixed the real issue, and know that I can safely remove this.  # noqa: ERA001
	multiprocessing.set_start_method('spawn')

	# Well, actually, I don't want to be programming for so long that I learn that much. I want to heal and do things in my areas of competency.
