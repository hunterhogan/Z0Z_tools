"""Provide utility functions, sentinel values, and structural `Protocol` types.

(AI generated docstring)

You can use this module to access shared utilities and type-checking protocols used across
`humpy_toolz`. The `raises` function supports test assertions. The `no_default` sentinel
distinguishes between 'no argument provided' and `None` as an explicit argument value. The
`Protocol` classes are copied from `_typeshed` [1] to provide structural type annotations
without a runtime dependency on that internal module.

Contents
--------
Functions
	raises
		Check whether calling a callable raises a specific exception type.

Variables
	no_default
		Sentinel that signals no default argument was provided.

Classes
	SupportsBool
		Protocol for objects implementing `__bool__`.
	SupportsDunderGT
		Protocol for objects implementing `__gt__`.
	SupportsDunderLT
		Protocol for objects implementing `__lt__`.
	SupportsGetItem
		Protocol for objects implementing `__getitem__`.

Type Aliases
	SupportsRichComparison
		Union of `SupportsDunderLT[Any]` and `SupportsDunderGT[Any]`.

References
----------
[1] _typeshed.__init__ - typeshed on GitHub
	https://github.com/python/typeshed/blob/main/stdlib/_typeshed/__init__.pyi
"""
from collections.abc import Callable
from typing import Any, Literal, Protocol, TypeVar

def raises(err: type[Exception], lamda: Callable[[], None]) -> bool:
	"""Check whether calling `lamda` raises `err`.

	(AI generated docstring)

	You can use `raises` in test assertions to verify that a callable raises a specific
	exception type. `raises` invokes `lamda` inside a `try` block and returns `True` if
	`lamda` raises `err`, or `False` if `lamda` returns normally.

	Parameters
	----------
	err : type[Exception]
		The exception type to check for.
	lamda : Callable[[], None]
		A zero-argument callable to invoke.

	Returns
	-------
	didRaise : bool
		`True` if `lamda` raised `err`, `False` if `lamda` returned without raising.

	Examples
	--------
	From `humpy_toolz.tests.test_utils`:

		```python
		from humpy_toolz.utils import raises

		assert raises(ZeroDivisionError, lambda: 1 / 0)
		assert not raises(ZeroDivisionError, lambda: 1)
		```
	"""
	try:
		lamda()
		return False  # noqa: TRY300
	except err:
		return True

no_default: Literal['__no__default__'] = '__no__default__'
"""Signal that no default argument was provided, distinct from `None`.

(AI generated docstring)

You can use `no_default` as the default value for optional parameters in functions that
must distinguish between 'no argument provided' and an explicit `None` argument. `no_default`
is typed as `Literal['__no__default__']` so that type checkers can distinguish calls that
pass `no_default` from calls that pass other values. The string value `'__no__default__'`
survives `pickle` [1] serialization, which enables safe use in parallel and distributed
contexts.

References
----------
[1] pickle - Python Standard Library
	https://docs.python.org/3/library/pickle.html
"""

_KT_contra = TypeVar("_KT_contra", contravariant=True)
_T_contra = TypeVar("_T_contra", contravariant=True)
_VT_co = TypeVar("_VT_co", covariant=True)

class SupportsBool(Protocol):
	"""Represent any object that supports truth-value testing via `__bool__`.

	(AI generated docstring)

	You can use `SupportsBool` as a type annotation for parameters or return values that
	require truth-value testing. `SupportsBool` is copied from `_typeshed` [1].

	References
	----------
	[1] _typeshed.__init__ - typeshed on GitHub
		https://github.com/python/typeshed/blob/main/stdlib/_typeshed/__init__.pyi
	"""
	def __bool__(self) -> bool:
		"""Return the truth value of the object."""
		...

class SupportsDunderLT(Protocol[_T_contra]):
	"""Represent any object that supports the less-than operator via `__lt__`.

	(AI generated docstring)

	You can use `SupportsDunderLT` as a type annotation for parameters or return values
	that must support the `<` comparison operator. `SupportsDunderLT` is copied from
	`_typeshed` [1].

	References
	----------
	[1] _typeshed.__init__ - typeshed on GitHub
		https://github.com/python/typeshed/blob/main/stdlib/_typeshed/__init__.pyi
	"""
	def __lt__(self, other: _T_contra, /) -> SupportsBool:
		"""Less-than comparison operator."""
		...

class SupportsDunderGT(Protocol[_T_contra]):
	"""Represent any object that supports the greater-than operator via `__gt__`.

	(AI generated docstring)

	You can use `SupportsDunderGT` as a type annotation for parameters or return values
	that must support the `>` comparison operator. `SupportsDunderGT` is copied from
	`_typeshed` [1].

	References
	----------
	[1] _typeshed.__init__ - typeshed on GitHub
		https://github.com/python/typeshed/blob/main/stdlib/_typeshed/__init__.pyi
	"""
	def __gt__(self, other: _T_contra, /) -> SupportsBool:
		"""Greater-than comparison operator."""
		...

class SupportsGetItem(Protocol[_KT_contra, _VT_co]):
	"""Represent any object that supports item access via `__getitem__`.

	(AI generated docstring)

	You can use `SupportsGetItem` as a type annotation for parameters or return values
	that support indexing with `[]`. `SupportsGetItem` is copied from `_typeshed` [1].

	References
	----------
	[1] _typeshed.__init__ - typeshed on GitHub
		https://github.com/python/typeshed/blob/main/stdlib/_typeshed/__init__.pyi
	"""
	def __getitem__(self, key: _KT_contra, /) -> _VT_co:
		"""Item access operator."""
		...

type SupportsRichComparison = SupportsDunderLT[Any] | SupportsDunderGT[Any]
"""Represent any object that supports rich comparison via `__lt__` or `__gt__`.

(AI generated docstring)

You can use `SupportsRichComparison` as a type annotation for objects that support the `<`
or `>` operators. `SupportsRichComparison` is copied from `_typeshed` [1].

See Also
--------
SupportsDunderLT : Protocol for objects implementing `__lt__`.
SupportsDunderGT : Protocol for objects implementing `__gt__`.

References
----------
[1] _typeshed.__init__ - typeshed on GitHub
	https://github.com/python/typeshed/blob/main/stdlib/_typeshed/__init__.pyi
"""
