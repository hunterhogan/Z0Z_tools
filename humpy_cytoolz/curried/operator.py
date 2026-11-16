# ruff:ignore[undocumented-public-module]
from __future__ import annotations

from humpy_cytoolz.dicttoolz import keyfilter, valfilter, valmap
from humpy_cytoolz.functoolz import complement, curry
from typing import TYPE_CHECKING
import operator

if TYPE_CHECKING:
	from collections.abc import Callable

boxOf_operatorNotCurried: set[str] = {
	'__abs__', '__index__', '__inv__', '__invert__', '__neg__', '__not__', '__pos__', '_abs', 'abs', 'attrgetter', 'index', 'inv',
	'invert', 'is_none', 'is_not_none', 'itemgetter', 'neg', 'not_', 'pos', 'truth',
}

lookupOperator: dict[str, Callable[..., object]] = valfilter(callable, vars(operator))
locals().update(lookupOperator)
locals().update(valmap(curry, keyfilter(complement(boxOf_operatorNotCurried.__contains__), lookupOperator)))

del complement, curry, keyfilter, lookupOperator, operator, TYPE_CHECKING, valfilter, valmap
