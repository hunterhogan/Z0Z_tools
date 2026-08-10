
from collections.abc import Callable, Hashable, Mapping, MutableMapping, Sequence
from humpy_toolz.theTypes import CanGetSetitem
from optype import CanBool, CanGetitem
from optype.typing import AnyIterable, EmptyIterable
from typing import Any, overload, TypeGuard
from typing_extensions import TypeIs

__all__ = ('assoc', 'assoc_in', 'dissoc', 'get_in', 'itemfilter', 'itemmap', 'keyfilter', 'keymap', 'merge', 'merge_with', 'update_in', 'valfilter', 'valmap')

@overload
def assoc[K: Hashable, V](d: Mapping[K, V], key: K, value: V, factory: Callable[..., dict[K, V]] = dict) -> dict[K, V]:
    ...

@overload
def assoc[K: Hashable, V](d: Mapping[K, V], key: K, value: V, factory: Callable[..., MutableMapping[K, V]]) -> MutableMapping[K, V]:
    ...

def assoc[K: Hashable, V](d: Mapping[K, V], key: K, value: V, factory: Callable[..., MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
    ...

@overload
def assoc_in[K1: Hashable, K2: Hashable, V2, V1](d: Mapping[K1, Mapping[K2, V2] | V1], keys: tuple[K1, K2], value: V2) -> dict[K1, dict[K2, V2] | V1 | V2]:
    ...

@overload
def assoc_in[K1: Hashable, K2: Hashable, V2, V1](d: Mapping[K1, Mapping[K2, V2] | V1], keys: tuple[K1, K2], value: V2, *, factory: Callable[..., MutableMapping[K1, Any]]) -> MutableMapping[K1, Any]:
    ...

@overload
def assoc_in[K1: Hashable, K2: Hashable, K3: Hashable, V3, V2, V1](d: Mapping[K1, Mapping[K2, Mapping[K3, V3] | V2] | V1], keys: tuple[K1, K2, K3], value: V3) -> dict[K1, dict[K2, dict[K3, V3] | V2 | V3] | V1 | V3]:
    ...

@overload
def assoc_in[K1: Hashable, K2: Hashable, K3: Hashable, V3, V2, V1](d: Mapping[K1, Mapping[K2, Mapping[K3, V3] | V2] | V1], keys: tuple[K1, K2, K3], value: V3, *, factory: Callable[..., MutableMapping[K1, Any]]) -> MutableMapping[K1, Any]:
    ...

@overload
def assoc_in[K: Hashable, V](d: Mapping[K, V], keys: Sequence[K], value: V) -> dict[K, V]:
    ...

@overload
def assoc_in[K: Hashable, V](d: Mapping[K, V], keys: Sequence[K], value: V, *, factory: Callable[..., MutableMapping[K, V]]) -> MutableMapping[K, V]:
    ...

def assoc_in[K1: Hashable, K2: Hashable, K3: Hashable, V3, V2, V1](d: Mapping[K1, V1] | Mapping[K1, Mapping[K2, V2] | V1] | Mapping[K1, Mapping[K2, Mapping[K3, V3] | V2] | V1], keys: Sequence[K1] | tuple[K1, K2] | tuple[K1, K2, K3], value: V1 | V2 | V3, *, factory: Callable[..., MutableMapping[K1, V1]] = dict) -> MutableMapping[K1, V1] | dict[K1, dict[K2, V2] | V1 | V2] | dict[K1, dict[K2, dict[K3, V3] | V2 | V3] | V1 | V3]:
    ...

@overload
def dissoc[K: Hashable, V](d: Mapping[K, V], *keys: K, factory: Callable[..., dict[K, V]] = dict) -> dict[K, V]:
    ...

@overload
def dissoc[K: Hashable, V](d: Mapping[K, V], *keys: K, factory: Callable[..., MutableMapping[K, V]]) -> MutableMapping[K, V]:
    ...

def dissoc[K: Hashable, V](d: Mapping[K, V], *keys: K, factory: Callable[..., MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
    ...

@overload
def get_in[Collection, Value_default](keys: EmptyIterable, coll: Collection, default: Value_default | None = None, no_default: CanBool = False) -> Collection:
    ...

@overload
def get_in[Key0, Value, Value_default](keys: tuple[Key0], coll: CanGetSetitem[Key0, Value], default: Value_default, no_default: CanBool = False) -> Value | Value_default:
    ...

@overload
def get_in[Key0, Value](keys: tuple[Key0], coll: CanGetSetitem[Key0, Value], default: None = None, no_default: CanBool = False) -> Value | None:
    ...

@overload
def get_in[Key0, Value, Value_default](keys: tuple[Key0], coll: CanGetitem[Key0, Value], default: Value_default, no_default: CanBool = False) -> Value | Value_default:
    ...

@overload
def get_in[Key0, Value](keys: tuple[Key0], coll: CanGetitem[Key0, Value], default: None = None, no_default: CanBool = False) -> Value | None:
    ...

@overload
def get_in[Key0, Key1, Value, Value_default](keys: tuple[Key0, Key1], coll: CanGetitem[Key0, CanGetSetitem[Key1, Value]], default: Value_default, no_default: CanBool = False) -> Value | Value_default:
    ...

@overload
def get_in[Key0, Key1, Value](keys: tuple[Key0, Key1], coll: CanGetitem[Key0, CanGetSetitem[Key1, Value]], default: None = None, no_default: CanBool = False) -> Value | None:
    ...

@overload
def get_in[Key0, Key1, Value, Value_default](keys: tuple[Key0, Key1], coll: CanGetitem[Key0, CanGetitem[Key1, Value]], default: Value_default, no_default: CanBool = False) -> Value | Value_default:
    ...

@overload
def get_in[Key0, Key1, Value](keys: tuple[Key0, Key1], coll: CanGetitem[Key0, CanGetitem[Key1, Value]], default: None = None, no_default: CanBool = False) -> Value | None:
    ...

@overload
def get_in[Key0, Key1, Key2, Value, Value_default](keys: tuple[Key0, Key1, Key2], coll: CanGetitem[Key0, CanGetitem[Key1, CanGetSetitem[Key2, Value]]], default: Value_default, no_default: CanBool = False) -> Value | Value_default:
    ...

@overload
def get_in[Key0, Key1, Key2, Value](keys: tuple[Key0, Key1, Key2], coll: CanGetitem[Key0, CanGetitem[Key1, CanGetSetitem[Key2, Value]]], default: None = None, no_default: CanBool = False) -> Value | None:
    ...

@overload
def get_in[Key0, Key1, Key2, Value, Value_default](keys: tuple[Key0, Key1, Key2], coll: CanGetitem[Key0, CanGetitem[Key1, CanGetitem[Key2, Value]]], default: Value_default, no_default: CanBool = False) -> Value | Value_default:
    ...

@overload
def get_in[Key0, Key1, Key2, Value](keys: tuple[Key0, Key1, Key2], coll: CanGetitem[Key0, CanGetitem[Key1, CanGetitem[Key2, Value]]], default: None = None, no_default: CanBool = False) -> Value | None:
    ...

@overload
def get_in[Key0, Key1, Key2, Key3, Value, Value_default](keys: tuple[Key0, Key1, Key2, Key3], coll: CanGetitem[Key0, CanGetitem[Key1, CanGetitem[Key2, CanGetSetitem[Key3, Value]]]], default: Value_default, no_default: CanBool = False) -> Value | Value_default:
    ...

@overload
def get_in[Key0, Key1, Key2, Key3, Value](keys: tuple[Key0, Key1, Key2, Key3], coll: CanGetitem[Key0, CanGetitem[Key1, CanGetitem[Key2, CanGetSetitem[Key3, Value]]]], default: None = None, no_default: CanBool = False) -> Value | None:
    ...

@overload
def get_in[Key0, Key1, Key2, Key3, Value, Value_default](keys: tuple[Key0, Key1, Key2, Key3], coll: CanGetitem[Key0, CanGetitem[Key1, CanGetitem[Key2, CanGetitem[Key3, Value]]]], default: Value_default, no_default: CanBool = False) -> Value | Value_default:
    ...

@overload
def get_in[Key0, Key1, Key2, Key3, Value](keys: tuple[Key0, Key1, Key2, Key3], coll: CanGetitem[Key0, CanGetitem[Key1, CanGetitem[Key2, CanGetitem[Key3, Value]]]], default: None = None, no_default: CanBool = False) -> Value | None:
    ...

@overload
def get_in[Key, Collection, Value_default](keys: AnyIterable[Key], coll: Collection, default: Value_default | None = None, no_default: CanBool = False) -> Any:
    ...

def get_in(keys: Any, coll: Any, default: Any = None, no_default: CanBool = False) -> Any:
    ...

@overload
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](predicate: Callable[[tuple[K0, V0]], TypeIs[tuple[K1, V1]]], d: Mapping[K0, V0], factory: Callable[..., dict[K1, V1]] = dict) -> dict[K1, V1]:
    ...

@overload
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](predicate: Callable[[tuple[K0, V0]], TypeGuard[tuple[K1, V1]]], d: Mapping[K0, V0], factory: Callable[..., dict[K1, V1]] = dict) -> dict[K1, V1]:
    ...

@overload
def itemfilter[K0: Hashable, V0](predicate: Callable[[tuple[K0, V0]], bool], d: Mapping[K0, V0], factory: Callable[..., dict[K0, V0]] = dict) -> dict[K0, V0]:
    ...

@overload
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](predicate: Callable[[tuple[K0, V0]], TypeIs[tuple[K1, V1]]], d: Mapping[K0, V0], factory: Callable[..., MutableMapping[K1, V1]]) -> MutableMapping[K1, V1]:
    ...

@overload
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](predicate: Callable[[tuple[K0, V0]], TypeGuard[tuple[K1, V1]]], d: Mapping[K0, V0], factory: Callable[..., MutableMapping[K1, V1]]) -> MutableMapping[K1, V1]:
    ...

