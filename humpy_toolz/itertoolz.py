# pyright: reportArgumentType=false
# pyright: reportAssignmentType=false
# pyright: reportCallIssue=false
# pyright: reportIndexIssue=false
# pyright: reportMissingParameterType=false
# pyright: reportOptionalMemberAccess=false
# pyright: reportOverlappingOverload=false
# pyright: reportPossiblyUnboundVariable=false
# pyright: reportReturnType=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownLambdaType=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnnecessaryComparison=false
# ruff: noqa: D100, DOC201, TRY300, PERF203, DOC402, S311, PLC0415, B905, PLR0911, ERA001, E101, E731, RUF052, DOC501
# ty:ignore[call-non-callable]
# ty:ignore[call-top-callable]
# ty:ignore[invalid-argument-type]
# ty:ignore[invalid-assignment]
# ty:ignore[invalid-return-type]
# ty:ignore[invalid-yield]
# ty:ignore[no-matching-overload]
# ty:ignore[not-subscriptable]
from __future__ import annotations

from collections import defaultdict, deque
from collections.abc import Sequence
from functools import partial
from humpy_toolz.utils import no_default
from itertools import filterfalse, zip_longest
from operator import is_not, itemgetter
from typing import cast, overload, TYPE_CHECKING
import heapq
import itertools

if TYPE_CHECKING:
	from collections.abc import Callable, Collection, Hashable, ItemsView, Iterable, Iterator, KeysView, Mapping, ValuesView
	from humpy_toolz._theTypes import (
		K, KHashable, L, P, R, Randomable, S, SSequence, SupportsDunderLT, SupportsGetItem, T, TIterable, TSupportsRichComparison, U)
	from typing import Any, Literal
	from typing_extensions import TypeIs

__all__ = ('accumulate', 'concat', 'concatv', 'cons', 'count', 'diff', 'drop', 'first', 'frequencies', 'get', 'groupby', 'interleave', 'interpose', 'isdistinct', 'isiterable', 'iterate', 'join', 'last', 'mapcat', 'merge_sorted', 'nth', 'partition', 'partition_all', 'peek', 'peekn', 'pluck', 'random_sample', 'reduceby', 'remove', 'second', 'sliding_window', 'tail', 'take', 'take_nth', 'topk', 'unique')

no_pad: Literal['__no__pad__'] = '__no__pad__'

@overload
def accumulate(binop: Callable[[T, T], T], seq: Iterable[T], initial: Literal['__no__default__'] = no_default) -> Iterator[T]: ...
@overload
def accumulate(binop: Callable[[T, S], T], seq: Iterable[S], initial: T) -> Iterator[T]: ...
def accumulate(binop: Callable[[T, S], T], seq: Iterable[S], initial: T | Literal['__no__default__'] = no_default) -> Iterator[T]:
	"""Repeatedly apply binary function to a sequence, accumulating results

	>>> from operator import add, mul
	>>> list(accumulate(add, [1, 2, 3, 4, 5]))
	[1, 3, 6, 10, 15]
	>>> list(accumulate(mul, [1, 2, 3, 4, 5]))
	[1, 2, 6, 24, 120]

	Accumulate is similar to ``reduce`` and is good for making functions like
	cumulative sum:

	>>> from functools import partial, reduce
	>>> sum    = partial(reduce, add)
	>>> cumsum = partial(accumulate, add)

	Accumulate also takes an optional argument that will be used as the first
	value. This is similar to reduce.

	>>> list(accumulate(add, [1, 2, 3], -1))
	[-1, 0, 2, 5]
	>>> list(accumulate(add, [], 1))
	[1]

	See Also
	--------
		itertools.accumulate :  In standard itertools for Python 3.2+
	"""
	seq = iter(seq)
	if initial == no_default:
		try:
			result: S = next(seq)
		except StopIteration:
			return
	else:
		result = initial
	yield result
	for elem in seq:
		result = binop(result, elem)
		yield result

def concat(seqs: Iterable[Iterable[T]]) -> Iterator[T]:
	"""Concatenate zero or more iterables, any of which may be infinite.

	An infinite sequence will prevent the rest of the arguments from
	being included.

	We use chain.from_iterable rather than ``chain(*seqs)`` so that seqs
	can be a generator.

	>>> list(concat([[], [1], [2, 3]]))
	[1, 2, 3]

	See Also
	--------
		itertools.chain.from_iterable  equivalent
	"""
	return itertools.chain.from_iterable(seqs)

def concatv(*seqs: Iterable[T]) -> Iterator[T]:
	"""Variadic version of concat

	>>> list(concatv([], ["a"], ["b", "c"]))
	['a', 'b', 'c']

	See Also
	--------
		itertools.chain
	"""
	return concat(seqs)

def cons(el: T, seq: Iterable[T]) -> Iterator[T]:
	"""Add el to beginning of (possibly infinite) sequence seq.

	>>> list(cons(1, [2, 3]))
	[1, 2, 3]
	"""
	return itertools.chain([el], seq)

def count(seq: Iterable[Any]) -> int:
	"""Count the number of items in seq

	Like the builtin ``len`` but works on lazy sequences.

	Not to be confused with ``itertools.count``

	See Also
	--------
		len
	"""
	if hasattr(seq, '__len__'):
		return len(seq)
	return sum(1 for _i in seq)

