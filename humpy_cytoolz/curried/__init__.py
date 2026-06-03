"""
Alternate namespace for cytoolz such that all functions are curried

Currying provides implicit partial evaluation of all functions

Example:

    Get usually requires two arguments, an index and a collection
    >>> from humpy_cytoolz.curried import get
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
    humpy_cytoolz.functoolz.curry
"""
from . import operator
from .exceptions import merge, merge_with
from humpy_cytoolz import (
	apply, comp, complement, compose, compose_left, concat, concatv, count, curry, diff, first, flip, frequencies,
	identity, interleave, isdistinct, isiterable, juxt, last, memoize, merge_sorted, peek, pipe, second, thread_first,
	thread_last)
import humpy_cytoolz

accumulate = humpy_cytoolz.curry(humpy_cytoolz.accumulate)
assoc = humpy_cytoolz.curry(humpy_cytoolz.assoc)
assoc_in = humpy_cytoolz.curry(humpy_cytoolz.assoc_in)
cons = humpy_cytoolz.curry(humpy_cytoolz.cons)
countby = humpy_cytoolz.curry(humpy_cytoolz.countby)
dissoc = humpy_cytoolz.curry(humpy_cytoolz.dissoc)
do = humpy_cytoolz.curry(humpy_cytoolz.do)
drop = humpy_cytoolz.curry(humpy_cytoolz.drop)
excepts = humpy_cytoolz.curry(humpy_cytoolz.excepts)
filter = humpy_cytoolz.curry(humpy_cytoolz.filter)  # noqa: A001
get = humpy_cytoolz.curry(humpy_cytoolz.get)
get_in = humpy_cytoolz.curry(humpy_cytoolz.get_in)
groupby = humpy_cytoolz.curry(humpy_cytoolz.groupby)
interpose = humpy_cytoolz.curry(humpy_cytoolz.interpose)
itemfilter = humpy_cytoolz.curry(humpy_cytoolz.itemfilter)
itemmap = humpy_cytoolz.curry(humpy_cytoolz.itemmap)
iterate = humpy_cytoolz.curry(humpy_cytoolz.iterate)
join = humpy_cytoolz.curry(humpy_cytoolz.join)
keyfilter = humpy_cytoolz.curry(humpy_cytoolz.keyfilter)
keymap = humpy_cytoolz.curry(humpy_cytoolz.keymap)
map = humpy_cytoolz.curry(humpy_cytoolz.map)  # noqa: A001
mapcat = humpy_cytoolz.curry(humpy_cytoolz.mapcat)
nth = humpy_cytoolz.curry(humpy_cytoolz.nth)
partial = humpy_cytoolz.curry(humpy_cytoolz.partial)
partition = humpy_cytoolz.curry(humpy_cytoolz.partition)
partition_all = humpy_cytoolz.curry(humpy_cytoolz.partition_all)
partitionby = humpy_cytoolz.curry(humpy_cytoolz.partitionby)
peekn = humpy_cytoolz.curry(humpy_cytoolz.peekn)
pluck = humpy_cytoolz.curry(humpy_cytoolz.pluck)
random_sample = humpy_cytoolz.curry(humpy_cytoolz.random_sample)
reduce = humpy_cytoolz.curry(humpy_cytoolz.reduce)
reduceby = humpy_cytoolz.curry(humpy_cytoolz.reduceby)
remove = humpy_cytoolz.curry(humpy_cytoolz.remove)
sliding_window = humpy_cytoolz.curry(humpy_cytoolz.sliding_window)
sorted = humpy_cytoolz.curry(humpy_cytoolz.sorted)  # noqa: A001
tail = humpy_cytoolz.curry(humpy_cytoolz.tail)
take = humpy_cytoolz.curry(humpy_cytoolz.take)
take_nth = humpy_cytoolz.curry(humpy_cytoolz.take_nth)
topk = humpy_cytoolz.curry(humpy_cytoolz.topk)
unique = humpy_cytoolz.curry(humpy_cytoolz.unique)
update_in = humpy_cytoolz.curry(humpy_cytoolz.update_in)
valfilter = humpy_cytoolz.curry(humpy_cytoolz.valfilter)
valmap = humpy_cytoolz.curry(humpy_cytoolz.valmap)
del humpy_cytoolz