@overload
def itemfilter[K0: Hashable, V0, K1: Hashable, V1](predicate: Callable[[tuple[K0, V0]], bool], d: Mapping[K0, V0], factory: Callable[..., MutableMapping[K1, V1]]) -> MutableMapping[K1, V1]:
    ...

def itemfilter[K0: Hashable, V0, K1: Hashable, V1](predicate: Callable[[tuple[K0, V0]], bool] | Callable[[tuple[K0, V0]], TypeGuard[tuple[K1, V1]]] | Callable[[tuple[K0, V0]], TypeIs[tuple[K1, V1]]], d: Mapping[K0, V0], factory: Callable[..., MutableMapping[K1, V1]] | Callable[..., dict[K1, V1]] | Callable[..., dict[K0, V0]] = dict) -> MutableMapping[K1, V1] | dict[K1, V1] | dict[K0, V0]:
    ...

@overload
def itemmap[K0: Hashable, V0, K1: Hashable, V1](func: Callable[[tuple[K0, V0]], tuple[K1, V1]], d: Mapping[K0, V0], factory: Callable[..., dict[K1, V1]] = dict) -> dict[K1, V1]:
    ...

@overload
def itemmap[K0: Hashable, V0, K1: Hashable, V1](func: Callable[[tuple[K0, V0]], tuple[K1, V1]], d: Mapping[K0, V0], factory: Callable[..., MutableMapping[K1, V1]]) -> MutableMapping[K1, V1]:
    ...