@overload
def diff(*seqs: Iterable[T], default: Literal['__no__default__'] = no_default, key: Callable[[T], Any] | None = None) -> Iterator[tuple[T | None, ...]]: ...
@overload
def diff(*seqs: Iterable[T], default: U, key: Callable[[T], Any] | None = None) -> Iterator[tuple[T | U, ...]]: ...
@overload
def diff(*seqs: Iterable[T], default: T, key: Callable[[T], Any] | None = None) -> Iterator[tuple[T, ...]]: ...
def diff(*seqs: Iterable[T], default: U | Literal['__no__default__'] = no_default, key: Callable[[T], Any] | None = None) -> Iterator[tuple[T | U | None, ...]]:
	"""Return those items that differ between sequences

	>>> list(diff([1, 2, 3], [1, 2, 10, 100]))
	[(3, 10)]

	Shorter sequences may be padded with a ``default`` value:

	>>> list(diff([1, 2, 3], [1, 2, 10, 100], default=None))
	[(3, 10), (None, 100)]

	A ``key`` function may also be applied to each item to use during
	comparisons:

	>>> list(diff(['apples', 'bananas'], ['Apples', 'Oranges'], key=str.lower))
	[('bananas', 'Oranges')]
	"""
	N: int = len(seqs)
	if N == 1 and isinstance(seqs[0], list):
		seqs = seqs[0]
		N = len(seqs)
	if N < 2:
		message = 'Too few sequences given (min 2 required)'
		raise TypeError(message)
	if default == no_default:
		iters: Iterator[tuple[T, ...]] = zip(*seqs, strict=False)
	else:
		iters = zip_longest(*seqs, fillvalue=default)
	if key is None:
		for items in iters:
			if items.count(items[0]) != N:
				yield items
	else:
		for items in iters:
			vals: tuple[Any, ...] = tuple(map(key, items))
			if vals.count(vals[0]) != N:
				yield items

def drop(n: int, seq: Iterable[T]) -> Iterator[T]:
	"""The sequence following the first n elements

	>>> list(drop(2, [10, 20, 30, 40, 50]))
	[30, 40, 50]

	See Also
	--------
		take
		tail
	"""
	return itertools.islice(seq, n, None)

def first(seq: Iterable[T]) -> T:
	"""The first element in a sequence

	>>> first('ABC')
	'A'
	"""
	return next(iter(seq))

def frequencies(seq: Iterable[T]) -> dict[T, int]:
	"""Find number of occurrences of each value in seq

	>>> frequencies(['cat', 'cat', 'ox', 'pig', 'pig', 'cat'])  #doctest: +SKIP
	{'cat': 3, 'ox': 1, 'pig': 2}

	See Also
	--------
		countby
		groupby
	"""
	d: dict[T, int] = defaultdict(int)
	for item in seq:
		d[item] += 1
	return dict(d)

@overload
def getter(index: Sequence[K]) -> Callable[[SupportsGetItem[K, T]], tuple[T, ...]]: ...
@overload
def getter(index: K) -> Callable[[SupportsGetItem[K, T]], T]: ...
def getter(index: K | Sequence[K]) -> Callable[[SupportsGetItem[K, T]], T | tuple[T, ...]]:
	if isinstance(index, Sequence) and not isinstance(index, str):
		if len(index) == 1:
			element: K = index[0]

			def one_tuple(x: SupportsGetItem[K, T]) -> tuple[T]:
				return (x[element],)
			callableGetter: Callable[[SupportsGetItem[K, T]], tuple[T]] = one_tuple
		elif index:
			callableGetter = itemgetter(*index)
		else:
			def emptyTuple(_x: SupportsGetItem[K, T]) -> tuple[()]:
				return ()
			callableGetter = emptyTuple
	else:
		callableGetter = itemgetter(index)
	return callableGetter

def _get(ind: K, seq: SupportsGetItem[K, T], default: T) -> T:
	try:
		return seq[ind]
	except (KeyError, IndexError):
		return default
""" # TODO troubleshoot `get` type annotations
	# NOTE this part is correct.
	ww: Callable[[fs2Path], DecodedFilename] = compose(librarianDecodesFilename, fs_path.basename)
	# NOTE `T` should be a TypeVar. The input to get is `DecodedFilename`, a typeddict[str, str].
	# I guess the annotation is returning an item tuple instead of the value.
	qq: Callable[[fs2Path], tuple[T, ...]] = compose(get('fractionType'), ww)
"""
@overload
def get(ind: Sequence[K], seq: SupportsGetItem[K, T], default: T | Literal['__no__default__'] = no_default) -> tuple[T, ...]: ...
@overload
def get(ind: K, seq: SupportsGetItem[K, T], default: T | Literal['__no__default__'] = no_default) -> T: ...
def get(ind: K | Sequence[K], seq: SupportsGetItem[K, T], default: T | Literal['__no__default__'] = no_default) -> T | tuple[T, ...]:
	"""Get element in a sequence or dict

	Provides standard indexing

	>>> get(1, 'ABC')       # Same as 'ABC'[1]
	'B'

	Pass a list to get multiple values

	>>> get([1, 2], 'ABC')  # ('ABC'[1], 'ABC'[2])
	('B', 'C')

	Works on any value that supports indexing/getitem
	For example here we see that it works with dictionaries

	>>> phonebook = {'Alice':  '555-1234',
	...              'Bob':    '555-5678',
	...              'Charlie':'555-9999'}
	>>> get('Alice', phonebook)
	'555-1234'

	>>> get(['Alice', 'Bob'], phonebook)
	('555-1234', '555-5678')

	Provide a default for missing values

	>>> get(['Alice', 'Dennis'], phonebook, None)
	('555-1234', None)

	See Also
	--------
		pluck
	"""
	try:
		return seq[ind]
	except TypeError:
		if isinstance(ind, Sequence) and not isinstance(ind, str):
			if default == no_default:
				# TODO I think len == 1 and len > 1 can have the same logic.
				if len(ind) > 1:
					return itemgetter(*ind)(seq)
				elif ind:
					return (seq[ind[0]],)
				else:
					return ()
			else:
				return tuple(_get(i, seq, default) for i in ind)
		elif default != no_default:
			return default
		else:
			raise
	except (KeyError, IndexError):
		if default == no_default:
			raise
		return default

