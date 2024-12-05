from pathlib import Path
import tempfile
import unittest
from Z0Z_tools.Z0Z_io import dataTabularTOpathFilenameDelimited

class TestDataTabularTOpathFilenameDelimited(unittest.TestCase):
    """Test suite for dataTabularTOpathFilenameDelimited function."""

    def test_basicFunctionality(self):
        """Test basic functionality with different data types."""
        with tempfile.TemporaryDirectory() as tempdir:
            pathFilenameTest = Path(tempdir) / 'test_output.txt'
            
            tableColumns = ['String', 'Integer', 'Float']
            tableRows = [
                ['apple', 1, 1.5],
                ['banana', 2, 2.5],
                ['cherry', 3, 3.5]
            ]

            dataTabularTOpathFilenameDelimited(pathFilenameTest, tableRows, tableColumns)

            # Verify file content
            with open(pathFilenameTest, 'r') as readStream:
                lines = readStream.readlines()
                
            self.assertEqual(lines[0].strip(), 'String\tInteger\tFloat')
            self.assertEqual(lines[1].strip(), 'apple\t1\t1.5')
            self.assertEqual(lines[2].strip(), 'banana\t2\t2.5')
            self.assertEqual(lines[3].strip(), 'cherry\t3\t3.5')

    def test_differentDelimiters(self):
        """Test using different delimiters."""
        with tempfile.TemporaryDirectory() as tempdir:
            pathFilenameTest = Path(tempdir) / 'test_output.csv'
            
            tableColumns = ['Column1', 'Column2']
            tableRows = [['A', 'B'], ['C', 'D']]

            for delimiterOutput in [',', ';', '|']:
                dataTabularTOpathFilenameDelimited(
                    pathFilenameTest, tableRows, tableColumns, delimiterOutput)

                with open(pathFilenameTest, 'r') as readStream:
                    content = readStream.read()
                
                self.assertTrue(delimiterOutput.join(['Column1', 'Column2']) in content)
                self.assertTrue(delimiterOutput.join(['A', 'B']) in content)

    def test_emptyData(self):
        """Test handling of empty data."""
        with tempfile.TemporaryDirectory() as tempdir:
            pathFilenameTest = Path(tempdir) / 'test_empty.txt'
            
            # Test with empty rows
            dataTabularTOpathFilenameDelimited(
                pathFilenameTest, [], ['Column1', 'Column2'])
            
            with open(pathFilenameTest, 'r') as readStream:
                content = readStream.read().strip()
                self.assertEqual(content, 'Column1\tColumn2')

            # Test with empty columns
            dataTabularTOpathFilenameDelimited(
                pathFilenameTest, [['A', 'B']], [])
            
            with open(pathFilenameTest, 'r') as readStream:
                content = readStream.read().strip()
                self.assertEqual(content, 'A\tB')

if __name__ == '__main__':
    unittest.main()