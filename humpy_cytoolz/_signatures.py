# pyright: reportUnknownLambdaType=false
# ruff:file-ignore[unused-lambda-argument, builtin-lambda-argument-shadowing, try-consider-else]
from __future__ import annotations

from collections.abc import Callable, Mapping
from importlib import import_module
from typing import Any, TYPE_CHECKING
import builtins
import functools
import inspect
import itertools
import operator
import sys

if TYPE_CHECKING:
	from types import ModuleType

type SignatureSpecification = tuple[int, Callable[..., Any], tuple[str, ...], inspect.Signature]
type SignatureInput = Callable[..., Any] | tuple[int, Callable[..., Any]] | tuple[int, Callable[..., Any], tuple[str, ...]]

module_info: dict[ModuleType | str, dict[str, list[SignatureInput]]] = {}
module_info[builtins] = {
	'abs': [lambda x: None],
	'all': [lambda iterable: None],
	'anext': [lambda aiterator: None, lambda aiterator, default: None],
	'any': [lambda iterable: None],
	'ascii': [lambda obj: None],
	'bin': [lambda number: None],
	'bool': [lambda x=False: None],
	'bytearray': [lambda: None, lambda int: None, lambda string, encoding='utf8', errors='strict': None],
	'callable': [lambda obj: None],
	'chr': [lambda i: None],
	'classmethod': [lambda function: None],
	'complex': [lambda real=0, imag=0: None],
	'delattr': [lambda obj, name: None],
	'dict': [lambda **kwargs: None, lambda mapping, **kwargs: None],
	'dir': [lambda: None, lambda object: None],
	'divmod': [lambda x, y: None],
	'enumerate': [(0, lambda iterable, start=0: None)],
	'eval': [lambda source: None, lambda source, globals: None, lambda source, globals, locals: None],
	'filter': [lambda function, iterable: None],
	'float': [lambda x=0.0: None],
	'format': [lambda value: None, lambda value, format_spec: None],
	'frozenset': [lambda: None, lambda iterable: None],
	'getattr': [lambda object, name: None, lambda object, name, default: None],
	'globals': [lambda: None],
	'hasattr': [lambda obj, name: None],
	'hash': [lambda obj: None],
	'hex': [lambda number: None],
	'id': [lambda obj: None],
	'input': [lambda: None, lambda prompt: None],
	'int': [lambda x=0: None, (0, lambda x, base=10: None)],
	'isinstance': [lambda obj, class_or_tuple: None],
	'issubclass': [lambda cls, class_or_tuple: None],
	'iter': [lambda iterable: None, lambda callable, sentinel: None],
	'len': [lambda obj: None],
	'list': [lambda: None, lambda iterable: None],
	'locals': [lambda: None],
	'map': [lambda func, sequence, *iterables: None],
	'memoryview': [(0, lambda object: None)],
	'next': [lambda iterator: None, lambda iterator, default: None],
	'object': [lambda: None],
	'oct': [lambda number: None],
	'ord': [lambda c: None],
	'pow': [lambda x, y: None, lambda x, y, z: None],
	'property': [lambda fget=None, fset=None, fdel=None, doc=None: None],
	'range': [lambda stop: None, lambda start, stop: None, lambda start, stop, step: None],
	'repr': [lambda obj: None],
	'reversed': [lambda sequence: None],
	'round': [(0, lambda number, ndigits=0: None)],
	'set': [lambda: None, lambda iterable: None],
	'setattr': [lambda obj, name, value: None],
	'slice': [lambda stop: None, lambda start, stop: None, lambda start, stop, step: None],
	'staticmethod': [lambda function: None],
	'sum': [lambda iterable: None, lambda iterable, start: None],
	'super': [lambda type: None, lambda type, obj: None],
	'tuple': [lambda: None, lambda iterable: None],
	'type': [lambda object: None, lambda name, bases, dict: None],
	'vars': [lambda: None, lambda object: None],
	'zip': [(0, lambda *iterables: None, ('strict',))],
	'__build_class__': [(2, lambda func, name, *bases, **kwds: None, ('metaclass',))],
	'__import__': [(0, lambda name, globals=None, locals=None, fromlist=None, level=None: None)],
}
if sys.version_info >= (3, 15):
	module_info[builtins]['frozendict'] = [lambda **kwargs: None, lambda mapping, **kwargs: None]

