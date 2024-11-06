import unittest
from Z0Z_tools.Z0Z_dataStructure import updateExtendPolishDictionaryLists, stringItUp
import numpy

class TestUpdateExtendDictionaryLists(unittest.TestCase):

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

class TestStringItUp(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()