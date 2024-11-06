from pathlib import Path
from unittest.mock import patch
from Z0Z_tools import pipAnything
import tempfile
import unittest

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

if __name__ == '__main__':
    unittest.main()
