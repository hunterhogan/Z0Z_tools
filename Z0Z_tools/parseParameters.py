"""
Provides parameter and input validation, integer parsing, and concurrency handling utilities.
"""
from collections.abc import Iterable, Sized
from dataclasses import dataclass
from typing import Any
import charset_normalizer
import multiprocessing

@dataclass
class ErrorMessageContext:
	parameterValue: Any = None
	parameterValueType: str | None = None
	containerType: str | None = None
	isElement: bool = False

def _constructErrorMessage(context: ErrorMessageContext, parameterName: str, parameterType: type[Any] | None) -> str:
	"""Constructs error message from available context using template:
	I received ["value" | a value | None] [of type `type` | None] [as an element in | None] [a `containerType` type | None] but `parameterName` must have integers [in type(s) `parameterType` | None].

	Hypothetically, this is a prototype that can be generalized to other functions. In this package and a few of my other packages, I have developed standardized error messages, but those are quite different from this. I will certainly continue to develop this kind of functionality, and this function will influence things.
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

# NOTE: For the `limit` parameter, the most precise type is `Union[bool, float, int, None]`
# because `None` is in fact a valid option for the parameter, which is why I'm not using `Optional[Union[int, float, bool]]`.
def defineConcurrencyLimit(limit: bool | float | int | None) -> int:
	"""
	Determines the concurrency limit based on the provided parameter. This package has Pytest tests you can import and run on this function. `from Z0Z_tools.pytest_parseParameters import makeTestSuiteConcurrencyLimit`

	Parameters:
		limit: Whether and how to limit CPU usage. Accepts True/False, an integer count, or a fraction of total CPUs.
				Positive and negative values have different behaviors, see code for details.

	Returns:
		concurrencyLimit: The calculated concurrency limit, ensuring it is at least 1.

	Notes:
		If you want to be extra nice to your users, consider using `Z0Z_tools.oopsieKwargsie()` to handle
	malformed inputs. For example:

	```
	if not (CPUlimit is None or isinstance(CPUlimit, (bool, int, float))):
		CPUlimit = oopsieKwargsie(CPUlimit)
	```

	Example parameter:
		from typing import Optional, Union
		CPUlimit: Optional[Union[int, float, bool]] = None

	Example parameter:
		from typing import Union
		CPUlimit: Union[bool, float, int, None]

	Example docstring:

	Parameters:
		CPUlimit: whether and how to limit the CPU usage. See notes for details.

	Limits on CPU usage `CPUlimit`:
		- `False`, `None`, or `0`: No limits on CPU usage; uses all available CPUs. All other values will potentially limit CPU usage.
		- `True`: Yes, limit the CPU usage; limits to 1 CPU.
		- Integer `>= 1`: Limits usage to the specified number of CPUs.
		- Decimal value (`float`) between 0 and 1: Fraction of total CPUs to use.
		- Decimal value (`float`) between -1 and 0: Fraction of CPUs to *not* use.
		- Integer `<= -1`: Subtract the absolute value from total CPUs.
	"""
	cpuTotal = multiprocessing.cpu_count()
	concurrencyLimit = cpuTotal

	if isinstance(limit, str):
		limitFromString = oopsieKwargsie(limit) # type: ignore
		if isinstance(limitFromString, str):
			try:
				limit = float(limitFromString)
			except ValueError:
				raise ValueError(f"I received '{limitFromString}', but it must be a number, True, False, or None.")
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
		case _: pass # To placate Pylance "strict" erroneously saying not all int or float are covered.

	return max(int(concurrencyLimit), 1)

def intInnit(listInt_Allegedly: Iterable[Any], parameterName: str | None = None, parameterType: type[Any] | None = None) -> list[int]:
	"""
	Validates and converts input values to a list of integers.

	Accepts various numeric types and attempts to convert them into integers while providing descriptive error messages.

	Parameters
		listInt_Allegedly: The input sequence that should contain integer-compatible values.
			Accepts integers, strings, floats, complex numbers, and binary data.
			Rejects boolean values and non-integer numeric values.

		parameterName ('the parameter'): Name of the parameter from your function for which this function is validating the input validated: if there is an error message, it provides context to your user. Defaults to 'the parameter'.

		parameterType: Expected type(s) of the parameter, used in error messages.

	Returns
		A list containing validated integers.

	Raises
		ValueError: When the input is empty or contains non-integer compatible values.
		TypeError: When an element is a boolean or incompatible type.
		RuntimeError: If the input sequence length changes during iteration.

	Notes
		This package includes Pytest tests that can be imported and run:
		`from Z0Z_tools.pytest_parseParameters import makeTestSuiteIntInnit`

		The function performs strict validation and follows fail-early principles to catch potential issues before they become catastrophic.
	"""
	parameterName = parameterName or 'the parameter'
	parameterType = parameterType or list

	if not listInt_Allegedly:
		raise ValueError(f"I did not receive a value for {parameterName}, but it is required.")

	# Be nice: assume the input container is valid and every element is valid.
	# Nevertheless, this is a "fail-early" step, so reject ambiguity and try to induce errors now that could be catastrophic later.
	# And, be helpful: provide a meaningful error message so the user can correct the issue.
	try:
		iter(listInt_Allegedly)
		lengthInitial = None
		if isinstance(listInt_Allegedly, Sized):
			lengthInitial = len(listInt_Allegedly)

		listValidated: list[int] = []

		for allegedInt in listInt_Allegedly:
			errorMessageContext = ErrorMessageContext(
				parameterValue = allegedInt,
				parameterValueType = type(allegedInt).__name__,
				isElement = True
			)

			# Always rejected
			if isinstance(allegedInt, bool):
				raise TypeError(errorMessageContext)

			# The Python type is not `int`, but maybe the value is clearly an integer.
			# Through a series of conversions, allow data to cascade down into either an `int` or a meaningful error message.

			if isinstance(allegedInt, (bytes, bytearray, memoryview)):
				errorMessageContext.parameterValue = None  # Don't expose binary data in error messages
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

			if lengthInitial is not None and isinstance(listInt_Allegedly, Sized):
				if len(listInt_Allegedly) != lengthInitial:
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
		raise RuntimeError(
			f"The input sequence {parameterName} was modified during iteration. "
			f"Initial length {lengthInitial}, current length {lengthCurrent}."
		) from None

def oopsieKwargsie(huh: Any) -> bool | None | str:
	"""
	If a calling function passes a `str` to a parameter that shouldn't receive a `str`, `oopsieKwargsie()` might help you avoid an Exception. It tries to interpret the string as `True`, `False`, or `None`. This package has Pytest tests you can import and run on this function. `from Z0Z_tools.pytest_parseParameters import makeTestSuiteOopsieKwargsie`

	Parameters:
		huh: The input string to be parsed.

	Returns:
		(bool | None | str): The reserved keywords `True`, `False`, or `None` or the original string, `huh`.
	"""
	if not isinstance(huh, str):
		try:
			huh = str(huh)
		except Exception:
			return huh
	formatted = huh.strip().title()
	if formatted == str(True):
		return True
	elif formatted == str(False):
		return False
	elif formatted == str(None):
		return None
	else:
		return huh

if __name__ == '__main__':
	# Frankly, I cannot remember the precise reason I put this in some modules. It solved the concurrency problem I was having at the time,
	# but it felt like a hack at the time and it feels even more like a hack now. I suspect I will eventually learn enough so that I can
	# come full circle: know why I added it, know how I already fixed the real issue, and know that I can safely remove this.
	multiprocessing.set_start_method('spawn')

	# Well, actually, I don't want to be programming for so long that I learn that much. I want to heal and do things in my areas of competency.
