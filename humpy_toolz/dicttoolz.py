"""Provide immutable, functional-style operations on `Mapping`[1] objects.

(AI generated docstring)

You can use this module to transform, filter, retrieve from, and merge `Mapping`[1] objects
without modifying the source mapping. Each function returns a new mapping created by a
`factory` argument that defaults to `dict`. Functions that navigate nested structures accept
a `Sequence`[1] of keys to specify the path.

Contents
--------
Classes
	SupportsGetItem
		Structural type constraint for objects that support item retrieval via `__getitem__`.

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
		Retain only items from `d` whose key-value pairs satisfy `predicate` and return a new `Mapping`.
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
from collections.abc import Callable, Hashable, Mapping, MutableMapping, Sequence
from functools import reduce
from typing import Any, cast, Literal, overload, TYPE_CHECKING, TypeGuard
from typing_extensions import TypeIs
import contextlib
import operator

if TYPE_CHECKING:
	from humpy_toolz.utils import SupportsGetItem

__all__ = ('assoc', 'assoc_in', 'dissoc', 'get_in', 'itemfilter', 'itemmap', 'keyfilter', 'keymap', 'merge', 'merge_with', 'update_in', 'valfilter', 'valmap')

@overload
def assoc[K: Hashable, V](d: Mapping[K, V], key: K, value: V, factory: Callable[[], dict[K, V]] = dict) -> dict[K, V]: ...
@overload
def assoc[K: Hashable, V](d: Mapping[K, V], key: K, value: V, factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
def assoc[K: Hashable, V](d: Mapping[K, V], key: K, value: V, factory: Callable[[], MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
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
def assoc_in[K1, K2, V1, V2](d: Mapping[K1, Mapping[K2, V2] | V1], keys: tuple[K1, K2], value: V2) -> dict[K1, dict[K2, V2] | V1 | V2]: ...
@overload
def assoc_in[K1, K2, V1, V2](d: Mapping[K1, Mapping[K2, V2] | V1], keys: tuple[K1, K2], value: V2, *, factory: Callable[[], MutableMapping[K1, Any]]) -> MutableMapping[K1, Any]: ...

# Overloads for nested dictionaries with tuple keys (3-level nesting)
@overload
def assoc_in[K1, K2, K3, V1, V2, V3](d: Mapping[K1, Mapping[K2, Mapping[K3, V3] | V2] | V1], keys: tuple[K1, K2, K3], value: V3) -> dict[K1, dict[K2, dict[K3, V3] | V2 | V3] | V1 | V3]: ...
@overload
def assoc_in[K1, K2, K3, V1, V2, V3](d: Mapping[K1, Mapping[K2, Mapping[K3, V3] | V2] | V1], keys: tuple[K1, K2, K3], value: V3, *, factory: Callable[[], MutableMapping[K1, Any]]) -> MutableMapping[K1, Any]: ...

# General overloads for backwards compatibility
@overload
def assoc_in[K, V](d: Mapping[K, V], keys: Sequence[K], value: V) -> dict[K, V]: ...
@overload
def assoc_in[K, V](d: Mapping[K, V], keys: Sequence[K], value: V, *, factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
def assoc_in[K, V](d: Mapping[K, V], keys: Sequence[K], value: V, *, factory: Callable[[], MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:  # pyright: ignore[reportInconsistentOverload]
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
def dissoc[K: Hashable, V](d: Mapping[K, V], *keys: K, factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
def dissoc[K: Hashable, V](d: Mapping[K, V], *keys: K, factory: Callable[[], MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
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
	>>> dissoc({'x': 1}, 'y') # Ignores missing keys
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

@overload
def get_in[K, V](keys: Sequence[K], coll: Sequence[V] | SupportsGetItem[K, V], default: None = None, *, no_default: Literal[True]) -> V: ...
@overload
def get_in[K, V](keys: Sequence[K], coll: Sequence[V] | SupportsGetItem[K, V], default: V, no_default: Literal[True]) -> V: ...
@overload
def get_in[K, V0, V1](keys: Sequence[K], coll: Sequence[V0] | SupportsGetItem[K, V0], default: V1, no_default: bool = False) -> V0 | V1: ...  # noqa: FBT001, FBT002
@overload
def get_in[K, V](keys: Sequence[K], coll: Sequence[V] | SupportsGetItem[K, V], default: None = None, no_default: bool = False) -> V | None: ...  # noqa: FBT001, FBT002
def get_in[K, V0, V1](keys: Sequence[K], coll: Sequence[V0] | SupportsGetItem[K, V0], default: V1 | None = None, no_default: bool = False) -> V0 | V1 | None:  # noqa: FBT001, FBT002
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
	keys : Sequence[K]
		`Sequence` of keys that describes the path to traverse in `coll`.
	coll : SupportsGetItem[K, V]
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

	Raises
	------
	KeyError
		When `no_default` is `True` and a key is missing from a mapping.
	IndexError
		When `no_default` is `True` and an index is out of range.
	TypeError
		When `no_default` is `True` and a key type is incompatible with `coll`.

	See Also
	--------
	itertoolz.get : Retrieve a value or values from a collection.
	operator.getitem : Return the value at a given key in a collection.
	assoc_in : Create a new `Mapping` from `d` with a value at a nested path.
	update_in : Apply a `Callable` to a value at a nested path in a `Mapping`.

	Examples
	--------
	>>> transaction = {'name': 'Alice',
	...                'purchase': {'items': ['Apple', 'Orange'],
	...                             'costs': [0.50, 1.25]},
	...                'credit card': '5555-1234-1234-1234'}
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
		return reduce(operator.getitem, keys, coll)  # pyright: ignore[reportArgumentType, reportReturnType] # ty:ignore[invalid-return-type]
	else:
		v: V1 | None = default
		with contextlib.suppress(KeyError, IndexError, TypeError):
			v = reduce(operator.getitem, keys, coll)  # pyright: ignore[reportAssignmentType, reportArgumentType] # ty:ignore[invalid-assignment]
		return v
	try:
		return reduce(operator.getitem, keys, coll)
	except (KeyError, IndexError, TypeError):
		if no_default:
			raise
		return default

@overload
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](predicate: Callable[[tuple[K0, V0]], TypeIs[tuple[K1, V1]]], d: Mapping[K0, V0], factory: Callable[[], dict[K1, V1]] = dict) -> dict[K1, V1]: ...
@overload
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](predicate: Callable[[tuple[K0, V0]], TypeGuard[tuple[K1, V1]]], d: Mapping[K0, V0], factory: Callable[[], dict[K1, V1]] = dict) -> dict[K1, V1]: ...
@overload
def itemfilter[K: Hashable, V](predicate: Callable[[tuple[K, V]], bool], d: Mapping[K, V], factory: Callable[[], dict[K, V]] = dict) -> dict[K, V]: ...
@overload
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](predicate: Callable[[tuple[K0, V0]], TypeIs[tuple[K1, V1]]], d: Mapping[K0, V0], factory: Callable[[], MutableMapping[K1, V1]]) -> MutableMapping[K1, V1]: ...
@overload
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](predicate: Callable[[tuple[K0, V0]], TypeGuard[tuple[K1, V1]]], d: Mapping[K0, V0], factory: Callable[[], MutableMapping[K1, V1]]) -> MutableMapping[K1, V1]: ...
@overload
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](predicate: Callable[[tuple[K0, V0]], bool], d: Mapping[K0, V0], factory: Callable[[], MutableMapping[K1, V1]]) -> MutableMapping[K1, V1]: ...
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](predicate: Callable[[tuple[K0, V0]], bool] | Callable[[tuple[K0, V0]], TypeGuard[tuple[K1, V1]]] | Callable[[tuple[K0, V0]], TypeIs[tuple[K1, V1]]], d: Mapping[K0, V0], factory: Callable[[], MutableMapping[K1, V1]] = dict) -> MutableMapping[K1, V1]:
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
			k, v = cast('tuple[K1, V1]', item)
			rv[k] = v
	return rv

@overload
def itemmap[K0: Hashable, K1: Hashable, V0, V1](func: Callable[[tuple[K0, V0]], tuple[K1, V1]], d: Mapping[K0, V0], factory: Callable[..., dict[K1, V1]] = dict) -> dict[K1, V1]: ...
@overload
def itemmap[K0: Hashable, K1: Hashable, V0, V1](func: Callable[[tuple[K0, V0]], tuple[K1, V1]], d: Mapping[K0, V0], factory: Callable[..., MutableMapping[K1, V1]]) -> MutableMapping[K1, V1]: ...
def itemmap[K0: Hashable, K1: Hashable, V0, V1](func: Callable[[tuple[K0, V0]], tuple[K1, V1]], d: Mapping[K0, V0], factory: Callable[..., MutableMapping[K1, V1]] = dict) -> MutableMapping[K1, V1]:
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
def keyfilter[K0: Hashable, K1: Hashable, V](predicate: Callable[[K0], TypeIs[K1]], d: Mapping[K0, V], factory: Callable[[], dict[K1, V]] = dict) -> dict[K1, V]: ...
@overload
def keyfilter[K0: Hashable, K1: Hashable, V](predicate: Callable[[K0], TypeGuard[K1]], d: Mapping[K0, V], factory: Callable[[], dict[K1, V]] = dict) -> dict[K1, V]: ...
@overload
def keyfilter[K: Hashable, V](predicate: Callable[[K], bool], d: Mapping[K, V], factory: Callable[[], dict[K, V]] = dict) -> dict[K, V]: ...
@overload
def keyfilter[K0: Hashable, K1: Hashable, V](predicate: Callable[[K0], TypeIs[K1]], d: Mapping[K0, V], factory: Callable[[], MutableMapping[K1, V]]) -> MutableMapping[K1, V]: ...
@overload
def keyfilter[K0: Hashable, K1: Hashable, V](predicate: Callable[[K0], TypeGuard[K1]], d: Mapping[K0, V], factory: Callable[[], MutableMapping[K1, V]]) -> MutableMapping[K1, V]: ...
@overload
def keyfilter[K0: Hashable, K1: Hashable, V](predicate: Callable[[K0], bool], d: Mapping[K0, V], factory: Callable[[], MutableMapping[K1, V]]) -> MutableMapping[K1, V]: ...
def keyfilter[K0: Hashable, K1: Hashable, V](predicate: Callable[[K0], bool] | Callable[[K0], TypeGuard[K1]] | Callable[[K0], TypeIs[K1]], d: Mapping[K0, V], factory: Callable[[], MutableMapping[K1, V]] = dict) -> MutableMapping[K1, V]:
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
			rv[cast('K1', k)] = v
	return rv

@overload
def keymap[K0: Hashable, K1: Hashable, V](func: Callable[[K0], K1], d: Mapping[K0, V], factory: Callable[[], dict[K1, V]] = dict) -> dict[K1, V]: ...
@overload
def keymap[K0: Hashable, K1: Hashable, V](func: Callable[[K0], K1], d: Mapping[K0, V], factory: Callable[[], MutableMapping[K1, V]]) -> MutableMapping[K1, V]: ...
def keymap[K0: Hashable, K1: Hashable, V](func: Callable[[K0], K1], d: Mapping[K0, V], factory: Callable[[], MutableMapping[K1, V]] = dict) -> MutableMapping[K1, V]:
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
def merge_with[K: Hashable, V](func: Callable[[Sequence[V]], V], *dicts: Mapping[K, V], factory: Callable[[], dict[K, V]] = dict) -> dict[K, V]: ...
@overload
def merge_with[K: Hashable, V](func: Callable[[Sequence[V]], V], *dicts: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
def merge_with[K: Hashable, V](func: Callable[[Sequence[V]], V], *dicts: Mapping[K, V], factory: Callable[[], MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
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

# TODO Given `d: dict[str, int | str]`. It does not follow that `func: Callable[[int | str], int | str]`
@overload
def update_in[K, V](d: Mapping[K, V], keys: Sequence[K], func: Callable[[V | None], V], default: None = None, *, factory: Callable[..., MutableMapping[K, V]] = dict) -> dict[K, V]: ...
@overload
def update_in[K, V](d: Mapping[K, V], keys: Sequence[K], func: Callable[[V], V], default: V, factory: Callable[..., MutableMapping[K, V]] = dict) -> dict[K, V]: ...
@overload
def update_in[K, V](d: Mapping[K, V], keys: Sequence[K], func: Callable[[V | None], V], default: None = None, *, factory: Callable[..., MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
@overload
def update_in[K, V](d: Mapping[K, V], keys: Sequence[K], func: Callable[[V], V], default: V, factory: Callable[..., MutableMapping[K, V]]) -> MutableMapping[K, V]: ...
def update_in[K, V](d: Mapping[K, V], keys: Sequence[K], func: Callable[[V | None], V] | Callable[[V], V], default: V | None = None, factory: Callable[..., MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
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
	d : Mapping[K, V]
		Source `Mapping`.
	keys : Sequence[K]
		Non-empty sequence of keys specifying the nested path to the value to update in `d`.
	func : Callable[[V], V]
		`Callable` applied to the current value at the path in `keys`. If the innermost
		key is absent from `d`, `func` receives `default`.
	default : V | None = None
		Value passed to `func` when the innermost key is absent from `d`.
	factory : Callable[[], MutableMapping[K, V]] = dict
		`Callable` that creates each new `MutableMapping`[1] in the result.

	Returns
	-------
	mappingUpdated : MutableMapping[K, V]
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

	>>> update_in({}, [1, 2, 3], str, default="bar")
	{1: {2: {3: 'bar'}}}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	rv = dATk = factory(d)
	dequeKeys: deque[K] = deque(keys)
	keyFinal: K = dequeKeys.pop()
	sherpa: MutableMapping[K, V] = factory(d)
	while dequeKeys:
		k: K = dequeKeys.popleft()
		sherpa = cast('MutableMapping[K, V]', sherpa.get(k, factory()))
		dATk[k] = dATk = factory(sherpa)  # pyright: ignore[reportArgumentType] # ty:ignore[invalid-assignment]
	dATk[keyFinal] = func(sherpa.get(keyFinal, default))  # pyright: ignore[reportArgumentType] # ty:ignore[invalid-argument-type]
	return rv

@overload
def valfilter[K: Hashable, V0, V1](predicate: Callable[[V0], TypeIs[V1]], d: Mapping[K, V0], factory: Callable[[], dict[K, V1]] = dict) -> dict[K, V1]: ...
@overload
def valfilter[K: Hashable, V0, V1](predicate: Callable[[V0], TypeGuard[V1]], d: Mapping[K, V0], factory: Callable[[], dict[K, V1]] = dict) -> dict[K, V1]: ...
@overload
def valfilter[K: Hashable, V](predicate: Callable[[V], bool], d: Mapping[K, V]) -> dict[K, V]: ...
@overload
def valfilter[K: Hashable, V0, V1](predicate: Callable[[V0], TypeIs[V1]], d: Mapping[K, V0], factory: Callable[[], MutableMapping[K, V1]]) -> MutableMapping[K, V1]: ...
@overload
def valfilter[K: Hashable, V0, V1](predicate: Callable[[V0], TypeGuard[V1]], d: Mapping[K, V0], factory: Callable[[], MutableMapping[K, V1]]) -> MutableMapping[K, V1]: ...
@overload
def valfilter[K: Hashable, V0, V1](predicate: Callable[[V0], bool], d: Mapping[K, V0], factory: Callable[[], MutableMapping[K, V1]]) -> MutableMapping[K, V1]: ...

def valfilter[K: Hashable, V0, V1](predicate: Callable[[V0], bool] | Callable[[V0], TypeGuard[V1]] | Callable[[V0], TypeIs[V1]], d: Mapping[K, V0], factory: Callable[[], MutableMapping[K, V1]] = dict) -> MutableMapping[K, V1]:
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
	rv: MutableMapping[K, V1] = factory()
	for k, v in d.items():
		if predicate(v):
			rv[k] = cast('V1', v)
	return rv

@overload
def valmap[K: Hashable, V0, V1](func: Callable[[V0], V1], d: Mapping[K, V0], factory: Callable[[], dict[K, V1]] = dict) -> dict[K, V1]: ...
@overload
def valmap[K: Hashable, V0, V1](func: Callable[[V0], V1], d: Mapping[K, V0], factory: Callable[[], MutableMapping[K, V1]]) -> MutableMapping[K, V1]: ...
def valmap[K: Hashable, V0, V1](func: Callable[[V0], V1], d: Mapping[K, V0], factory: Callable[[], MutableMapping[K, V1]] = dict) -> MutableMapping[K, V1]:
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
