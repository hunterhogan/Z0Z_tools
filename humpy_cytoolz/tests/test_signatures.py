"""Expected values come from upstream toolz's test suite, which `humpy_cytoolz` keeps, unless a comment names another basis.

`is_valid_args` answers whether the arguments complete a valid call; `is_partial_args` answers whether more arguments
could complete one. `_signatures` binds with `inspect.Signature`, so `Signature.bind` is not an independent reference.
"""
from __future__ import annotations

from humpy_cytoolz._signatures import has_keywords, has_varargs, is_arity, is_partial_args, is_valid_args, num_required_args
from humpy_cytoolz.tests import messageTestFailure
from humpy_cytoolz.tests.dataSamples.signatures import (
	signatureABDefaultsCD, signatureArgs, signatureEmpty, signatureFuncDefaultNone, signatureKwargs, signatureLikePartial, signatureX,
	signatureXArgs, signatureXDefault1, signatureXKeywordOnly, signatureXPositionalOnly, signatureXYArgsKwargs, signatureXYDefault1Kwargs)
from typing import TYPE_CHECKING
import functools
import pytest
import sys

if TYPE_CHECKING:
	from _pytest.mark.structures import ParameterSet
	from collections.abc import Callable
	from typing import Any

reasonDefectBindPartial: str = ('`is_partial_args` asks `inspect.Signature.bind_partial`, which refuses a keyword named like a missing positional-only'
	' parameter even when `**keywords` would take it; `functools.partial` has such a signature from Python 3.13.')

