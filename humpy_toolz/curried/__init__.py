# ruff:file-ignore[builtin-import-shadowing] `filter`, `map`, `pow`, `sorted`
"""
Alternate namespace for toolz such that all functions are curried

Currying provides implicit partial evaluation of all functions

Example:

	Get usually requires two arguments, an index and a collection
	>>> from humpy_toolz.curried import get
	>>> get(0, ('a', 'b'))
	'a'

	When we use it in higher order functions we often want to pass a partially
	evaluated form
	>>> data = [(1, 2), (11, 22), (111, 222)]
	>>> list(map(lambda seq: get(0, seq), data))
	[1, 11, 111]

	The curried version allows simple expression of partial evaluation
	>>> list(map(get(0), data))
	[1, 11, 111]

See Also
--------
	humpy_toolz.functoolz.curry
"""

from __future__ import annotations

from humpy_toolz import (
	apply as apply, comp as comp, complement as complement, compose as compose, compose_left as compose_left, concat as concat,
	concatv as concatv, count as count, curry as curry, diff as diff, first as first, flip as flip, frequencies as frequencies,
	identity as identity, interleave as interleave, isdistinct as isdistinct, isiterable as isiterable, juxt as juxt, last as last,
	memoize as memoize, merge_sorted as merge_sorted, peek as peek, pipe as pipe, second as second, thread_first as thread_first,
	thread_last as thread_last)
from humpy_toolz.curried import operator as operator
from humpy_toolz.curried.exceptions import merge as merge, merge_with as merge_with
from humpy_toolz.curried.toolz import (
	accumulate as accumulate, assoc as assoc, assoc_in as assoc_in, cons as cons, countby as countby, dissoc as dissoc, do as do, drop as drop,
	excepts as excepts, filter as filter, get as get, get_in as get_in, groupby as groupby, interpose as interpose, itemfilter as itemfilter,
	itemmap as itemmap, iterate as iterate, join as join, keyfilter as keyfilter, keymap as keymap, map as map, mapcat as mapcat, nth as nth,
	partial as partial, partition as partition, partition_all as partition_all, partitionby as partitionby, peekn as peekn, pluck as pluck,
	random_sample as random_sample, reduce as reduce, reduceby as reduceby, remove as remove, sliding_window as sliding_window,
	sorted as sorted, tail as tail, take as take, take_nth as take_nth, topk as topk, unique as unique, update_in as update_in,
	valfilter as valfilter, valmap as valmap)

# Re-exported, not curried
__all__: list[str] = [
	'apply',
	'comp',
	'complement',
	'compose',
	'compose_left',
	'concat',
	'concatv',
	'count',
	'curry',
	'diff',
	'first',
	'flip',
	'frequencies',
	'identity',
	'interleave',
	'isdistinct',
	'isiterable',
	'juxt',
	'last',
	'memoize',
	'merge_sorted',
	'peek',
	'pipe',
	'second',
	'thread_first',
	'thread_last']

# Re-exported submodule
__all__ += [
	'operator',
]

# Re-exported from exceptions
__all__ += [
	'merge',
	'merge_with',
]

# Curried functions
__all__ += [
	'accumulate',
	'assoc',
	'assoc_in',
	'cons',
	'countby',
	'dissoc',
	'do',
	'drop',
	'excepts',
	'filter',
	'get',
	'get_in',
	'groupby',
	'interpose',
	'itemfilter',
	'itemmap',
	'iterate',
	'join',
	'keyfilter',
	'keymap',
	'map',
	'mapcat',
	'nth',
	'partial',
	'partition',
	'partition_all',
	'partitionby',
	'peekn',
	'pluck',
	'random_sample',
	'reduce',
	'reduceby',
	'remove',
	'sliding_window',
	'sorted',
	'tail',
	'take',
	'take_nth',
	'topk',
	'unique',
	'update_in',
	'valfilter',
	'valmap',
]
