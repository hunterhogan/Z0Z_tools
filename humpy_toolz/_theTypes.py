from __future__ import annotations

from collections.abc import Callable, Hashable, Iterable, Sequence
from typing import Any, Protocol, TypeVar
from typing_extensions import ParamSpec

_KT_contra = TypeVar('_KT_contra', contravariant=True)
_T_contra = TypeVar('_T_contra', contravariant=True)
_VT_co = TypeVar('_VT_co', covariant=True)

class Randomable(Protocol):
	"""Protocol for objects exposing a ``random() -> float`` method."""

	def random(self) -> float: ...

class SupportsBool(Protocol):
	"""Objects supporting truth-value testing via ``__bool__``."""

	def __bool__(self) -> bool: ...

class SupportsDunderGT(Protocol[_T_contra]):
	"""Objects supporting the ``__gt__`` operator."""

	def __gt__(self, other: _T_contra, /) -> SupportsBool: ...

class SupportsDunderLT(Protocol[_T_contra]):
	"""Objects supporting the ``__lt__`` operator."""

	def __lt__(self, other: _T_contra, /) -> SupportsBool: ...

class SupportsGetItem(Protocol[_KT_contra, _VT_co]):
	"""Objects supporting item access via ``__getitem__``."""

	def __getitem__(self, key: _KT_contra, /) -> _VT_co: ...

type SupportsRichComparison = SupportsDunderLT[Any] | SupportsDunderGT[Any]

Instance = TypeVar('Instance')
K = TypeVar('K', bound=Hashable)
K0 = TypeVar('K0', bound=Hashable)
K1 = TypeVar('K1', bound=Hashable)
K2 = TypeVar('K2', bound=Hashable)
K3 = TypeVar('K3', bound=Hashable)
L = TypeVar('L')
P = ParamSpec('P')
R = TypeVar('R')
S = TypeVar('S')
SSequence = TypeVar('SSequence', bound=Sequence[Any])
T = TypeVar('T')
T0 = TypeVar('T0')
T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')
T5 = TypeVar('T5')
T6 = TypeVar('T6')
TIterable = TypeVar('TIterable', bound=Iterable[Any])
TSupportsRichComparison = TypeVar('TSupportsRichComparison', bound=SupportsRichComparison)
U = TypeVar('U')
V = TypeVar('V')
V_co = TypeVar('V_co', covariant=True)
V0 = TypeVar('V0')
V1 = TypeVar('V1')
V2 = TypeVar('V2')
V3 = TypeVar('V3')
_T = TypeVar('_T')
_Instance = TypeVar('_Instance')
type _Getter[_Instance, _T] = Callable[[_Instance], _T]
type _Setter[_Instance, _T] = Callable[[_Instance, _T], None]
type _Deleter[_Instance] = Callable[[_Instance], None]
type InstancePropertyState[_Instance, _T] = tuple[
	_Getter[_Instance, _T] | None, _Setter[_Instance, _T] | None, _Deleter[_Instance] | None, str | None, _T | None
]
type CurryState = tuple[Any, ...]
TypeElement = TypeVar('TypeElement')
TypeResult = TypeVar('TypeResult')

type MapFunction[TypeElement, TypeResult] = Callable[[Callable[[Iterable[TypeElement]], TypeResult], Iterable[Iterable[TypeElement]]], Iterable[TypeResult]]
