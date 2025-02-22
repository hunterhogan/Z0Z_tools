from typing import Any, Literal
from tests.conftest import *
from decimal import Decimal
from fractions import Fraction
from collections.abc import Iterable
from numpy.typing import NDArray
import datetime
import numpy
import pytest

class CustomIterable:
	def __init__(self, items: Iterable[Any]) -> None: self.items = items
	def __iter__(self) -> Iterable[Any]: return iter(self.items)

@pytest.mark.parametrize("description,value_scrapPile,expected", [
	# Basic types and structures
	("Empty input", [], []),
	("Prime numbers", [11, 13, 17], ['11', '13', '17']),
	("Cardinal directions", ["NE", "SW", "SE"], ["NE", "SW", "SE"]),
	("Country codes", ["FR", "JP", "BR"], ["FR", "JP", "BR"]),
	("Boolean values", [True, False], ['True', 'False']),
	("None value", [None], ['None']),
	# Numbers and numeric types
	("Fibonacci floats", [2.584, -4.236, 6.854], ['2.584', '-4.236', '6.854']),
	("Complex with primes", [complex(11,0), complex(13,0)], ['(11+0j)', '(13+0j)']),
	("Decimal and Fraction", [Decimal('3.141'), Fraction(89, 55)], ['3.141', '89/55']),
	("NumPy primes", numpy.array([11, 13, 17]), ['11', '13', '17']),  # type: ignore
	# Temporal types with meaningful dates
	("Historical date", [datetime.date(1789, 7, 14)], ['1789-07-14']),  # Bastille Day
	("Time zones", [datetime.time(23, 11, 37)], ['23:11:37']),  # Non-standard time
	("Moon landing", [datetime.datetime(1969, 7, 20, 20, 17, 40)], ['1969-07-20 20:17:40']),
	# Binary data - accepting either representation
	("Prime bytes", [b'\x0B', b'\x0D', b'\x11'], [repr(b'\x0b'), repr(b'\x0d'), repr(b'\x11')]),  # Let Python choose representation
	("Custom bytearray", [bytearray(b"DEADBEEF")], ["bytearray(b'DEADBEEF')"]),
	# Nested structures with unique values
	("Nested dictionary", {'phi': 1.618, 'euler': 2.718}, ['phi', '1.618', 'euler', '2.718']),
	("Mixed nesting", [{'NE': 37}, {'SW': 41}], ['NE', '37', 'SW', '41']),
	("Tuples and lists", [(13, 17), [19, 23]], ['13', '17', '19', '23']),
	("Sets and frozensets", [{37, 41}, frozenset([43, 47])], ['41', '37', '43', '47']),
	# Special cases and error handling
	("NaN and Infinities", [float('nan'), float('inf'), -float('inf')], ['nan', 'inf', '-inf']),
	("Large prime", [10**19 + 33], ['10000000000000000033']),
	("Simple recursive", [[[...]]], ['Ellipsis']),  # Recursive list
	("Complex recursive", {'self': {'self': None}}, ['self', 'self', 'None']),
	# Generators and custom iterables
	("Generator from primes", (x for x in [11, 13, 17]), ['11', '13', '17']),
	("Iterator from Fibonacci", iter([3, 5, 8, 13]), ['3', '5', '8', '13']),
	("Custom iterable cardinal", CustomIterable(["NW", "SE", "NE"]), ["NW", "SE", "NE"]),
	("Custom iterable empty", CustomIterable([]), []),
	# Weird stuff
	# ("Basic object", object(), []), # does not and should not create an error. Difficult to test with `standardizedEqualTo` because the memory address will change.
	("Bad __str__", type('BadStr', (), {'__str__': lambda x: None})(), [None]),
	# Error cases
	("Raising __str__", type('RaisingStr', (), {'__str__': lambda x: 1/0})(), ZeroDivisionError),
], ids=lambda x: x if isinstance(x, str) else "")
def testStringItUp(description: str, value_scrapPile: list[Any], expected: list[str] | type[Exception]) -> None:
	"""Test stringItUp with various inputs."""
	standardizedEqualTo(expected, stringItUp, value_scrapPile)

@pytest.mark.parametrize("description,value_scrapPile,expected", [
	("Memory view", memoryview(b"DEADBEEF"), ["<memory at 0x"]),  # Special handling for memoryview
], ids=lambda x: x if isinstance(x, str) else "")
def testStringItUpErrorCases(description: Literal['Memory view'], value_scrapPile: memoryview, expected: str) -> None:
	result = stringItUp(value_scrapPile)
	assert len(result) == 1
	assert result[0].startswith(expected[0])

