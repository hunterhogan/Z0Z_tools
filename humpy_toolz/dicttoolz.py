# ruff:file-ignore[boolean-default-value-positional-argument]
"""Provide immutable, functional-style operations on `Mapping`[1] objects.

You can use this module to transform, filter, retrieve from, and merge `Mapping`[1] objects without
modifying the source mapping. Each function returns a new mapping created by a `factory` argument that
defaults to `dict`. Functions that navigate nested structures accept a `Sequence`[1] of keys to
specify the path.

Contents
--------
Functions
	assoc
		Create a new `Mapping` with `key` associated with `value`.
	assoc_in
		Create a new `MutableMapping` from `d` with `value` at the path specified by `keys`.
	dissoc
		Create a new `MutableMapping` from `d` with the specified `keys` removed.
	get_in
		Retrieve a value from a potentially nested collection using a sequence of keys.
	itemfilter
		Retain only items from `d` whose key-value pairs satisfy `predicate` and return a new
		`Mapping`.
	itemmap
		Apply `func` to all items of `d` and return a new `Mapping` with the transformed items.
	keyfilter
		Retain only items from `d` whose keys satisfy `predicate` and return a new `Mapping`.
	keymap
		Apply `func` to all keys of `d` and return a new `Mapping` with the transformed keys.
	merge
		Merge a collection of `Mapping` objects and return a new `Mapping`.
	merge_with
		Merge `Mapping` objects and apply a `Callable` to combined values.
	update_in
		Apply a `Callable` to a value at a nested path in a `Mapping`.
	valfilter
		Retain only items from `d` whose values satisfy `predicate` and return a new `Mapping`.
	valmap
		Apply `func` to all values of `d` and return a new `Mapping` with the transformed values.

References
----------
[1] Python `collections.abc` module
	https://docs.python.org/3/library/collections.abc.html
"""
from __future__ import annotations

from collections import defaultdict, deque
from collections.abc import Mapping
from copy import deepcopy
from functools import reduce
from typing import overload, TYPE_CHECKING
import contextlib
import operator

if TYPE_CHECKING:
	from collections.abc import Callable, Hashable, MutableMapping, Sequence
	from optype import CanBool, CanGetitem, CanIter, CanNext
	from typing import Any, TypeGuard
	from typing_extensions import TypeIs

"""# TODO update functions to work with `frozendict`.
# pyright: reportArgumentType=false
# pyright: reportAssignmentType=false
# pyright: reportInconsistentOverload=false
# pyright: reportReturnType=false
# ty:ignore[invalid-assignment]
# ty:ignore[invalid-return-type]"""
__all__ = (
	'assoc',
	'assoc_in',
	'dissoc',
	'get_in',
	'itemfilter',
	'itemmap',
	'keyfilter',
	'keymap',
	'merge',
	'merge_with',
	'update_in',
	'valfilter',
	'valmap',
)