@overload
def groupby(key: Callable[[T], KHashable], seq: Iterable[T]) -> dict[KHashable, list[T]]: ...
@overload
def groupby(key: KHashable, seq: Iterable[T]) -> dict[KHashable, list[T]]: ...
def groupby(key: Callable[[T], KHashable] | KHashable, seq: Iterable[T]) -> dict[KHashable, list[T]]:
	"""Group a collection by a key function

	>>> names = ['Alice', 'Bob', 'Charlie', 'Dan', 'Edith', 'Frank']
	>>> groupby(len, names)  # doctest: +SKIP
	{3: ['Bob', 'Dan'], 5: ['Alice', 'Edith', 'Frank'], 7: ['Charlie']}

	>>> iseven = lambda x: x % 2 == 0
	>>> groupby(iseven, [1, 2, 3, 4, 5, 6, 7, 8])  # doctest: +SKIP
	{False: [1, 3, 5, 7], True: [2, 4, 6, 8]}

	Non-callable keys imply grouping on a member.

	>>> groupby('gender', [{'name': 'Alice', 'gender': 'F'},
	...                    {'name': 'Bob', 'gender': 'M'},
	...                    {'name': 'Charlie', 'gender': 'M'}]) # doctest:+SKIP
	{'F': [{'gender': 'F', 'name': 'Alice'}],
	 'M': [{'gender': 'M', 'name': 'Bob'},
		   {'gender': 'M', 'name': 'Charlie'}]}

	Not to be confused with ``itertools.groupby``

	See Also
	--------
		countby
	"""
	if not callable(key):
		predicate: Callable[[SupportsGetItem[KHashable, T]], tuple[T]] = getter(key)
	else:
		predicate = key
	d: defaultdict[KHashable, list[T]] = defaultdict(list)
	for item in seq:
		d[predicate(item)].append(item)
	return dict(d)

def interleave(seqs: Iterable[Iterable[T]]) -> Iterator[T]:
	"""Interleave a sequence of sequences

	>>> list(interleave([[1, 2], [3, 4]]))
	[1, 3, 2, 4]

	>>> ''.join(interleave(('ABC', 'XY')))
	'AXBYC'

	Both the individual sequences and the sequence of sequences may be infinite

	Returns a lazy iterator
	"""
	iters: Iterator[Iterator[T]] = itertools.cycle(map(iter, seqs))
	while True:
		try:
			for itr in iters:
				yield next(itr)
			return
		except StopIteration:
			predicate: Callable[[Iterator[T]], bool] = partial(is_not, itr)
			iters = itertools.cycle(itertools.takewhile(predicate, iters))

def interpose(el: T, seq: Iterable[T]) -> Iterator[T]:
	"""Introduce element between each pair of elements in seq

	>>> list(interpose("a", [1, 2, 3]))
	[1, 'a', 2, 'a', 3]
	"""
	interposed: Iterator[T] = concat(zip(itertools.repeat(el), seq))
	next(interposed)
	return interposed

def isdistinct(seq: Collection[Any]) -> bool:
	"""All values in sequence are distinct

	>>> isdistinct([1, 2, 3])
	True
	>>> isdistinct([1, 2, 1])
	False

	>>> isdistinct("Hello")
	False
	>>> isdistinct("World")
	True
	"""
	if iter(seq) is seq:
		seen: set[Any] = set()
		seen_add: Callable[[Any], None] = seen.add
		for item in seq:
			if item in seen:
				return False
			seen_add(item)
		return True
	else:
		return len(seq) == len(set(seq))

@overload
def isiterable(x: TIterable) -> TypeIs[TIterable]: ...
@overload
def isiterable(x: object) -> bool: ...
def isiterable(x: Any) -> bool:
	"""Is x iterable?

	>>> isiterable([1, 2, 3])
	True
	>>> isiterable('abc')
	True
	>>> isiterable(5)
	False
	"""
	try:
		iter(x)
		return True
	except TypeError:
		return False

def iterate(func: Callable[[T], T], x: T) -> Iterator[T]:
	"""Repeatedly apply a function func onto an original input

	Yields x, then func(x), then func(func(x)), then func(func(func(x))), etc..

	>>> def inc(x):  return x + 1
	>>> counter = iterate(inc, 0)
	>>> next(counter)
	0
	>>> next(counter)
	1
	>>> next(counter)
	2

	>>> double = lambda x: x * 2
	>>> powers_of_two = iterate(double, 1)
	>>> next(powers_of_two)
	1
	>>> next(powers_of_two)
	2
	>>> next(powers_of_two)
	4
	>>> next(powers_of_two)
	8
	"""
	while True:
		yield x
		x = func(x)

