"""SSOT for Pytest. Implementing new ways of structuring tests.
- Other test modules should not import directly from the package being tested: they should import from here.
- This module should import from the package being tested.
- All fixtures should be here.
- Temporary files and directories should be created and cleaned up here.
- Prefer to make predictable data and use the test data in the tests/dataSamples directory over generating random data or artificial data."""

from numpy.typing import NDArray
import numpy
import pytest
import scipy.signal.windows as SciPy
import torch
from tests.conftest import *
from typing import Callable, Any, Union
from pathlib import Path
from typing import Generator, Set, Any, Type, Union, Sequence, Callable
import pytest
import shutil
import uuid
from unittest.mock import patch
from Z0Z_tools import halfsine, tukey, cosineWings, equalPower
from Z0Z_tools import halfsineTensor, tukeyTensor, cosineWingsTensor, equalPowerTensor  # type: ignore

all = [
    'halfsine',
    'tukey',
    'cosineWings',
    'equalPower',
    'halfsineTensor',
    'tukeyTensor',
    'cosineWingsTensor',
    'equalPowerTensor',
]

# SSOT for test data paths
pathDataSamples = Path("tests/dataSamples")
pathTempRoot = pathDataSamples / "tmp"

# The registrar maintains the register of temp files
registrarTempFiles: Set[Path] = set()

def addTempFileToRegister(path: Path) -> None:
    """The registrar adds a temp file to the register."""
    registrarTempFiles.add(path)

def cleanupTempFileRegister() -> None:
    """The registrar cleans up temp files in the register."""
    for pathTemp in sorted(registrarTempFiles, reverse=True):
        try:
            if pathTemp.is_file():
                pathTemp.unlink(missing_ok=True)
            elif pathTemp.is_dir():
                shutil.rmtree(pathTemp, ignore_errors=True)
        except Exception as ERRORmessage:
            print(f"Warning: Failed to clean up {pathTemp}: {ERRORmessage}")
    registrarTempFiles.clear()

@pytest.fixture(scope="session", autouse=True)
def setupTeardownTestData() -> Generator[None, None, None]:
    """Auto-fixture to setup test data directories and cleanup after."""
    pathDataSamples.mkdir(exist_ok=True)
    pathTempRoot.mkdir(exist_ok=True)
    yield
    cleanupTempFileRegister()

@pytest.fixture
def pathTempTesting(request: pytest.FixtureRequest) -> Path:
    """Create a unique temp directory for each test function."""
    # Sanitize test name for filesystem compatibility
    sanitizedName = request.node.name.replace('[', '_').replace(']', '_').replace('/', '_')
    uniqueDirectory = f"{sanitizedName}_{uuid.uuid4()}"
    pathTemp = pathTempRoot / uniqueDirectory
    pathTemp.mkdir(parents=True)

    addTempFileToRegister(pathTemp)
    return pathTemp

@pytest.fixture
def redirectPipAnything(monkeypatch: pytest.MonkeyPatch, pathTempTesting: Path) -> None:
    """Redirect pip package operations to test directories."""
    def mockTempdir(*args, **kwargs) -> str:
        pathTemp = pathTempTesting / f"pip_temp_{uuid.uuid4()}"
        pathTemp.mkdir(parents=True)
        addTempFileToRegister(pathTemp)
        return str(pathTemp)

    monkeypatch.setattr('tempfile.mkdtemp', mockTempdir)
    monkeypatch.setattr('tempfile.gettempdir', lambda: str(pathTempTesting))

"""
Section: Standardized test structures"""

def formatTestMessage(expected: Any, actual: Any, functionName: str, *arguments: Any, **keywordArguments: Any) -> str:
    """Format assertion message for any test comparison."""
    listArgumentComponents = [str(parameter) for parameter in arguments]
    listKeywordComponents = [f"{key}={value}" for key, value in keywordArguments.items()]
    joinedArguments = ', '.join(listArgumentComponents + listKeywordComponents)

    return (f"\nTesting: `{functionName}({joinedArguments})`\n"
            f"Expected: {expected}\n"
            f"Got: {actual}")

