import unittest
from Z0Z_tools.Z0Z_dataStructure import updateExtendPolishDictionaryLists

class TestUpdateExtendDictionaryLists(unittest.TestCase):

    def test_basic_functionality(self):
        primus = {'a': [3, 1], 'b': [2]}
        secundus = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        expected = {'a': [3, 1, 9, 6, 1, 22, 3], 'b': [2, 111111, 2, 3]}
        result = updateExtendPolishDictionaryLists(primus, secundus, destroyDuplicates=False, ignoreListOrdering=False)
        self.assertEqual(result, expected)

    def test_ignore_list_ordering(self):
        primus = {'a': [3, 1], 'b': [2]}
        secundus = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        expected = {'a': [1, 1, 3, 3, 6, 9, 22], 'b': [2, 2, 3, 111111]}
        result = updateExtendPolishDictionaryLists(primus, secundus, destroyDuplicates=False, ignoreListOrdering=True)
        self.assertEqual(result, expected)

    def test_destroy_duplicates(self):
        primus = {'a': [3, 1], 'b': [2]}
        secundus = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        expected = {'a': [3, 1, 9, 6, 22], 'b': [2, 111111, 3]}
        result = updateExtendPolishDictionaryLists(primus, secundus, destroyDuplicates=True, ignoreListOrdering=False)
        self.assertEqual(result, expected)

    def test_single_dictionary_secundus2(self):
        secundus = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        expected = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        result = updateExtendPolishDictionaryLists({}, secundus, destroyDuplicates=False, ignoreListOrdering=False)
        self.assertEqual(result, expected)

    def test_single_dictionary_secundus_ignore_list_ordering2(self):
        secundus = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        expected = {'a': [1, 3, 6, 9, 22], 'b': [2, 3, 111111]}
        result = updateExtendPolishDictionaryLists({}, secundus, destroyDuplicates=False, ignoreListOrdering=True)
        self.assertEqual(result, expected)

    def test_single_dictionary_secundus_destroy_duplicates2(self):
        secundus = {'a': [9, 6, 1, 22, 3, 9], 'b': [111111, 2, 3, 2]}
        expected = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        result = updateExtendPolishDictionaryLists({}, secundus, destroyDuplicates=True, ignoreListOrdering=False)
        self.assertEqual(result, expected)

    def test_single_dictionary_secundus_destroy_duplicates_ignore_list_ordering2(self):
        secundus = {'a': [9, 6, 1, 22, 3, 9], 'b': [111111, 2, 3, 2]}
        expected = {'a': [1, 3, 6, 9, 22], 'b': [2, 3, 111111]}
        result = updateExtendPolishDictionaryLists({}, secundus, destroyDuplicates=True, ignoreListOrdering=True)
        self.assertEqual(result, expected)
    def test_empty_dictionaries(self):
        primus = {}
        secundus = {}
        expected = {}
        result = updateExtendPolishDictionaryLists(primus, secundus, destroyDuplicates=False, ignoreListOrdering=False)
        self.assertEqual(result, expected)

    def test_empty_and_non_empty_dictionary(self):
        primus = {}
        secundus = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        expected = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        result = updateExtendPolishDictionaryLists(primus, secundus, destroyDuplicates=False, ignoreListOrdering=False)
        self.assertEqual(result, expected)

    def test_non_empty_and_empty_dictionary(self):
        primus = {'a': [3, 1], 'b': [2]}
        secundus = {}
        expected = {'a': [3, 1], 'b': [2]}
        result = updateExtendPolishDictionaryLists(primus, secundus, destroyDuplicates=False, ignoreListOrdering=False)
        self.assertEqual(result, expected)

    def test_empty_dictionaries_with_options(self):
        primus = {}
        secundus = {}
        expected = {}
        result = updateExtendPolishDictionaryLists(primus, secundus, destroyDuplicates=True, ignoreListOrdering=True)
        self.assertEqual(result, expected)

    def test_single_empty_dictionary(self):
        primus = {}
        expected = {}
        result = updateExtendPolishDictionaryLists(primus, destroyDuplicates=False, ignoreListOrdering=False)
        self.assertEqual(result, expected)

    def test_single_empty_dictionary_with_options(self):
        primus = {}
        expected = {}
        result = updateExtendPolishDictionaryLists(primus, destroyDuplicates=True, ignoreListOrdering=True)
        self.assertEqual(result, expected)

    def test_single_dictionary_primus(self):
        primus = {'a': [3, 1], 'b': [2]}
        expected = {'a': [3, 1], 'b': [2]}
        result = updateExtendPolishDictionaryLists(primus, destroyDuplicates=False, ignoreListOrdering=False)
        self.assertEqual(result, expected)

    def test_single_dictionary_primus_ignore_list_ordering_variant(self):
        primus = {'a': [3, 1], 'b': [2]}
        expected = {'a': [1, 3], 'b': [2]}
        result = updateExtendPolishDictionaryLists(primus, destroyDuplicates=False, ignoreListOrdering=True)
        self.assertEqual(result, expected)

    def test_single_dictionary_primus_destroy_duplicates_ignore_list_ordering_variant(self):
        primus = {'a': [3, 1, 3], 'b': [2, 2]}
        expected = {'a': [3, 1], 'b': [2]}
        result = updateExtendPolishDictionaryLists(primus, destroyDuplicates=True, ignoreListOrdering=False)
        self.assertEqual(result, expected)

    def test_single_dictionary_primus_destroy_duplicates_ignore_list_ordering(self):
        primus = {'a': [3, 1, 3], 'b': [2, 2]}
        expected = {'a': [1, 3], 'b': [2]}
        result = updateExtendPolishDictionaryLists(primus, destroyDuplicates=True, ignoreListOrdering=True)
        self.assertEqual(result, expected)

    def test_single_dictionary_secundus(self):
        secundus = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        expected = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        result = updateExtendPolishDictionaryLists(secundus, destroyDuplicates=False, ignoreListOrdering=False)
        self.assertEqual(result, expected)

    def test_single_dictionary_secundus_ignore_list_ordering(self):
        secundus = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        expected = {'a': [1, 3, 6, 9, 22], 'b': [2, 3, 111111]}
        result = updateExtendPolishDictionaryLists(secundus, destroyDuplicates=False, ignoreListOrdering=True)
        self.assertEqual(result, expected)

    def test_single_dictionary_secundus_destroy_duplicates(self):
        secundus = {'a': [9, 6, 1, 22, 3, 9], 'b': [111111, 2, 3, 2]}
        expected = {'a': [9, 6, 1, 22, 3], 'b': [111111, 2, 3]}
        result = updateExtendPolishDictionaryLists(secundus, destroyDuplicates=True, ignoreListOrdering=False)
        self.assertEqual(result, expected)

    def test_single_dictionary_secundus_destroy_duplicates_ignore_list_ordering(self):
        secundus = {'a': [9, 6, 1, 22, 3, 9], 'b': [111111, 2, 3, 2]}
        expected = {'a': [1, 3, 6, 9, 22], 'b': [2, 3, 111111]}
        result = updateExtendPolishDictionaryLists(secundus, destroyDuplicates=True, ignoreListOrdering=True)
        self.assertEqual(result, expected)
if __name__ == '__main__':
    unittest.main()
