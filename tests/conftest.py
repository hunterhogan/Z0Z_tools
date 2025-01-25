"""SSOT for Pytest. Implementing new ways of structuring tests.
- Other test modules should not import directly from the package being tested: they should import from here.
- This module should import from the package being tested.
- All fixtures should be here.
- Temporary files and directories should be created and cleaned up here.
- Prefer to make predictable data and use the test data in the tests/dataSamples directory over generating random data or artificial data."""

from numpy.typing import ArrayLike, NDArray
from typing import Generator, Set, Any, Type, Union, Sequence, Callable
from unittest.mock import patch
from Z0Z_tools import *
from Z0Z_tools.pytestForYourUse import *
import numpy
import pandas
import pathlib
import pytest
import scipy.signal.windows as SciPy
import shutil
import torch
import uuid

# SSOT for test data paths and filenames
pathDataSamples = pathlib.Path("tests/dataSamples")
# NOTE `tmp` is not a diminutive form of temporary: it signals a technical term
pathTmpRoot = pathDataSamples / "tmp"

registerOfTemporaryFilesystemObjects: Set[pathlib.Path] = set()

def registrarRecordsTmpObject(path: pathlib.Path) -> None:
    """The registrar adds a temp file to the register."""
    registerOfTemporaryFilesystemObjects.add(path)

def registrarDeletesTmpObjects() -> None:
    """The registrar cleans up temp files in the register."""
    for pathTemp in sorted(registerOfTemporaryFilesystemObjects, reverse=True):
        try:
            if pathTemp.is_file():
                pathTemp.unlink(missing_ok=True)
            elif pathTemp.is_dir():
                shutil.rmtree(pathTemp, ignore_errors=True)
        except Exception as ERRORmessage:
            print(f"Warning: Failed to clean up {pathTemp}: {ERRORmessage}")
    registerOfTemporaryFilesystemObjects.clear()

@pytest.fixture(scope="session", autouse=True)
def setupTeardownTmpObjects() -> Generator[None, None, None]:
    """Auto-fixture to setup test data directories and cleanup after."""
    pathDataSamples.mkdir(exist_ok=True)
    pathTmpRoot.mkdir(exist_ok=True)
    yield
    registrarDeletesTmpObjects()

@pytest.fixture
def pathTmpTesting(request: pytest.FixtureRequest) -> pathlib.Path:
    pathTmp = pathTmpRoot / str(uuid.uuid4().hex)
    pathTmp.mkdir(parents=True, exist_ok=False)

    registrarRecordsTmpObject(pathTmp)
    return pathTmp

@pytest.fixture
def pathFilenameTmpTesting(request: pytest.FixtureRequest) -> pathlib.Path:
    try:
        extension = request.param
    except AttributeError:
        extension = ".txt"

    uuidHex = uuid.uuid4().hex
    subpath = uuidHex[0:-8]
    filenameStem = uuidHex[-8:None]

    pathFilenameTmp = pathlib.Path(pathTmpRoot, subpath, filenameStem + extension)
    pathFilenameTmp.parent.mkdir(parents=True, exist_ok=False)

    registrarRecordsTmpObject(pathFilenameTmp)
    return pathFilenameTmp

@pytest.fixture
def mockTemporaryFiles(monkeypatch: pytest.MonkeyPatch, pathTmpTesting: pathlib.Path) -> None:
    """Mock all temporary filesystem operations to use pathTmpTesting."""
    monkeypatch.setattr('tempfile.mkdtemp', lambda *a, **k: str(pathTmpTesting))
    monkeypatch.setattr('tempfile.gettempdir', lambda: str(pathTmpTesting))
    monkeypatch.setattr('tempfile.mkstemp', lambda *a, **k: (0, str(pathTmpTesting)))

# Fixtures
@pytest.fixture
def setupDirectoryStructure(pathTmpTesting):
    """Create a complex directory structure for testing findRelativePath."""
    baseDirectory = pathTmpTesting / "base"
    baseDirectory.mkdir()

    # Create nested directories
    for subdir in ["dir1/subdir1", "dir2/subdir2", "dir3/subdir3"]:
        (baseDirectory / subdir).mkdir(parents=True)

    # Create some files
    (baseDirectory / "dir1/file1.txt").touch()
    (baseDirectory / "dir2/file2.txt").touch()

    return baseDirectory

