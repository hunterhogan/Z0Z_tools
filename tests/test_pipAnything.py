import pytest
from pathlib import Path
from Z0Z_tools import pipAnything
import sys

TEST_DATA_DIR = Path('tests/dataSamples/tmp')

@pytest.fixture(autouse=True)
def setup_test_directory():
    """Ensure test directory exists and is clean before each test."""
    TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)
    yield

@pytest.fixture
def requirements_file():
    """Create a requirements file in the test directory."""
    req_file = TEST_DATA_DIR / 'requirements.txt'
    req_file.write_text("""
    # This is a comment
    package-A==1.2.3
    package-B>=4.5.6,<=7.8.9
    package_C
    # Another comment
    analyzeAudio@git+https://github.com/hunterhogan/analyzeAudio.git
    """)
    return req_file

@pytest.fixture
def package_dir():
    """Create a fake package directory with requirements."""
    pkg_dir = TEST_DATA_DIR / 'test_package'
    pkg_dir.mkdir(exist_ok=True)
    (pkg_dir / 'requirements.txt').write_text('numpy\npandas')
    return pkg_dir

def test_makeListRequirementsFromRequirementsFile(requirements_file):
    """Test requirements file parsing with various inputs."""
    requirements = pipAnything.makeListRequirementsFromRequirementsFile(requirements_file)
    assert len(requirements) == 4
    assert 'package-A==1.2.3' in requirements
    assert 'package-B>=4.5.6,<=7.8.9' in requirements
    assert 'package_C' in requirements
    assert 'analyzeAudio@git+https://github.com/hunterhogan/analyzeAudio.git' in requirements

def test_multiple_requirements_files():
    """Test processing multiple requirements files."""
    req1 = TEST_DATA_DIR / 'req1.txt'
    req2 = TEST_DATA_DIR / 'req2.txt'

    req1.write_text('package-A==1.0\npackage-B==2.0')
    req2.write_text('package-B==2.0\npackage-C==3.0')

    requirements = pipAnything.makeListRequirementsFromRequirementsFile(req1, req2)
    assert len(requirements) == 3
    assert sorted(requirements) == ['package-A==1.0', 'package-B==2.0', 'package-C==3.0']

def test_nonexistent_requirements_file():
    """Test handling of non-existent requirements file."""
    nonexistent = TEST_DATA_DIR / 'nonexistent.txt'
    requirements = pipAnything.makeListRequirementsFromRequirementsFile(nonexistent)
    assert len(requirements) == 0

@pytest.mark.parametrize("content,expected_count", [
    ("invalid==requirement==1.0\nvalid-package==1.0", 1),
    ("spaces in package==1.0\n@#$%^invalid\nvalid-pkg==1.0", 1),
    ("valid-1==1.0\nvalid-2==2.0", 2),
])
def test_invalid_requirements(content, expected_count):
    """Test handling of invalid requirements content."""
    req_file = TEST_DATA_DIR / 'requirements.txt'
    req_file.write_text(content)
    requirements = pipAnything.makeListRequirementsFromRequirementsFile(req_file)
    assert len(requirements) == expected_count

def test_make_setupDOTpy():
    """Test setup.py content generation."""
    relative_path = 'my_package'
    requirements = ['numpy', 'pandas']
    setup_content = pipAnything.make_setupDOTpy(relative_path, requirements)

    assert f"name='{Path(relative_path).name}'" in setup_content
    assert f"packages=find_packages(where=r'{relative_path}')" in setup_content
    assert f"package_dir={{'': r'{relative_path}'}}" in setup_content
    assert f"install_requires={requirements}," in setup_content
    assert "include_package_data=True" in setup_content

def test_installPackageTarget(mocker, package_dir):
    """Test package installation process."""
    mock_popen = mocker.patch('subprocess.Popen')
    mock_process = mocker.MagicMock()
    mock_process.stdout = ['Installing...', 'Done!']
    mock_process.wait.return_value = 0
    mock_popen.return_value = mock_process

    pipAnything.installPackageTarget(package_dir)

    mock_popen.assert_called_once()
    args = mock_popen.call_args[1]['args']
    assert args[0] == sys.executable
    assert args[1:4] == ['-m', 'pip', 'install']

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

def test_snark_level(mocker):
    """Test appropriate levels of snark in messages."""
    mocker.patch('sys.argv', ['script.py'])
    mock_exit = mocker.patch('sys.exit')
    mock_print = mocker.patch('builtins.print')

    pipAnything.main()

    mock_print.assert_called()
    mock_exit.assert_called_once_with(1)

    printed_messages = ' '.join(str(call.args[0])
                              for call in mock_print.call_args_list)
    assert 'obviously' not in printed_messages.lower()