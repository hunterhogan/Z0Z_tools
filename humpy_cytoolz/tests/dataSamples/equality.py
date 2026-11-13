"""Objects whose equality comparison differs from identity."""
from __future__ import annotations

class EqualsEveryString:
	"""Object equal to itself and to every `str`, and to nothing else: an object whose `==` does not mean identity, as a NumPy array's does not."""

	def __eq__(self, other: object) -> bool:
		return other is self or isinstance(other, str)

	def __hash__(self) -> int:
		return id(self)

	def __repr__(self) -> str:
		return f'{type(self).__name__}()'

equalsEveryString: EqualsEveryString = EqualsEveryString()