@overload
def assoc[K: Hashable, V](d: Mapping[K, V], key: K, value: V, factory: Callable[[], dict[K, V]] = dict) -> dict[K, V]: ...
@overload
def assoc[K: Hashable, V](
	d: Mapping[K, V], key: K, value: V, factory: Callable[[], MutableMapping[K, V]]
) -> MutableMapping[K, V]: ...
def assoc[K: Hashable, V](
	d: Mapping[K, V], key: K, value: V, factory: Callable[[], MutableMapping[K, V]] = dict
) -> MutableMapping[K, V]:
	"""Create a new `Mapping`[1] with `key` associated with `value`.

	You can use `assoc` (***assoc***iate) to copy `d` (***d***ictionary) to a new `Mapping` created by
	`factory` and assign `value` to `key`. `assoc` does not change `d`.

	Parameters
	----------
	d : Mapping[K, V]
		Source `Mapping`.
	key : K
		`key` that `assoc` inserts or replaces.
	value : V
		`value` that `assoc` assigns to `key`.
	factory : Callable[[], MutableMapping[K, V]] = dict
		`Callable` that creates the `MutableMapping`[1] to `return`.

	Returns
	-------
	mappingUpdated : MutableMapping[K, V]
		New `Mapping` with `key` associated to `value`.

	Examples
	--------
	>>> assoc({}, 'a', 1)
	{'a': 1}
	>>> assoc({'a': 1}, 'a', 3)
	{'a': 3}
	>>> assoc({'a': 1}, 'b', 3)
	{'a': 1, 'b': 3}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	d2: MutableMapping[K, V] = factory()
	d2.update(d)
	d2[key] = value
	return d2

# Overloads for nested dictionaries with tuple keys (2-level nesting)
@overload
def assoc_in[K1: Hashable, K2: Hashable, V2, V1](d: Mapping[K1, Mapping[K2, V2] | V1], keys: tuple[K1, K2], value: V2) -> dict[K1, dict[K2, V2] | V1 | V2]: ...
@overload
def assoc_in[K1: Hashable, K2: Hashable, V2, V1](
	d: Mapping[K1, Mapping[K2, V2] | V1], keys: tuple[K1, K2], value: V2, *, factory: Callable[[], MutableMapping[K1, Any]]
) -> MutableMapping[K1, Any]: ...

# Overloads for nested dictionaries with tuple keys (3-level nesting)
@overload
def assoc_in[K1: Hashable, K2: Hashable, K3: Hashable, V3, V2, V1](
	d: Mapping[K1, Mapping[K2, Mapping[K3, V3] | V2] | V1], keys: tuple[K1, K2, K3], value: V3
) -> dict[K1, dict[K2, dict[K3, V3] | V2 | V3] | V1 | V3]: ...
@overload
def assoc_in[K1: Hashable, K2: Hashable, K3: Hashable, V3, V2, V1](
	d: Mapping[K1, Mapping[K2, Mapping[K3, V3] | V2] | V1],
	keys: tuple[K1, K2, K3],
	value: V3,
	*,
	factory: Callable[[], MutableMapping[K1, Any]],
) -> MutableMapping[K1, Any]: ...

# General overloads for backwards compatibility
@overload
def assoc_in[K: Hashable, V](d: Mapping[K, V], keys: Sequence[K], value: V) -> dict[K, V]: ...
@overload
def assoc_in[K: Hashable, V](d: Mapping[K, V], keys: Sequence[K], value: V, *, factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
def assoc_in[K: Hashable, V](d: Mapping[K, V], keys: Sequence[K], value: V, *, factory: Callable[[], MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
	"""Create a new `MutableMapping` from `d` with `value` at the path specified by `keys`.

	(AI generated docstring)

	You can use `assoc_in` to produce a copy of `d` with `value` placed at the nested
	location given by `keys`. `assoc_in` creates intermediate `MutableMapping` instances
	as needed when a key in `keys` is absent from `d`. `assoc_in` does not mutate `d` or
	any nested `Mapping` within `d`.

	Parameters
	----------
	d : Mapping[K, V]
		Source `Mapping`.
	keys : Iterable[K]
		Non-empty sequence of keys specifying the nested path to the target location in `d`.
	value : V
		The value to place at the location specified by `keys`.
	factory : Callable[[], MutableMapping[K, V]] = dict
		`Callable` that creates each new `MutableMapping`[1] in the result.

	Returns
	-------
	mappingUpdated : MutableMapping[K, V]
		New `MutableMapping` based on `d` with `value` at the path specified by `keys`.

	See Also
	--------
	update_in : Apply a `Callable` to a value at a nested path in a `Mapping`.
	get_in : Retrieve a value at a nested path in a `Mapping`.
	assoc : Create a new `Mapping` from `d` with one key associated to a value.

	Examples
	--------
	>>> assoc_in({'a': 1}, ['a'], 2)
	{'a': 2}
	>>> assoc_in({'a': {'b': 1}}, ['a', 'b'], 2)
	{'a': {'b': 2}}
	>>> assoc_in({}, ['a', 'b'], 1)
	{'a': {'b': 1}}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	return update_in(d, keys, lambda _x: value, value, factory)