def standardComparison(expected: Any, functionTarget: Callable, *arguments: Any, **keywordArguments: Any) -> None:
    """Template for tests expecting an error."""
    if type(expected) == Type[Exception]:
        messageExpected = expected.__name__
    else:
        messageExpected = expected

    try:
        messageActual = actual = functionTarget(*arguments, **keywordArguments)
    except Exception as actualError:
        messageActual = type(actualError).__name__
        actual = type(actualError)

    assert actual == expected, formatTestMessage(messageExpected, messageActual, functionTarget.__name__, *arguments, **keywordArguments)

def expectSystemExit(expected: Union[str, int, Sequence[int]], functionTarget: Callable, *arguments: Any) -> None:
    """Template for tests expecting SystemExit.

    Parameters
        expected: Exit code expectation:
            - "error": any non-zero exit code
            - "nonError": specifically zero exit code
            - int: exact exit code match
            - Sequence[int]: exit code must be one of these values
        functionTarget: The function to test
        arguments: Arguments to pass to the function
    """
    with pytest.raises(SystemExit) as exitInfo:
        functionTarget(*arguments)

    exitCode = exitInfo.value.code

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

"""Section: Array comparison test templates"""

def standardArrayComparison(arrayExpected: NDArray | torch.Tensor,
                          functionTarget: Callable,
                          *arguments: Any,
                          rtol: float = 1e-7,
                          atol: float = 0,
                          **keywordArguments: Any) -> None:
    """Template for tests comparing array outputs.

    Uses numpy.allclose or torch.allclose for comparison and provides readable error messages.
    """
    try:
        arrayActual = functionTarget(*arguments, **keywordArguments)
    except Exception as actualError:
        raise type(actualError)(formatTestMessage(
            arrayExpected, type(actualError).__name__,
            functionTarget.__name__, *arguments, **keywordArguments
        )) from actualError

    compareMethod = torch if isinstance(arrayActual, torch.Tensor) else numpy

    assert compareMethod.allclose(arrayActual, arrayExpected, rtol=rtol, atol=atol), \
        formatTestMessage(arrayExpected, arrayActual, functionTarget.__name__,
                         *arguments, **keywordArguments)

def verifyArrayProperties(arrayTarget: NDArray | torch.Tensor,
                         shapeExpected: tuple[int, ...] | None = None,
                         minValue: float | None = None,
                         maxValue: float | None = None,
                         symmetryAxis: int | None = None) -> None:
    """Template for verifying array properties with clear error messages."""
    compareMethod = torch if isinstance(arrayTarget, torch.Tensor) else numpy

    if shapeExpected is not None:
        assert arrayTarget.shape == shapeExpected, \
            f"Shape mismatch\nExpected: {shapeExpected}\nGot: {arrayTarget.shape}"

    if minValue is not None:
        assert compareMethod.all(arrayTarget >= minValue), \
            f"Values below minimum {minValue}\nGot: {arrayTarget.min()}"

    if maxValue is not None:
        assert compareMethod.all(arrayTarget <= maxValue), \
            f"Values above maximum {maxValue}\nGot: {arrayTarget.max()}"

    if symmetryAxis is not None:
        midpoint = arrayTarget.shape[symmetryAxis] // 2
        sliceForward = [slice(None)] * arrayTarget.ndim
        sliceForward[symmetryAxis] = slice(0, midpoint)
        firstHalf = arrayTarget[tuple(sliceForward)]

        # Use flip instead of negative step for better compatibility
        if isinstance(arrayTarget, torch.Tensor):
            secondHalf = torch.flip(arrayTarget, [symmetryAxis])[tuple(sliceForward)]
        else:
            secondHalf = numpy.flip(arrayTarget, axis=symmetryAxis)[tuple(sliceForward)]

        assert compareMethod.allclose(firstHalf, secondHalf), \
            formatTestMessage(firstHalf, secondHalf, "symmetry check",
                            f"axis={symmetryAxis}")

"""Section: Windowing function testing utilities"""

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
