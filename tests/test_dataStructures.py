
from decimal import Decimal
from fractions import Fraction
from itertools import count, islice
import datetime
import numpy
import pytest
import uuid
from Z0Z_tools import updateExtendPolishDictionaryLists, stringItUp

def testStringItUpEmptyInput():
    """Test stringItUp with empty input."""
    assert stringItUp() == []

def testStringItUpWithBytearray():
    """Test stringItUp with bytearray input."""
    assert stringItUp(bytearray(b"bytearray")) == ["bytearray(b'bytearray')"]

def testStringItUpWithGenerator():
    """Test stringItUp with a generator."""
    def generateNumbers():
        for index in range(3):
            yield index
    assert stringItUp(generateNumbers()) == ['0', '1', '2']

def testStringItUpWithInfiniteIterator():
    """Test stringItUp with an infinite iterator, limited by islice."""
    infiniteGenerator = count()
    limitedGenerator = islice(infiniteGenerator, 5)
    assert stringItUp(limitedGenerator) == ['0', '1', '2', '3', '4']

def testStringItUpWithCustomIterable():
    """Test stringItUp with an object that has a custom __iter__ method."""
    class CustomIterable:
        def __iter__(self):
            return iter([1, 2, 3])
    assert stringItUp(CustomIterable()) == ['1', '2', '3']

def testStringItUpWithRecursiveStructure():
    """Test stringItUp with a recursive structure."""
    recursiveList = []
    recursiveList.append(recursiveList)
    assert stringItUp(recursiveList) == ['[[...]]']

def testStringItUpWithRecursiveStructureNested():
    """Test stringItUp with a nested recursive structure."""
    recursiveList = []
    recursiveList.append(recursiveList)
    assert stringItUp([recursiveList, 'hello']) == ["[[[...]], 'hello']"]

def testStringItUpWithNanAndInf():
    """Test stringItUp with NaN and Infinity."""
    assert stringItUp(float('nan'), float('inf')) == ['nan', 'inf']

def testStringItUpWithLargeNumbers():
    """Test stringItUp with large numbers."""
    largeNumber = 10**100
    assert stringItUp(largeNumber) == [str(largeNumber)]

def testStringItUpWithDecimal():
    """Test stringItUp with Decimal objects."""
    assert stringItUp(Decimal('1.1')) == ['1.1']

def testStringItUpWithFraction():
    """Test stringItUp with Fraction objects."""
    assert stringItUp(Fraction(1, 3)) == ['1/3']

def testStringItUpWithDates():
    """Test stringItUp with date objects."""
    dateSample = datetime.date(2021, 1, 1)
    assert stringItUp(dateSample) == ['2021-01-01']

def testStringItUpWithTimes():
    """Test stringItUp with time objects."""
    timeSample = datetime.time(12, 34, 56)
    assert stringItUp(timeSample) == ['12:34:56']

def testStringItUpWithDatetime():
    """Test stringItUp with datetime objects."""
    datetimeSample = datetime.datetime(2021, 1, 1, 12, 34, 56)
    assert stringItUp(datetimeSample) == ['2021-01-01 12:34:56']

def testStringItUpWithUUID():
    """Test stringItUp with UUID objects."""
    uuidSample = uuid.uuid4()
    assert stringItUp(uuidSample) == [str(uuidSample)]

def testStringItUpWithMemoryView():
    """Test stringItUp with memoryview objects."""
    resultStringItUp = stringItUp(memoryview(b"memoryview"))
    expectedPrefix = "<memory at 0x"
    assert resultStringItUp[0].startswith(expectedPrefix)

def testStringItUpWithEmptyIterables():
    """Test stringItUp with empty iterable types."""
    assert stringItUp([], (), set()) == []

def testStringItUpWithMixedNestedIterables():
    """Test stringItUp with mixed nested iterables."""
    dataSample = [1, (2, {3, "four"}), {"five": [6, 7]}]
    assert set(stringItUp(dataSample)) == set(["1", "2", "3", "four", "five", "6", "7"])

def testStringItUpWithLargeData():
    """Test stringItUp with large data."""
    largeList = list(range(1000))
    resultStringItUp = stringItUp(largeList)
    assert len(resultStringItUp) == 1000
    for index in range(1000):
        assert resultStringItUp[index] == str(index)

@pytest.mark.parametrize("primusDictionary, secundusDictionary, expectedDictionary", [
    (
        {'a': [1, 'two'], 'b': [True, None]},
        {'a': [3.14, 'four'], 'b': [False, 'none']},
        {'a': [1, 'two', 3.14, 'four'], 'b': [True, None, False, 'none']}
    ),
])
def testUpdateExtendPolishDictionaryListsMixedTypes(primusDictionary, secundusDictionary, expectedDictionary):
    """Test updateExtendPolishDictionaryLists with mixed types in values."""
    resultDictionary = updateExtendPolishDictionaryLists(primusDictionary, secundusDictionary)
    assert resultDictionary == expectedDictionary

def testUpdateExtendPolishDictionaryListsNonStringKeys():
    """Test updateExtendPolishDictionaryLists with non-string keys."""
    primusDictionary = {None: [3], True: [2]}
    secundusDictionary = {1: [1], (4, 5): [4]}
    expectedDictionary = {'(4, 5)': [4], '1': [1], 'None': [3], 'True': [2]}
    resultDictionary = updateExtendPolishDictionaryLists(primusDictionary, secundusDictionary)  # type: ignore
    assert resultDictionary == expectedDictionary

