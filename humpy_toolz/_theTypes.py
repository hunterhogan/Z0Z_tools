from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any, Protocol, TypeVar

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

type MapFunction[TypeElement, TypeResult] = Callable[[Callable[[Iterable[TypeElement]], TypeResult], Iterable[Iterable[TypeElement]]], Iterable[TypeResult]]
