from pathlib import Path
from unittest.mock import patch, MagicMock
from Z0Z_tools import pipAnything
import tempfile
import unittest
import sys
import subprocess

class TestPipAnything(unittest.TestCase):

    def test_makeListRequirementsFromRequirementsFile(self):
        """
        Test the makeListRequirementsFromRequirementsFile function.
        """
        with tempfile.TemporaryDirectory() as tempdir:
            # Create a temporary requirements file
            requirements_file = Path(tempdir) / 'requirements.txt'
            requirements_content = """
            # This is a comment
            package-A==1.2.3
            package-B>=4.5.6,<=7.8.9
            package_C
            # Another comment
            analyzeAudio@git+https://github.com/hunterhogan/analyzeAudio.git
            """
            requirements_file.write_text(requirements_content)

            # Test with a single file
            requirements = pipAnything.makeListRequirementsFromRequirementsFile(requirements_file)
            self.assertEqual(len(requirements), 4)
            self.assertIn('package-A==1.2.3', requirements)
            self.assertIn('package-B>=4.5.6,<=7.8.9', requirements)
            self.assertIn('package_C', requirements)
            self.assertIn('analyzeAudio@git+https://github.com/hunterhogan/analyzeAudio.git', requirements)

            # Test with multiple files
            requirements2 = pipAnything.makeListRequirementsFromRequirementsFile(requirements_file, requirements_file)
            self.assertEqual(len(requirements2), 4)  # Should still be 4, duplicates removed

            # Test with non-existent file
            nonexistent_file = Path(tempdir) / 'nonexistent.txt'
            requirements3 = pipAnything.makeListRequirementsFromRequirementsFile(nonexistent_file)
            self.assertEqual(len(requirements3), 0)  # Should be empty

    def test_make_setupDOTpy(self):
        """
        Test the make_setupDOTpy function.
        """
        relative_path_package = 'my_package'
        list_requirements = ['numpy', 'pandas']
        setup_content = pipAnything.make_setupDOTpy(relative_path_package, list_requirements)

        # Check if the generated content contains expected elements
        self.assertIn(f"name='{Path(relative_path_package).name}'", setup_content)
        self.assertIn(f"packages=find_packages(where=r'{relative_path_package}')", setup_content)
        self.assertIn(f"package_dir={{'': r'{relative_path_package}'}}", setup_content)
        self.assertIn(f"install_requires={list_requirements},", setup_content)
        self.assertIn("include_package_data=True", setup_content)

    @patch('subprocess.Popen')
    @patch('tempfile.mkdtemp')
    def test_installPackageTarget(self, mockMkdtemp, mockPopen):
        """Test the installPackageTarget function."""
        # Setup mocks
        mockTempDir = str(Path('unittests/dataSamples/tmp/fake_temp_dir').resolve())
        mockMkdtemp.return_value = mockTempDir
        
        mockProcess = MagicMock()
        mockProcess.stdout = ['Installing...', 'Done!']
        mockProcess.wait.return_value = 0
        mockPopen.return_value = mockProcess

        with tempfile.TemporaryDirectory() as tempdir:
            # Create a fake package directory
            package_dir = Path(tempdir) / 'test_package'
            package_dir.mkdir(parents=True, exist_ok=True)
            
            # Create requirements.txt
            requirements_file = package_dir / 'requirements.txt'
            requirements_file.write_text('numpy\npandas')

            # Test installation
            pipAnything.installPackageTarget(package_dir)

            # Verify pip command
            mockPopen.assert_called_once()
            args = mockPopen.call_args[1]['args']
            self.assertEqual(args[0], sys.executable)
            self.assertEqual(args[1:4], ['-m', 'pip', 'install'])

    def test_subtle_jab(self):
        """Test if the code maintains appropriate levels of passive-aggressiveness."""
        with patch('Z0Z_tools.pipAnything.everyone_knows_what___main___is') as mock_main:
            pipAnything.readability_counts()
            mock_main.assert_called_once()
            # If you need this comment to understand what readability_counts() does,
            # then readability_counts() has failed its mission in life

    def test_CLI_functions(self):
        """Test the CLI-related functions."""
        test_cases = [
            # Missing argument
            {
                'argv': ['script.py'],
                'expected_exit': True
            },
            # Invalid directory
            {
                'argv': ['script.py', '/nonexistent/path'],
                'expected_exit': True
            }
        ]

        for case in test_cases:
            with patch('sys.argv', case['argv']), \
                 patch('sys.exit') as mock_exit, \
                 patch('builtins.print') as mock_print:
                
                pipAnything.everyone_knows_what___main___is()
                
                if case['expected_exit']:
                    mock_exit.assert_called_once_with(1)
                    mock_print.assert_called()

    def test_snark_level(self):
        """Ensures the code's snark remains at professionally acceptable levels."""
        originalArgv = sys.argv
        sys.argv = ['script.py']  # Trigger the usage message
        
        with patch('sys.exit') as mock_exit, \
             patch('builtins.print') as mock_print:
            pipAnything.main()
            
            # Verify that the snark was delivered with surgical precision
            mock_print.assert_called()
            mock_exit.assert_called_once_with(1)
            
            # Test if the -m explanation maintains perfect levels of obviousness
            printed_messages = ' '.join(str(call.args[0]) for call in mock_print.call_args_list)
            self.assertNotIn('obviously', printed_messages.lower())
        
        sys.argv = originalArgv  # Restore original argv

    def test_invalid_requirements(self):
        """Test handling of invalid requirements file content."""
        with tempfile.TemporaryDirectory() as tempdir:
            requirements_file = Path(tempdir) / 'requirements.txt'
            invalid_content = """
            invalid==requirement==1.0
            # Comment
            valid-package==1.0
            spaces in package==1.0
            @#$%^invalid characters
            """
            requirements_file.write_text(invalid_content)

            requirements = pipAnything.makeListRequirementsFromRequirementsFile(requirements_file)
            self.assertEqual(len(requirements), 1)
            self.assertIn('valid-package==1.0', requirements)

    def test_multiple_requirements_files(self):
        """Test processing multiple requirements files."""
        with tempfile.TemporaryDirectory() as tempdir:
            # Create two requirements files
            req1 = Path(tempdir) / 'req1.txt'
            req2 = Path(tempdir) / 'req2.txt'
            
            req1.write_text('package-A==1.0\npackage-B==2.0')
            req2.write_text('package-B==2.0\npackage-C==3.0')

            # Test combining requirements
            requirements = pipAnything.makeListRequirementsFromRequirementsFile(req1, req2)
            self.assertEqual(len(requirements), 3)
            self.assertEqual(sorted(requirements), 
                           ['package-A==1.0', 'package-B==2.0', 'package-C==3.0'])

if __name__ == '__main__':
    unittest.main()