parametersArguments: tuple[ParameterSet, ...] = (
	pytest.param(signatureEmpty, (), {}, True, True, id='signatureEmpty'),
	pytest.param(signatureEmpty, (1,), {}, False, False, id='signatureEmpty-1'),
	pytest.param(signatureEmpty, (), {'x': 1}, False, False, id='signatureEmpty-x'),
	pytest.param(signatureX, (), {}, False, True, id='signatureX'),
	pytest.param(signatureX, (1,), {}, True, True, id='signatureX-1'),
	pytest.param(signatureX, (), {'x': 1}, True, True, id='signatureX-x'),
	pytest.param(signatureX, (1,), {'x': 2}, False, False, id='signatureX-1-x'),
	pytest.param(signatureX, (1,), {'y': 2}, False, False, id='signatureX-1-y'),
	pytest.param(signatureX, (1, 2), {}, False, False, id='signatureX-1-2'),
	pytest.param(signatureX, (), {'x': 1, 'y': 2}, False, False, id='signatureX-x-y'),
	pytest.param(signatureXDefault1, (), {}, True, True, id='signatureXDefault1'),
	pytest.param(signatureXDefault1, (1,), {}, True, True, id='signatureXDefault1-1'),
	pytest.param(signatureXDefault1, (), {'x': 1}, True, True, id='signatureXDefault1-x'),
	pytest.param(signatureXDefault1, (1,), {'x': 2}, False, False, id='signatureXDefault1-1-x'),
	pytest.param(signatureXDefault1, (1,), {'y': 2}, False, False, id='signatureXDefault1-1-y'),
	pytest.param(signatureXDefault1, (1, 2), {}, False, False, id='signatureXDefault1-1-2'),
	pytest.param(signatureXDefault1, (), {'x': 1, 'y': 2}, False, False, id='signatureXDefault1-x-y'),
	pytest.param(signatureArgs, (), {}, True, True, id='signatureArgs'),
	pytest.param(signatureArgs, (1,), {}, True, True, id='signatureArgs-1'),
	pytest.param(signatureArgs, (1, 2), {}, True, True, id='signatureArgs-1-2'),
	pytest.param(signatureArgs, (), {'x': 1}, False, False, id='signatureArgs-x'),
	pytest.param(signatureKwargs, (), {}, True, True, id='signatureKwargs'),
	pytest.param(signatureKwargs, (), {'x': 1}, True, True, id='signatureKwargs-x'),
	pytest.param(signatureKwargs, (), {'x': 1, 'y': 2}, True, True, id='signatureKwargs-x-y'),
	pytest.param(signatureKwargs, (1,), {}, False, False, id='signatureKwargs-1'),
	pytest.param(signatureXArgs, (), {}, False, True, id='signatureXArgs'),
	pytest.param(signatureXArgs, (1,), {}, True, True, id='signatureXArgs-1'),
	pytest.param(signatureXArgs, (1, 2), {}, True, True, id='signatureXArgs-1-2'),
	pytest.param(signatureXArgs, (), {'x': 1}, True, True, id='signatureXArgs-x'),
	pytest.param(signatureXArgs, (1,), {'x': 1}, False, False, id='signatureXArgs-1-x'),
	pytest.param(signatureXArgs, (1,), {'y': 1}, False, False, id='signatureXArgs-1-y'),
	pytest.param(signatureXYDefault1Kwargs, (), {}, False, True, id='signatureXYDefault1Kwargs'),
	pytest.param(signatureXYDefault1Kwargs, (1,), {}, True, True, id='signatureXYDefault1Kwargs-1'),
	pytest.param(signatureXYDefault1Kwargs, (), {'x': 1}, True, True, id='signatureXYDefault1Kwargs-x'),
	pytest.param(signatureXYDefault1Kwargs, (1, 2), {}, True, True, id='signatureXYDefault1Kwargs-1-2'),
	pytest.param(signatureXYDefault1Kwargs, (), {'x': 1, 'y': 2, 'z': 3}, True, True, id='signatureXYDefault1Kwargs-x-y-z'),
	pytest.param(signatureXYDefault1Kwargs, (1, 2), {'y': 3}, False, False, id='signatureXYDefault1Kwargs-1-2-y'),
	pytest.param(signatureABDefaultsCD, (), {}, False, True, id='signatureABDefaultsCD'),
	pytest.param(signatureABDefaultsCD, (1,), {}, False, True, id='signatureABDefaultsCD-1'),
	pytest.param(signatureABDefaultsCD, (1, 2), {}, True, True, id='signatureABDefaultsCD-1-2'),
	pytest.param(signatureABDefaultsCD, (1,), {'c': 3}, False, True, id='signatureABDefaultsCD-1-c'),
	pytest.param(signatureABDefaultsCD, (1,), {'e': 3}, False, False, id='signatureABDefaultsCD-1-e'),
	pytest.param(signatureABDefaultsCD, (1, 2), {'e': 3}, False, False, id='signatureABDefaultsCD-1-2-e'),
	pytest.param(signatureABDefaultsCD, (1, 2), {'b': 3}, False, False, id='signatureABDefaultsCD-1-2-b'),
	pytest.param(signatureFuncDefaultNone, (), {}, True, True, id='signatureFuncDefaultNone'),
	pytest.param(signatureFuncDefaultNone, (None,), {}, True, True, id='signatureFuncDefaultNone-None'),
	pytest.param(signatureFuncDefaultNone, (), {'func': None}, True, True, id='signatureFuncDefaultNone-func'),
	pytest.param(signatureFuncDefaultNone, (None,), {'func': None}, False, False, id='signatureFuncDefaultNone-None-func'),
	# Reference: Python's rules for binding positional-only and keyword-only parameters.
	pytest.param(signatureXPositionalOnly, (), {}, False, True, id='signatureXPositionalOnly'),
	pytest.param(signatureXPositionalOnly, (1,), {}, True, True, id='signatureXPositionalOnly-1'),
	pytest.param(signatureXPositionalOnly, (), {'x': 1}, False, False, id='signatureXPositionalOnly-x'),
	pytest.param(signatureXKeywordOnly, (), {}, False, True, id='signatureXKeywordOnly'),
	pytest.param(signatureXKeywordOnly, (1,), {}, False, False, id='signatureXKeywordOnly-1'),
	pytest.param(signatureXKeywordOnly, (), {'x': 1}, True, True, id='signatureXKeywordOnly-x'),
	pytest.param(1, (), {}, False, False, id='notCallable'),
	# Builtins without introspectable signatures come from the signature registry in `_signatures`.
	pytest.param(abs, (), {}, False, True, id='abs'),
	pytest.param(abs, (1,), {}, True, True, id='abs-1'),
	pytest.param(abs, (), {'x': 1}, False, False, id='abs-x'),
	pytest.param(abs, (1, 2), {}, False, False, id='abs-1-2'),
	pytest.param(complex, (), {}, True, True, id='complex'),
	pytest.param(complex, (1,), {}, True, True, id='complex-1'),
	pytest.param(complex, (), {'real': 1}, True, True, id='complex-real'),
	pytest.param(complex, (1, 2), {}, True, True, id='complex-1-2'),
	pytest.param(complex, (1,), {'imag': 2}, True, True, id='complex-1-imag'),
	pytest.param(complex, (1,), {'real': 2}, False, False, id='complex-1-real'),
	pytest.param(complex, (1, 2, 3), {}, False, False, id='complex-1-2-3'),
	pytest.param(complex, (1, 2), {'imag': 3}, False, False, id='complex-1-2-imag'),
	pytest.param(int, (), {}, True, True, id='int'),
	pytest.param(int, (1,), {}, True, True, id='int-1'),
	pytest.param(int, (), {'x': 1}, True, True, id='int-x'),
	pytest.param(int, (1, 2), {}, True, True, id='int-1-2'),
	pytest.param(int, (1,), {'base': 2}, True, True, id='int-1-base'),
	pytest.param(int, (), {'x': 1, 'base': 2}, True, True, id='int-x-base'),
	pytest.param(int, (), {'base': 2}, False, True, id='int-base'),
	pytest.param(int, (1, 2, 3), {}, False, False, id='int-1-2-3'),
	pytest.param(map, (), {}, False, True, id='map'),
	pytest.param(map, (1,), {}, False, True, id='map-1'),
	pytest.param(map, (1, 2), {}, True, True, id='map-1-2'),
	pytest.param(map, (1, 2, 3), {}, True, True, id='map-1-2-3'),
	pytest.param(map, (1, 2, 3, 4), {}, True, True, id='map-1-2-3-4'),
	pytest.param(min, (), {}, False, True, id='min'),
	pytest.param(min, (1,), {}, True, True, id='min-1'),
	pytest.param(min, (), {'iterable': 1}, False, False, id='min-iterable'),
	pytest.param(min, (1, 2), {}, True, True, id='min-1-2'),
	pytest.param(min, (1, 2, 3), {}, True, True, id='min-1-2-3'),
	pytest.param(min, (), {'key': None}, False, True, id='min-key'),
	pytest.param(min, (1,), {'key': None}, True, True, id='min-1-key'),
	pytest.param(min, (1, 2), {'key': None}, True, True, id='min-1-2-key'),
	pytest.param(min, (1, 2, 3), {'key': None}, True, True, id='min-1-2-3-key'),
	pytest.param(min, (), {'key': None, 'default': None}, False, True, id='min-key-default'),
	pytest.param(min, (1,), {'key': None, 'default': None}, True, True, id='min-1-key-default'),
	pytest.param(min, (1, 2), {'key': None, 'default': None}, False, False, id='min-1-2-key-default'),
	pytest.param(min, (1, 2, 3), {'key': None, 'default': None}, False, False, id='min-1-2-3-key-default'),
	pytest.param(range, (), {}, False, True, id='range'),
	pytest.param(range, (1,), {}, True, True, id='range-1'),
	pytest.param(range, (1, 2), {}, True, True, id='range-1-2'),
	pytest.param(range, (1, 2, 3), {}, True, True, id='range-1-2-3'),
	pytest.param(range, (1, 2), {'step': 3}, False, False, id='range-1-2-step'),
	pytest.param(range, (1, 2, 3, 4), {}, False, False, id='range-1-2-3-4'),
	pytest.param(functools.partial, (), {}, False, True, id='partial'),
	pytest.param(functools.partial, (1,), {}, True, True, id='partial-1'),
	pytest.param(functools.partial, (1,), {'func': 1}, True, True, id='partial-1-func'),
	pytest.param(functools.partial, (1, 2), {}, True, True, id='partial-1-2'),
)

