from collections.abc import Callable, Generator
from numpy import dtype, float32, ndarray
from numpy.typing import NDArray
from pathlib import Path
from typing import Any, ClassVar, Final
from Z0Z_tools import ArrayWaveforms, loadWaveforms, readAudioFile, Waveform
import numpy
import pathlib
import pytest
import shutil
import soundfile
import torch
import uuid

atolDEFAULT: Final[float] = 1e-7
rtolDEFAULT: Final[float] = 1e-7
amplitudeNorm: Final[float] = 1.0

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
		except Exception as ERRORmessage:  # noqa: PERF203
			print(f"Warning: Failed to clean up {pathTmp}: {ERRORmessage}")  # noqa: T201
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
	monkeypatch.setattr('tempfile.mkdtemp', lambda *a, **k: str(pathTmpTesting))  # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]
	monkeypatch.setattr('tempfile.gettempdir', lambda: str(pathTmpTesting))
	monkeypatch.setattr('tempfile.mkstemp', lambda *a, **k: (0, str(pathTmpTesting))) # pyright: ignore[reportUnknownLambdaType, reportUnknownArgumentType]

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
def tableSample() -> tuple[list[list[int | str]], list[str]]:
	tableColumns: list[str] = ['columnA', 'columnB']
	tableRows: list[list[int | str]] = [
		[5, 'N'],
		[8, 'E'],
		[13, 'S']
	]
	return tableRows, tableColumns

"""Section: Windowing function testing utilities"""

@pytest.fixture(params=[256, 1024, 1024 * 8, 44100, 44100 * 11])
def lengthWindow(request: pytest.FixtureRequest) -> int:
	return request.param

@pytest.fixture(params=[0.0, 0.1, 0.5, 1.0])
def ratioTaper(request: pytest.FixtureRequest) -> float:
	return request.param

@pytest.fixture(params=['cpu'] + (['cuda'] if torch.cuda.is_available() else []))
def device(request: pytest.FixtureRequest) -> str:
	return request.param

toleranceUniversal: Final[float] = 0.1
LUFSnormalizeTarget: Final[float] = -16.0
atolUniversal = 1e-5
rtolUniversal = 1e-5

pathDataSamples = Path("tests/dataSamples/labeled")

listFilenamesSameShape = [
    "WAV_44100_ch2_sec5_Sine_Copy0.wav",
    "WAV_44100_ch2_sec5_Sine_Copy1.wav",
    "WAV_44100_ch2_sec5_Sine_Copy2.wav",
    "WAV_44100_ch2_sec5_Sine_Copy3.wav",
]

@pytest.fixture
def listPathFilenamesArrayWaveforms() -> list[Path]:
	return [pathDataSamples / filename for filename in listFilenamesSameShape]

@pytest.fixture
def array44100_ch2_sec5_Sine(listPathFilenamesArrayWaveforms: list[Path]) -> ArrayWaveforms:
    """
    Load the four WAV files with the same shape into an array.

    Returns:
        arrayWaveforms: Array of waveforms with shape (channels, samples, count_of_waveforms)
    """
    return loadWaveforms(listPathFilenamesArrayWaveforms)

class WaveformAndMetadata:
	_cacheWaveforms: ClassVar[dict[Path, Waveform]] = {}
	def __init__(self, pathFilename: Path, LUFS: float, sampleRate: float, channelsTotal: int, ID: str) -> None:
		self.pathFilename: Path = pathFilename
		self.LUFS: float = LUFS
		self.sampleRate: float = sampleRate
		self.channelsTotal: int = channelsTotal
		self.ID: str = ID

	@property
	def waveform(self) -> Waveform:
		if self.pathFilename not in self._cacheWaveforms:
			if self.channelsTotal == 2:
				ImaWaveform: Waveform = readAudioFile(self.pathFilename, self.sampleRate)
			else:
				try:
					with soundfile.SoundFile(self.pathFilename) as readSoundFile:
						ImaSoundFile: ndarray[tuple[int, int], dtype[float32]] = readSoundFile.read(dtype='float32', always_2d=True).astype(float32)
				except soundfile.LibsndfileError as ERRORmessage:
					if 'System error' in str(ERRORmessage):
						message = f"File not found: {self.pathFilename}"
						raise FileNotFoundError(message) from ERRORmessage
					else:  # noqa: RET506
						raise
				ImaWaveform = ImaSoundFile.T
			self._cacheWaveforms[self.pathFilename] = ImaWaveform
		return self._cacheWaveforms[self.pathFilename]