if sys.version_info >= (3, 14):
	module_info[builtins]['map'] = [(2, lambda func, sequence, *iterables: None, ('strict',))]

module_info[builtins]['exec'] = [lambda source: None, lambda source, globals: None, lambda source, globals, locals: None]
module_info[builtins].update(
	breakpoint=[lambda *args, **kws: None],
	bytes=[lambda: None, lambda int: None, lambda string, encoding='utf8', errors='strict': None],
	compile=[(0, lambda source, filename, mode, flags=0, dont_inherit=False, optimize=-1: None)],
	max=[(1, lambda iterable: None, ('default', 'key')), (1, lambda arg1, arg2, *args: None, ('key',))],
	min=[(1, lambda iterable: None, ('default', 'key')), (1, lambda arg1, arg2, *args: None, ('key',))],
	open=[(0, lambda file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None: None)],
	sorted=[(1, lambda iterable: None, ('key', 'reverse'))],
	str=[lambda object='', encoding='utf', errors='strict': None],
)
module_info[builtins]['print'] = [(0, lambda *args: None, ('sep', 'end', 'file', 'flush'))]
module_info[functools] = {
	'cmp_to_key': [(0, lambda mycmp: None)],
	'partial': [lambda func, *args, **kwargs: None],
	'partialmethod': [lambda func, *args, **kwargs: None],
}
module_info[itertools] = {
	'accumulate': [(0, lambda iterable, func=None: None, ('initial',))],
	'chain': [lambda *iterables: None],
	'combinations': [(0, lambda iterable, r: None)],
	'combinations_with_replacement': [(0, lambda iterable, r: None)],
	'compress': [(0, lambda data, selectors: None)],
	'count': [lambda start=0, step=1: None],
	'cycle': [lambda iterable: None],
	'dropwhile': [lambda predicate, iterable: None],
	'filterfalse': [lambda function, sequence: None],
	'groupby': [(0, lambda iterable, key=None: None)],
	'islice': [lambda iterable, stop: None, lambda iterable, start, stop: None, lambda iterable, start, stop, step: None],
	'pairwise': [lambda iterable: None],
	'permutations': [(0, lambda iterable, r=0: None)],
	'product': [(0, lambda *iterables: None, ('repeat',))],
	'repeat': [(0, lambda object, times=None: None)],
	'starmap': [lambda function, sequence: None],
	'takewhile': [lambda predicate, iterable: None],
	'tee': [lambda iterable: None, lambda iterable, n: None],
	'zip_longest': [(0, lambda *iterables: None, ('fillvalue',))],
}
module_info[operator] = {
	'__abs__': [lambda a: None],
	'__add__': [lambda a, b: None],
	'__and__': [lambda a, b: None],
	'__concat__': [lambda a, b: None],
	'__contains__': [lambda a, b: None],
	'__delitem__': [lambda a, b: None],
	'__eq__': [lambda a, b: None],
	'__floordiv__': [lambda a, b: None],
	'__ge__': [lambda a, b: None],
	'__getitem__': [lambda a, b: None],
	'__gt__': [lambda a, b: None],
	'__iadd__': [lambda a, b: None],
	'__iand__': [lambda a, b: None],
	'__iconcat__': [lambda a, b: None],
	'__ifloordiv__': [lambda a, b: None],
	'__ilshift__': [lambda a, b: None],
	'__imatmul__': [lambda a, b: None],
	'__imod__': [lambda a, b: None],
	'__imul__': [lambda a, b: None],
	'__index__': [lambda a: None],
	'__inv__': [lambda a: None],
	'__invert__': [lambda a: None],
	'__ior__': [lambda a, b: None],
	'__ipow__': [lambda a, b: None],
	'__irepeat__': [lambda a, b: None],
	'__irshift__': [lambda a, b: None],
	'__isub__': [lambda a, b: None],
	'__itruediv__': [lambda a, b: None],
	'__ixor__': [lambda a, b: None],
	'__le__': [lambda a, b: None],
	'__lshift__': [lambda a, b: None],
	'__lt__': [lambda a, b: None],
	'__matmul__': [lambda a, b: None],
	'__mod__': [lambda a, b: None],
	'__mul__': [lambda a, b: None],
	'__ne__': [lambda a, b: None],
	'__neg__': [lambda a: None],
	'__not__': [lambda a: None],
	'__or__': [lambda a, b: None],
	'__pos__': [lambda a: None],
	'__pow__': [lambda a, b: None],
	'__rshift__': [lambda a, b: None],
	'__setitem__': [lambda a, b, c: None],
	'__sub__': [lambda a, b: None],
	'__truediv__': [lambda a, b: None],
	'__xor__': [lambda a, b: None],
	'abs': [lambda a: None],
	'add': [lambda a, b: None],
	'and_': [lambda a, b: None],
	'attrgetter': [lambda attr, *args: None],
	'concat': [lambda a, b: None],
	'contains': [lambda a, b: None],
	'countOf': [lambda a, b: None],
	'delitem': [lambda a, b: None],
	'eq': [lambda a, b: None],
	'floordiv': [lambda a, b: None],
	'ge': [lambda a, b: None],
	'getitem': [lambda a, b: None],
	'gt': [lambda a, b: None],
	'iadd': [lambda a, b: None],
	'iand': [lambda a, b: None],
	'iconcat': [lambda a, b: None],
	'ifloordiv': [lambda a, b: None],
	'ilshift': [lambda a, b: None],
	'imatmul': [lambda a, b: None],
	'imod': [lambda a, b: None],
	'imul': [lambda a, b: None],
	'index': [lambda a: None],
	'indexOf': [lambda a, b: None],
	'inv': [lambda a: None],
	'invert': [lambda a: None],
	'ior': [lambda a, b: None],
	'ipow': [lambda a, b: None],
	'irepeat': [lambda a, b: None],
	'irshift': [lambda a, b: None],
	'is_': [lambda a, b: None],
	'is_not': [lambda a, b: None],
	'isub': [lambda a, b: None],
	'itemgetter': [lambda item, *args: None],
	'itruediv': [lambda a, b: None],
	'ixor': [lambda a, b: None],
	'le': [lambda a, b: None],
	'length_hint': [lambda obj: None, lambda obj, default: None],
	'lshift': [lambda a, b: None],
	'lt': [lambda a, b: None],
	'matmul': [lambda a, b: None],
	'methodcaller': [lambda name, *args, **kwargs: None],
	'mod': [lambda a, b: None],
	'mul': [lambda a, b: None],
	'ne': [lambda a, b: None],
	'neg': [lambda a: None],
	'not_': [lambda a: None],
	'or_': [lambda a, b: None],
	'pos': [lambda a: None],
	'pow': [lambda a, b: None],
	'rshift': [lambda a, b: None],
	'setitem': [lambda a, b, c: None],
	'sub': [lambda a, b: None],
	'truediv': [lambda a, b: None],
	'truth': [lambda a: None],
	'xor': [lambda a, b: None],
}
module_info['humpy_cytoolz'] = {
	'curry': [(0, lambda *args, **kwargs: None)],
	'excepts': [(0, lambda exc, func, handler=None: None)],
	'flip': [(0, lambda func=None, a=None, b=None: None)],
	'juxt': [(0, lambda *funcs: None)],
	'memoize': [(0, lambda func=None, cache=None, key=None: None)],
}
module_info['humpy_cytoolz.functoolz'] = {
	'Compose': [(0, lambda funcs: None)],
}

