from Z0Z_tools import makeListRequirementsFromRequirementsFile, installPackageTarget
from Z0Z_tools.pipAnything import make_setupDOTpy
from pathlib import Path
import unittest
from unittest.mock import patch, Mock

class TestPipAnything(unittest.TestCase):
    @patch('builtins.open', new_callable=Mock(return_value=Mock(readlines=['package1\n', 'package2==1.0.0\n', '#comment\n', ' \n', '\t\n'])))
    def test_makeListRequirementsFromRequirementsFile(self):
        # Test with valid requirements.txt content
        listRequirements = makeListRequirementsFromRequirementsFile('requirements.txt')
        self.assertEqual(listRequirements, ['package1', 'package2==1.0.0'])

    def test_make_setupDOTpy(self):
        # Test setup.py content generation
        relativePathPackage = 'my_package'
        listRequirements = ['numpy', 'pandas']
        setupContent = make_setupDOTpy(relativePathPackage, listRequirements)
        self.assertIn(f"name='{Path(relativePathPackage).name}'", setupContent)
        self.assertIn(f"packages=find_packages(where=r'{relativePathPackage}')", setupContent)
        self.assertIn(f"package_dir={{'': r'{relativePathPackage}'}}", setupContent)
        self.assertIn(f"install_requires={listRequirements}", setupContent)

    @patch('subprocess.Popen')
    @patch('tempfile.mkdtemp')
    @patch('pathlib.Path.open')
    def test_installPackageTarget(self, mock_open_file, mock_mkdtemp, mock_subprocess):
        # Mocking external dependencies
        mock_mkdtemp.return_value = '/tmp/temp_dir'
        mock_process = Mock()
        mock_process.returncode = 0  # Simulate successful pip install
        mock_subprocess.return_value = mock_process

        # Test installPackageTarget function
        installPackageTarget('my_package')

        # Assertions to check if the function interacts with dependencies as expected
        mock_mkdtemp.assert_called_once()
        mock_open_file.assert_called_once()
        mock_subprocess.assert_called_once()

if __name__ == "__main__":
    unittest.main()