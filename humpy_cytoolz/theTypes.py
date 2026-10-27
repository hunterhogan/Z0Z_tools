from __future__ import annotations

from optype import CanBool as SupportsBool, CanGetitem, CanGetitem as SupportsGetItem, CanGt as SupportsDunderGT, CanGtSame, CanLt as SupportsDunderLT, CanLtSame, CanSetitem
from typing import Protocol

class CanGetSetitem[Key, Value](CanGetitem[Key, Value], CanSetitem[Key, Value], Protocol): ...

class Randomable(Protocol):
	"""Protocol for objects exposing a ``random() -> float`` method."""

	def random(self) -> float: ...

type SupportsRichComparison = CanLtSame | CanGtSame