def num_pos_args(sigspec: inspect.Signature) -> builtins.int:
	"""Return the number of positional arguments.  ``f(x, y=1)`` has 1"""
	return sum(1 for x in sigspec.parameters.values() if x.kind == x.POSITIONAL_OR_KEYWORD and x.default is x.empty)

def get_exclude_keywords(num_pos_only: builtins.int, sigspec: inspect.Signature) -> tuple[str, ...]:
	"""Return the names of position-only arguments if func has **kwargs"""
	if num_pos_only == 0:
		return ()
	has_kwargs: builtins.bool = any(x.kind == x.VAR_KEYWORD for x in sigspec.parameters.values())
	if not has_kwargs:
		return ()
	pos_args: builtins.list[inspect.Parameter] = list(sigspec.parameters.values())[:num_pos_only]
	return tuple(x.name for x in pos_args)

def signature_or_spec(func: Callable[..., Any]) -> inspect.Signature | None:
	try:
		return inspect.signature(func)
	except (ValueError, TypeError):
		return None

def expand_sig(sig: SignatureInput) -> SignatureSpecification:
	"""Convert the signature spec in ``module_info`` to add to ``signatures``

	The input signature spec is one of:
		- ``lambda_func``
		- ``(num_position_args, lambda_func)``
		- ``(num_position_args, lambda_func, keyword_only_args)``

	The output signature spec is:
		``(num_position_args, lambda_func, keyword_exclude, sigspec)``

	where ``keyword_exclude`` includes keyword only arguments and, if variadic
	keywords is present, the names of position-only argument.  The latter is
	included to support builtins such as ``partial(func, *args, **kwargs)``,
	which allows ``func=`` to be used as a keyword even though it's the name
	of a positional argument.
	"""
	if callable(sig):
		func: Callable[..., Any] = sig
		sigspec: inspect.Signature = inspect.signature(func)
		num_pos_only: builtins.int = num_pos_args(sigspec)
		keyword_only = ()
	else:
		if len(sig) == 3:
			num_pos_only, func, keyword_only = sig
		else:
			num_pos_only, func = sig
			keyword_only = ()
		sigspec = inspect.signature(func)
	keyword_exclude: tuple[str, ...] = get_exclude_keywords(num_pos_only, sigspec)
	return (num_pos_only, func, keyword_only + keyword_exclude, sigspec)