# === CALLABLE + CALLABLE (4 overloads) ===
@overload
def join(
	leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U]
) -> Iterator[tuple[T, U]]: ...
@overload
def join(
	leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U], left_default: L
) -> Iterator[tuple[T | L, U]]: ...
@overload
def join(
	leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U], *, right_default: R
) -> Iterator[tuple[T, U | R]]: ...
@overload
def join(
	leftkey: Callable[[T], Hashable],
	leftseq: Iterable[T],
	rightkey: Callable[[U], Hashable],
	rightseq: Iterable[U],
	left_default: L,
	right_default: R,
) -> Iterator[tuple[T | L, U | R]]: ...

# === HASHABLE + CALLABLE (4 overloads) ===
@overload
def join(
	leftkey: Hashable, leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U]
) -> Iterator[tuple[T, U]]: ...
@overload
def join(
	leftkey: Hashable, leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U], left_default: L
) -> Iterator[tuple[T | L, U]]: ...
@overload
def join(
	leftkey: Hashable, leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U], *, right_default: R
) -> Iterator[tuple[T, U | R]]: ...
@overload
def join(
	leftkey: Hashable, leftseq: Iterable[T], rightkey: Callable[[U], Hashable], rightseq: Iterable[U], left_default: L, right_default: R
) -> Iterator[tuple[T | L, U | R]]: ...

# === CALLABLE + HASHABLE (4 overloads) ===
@overload
def join(
	leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Hashable, rightseq: Iterable[U]
) -> Iterator[tuple[T, U]]: ...
@overload
def join(
	leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Hashable, rightseq: Iterable[U], left_default: L
) -> Iterator[tuple[T | L, U]]: ...
@overload
def join(
	leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Hashable, rightseq: Iterable[U], *, right_default: R
) -> Iterator[tuple[T, U | R]]: ...
@overload
def join(
	leftkey: Callable[[T], Hashable], leftseq: Iterable[T], rightkey: Hashable, rightseq: Iterable[U], left_default: L, right_default: R
) -> Iterator[tuple[T | L, U | R]]: ...

# === HASHABLE + HASHABLE (4 overloads) ===
@overload
def join(leftkey: Hashable, leftseq: Iterable[T], rightkey: Hashable, rightseq: Iterable[U]) -> Iterator[tuple[T, U]]: ...
@overload
def join(
	leftkey: Hashable, leftseq: Iterable[T], rightkey: Hashable, rightseq: Iterable[U], left_default: L
) -> Iterator[tuple[T | L, U]]: ...
@overload
def join(
	leftkey: Hashable, leftseq: Iterable[T], rightkey: Hashable, rightseq: Iterable[U], *, right_default: R
) -> Iterator[tuple[T, U | R]]: ...
@overload
def join(
	leftkey: Hashable, leftseq: Iterable[T], rightkey: Hashable, rightseq: Iterable[U], left_default: L, right_default: R
) -> Iterator[tuple[T | L, U | R]]: ...
def join(
	leftkey: Callable[[T], Hashable] | Hashable,
	leftseq: Iterable[T],
	rightkey: Callable[[U], Hashable] | Hashable,
	rightseq: Iterable[U],
	left_default: L | Literal['__no__default__'] = no_default,
	right_default: R | Literal['__no__default__'] = no_default,
) -> Iterator[tuple[T | L, U | R]]:
	"""Join two sequences on common attributes

	This is a semi-streaming operation.  The LEFT sequence is fully evaluated
	and placed into memory.  The RIGHT sequence is evaluated lazily and so can
	be arbitrarily large.

	(Note: If right_default is defined, then unique keys of rightseq
		will also be stored in memory.)

	>>> friends = [('Alice', 'Edith'),
	...            ('Alice', 'Zhao'),
	...            ('Edith', 'Alice'),
	...            ('Zhao', 'Alice'),
	...            ('Zhao', 'Edith')]

	>>> cities = [('Alice', 'NYC'),
	...           ('Alice', 'Chicago'),
	...           ('Dan', 'Sydney'),
	...           ('Edith', 'Paris'),
	...           ('Edith', 'Berlin'),
	...           ('Zhao', 'Shanghai')]

	>>> # Vacation opportunities
	>>> # In what cities do people have friends?
	>>> result = join(second, friends,
	...               first, cities)
	>>> for ((a, b), (c, d)) in sorted(unique(result)):
	...     print((a, d))
	('Alice', 'Berlin')
	('Alice', 'Paris')
	('Alice', 'Shanghai')
	('Edith', 'Chicago')
	('Edith', 'NYC')
	('Zhao', 'Chicago')
	('Zhao', 'NYC')
	('Zhao', 'Berlin')
	('Zhao', 'Paris')

	Specify outer joins with keyword arguments ``left_default`` and/or
	``right_default``.  Here is a full outer join in which unmatched elements
	are paired with None.

	>>> identity = lambda x: x
	>>> list(join(identity, [1, 2, 3],
	...           identity, [2, 3, 4],
	...           left_default=None, right_default=None))
	[(2, 2), (3, 3), (None, 4), (1, None)]

	Usually the key arguments are callables to be applied to the sequences.  If
	the keys are not obviously callable then it is assumed that indexing was
	intended, e.g. the following is a legal change.
	The join is implemented as a hash join and the keys of leftseq must be
	hashable. Additionally, if right_default is defined, then keys of rightseq
	must also be hashable.

	>>> # result = join(second, friends, first, cities)
	>>> result = join(1, friends, 0, cities)  # doctest: +SKIP
	"""
	if not callable(leftkey):
		leftkey = getter(leftkey)
	if not callable(rightkey):
		rightkey = getter(rightkey)
	d: dict[Hashable, list[T]] = groupby(leftkey, leftseq)
	if left_default == no_default and right_default == no_default:
		for item in rightseq:
			key = rightkey(item)
			if key in d:
				for left_match in d[key]:
					yield (left_match, item)
	elif left_default != no_default and right_default == no_default:
		for item in rightseq:
			key = rightkey(item)
			if key in d:
				for left_match in d[key]:
					yield (left_match, item)
			else:
				yield (left_default, item)
	elif right_default != no_default:
		seen_keys: set[Hashable] = set()
		seen: Callable[[Hashable], None] = seen_keys.add
		if left_default == no_default:
			for item in rightseq:
				key: Hashable = rightkey(item)
				seen(key)
				if key in d:
					for left_match in d[key]:
						yield (left_match, item)
		else:
			for item in rightseq:
				key = rightkey(item)
				seen(key)
				if key in d:
					for left_match in d[key]:
						yield (left_match, item)
				else:
					yield (left_default, item)
		for key, matches in d.items():
			if key not in seen_keys:
				for match in matches:
					yield (match, right_default)