@overload
def dissoc[K: Hashable, V](d: Mapping[K, V], *keys: K, factory: Callable[[], dict[K, V]] = dict) -> dict[K, V]: ...
@overload
def dissoc[K: Hashable, V](
	d: Mapping[K, V], *keys: K, factory: Callable[[], MutableMapping[K, V]]
) -> MutableMapping[K, V]: ...
def dissoc[K: Hashable, V](
	d: Mapping[K, V], *keys: K, factory: Callable[[], MutableMapping[K, V]] = dict
) -> MutableMapping[K, V]:
	"""Create a new `MutableMapping`[1] from `d` with the specified `keys` removed.

	(AI generated docstring)

	You can use `dissoc` (***dissoc***iate) to copy `d` (***d***ictionary) to a new `MutableMapping`
	created by `factory`, then remove each key in `keys` from the result. `dissoc` does not change
	`d`. Keys in `keys` that are absent from `d` are silently ignored.

	Parameters
	----------
	d : Mapping[K, V]
		Source `Mapping`.
	*keys : K
		Keys to remove from `d` in the returned `MutableMapping`.
	factory : Callable[[], MutableMapping[K, V]] = dict
		`Callable` that creates the `MutableMapping`[1] to `return`.

	Returns
	-------
	mappingReduced : MutableMapping[K, V]
		New `MutableMapping` containing all items from `d` except those whose keys are in `keys`.

	Algorithm Details
	-----------------
	`dissoc` selects between two strategies based on the ratio of removed keys to total keys.

	When fewer than 60% of keys are removed, `dissoc` copies all items from `d` and then
	deletes the specified keys one by one.

	When 60% or more of keys are removed, `dissoc` computes the set of remaining keys and
	copies only those items to the result, avoiding unnecessary copy-and-delete operations.

	See Also
	--------
	assoc : Create a new `MutableMapping` from `d` with one key associated to a value.

	Examples
	--------
	>>> dissoc({'x': 1, 'y': 2}, 'y')
	{'x': 1}
	>>> dissoc({'x': 1, 'y': 2}, 'y', 'x')
	{}
	>>> dissoc({'x': 1}, 'y')  # Ignores missing keys
	{'x': 1}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	d2: MutableMapping[K, V] = factory()
	if len(keys) < len(d) * 0.6:
		d2.update(d)
		for key in keys:
			if key in d2:
				del d2[key]
	else:
		remaining: set[K] = set(d)
		remaining.difference_update(keys)
		for k in remaining:
			d2[k] = d[k]
	return d2

def get_in[T, R, R2](keys: CanIter[CanNext[T]], coll: CanGetitem[T, R], default: R2 | None = None, no_default: CanBool = False) -> R | R2 | None:
	"""Retrieve a value from a potentially nested `coll` (***coll***ection) using a `Sequence` of `keys`.

	You can use `get_in` to navigate into a nested `coll` (***coll***ection) by following a
	`Sequence` of `keys`. `get_in` applies each key in `keys` sequentially using
	`operator.getitem`[1].

	If the desired key does not exist, `get_in` will `raise` an `Exception` or `return` `default`
	depending on the parameter `no_default`. If `no_default` is `False`, which is the default,
	`get_in` will `return` `default`. If `no_default` is `True`, `get_in` will `raise` an
	`Exception`.

	Parameters
	----------
	keys : Sequence[T]
		`Sequence` of keys that describes the path to traverse in `coll`.
	coll : SupportsGetItem[T, V]
		Python `object` to traverse. `get_in` uses `operator.getitem`[1], so the nested objects in
		`coll` can be nested o any type that works with `operator.getitem`, such as a `dict` or
		`list`.
	default : V | None = None
		Value to return when the path in `keys` does not exist in `coll`.
	no_default : bool = False
		When `True`, `raise` `KeyError`, `IndexError`, or `TypeError` instead of returning `default`.

	Returns
	-------
	value : V | None
		The value at the nested path in `coll`, or `default` if the path does not exist.

	See Also
	--------
	itertoolz.get : Retrieve a value or values from a collection.
	operator.getitem : Return the value at a given key in a collection.
	assoc_in : Create a new `Mapping` from `d` with a value at a nested path.
	update_in : Apply a `Callable` to a value at a nested path in a `Mapping`.

	Examples
	--------
	>>> transaction = {
	...     'name': 'Alice',
	...     'purchase': {'items': ['Apple', 'Orange'], 'costs': [0.50, 1.25]},
	...     'credit card': '5555-1234-1234-1234',
	... }
	>>> get_in(['purchase', 'items', 0], transaction)
	'Apple'
	>>> get_in(['name'], transaction)
	'Alice'
	>>> get_in(['purchase', 'total'], transaction)
	>>> get_in(['purchase', 'items', 'apple'], transaction)
	>>> get_in(['purchase', 'items', 10], transaction)
	>>> get_in(['purchase', 'total'], transaction, 0)
	0
	>>> get_in(['y'], {}, no_default=True)
	Traceback (most recent call last):
		...
	KeyError: 'y'

	References
	----------
	[1] Python `operator` module
		https://docs.python.org/3/library/operator.html#operator.getitem
	"""
	if no_default:
		return reduce(operator.getitem, keys, coll)
	else:
		v: R | R2 | None = default
		with contextlib.suppress(KeyError, IndexError, TypeError):
			v = reduce(operator.getitem, keys, coll)
		return v

@overload
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](
	predicate: Callable[[tuple[K0, V0]], TypeIs[tuple[K1, V1]]],
	d: Mapping[K0, V0],
	factory: Callable[[], dict[K1, V1]] = dict,
) -> dict[K1, V1]: ...
@overload
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](
	predicate: Callable[[tuple[K0, V0]], TypeGuard[tuple[K1, V1]]],
	d: Mapping[K0, V0],
	factory: Callable[[], dict[K1, V1]] = dict,
) -> dict[K1, V1]: ...
@overload
def itemfilter[K: Hashable, V](
	predicate: Callable[[tuple[K, V]], bool], d: Mapping[K, V], factory: Callable[[], dict[K, V]] = dict
) -> dict[K, V]: ...
@overload
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](
	predicate: Callable[[tuple[K0, V0]], TypeIs[tuple[K1, V1]]],
	d: Mapping[K0, V0],
	factory: Callable[[], MutableMapping[K1, V1]],
) -> MutableMapping[K1, V1]: ...
@overload
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](
	predicate: Callable[[tuple[K0, V0]], TypeGuard[tuple[K1, V1]]],
	d: Mapping[K0, V0],
	factory: Callable[[], MutableMapping[K1, V1]],
) -> MutableMapping[K1, V1]: ...
@overload
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](
	predicate: Callable[[tuple[K0, V0]], bool], d: Mapping[K0, V0], factory: Callable[[], MutableMapping[K1, V1]]
) -> MutableMapping[K1, V1]: ...
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](
	predicate: Callable[[tuple[K0, V0]], bool]
	| Callable[[tuple[K0, V0]], TypeGuard[tuple[K1, V1]]]
	| Callable[[tuple[K0, V0]], TypeIs[tuple[K1, V1]]],
	d: Mapping[K0, V0],
	factory: Callable[[], MutableMapping[K1, V1]] = dict,
) -> MutableMapping[K1, V1]:
	"""Retain only items from `d` whose key-value pairs satisfy `predicate` and return a new `Mapping`.

	(AI generated docstring)

	You can use `itemfilter` to select items from `d` (***d***ictionary) by both key and value
	simultaneously. `itemfilter` calls `predicate` with each item yielded by `d.items()`. Each
	item is passed to `predicate` as a `tuple[K, V]`. `itemfilter` inserts each item for which
	`predicate` returns `True` into a new `MutableMapping`[1] created by `factory`. `itemfilter`
	does not change `d`.

	Parameters
	----------
	predicate : Callable[[tuple[K, V]], bool]
		`Callable` applied to each item of `d`. Each item is passed to `predicate` as a
		`tuple[K, V]`, and `predicate` must return `True` for the item to be retained.
	d : Mapping[K, V]
		Source `Mapping`[1]. `itemfilter` reads all items from `d` and does not change `d`.
	factory : Callable[[], MutableMapping[K, V]] = dict
		`Callable` that creates the `MutableMapping`[1] to `return`.

	Returns
	-------
	mappingFiltered : MutableMapping[K, V]
		New `MutableMapping` created by `factory` containing only items from `d` for which
		`predicate` returns `True`.

	See Also
	--------
	keyfilter : Retain only items from `d` whose keys satisfy `predicate` and return a new `Mapping`.
	valfilter : Retain only items from `d` whose values satisfy `predicate` and return a new `Mapping`.
	itemmap : Apply a `Callable` to all items of a `Mapping` and return a new `Mapping`.

	Examples
	--------
	>>> def isvalid(item):
	...     k, v = item
	...     return k % 2 == 0 and v < 4

	>>> d = {1: 2, 2: 3, 3: 4, 4: 5}
	>>> itemfilter(isvalid, d)
	{2: 3}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	rv: MutableMapping[K1, V1] = factory()
	for item in d.items():
		if predicate(item):
			k, v = item
			rv[k] = v
	return rv

