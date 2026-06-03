# cython: embedsignature=True
# cython: freethreading_compatible=True
# cython: language_level=3
from cpython.dict cimport (PyDict_Check, PyDict_CheckExact, PyDict_GetItem,
						   PyDict_New, PyDict_Next,
						   PyDict_SetItem, PyDict_Update, PyDict_DelItem)
from cpython.list cimport PyList_Append, PyList_New
from cpython.object cimport PyObject_SetItem
from cpython.ref cimport PyObject, Py_DECREF, Py_INCREF, Py_XDECREF

# Locally defined bindings that differ from `cython.cpython` bindings
from humpy_cytoolz.cpython cimport PyDict_Next_Compat, PtrIter_Next

from collections import abc

# cdef aliases to eliminate global lookups

cdef object Mapping = abc.Mapping
del abc

__all__ = ['merge', 'merge_with', 'valmap', 'keymap', 'itemmap', 'valfilter',
		   'keyfilter', 'itemfilter', 'assoc', 'dissoc', 'assoc_in', 'get_in',
		   'update_in']

cdef class _iter_mapping:
	""" Keep a handle on the current item to prevent memory clean up too early"""
	def __cinit__(self, object it):
		self.it = it
		self.cur = None

	def __iter__(self):
		return self

	def __next__(self):
		self.cur = next(self.it)
		return self.cur

cdef int PyMapping_Next(object p, Py_ssize_t *ppos, PyObject* *pkey, PyObject* *pval) except -1:
	"""Mimic "PyDict_Next" interface, but for any mapping"""
	cdef PyObject *obj
	obj = PtrIter_Next(p)
	if obj is NULL:
		return 0
	pkey[0] = <PyObject*>(<object>obj)[0]
	pval[0] = <PyObject*>(<object>obj)[1]
	Py_XDECREF(obj)  # removing this results in memory leak
	return 1

cdef f_map_next get_map_iter(object d, PyObject* *ptr) except NULL:
	"""Return function pointer to perform iteration over object returned in ptr.

	The returned function signature matches "PyDict_Next".  If ``d`` is a dict,
	then the returned function *is* PyDict_Next, so iteration wil be very fast.

	The object returned through ``ptr`` needs to have its reference count
	reduced by one once the caller "owns" the object.

	This function lets us control exactly how iteration should be performed
	over a given mapping.  The current rules are:

	1) If ``d`` is exactly a dict, use PyDict_Next
	2) If ``d`` is subtype of dict, use PyMapping_Next.  This lets the user
	   control the order iteration, such as for ordereddict.
	3) If using PyMapping_Next, iterate using ``iteritems`` if possible,
	   otherwise iterate using ``items``.

	"""
	cdef object val
	cdef f_map_next rv
	if PyDict_CheckExact(d):
		val = d
		rv = &PyDict_Next_Compat
	else:
		val = _iter_mapping(iter(d.items()))
		rv = &PyMapping_Next
	Py_INCREF(val)
	ptr[0] = <PyObject*>val
	return rv

cdef get_factory(name, kwargs):
	factory = kwargs.pop('factory', dict)
	if kwargs:
		raise TypeError("{0}() got an unexpected keyword argument "
						"'{1}'".format(name, kwargs.popitem()[0]))
	return factory

cdef object c_merge(object dicts, object factory=dict):
	cdef object rv
	rv = factory()
	if PyDict_CheckExact(rv):
		for d in dicts:
			PyDict_Update(rv, d)
	else:
		for d in dicts:
			rv.update(d)
	return rv

def merge(*dicts, factory=dict):
	"""\
merge(*dicts: collections.abc.Mapping[K, V], factory: collections.abc.Callable[[], collections.abc.MutableMapping[K, V]] = dict) -> collections.abc.MutableMapping[K, V]

Merge a collection of dictionaries and return a new `Mapping`.

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
	return c_merge(dicts, factory)

cdef object c_merge_with(object func, object dicts, object factory=dict):
	cdef:
		dict result
		object rv, d
		list seq
		f_map_next f
		PyObject *obj
		PyObject *pkey
		PyObject *pval
		Py_ssize_t pos

	result = PyDict_New()
	rv = factory()
	for d in dicts:
		f = get_map_iter(d, &obj)
		d = <object>obj
		Py_DECREF(d)
		pos = 0
		while f(d, &pos, &pkey, &pval):
			obj = PyDict_GetItem(result, <object>pkey)
			if obj is NULL:
				seq = PyList_New(0)
				PyList_Append(seq, <object>pval)
				PyDict_SetItem(result, <object>pkey, seq)
			else:
				PyList_Append(<object>obj, <object>pval)

	f = get_map_iter(result, &obj)
	d = <object>obj
	Py_DECREF(d)
	pos = 0
	while f(d, &pos, &pkey, &pval):
		PyObject_SetItem(rv, <object>pkey, func(<object>pval))
	return rv

def merge_with(func, *dicts, factory=dict):
	"""\
