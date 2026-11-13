"""Small functions that the `humpy_cytoolz` docstrings use in their examples, as named functions instead of lambdas."""
from __future__ import annotations

from humpy_cytoolz.functoolz import curry

def isEven(integer: int) -> bool:
	"""Return `True` when `integer` is divisible by two."""
	return integer % 2 == 0

def addToSet[个](setAccumulated: set[个], item: 个) -> set[个]:
	"""Add `item` to `setAccumulated` and return `setAccumulated`, as the `reduceby` docstring's `set_add` does."""
	setAccumulated.add(item)
	return setAccumulated

def pairAccumulated[个, 文义](accumulated: 个, item: 文义) -> tuple[个, 文义]:
	"""Return `(accumulated, item)`, so the result of a reduction records every step and its order."""
	return (accumulated, item)

def keyEvenValueLessThan4吗(item: tuple[int, int]) -> bool:
	"""Whether the key of `item` is even and its value is less than 4, as the `itemfilter` docstring's `isvalid` asks."""
	return item[0] % 2 == 0 and item[1] < 4

def scaleSum(x: int, y: int, a: int = 10) -> int:
	"""Return `a * (x + y)`, as the `curry` docstring's `f` does."""
	return a * (x + y)

@curry
def addCurried(augend: int, addend: int) -> int:
	"""Return `augend + addend`; a module-level function that `curry` decorates, so `pickle` finds it by its qualified name."""
	return augend + addend

def keyIgnoresKeywords(args: tuple[object, ...], kwargs: dict[str, object]) -> tuple[object, ...]:
	"""Return `args`: the `memoize` docstring's key function that ignores extraneous keyword arguments."""
	return args
