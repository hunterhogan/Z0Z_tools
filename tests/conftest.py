from collections.abc import Callable, Generator
from numpy.typing import NDArray
from typing import Any, Final
from Z0Z_tools import *
from Z0Z_tools.pytestForYourUse import *
import numpy
import pandas
import pathlib
import pytest
import shutil
import soundfile
import torch
import uuid

atolDEFAULT: Final[float] = 1e-7
rtolDEFAULT: Final[float] = 1e-7

# SSOT for test data paths and filenames
pathDataSamples = pathlib.Path("tests/dataSamples")
pathTmpRoot: pathlib.Path = pathDataSamples / "tmp"

registerOfTemporaryFilesystemObjects: set[pathlib.Path] = set()

def registrarRecordsTmpObject(path: pathlib.Path) -> None:
	"""The registrar adds a tmp file to the register."""
	registerOfTemporaryFilesystemObjects.add(path)

def registrarDeletesTmpObjects() -> None:
	"""The registrar cleans up tmp files in the register."""
	for pathTmp in sorted(registerOfTemporaryFilesystemObjects, reverse=True):
		try:
			if pathTmp.is_file():
				pathTmp.unlink(missing_ok=True)
			elif pathTmp.is_dir():
				shutil.rmtree(pathTmp, ignore_errors=True)
		except Exception as ERRORmessage:
			print(f"Warning: Failed to clean up {pathTmp}: {ERRORmessage}")
	registerOfTemporaryFilesystemObjects.clear()

@pytest.fixture(scope="session", autouse=True)
def setupTeardownTmpObjects() -> Generator[None]:
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
		extension: str = request.param
	except AttributeError:
		extension = ".txt"

	uuidHex: str = uuid.uuid4().hex
	subpath: str = uuidHex[0:-8]
	filenameStem: str = uuidHex[-8:None]

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
def setupDirectoryStructure(pathTmpTesting: pathlib.Path) -> pathlib.Path:
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

# Fixtures

@pytest.fixture
def dataframeSample() -> pandas.DataFrame:
	return pandas.DataFrame({
		'columnA': [1, 2, 3],
		'columnB': ['a', 'b', 'c']
	})

"""
Section: Windowing function testing utilities"""

@pytest.fixture(params=[256, 1024, 1024 * 8, 44100, 44100 * 11])
def lengthWindow(request: pytest.FixtureRequest) -> int:
	return request.param

@pytest.fixture(params=[0.0, 0.1, 0.5, 1.0])
def ratioTaper(request: pytest.FixtureRequest) -> float:
	return request.param

@pytest.fixture(params=['cpu'] + (['cuda'] if torch.cuda.is_available() else []))
def device(request: pytest.FixtureRequest) -> str:
	return request.param

"""
Section: Standardized assert statements and failure messages"""

def uniformTestFailureMessage(expected: Any, actual: Any, functionName: str, *arguments: Any, **keywordArguments: Any) -> str:
	"""Format assertion message for any test comparison."""
	listArgumentComponents: list[str] = [str(parameter) for parameter in arguments]
	listKeywordComponents: list[str] = [f"{key}={value}" for key, value in keywordArguments.items()]
	joinedArguments: str = ', '.join(listArgumentComponents + listKeywordComponents)

	return (f"\nTesting: `{functionName}({joinedArguments})`\n"
			f"Expected: {expected}\n"
			f"Got: {actual}")

def standardizedEqualTo(expected: Any, functionTarget: Callable[..., Any], *arguments: Any, **keywordArguments: Any) -> None:
	"""Template for most tests to compare the actual outcome with the expected outcome, including expected errors."""
	if type(expected) == type[Exception]:
		messageExpected: str = expected.__name__
	else:
		messageExpected = expected

	try:
		messageActual = actual = functionTarget(*arguments, **keywordArguments)
	except Exception as actualError:
		messageActual: str = type(actualError).__name__
		actual = type(actualError)

	assert actual == expected, uniformTestFailureMessage(messageExpected, messageActual, functionTarget.__name__, *arguments, **keywordArguments)

def prototype_numpyAllClose(expected: NDArray[Any], atol: float | None, rtol: float | None, functionTarget: Callable[..., Any], *arguments: Any, **keywordArguments: Any) -> None:
	"""Template for tests using numpy.allclose comparison."""
	if atol is None:
		atol = atolDEFAULT
	if rtol is None:
		rtol = rtolDEFAULT
	try:
		actual = functionTarget(*arguments, **keywordArguments)
	except Exception as actualError:
		messageActual: str = type(actualError).__name__
		actual = type(actualError)
		messageExpected = expected if isinstance(expected, type) else "array-like result"
		assert actual == expected, uniformTestFailureMessage(messageExpected, messageActual, functionTarget.__name__, *arguments, **keywordArguments)
	else:
		assert numpy.allclose(actual, expected, rtol, atol), uniformTestFailureMessage(expected, actual, functionTarget.__name__, *arguments, **keywordArguments)

def prototype_numpyArrayEqual(expected: NDArray[Any], functionTarget: Callable[..., Any], *arguments: Any, **keywordArguments: Any) -> None:
	"""Template for tests using numpy.array_equal comparison."""
	try:
		actual = functionTarget(*arguments, **keywordArguments)
	except Exception as actualError:
		messageActual: str = type(actualError).__name__
		actual = type(actualError)
		messageExpected = expected if isinstance(expected, type) else "array-like result"
		assert actual == expected, uniformTestFailureMessage(messageExpected, messageActual, functionTarget.__name__, *arguments, **keywordArguments)
	else:
		assert numpy.array_equal(actual, expected), uniformTestFailureMessage(expected, actual, functionTarget.__name__, *arguments, **keywordArguments)

"""
Section: This garbage needs to be replaced."""

dumbassDictionaryPathFilenamesAudioFiles: dict[str, pathlib.Path | list[pathlib.Path]] = {
	'mono': pathDataSamples / "testWooWooMono16kHz32integerClipping9sec.wav",
	'stereo': pathDataSamples / "testSine2ch5sec.wav",
	'video': pathDataSamples / "testVideo11sec.mkv",
	'mono_copies': [pathDataSamples / f"testWooWooMono16kHz32integerClipping9secCopy{i}.wav" for i in range(1, 4)],
	'stereo_copies': [pathDataSamples / f"testSine2ch5secCopy{i}.wav" for i in range(1, 5)]
}
@pytest.fixture
def waveform_data() -> dict[str, dict[str, Any]]:
	"""Fixture providing sample waveform data and sample rates."""
	mono_data, mono_sr = soundfile.read(dumbassDictionaryPathFilenamesAudioFiles['mono'], dtype='float32')
	stereo_data, stereo_sr = soundfile.read(dumbassDictionaryPathFilenamesAudioFiles['stereo'], dtype='float32')
	return {
		'mono': {
			'waveform': mono_data.astype(numpy.float32),
			'sample_rate': mono_sr
		},
		'stereo': {
			'waveform': stereo_data.astype(numpy.float32),
			'sample_rate': stereo_sr
		}
	}