@overload
def itemmap[K0: Hashable, V0, K1: Hashable, V1](
	func: Callable[[tuple[K0, V0]], tuple[K1, V1]],
	d: Mapping[K0, V0],
	factory: Callable[..., dict[K1, V1]] = dict,
) -> dict[K1, V1]: ...
@overload
def itemmap[K0: Hashable, V0, K1: Hashable, V1](
	func: Callable[[tuple[K0, V0]], tuple[K1, V1]],
	d: Mapping[K0, V0],
	factory: Callable[..., MutableMapping[K1, V1]],
) -> MutableMapping[K1, V1]: ...
def itemmap[K0: Hashable, V0, K1: Hashable, V1](
	func: Callable[[tuple[K0, V0]], tuple[K1, V1]],
	d: Mapping[K0, V0],
	factory: Callable[..., MutableMapping[K1, V1]] = dict,
) -> MutableMapping[K1, V1]:
	"""Apply `func` to all items of `d` and return a new `Mapping` with the transformed items.

	(AI generated docstring)

	You can use `itemmap` to transform all keys and values in `d` simultaneously without
	changing `d`. `itemmap` applies `func` to each item yielded by `d.items()`. Each item
	is passed to `func` as a `tuple[K, V]`, and `func` must return a `tuple[L, W]`. `itemmap`
	inserts each returned `tuple` as a new key-value pair in a `MutableMapping`[1] created
	by `factory`.

	Parameters
	----------
	func : Callable[[tuple[K, V]], tuple[L, W]]
		`Callable` applied to each item of `d`. Each item of `d` is passed to `func` as a
		`tuple[K, V]`, and `func` must return a `tuple[L, W]` containing the new key and value.
	d : Mapping[K, V]
		Source `Mapping`[1]. `itemmap` reads all items from `d` and does not change `d`.
	factory : Callable[[], MutableMapping[L, W]] = dict
		`Callable` that creates the `MutableMapping`[1] to `return`.

	Returns
	-------
	mappingTransformed : MutableMapping[L, W]
		New `MutableMapping` created by `factory` populated with each `tuple[L, W]` returned
		by `func`.

	See Also
	--------
	keymap : Apply a `Callable` to all keys of a `Mapping` and return a new `Mapping`.
	valmap : Apply a `Callable` to all values of a `Mapping` and return a new `Mapping`.

	Examples
	--------
	>>> accountids = {'Alice': 10, 'Bob': 20}
	>>> itemmap(reversed, accountids)  # doctest: +SKIP
	{10: 'Alice', 20: 'Bob'}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	return factory(map(func, d.items()))

@overload
def keyfilter[K0: Hashable, K1: Hashable, V](
	predicate: Callable[[K0], TypeIs[K1]], d: Mapping[K0, V], factory: Callable[[], dict[K1, V]] = dict
) -> dict[K1, V]: ...
@overload
def keyfilter[K0: Hashable, K1: Hashable, V](
	predicate: Callable[[K0], TypeGuard[K1]], d: Mapping[K0, V], factory: Callable[[], dict[K1, V]] = dict
) -> dict[K1, V]: ...
@overload
def keyfilter[K: Hashable, V](
	predicate: Callable[[K], bool], d: Mapping[K, V], factory: Callable[[], dict[K, V]] = dict
) -> dict[K, V]: ...
@overload
def keyfilter[K0: Hashable, K1: Hashable, V](
	predicate: Callable[[K0], TypeIs[K1]], d: Mapping[K0, V], factory: Callable[[], MutableMapping[K1, V]]
) -> MutableMapping[K1, V]: ...
@overload
def keyfilter[K0: Hashable, K1: Hashable, V](
	predicate: Callable[[K0], TypeGuard[K1]],
	d: Mapping[K0, V],
	factory: Callable[[], MutableMapping[K1, V]],
) -> MutableMapping[K1, V]: ...
@overload
def keyfilter[K0: Hashable, V, K1: Hashable](
	predicate: Callable[[K0], bool], d: Mapping[K0, V], factory: Callable[[], MutableMapping[K1, V]]
) -> MutableMapping[K1, V]: ...
def keyfilter[K0: Hashable, K1: Hashable, V](
	predicate: Callable[[K0], bool] | Callable[[K0], TypeGuard[K1]] | Callable[[K0], TypeIs[K1]],
	d: Mapping[K0, V],
	factory: Callable[[], MutableMapping[K1, V]] = dict,
) -> MutableMapping[K1, V]:
	"""Retain only items from `d` whose keys satisfy `predicate` and return a new `Mapping`.

	(AI generated docstring)

	You can use `keyfilter` to select items from `d` (***d***ictionary) by their keys. `keyfilter`
	calls `predicate` with each key yielded by `d.keys()`. `keyfilter` inserts each item whose
	key causes `predicate` to return `True` into a new `MutableMapping`[1] created by `factory`.
	`keyfilter` does not change `d`.

	Parameters
	----------
	predicate : Callable[[K], bool]
		`Callable` applied to each key of `d`. `keyfilter` keeps each item for which `predicate`
		returns `True`.
	d : Mapping[K, V]
		Source `Mapping`[1]. `keyfilter` reads all items from `d` and does not change `d`.
	factory : Callable[[], MutableMapping[K, V]] = dict
		`Callable` that creates the `MutableMapping`[1] to `return`.

	Returns
	-------
	mappingFiltered : MutableMapping[K, V]
		New `MutableMapping` created by `factory` containing only items from `d` whose keys
		cause `predicate` to return `True`.

	See Also
	--------
	valfilter : Retain only items from `d` whose values satisfy `predicate` and return a new `Mapping`.
	itemfilter : Retain only items from `d` whose key-value pairs satisfy `predicate` and return a new `Mapping`.
	keymap : Apply a `Callable` to all keys of a `Mapping` and return a new `Mapping`.

	Examples
	--------
	>>> iseven = lambda x: x % 2 == 0
	>>> d = {1: 2, 2: 3, 3: 4, 4: 5}
	>>> keyfilter(iseven, d)
	{2: 3, 4: 5}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	rv: MutableMapping[K1, V] = factory()
	for k, v in d.items():
		if predicate(k):
			rv[k] = v
	return rv

