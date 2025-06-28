"""Utility functions for handling `None` values and coping with common programming patterns.

(AI generated docstring)

This module provides helper functions for defensive programming and error handling, particularly for dealing with `None` values that should not occur in correct program flow.

"""
from typing import TypeVar

TypeSansNone = TypeVar('TypeSansNone')

def raiseIfNone(returnTarget: TypeSansNone | None, errorMessage: str | None = None) -> TypeSansNone:
	"""Raise a `ValueError` if the target value is `None`, otherwise return the value: tell the type checker that the return value is not `None`.

	(AI generated docstring)

	This is a defensive programming function that converts unexpected `None` values into explicit errors with context. It is useful for asserting that functions that might return `None` have actually returned a meaningful value.

	Parameters
	----------
	returnTarget : TypeSansNone | None
		The value to check for `None`. If not `None`, this value is returned unchanged.
	errorMessage : str | None = None
		Custom error message to include in the `ValueError`. If `None`, a default message with debugging hints is used.

	Returns
	-------
	returnTarget : TypeSansNone
		The original `returnTarget` value, guaranteed to not be `None`.

	Raises
	------
	ValueError
		If `returnTarget` is `None`.

	Examples
	--------
	Ensure a function result is not `None`:

	```python
	def findFirstMatch(listItems: list[str], pattern: str) -> str | None:
		for item in listItems:
			if pattern in item:
				return item
		return None

	listFiles = ['document.txt', 'image.png', 'data.csv']
	filename = raiseIfNone(findFirstMatch(listFiles, '.txt'))
	# Returns 'document.txt'
	```

	Handle dictionary lookups with custom error messages:

	```python
	configurationMapping = {'host': 'localhost', 'port': 8080}
	host = raiseIfNone(configurationMapping.get('host'),
					"Configuration must include 'host' setting")
	# Returns 'localhost'

	# This would raise ValueError with custom message:
	# database = raiseIfNone(configurationMapping.get('database'),
	#                       "Configuration must include 'database' setting")
	```

	Thanks
	------
	sobolevn, https://github.com/sobolevn, for the seed of the function. https://github.com/python/typing/discussions/1997#discussioncomment-13108399

	"""
	if returnTarget is None:
		message = errorMessage or 'A function unexpectedly returned `None`. Hint: look at the traceback immediately before `raiseIfNone`.'
		raise ValueError(message)
	return returnTarget