def last(seq: Iterable[T]) -> T:
	"""The last element in a sequence

	>>> last('ABC')
	'C'
	"""
	return tail(1, seq)[0]

def mapcat(func: Callable[[T], Iterable[R]], seqs: Iterable[T]) -> Iterator[R]:
	"""Apply func to each sequence in seqs, concatenating results.

	>>> list(mapcat(lambda s: [c.upper() for c in s],
	...             [["a", "b"], ["c", "d", "e"]]))
	['A', 'B', 'C', 'D', 'E']
	"""
	return concat(map(func, seqs))

def _merge_sorted_binary(seqs: Sequence[Iterable[SupportsDunderLT[Any]]]) -> Iterator[SupportsDunderLT[Any]]:
	mid: int = len(seqs) // 2
	L1: Sequence[Iterable[SupportsDunderLT[Any]]] = seqs[:mid]
	if len(L1) == 1:
		seq1: Iterator[SupportsDunderLT[Any]] = iter(L1[0])
	else:
		seq1 = _merge_sorted_binary(L1)
	L2: Sequence[Iterable[SupportsDunderLT[Any]]] = seqs[mid:]
	if len(L2) == 1:
		seq2: Iterator[SupportsDunderLT[Any]] = iter(L2[0])
	else:
		seq2 = _merge_sorted_binary(L2)
	try:
		val2: SupportsDunderLT[Any] = next(seq2)
	except StopIteration:
		yield from seq1
		return
	for val1 in seq1:
		if val2 < val1:
			yield val2
			for val2 in seq2:
				if val2 < val1:
					yield val2
				else:
					yield val1
					break
			else:
				break
		else:
			yield val1
	else:
		yield val2
		yield from seq2
		return
	yield val1
	yield from seq1

def _merge_sorted_binary_key(seqs: Sequence[Iterable[T]], key: Callable[[T], SupportsDunderLT[Any]]) -> Iterator[T]:
	mid: int = len(seqs) // 2
	L1: Sequence[Iterable[T]] = seqs[:mid]
	if len(L1) == 1:
		seq1: Iterator[T] = iter(L1[0])
	else:
		seq1 = _merge_sorted_binary_key(L1, key)
	L2: Sequence[Iterable[T]] = seqs[mid:]
	if len(L2) == 1:
		seq2: Iterator[T] = iter(L2[0])
	else:
		seq2 = _merge_sorted_binary_key(L2, key)
	try:
		val2: T = next(seq2)
	except StopIteration:
		yield from seq1
		return
	key2: SupportsDunderLT[Any] = key(val2)
	for val1 in seq1:
		key1: SupportsDunderLT[Any] = key(val1)
		if key2 < key1:
			yield val2
			for val2 in seq2:
				key2 = key(val2)
				if key2 < key1:
					yield val2
				else:
					yield val1
					break
			else:
				break
		else:
			yield val1
	else:
		yield val2
		yield from seq2
		return
	yield val1
	yield from seq1

@overload
def merge_sorted(*seqs: Iterable[TSupportsRichComparison], key: None = None) -> Iterator[TSupportsRichComparison]: ...
@overload
def merge_sorted(*seqs: Iterable[T], key: Callable[[T], SupportsDunderLT[Any]]) -> Iterator[T]: ...
def merge_sorted(*seqs: Iterable[T], key: Callable[[T], SupportsDunderLT[Any]] | None = None) -> Iterator[T]:
	"""Merge and sort a collection of sorted collections

	This works lazily and only keeps one value from each iterable in memory.

	>>> list(merge_sorted([1, 3, 5], [2, 4, 6]))
	[1, 2, 3, 4, 5, 6]

	>>> ''.join(merge_sorted('abc', 'abc', 'abc'))
	'aaabbbccc'

	The "key" function used to sort the input may be passed as a keyword.

	>>> list(merge_sorted([2, 3], [1, 3], key=lambda x: x // 3))
	[2, 1, 3, 3]
	"""
	if len(seqs) == 0:
		return iter([])
	elif len(seqs) == 1:
		return iter(seqs[0])
	if key is None:
		return _merge_sorted_binary(seqs)
	else:
		return _merge_sorted_binary_key(seqs, key)

def nth(n: int, seq: Iterable[T]) -> T:
	"""The nth element in a sequence

	>>> nth(1, 'ABC')
	'B'
	"""
	if isinstance(seq, (tuple, list, Sequence)):
		return seq[n]
	else:
		return next(itertools.islice(seq, n, None))