def itemmap[K0: Hashable, V0, K1: Hashable, V1](func: Callable[[tuple[K0, V0]], tuple[K1, V1]], d: Mapping[K0, V0], factory: Callable[..., MutableMapping[K1, V1]] = dict) -> MutableMapping[K1, V1]:
    ...

@overload
def keyfilter[K0: Hashable, K1: Hashable, V](predicate: Callable[[K0], TypeIs[K1]], d: Mapping[K0, V], factory: Callable[..., dict[K1, V]] = dict) -> dict[K1, V]:
    ...

@overload
def keyfilter[K0: Hashable, K1: Hashable, V](predicate: Callable[[K0], TypeGuard[K1]], d: Mapping[K0, V], factory: Callable[..., dict[K1, V]] = dict) -> dict[K1, V]:
    ...

@overload
def keyfilter[K0: Hashable, V](predicate: Callable[[K0], bool], d: Mapping[K0, V], factory: Callable[..., dict[K0, V]] = dict) -> dict[K0, V]:
    ...

@overload
def keyfilter[K0: Hashable, K1: Hashable, V](predicate: Callable[[K0], TypeIs[K1]], d: Mapping[K0, V], factory: Callable[..., MutableMapping[K1, V]]) -> MutableMapping[K1, V]:
    ...

@overload
def keyfilter[K0: Hashable, K1: Hashable, V](predicate: Callable[[K0], TypeGuard[K1]], d: Mapping[K0, V], factory: Callable[..., MutableMapping[K1, V]]) -> MutableMapping[K1, V]:
    ...

@overload
def keyfilter[K0: Hashable, V, K1: Hashable](predicate: Callable[[K0], bool], d: Mapping[K0, V], factory: Callable[..., MutableMapping[K1, V]]) -> MutableMapping[K1, V]:
    ...

def keyfilter[K0: Hashable, K1: Hashable, V](predicate: Callable[[K0], bool] | Callable[[K0], TypeGuard[K1]] | Callable[[K0], TypeIs[K1]], d: Mapping[K0, V], factory: Callable[..., MutableMapping[K1, V]] = dict) -> MutableMapping[K1, V]:
    ...

@overload
def keymap[K0: Hashable, K1: Hashable, V](func: Callable[[K0], K1], d: Mapping[K0, V], factory: Callable[..., dict[K1, V]] = dict) -> dict[K1, V]:
    ...

