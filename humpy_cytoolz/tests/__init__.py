"""Test the humpy_cytoolz package; cibuildwheel runs this package against each built wheel.

Test package organization (in humpy_cytoolz/tests/):
- conftest.py: Hooks that name the compiled modules under test and any that are older than their source
- dataSamples/: Samples whose meaning does not depend on a test, named by content
- test_curried.py: Which functions the curried namespace curries, and which it re-exports unchanged
- test_dicttoolz.py: Functions over mappings, for every kind of input mapping and every factory
- test_doctests.py: Every example in the modules' docstrings
- test_functoolz.py: Composition, currying, memoizing, and pickling function objects
- test_itertoolz.py: Functions over iterables, and the aliases of standard-library and `more_itertools` functions
- test_recipes.py: Counting and partitioning by a key function
- test_signatures.py: Introspection of signatures, which `curry` uses to decide whether to call
- test_utils.py: The sentinel, `raises`, and the location of the `.pxd` files
- typeAssertions_*.py: Static type assertions for type checkers; pytest does not collect them
"""
from __future__ import annotations

from hunterMakesPy.tests import assertEqualTo as assertEqualTo, messageTestFailure as messageTestFailure