def partition(n: int, seq: Iterable[T], pad: P | Literal['__no__pad__'] = no_pad) -> Iterator[tuple[T, ...]] | Iterator[tuple[T | P, ...]]:
	"""Partition sequence into tuples of length n

	>>> list(partition(2, [1, 2, 3, 4]))
	[(1, 2), (3, 4)]

	If the length of ``seq`` is not evenly divisible by ``n``, the final tuple
	is dropped if ``pad`` is not specified, or filled to length ``n`` by pad:

	>>> list(partition(2, [1, 2, 3, 4, 5]))
	[(1, 2), (3, 4)]

	>>> list(partition(2, [1, 2, 3, 4, 5], pad=None))
	[(1, 2), (3, 4), (5, None)]

	See Also
	--------
		partition_all
	"""
	args: list[Iterator[T]] = [iter(seq)] * n
	if pad == no_pad:
		return zip(*args, strict=False)
	else:
		fillvalue: P = pad
		return zip_longest(*args, fillvalue=fillvalue)

def partition_all(n: int, seq: Iterable[T]) -> Iterator[tuple[T, ...]]:
	"""Partition all elements of sequence into tuples of length at most n

	The final tuple may be shorter to accommodate extra elements.

	>>> list(partition_all(2, [1, 2, 3, 4]))
	[(1, 2), (3, 4)]

	>>> list(partition_all(2, [1, 2, 3, 4, 5]))
	[(1, 2), (3, 4), (5,)]

	See Also
	--------
		partition
	"""
	args: list[Iterator[T]] = [iter(seq)] * n
	it: Iterator[tuple[T, ...]] = zip_longest(*args, fillvalue=no_pad)
	try:
		prev: tuple[T, ...] = next(it)
	except StopIteration:
		return
	for item in it:
		yield prev
		prev = item
	if prev[-1] is no_pad:
		try:
			end: int = len(seq) % n
			if prev[end - 1] is no_pad or prev[end] is not no_pad:
				message = 'The sequence passed to `partition_all` has invalid length'
				raise LookupError(message)
			yield prev[:end]
		except TypeError:
			lo, hi = (0, n)
			while lo < hi:
				mid: int = (lo + hi) // 2
				if prev[mid] is no_pad:
					hi: int = mid
				else:
					lo: int = mid + 1
			yield prev[:lo]
	else:
		yield prev

def peek(seq: Iterable[T]) -> tuple[T, Iterator[T]]:
	"""Retrieve the next element of a sequence

	Returns the first element and an iterable equivalent to the original
	sequence, still having the element retrieved.

	>>> seq = [0, 1, 2, 3, 4]
	>>> first, seq = peek(seq)
	>>> first
	0
	>>> list(seq)
	[0, 1, 2, 3, 4]
	"""
	iterator: Iterator[T] = iter(seq)
	item: T = next(iterator)
	return (item, itertools.chain((item,), iterator))

def peekn(n: int, seq: Iterable[T]) -> tuple[tuple[T, ...], Iterator[T]]:
	"""Retrieve the next n elements of a sequence

	Returns a tuple of the first n elements and an iterable equivalent
	to the original, still having the elements retrieved.

	>>> seq = [0, 1, 2, 3, 4]
	>>> first_two, seq = peekn(2, seq)
	>>> first_two
	(0, 1)
	>>> list(seq)
	[0, 1, 2, 3, 4]
	"""
	iterator: Iterator[T] = iter(seq)
	peeked: tuple[T, ...] = tuple(take(n, iterator))
	return (peeked, itertools.chain(iter(peeked), iterator))

@overload
def pluck(ind: list[Any], seqs: Iterable[Sequence[T] | Mapping[Any, T]], default: T | Literal['__no__default__'] = ...) -> Iterator[tuple[T, ...]]: ...
@overload
def pluck(ind: Any, seqs: Iterable[Sequence[T] | Mapping[Any, T]], default: T | Literal['__no__default__'] = ...) -> Iterator[T]: ...
def pluck(ind: Any | list[Any], seqs: Iterable[Sequence[T] | Mapping[Any, T]], default: T | Literal['__no__default__'] = no_default) -> Iterator[T] | Iterator[tuple[T, ...]]:
	"""Plucks an element or several elements from each item in a sequence.

	``pluck`` maps ``itertoolz.get`` over a sequence and returns one or more
	elements of each item in the sequence.

	This is equivalent to running `map(curried.get(ind), seqs)`

	``ind`` can be either a single string/index or a list of strings/indices.
	``seqs`` should be sequence containing sequences or dicts.

	e.g.

	>>> data = [{'id': 1, 'name': 'Cheese'}, {'id': 2, 'name': 'Pies'}]
	>>> list(pluck('name', data))
	['Cheese', 'Pies']
	>>> list(pluck([0, 1], [[1, 2, 3], [4, 5, 7]]))
	[(1, 2), (4, 5)]

	See Also
	--------
		get
		map
	"""
	if default == no_default:
		get: Callable[[SupportsGetItem[Any, T]], tuple[T, ...]] = getter(ind)
		return map(get, seqs)
	elif isinstance(ind, list):
		return (tuple(_get(item, seq, default) for item in ind) for seq in seqs)
	return (_get(ind, seq, default) for seq in seqs)