@overload
def keymap[K0: Hashable, K1: Hashable, V](
	func: Callable[[K0], K1], d: Mapping[K0, V], factory: Callable[[], dict[K1, V]] = dict
) -> dict[K1, V]: ...
@overload
def keymap[K0: Hashable, K1: Hashable, V](
	func: Callable[[K0], K1], d: Mapping[K0, V], factory: Callable[[], MutableMapping[K1, V]]
) -> MutableMapping[K1, V]: ...
def keymap[K0: Hashable, K1: Hashable, V](
	func: Callable[[K0], K1], d: Mapping[K0, V], factory: Callable[[], MutableMapping[K1, V]] = dict
) -> MutableMapping[K1, V]:
	"""Apply `func` to all keys of `d` and return a new `Mapping` with the transformed keys.

	(AI generated docstring)

	You can use `keymap` to transform all keys in `d` without changing `d`. `keymap` applies
	`func` to each key yielded by `d.keys()` and builds a new `MutableMapping`[1] created by
	`factory`, associating each transformed key with the corresponding original value of `d`.

	Parameters
	----------
	func : Callable[[K], L]
		`Callable` applied to each key of `d`. Each key of `d` is passed to `func`
		individually, and `func` returns the corresponding transformed key.
	d : Mapping[K, V]
		Source `Mapping`[1]. `keymap` reads all keys from `d` and does not change `d`.
	factory : Callable[[], MutableMapping[L, V]] = dict
		`Callable` that creates the `MutableMapping`[1] to `return`.

	Returns
	-------
	mappingTransformed : MutableMapping[L, V]
		New `MutableMapping` created by `factory` in which each key from `d` is replaced by
		the result of applying `func` to that key, associated with the original value of `d`.

	See Also
	--------
	valmap : Apply a `Callable` to all values of a `Mapping` and return a new `Mapping`.
	itemmap : Apply a `Callable` to all items of a `Mapping` and return a new `Mapping`.

	Examples
	--------
	>>> bills = {'Alice': [20, 15, 30], 'Bob': [10, 35]}
	>>> keymap(str.lower, bills)  # doctest: +SKIP
	{'alice': [20, 15, 30], 'bob': [10, 35]}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	rv: MutableMapping[K1, V] = factory()
	rv.update(zip(map(func, d.keys()), d.values(), strict=True))
	return rv

# TODO Think about: the `*dicts` need not be homogeneous.
# TODO Think about: the `*dicts` need not match the factory.
# TODO Think about: the `*dicts` need not match the return.
@overload
def merge[K: Hashable, V](*dicts: Mapping[K, V], factory: Callable[[], dict[K, V]] = dict) -> dict[K, V]: ...
@overload
def merge[K: Hashable, V](*dicts: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
def merge[K: Hashable, V](*dicts: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
	"""Merge a collection of dictionaries and return a new `Mapping`.

	(AI generated docstring)

	You can use `merge` to combine two or more `Mapping`[1] objects into a single new `Mapping`.
	`merge` calls `factory` to create the result, then updates it in order with each `Mapping` in
	`dicts`. When the same key appears in more than one element, the value from the later element
	takes precedence. You can also pass a single `Iterable[Mapping[K, V]]` as the sole positional
	argument instead of multiple `Mapping` arguments.

	Parameters
	----------
	*dicts : Mapping[K, V]
		`Mapping` objects to merge. Alternatively, pass a single `Iterable[Mapping[K, V]]` as the
		sole positional argument.
	factory : Callable[[], MutableMapping[K, V]] = dict
		`Callable` that creates the `MutableMapping`[1] to `return`.

	Returns
	-------
	mappingMerged : MutableMapping[K, V]
		New `MutableMapping` created by `factory` containing all key-value pairs from `dicts`. For
		duplicate keys, the value from the last `Mapping` in `dicts` that contains the key takes
		precedence.

	See Also
	--------
	merge_with : Merge dictionaries and apply a `Callable` to combined values.

	Examples
	--------
	>>> merge({1: 'one'}, {2: 'two'})
	{1: 'one', 2: 'two'}

	Later dictionaries have precedence

	>>> merge({1: 2, 3: 4}, {3: 3, 4: 4})
	{1: 2, 3: 3, 4: 4}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	if len(dicts) == 1 and not isinstance(dicts[0], Mapping):
		dicts = dicts[0]
	rv: MutableMapping[K, V] = factory()
	for d in dicts:
		rv.update(d)
	return rv