@pytest.mark.parametrize('func, args, kwargs, expected, isPartial', (
	*parametersArguments,
	pytest.param(functools.partial, (), {'func': 1}, False, True, id='partial-func'),
	pytest.param(signatureLikePartial, (), {'func': 1}, False, True, id='signatureLikePartial-func'),
))
def test_is_valid_args(func: Callable[..., Any], args: tuple[Any, ...], kwargs: dict[str, Any], expected: bool, isPartial: bool) -> None:
	assert is_valid_args(func, args, kwargs) is expected, messageTestFailure(is_valid_args(func, args, kwargs), expected, is_valid_args.__name__, func, args, kwargs)

@pytest.mark.parametrize('func, args, kwargs, isValid, expected', (
	*parametersArguments,
	pytest.param(functools.partial, (), {'func': 1}, False, True, id='partial-func', marks=pytest.mark.xfail(
		functools.partial.__text_signature__ is not None, strict=True, reason=reasonDefectBindPartial)),
	pytest.param(signatureLikePartial, (), {'func': 1}, False, True, id='signatureLikePartial-func', marks=pytest.mark.xfail(strict=True, reason=reasonDefectBindPartial)),
))
def test_is_partial_args(func: Callable[..., Any], args: tuple[Any, ...], kwargs: dict[str, Any], isValid: bool, expected: bool) -> None:
	assert is_partial_args(func, args, kwargs) is expected, messageTestFailure(is_partial_args(func, args, kwargs), expected, is_partial_args.__name__, func, args, kwargs)