@overload
def keymap[K0: Hashable, K1: Hashable, V](func: Callable[[K0], K1], d: Mapping[K0, V], factory: Callable[..., MutableMapping[K1, V]]) -> MutableMapping[K1, V]:
    ...

def keymap[K0: Hashable, K1: Hashable, V](func: Callable[[K0], K1], d: Mapping[K0, V], factory: Callable[..., MutableMapping[K1, V]] = dict) -> MutableMapping[K1, V]:
    ...

@overload
def merge[K: Hashable, V](*dicts: Mapping[K, V], factory: Callable[..., dict[K, V]] = dict) -> dict[K, V]:
    ...

@overload
def merge[K: Hashable, V](*dicts: Mapping[K, V], factory: Callable[..., MutableMapping[K, V]]) -> MutableMapping[K, V]:
    ...

def merge[K: Hashable, V](*dicts: Mapping[K, V], factory: Callable[..., MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
    ...

@overload
def merge_with[V, K: Hashable](func: Callable[[Sequence[V]], V], *dicts: Mapping[K, V], factory: Callable[..., dict[K, V]] = dict) -> dict[K, V]:
    ...

@overload
def merge_with[V, K: Hashable](func: Callable[[Sequence[V]], V], *dicts: Mapping[K, V], factory: Callable[..., MutableMapping[K, V]]) -> MutableMapping[K, V]:
    ...

def merge_with[V, K: Hashable](func: Callable[[Sequence[V]], V], *dicts: Mapping[K, V], factory: Callable[..., MutableMapping[K, V]] = dict) -> MutableMapping[K, V]:
    ...

def update_in[K: Hashable, V_co](d: Mapping[K, Mapping[K, V_co] | V_co], keys: Sequence[K], func: Callable[[V_co | None], V_co] | Callable[[V_co], V_co], default: V_co | None = None, factory: Callable[..., Mapping[K, Mapping[K, V_co] | V_co]] = dict) -> Mapping[K, Mapping[K, V_co] | V_co]:
    ...

@overload
def valfilter[K: Hashable, V0, V1](predicate: Callable[[V0], TypeIs[V1]], d: Mapping[K, V0], factory: Callable[..., dict[K, V1]] = dict) -> dict[K, V1]:
    ...

@overload
def valfilter[K: Hashable, V0, V1](predicate: Callable[[V0], TypeGuard[V1]], d: Mapping[K, V0], factory: Callable[..., dict[K, V1]] = dict) -> dict[K, V1]:
    ...

@overload
def valfilter[K: Hashable, V0, V1](predicate: Callable[[V0], bool], d: Mapping[K, V0], factory: Callable[..., dict[K, V1]] = dict) -> dict[K, V1]:
    ...

@overload
def valfilter[K: Hashable, V0, V1](predicate: Callable[[V0], TypeIs[V1]], d: Mapping[K, V0], factory: Callable[..., MutableMapping[K, V1]]) -> MutableMapping[K, V1]:
    ...

@overload
def valfilter[K: Hashable, V0, V1](predicate: Callable[[V0], TypeGuard[V1]], d: Mapping[K, V0], factory: Callable[..., MutableMapping[K, V1]]) -> MutableMapping[K, V1]:
    ...

@overload
def valfilter[K: Hashable, V0, V1](predicate: Callable[[V0], bool], d: Mapping[K, V0], factory: Callable[..., MutableMapping[K, V1]]) -> MutableMapping[K, V1]:
    ...

def valfilter[K: Hashable, V0, V1](predicate: Callable[[V0], bool] | Callable[[V0], TypeIs[V1]] | Callable[[V0], TypeGuard[V1]], d: Mapping[K, V0], factory: Callable[..., dict[K, V1]] | Callable[..., MutableMapping[K, V1]] = dict) -> dict[K, V1] | MutableMapping[K, V1]:
    ...

@overload
def valmap[V0, V1, K: Hashable](func: Callable[[V0], V1], d: Mapping[K, V0], factory: Callable[..., dict[K, V1]] = dict) -> dict[K, V1]:
    ...

@overload
def valmap[V0, V1, K: Hashable](func: Callable[[V0], V1], d: Mapping[K, V0], factory: Callable[..., MutableMapping[K, V1]]) -> MutableMapping[K, V1]:
    ...

def valmap[V0, V1, K: Hashable](func: Callable[[V0], V1], d: Mapping[K, V0], factory: Callable[..., MutableMapping[K, V1]] = dict) -> MutableMapping[K, V1]:
    ...