def random_sample(prob: float, seq: Iterable[T], random_state: Randomable | int | float | str | bytes | bytearray | None = None) -> Iterator[T]:
	"""Return elements from a sequence with probability of prob

	Returns a lazy iterator of random items from seq.

	``random_sample`` considers each item independently and without
	replacement. See below how the first time it returned 13 items and the
	next time it returned 6 items.

	>>> seq = list(range(100))
	>>> list(random_sample(0.1, seq)) # doctest: +SKIP
	[6, 9, 19, 35, 45, 50, 58, 62, 68, 72, 78, 86, 95]
	>>> list(random_sample(0.1, seq)) # doctest: +SKIP
	[6, 44, 54, 61, 69, 94]

	Providing an integer seed for ``random_state`` will result in
	deterministic sampling. Given the same seed it will return the same sample
	every time.

	>>> list(random_sample(0.1, seq, random_state=2016))
	[7, 9, 19, 25, 30, 32, 34, 48, 59, 60, 81, 98]
	>>> list(random_sample(0.1, seq, random_state=2016))
	[7, 9, 19, 25, 30, 32, 34, 48, 59, 60, 81, 98]

	``random_state`` can also be any object with a method ``random`` that
	returns floats between 0.0 and 1.0 (exclusive).

	>>> from random import Random
	>>> randobj = Random(2016)
	>>> list(random_sample(0.1, seq, random_state=randobj))
	[7, 9, 19, 25, 30, 32, 34, 48, 59, 60, 81, 98]
	"""
	if hasattr(random_state, 'random'):
		getNumber: Randomable = cast('Randomable', random_state)
	else:
		from random import Random
		getNumber = Random(random_state)
	return filter(lambda _faux_bool: getNumber.random() < prob, seq)

@overload
def reduceby(key: Callable[[T], K], binop: Callable[[T, T], T], seq: Iterable[T]) -> dict[K, T]: ...
@overload
def reduceby(key: Callable[[T], K], binop: Callable[[T, T], T], seq: Iterable[T], init: T | Callable[[], T]) -> dict[K, T]: ...
@overload
def reduceby(
	key: Any,  # when not callable, use identity function
	binop: Callable[[T, T], T],
	seq: Iterable[T],
) -> dict[T, T]: ...
@overload
def reduceby(
	key: Any,  # when not callable, use identity function
	binop: Callable[[T, T], T],
	seq: Iterable[T],
	init: T | Callable[[], T],
) -> dict[T, T]: ...
def reduceby(key: Callable[[T], K] | Any, binop: Callable[[T, T], T], seq: Iterable[T], init: T | Callable[[], T] | Literal['__no__default__'] = no_default) -> dict[K, T]:
	"""Perform a simultaneous groupby and reduction

	The computation:

	>>> result = reduceby(key, binop, seq, init)      # doctest: +SKIP

	is equivalent to the following:

	>>> def reduction(group):                           # doctest: +SKIP
	...     return reduce(binop, group, init)           # doctest: +SKIP

	>>> groups = groupby(key, seq)                    # doctest: +SKIP
	>>> result = valmap(reduction, groups)              # doctest: +SKIP

	But the former does not build the intermediate groups, allowing it to
	operate in much less space.  This makes it suitable for larger datasets
	that do not fit comfortably in memory

	The ``init`` keyword argument is the default initialization of the
	reduction.  This can be either a constant value like ``0`` or a callable
	like ``lambda : 0`` as might be used in ``defaultdict``.

	Simple Examples
	---------------

	>>> from operator import add, mul
	>>> iseven = lambda x: x % 2 == 0

	>>> data = [1, 2, 3, 4, 5]

	>>> reduceby(iseven, add, data)  # doctest: +SKIP
	{False: 9, True: 6}

	>>> reduceby(iseven, mul, data)  # doctest: +SKIP
	{False: 15, True: 8}

	Complex Example
	---------------

	>>> projects = [{'name': 'build roads', 'state': 'CA', 'cost': 1000000},
	...             {'name': 'fight crime', 'state': 'IL', 'cost': 100000},
	...             {'name': 'help farmers', 'state': 'IL', 'cost': 2000000},
	...             {'name': 'help farmers', 'state': 'CA', 'cost': 200000}]

	>>> reduceby('state',                        # doctest: +SKIP
	...          lambda acc, x: acc + x['cost'],
	...          projects, 0)
	{'CA': 1200000, 'IL': 2100000}

	Example Using ``init``
	----------------------

	>>> def set_add(s, i):
	...     s.add(i)
	...     return s

	>>> reduceby(iseven, set_add, [1, 2, 3, 4, 1, 2, 3], set)  # doctest: +SKIP
	{True:  set([2, 4]),
	 False: set([1, 3])}
	"""
	is_no_default: bool = init == no_default
	if not is_no_default and (not callable(init)):
		_init: T = init
		init = lambda: _init
	if not callable(key):
		key = getter(key)
	d: dict[K, T] = {}
	for item in seq:
		k: K = key(item)
		if k not in d:
			if is_no_default:
				d[k] = item
				continue
			else:
				d[k] = init()
		d[k] = binop(d[k], item)
	return d

def remove(predicate: Callable[[T], bool], seq: Iterable[T]) -> Iterable[T]:
	"""Return those items of sequence for which predicate(item) is False

	>>> def iseven(x):
	...     return x % 2 == 0
	>>> list(remove(iseven, [1, 2, 3, 4]))
	[1, 3]
	"""
	return filterfalse(predicate, seq)

# def rest[T](seq: Iterable[T]) -> Iterable[T]: ...
rest = partial(drop, 1)

def second(seq: Iterable[T]) -> T:
	"""The second element in a sequence

	>>> second('ABC')
	'B'
	"""
	seq = iter(seq)
	next(seq)
	return next(seq)