@overload
def merge_with[V, K: Hashable](
	func: Callable[[Sequence[V]], V], *dicts: Mapping[K, V], factory: Callable[[], dict[K, V]] = dict
) -> dict[K, V]: ...
@overload
def merge_with[V, K: Hashable](
	func: Callable[[Sequence[V]], V], *dicts: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]]
) -> MutableMapping[K, V]: ...
def merge_with[V, K: Hashable](
	func: Callable[[Sequence[V]], V], *dicts: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]] = dict
) -> MutableMapping[K, V]:
	"""Merge dictionaries and apply a `Callable` to combined values.

	(AI generated docstring)

	You can use `merge_with` to combine two or more `Mapping`[1] objects and resolve key conflicts
	by applying `func` to a `list` of all values associated with each key. For each key that
	appears in one or more elements of `dicts`, `merge_with` collects all associated values into a
	`list` in the order they appear across `dicts`, then calls `func` with that `list` to produce
	the value in the result. You can also pass a single `Iterable[Mapping[K, V]]` as the sole
	positional argument after `func`.

	Parameters
	----------
	func : Callable[[list[V]], V]
		`Callable` applied to the `list` of values associated with each key across all `Mapping`
		objects in `dicts`. `func` receives a non-empty `list` and must return the merged value for
		that key.
	*dicts : Mapping[K, V]
		`Mapping` objects to merge. Alternatively, pass a single `Iterable[Mapping[K, V]]` as the
		sole positional argument after `func`.
	factory : Callable[[], MutableMapping[K, V]] = dict
		`Callable` that creates the `MutableMapping`[1] to `return`.

	Returns
	-------
	mappingMerged : MutableMapping[K, V]
		New `MutableMapping` created by `factory` where each key maps to the result of calling
		`func` with all values associated with that key across `dicts`.

	See Also
	--------
	merge : Merge a collection of `Mapping` objects into a new `Mapping`.

	Examples
	--------
	>>> merge_with(sum, {1: 1, 2: 2}, {1: 10, 2: 20})
	{1: 11, 2: 22}

	>>> merge_with(first, {1: 1, 2: 2}, {2: 20, 3: 30})  # doctest: +SKIP
	{1: 1, 2: 2, 3: 30}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	if len(dicts) == 1 and not isinstance(dicts[0], Mapping):
		dicts = dicts[0]
	groupedValues: defaultdict[K, list[V]] = defaultdict(list)
	for d in dicts:
		for k, v in d.items():
			groupedValues[k].append(v)
	rv: MutableMapping[K, V] = factory()
	for k, valueList in groupedValues.items():
		rv[k] = func(valueList)
	return rv

def update_in[K: Hashable, V_co](
	d: Mapping[K, Mapping[K, V_co] | V_co]
	, keys: Sequence[K]
	, func: Callable[[V_co | None], V_co] | Callable[[V_co], V_co]
	, default: V_co | None = None
	, factory: Callable[..., Mapping[K, Mapping[K, V_co] | V_co]] = dict
) -> Mapping[K, Mapping[K, V_co] | V_co]:
	"""Apply a `Callable` to a value at a nested path in a `Mapping`.

	(AI generated docstring)

	You can use `update_in` to produce a copy of `d` with the value at the nested path
	specified by `keys` replaced by the result of calling `func` on the current value.
	`update_in` creates intermediate `MutableMapping` instances as needed when a key in
	`keys` is absent from `d`. If the innermost key is absent, `func` receives `default`
	instead of an existing value. `update_in` does not mutate `d` or any nested `Mapping`
	within `d`.

	Parameters
	----------
	d : Mapping[K, V_co]
		Source `Mapping`.
	keys : Sequence[K]
		Non-empty sequence of keys specifying the nested path to the value to update in `d`.
	func : Callable[[V_co], V_co] | Callable[[V_co | None], V_co]
		`Callable` applied to the current value at the path in `keys`. If the innermost
		key is absent from `d`, `func` receives `default`.
	default : V_co | None = None
		Value passed to `func` when the innermost key is absent from `d`.
	factory : Callable[[], MutableMapping[K, V_co]] = dict
		`Callable` that creates each new `MutableMapping`[1] in the result.

	Returns
	-------
	mappingUpdated : MutableMapping[K, V_co]
		New `MutableMapping` based on `d` with the value at the path specified by `keys`
		replaced by the result of `func`.

	See Also
	--------
	assoc_in : Create a new `Mapping` from `d` with a value at a nested path.
	get_in : Retrieve a value at a nested path in a `Mapping`.
	assoc : Create a new `Mapping` from `d` with one key associated to a value.

	Examples
	--------
	>>> inc = lambda x: x + 1
	>>> update_in({'a': 0}, ['a'], inc)
	{'a': 1}

	>>> update_in({}, ['z'], inc, 0)
	{'z': 1}

	>>> update_in({}, [1, 2, 3], str, default='bar')
	{1: {2: {3: 'bar'}}}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	# DEVELOPMENT Python 3.15 includes `builtins.frozendict`, which does not have `__setitem__`, and
	# could be passed as `factory`.
	# https://docs.python.org/3.15/whatsnew/3.15.html#pep-814-add-frozendict-built-in-type

	# DEVELOPMENT The original toolz function applied `factory` to every _existing_ mapping, as
	# opposed to only using it to create a new mapping. That's excessive.
	# - If the user wants the topmost mapping to be the same type as `factory`, for example, the user
	#   can easily call factory before or after `update_in`. So, it should not be applied to the
	#   topmost mapping.
	# - If `d` has nested heterogenous mappings, applying `factory` homogenizes the mappings of
	#   `keys`. `update_in` is supposed to update one value: that doesn't imply or require altering
	#   the `type` of any existing mapping.

	#---------- Initialize. --------------------------------------------------
	# DEVELOPMENT preserves the original `type`.
	returnMe: Mapping[K, Mapping[K, V_co] | V_co] = deepcopy(d)
	# DEVELOPMENT The mutable containers in `returnMe` can be changed by modifying `mappingATkey`.
	mappingATkey: Mapping[K, Mapping[K, V_co] | V_co] = returnMe
	sherpa: Mapping[K, Mapping[K, V_co] | V_co] = deepcopy(d)
	dequeKeys: deque[K] = deque(keys)

	keyFinal: K = dequeKeys.pop()

	#--------- From outermost mapping, `d`, get or construct innermost mapping --------------
	while dequeKeys:
		# DEVELOPMENT Never fails:
		key: K = dequeKeys.popleft()
		# DEVELOPMENT Never fails:
		sherpa = sherpa.get(key, factory())

		try:
			# DEVELOPMENT `mappingATkey = sherpa` never fails.
			# DEVELOPMENT `mappingATkey[key]` raises exception if `setitem` isn't available.
			mappingATkey[key] = mappingATkey = sherpa  # pyright: ignore[reportIndexIssue]
		except TypeError:
			reconstructor = type(mappingATkey)
			mappingATkey = dict(mappingATkey)
			operator.setitem(mappingATkey, key, sherpa)  # pyright: ignore[reportCallIssue]  # ty:ignore[no-matching-overload]
			mappingATkey = reconstructor(mappingATkey)  # pyright: ignore[reportCallIssue]  # ty:ignore[too-many-positional-arguments]
			mappingATkey = sherpa

		del key

	#--------- Compute value at location `keys` --------------------------
	# DEVELOPMENT Never fails:
	valueUpdated: V_co = func(sherpa.get(keyFinal, default))  # ty:ignore[invalid-argument-type]
	del default, dequeKeys, func, sherpa

	#--------- Innermost `mapping[keys[-1]] = func(mapping.get(keys[-1], default))` -----------
	try:
		# DEVELOPMENT `mappingATkey[keyFinal]` raises exception if `setitem` isn't available.
		mappingATkey[keyFinal] = valueUpdated  # pyright: ignore[reportIndexIssue]
	except TypeError:
		reconstructor = type(mappingATkey)
		mappingATkey = dict(mappingATkey)
		operator.setitem(mappingATkey, keyFinal, valueUpdated)
		mappingATkey = reconstructor(mappingATkey)  # pyright: ignore[reportCallIssue]  # ty:ignore[too-many-positional-arguments]

	return returnMe

