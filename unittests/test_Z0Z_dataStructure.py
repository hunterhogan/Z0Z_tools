from decimal import Decimal
from fractions import Fraction
from itertools import count, islice
from Z0Z_tools.Z0Z_dataStructure import updateExtendPolishDictionaryLists, stringItUp
import datetime
import numpy
import unittest
import uuid

class TestStringItUp(unittest.TestCase):

    def test_empty_input(self):
        self.assertEqual(stringItUp(), [])

    def test_with_bytearray(self):
        self.assertEqual(stringItUp(bytearray(b"bytearray")), ["bytearray(b'bytearray')"])

    def test_with_generator(self):
        def gen():
            for i in range(3):
                yield i
        self.assertEqual(stringItUp(gen()), ['0', '1', '2'])

    def test_with_infinite_iterator(self):
        infinite_gen = count()
        limited_gen = islice(infinite_gen, 5)
        self.assertEqual(stringItUp(limited_gen), ['0', '1', '2', '3', '4'])

    def test_with_object_with_custom_iter(self):
        class CustomIter:
            def __iter__(self):
                return iter([1, 2, 3])
        self.assertEqual(stringItUp(CustomIter()), ['1', '2', '3'])

    def test_with_recursive_structure(self):
        chicken_tikka_masala = []
        chicken_tikka_masala.append(chicken_tikka_masala)
        self.assertEqual(stringItUp(chicken_tikka_masala), ['[[...]]'])

    def test_with_recursive_structure2(self):
        chicken_tikka_masala = []
        chicken_tikka_masala.append(chicken_tikka_masala)
        self.assertEqual(stringItUp([chicken_tikka_masala, 'wazzup']), ["[[[...]], 'wazzup']"])

    def test_with_nan_and_inf(self):
        self.assertEqual(stringItUp(float('nan'), float('inf')), ['nan', 'inf'])

    def test_with_large_numbers(self):
        large_number = 10**100
        self.assertEqual(stringItUp(large_number), [str(large_number)])

    def test_with_decimal(self):
        self.assertEqual(stringItUp(Decimal('1.1')), ['1.1'])

    def test_with_fraction(self):
        self.assertEqual(stringItUp(Fraction(1, 3)), ['1/3'])

    def test_with_dates(self):
        date = datetime.date(2021, 1, 1)
        self.assertEqual(stringItUp(date), ['2021-01-01'])

    def test_with_times(self):
        time = datetime.time(12, 34, 56)
        self.assertEqual(stringItUp(time), ['12:34:56'])

    def test_with_datetime(self):
        dt = datetime.datetime(2021, 1, 1, 12, 34, 56)
        self.assertEqual(stringItUp(dt), ['2021-01-01 12:34:56'])

    def test_with_uuid(self):
        my_uuid = uuid.uuid4()
        self.assertEqual(stringItUp(my_uuid), [str(my_uuid)])

    def test_with_memoryview(self):
        result = stringItUp(memoryview(b"memoryview"))
        expected_prefix = "<memory at 0x"
        self.assertTrue(result[0].startswith(expected_prefix))

    def test_empty_iterable_types(self):
        self.assertEqual(stringItUp([], (), set()), [])

    def test_mixed_nested_iterables(self):
        data = [1, (2, {3, "four"}), {"five": [6, 7]}]
        self.assertCountEqual(stringItUp(data), ["1", "2", "3", "four", "five", "6", "7"])

    def test_large_data(self):
        large_list = list(range(1000))
        result = stringItUp(large_list)
        self.assertEqual(len(result), 1000)
        for i in range(1000):
            self.assertEqual(result[i], str(i))