signatures: dict[Callable[..., Any], tuple[SignatureSpecification, ...]] = {}

def create_signature_registry(
	module_info: dict[ModuleType | str, dict[str, list[SignatureInput]]] = module_info,
	signatures: dict[Callable[..., Any], tuple[SignatureSpecification, ...]] = signatures,
) -> None:
	for module, info in module_info.items():
		if isinstance(module, str):
			module = import_module(module)
		for name, sigs in info.items():
			if hasattr(module, name):
				new_sigs: builtins.tuple[SignatureSpecification, ...] = tuple(expand_sig(sig) for sig in sigs)
				signatures[getattr(module, name)] = new_sigs

def check_valid(sig: SignatureSpecification, args: tuple[Any, ...], kwargs: Mapping[str, Any]) -> builtins.bool:
	"""Like ``is_valid_args`` for the given signature spec"""
	num_pos_only, func, keyword_exclude, _sigspec = sig
	if len(args) < num_pos_only:
		return False
	if keyword_exclude:
		kwargs = dict(kwargs)
		for item in keyword_exclude:
			kwargs.pop(item, None)
	try:
		func(*args, **kwargs)
		return True
	except TypeError:
		return False

def _is_valid_args(func: Callable[..., Any], args: tuple[Any, ...], kwargs: Mapping[str, Any]) -> builtins.bool | None:
	"""Like ``is_valid_args`` for builtins in our ``signatures`` registry"""
	if func not in signatures:
		return None
	sigs: builtins.tuple[SignatureSpecification, ...] = signatures[func]
	return any(check_valid(sig, args, kwargs) for sig in sigs)

def check_partial(sig: SignatureSpecification, args: tuple[Any, ...], kwargs: Mapping[str, Any]) -> builtins.bool | None:
	"""Like ``is_partial_args`` for the given signature spec"""
	num_pos_only, func, keyword_exclude, sigspec = sig
	if len(args) < num_pos_only:
		pad: builtins.tuple[None, ...] = (None,) * (num_pos_only - len(args))
		args += pad
	if keyword_exclude:
		kwargs = dict(kwargs)
		for item in keyword_exclude:
			kwargs.pop(item, None)
	return is_partial_args(func, args, kwargs, sigspec)

def _is_partial_args(func: Callable[..., Any], args: tuple[Any, ...], kwargs: Mapping[str, Any]) -> builtins.bool | None:
	"""Like ``is_partial_args`` for builtins in our ``signatures`` registry"""
	if func not in signatures:
		return None
	sigs: builtins.tuple[SignatureSpecification, ...] = signatures[func]
	return any(check_partial(sig, args, kwargs) for sig in sigs)

def check_arity(n: builtins.int, sig: SignatureSpecification) -> builtins.bool | None:
	num_pos_only, func, keyword_exclude, sigspec = sig
	if keyword_exclude or num_pos_only > n:
		return False
	return is_arity(n, func, sigspec)

def _is_arity(n: builtins.int, func: Callable[..., Any]) -> builtins.bool | None:
	if func not in signatures:
		return None
	sigs: builtins.tuple[SignatureSpecification, ...] = signatures[func]
	checks: builtins.list[builtins.bool | None] = [check_arity(n, sig) for sig in sigs]
	if all(checks):
		return True
	elif any(checks):
		return None
	return False