merge_with(func: collections.abc.Callable[[list[V]], V], *dicts: collections.abc.Mapping[K, V], factory: collections.abc.Callable[[], collections.abc.MutableMapping[K, V]] = dict) -> collections.abc.MutableMapping[K, V]

Merge dictionaries and apply a `Callable` to combined values.

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
	return c_merge_with(func, dicts, factory)

cpdef object valmap(object func, object d, object factory=dict):
	"""valmap(func: collections.abc.Callable[[V], W], d: collections.abc.Mapping[K, V], factory: collections.abc.Callable[[], collections.abc.MutableMapping[K, W]] = dict) -> collections.abc.MutableMapping[K, W]

	Apply `func` to all values of `d` and return a new `Mapping` with the transformed values.

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
	cdef:
		object rv
		f_map_next f
		PyObject *obj
		PyObject *pkey
		PyObject *pval
		Py_ssize_t pos = 0

	rv = factory()
	f = get_map_iter(d, &obj)
	d = <object>obj
	Py_DECREF(d)
	while f(d, &pos, &pkey, &pval):
		rv[<object>pkey] = func(<object>pval)
	return rv

cpdef object keymap(object func, object d, object factory=dict):
	"""keymap(func: collections.abc.Callable[[K], L], d: collections.abc.Mapping[K, V], factory: collections.abc.Callable[[], collections.abc.MutableMapping[L, V]] = dict) -> collections.abc.MutableMapping[L, V]

	Apply `func` to all keys of `d` and return a new `Mapping` with the transformed keys.

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
	cdef:
		object rv
		f_map_next f
		PyObject *obj
		PyObject *pkey
		PyObject *pval
		Py_ssize_t pos = 0

	rv = factory()
	f = get_map_iter(d, &obj)
	d = <object>obj
	Py_DECREF(d)
	while f(d, &pos, &pkey, &pval):
		rv[func(<object>pkey)] = <object>pval
	return rv

cpdef object itemmap(object func, object d, object factory=dict):
	"""itemmap(func: collections.abc.Callable[[tuple[K, V]], tuple[L, W]], d: collections.abc.Mapping[K, V], factory: collections.abc.Callable[[], collections.abc.MutableMapping[L, W]] = dict) -> collections.abc.MutableMapping[L, W]

	Apply `func` to all items of `d` and return a new `Mapping` with the transformed items.

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
	cdef:
		object rv, k, v
		f_map_next f
		PyObject *obj
		PyObject *pkey
		PyObject *pval
		Py_ssize_t pos = 0

	rv = factory()
	f = get_map_iter(d, &obj)
	d = <object>obj
	Py_DECREF(d)
	while f(d, &pos, &pkey, &pval):
		k, v = func((<object>pkey, <object>pval))
		rv[k] = v
	return rv

cpdef object valfilter(object predicate, object d, object factory=dict):
	"""valfilter(predicate: collections.abc.Callable[[V], bool], d: collections.abc.Mapping[K, V], factory: collections.abc.Callable[[], collections.abc.MutableMapping[K, V]] = dict) -> collections.abc.MutableMapping[K, V]

	Retain only items from `d` whose values satisfy `predicate` and return a new `Mapping`.

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

	>>> iseven = lambda x: x % 2 == 0
	>>> d = {1: 2, 2: 3, 3: 4, 4: 5}
	>>> valfilter(iseven, d)
	{1: 2, 3: 4}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	cdef:
		object rv
		f_map_next f
		PyObject *obj
		PyObject *pkey
		PyObject *pval
		Py_ssize_t pos = 0

	rv = factory()
	f = get_map_iter(d, &obj)
	d = <object>obj
	Py_DECREF(d)
	while f(d, &pos, &pkey, &pval):
		if predicate(<object>pval):
			rv[<object>pkey] = <object>pval
	return rv

cpdef object keyfilter(object predicate, object d, object factory=dict):
	"""keyfilter(predicate: collections.abc.Callable[[K], bool], d: collections.abc.Mapping[K, V], factory: collections.abc.Callable[[], collections.abc.MutableMapping[K, V]] = dict) -> collections.abc.MutableMapping[K, V]

	Retain only items from `d` whose keys satisfy `predicate` and return a new `Mapping`.

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

	>>> iseven = lambda x: x % 2 == 0
	>>> d = {1: 2, 2: 3, 3: 4, 4: 5}
	>>> keyfilter(iseven, d)
	{2: 3, 4: 5}

	References
	----------
	[1] Python `collections.abc` module
		https://docs.python.org/3/library/collections.abc.html
	"""
	cdef:
		object rv
		f_map_next f
		PyObject *obj
		PyObject *pkey
		PyObject *pval
		Py_ssize_t pos = 0

	rv = factory()
	f = get_map_iter(d, &obj)
	d = <object>obj
	Py_DECREF(d)
	while f(d, &pos, &pkey, &pval):
		if predicate(<object>pkey):
			rv[<object>pkey] = <object>pval
	return rv