def testUpdateExtendPolishDictionaryListsConflictingDataTypes():
    """Test updateExtendPolishDictionaryLists with conflicting data types."""
    primusDictionary = {'a': 1, 'b': 2}
    secundusDictionary = {'a': 3, 'c': 4}
    with pytest.raises(TypeError):
        resultDictionary = updateExtendPolishDictionaryLists(primusDictionary, secundusDictionary)  # type: ignore

def testUpdateExtendPolishDictionaryListsKillErroneousDataTypes():
    """Test updateExtendPolishDictionaryLists with killErroneousDataTypes=True."""
    primusDictionary = {'a': [1, 2], 'b': [3, 4]}
    secundusDictionary = {'a': 3, 'c': 4}
    expectedDictionary = {'a': [1, 2], 'b': [3, 4]}
    resultDictionary = updateExtendPolishDictionaryLists(primusDictionary, secundusDictionary, killErroneousDataTypes=True)  # type: ignore
    assert resultDictionary == expectedDictionary

def testUpdateExtendPolishDictionaryListsBasicFunctionality():
    """Test basic functionality of updateExtendPolishDictionaryLists."""
    primusDictionary = {'a': [3, 1], 'b': [2]}
    secundusDictionary = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
    expectedDictionary = {'a': [3, 1, 9, 6, 1, 22, 3], 'b': [2, 111111, 2, 3]}
    resultDictionary = updateExtendPolishDictionaryLists(primusDictionary, secundusDictionary, destroyDuplicates=False, reorderLists=False)
    assert resultDictionary == expectedDictionary

def testUpdateExtendPolishDictionaryListsIgnoreOrdering():
    """Test updateExtendPolishDictionaryLists with reorderLists=True."""
    primusDictionary = {'a': [3, 1], 'b': [2]}
    secundusDictionary = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
    expectedDictionary = {'a': [1, 1, 3, 3, 6, 9, 22], 'b': [2, 2, 3, 111111]}
    resultDictionary = updateExtendPolishDictionaryLists(primusDictionary, secundusDictionary, destroyDuplicates=False, reorderLists=True)
    assert resultDictionary == expectedDictionary

def testUpdateExtendPolishDictionaryListsDestroyDuplicates():
    """Test updateExtendPolishDictionaryLists with destroyDuplicates=True."""
    primusDictionary = {'a': [3, 1], 'b': [2]}
    secundusDictionary = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
    expectedDictionary = {'a': [3, 1, 9, 6, 22], 'b': [2, 111111, 3]}
    resultDictionary = updateExtendPolishDictionaryLists(primusDictionary, secundusDictionary, destroyDuplicates=True, reorderLists=False)
    assert resultDictionary == expectedDictionary

def testUpdateExtendPolishDictionaryListsSingleSecundus():
    """Test updateExtendPolishDictionaryLists with empty primus dictionary."""
    primusDictionary = {}
    secundusDictionary = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
    expectedDictionary = secundusDictionary.copy()
    resultDictionary = updateExtendPolishDictionaryLists(primusDictionary, secundusDictionary, destroyDuplicates=False, reorderLists=False)
    assert resultDictionary == expectedDictionary

def testUpdateExtendPolishDictionaryListsEmptyDictionaries():
    """Test updateExtendPolishDictionaryLists with empty dictionaries."""
    primusDictionary = {}
    secundusDictionary = {}
    expectedDictionary = {}
    resultDictionary = updateExtendPolishDictionaryLists(primusDictionary, secundusDictionary, destroyDuplicates=False, reorderLists=False)
    assert resultDictionary == expectedDictionary

def testUpdateExtendPolishDictionaryListsWithSets():
    """Test updateExtendPolishDictionaryLists with sets as values."""
    primusDictionary = {'a': {3, 1}, 'b': {2}}
    secundusDictionary = {'a': {9, 6, 1, 22, 3}, 'b': {111111, 2, 3}}
    expectedDictionary = {'a': [1, 3, 6, 9, 22], 'b': [2, 3, 111111]}
    resultDictionary = updateExtendPolishDictionaryLists(primusDictionary, secundusDictionary, destroyDuplicates=True, reorderLists=True)  # type: ignore
    assert sorted(resultDictionary['a']) == expectedDictionary['a']

def testUpdateExtendPolishDictionaryListsWithTuples():
    """Test updateExtendPolishDictionaryLists with tuples as values."""
    primusDictionary = {'a': (3, 1), 'b': (2,)}
    secundusDictionary = {'a': (9, 6, 1, 22, 3), 'b': (111111, 2, 3)}
    expectedDictionary = {'a': [3, 1, 9, 6, 1, 22, 3], 'b': [2, 111111, 2, 3]}
    resultDictionary = updateExtendPolishDictionaryLists(primusDictionary, secundusDictionary, destroyDuplicates=False, reorderLists=False)
    assert resultDictionary == expectedDictionary

def testUpdateExtendPolishDictionaryListsWithNdarray():
    """Test updateExtendPolishDictionaryLists with numpy arrays as values."""
    primusDictionary = {'a': numpy.array([3, 1]), 'b': numpy.array([2])}
    secundusDictionary = {'a': numpy.array([9, 6, 1, 22, 3]), 'b': numpy.array([111111, 2, 3])}
    expectedDictionary = {'a': [3, 1, 9, 6, 1, 22, 3], 'b': [2, 111111, 2, 3]}
    resultDictionary = updateExtendPolishDictionaryLists(primusDictionary, secundusDictionary, destroyDuplicates=False, reorderLists=False)  # type: ignore
    assert resultDictionary == expectedDictionary