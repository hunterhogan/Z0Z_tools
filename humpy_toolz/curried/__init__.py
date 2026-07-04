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
import humpy_toolz

accumulate = humpy_toolz.curry(humpy_toolz.accumulate)
assoc = humpy_toolz.curry(humpy_toolz.assoc)
assoc_in = humpy_toolz.curry(humpy_toolz.assoc_in)
cons = humpy_toolz.curry(humpy_toolz.cons)
countby = humpy_toolz.curry(humpy_toolz.countby)
dissoc = humpy_toolz.curry(humpy_toolz.dissoc)
do = humpy_toolz.curry(humpy_toolz.do)
drop = humpy_toolz.curry(humpy_toolz.drop)
excepts = humpy_toolz.curry(humpy_toolz.excepts)
filter = humpy_toolz.curry(humpy_toolz.filter)
get = humpy_toolz.curry(humpy_toolz.get)
get_in = humpy_toolz.curry(humpy_toolz.get_in)
groupby = humpy_toolz.curry(humpy_toolz.groupby)
interpose = humpy_toolz.curry(humpy_toolz.interpose)
itemfilter = humpy_toolz.curry(humpy_toolz.itemfilter)
itemmap = humpy_toolz.curry(humpy_toolz.itemmap)
iterate = humpy_toolz.curry(humpy_toolz.iterate)
join = humpy_toolz.curry(humpy_toolz.join)
keyfilter = humpy_toolz.curry(humpy_toolz.keyfilter)
keymap = humpy_toolz.curry(humpy_toolz.keymap)
map = humpy_toolz.curry(humpy_toolz.map)
mapcat = humpy_toolz.curry(humpy_toolz.mapcat)
nth = humpy_toolz.curry(humpy_toolz.nth)
partial = humpy_toolz.curry(humpy_toolz.partial)
partition = humpy_toolz.curry(humpy_toolz.partition)
partition_all = humpy_toolz.curry(humpy_toolz.partition_all)
partitionby = humpy_toolz.curry(humpy_toolz.partitionby)
peekn = humpy_toolz.curry(humpy_toolz.peekn)
pluck = humpy_toolz.curry(humpy_toolz.pluck)
random_sample = humpy_toolz.curry(humpy_toolz.random_sample)
reduce = humpy_toolz.curry(humpy_toolz.reduce)
reduceby = humpy_toolz.curry(humpy_toolz.reduceby)
remove = humpy_toolz.curry(humpy_toolz.remove)
sliding_window = humpy_toolz.curry(humpy_toolz.sliding_window)
sorted = humpy_toolz.curry(humpy_toolz.sorted)
tail = humpy_toolz.curry(humpy_toolz.tail)
take = humpy_toolz.curry(humpy_toolz.take)
take_nth = humpy_toolz.curry(humpy_toolz.take_nth)
topk = humpy_toolz.curry(humpy_toolz.topk)
unique = humpy_toolz.curry(humpy_toolz.unique)
update_in = humpy_toolz.curry(humpy_toolz.update_in)
valfilter = humpy_toolz.curry(humpy_toolz.valfilter)
valmap = humpy_toolz.curry(humpy_toolz.valmap)
del humpy_toolz
