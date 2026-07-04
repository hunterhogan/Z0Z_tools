# ruff: noqa: D100
from __future__ import annotations

from humpy_toolz.itertoolz import partition_all
from humpy_toolz.utils import no_default
from typing import overload, TYPE_CHECKING
import functools

if TYPE_CHECKING:
	from collections.abc import Callable, Iterable
	from humpy_toolz._theTypes import MapFunction, TypeElement, TypeResult
	from typing import Literal

@overload
def _reduce(
	func: Callable[[TypeElement, TypeElement], TypeElement],
	seq: Iterable[TypeElement],
	initial: None = None,
) -> TypeElement: ...
@overload
def _reduce(
	func: Callable[[TypeResult, TypeElement], TypeResult],
	seq: Iterable[TypeElement],
	initial: TypeResult,
) -> TypeResult: ...
def _reduce(
	func: Callable[[TypeResult, TypeElement], TypeResult] | Callable[[TypeElement, TypeElement], TypeElement],
	seq: Iterable[TypeElement],
	initial: TypeResult | None = None,
) -> TypeResult | TypeElement:
	if initial is None:
		return functools.reduce(func, seq)
	else:
		return functools.reduce(func, seq, initial)

@overload
def fold(
	binop: Callable[[TypeElement, TypeElement], TypeElement],
	seq: Iterable[TypeElement],
	default: Literal['__no__default__'] = no_default,
	map: MapFunction[TypeElement, TypeElement] = map,
	chunksize: int = 128,
	combine: Callable[[TypeElement, TypeElement], TypeElement] | None = None,
) -> TypeElement: ...
@overload
def fold(
	binop: Callable[[TypeResult, TypeElement], TypeResult],
	seq: Iterable[TypeElement],
	default: TypeResult,
	map: MapFunction[TypeElement, TypeResult] = map,
	chunksize: int = 128,
	combine: Callable[[TypeResult, TypeResult], TypeResult] | None = None,
) -> TypeResult: ...
def fold(
	binop: Callable[[TypeResult, TypeElement], TypeResult] | Callable[[TypeElement, TypeElement], TypeElement],
	seq: Iterable[TypeElement],
	default: TypeResult | Literal['__no__default__'] = no_default,
	map: MapFunction[TypeElement, TypeResult] | MapFunction[TypeElement, TypeElement] = map,
	chunksize: int = 128,
	combine: Callable[[TypeResult, TypeResult], TypeResult] | Callable[[TypeElement, TypeElement], TypeElement] | None = None,
) -> TypeResult | TypeElement:
	"""
	Reduce without guarantee of ordered reduction.

	Parameters
	----------
	binops
		Associative operator. The associative property allows us to
		leverage a parallel map to perform reductions in parallel.

	inputs:

	``binop``     - associative operator. The associative property allows us to
					leverage a parallel map to perform reductions in parallel.

	``seq``       - a sequence to be aggregated
	``default``   - an identity element like 0 for ``add`` or 1 for mul

	``map``       - an implementation of ``map``. This may be parallel and
					determines how work is distributed.
	``chunksize`` - Number of elements of ``seq`` that should be handled
					within a single function call
	``combine``   - Binary operator to combine two intermediate results.
					If ``binop`` is of type (total, item) -> total
					then ``combine`` is of type (total, total) -> total
					Defaults to ``binop`` for common case of operators like add

	Fold chunks up the collection into blocks of size ``chunksize`` and then
	feeds each of these to calls to ``reduce``. This work is distributed
	with a call to ``map``, gathered back and then refolded to finish the
	computation. In this way ``fold`` specifies only how to chunk up data but
	leaves the distribution of this work to an externally provided ``map``
	function. This function can be sequential or rely on multithreading,
	multiprocessing, or even distributed solutions.

	If ``map`` intends to serialize functions it should be prepared to accept
	and serialize lambdas. Note that the standard ``pickle`` module fails
	here.

	Example
	-------

	>>> # Provide a parallel map to accomplish a parallel sum
	>>> from operator import add
	>>> fold(add, [1, 2, 3, 4], chunksize=2, map=map)
	10
	"""
	assert chunksize > 1
	if combine is None:
		combine = binop
	chunks = partition_all(chunksize, seq)
	if default == no_default:
		results = map(functools.partial(_reduce, binop), chunks)
	else:
		results = map(functools.partial(_reduce, binop, initial=default), chunks)
	results = list(results)
	if len(results) == 1:
		return results[0]
	else:
		return fold(combine, results, map=map, chunksize=chunksize)
