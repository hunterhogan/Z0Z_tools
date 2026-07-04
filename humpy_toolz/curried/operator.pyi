import sys
from humpy_toolz.functoolz import curry
# Unary operators and special cases - not curried (from IGNORE set in operator.py)
from operator import (
	__abs__ as __abs__, __index__ as __index__, __inv__ as __inv__, __invert__ as __invert__, __neg__ as __neg__, __not__ as __not__,
	__pos__ as __pos__, abs as abs, attrgetter as attrgetter, index as index, inv as inv, invert as invert, itemgetter as itemgetter,
	neg as neg, not_ as not_, pos as pos, truth as truth)
import operator

__all__ = [
	# Unary operators and special cases (not curried)
	"__abs__",
	"__index__",
	"__inv__",
	"__invert__",
	"__neg__",
	"__not__",
	"__pos__",
	"abs",
	"attrgetter",
	"index",
	"inv",
	"invert",
	"itemgetter",
	"neg",
	"not_",
	"pos",
	"truth",
]

if (3, 14) <= sys.version_info:  # noqa: PYI002
	from operator import is_not_none, is_none
	__all__ += ['is_none', 'is_not_none']

# Binary and n-ary operators (curried)
__all__ += [
	"__add__",
	"__and__",
	"__concat__",
	"__contains__",
	"__delitem__",
	"__eq__",
	"__floordiv__",
	"__ge__",
	"__getitem__",
	"__gt__",
	"__iadd__",
	"__iand__",
	"__iconcat__",
	"__ifloordiv__",
	"__ilshift__",
	"__imatmul__",
	"__imod__",
	"__imul__",
	"__ior__",
	"__ipow__",
	"__irshift__",
	"__isub__",
	"__itruediv__",
	"__ixor__",
	"__le__",
	"__lshift__",
	"__lt__",
	"__matmul__",
	"__mod__",
	"__mul__",
	"__ne__",
	"__or__",
	"__pow__",
	"__rshift__",
	"__setitem__",
	"__sub__",
	"__truediv__",
	"__xor__",
	"add",
	"and_",
	"concat",
	"contains",
	"countOf",
	"delitem",
	"eq",
	"floordiv",
	"ge",
	"getitem",
	"gt",
	"iadd",
	"iand",
	"iconcat",
	"ifloordiv",
	"ilshift",
	"imatmul",
	"imod",
	"imul",
	"indexOf",
	"ior",
	"ipow",
	"irshift",
	"is_",
	"is_not",
	"isub",
	"itruediv",
	"ixor",
	"le",
	"length_hint",
	"lshift",
	"lt",
	"matmul",
	"methodcaller",
	"mod",
	"mul",
	"ne",
	"or_",
	"pow",
	"rshift",
	"setitem",
	"sub",
	"truediv",
	"xor",
]

# Binary and n-ary operators - curried
# Define non-dunder versions (canonical), then alias dunder versions

# Arithmetic operators
add = curry(operator.add)
__add__ = add

sub = curry(operator.sub)
__sub__ = sub

mul = curry(operator.mul)
__mul__ = mul

truediv = curry(operator.truediv)
__truediv__ = truediv

floordiv = curry(operator.floordiv)
__floordiv__ = floordiv

mod = curry(operator.mod)
__mod__ = mod

pow = curry(operator.pow)
__pow__ = pow

matmul = curry(operator.matmul)
__matmul__ = matmul

# Bitwise operators
and_ = curry(operator.and_)
__and__ = and_

or_ = curry(operator.or_)
__or__ = or_

xor = curry(operator.xor)
__xor__ = xor

lshift = curry(operator.lshift)
__lshift__ = lshift

rshift = curry(operator.rshift)
__rshift__ = rshift

# Comparison operators
eq = curry(operator.eq)
__eq__ = eq

ne = curry(operator.ne)
__ne__ = ne

lt = curry(operator.lt)
__lt__ = lt

le = curry(operator.le)
__le__ = le

gt = curry(operator.gt)
__gt__ = gt

ge = curry(operator.ge)
__ge__ = ge

# In-place operators
iadd = curry(operator.iadd)
__iadd__ = iadd

isub = curry(operator.isub)
__isub__ = isub

imul = curry(operator.imul)
__imul__ = imul

itruediv = curry(operator.itruediv)
__itruediv__ = itruediv

ifloordiv = curry(operator.ifloordiv)
__ifloordiv__ = ifloordiv

imod = curry(operator.imod)
__imod__ = imod

ipow = curry(operator.ipow)
__ipow__ = ipow

imatmul = curry(operator.imatmul)
__imatmul__ = imatmul

iand = curry(operator.iand)
__iand__ = iand

ior = curry(operator.ior)
__ior__ = ior

ixor = curry(operator.ixor)
__ixor__ = ixor

ilshift = curry(operator.ilshift)
__ilshift__ = ilshift

irshift = curry(operator.irshift)
__irshift__ = irshift

# Sequence/container operators
concat = curry(operator.concat)
__concat__ = concat

iconcat = curry(operator.iconcat)
__iconcat__ = iconcat

contains = curry(operator.contains)
__contains__ = contains

getitem = curry(operator.getitem)
__getitem__ = getitem

setitem = curry(operator.setitem)
__setitem__ = setitem

delitem = curry(operator.delitem)
__delitem__ = delitem

# Other binary operators
is_ = curry(operator.is_)
is_not = curry(operator.is_not)

if (3, 11) <= sys.version_info:  # noqa: PYI002
	call = curry(operator.call)
	__call__ = call
	__all__ += ["__call__", "call"]

# Utility functions
countOf = curry(operator.countOf)
indexOf = curry(operator.indexOf)
length_hint = curry(operator.length_hint)
methodcaller = curry(operator.methodcaller)
