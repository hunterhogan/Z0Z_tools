# pyright: reportUnknownVariableType=false
# ruff: noqa: D104 RUF067 F403 A004 PLC0415 F405, SLF001
from __future__ import annotations

from .dicttoolz import *
from .functoolz import *
from .itertoolz import *
from .recipes import *
from builtins import filter as filter, map as map, sorted as sorted
from functools import partial as partial, reduce as reduce
from humpy_toolz.dicttoolz import (
	assoc as assoc, assoc_in as assoc_in, dissoc as dissoc, get_in as get_in, itemfilter as itemfilter, itemmap as itemmap,
	keyfilter as keyfilter, keymap as keymap, merge as merge, merge_with as merge_with, update_in as update_in, valfilter as valfilter,
	valmap as valmap)
from humpy_toolz.functoolz import (
	apply as apply, complement as complement, compose as compose, compose_left as compose_left, curry as curry, do as do, excepts as excepts,
	flip as flip, identity as identity, juxt as juxt, memoize as memoize, pipe as pipe, thread_first as thread_first,
	thread_last as thread_last)
from humpy_toolz.itertoolz import (
	accumulate as accumulate, concat as concat, concatv as concatv, cons as cons, count as count, diff as diff, drop as drop, first as first,
	frequencies as frequencies, get as get, groupby as groupby, interleave as interleave, interpose as interpose, isdistinct as isdistinct,
	isiterable as isiterable, iterate as iterate, join as join, last as last, mapcat as mapcat, merge_sorted as merge_sorted, nth as nth,
	partition as partition, partition_all as partition_all, peek as peek, peekn as peekn, pluck as pluck, random_sample as random_sample,
	reduceby as reduceby, remove as remove, second as second, sliding_window as sliding_window, tail as tail, take as take,
	take_nth as take_nth, topk as topk, unique as unique)
from humpy_toolz.recipes import countby as countby, partitionby as partitionby

comp = compose

__version__: str = '1.1.0'

functoolz._sigs.create_signature_registry()

def __getattr__(name: str) -> str:
    if name == '__version__':
        from importlib.metadata import version
        rv: str = version('humpy_toolz')
        globals()[name] = rv
        return rv
    message: str = f'module {__name__!r} has no attribute {name!r}'
    raise AttributeError(message)