def ingestSampleData() -> list[WaveformAndMetadata]:
	"""Parse LUFS*.wav filenames and create WaveformData objects without loading waveforms."""
	listWaveformData: list[WaveformAndMetadata] = []
	for pathFilename in pathDataSamples.glob("LUFS*.wav"):
		LUFSAsStr, sampleRateAsStr, channelsTotalAsStr, ID = pathFilename.stem.split("_", maxsplit=3)
		LUFS = -float(LUFSAsStr[len('LUFS'):])
		sampleRate = float(sampleRateAsStr)
		channelsTotal = int(channelsTotalAsStr[len('ch'):])
		listWaveformData.append(WaveformAndMetadata(pathFilename=pathFilename, LUFS=LUFS, sampleRate=sampleRate, channelsTotal=channelsTotal, ID=ID))
	return listWaveformData

def sampleData() -> list[WaveformAndMetadata]:
	return ingestSampleData()

def sampleData44100() -> list[WaveformAndMetadata]:
	return [dataSample for dataSample in ingestSampleData() if dataSample.sampleRate == 44100]

def sampleData48000() -> list[WaveformAndMetadata]:
	return [dataSample for dataSample in ingestSampleData() if dataSample.sampleRate == 48000]

"""Section: Standardized assert statements and failure messages"""

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
	if type(expected) == type[Exception]:  # noqa: E721
		messageExpected: str = expected.__name__
	else:
		messageExpected = expected

	try:
		messageActual = actual = functionTarget(*arguments, **keywordArguments)
	except Exception as actualError:
		messageActual: str = type(actualError).__name__
		actual = type(actualError)

	assert actual == expected, uniformTestFailureMessage(messageExpected, messageActual, functionTarget.__name__, *arguments, **keywordArguments)

def prototype_numpyAllClose(expected: NDArray[Any] | type[Exception], atol: float | None, rtol: float | None, functionTarget: Callable[..., Any], *arguments: Any, **keywordArguments: Any) -> None:
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
		if isinstance(expected, type):
			message = f"Expected an exception of type {expected.__name__}, but got a result"
			raise AssertionError(message)
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

"""Section: Audio file fixtures for testing readAudioFile, writeWAV, and related functions"""

pathDataSamplesRoot = pathlib.Path("tests/dataSamples")

@pytest.fixture
def waveformMono16kHz() -> WaveformAndMetadata:
	"""Fixture providing mono 16kHz waveform for readAudioFile testing."""
	pathFilename = pathDataSamplesRoot / "testWooWooMono16kHz32integerClipping9sec.wav"
	return WaveformAndMetadata(pathFilename=pathFilename, LUFS=-23.0, sampleRate=16000.0, channelsTotal=1, ID="mono16kHz")

@pytest.fixture
def waveformStereo44kHz() -> WaveformAndMetadata:
	"""Fixture providing stereo 44.1kHz waveform for readAudioFile testing."""
	pathFilename = pathDataSamplesRoot / "testSine2ch5sec.wav"
	return WaveformAndMetadata(pathFilename=pathFilename, LUFS=-23.0, sampleRate=44100.0, channelsTotal=2, ID="stereo44kHz")

@pytest.fixture
def waveformMono96kHz() -> WaveformAndMetadata:
	"""Fixture providing mono 96kHz waveform for resampleWaveform testing."""
	pathFilename = pathDataSamplesRoot / "testParkMono96kHz32float12.1sec.wav"
	return WaveformAndMetadata(pathFilename=pathFilename, LUFS=-23.0, sampleRate=96000.0, channelsTotal=1, ID="mono96kHz")

@pytest.fixture
def waveformStereo48kHz() -> WaveformAndMetadata:
	"""Fixture providing stereo 48kHz waveform for testing."""
	pathFilename = pathDataSamplesRoot / "testTrain2ch48kHz6.3sec.wav"
	return WaveformAndMetadata(pathFilename=pathFilename, LUFS=-23.0, sampleRate=48000.0, channelsTotal=2, ID="stereo48kHz")

@pytest.fixture
def listWaveformsSameStereoShape() -> list[WaveformAndMetadata]:
	"""Fixture providing multiple stereo waveforms with same shape for loadWaveforms testing."""
	basePath = pathDataSamplesRoot
	listWaveforms: list[WaveformAndMetadata] = []
	for indexCopy in [1, 2, 3, 4]:
		pathFilename = basePath / f"testSine2ch5secCopy{indexCopy}.wav"
		waveformData = WaveformAndMetadata(pathFilename=pathFilename, LUFS=-23.0, sampleRate=44100.0, channelsTotal=2, ID=f"stereoCopy{indexCopy}")
		listWaveforms.append(waveformData)
	return listWaveforms

