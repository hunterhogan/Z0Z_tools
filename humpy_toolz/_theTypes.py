from __future__ import annotations

from collections.abc import Hashable, Iterable, Sequence
from typing import Any, Protocol, TypeAlias, TypeVar

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

SupportsRichComparison: TypeAlias = SupportsDunderLT[Any] | SupportsDunderGT[Any]

K = TypeVar('K')
KHashable = TypeVar('KHashable', bound=Hashable)
K0Hashable = TypeVar('K0Hashable', bound=Hashable)
K1 = TypeVar('K1')
K1Hashable = TypeVar('K1Hashable', bound=Hashable)
K2 = TypeVar('K2')
K3 = TypeVar('K3')
L = TypeVar('L')
P = TypeVar('P')
R = TypeVar('R')
S = TypeVar('S')
SSequence = TypeVar('SSequence', bound=Sequence[Any])
T = TypeVar('T')
TIterable = TypeVar('TIterable', bound=Iterable[Any])
TSupportsRichComparison = TypeVar('TSupportsRichComparison', bound=SupportsRichComparison)
U = TypeVar('U')
V = TypeVar('V')
V0 = TypeVar('V0')
V1 = TypeVar('V1')
V2 = TypeVar('V2')
V3 = TypeVar('V3')
