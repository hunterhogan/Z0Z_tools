"""Alternate namespace for `humpy_cytoolz` where functions are curried.

Currying provides implicit partial evaluation of functions.

Examples
--------
`get` usually requires two arguments, an index and a collection.

	>>> from humpy_cytoolz.curried import get
	>>> get(0, ('a', 'b'))
	'a'

When we use it in higher-order functions, we often want a partially evaluated form.

	>>> data = [(1, 2), (11, 22), (111, 222)]
	>>> list(map(get(0), data))
	[1, 11, 111]

See Also
--------
`humpy_cytoolz.functoolz.curry`
"""
# ruff: file-ignore[builtin-import-shadowing, unconventional-import-alias]
from __future__ import annotations

from . import operator as operator
from ._curryFactory import (
	accumulate as accumulate, assoc as assoc, assoc_in as assoc_in, cons as cons, countby as countby, dissoc as dissoc, do as do, drop as drop,
	excepts as excepts, filter as filter, get as get, get_in as get_in, groupby as groupby, interpose as interpose, isdistinct as isdistinct,
	itemfilter as itemfilter, itemmap as itemmap, iterate as iterate, join as join, keyfilter as keyfilter, keymap as keymap, map as map,
	mapcat as mapcat, nth as nth, partial as partial, partition as partition, partition_all as partition_all, partitionby as partitionby,
	peekn as peekn, pluck as pluck, random_sample as random_sample, reduce as reduce, reduceby as reduceby, remove as remove,
	sliding_window as sliding_window, sorted as sorted, tail as tail, take as take, take_nth as take_nth, topk as topk, unique as unique,
	update_in as update_in, valfilter as valfilter, valmap as valmap)
from ._curryHomemade import merge as merge, merge_with as merge_with
from humpy_cytoolz import (
	apply as apply, comp as comp, complement as complement, compose as compose, compose_left as compose_left, concat as concat,
	concatv as concatv, count as count, curry as curry, diff as diff, first as first, flip as flip, frequencies as frequencies,
	identity as identity, interleave as interleave, isiterable as isiterable, juxt as juxt, last as last, memoize as memoize,
	merge_sorted as merge_sorted, peek as peek, pipe as pipe, second as second, thread_first as thread_first, thread_last as thread_last)
