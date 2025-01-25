from tests.conftest import *
from decimal import Decimal
from fractions import Fraction
import datetime
import numpy
import pytest

class CustomIterable:
    def __init__(self, items): self.items = items
    def __iter__(self): return iter(self.items)

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
def testStringItUp(description, value_scrapPile, expected):
    """Test stringItUp with various inputs."""
    standardizedEqualTo(expected, stringItUp, value_scrapPile)

@pytest.mark.parametrize("description,value_scrapPile,expected", [
    ("Memory view", memoryview(b"DEADBEEF"), ["<memory at 0x"]),  # Special handling for memoryview
], ids=lambda x: x if isinstance(x, str) else "")
def testStringItUpErrorCases(description, value_scrapPile, expected):
    result = stringItUp(value_scrapPile)
    assert len(result) == 1
    assert result[0].startswith(expected[0])

@pytest.mark.parametrize("description,value_dictionaryLists,keywordArguments,expected", [
    ("Empty dictionaries", ({}, {}), {}, {} ),
    ("Mixed value types", ({'ne': [11, 'prime'], 'sw': [True, None]}, {'ne': [3.141, 'golden'], 'sw': [False, 'void']}), {'destroyDuplicates': False, 'reorderLists': False}, {'ne': [11, 'prime', 3.141, 'golden'], 'sw': [True, None, False, 'void']} ),
    ("Non-string keys", ({None: [13], True: [17]}, {19: [23], (29, 31): [37]}), {'destroyDuplicates': False, 'reorderLists': False}, {'None': [13], 'True': [17], '19': [23], '(29, 31)': [37]} ), # Various sequence types
    ("Set values", ({'ne': {11, 13}, 'sw': {17}}, {'ne': {19, 23, 13, 29, 11}, 'sw': {31, 17, 37}}), {'destroyDuplicates': True, 'reorderLists': True}, {'ne': [11, 13, 19, 23, 29], 'sw': [17, 31, 37]} ),
    ("Tuple values", ({'ne': (11, 13), 'sw': (17,)}, {'ne': (19, 23, 13, 29, 11), 'sw': (31, 17, 37)}), {'destroyDuplicates': False, 'reorderLists': False}, {'ne': [11, 13, 19, 23, 13, 29, 11], 'sw': [17, 31, 17, 37]} ),
    ("NumPy arrays", ({'ne': numpy.array([11, 13]), 'sw': numpy.array([17])}, {'ne': numpy.array([19, 23, 13, 29, 11]), 'sw': numpy.array([31, 17, 37])}), {'destroyDuplicates': False, 'reorderLists': False}, {'ne': [11, 13, 19, 23, 13, 29, 11], 'sw': [17, 31, 17, 37]} ),
    ("Destroy duplicates", ({'fr': [11, 13], 'jp': [17]}, {'fr': [19, 23, 13, 29, 11], 'jp': [31, 17, 37]}), {'destroyDuplicates': True, 'reorderLists': False}, {'fr': [11, 13, 19, 23, 29], 'jp': [17, 31, 37]} ),
    ("Reorder lists", ({'fr': [11, 13], 'jp': [17]}, {'fr': [19, 23, 13, 29, 11], 'jp': [31, 17, 37]}), {'destroyDuplicates': False, 'reorderLists': True}, {'fr': [11, 11, 13, 13, 19, 23, 29], 'jp': [17, 17, 31, 37]} ),
    ("Non-iterable values", ({'ne': 13, 'sw': 17}, {'ne': 19, 'nw': 23}), {'destroyDuplicates': False, 'reorderLists': False}, TypeError ),
    ("Skip erroneous types", ({'ne': [11, 13], 'sw': [17, 19]}, {'ne': 23, 'nw': 29}), {'killErroneousDataTypes': True}, {'ne': [11, 13], 'sw': [17, 19]} ),
], ids=lambda x: x if isinstance(x, str) else "")
def testUpdateExtendPolishDictionaryLists(description, value_dictionaryLists, keywordArguments, expected):
    standardizedEqualTo(expected, updateExtendPolishDictionaryLists, *value_dictionaryLists, **keywordArguments)
    # NOTE one line of code with `standardizedEqualTo` replaced the following ten lines of code.
    # if isinstance(expected, type) and issubclass(expected, Exception):
    #     with pytest.raises(expected):
    #         updateExtendPolishDictionaryLists(*value_dictionaryLists, **keywordArguments)
    # else:
    #     result = updateExtendPolishDictionaryLists(*value_dictionaryLists, **keywordArguments)
    #     if description == "Set values":  # Special handling for unordered sets
    #         for key in result:
    #             assert sorted(result[key]) == sorted(expected[key]) # type: ignore
    #     else:
    #         assert result == expected
