"""Every example in the docstrings of each module is a reference; `doctest` runs them, and none may fail.

`humpy_cytoolz/__init__.py` re-exports its functions without examples of its own, so it is not a member. Examples marked
`+SKIP` print a `dict` whose order or a `set` whose repr `doctest` cannot compare; the test modules assert those values.
"""
from __future__ import annotations

from humpy_cytoolz.tests import assertEqualTo
from typing import TYPE_CHECKING
import doctest
import humpy_cytoolz.curried
import humpy_cytoolz.dicttoolz
import humpy_cytoolz.functoolz
import humpy_cytoolz.itertoolz
import humpy_cytoolz.recipes
import pytest

if TYPE_CHECKING:
	from types import ModuleType

@pytest.mark.parametrize('module', (
	humpy_cytoolz.curried, humpy_cytoolz.dicttoolz, humpy_cytoolz.functoolz, humpy_cytoolz.itertoolz, humpy_cytoolz.recipes,
), ids=('curried', 'dicttoolz', 'functoolz', 'itertoolz', 'recipes'))
def test_doctest(module: ModuleType) -> None:
	testResults: doctest.TestResults = doctest.testmod(module)
	assertEqualTo((testResults.failed, 0 < testResults.attempted), (0, True), doctest.testmod.__name__, module)