@pytest.mark.parametrize('func, expected', (
	pytest.param(signatureEmpty, 0, id='signatureEmpty'),
	pytest.param(signatureX, 1, id='signatureX'),
	pytest.param(signatureXArgs, 1, id='signatureXArgs'),
	pytest.param(signatureXYDefault1Kwargs, 1, id='signatureXYDefault1Kwargs'),
	pytest.param(signatureXYArgsKwargs, 2, id='signatureXYArgsKwargs'),
	# Reference: upstream toolz's docstring counts required positional arguments, so a keyword-only parameter counts none.
	pytest.param(signatureXKeywordOnly, 0, id='signatureXKeywordOnly'),
	pytest.param(map, 2, id='map'),
	pytest.param(dict, None, id='dict'),
))
def test_num_required_args(func: Callable[..., Any], expected: int | None) -> None:
	assert num_required_args(func) == expected, messageTestFailure(num_required_args(func), expected, num_required_args.__name__, func)

@pytest.mark.parametrize('func, expected', (
	pytest.param(signatureEmpty, False, id='signatureEmpty'),
	pytest.param(signatureX, False, id='signatureX'),
	pytest.param(signatureXDefault1, True, id='signatureXDefault1'),
	pytest.param(signatureKwargs, True, id='signatureKwargs'),
	pytest.param(int, True, id='int'),
	pytest.param(sorted, True, id='sorted'),
	pytest.param(max, True, id='max'),
	# Reference: Python's documentation of `map`: the keyword-only `strict` is new in Python 3.14.
	pytest.param(map, True, id='map-python314', marks=pytest.mark.skipif(sys.version_info < (3, 14), reason='`map` has no keyword before Python 3.14.')),
	pytest.param(map, False, id='map-python313', marks=pytest.mark.skipif((3, 14) <= sys.version_info, reason='`map` has the keyword `strict` from Python 3.14.')),
	pytest.param(bytearray, None, id='bytearray'),
))
def test_has_keywords(func: Callable[..., Any], expected: bool | None) -> None:
	assert has_keywords(func) is expected, messageTestFailure(has_keywords(func), expected, has_keywords.__name__, func)

@pytest.mark.parametrize('func, expected', (
	pytest.param(signatureEmpty, False, id='signatureEmpty'),
	pytest.param(signatureArgs, True, id='signatureArgs'),
	pytest.param(signatureKwargs, False, id='signatureKwargs'),
	pytest.param(signatureXYArgsKwargs, True, id='signatureXYArgsKwargs'),
	pytest.param(map, True, id='map'),
	pytest.param(max, None, id='max'),
	pytest.param(1, False, id='notCallable'),
))
def test_has_varargs(func: Callable[..., Any], expected: bool | None) -> None:
	assert has_varargs(func) is expected, messageTestFailure(has_varargs(func), expected, has_varargs.__name__, func)

@pytest.mark.parametrize('n, func, expected', (
	pytest.param(0, signatureEmpty, True, id='0-signatureEmpty'),
	pytest.param(1, signatureEmpty, False, id='1-signatureEmpty'),
	pytest.param(1, signatureX, True, id='1-signatureX'),
	pytest.param(1, signatureXArgs, False, id='1-signatureXArgs'),
	pytest.param(1, all, True, id='1-all'),
	pytest.param(2, map, False, id='2-map'),
	pytest.param(2, range, None, id='2-range'),
))
def test_is_arity(n: int, func: Callable[..., Any], expected: bool | None) -> None:
	assert is_arity(n, func) is expected, messageTestFailure(is_arity(n, func), expected, is_arity.__name__, n, func)