@overload
def sliding_window(n: Literal[1], seq: Iterable[T]) -> Iterator[tuple[T]]: ...
@overload
def sliding_window(n: Literal[2], seq: Iterable[T]) -> Iterator[tuple[T, T]]: ...
@overload
def sliding_window(n: Literal[3], seq: Iterable[T]) -> Iterator[tuple[T, T, T]]: ...
@overload
def sliding_window(n: Literal[4], seq: Iterable[T]) -> Iterator[tuple[T, T, T, T]]: ...
@overload
def sliding_window(n: Literal[5], seq: Iterable[T]) -> Iterator[tuple[T, T, T, T, T]]: ...
@overload
def sliding_window(n: int, seq: Iterable[T]) -> Iterator[tuple[T, ...]]: ...
def sliding_window(n: int, seq: Iterable[Any]) -> Iterator[tuple[Any, ...]]:
	"""A sequence of overlapping subsequences

	>>> list(sliding_window(2, [1, 2, 3, 4]))
	[(1, 2), (2, 3), (3, 4)]

	This function creates a sliding window suitable for transformations like
	sliding means / smoothing

	>>> mean = lambda seq: float(sum(seq)) / len(seq)
	>>> list(map(mean, sliding_window(2, [1, 2, 3, 4])))
	[1.5, 2.5, 3.5]
	"""
	return zip(*(deque(itertools.islice(it, i), 0) or it for i, it in enumerate(itertools.tee(seq, n))))

@overload
def tail(n: int, seq: SSequence) -> SSequence: ...
@overload
def tail(n: int, seq: Mapping[KHashable, Any]) -> tuple[KHashable, ...]: ...
@overload
def tail(n: int, seq: ItemsView[KHashable, T]) -> tuple[tuple[KHashable, T], ...]: ...
@overload
def tail(n: int, seq: KeysView[KHashable]) -> tuple[KHashable, ...]: ...
@overload
def tail(n: int, seq: ValuesView[T]) -> tuple[T, ...]: ...
def tail(n: int, seq: SSequence | Mapping[KHashable, Any] | ItemsView[KHashable, T] | KeysView[KHashable] | ValuesView[T]) -> SSequence | tuple[KHashable, ...] | tuple[tuple[KHashable, T], ...] | tuple[T, ...]:
	"""The last n elements of a sequence

	>>> tail(2, [10, 20, 30, 40, 50])
	[40, 50]

	See Also
	--------
		drop
		take
	"""
	try:
		return seq[len(seq) - n: None]
	except (TypeError, KeyError):
		return tuple(deque(seq, n))

def take(n: int, seq: Iterable[T]) -> Iterator[T]:
	"""The first n elements of a sequence

	>>> list(take(2, [10, 20, 30, 40, 50]))
	[10, 20]

	See Also
	--------
		drop
		tail
	"""
	return itertools.islice(seq, n)

def take_nth(n: int, seq: Iterable[T]) -> Iterator[T]:
	"""Every nth item in seq

	>>> list(take_nth(2, [10, 20, 30, 40, 50]))
	[10, 30, 50]
	"""
	return itertools.islice(seq, 0, None, n)

@overload
def topk(k: Literal[1], seq: Iterable[T], key: Callable[[T], Any] | None = ...) -> tuple[T]: ...
@overload
def topk(k: Literal[2], seq: Iterable[T], key: Callable[[T], Any] | None = ...) -> tuple[T, T]: ...
@overload
def topk(k: Literal[3], seq: Iterable[T], key: Callable[[T], Any] | None = ...) -> tuple[T, T, T]: ...
@overload
def topk(k: Literal[4], seq: Iterable[T], key: Callable[[T], Any] | None = ...) -> tuple[T, T, T, T]: ...
@overload
def topk(k: Literal[5], seq: Iterable[T], key: Callable[[T], Any] | None = ...) -> tuple[T, T, T, T, T]: ...
@overload
def topk(k: int, seq: Iterable[T], key: Callable[[T], Any] | None = None) -> tuple[T, ...]: ...
def topk(k: int, seq: Iterable[Any], key: Callable[[Any], Any] | None = None) -> tuple[Any, ...]:
	"""Find the k largest elements of a sequence

	Operates lazily in ``n*log(k)`` time

	>>> topk(2, [1, 100, 10, 1000])
	(1000, 100)

	Use a key function to change sorted order

	>>> topk(2, ['Alice', 'Bob', 'Charlie', 'Dan'], key=len)
	('Charlie', 'Alice')

	See Also
	--------
		heapq.nlargest
	"""
	if key is not None and (not callable(key)):
		key = getter(key)
	return tuple(heapq.nlargest(k, seq, key=key))

def unique(seq: Iterable[T], key: Callable[[T], Any] | None = None) -> Iterator[T]:
	"""Return only unique elements of a sequence

	>>> tuple(unique((1, 2, 3)))
	(1, 2, 3)
	>>> tuple(unique((1, 2, 1, 3)))
	(1, 2, 3)

	Uniqueness can be defined by key keyword

	>>> tuple(unique(['cat', 'mouse', 'dog', 'hen'], key=len))
	('cat', 'mouse')
	"""
	seen: set[T] = set()
	seen_add: Callable[[T], None] = seen.add
	if key is None:
		for item in seq:
			if item not in seen:
				seen_add(item)
				yield item
	else:
		for item in seq:
			val: T = key(item)
			if val not in seen:
				seen_add(val)
				yield item
