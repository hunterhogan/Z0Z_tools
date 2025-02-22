from tests.conftest import *
from unittest.mock import AsyncMock, MagicMock, NonCallableMagicMock
import pathlib
import pytest
import pytest_mock
import subprocess
import sys

@pytest.mark.parametrize("description,content,expected", [
	("Basic requirements", "# This is a comment\n package-NE==1.13.0\n package-SW>=4.17.0,<=7.23.0\n package_NW\n analyzeAudio@git+https://github.com/hunterhogan/analyzeAudio.git ", [ 'analyzeAudio@git+https://github.com/hunterhogan/analyzeAudio.git', 'package-NE==1.13.0', 'package-SW>=4.17.0,<=7.23.0', 'package_NW' ] ),
	("Invalid requirements", "invalid==requirement==1.0\nvalid-package==1.13.0", ['valid-package==1.13.0'] ),
	("Multiple valid packages", "package-FR==11.0\npackage-JP==13.0", ['package-FR==11.0', 'package-JP==13.0'] ),
	("Empty file", "", []),
	("Comments only", "# Comment 1\n# Comment 2", []),
	("Whitespace only", "	\n\t\n", []),
	]
	, ids=lambda x: x if isinstance(x, str) else ""
)
def test_makeListRequirementsFromRequirementsFile(description: str, content: str, expected: list[str], pathTmpTesting: pathlib.Path) -> None:
	"""Test requirements file parsing with various inputs."""
	pathRequirementsFile: pathlib.Path = pathTmpTesting / "requirements.txt"
	pathRequirementsFile.write_text(content)
	standardizedEqualTo(expected, makeListRequirementsFromRequirementsFile, pathRequirementsFile)

@pytest.mark.parametrize("description,paths,expected", [
	("Multiple files with unique entries", [ ('requirements1.txt', 'package-NE==11.0\npackage-NW==13.0'), ('requirements2.txt', 'package-SW==17.0\npackage-SE==19.0') ], ['package-NE==11.0', 'package-NW==13.0', 'package-SE==19.0', 'package-SW==17.0'] ),
	("Multiple files with duplicates", [ ('requirements1.txt', 'package-FR==11.0\npackage-common==13.0'), ('requirements2.txt', 'package-JP==17.0\npackage-common==13.0') ], ['package-FR==11.0', 'package-JP==17.0', 'package-common==13.0'] ),
])
def test_multiple_requirements_files(description: str, paths: list[tuple[str, str]], expected: list[str], pathTmpTesting: pathlib.Path) -> None:
	"""Test processing multiple requirements files."""
	ListPathFilenames: list[pathlib.Path] = []
	for filename, content in paths:
		pathFile = pathTmpTesting / filename
		pathFile.write_text(content)
		ListPathFilenames.append(pathFile)

	standardizedEqualTo(expected, makeListRequirementsFromRequirementsFile, *ListPathFilenames)

def test_nonexistent_requirements_file(pathTmpTesting: pathlib.Path) -> None:
	"""Test handling of non-existent requirements file."""
	pathFilenameNonexistent: pathlib.Path = pathTmpTesting / 'nonexistent.txt'
	standardizedEqualTo([], makeListRequirementsFromRequirementsFile, pathFilenameNonexistent)

@pytest.mark.parametrize("description,relativePathPackage,listRequirements,expected_contains", [
	("Basic setup", 'package-NE', ['numpy>=11.0', 'pandas>=13.0'], [ "name='package-NE'", "packages=find_packages(where=r'package-NE')", "package_dir={'': r'package-NE'}", "install_requires=['numpy>=11.0', 'pandas>=13.0']", "include_package_data=True" ] ),
	("Empty requirements", 'package-SW', [], [ "name='package-SW'", "install_requires=[]" ] ),
])
def test_make_setupDOTpy(description: str, relativePathPackage: str, listRequirements: list[str], expected_contains: list[str]):
	"""Test setup.py content generation."""
	setup_content: str = make_setupDOTpy(relativePathPackage, listRequirements)
	for expected in expected_contains:
		assert expected in setup_content

@pytest.mark.usefixtures("mockTemporaryFiles")
def test_installPackageTarget(mocker: pytest_mock.MockFixture, pathTmpTesting: pathlib.Path) -> None:
	"""Test package installation process."""
	# Setup test package structure
	pathPackageDir: pathlib.Path = pathTmpTesting / 'test-package-NE'
	pathPackageDir.mkdir()
	(pathPackageDir / 'requirements.txt').write_text('numpy>=11.0\npandas>=13.0')
	(pathPackageDir / '__init__.py').write_text('')
	(pathPackageDir / 'module_prime.py').write_text('print("Prime module")')

	# Mock subprocess.Popen
	mock_process: MagicMock = mocker.MagicMock()
	mock_process.stdout = ["Installing test-package-NE...\n"]
	mock_process.wait.return_value = 0
	mocker.patch('subprocess.Popen', return_value=mock_process)

	installPackageTarget(pathPackageDir)

	# Verify Popen was called correctly
	subprocess.Popen.assert_called_once() # type: ignore
	call_args = subprocess.Popen.call_args[1]['args'] # type: ignore
	assert call_args[0] == sys.executable
	assert call_args[1:4] == ['-m', 'pip', 'install']

def test_main_function_chain(mocker: pytest_mock.MockFixture) -> None:
	"""Test the main function call chain."""
	mock_readability: MagicMock | AsyncMock | NonCallableMagicMock = mocker.patch('Z0Z_tools.pipAnything.readability_counts')
	main()
	mock_readability.assert_called_once()
