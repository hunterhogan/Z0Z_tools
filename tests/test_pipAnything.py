from typing import Generator
import pytest
from typing import Any
import pathlib
from Z0Z_tools import pipAnything
import sys
import subprocess

def test_makeListRequirementsFromRequirementsFile(pathTempTesting):
    """Test requirements file parsing with various inputs."""
    pathRequirementsFile = pathTempTesting / "requirements.txt"
    pathRequirementsFile.write_text(
        """
        # This is a comment
        package-A==1.2.3
        package-B>=4.5.6,<=7.8.9
        package_C
        analyzeAudio@git+https://github.com/hunterhogan/analyzeAudio.git
        """
    )
    requirements = pipAnything.makeListRequirementsFromRequirementsFile(pathRequirementsFile)
    # Updated assertion to match actual valid requirements
    assert len(requirements) == 4
    assert 'package-A==1.2.3' in requirements
    assert 'package-B>=4.5.6,<=7.8.9' in requirements
    assert 'package_C' in requirements
    assert 'analyzeAudio@git+https://github.com/hunterhogan/analyzeAudio.git' in requirements

@pytest.mark.parametrize("content,expected_requirements", [
    (
        "invalid==requirement==1.0\nvalid-package==1.0",
        ['valid-package==1.0']
    ),
    (
        "spaces in package==1.0\n@#$%^invalid\nvalid-pkg==1.0",
        ['valid-pkg==1.0']
    ),
    (
        "valid-1==1.0\nvalid-2==2.0",
        ['valid-1==1.0', 'valid-2==2.0']
    ),
])
def test_invalid_requirements(content, expected_requirements, pathTempTesting):
    """Test handling of invalid requirements content."""
    pathFilenameRequirements = pathTempTesting / 'requirements.txt'
    pathFilenameRequirements.write_text(content)
    requirements = pipAnything.makeListRequirementsFromRequirementsFile(pathFilenameRequirements)
    assert set(requirements) == set(expected_requirements)

def test_nonexistent_requirements_file(pathTempTesting):
    """Test handling of non-existent requirements file."""
    pathFilenameNonexistent = pathTempTesting / 'nonexistent.txt'
    requirements = pipAnything.makeListRequirementsFromRequirementsFile(pathFilenameNonexistent)
    assert len(requirements) == 0

def test_multiple_requirements_files(pathTempTesting):
    """Test processing multiple requirements files."""
    pathFilenameRequirements1 = pathTempTesting / 'pathFilenameRequirements1.txt'
    pathFilenameRequirements2 = pathTempTesting / 'pathFilenameRequirements2.txt'
    pathFilenameRequirements1.write_text('package-A==1.0\npackage-B==2.0')
    pathFilenameRequirements2.write_text('package-B==2.0\npackage-C==3.0')
    requirements = pipAnything.makeListRequirementsFromRequirementsFile(pathFilenameRequirements1, pathFilenameRequirements2)
    assert len(requirements) == 3
    assert sorted(requirements) == ['package-A==1.0', 'package-B==2.0', 'package-C==3.0']

def test_make_setupDOTpy():
    """Test setup.py content generation."""
    relative_path = 'my_package'
    requirements = ['numpy', 'pandas']
    setup_content = pipAnything.make_setupDOTpy(relative_path, requirements)

    assert f"name='{pathlib.Path(relative_path).name}'" in setup_content
    assert f"packages=find_packages(where=r'{relative_path}')" in setup_content
    assert f"package_dir={{'': r'{relative_path}'}}" in setup_content
    assert f"install_requires={requirements}," in setup_content
    assert "include_package_data=True" in setup_content

@pytest.mark.usefixtures("redirectPipAnything")
def test_installPackageTarget(mocker, pathTempTesting: pathlib.Path):
    """Test installPackageTarget with mock instead of a real pip install."""
    pathPackageDir = pathTempTesting / 'test_package'
    pathPackageDir.mkdir()
    pathRequirements = pathPackageDir / 'requirements.txt'
    pathRequirements.write_text('numpy\npandas')

    (pathPackageDir / '__init__.py').write_text('# ...existing code...')
    (pathPackageDir / 'dummy_module.py').write_text('print("Hello from dummy_module")')

    # Mock the subprocess.Popen call
    mock_process = mocker.MagicMock()
    mock_process.stdout = ["Pretending to install...\n"]
    mock_process.wait.return_value = 0
    mock_popen = mocker.patch.object(subprocess, "Popen", return_value=mock_process)

    pipAnything.installPackageTarget(pathPackageDir)

    # Assert we didn't really install anything; just called pip
    mock_popen.assert_called_once()
    callArgs = mock_popen.call_args[1]["args"]
    assert callArgs[0] == sys.executable
    assert callArgs[1:4] == ["-m", "pip", "install"]

@pytest.mark.parametrize("argv,should_exit", [
    (['script.py'], True),
    (['script.py', '/nonexistent/path'], True),
])
def test_CLI_functions(mocker, argv, should_exit):
    """Test CLI argument handling."""
    mocker.patch('sys.argv', argv)
    mock_exit = mocker.patch('sys.exit')
    mock_print = mocker.patch('builtins.print')

    pipAnything.everyone_knows_what___main___is()

    if should_exit:
        mock_exit.assert_called_once_with(1)
        mock_print.assert_called()