cpdef object itemfilter(object predicate, object d, object factory=dict):
	"""itemfilter(predicate: collections.abc.Callable[[tuple[K, V]], bool], d: collections.abc.Mapping[K, V], factory: collections.abc.Callable[[], collections.abc.MutableMapping[K, V]] = dict) -> collections.abc.MutableMapping[K, V]

	Retain only items from `d` whose key-value pairs satisfy `predicate` and return a new `Mapping`.

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
	cdef:
		object rv, k, v
		f_map_next f
		PyObject *obj
		PyObject *pkey
		PyObject *pval
		Py_ssize_t pos = 0

	rv = factory()
	f = get_map_iter(d, &obj)
	d = <object>obj
	Py_DECREF(d)
	while f(d, &pos, &pkey, &pval):
		k = <object>pkey
		v = <object>pval
		if predicate((k, v)):
			rv[k] = v
	return rv

cpdef object assoc(object d, object key, object value, object factory=dict):
	"""assoc(d: collections.abc.Mapping[K, V], key: K, value: V, factory: collections.abc.Callable[[], collections.abc.MutableMapping[K, V]] = dict) -> collections.abc.MutableMapping[K, V]

	Create a new `Mapping`[1] with `key` associated with `value`.

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
	cdef object rv
	rv = factory()
	if PyDict_CheckExact(rv):
		PyDict_Update(rv, d)
	else:
		rv.update(d)
	rv[key] = value
	return rv

cpdef object assoc_in(object d, object keys, object value, object factory=dict):
	"""assoc_in(d: collections.abc.Mapping[K, V], keys: collections.abc.Sequence[K], value: V, factory: collections.abc.Callable[[], collections.abc.MutableMapping[K, V]] = dict) -> collections.abc.MutableMapping[K, V]

	Create a new `MutableMapping` from `d` with `value` at the path specified by `keys`.

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
	cdef object prevkey, key
	cdef object rv, inner, dtemp
	prevkey, keys = keys[0], keys[1:]
	rv = factory()
	if PyDict_CheckExact(rv):
		PyDict_Update(rv, d)
	else:
		rv.update(d)
	inner = rv

	for key in keys:
		if prevkey in d:
			d = d[prevkey]
			dtemp = factory()
			if PyDict_CheckExact(dtemp):
				PyDict_Update(dtemp, d)
			else:
				dtemp.update(d)
		else:
			d = factory()
			dtemp = d
		inner[prevkey] = dtemp
		prevkey = key
		inner = dtemp

	inner[prevkey] = value
	return rv

cdef object c_dissoc(object d, object keys, object factory=dict):
	# implementation copied from humpy_toolz.  Not benchmarked.
	cdef object rv
	rv = factory()
	if len(keys) < len(d) * 0.6:
		rv.update(d)
		for key in keys:
			if key in rv:
				del rv[key]
	else:
		remaining = set(d)
		remaining.difference_update(keys)
		for k in remaining:
			rv[k] = d[k]
	return rv

def dissoc(d, *keys, **kwargs):
	"""dissoc(d: collections.abc.Mapping[K, V], *keys: K, factory: collections.abc.Callable[[], collections.abc.MutableMapping[K, V]] = dict) -> collections.abc.MutableMapping[K, V]

	Create a new `MutableMapping`[1] from `d` with the specified `keys` removed.

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
	return c_dissoc(d, keys, get_factory('dissoc', kwargs))

cpdef object update_in(object d, object keys, object func, object default=None, object factory=dict):
	"""update_in(d: collections.abc.Mapping[K, V], keys: collections.abc.Sequence[K], func: collections.abc.Callable[[V], V], default: V | None = None, factory: collections.abc.Callable[[], collections.abc.MutableMapping[K, V]] = dict) -> collections.abc.MutableMapping[K, V]

	Apply a `Callable` to a value at a nested path in a `Mapping`.

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
	cdef object prevkey, key
	cdef object rv, inner, dtemp
	prevkey, keys = keys[0], keys[1:]
	rv = factory()
	if PyDict_CheckExact(rv):
		PyDict_Update(rv, d)
	else:
		rv.update(d)
	inner = rv

	for key in keys:
		if prevkey in d:
			d = d[prevkey]
			dtemp = factory()
			if PyDict_CheckExact(dtemp):
				PyDict_Update(dtemp, d)
			else:
				dtemp.update(d)
		else:
			d = factory()
			dtemp = d
		inner[prevkey] = dtemp
		prevkey = key
		inner = dtemp

	if prevkey in d:
		key = func(d[prevkey])
	else:
		key = func(default)
	inner[prevkey] = key
	return rv

cdef tuple _get_in_exceptions = (KeyError, IndexError, TypeError)

cpdef object get_in(object keys, object coll, object default=None, object no_default=False):
	"""get_in(keys: collections.abc.Sequence[K], coll: humpy_toolz.dicttoolz.SupportsGetItem[K, V], default: Optional[V] = None, no_default: bool = False) -> Optional[V]

	Retrieve a value from a potentially nested `coll` (***coll***ection) using a `Sequence` of `keys`.

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
	cdef object item
	try:
		for item in keys:
			coll = coll[item]
		return coll
	except _get_in_exceptions:
		if no_default:
			raise
		return default