@pytest.mark.parametrize("description,value_dictionaryLists,keywordArguments,expected", [
	("Mixed value types", ({'ne': [11, 'prime'], 'sw': [True, None]}, {'ne': [3.141, 'golden'], 'sw': [False, 'void']}), {'destroyDuplicates': False, 'reorderLists': False}, {'ne': [11, 'prime', 3.141, 'golden'], 'sw': [True, None, False, 'void']} ),
	("Empty dictionaries", (dict[str, list[Any]](), dict[str, list[Any]]()), dict[str, Any](), dict[str, list[Any]]() ),
	("Tuple values", ({'ne': (11, 13), 'sw': (17,)}, {'ne': (19, 23, 13, 29, 11), 'sw': (31, 17, 37)}), {'destroyDuplicates': False, 'reorderLists': False}, {'ne': [11, 13, 19, 23, 13, 29, 11], 'sw': [17, 31, 17, 37]} ),
	("Set values", ({'ne': {11, 13}, 'sw': {17}}, {'ne': {19, 23, 13, 29, 11}, 'sw': {31, 17, 37}}), {'destroyDuplicates': True, 'reorderLists': True}, {'ne': [11, 13, 19, 23, 29], 'sw': [17, 31, 37]} ),
	("NumPy arrays", ({'ne': numpy.array([11, 13]), 'sw': numpy.array([17])}, {'ne': numpy.array([19, 23, 13, 29, 11]), 'sw': numpy.array([31, 17, 37])}), {'destroyDuplicates': False, 'reorderLists': False}, {'ne': [11, 13, 19, 23, 13, 29, 11], 'sw': [17, 31, 17, 37]} ),
	("Destroy duplicates", ({'fr': [11, 13], 'jp': [17]}, {'fr': [19, 23, 13, 29, 11], 'jp': [31, 17, 37]}), {'destroyDuplicates': True, 'reorderLists': False}, {'fr': [11, 13, 19, 23, 29], 'jp': [17, 31, 37]} ),
	("Non-string keys", ({None: [13], True: [17]}, {19: [23], (29, 31): [37]}), {'destroyDuplicates': False, 'reorderLists': False}, {'None': [13], 'True': [17], '19': [23], '(29, 31)': [37]} ),  # type: ignore
	("Reorder lists", ({'fr': [11, 13], 'jp': [17]}, {'fr': [19, 23, 13, 29, 11], 'jp': [31, 17, 37]}), {'destroyDuplicates': False, 'reorderLists': True}, {'fr': [11, 11, 13, 13, 19, 23, 29], 'jp': [17, 17, 31, 37]} ),
	("Non-iterable values", ({'ne': 13, 'sw': 17}, {'ne': 19, 'nw': 23}), {'destroyDuplicates': False, 'reorderLists': False}, TypeError ),
	("Skip erroneous types", ({'ne': [11, 13], 'sw': [17, 19]}, {'ne': 23, 'nw': 29}), {'killErroneousDataTypes': True}, {'ne': [11, 13], 'sw': [17, 19]} ),
], ids=lambda x: x if isinstance(x, str) else "")
def testUpdateExtendPolishDictionaryLists(description: str, value_dictionaryLists: tuple[dict[Any, Any],...], keywordArguments: dict[Any,Any], expected: dict[str, Any] | type[TypeError] ) -> None:
	standardizedEqualTo(expected, updateExtendPolishDictionaryLists, *value_dictionaryLists, **keywordArguments)
	# NOTE one line of code with `standardizedEqualTo` replaced the following ten lines of code.
	# if isinstance(expected, type) and issubclass(expected, Exception):
	#	 with pytest.raises(expected):
	#		 updateExtendPolishDictionaryLists(*value_dictionaryLists, **keywordArguments)
	# else:
	#	 result = updateExtendPolishDictionaryLists(*value_dictionaryLists, **keywordArguments)
	#	 if description == "Set values":  # Special handling for unordered sets
	#		 for key in result:
	#			 assert sorted(result[key]) == sorted(expected[key]) # type: ignore
	#	 else:
	#		 assert result == expected

@pytest.mark.parametrize("description,value_arrayTarget,expected", [
	("One range", numpy.array(list(range(50,60))), "[*range(50,60)]"),
	("Value, range", numpy.array([123]+list(range(71,81))), "[123,*range(71,81)]"),
	("range, value", numpy.array(list(range(91,97))+[101]), "[*range(91,97),101]"),
	("Value, range, value", numpy.array([151]+list(range(163,171))+[181]), "[151,*range(163,171),181]"),
	("Repeat values", numpy.array([191, 191, 191]), "[191]*3"),
	("Value with repeat", numpy.array([211, 223, 223, 223]), "[211]+[223]*3"),
	("Range with repeat", numpy.array(list(range(251,257))+[271, 271, 271]), "[*range(251,257)]+[271]*3"),
	("Value, range, repeat", numpy.array([281]+list(range(291,297))+[307, 307]), "[281,*range(291,297)]+[307]*2"),
	("repeat, value", numpy.array([313, 313, 313, 331, 331, 349]), "[313]*3+[331]*2+[349]"),
	("repeat, range", numpy.array([373, 373, 373]+list(range(383,389))), "[373]*3+[*range(383,389)]"),
	("repeat, range, value", numpy.array(7*[401]+list(range(409,415))+[421]), "[401]*7+[*range(409,415),421]"),
	("Repeated primes", numpy.array([431, 431, 431, 443, 443, 457]), "[431]*3+[443]*2+[457]"),
	("Two Ranges", numpy.array(list(range(461,471))+list(range(479,487))), "[*range(461,471),*range(479,487)]"),
	("2D array primes", numpy.array([[491, 499, 503], [509, 521, 523]]), "[[491,499,503],[509,521,523]]"),
	("3D array primes", numpy.array([[[541, 547], [557, 563]], [[569, 571], [577, 587]]]), "[[[541,547],[557,563]],[[569,571],[577,587]]]"),
], ids=lambda x: x if isinstance(x, str) else "")
def testAutoDecodingRLE(description: str, value_arrayTarget: NDArray[numpy.integer[Any]], expected: str) -> None:
	"""Test autoDecodingRLE with various input arrays."""
	standardizedEqualTo(expected, autoDecodingRLE, value_arrayTarget)