def check_varargs(sig: SignatureSpecification) -> builtins.bool | None:
	_num_pos_only, func, _keyword_exclude, sigspec = sig
	return has_varargs(func, sigspec)

def _has_varargs(func: Callable[..., Any]) -> builtins.bool | None:
	if func not in signatures:
		return None
	sigs: builtins.tuple[SignatureSpecification, ...] = signatures[func]
	checks: builtins.list[builtins.bool | None] = [check_varargs(sig) for sig in sigs]
	if all(checks):
		return True
	elif any(checks):
		return None
	return False

def check_keywords(sig: SignatureSpecification) -> builtins.bool | None:
	_num_pos_only, func, keyword_exclude, sigspec = sig
	if keyword_exclude:
		return True
	return has_keywords(func, sigspec)

def _has_keywords(func: Callable[..., Any]) -> builtins.bool | None:
	if func not in signatures:
		return None
	sigs: builtins.tuple[SignatureSpecification, ...] = signatures[func]
	checks: builtins.list[builtins.bool | None] = [check_keywords(sig) for sig in sigs]
	if all(checks):
		return True
	elif any(checks):
		return None
	return False

def check_required_args(sig: SignatureSpecification) -> builtins.int | None:
	_num_pos_only, func, _keyword_exclude, sigspec = sig
	return num_required_args(func, sigspec)

def _num_required_args(func: Callable[..., Any]) -> builtins.int | None:
	if func not in signatures:
		return None
	sigs: builtins.tuple[SignatureSpecification, ...] = signatures[func]
	vals: builtins.list[builtins.int | None] = [check_required_args(sig) for sig in sigs]
	val: builtins.int | None = vals[0]
	if all(x == val for x in vals):
		return val
	return None


def _check_sigspec[T](
	sigspec: inspect.Signature | None, func: Callable[..., Any], builtin_func: Callable[..., T], *builtin_args: Any
) -> tuple[inspect.Signature | None, T | bool | None]:
	inspection: inspect.Signature | ValueError | TypeError | None = sigspec
	if inspection is None:
		try:
			inspection = inspect.signature(func)
		except (ValueError, TypeError) as e:
			inspection = e
	if isinstance(inspection, ValueError):
		return (None, builtin_func(*builtin_args))
	elif not isinstance(inspection, inspect.Signature):
		if func in signatures and (hasattr(func, '__signature__') and hasattr(operator.attrgetter('__signature__')(func), '__get__')):
			val = builtin_func(*builtin_args)
			return (None, val)
		return (None, False)
	return (inspection, None)


def num_required_args(func: Callable[..., Any], sigspec: inspect.Signature | None = None) -> int | None:
	sigspec, rv = _check_sigspec(sigspec, func, _num_required_args, func)
	if sigspec is None:
		return rv
	return sum(1 for p in sigspec.parameters.values() if p.default is p.empty and p.kind in {p.POSITIONAL_OR_KEYWORD, p.POSITIONAL_ONLY})

def has_varargs(func: Callable[..., Any], sigspec: inspect.Signature | None = None) -> bool | None:
	sigspec, rv = _check_sigspec(sigspec, func, _has_varargs, func)
	if sigspec is None:
		return rv
	return any(p.kind == p.VAR_POSITIONAL for p in sigspec.parameters.values())

def has_keywords(func: Callable[..., Any], sigspec: inspect.Signature | None = None) -> bool | None:
	sigspec, rv = _check_sigspec(sigspec, func, _has_keywords, func)
	if sigspec is None:
		return rv
	return any(p.default is not p.empty or p.kind in {p.KEYWORD_ONLY, p.VAR_KEYWORD} for p in sigspec.parameters.values())

def is_valid_args(
	func: Callable[..., Any], args: tuple[Any, ...], kwargs: Mapping[str, Any], sigspec: inspect.Signature | None = None
) -> bool | None:
	sigspec, rv = _check_sigspec(sigspec, func, _is_valid_args, func, args, kwargs)
	if sigspec is None:
		return rv
	try:
		sigspec.bind(*args, **kwargs)
	except TypeError:
		return False
	return True

def is_partial_args(
	func: Callable[..., Any], args: tuple[Any, ...], kwargs: Mapping[str, Any], sigspec: inspect.Signature | None = None
) -> bool | None:
	sigspec, rv = _check_sigspec(sigspec, func, _is_partial_args, func, args, kwargs)
	if sigspec is None:
		return rv
	try:
		sigspec.bind_partial(*args, **kwargs)
	except TypeError:
		return False
	return True