@pytest.fixture
def pathFilenameWAV(pathTmpTesting):
    """Fixture providing a temporary WAV file path."""
    return pathTmpTesting / "test_output.wav"

@pytest.fixture
def dataframeSample():
    return pandas.DataFrame({
        'columnA': [1, 2, 3],
        'columnB': ['a', 'b', 'c']
    })

"""
Section: Windowing function testing utilities"""

@pytest.fixture(params=[256, 1024, 1024 * 8, 44100, 44100 * 11])
def lengthWindow(request):
    return request.param

@pytest.fixture(params=[0.0, 0.1, 0.5, 1.0])
def ratioTaper(request):
    return request.param

@pytest.fixture(params=['cpu'] + (['cuda'] if torch.cuda.is_available() else []))
def device(request):
    return request.param

@pytest.fixture
def windowingFunctionsPair():
    return [
        (cosineWings, cosineWingsTensor),
        (equalPower, equalPowerTensor),
        (halfsine, halfsineTensor),
        (tukey, tukeyTensor)
    ]

"""
Section: Standardized assert statements and failure messages"""

def uniformTestFailureMessage(expected: Any, actual: Any, functionName: str, *arguments: Any, **keywordArguments: Any) -> str:
    """Format assertion message for any test comparison."""
    listArgumentComponents = [str(parameter) for parameter in arguments]
    listKeywordComponents = [f"{key}={value}" for key, value in keywordArguments.items()]
    joinedArguments = ', '.join(listArgumentComponents + listKeywordComponents)

    return (f"\nTesting: `{functionName}({joinedArguments})`\n"
            f"Expected: {expected}\n"
            f"Got: {actual}")

def standardizedSystemExit(expected: Union[str, int, Sequence[int]], functionTarget: Callable, *arguments: Any, **keywordArguments: Any) -> None:
    """Template for tests expecting any SystemExit event.

    Parameters
        expected: Exit code expectation:
            If testing for a semantic outcome, prefer one of the semantic values for `expected`:
                - "error": any non-zero exit code.
                - "nonError": specifically zero exit code.
            If the specific exit code is in fact meaningful, predictable, and necessary to differentiate between different outcomes, use:
                - int: exact exit code match.
                - Sequence[int]: exit code must be one of these values.
        functionTarget: A callable that generates an outcome, which is often the target of the test.
        arguments: Arguments to pass to `functionTarget`.
        keywordArguments: Keyword arguments to pass to `functionTarget`.
    """
    with pytest.raises(SystemExit) as exitInfo:
        functionTarget(*arguments, **keywordArguments)

    exitCode = exitInfo.value.code

    # TODO converge with `uniformTestFailureMessage`
    if expected == "error":
        assert exitCode != 0, \
            f"Expected error exit (non-zero) but got code {exitCode}"
    elif expected == "nonError":
        assert exitCode == 0, \
            f"Expected non-error exit (0) but got code {exitCode}"
    elif isinstance(expected, (list, tuple)):
        assert exitCode in expected, \
            f"Expected exit code to be one of {expected} but got {exitCode}"
    else:
        assert exitCode == expected, \
            f"Expected exit code {expected} but got {exitCode}"

def standardizedEqualTo(expected: Any, functionTarget: Callable, *arguments: Any, **keywordArguments: Any) -> None:
    """Template for most tests to compare the actual outcome with the expected outcome, including expected errors."""
    if type(expected) == Type[Exception]:
        messageExpected = expected.__name__
    else:
        messageExpected = expected

    try:
        messageActual = actual = functionTarget(*arguments, **keywordArguments)
    except Exception as actualError:
        messageActual = type(actualError).__name__
        actual = type(actualError)

    assert actual == expected, uniformTestFailureMessage(messageExpected, messageActual, functionTarget.__name__, *arguments, **keywordArguments)
