"""Expected values come from the targets' docstrings unless a comment names another basis."""
from __future__ import annotations

from humpy_cytoolz.tests import assertEqualTo, messageTestFailure
from humpy_cytoolz.utils import consume, include_dirs, no_default, raises
from pathlib import Path
import functools
import importlib.resources
import more_itertools
import pytest

# Reference: the README states that functions with matching maintained implementations are aliases.
def test_consume() -> None:
	assertEqualTo(consume, more_itertools.consume, 'humpy_cytoolz.utils', consume)

# Reference: `itertoolz.pyi` declares `no_default` as `Literal['__no__default__']`.
def test_no_default() -> None:
	assertEqualTo((no_default, type(no_default)), ('__no__default__', str), 'humpy_cytoolz.utils', no_default)

@pytest.mark.parametrize('err, lamda, expected', (
	pytest.param(ZeroDivisionError, functools.partial((1).__truediv__, 0), True, id='ZeroDivisionError-divideBy0'),
	pytest.param(ZeroDivisionError, functools.partial((1).__truediv__, 13), False, id='ZeroDivisionError-divideBy13'),
	# Reference: `except err` accepts a tuple of exception types.
	pytest.param((KeyError, ZeroDivisionError), functools.partial((1).__truediv__, 0), True, id='tupleOfTypes-divideBy0'),
))
def test_raises(err: type[BaseException] | tuple[type[BaseException], ...], lamda: functools.partial[float], expected: bool) -> None:
	assert raises(err, lamda) is expected, messageTestFailure(raises(err, lamda), expected, raises.__name__, err, lamda)

# Relation: an exception of another type propagates, because `raises` catches only `err`.
def test_raisesError() -> None:
	with pytest.raises(ZeroDivisionError):
		raises(KeyError, functools.partial((1).__truediv__, 0))

# Reference: `importlib.resources.files` locates the installed package. The first directory contains the `humpy_cytoolz`
# directory, so `cimport humpy_cytoolz.itertoolz` finds `itertoolz.pxd` from it.
def test_include_dirs() -> None:
	assertEqualTo(Path(include_dirs()[0]), Path(str(importlib.resources.files('humpy_cytoolz'))).parent, include_dirs.__name__)