@pytest.fixture
def listWaveformsSameMonoShape() -> list[WaveformAndMetadata]:
	"""Fixture providing multiple mono waveforms with same shape for loadWaveforms testing."""
	basePath = pathDataSamplesRoot
	listWaveforms: list[WaveformAndMetadata] = []
	for indexCopy in [1, 2, 3]:
		pathFilename = basePath / f"testWooWooMono16kHz32integerClipping9secCopy{indexCopy}.wav"
		waveformData = WaveformAndMetadata(pathFilename=pathFilename, LUFS=-23.0, sampleRate=16000.0, channelsTotal=1, ID=f"monoCopy{indexCopy}")
		listWaveforms.append(waveformData)
	return listWaveforms

@pytest.fixture
def pathFilenameVideoForErrorTesting() -> pathlib.Path:
	"""Fixture providing video file path for testing error conditions."""
	return pathDataSamplesRoot / "testVideo11sec.mkv"

@pytest.fixture
def pathFilenameNonexistentForErrorTesting() -> pathlib.Path:
	"""Fixture providing nonexistent file path for testing error conditions."""
	return pathDataSamplesRoot / "fileDoesNotExist.wav"

"""Section: Spectrogram testing fixtures and parameters"""

@pytest.fixture(params=[1024, 2048, 4096])
def lengthWindowingFunctionSTFT(request: pytest.FixtureRequest) -> int:
	"""Fixture providing different windowing function lengths for STFT testing."""
	return request.param

@pytest.fixture(params=[256, 512, 1024])
def lengthHopSTFT(request: pytest.FixtureRequest) -> int:
	"""Fixture providing different hop lengths for STFT testing."""
	return request.param

@pytest.fixture(params=[22050, 44100, 48000])
def sampleRateTarget(request: pytest.FixtureRequest) -> int:
	"""Fixture providing different target sample rates for spectrogram testing."""
	return request.param

@pytest.fixture
def waveformDataStereo44kHz() -> WaveformAndMetadata:
	"""Fixture providing stereo 44.1kHz waveform data for spectrogram testing."""
	pathFilename = pathDataSamplesRoot / "testSine2ch5sec.wav"
	return WaveformAndMetadata(pathFilename=pathFilename, LUFS=-23.0, sampleRate=44100.0, channelsTotal=2, ID="stereo44kHz")

@pytest.fixture
def waveformDataMono16kHz() -> WaveformAndMetadata:
	"""Fixture providing mono 16kHz waveform data for spectrogram testing."""
	pathFilename = pathDataSamplesRoot / "testWooWooMono16kHz32integerClipping9sec.wav"
	return WaveformAndMetadata(pathFilename=pathFilename, LUFS=-23.0, sampleRate=16000.0, channelsTotal=1, ID="mono16kHz")

@pytest.fixture
def listWaveformDataSameStereoShape() -> list[WaveformAndMetadata]:
	"""Fixture providing multiple stereo waveforms with same shape for spectrogram testing."""
	basePath = pathDataSamplesRoot
	return [
		WaveformAndMetadata(pathFilename=basePath / "testSine2ch5secCopy1.wav", LUFS=-23.0, sampleRate=44100.0, channelsTotal=2, ID="stereoCopy1"),
		WaveformAndMetadata(pathFilename=basePath / "testSine2ch5secCopy2.wav", LUFS=-23.0, sampleRate=44100.0, channelsTotal=2, ID="stereoCopy2"),
		WaveformAndMetadata(pathFilename=basePath / "testSine2ch5secCopy3.wav", LUFS=-23.0, sampleRate=44100.0, channelsTotal=2, ID="stereoCopy3"),
		WaveformAndMetadata(pathFilename=basePath / "testSine2ch5secCopy4.wav", LUFS=-23.0, sampleRate=44100.0, channelsTotal=2, ID="stereoCopy4"),
	]

@pytest.fixture
def listPathFilenamesFromWaveformData(listWaveformDataSameStereoShape: list[WaveformAndMetadata]) -> list[Path]:
	"""Convert WaveformAndMetadata objects to path list for loadSpectrograms testing."""
	return [waveformData.pathFilename for waveformData in listWaveformDataSameStereoShape]
