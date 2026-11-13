"""The first seven primes, held by iterables that take each branch `humpy_cytoolz` has for its input.

`tail`, `nth`, and `last` index a sequence that is not a mapping and iterate everything else; `tail` slices only a
sequence that supports slicing. Every member iterates the same seven primes in the same order, so one expected value
describes every member. Consumers do not mutate these objects.
"""
from __future__ import annotations

from collections import deque, UserList
from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
	from _pytest.mark.structures import ParameterSet
	from collections.abc import Iterator

class IterableNotSequence[个]:
	"""Iterable that supports iteration and nothing else: no `len`, no indexing, no slicing."""

	def __init__(self, items: tuple[个, ...]) -> None:
		self.items: tuple[个, ...] = items

	def __iter__(self) -> Iterator[个]:
		return iter(self.items)

	def __repr__(self) -> str:
		return f'{type(self).__name__}({self.items!r})'

tuplePrimes: tuple[int, ...] = (2, 3, 5, 7, 11, 13, 17)

boxOfIterablesPrimes: tuple[ParameterSet, ...] = (
	pytest.param(tuplePrimes, id='tuplePrimes'),
	pytest.param([2, 3, 5, 7, 11, 13, 17], id='listPrimes'),
	pytest.param(UserList((2, 3, 5, 7, 11, 13, 17)), id='UserListPrimes'),
	pytest.param(deque((2, 3, 5, 7, 11, 13, 17)), id='dequePrimes'),
	pytest.param(dict.fromkeys(tuplePrimes), id='dictionaryKeysPrimes'),
	pytest.param(IterableNotSequence(tuplePrimes), id='IterableNotSequencePrimes'),
)

class IteratorRaises:
	"""Iterator whose every `next` raises `ValueError('sensor 13 disconnected')`, a message that no other code produces."""

	def __iter__(self) -> IteratorRaises:
		return self

	def __next__(self) -> int:
		raise ValueError(messageSensorDisconnected)

	def __repr__(self) -> str:
		return f'{type(self).__name__}()'

messageSensorDisconnected: str = 'sensor 13 disconnected'
