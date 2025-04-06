"""Source of coping."""
from numpy import dtype, float32, ndarray
from numpy.typing import NDArray
from pathlib import Path
from typing import Any, Final
from Z0Z_tools import loadWaveforms, readAudioFile, ArrayWaveforms, Waveform
import pytest
import soundfile

toleranceUniversal: Final[float] = 0.1
LUFSnormalizeTarget: Final[float] = -16.0
atolUniversal = 1e-5
rtolUniversal = 1e-5

pathDataSamples = Path("tests/dataSamples/labeled")

listFilenamesSameShape = [
    "WAV_44100_ch2_sec5_Sine_Copy0.wav",
    "WAV_44100_ch2_sec5_Sine_Copy1.wav",
    "WAV_44100_ch2_sec5_Sine_Copy2.wav",
    "WAV_44100_ch2_sec5_Sine_Copy3.wav",]

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
    arrayWaveforms = loadWaveforms(listPathFilenamesArrayWaveforms)
    return arrayWaveforms

class WaveformAndMetadata:
	_cacheWaveforms: dict[Path, NDArray[Any]] = {}
	def __init__(self, pathFilename: Path, LUFS: float, sampleRate: float, channelsTotal: int, ID: str):
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
						raise FileNotFoundError(f"File not found: {self.pathFilename}") from ERRORmessage
					else:
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
