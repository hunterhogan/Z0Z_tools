from typing import Optional, Union
import unittest
from unittest.mock import patch
from Z0Z_tools import defineConcurrencyLimit, oopsieKwargsie

class TestOopsieKwargsie(unittest.TestCase):
    """Test suite for oopsieKwargsie function."""

    def test_trueVariants(self):
        """Test various string representations of True."""
        trueVariants = ['True', 'TRUE', ' true ', 'TrUe']
        for variant in trueVariants:
            self.assertTrue(oopsieKwargsie(variant))

    def test_falseVariants(self):
        """Test various string representations of False."""
        falseVariants = ['False', 'FALSE', ' false ', 'FaLsE']
        for variant in falseVariants:
            self.assertFalse(oopsieKwargsie(variant))

    def test_noneVariants(self):
        """Test various string representations of None."""
        noneVariants = ['None', 'NONE', ' none ', 'NoNe']
        for variant in noneVariants:
            self.assertIsNone(oopsieKwargsie(variant))

    def test_otherStrings(self):
        """Test strings that should be returned unchanged."""
        testStrings = ['hello', '123', 'True story', 'False alarm']
        for testString in testStrings:
            self.assertEqual(oopsieKwargsie(testString), testString)

class TestDefineConcurrencyLimit(unittest.TestCase):
    """Test suite for defineConcurrencyLimit function."""

    def setUp(self):
        """Set up test fixtures."""
        self.cpuCountMocked = 8  # Define fixed CPU count for testing

    def runTestWithCPUcount(self, limitTest: Optional[Union[int, float, bool]], expectedResult: int) -> None:
        """Helper method to run tests with mocked CPU count."""
        with patch('multiprocessing.cpu_count', return_value=self.cpuCountMocked):
            resultTest = defineConcurrencyLimit(limitTest)
            self.assertEqual(resultTest, expectedResult)

    def test_defaultValues(self):
        """Test behavior with None, False, and 0."""
        for limitTest in [None, False, 0]:
            self.runTestWithCPUcount(limitTest, self.cpuCountMocked)

    def test_directInteger(self):
        """Test with direct integer values >= 1."""
        testCases = [
            (1, 1),
            (4, 4),
            (16, 16)
        ]
        for limitTest, expectedResult in testCases:
            self.runTestWithCPUcount(limitTest, expectedResult)

    def test_fractionFloat(self):
        """Test with float values between 0 and 1."""
        testCases = [
            (0.5, 4),  # 8 * 0.5 = 4
            (0.25, 2),  # 8 * 0.25 = 2
            (0.75, 6)  # 8 * 0.75 = 6
        ]
        for limitTest, expectedResult in testCases:
            self.runTestWithCPUcount(limitTest, expectedResult)

    def test_negativeFraction(self):
        """Test with float values between -1 and 0."""
        testCases = [
            (-0.5, 4),  # 8 - (8 * 0.5) = 4
            (-0.25, 6),  # 8 - (8 * 0.25) = 6
            (-0.75, 2)  # 8 - (8 * 0.75) = 2
        ]
        for limitTest, expectedResult in testCases:
            self.runTestWithCPUcount(limitTest, expectedResult)

    def test_negativeInteger(self):
        """Test with integer values <= -1."""
        testCases = [
            (-1, 7),  # 8 - 1 = 7
            (-3, 5),  # 8 - 3 = 5
            (-7, 1)  # 8 - 7 = 1 (minimum value)
        ]
        for limitTest, expectedResult in testCases:
            self.runTestWithCPUcount(limitTest, expectedResult)

    def test_booleanTrue(self):
        """Test with boolean True."""
        self.runTestWithCPUcount(True, 1)
        # Test the specific True case branch
        with patch('multiprocessing.cpu_count', return_value=self.cpuCountMocked):
            resultTest = defineConcurrencyLimit(True)
            self.assertEqual(resultTest, 1)
            # Ensure it's not just coincidentally 1
            self.assertNotEqual(defineConcurrencyLimit(None), 1)

    @patch('Z0Z_tools.parseParameters.oopsieKwargsie')
    def test_stringValues(self, mockOopsieKwargsie):
        """Test string value handling via oopsieKwargsie."""
        testCases = [
            ("true", True, 1),
            ("false", False, self.cpuCountMocked),
            ("none", None, self.cpuCountMocked),
            ("4", 4, 4)
        ]
        for stringInput, oopsieReturn, expectedResult in testCases:
            mockOopsieKwargsie.return_value = oopsieReturn
            self.runTestWithCPUcount(stringInput, expectedResult)

    def test_ensureMinimumOne(self):
        """Test that return value is never less than 1."""
        testCases = [
            (-10, 1),  # Would be -2, but minimum is 1
            (-0.99, 1),  # Would be ~0, but minimum is 1
            (0.1, 1)  # Would be 0.8, but minimum is 1
        ]
        for limitTest, expectedResult in testCases:
            self.runTestWithCPUcount(limitTest, expectedResult)

if __name__ == '__main__':
    unittest.main()