class TestUpdateExtendDictionaryLists(unittest.TestCase):

    def test_with_mixed_types_in_values(self):
        primus = {'a': [1, 'two'], 'b': [True, None]}
        secundus = {'a': [3.14, 'four'], 'b': [False, 'none']}
        expected = {
            'a': [1, 'two', 3.14, 'four'],
            'b': [True, None, False, 'none']
        }
        result = updateExtendPolishDictionaryLists(primus, secundus)
        self.assertEqual(result, expected)

    def test_with_non_string_keys(self):
        primus = {None: [3], True: [2]}
        secundus = {1: [1], (4, 5): [4]}
        expected ={'(4, 5)': [4], '1': [1], 'None': [3], 'True': [2]}
        result = updateExtendPolishDictionaryLists(primus, secundus) # type: ignore
        self.assertEqual(result, expected)

    def test_with_conflicting_data_types(self):
        primus = {'a': 1, 'b': 2}
        secundus = {'a': 3, 'c': 4}
        with self.assertRaises(TypeError):
            result = updateExtendPolishDictionaryLists(primus, secundus) # type: ignore

    def test_with_kill_erroneous_data_types(self):
        primus = {'a': [1, 2], 'b': [3, 4]}
        secundus = {'a': 3, 'c': 4}
        expected = {'a': [1, 2], 'b': [3, 4]}
        result = updateExtendPolishDictionaryLists(primus, secundus, killErroneousDataTypes=True) # type: ignore
        self.assertEqual(result, expected)

    def test_basic_functionality(self):
        primus = {'a': [3, 1], 'b': [2]}
        secundus = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        expected = {'a': [3, 1, 9, 6, 1, 22, 3], 'b': [2, 111111, 2, 3]}
        result = updateExtendPolishDictionaryLists(primus, secundus, destroyDuplicates=False, reorderLists=False)
        self.assertEqual(result, expected)

    def test_ignore_list_ordering(self):
        primus = {'a': [3, 1], 'b': [2]}
        secundus = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        expected = {'a': [1, 1, 3, 3, 6, 9, 22], 'b': [2, 2, 3, 111111]}
        result = updateExtendPolishDictionaryLists(primus, secundus, destroyDuplicates=False, reorderLists=True)
        self.assertEqual(result, expected)

    def test_destroy_duplicates(self):
        primus = {'a': [3, 1], 'b': [2]}
        secundus = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        expected = {'a': [3, 1, 9, 6, 22], 'b': [2, 111111, 3]}
        result = updateExtendPolishDictionaryLists(primus, secundus, destroyDuplicates=True, reorderLists=False)
        self.assertEqual(result, expected)

    def test_single_dictionary_secundus2(self):
        secundus = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        expected = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        result = updateExtendPolishDictionaryLists({}, secundus, destroyDuplicates=False, reorderLists=False)
        self.assertEqual(result, expected)

    def test_single_dictionary_secundus_ignore_list_ordering2(self):
        secundus = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        expected = {'a': [1, 3, 6, 9, 22], 'b': [2, 3, 111111]}
        result = updateExtendPolishDictionaryLists({}, secundus, destroyDuplicates=False, reorderLists=True)
        self.assertEqual(result, expected)

    def test_single_dictionary_secundus_destroy_duplicates2(self):
        secundus = {'a': [9, 6, 1, 22, 3, 9], 'b': [111111, 2, 3, 2]}
        expected = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        result = updateExtendPolishDictionaryLists({}, secundus, destroyDuplicates=True, reorderLists=False)
        self.assertEqual(result, expected)

    def test_single_dictionary_secundus_destroy_duplicates_ignore_list_ordering2(self):
        secundus = {'a': [9, 6, 1, 22, 3, 9], 'b': [111111, 2, 3, 2]}
        expected = {'a': [1, 3, 6, 9, 22], 'b': [2, 3, 111111]}
        result = updateExtendPolishDictionaryLists({}, secundus, destroyDuplicates=True, reorderLists=True)
        self.assertEqual(result, expected)

    def test_empty_dictionaries(self):
        primus = {}
        secundus = {}
        expected = {}
        result = updateExtendPolishDictionaryLists(primus, secundus, destroyDuplicates=False, reorderLists=False)
        self.assertEqual(result, expected)

    def test_empty_and_non_empty_dictionary(self):
        primus = {}
        secundus = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        expected = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        result = updateExtendPolishDictionaryLists(primus, secundus, destroyDuplicates=False, reorderLists=False)
        self.assertEqual(result, expected)

    def test_non_empty_and_empty_dictionary(self):
        primus = {'a': [3, 1], 'b': [2]}
        secundus = {}
        expected = {'a': [3, 1], 'b': [2]}
        result = updateExtendPolishDictionaryLists(primus, secundus, destroyDuplicates=False, reorderLists=False)
        self.assertEqual(result, expected)

    def test_empty_dictionaries_with_options(self):
        primus = {}
        secundus = {}
        expected = {}
        result = updateExtendPolishDictionaryLists(primus, secundus, destroyDuplicates=True, reorderLists=True)
        self.assertEqual(result, expected)

    def test_single_empty_dictionary(self):
        primus = {}
        expected = {}
        result = updateExtendPolishDictionaryLists(primus, destroyDuplicates=False, reorderLists=False)
        self.assertEqual(result, expected)

    def test_single_empty_dictionary_with_options(self):
        primus = {}
        expected = {}
        result = updateExtendPolishDictionaryLists(primus, destroyDuplicates=True, reorderLists=True)
        self.assertEqual(result, expected)

    def test_single_dictionary_primus(self):
        primus = {'a': [3, 1], 'b': [2]}
        expected = {'a': [3, 1], 'b': [2]}
        result = updateExtendPolishDictionaryLists(primus, destroyDuplicates=False, reorderLists=False)
        self.assertEqual(result, expected)

    def test_single_dictionary_primus_ignore_list_ordering_variant(self):
        primus = {'a': [3, 1], 'b': [2]}
        expected = {'a': [1, 3], 'b': [2]}
        result = updateExtendPolishDictionaryLists(primus, destroyDuplicates=False, reorderLists=True)
        self.assertEqual(result, expected)

    def test_single_dictionary_primus_destroy_duplicates_ignore_list_ordering_variant(self):
        primus = {'a': [3, 1, 3], 'b': [2, 2]}
        expected = {'a': [3, 1], 'b': [2]}
        result = updateExtendPolishDictionaryLists(primus, destroyDuplicates=True, reorderLists=False)
        self.assertEqual(result, expected)

    def test_single_dictionary_primus_destroy_duplicates_ignore_list_ordering(self):
        primus = {'a': [3, 1, 3], 'b': [2, 2]}
        expected = {'a': [1, 3], 'b': [2]}
        result = updateExtendPolishDictionaryLists(primus, destroyDuplicates=True, reorderLists=True)
        self.assertEqual(result, expected)

    def test_single_dictionary_secundus(self):
        secundus = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        expected = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        result = updateExtendPolishDictionaryLists(secundus, destroyDuplicates=False, reorderLists=False)
        self.assertEqual(result, expected)

    def test_single_dictionary_secundus_ignore_list_ordering(self):
        secundus = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        expected = {'a': [1, 3, 6, 9, 22], 'b': [2, 3, 111111]}
        result = updateExtendPolishDictionaryLists(secundus, destroyDuplicates=False, reorderLists=True)
        self.assertEqual(result, expected)

    def test_single_dictionary_secundus_destroy_duplicates(self):
        secundus = {'a': [9, 6, 1, 22, 3, 9], 'b': [111111, 2, 3, 2]}
        expected = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        result = updateExtendPolishDictionaryLists(secundus, destroyDuplicates=True, reorderLists=False)
        self.assertEqual(result, expected)

    def test_single_dictionary_secundus_destroy_duplicates_ignore_list_ordering(self):
        secundus = {'a': [9, 6, 1, 22, 3, 9], 'b': [111111, 2, 3, 2]}
        expected = {'a': [1, 3, 6, 9, 22], 'b': [2, 3, 111111]}
        result = updateExtendPolishDictionaryLists(secundus, destroyDuplicates=True, reorderLists=True)
        self.assertEqual(result, expected)

    def test_with_sets(self):
        primus = {'a': {3, 1}, 'b': {2}}
        secundus = {'a': {9, 6, 1, 22, 3}, 'b': {111111, 2, 3}}
        expected = {'a': [3, 1, 9, 6, 22], 'b': [2, 111111, 3]}
        result = updateExtendPolishDictionaryLists(primus, secundus, destroyDuplicates=True, reorderLists=False) # type: ignore
        self.assertCountEqual(result['a'], expected['a'])

    def test_with_tuples(self):
        primus = {'a': (3, 1), 'b': (2,)}
        secundus = {'a': (9, 6, 1, 22, 3), 'b': (111111, 2, 3)}
        expected = {'a': [3, 1, 9, 6, 1, 22, 3], 'b': [2, 111111, 2, 3]}
        result = updateExtendPolishDictionaryLists(primus, secundus, destroyDuplicates=False, reorderLists=False)
        self.assertEqual(result, expected)

    def test_with_ndarray(self):
        primus = {'a': numpy.array([3, 1]), 'b': numpy.array([2])}
        secundus = {'a': numpy.array([9, 6, 1, 22, 3]), 'b': numpy.array([111111, 2, 3])}
        expected = {'a': [3, 1, 9, 6, 1, 22, 3], 'b': [2, 111111, 2, 3]}
        result = updateExtendPolishDictionaryLists(primus, secundus, destroyDuplicates=False, reorderLists=False) # type: ignore
        self.assertEqual(result, expected)

    def test_empty_input(self):
        self.assertEqual(stringItUp(), [])

    def test_single_string(self):
        self.assertEqual(stringItUp("hello"), ["hello"])

    def test_single_integer(self):
        self.assertEqual(stringItUp(123), ["123"])

    def test_single_float(self):
        self.assertEqual(stringItUp(3.14), ["3.14"])

    def test_single_list(self):
        self.assertCountEqual(stringItUp([1, 2, "three"]), ["1", "2", "three"])

    def test_single_tuple(self):
        self.assertCountEqual(stringItUp((1, 2, "three")), ["1", "2", "three"])

    def test_single_set(self):
        self.assertCountEqual(stringItUp({1, 2, "three"}), ["1", "2", "three"])

    def test_single_dict(self):
        self.assertCountEqual(stringItUp({"a": 1, "b": "two"}), ["a", "1", "b", "two"])

    def test_nested_list(self):
        self.assertCountEqual(stringItUp([1, [2, "three"], 4]), ["1", "2", "three", "4"])

    def test_nested_tuple(self):
        self.assertCountEqual(stringItUp((1, (2, "three"), 4)), ["1", "2", "three", "4"])

    def test_nested_set(self):
        self.assertCountEqual(stringItUp({1, frozenset({2, "three"}), 4}), ["1", "2", "three", "4"])

    def test_nested_dict(self):
        self.assertCountEqual(stringItUp({"a": 1, "b": {"c": 2, "d": "three"}}), ["a", "1", "b", "c", "2", "d", "three"])

    def test_mixed_data_types(self):
        self.assertCountEqual(stringItUp(1, "two", [3, "four"], {"five": 5}), ["1", "two", "3", "four", "five", "5"])

    def test_with_numpy_array(self):
        self.assertCountEqual(stringItUp(numpy.array([1, 2, 3])), ["1", "2", "3"])

    def test_with_custom_object(self):
        class MyObject:
            def __str__(self):
                return "MyObject"
        self.assertEqual(stringItUp(MyObject()), ["MyObject"])

    def test_with_none(self):
        self.assertEqual(stringItUp(None), ["None"])

    def test_with_boolean(self):
        self.assertCountEqual(stringItUp(True, False), ["True", "False"])

    def test_with_complex_number(self):
        self.assertEqual(stringItUp(1+2j), ["(1+2j)"])

    def test_with_bytes(self):
        self.assertEqual(stringItUp(b"bytes"), ["b'bytes'"])

if __name__ == '__main__':
    unittest.main()