@overload
def valfilter[K: Hashable, T, V](predicate: Callable[[T], TypeIs[V]], d: Mapping[K, T], factory: Callable[[], dict[K, V]] = dict) -> dict[K, V]: ...
@overload
def valfilter[K: Hashable, T, V](predicate: Callable[[T], TypeGuard[V]], d: Mapping[K, T], factory: Callable[[], dict[K, V]] = dict) -> dict[K, V]: ...
@overload
def valfilter[K: Hashable, T, V](predicate: Callable[[V], bool], d: Mapping[K, T], factory: Callable[[], dict[K, V]] = dict) -> dict[K, V]: ...
@overload
def valfilter[K: Hashable, T, V](predicate: Callable[[T], TypeIs[V]], d: Mapping[K, T], factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
@overload
def valfilter[K: Hashable, T, V](predicate: Callable[[T], TypeGuard[V]], d: Mapping[K, T], factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
@overload
def valfilter[K: Hashable, T, V](predicate: Callable[[T], bool], d: Mapping[K, T], factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
def valfilter[K: Hashable, T, V](
	predicate: Callable[[T], bool] | Callable[[T], TypeIs[V]] | Callable[[T], TypeGuard[V]]
	, d: Mapping[K, T]
	, factory: Callable[[], dict[K, V]] | Callable[[], MutableMapping[K, V]] = dict
) -> dict[K, V] | MutableMapping[K, V]:
	"""Retain only items from `d` whose values satisfy `predicate` and return a new `Mapping`.

	(AI generated docstring)

	You can use `valfilter` to select items from `d` (***d***ictionary) by their values. `valfilter`
	calls `predicate` with each value yielded by `d.values()`. `valfilter` inserts each item whose
	value causes `predicate` to return `True` into a new `MutableMapping`[1] created by `factory`.
	`valfilter` does not change `d`.

	Parameters
	----------
	predicate : Callable[[V], bool]
		`Callable` applied to each value of `d`. `valfilter` keeps each item for which `predicate`
		returns `True`.
	d : Mapping[K, V]
		Source `Mapping`[1]. `valfilter` reads all items from `d` and does not change `d`.
	factory : Callable[[], MutableMapping[K, V]] = dict
		`Callable` that creates the `MutableMapping`[1] to `return`.

	Returns
	-------
	mappingFiltered : MutableMapping[K, V]
		New `MutableMapping` created by `factory` containing only items from `d` whose values
		cause `predicate` to return `True`.

	See Also
	--------
	keyfilter : Retain only items from `d` whose keys satisfy `predicate` and return a new `Mapping`.
	itemfilter : Retain only items from `d` whose key-value pairs satisfy `predicate` and return a new `Mapping`.
	valmap : Apply a `Callable` to all values of a `Mapping` and return a new `Mapping`.

	Examples
	--------
	>>> iseven = lambda x: x % 2 == 0
	>>> d = {1: 2, 2: 3, 3: 4, 4: 5}
	>>> valfilter(iseven, d)
	{1: 2, 3: 4}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	returnMe: MutableMapping[K, V] = factory()
	for k, v in d.items():
		if predicate(v):
			returnMe[k] = v
	return returnMe

@overload
def valmap[V0, V1, K: Hashable](
	func: Callable[[V0], V1], d: Mapping[K, V0], factory: Callable[[], dict[K, V1]] = dict
) -> dict[K, V1]: ...
@overload
def valmap[V0, V1, K: Hashable](
	func: Callable[[V0], V1], d: Mapping[K, V0], factory: Callable[[], MutableMapping[K, V1]]
) -> MutableMapping[K, V1]: ...
def valmap[V0, V1, K: Hashable](
	func: Callable[[V0], V1], d: Mapping[K, V0], factory: Callable[[], MutableMapping[K, V1]] = dict
) -> MutableMapping[K, V1]:
	"""Apply `func` to all values of `d` and return a new `Mapping` with the transformed values.

	(AI generated docstring)

	You can use `valmap` to transform all values in `d` without changing `d`. `valmap` applies
	`func` to each value yielded by `d.values()` and builds a new `MutableMapping`[1] created
	by `factory`, preserving each original key associated with its transformed value.

	Parameters
	----------
	func : Callable[[V], W]
		`Callable` applied to each value of `d`. Each value of `d` is passed to `func`
		individually, and `func` returns the corresponding transformed value.
	d : Mapping[K, V]
		Source `Mapping`[1]. `valmap` reads all values from `d` and does not change `d`.
	factory : Callable[[], MutableMapping[K, W]] = dict
		`Callable` that creates the `MutableMapping`[1] to `return`.

	Returns
	-------
	mappingTransformed : MutableMapping[K, W]
		New `MutableMapping` created by `factory` in which each key from `d` is associated
		with the result of applying `func` to the corresponding value of `d`.

	See Also
	--------
	keymap : Apply a `Callable` to all keys of a `Mapping` and return a new `Mapping`.
	itemmap : Apply a `Callable` to all items of a `Mapping` and return a new `Mapping`.

	Examples
	--------
	>>> bills = {'Alice': [20, 15, 30], 'Bob': [10, 35]}
	>>> valmap(sum, bills)  # doctest: +SKIP
	{'Alice': 65, 'Bob': 45}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	rv: MutableMapping[K, V1] = factory()
	rv.update(zip(d.keys(), map(func, d.values()), strict=True))
	return rv
