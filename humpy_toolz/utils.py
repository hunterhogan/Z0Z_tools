# noqa: D100
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from collections.abc import Callable
	from typing import Literal

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