def is_arity(n: int, func: Callable[..., Any], sigspec: inspect.Signature | None = None) -> bool | None:
	"""Does a function have only n positional arguments?

	This function relies on introspection and does not call the function.
	Returns None if validity can't be determined.

	>>> def f(x):
	...     return x
	>>> is_arity(1, f)
	True
	>>> def g(x, y=1):
	...     return x + y
	>>> is_arity(1, g)
	False
	"""
	sigspec, rv = _check_sigspec(sigspec, func, _is_arity, n, func)
	if sigspec is None:
		return rv
	num = num_required_args(func, sigspec)
	if num is not None:
		num = num == n
		if not num:
			return False
	varargs = has_varargs(func, sigspec)
	if varargs:
		return False
	keywords = has_keywords(func, sigspec)
	if keywords:
		return False
	if num is None or varargs is None or keywords is None:
		return None
	return True


cytoolz_info: dict[ModuleType | str, dict[str, list[SignatureInput]]] = {}
cytoolz_info['humpy_cytoolz.dicttoolz'] = dict(assoc=[lambda d, key, value, factory=dict: None], assoc_in=[lambda d, keys, value, factory=dict: None], dissoc=[lambda d, *keys, **kwargs: None], get_in=[lambda keys, coll, default=None, no_default=False: None], itemfilter=[lambda predicate, d, factory=dict: None], itemmap=[lambda func, d, factory=dict: None], keyfilter=[lambda predicate, d, factory=dict: None], keymap=[lambda func, d, factory=dict: None], merge=[lambda *dicts, **kwargs: None], merge_with=[lambda func, *dicts, **kwargs: None], update_in=[lambda d, keys, func, default=None, factory=dict: None], valfilter=[lambda predicate, d, factory=dict: None], valmap=[lambda func, d, factory=dict: None])
cytoolz_info['humpy_cytoolz.functoolz'] = dict(apply=[lambda *func_and_args, **kwargs: None], Compose=[lambda *funcs: None], complement=[lambda func: None], compose=[lambda *funcs: None], compose_left=[lambda *funcs: None], curry=[lambda *args, **kwargs: None], do=[lambda func, x: None], excepts=[lambda exc, func, handler=None: None], flip=[lambda: None, lambda func: None, lambda func, a: None, lambda func, a, b: None], _flip=[lambda func, a, b: None], identity=[lambda x: None], juxt=[lambda *funcs: None], memoize=[lambda cache=None, key=None: None, lambda func, cache=None, key=None: None], _memoize=[lambda func, cache=None, key=None: None], pipe=[lambda data, *funcs: None], return_none=[lambda exc: None], thread_first=[lambda val, *forms: None], thread_last=[lambda val, *forms: None])
cytoolz_info['humpy_cytoolz.itertoolz'] = dict(accumulate=[lambda binop, seq, initial='__no__default__': None], cons=[lambda el, seq: None], diff=[lambda *seqs, **kwargs: None], drop=[lambda n, seq: None], first=[lambda seq: None], frequencies=[lambda seq: None], get=[lambda ind, seq, default=None: None], getter=[lambda index: None], groupby=[lambda key, seq: None], identity=[lambda x: None], interleave=[lambda seqs: None], isiterable=[lambda x: None], join=[lambda leftkey, leftseq, rightkey, rightseq, left_default=None, right_default=None: None], last=[lambda seq: None], mapcat=[lambda func, seqs: None], nth=[lambda n, seq: None], partition=[lambda n, seq, pad=None: None], partition_all=[lambda n, seq: None], peek=[lambda seq: None], peekn=[lambda n, seq: None], pluck=[lambda ind, seqs, default=None: None], random_sample=[lambda prob, seq, random_state=None: None], reduceby=[lambda key, binop, seq, init=None: None], rest=[lambda seq: None], second=[lambda seq: None], sliding_window=[lambda n, seq: None], tail=[lambda n, seq: None], take=[lambda n, seq: None], take_nth=[lambda n, seq: None], topk=[lambda k, seq, key=None: None])
cytoolz_info['humpy_cytoolz.recipes'] = dict(countby=[lambda key, seq: None], partitionby=[lambda func, seq: None])

def update_signature_registry() -> None:
	module_info.update(cytoolz_info)
	create_signature_registry()
