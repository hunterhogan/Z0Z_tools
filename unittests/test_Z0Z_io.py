import os
from pathlib import Path
import tempfile
import unittest
from Z0Z_tools.Z0Z_io import dataTabularTOpathFilenameDelimited, findRelativePath

class TestDataTabularTOpathFilenameDelimited(unittest.TestCase):
    """Test suite for dataTabularTOpathFilenameDelimited function."""

    def setUp(self):
        """Create a temporary directory and test files for each test."""
        self.directoryTemporary = tempfile.mkdtemp()
        self.pathDirectory = Path(self.directoryTemporary)
        self.pathFilenameTest = self.pathDirectory / 'test_output.txt'
        
        # Test data that multiple tests will use
        self.tableColumnsBasic = ['String', 'Integer', 'Float']
        self.tableRowsBasic = [
            ['apple', 1, 1.5],
            ['banana', 2, 2.5],
            ['cherry', 3, 3.5]
        ]

    def tearDown(self):
        """Clean up temporary files after each test."""
        import shutil
        try:
            if self.pathFilenameTest.exists():
                self.pathFilenameTest.unlink()
            shutil.rmtree(self.directoryTemporary)
        except Exception as ERRORmessage:
            print(f"Warning: Cleanup failed - {ERRORmessage}")

    def verifyFileContent(self, pathFilename: Path, expectedContent: str) -> None:
        """Helper method to verify file content."""
        self.assertTrue(pathFilename.exists(), f"File not created: {pathFilename}")
        self.assertTrue(pathFilename.is_file(), f"Not a file: {pathFilename}")
        
        try:
            with open(pathFilename, 'r') as readStream:
                content = readStream.read().strip()
            self.assertEqual(content, expectedContent.strip())
        except Exception as ERRORmessage:
            self.fail(f"Failed to verify file content: {ERRORmessage}")

    def test_basicFunctionality(self):
        """Test basic functionality with different data types."""
        dataTabularTOpathFilenameDelimited(
            self.pathFilenameTest, 
            self.tableRowsBasic, 
            self.tableColumnsBasic
        )
        
        expectedContent = (
            'String\tInteger\tFloat\n'
            'apple\t1\t1.5\n'
            'banana\t2\t2.5\n'
            'cherry\t3\t3.5'
        )
        
        self.verifyFileContent(self.pathFilenameTest, expectedContent)

    def test_differentDelimiters(self):
        """Test using different delimiters."""
        tableRows = [['A', 'B'], ['C', 'D']]
        tableColumns = ['Column1', 'Column2']

        for delimiterOutput in [',', ';', '^|']:
            pathFilenameTest = self.pathDirectory / f'test_delimiterOutput.csv'
            
            dataTabularTOpathFilenameDelimited(
                pathFilenameTest, 
                tableRows, 
                tableColumns, 
                delimiterOutput
            )
            
            expectedContent = (
                f'Column1{delimiterOutput}Column2\n'
                f'A{delimiterOutput}B\n'
                f'C{delimiterOutput}D'
            )
            
            self.verifyFileContent(pathFilenameTest, expectedContent)

    def test_emptyData(self):
        """Test handling of empty data."""
        # Test with empty rows
        dataTabularTOpathFilenameDelimited(
            self.pathFilenameTest, 
            [], 
            ['Column1', 'Column2']
        )
        self.verifyFileContent(self.pathFilenameTest, 'Column1\tColumn2')

        # Test with empty columns
        dataTabularTOpathFilenameDelimited(
            self.pathFilenameTest, 
            [['A', 'B']], 
            []
        )
        self.verifyFileContent(self.pathFilenameTest, 'A\tB')

    def test_filePermissions(self):
        """Test handling of file permission errors."""
        if os.name != 'nt':  # Skip on Windows
            readOnlyDir = self.pathDirectory / 'readonly'
            readOnlyDir.mkdir(mode=0o444)
            pathFilenameReadOnly = readOnlyDir / 'test.txt'
            
            with self.assertRaises(PermissionError):
                dataTabularTOpathFilenameDelimited(
                    pathFilenameReadOnly, 
                    self.tableRowsBasic, 
                    self.tableColumnsBasic
                )

class TestFindRelativePath(unittest.TestCase):
    """Test suite for findRelativePath function."""

    def test_sameDirectory(self):
        """Test paths in the same directory."""
        pathSource = Path('/a/b/c/file1.txt')
        pathDestination = Path('/a/b/c/file2.txt')
        self.assertEqual(findRelativePath(pathSource, pathDestination), 'file2.txt')

    def test_parentChild(self):
        """Test parent to child directory relationships."""
        pathSource = Path('/a/b/c')
        pathDestination = Path('/a/b/c/d/e')
        self.assertEqual(findRelativePath(pathSource, pathDestination), 'd/e')

        # Child to parent
        self.assertEqual(findRelativePath(pathDestination, pathSource), '../..')

    def test_siblings(self):
        """Test sibling directory relationships."""
        pathSource = Path('/a/b/c1/d')
        pathDestination = Path('/a/b/c2/e')
        self.assertEqual(findRelativePath(pathSource, pathDestination), '../../c2/e')

    def test_differentBranches(self):
        """Test paths on completely different branches."""
        pathSource = Path('/a/b/c/d')
        pathDestination = Path('/w/x/y/z')
        self.assertEqual(findRelativePath(pathSource, pathDestination), '../../../../w/x/y/z')

    def test_stringInputs(self):
        """Test with string inputs instead of Path objects."""
        pathSource = '/a/b/c'
        pathDestination = '/a/b/d'
        self.assertEqual(findRelativePath(pathSource, pathDestination), '../d')

    def test_mixedInputTypes(self):
        """Test with mixed input types (string and Path)."""
        pathSource = '/a/b/c'
        pathDestination = Path('/a/b/d')
        self.assertEqual(findRelativePath(pathSource, pathDestination), '../d')
        self.assertEqual(findRelativePath(pathDestination, pathSource), '../c')

if __name__ == '__main__':
    unittest.main()