"""test_waveform or test_spectrogram? if a spectrogram is involved at any point, then test_spectrogram."""
from pathlib import Path
from tests.conftest import prototype_numpyAllClose, standardizedEqualTo, uniformTestFailureMessage, WaveformAndMetadata
from typing import Any, Final
from Z0Z_tools import loadSpectrograms, readAudioFile, stft, waveformSpectrogramWaveform
import numpy
import pytest

expectedSpectrogramDimensions: Final[int] = 4

class TestLoadSpectrograms:
	"""Test suite for loadSpectrograms functionality."""

	@pytest.mark.parametrize("sampleRateTarget", [22050, 44100, 48000])
	def test_loadSpectrograms_acceptsSampleRateTarget(self, listPathFilenamesFromWaveformData: list[Path], sampleRateTarget: int) -> None:
		"""Test that loadSpectrograms accepts different target sample rates and produces valid spectrograms."""
		arraySpectrograms, dictionaryWaveformMetadata = loadSpectrograms(listPathFilenamesFromWaveformData, sampleRateTarget)

		expectedCountFiles = len(listPathFilenamesFromWaveformData)
		actualShape = arraySpectrograms.shape
		actualCountFiles = actualShape[-1]
		actualCountMetadata = len(dictionaryWaveformMetadata)

		assert actualCountFiles == expectedCountFiles, uniformTestFailureMessage(
			expectedCountFiles, actualCountFiles, "loadSpectrograms", listPathFilenamesFromWaveformData, sampleRateTarget
		)
		assert actualCountMetadata == expectedCountFiles, uniformTestFailureMessage(
			expectedCountFiles, actualCountMetadata, "loadSpectrograms metadata count", listPathFilenamesFromWaveformData, sampleRateTarget
		)
		assert len(actualShape) == expectedSpectrogramDimensions, uniformTestFailureMessage(
			expectedSpectrogramDimensions, len(actualShape), "loadSpectrograms shape dimensions", listPathFilenamesFromWaveformData, sampleRateTarget
		)
		assert numpy.issubdtype(arraySpectrograms.dtype, numpy.complexfloating), uniformTestFailureMessage(
			"complex floating point type", arraySpectrograms.dtype, "loadSpectrograms dtype", listPathFilenamesFromWaveformData, sampleRateTarget
		)

	@pytest.mark.parametrize("lengthWindowingFunctionSTFT,lengthHopSTFT", [
		(1024, 256),
		(2048, 512),
		(4096, 1024)
	])
	def test_loadSpectrograms_acceptsSTFTParameters(self, listPathFilenamesFromWaveformData: list[Path], lengthWindowingFunctionSTFT: int, lengthHopSTFT: int) -> None:
		"""Test that loadSpectrograms accepts custom STFT parameters and produces spectrograms with expected shapes."""
		sampleRateTarget = 44100

		arraySpectrograms, _dictionaryWaveformMetadata = loadSpectrograms(
			listPathFilenamesFromWaveformData,
			sampleRateTarget,
			lengthWindowingFunction=lengthWindowingFunctionSTFT,
			lengthHop=lengthHopSTFT
		)

		waveformSingle = readAudioFile(listPathFilenamesFromWaveformData[0], sampleRateTarget)
		spectrogramExpected = stft(
			waveformSingle,
			sampleRate=sampleRateTarget,
			lengthWindowingFunction=lengthWindowingFunctionSTFT,
			lengthHop=lengthHopSTFT
		)

		expectedShape = spectrogramExpected.shape
		actualShape = arraySpectrograms.shape[:-1]

		assert actualShape == expectedShape, uniformTestFailureMessage(
			expectedShape, actualShape, "loadSpectrograms STFT shape",
			listPathFilenamesFromWaveformData, sampleRateTarget,
			lengthWindowingFunction=lengthWindowingFunctionSTFT, lengthHop=lengthHopSTFT
		)

	def test_loadSpectrograms_singleFile(self, waveformDataStereo44kHz: WaveformAndMetadata) -> None:
		"""Test loading a spectrogram from a single file."""
		sampleRateTarget = 44100
		listPathFilenameSingle = [waveformDataStereo44kHz.pathFilename]

		arraySpectrograms, dictionaryWaveformMetadata = loadSpectrograms(listPathFilenameSingle, sampleRateTarget)

		waveformSingle = readAudioFile(waveformDataStereo44kHz.pathFilename, sampleRateTarget)
		spectrogramExpected = stft(waveformSingle, sampleRate=sampleRateTarget)

		expectedShape = spectrogramExpected.shape
		actualShape = arraySpectrograms.shape[:-1]
		expectedCountFiles = 1
		actualCountFiles = arraySpectrograms.shape[-1]
		expectedCountMetadata = 1
		actualCountMetadata = len(dictionaryWaveformMetadata)

		assert actualShape == expectedShape, uniformTestFailureMessage(
			expectedShape, actualShape, "loadSpectrograms single file shape", listPathFilenameSingle, sampleRateTarget
		)
		assert actualCountFiles == expectedCountFiles, uniformTestFailureMessage(
			expectedCountFiles, actualCountFiles, "loadSpectrograms single file count", listPathFilenameSingle, sampleRateTarget
		)
		assert actualCountMetadata == expectedCountMetadata, uniformTestFailureMessage(
			expectedCountMetadata, actualCountMetadata, "loadSpectrograms single file metadata count", listPathFilenameSingle, sampleRateTarget
		)

	def test_loadSpectrograms_preservesWaveformMetadata(self, listPathFilenamesFromWaveformData: list[Path]) -> None:
		"""Test that loadSpectrograms preserves metadata consistently with actual waveform properties."""
		sampleRateTarget = 44100

		_arraySpectrograms, dictionaryWaveformMetadata = loadSpectrograms(listPathFilenamesFromWaveformData, sampleRateTarget)

		for index, pathFilename in enumerate(listPathFilenamesFromWaveformData):
			waveformSingle = readAudioFile(pathFilename, sampleRateTarget)
			metadataSingle = dictionaryWaveformMetadata[index]

			expectedLengthWaveform = waveformSingle.shape[1]
			actualLengthWaveform = metadataSingle['lengthWaveform']
			expectedPathFilename = str(pathFilename)
			actualPathFilename = metadataSingle['pathFilename']

			assert actualLengthWaveform == expectedLengthWaveform, uniformTestFailureMessage(
				expectedLengthWaveform, actualLengthWaveform, "loadSpectrograms metadata lengthWaveform",
				listPathFilenamesFromWaveformData, sampleRateTarget, indexFile=index
			)
			assert actualPathFilename == expectedPathFilename, uniformTestFailureMessage(
				expectedPathFilename, actualPathFilename, "loadSpectrograms metadata pathFilename",
				listPathFilenamesFromWaveformData, sampleRateTarget, indexFile=index
			)

	def test_loadSpectrograms_roundTripReconstructionAccuracy(self, waveformDataStereo44kHz: WaveformAndMetadata) -> None:
		"""Test that loadSpectrograms produces spectrograms that roundtrip through direct STFT operations."""
		sampleRateTarget = 44100
		listPathFilenameSingle = [waveformDataStereo44kHz.pathFilename]

		arraySpectrograms, _dictionaryWaveformMetadata = loadSpectrograms(listPathFilenameSingle, sampleRateTarget)

		waveformOriginal = readAudioFile(waveformDataStereo44kHz.pathFilename, sampleRateTarget)
		spectrogramDirect = stft(waveformOriginal, sampleRate=sampleRateTarget)

		expectedShape = spectrogramDirect.shape
		actualShape = arraySpectrograms.shape[:-1]
		expectedCountFiles = 1
		actualCountFiles = arraySpectrograms.shape[-1]

		assert actualShape == expectedShape, uniformTestFailureMessage(
			expectedShape, actualShape, "loadSpectrograms roundtrip shape comparison", listPathFilenameSingle, sampleRateTarget
		)
		assert actualCountFiles == expectedCountFiles, uniformTestFailureMessage(
			expectedCountFiles, actualCountFiles, "loadSpectrograms roundtrip file count", listPathFilenameSingle, sampleRateTarget
		)

	def test_loadSpectrograms_rejectsEmptyInput(self) -> None:
		"""Test that loadSpectrograms raises ValueError for empty input."""
		standardizedEqualTo(ValueError, loadSpectrograms, [], 44100)

class TestStft:
	"""Test suite for stft functionality."""

	def test_stft_forwardTransform(self, waveformDataStereo44kHz: WaveformAndMetadata) -> None:
		"""Test that stft produces complex-valued spectrograms from real waveforms."""
		waveformSingle = waveformDataStereo44kHz.waveform

		spectrogram = stft(waveformSingle)

		actualDtype = spectrogram.dtype
		expectedComplexFloating = True
		actualComplexFloating = numpy.issubdtype(actualDtype, numpy.complexfloating)
		expectedNonEmpty = True
		actualNonEmpty = spectrogram.shape[0] > 0 and spectrogram.shape[1] > 0

		assert actualComplexFloating == expectedComplexFloating, uniformTestFailureMessage(
			"complex floating point type", actualDtype, "stft forward transform dtype", waveformSingle
		)
		assert actualNonEmpty == expectedNonEmpty, uniformTestFailureMessage(
			"non-empty spectrogram", spectrogram.shape, "stft forward transform shape", waveformSingle
		)

	def test_stft_inverseTransform(self, waveformDataStereo44kHz: WaveformAndMetadata) -> None:
		"""Test that stft inverse transform reconstructs waveforms accurately."""
		waveformOriginal = waveformDataStereo44kHz.waveform

		spectrogram = stft(waveformOriginal)
		waveformReconstructed = stft(spectrogram, inverse=True, lengthWaveform=waveformOriginal.shape[1])

		prototype_numpyAllClose(
			waveformOriginal, 1e-2, 1e-2,
			lambda: waveformReconstructed
		)

	@pytest.mark.parametrize("lengthWindowingFunctionSTFT,lengthHopSTFT", [
		(1024, 256),
		(2048, 512),
		(4096, 1024)
	])
	def test_stft_acceptsSTFTParameters(self, waveformDataStereo44kHz: WaveformAndMetadata, lengthWindowingFunctionSTFT: int, lengthHopSTFT: int) -> None:
		"""Test that stft accepts different windowing and hop parameters."""
		waveformSingle = waveformDataStereo44kHz.waveform
		sampleRate = waveformDataStereo44kHz.sampleRate

		spectrogram = stft(
			waveformSingle,
			sampleRate=sampleRate,
			lengthWindowingFunction=lengthWindowingFunctionSTFT,
			lengthHop=lengthHopSTFT
		)

		expectedNonEmpty = True
		actualNonEmpty = spectrogram.shape[0] > 0 and spectrogram.shape[1] > 0
		expectedComplexFloating = True
		actualComplexFloating = numpy.issubdtype(spectrogram.dtype, numpy.complexfloating)

		assert actualNonEmpty == expectedNonEmpty, uniformTestFailureMessage(
			"non-empty spectrogram", spectrogram.shape, "stft with custom parameters shape",
			waveformSingle, sampleRate=sampleRate,
			lengthWindowingFunction=lengthWindowingFunctionSTFT, lengthHop=lengthHopSTFT
		)
		assert actualComplexFloating == expectedComplexFloating, uniformTestFailureMessage(
			"complex floating point type", spectrogram.dtype, "stft with custom parameters dtype",
			waveformSingle, sampleRate=sampleRate,
			lengthWindowingFunction=lengthWindowingFunctionSTFT, lengthHop=lengthHopSTFT
		)

	def test_stft_rejectsInverseWithoutLengthWaveform(self, waveformDataStereo44kHz: WaveformAndMetadata) -> None:
		"""Test that stft raises ValueError when inverse=True but lengthWaveform is not provided."""
		waveformSingle = waveformDataStereo44kHz.waveform
		spectrogram = stft(waveformSingle)

		standardizedEqualTo(ValueError, stft, spectrogram, inverse=True)

class TestWaveformSpectrogramWaveform:
	"""Test suite for waveformSpectrogramWaveform functionality."""

	def test_waveformSpectrogramWaveform_identityTransform(self, waveformDataStereo44kHz: WaveformAndMetadata) -> None:
		"""Test that waveformSpectrogramWaveform with identity function preserves waveforms."""
		waveformOriginal = waveformDataStereo44kHz.waveform

		def identitySpectrogram(spectrogram: Any) -> Any:
			return spectrogram

		processor = waveformSpectrogramWaveform(identitySpectrogram)
		waveformProcessed = processor(waveformOriginal)

		prototype_numpyAllClose(
			waveformOriginal, 1e-2, 1e-2,
			lambda: waveformProcessed
		)

	def test_waveformSpectrogramWaveform_magnitudeOnlyTransform(self, waveformDataStereo44kHz: WaveformAndMetadata) -> None:
		"""Test that waveformSpectrogramWaveform with magnitude-only processing changes the waveform."""
		waveformOriginal = waveformDataStereo44kHz.waveform

		def magnitudeOnlySpectrogram(spectrogram: Any) -> Any:
			return numpy.abs(spectrogram)

		processor = waveformSpectrogramWaveform(magnitudeOnlySpectrogram)
		waveformProcessed = processor(waveformOriginal)

		expectedShapeMatch = True
		actualShapeMatch = waveformOriginal.shape == waveformProcessed.shape
		expectedContentDifferent = True
		actualContentDifferent = not numpy.allclose(waveformOriginal, waveformProcessed, atol=1e-2, rtol=1e-2)

		assert actualShapeMatch == expectedShapeMatch, uniformTestFailureMessage(
			waveformOriginal.shape, waveformProcessed.shape, "waveformSpectrogramWaveform magnitude-only shape preservation", waveformOriginal
		)
		assert actualContentDifferent == expectedContentDifferent, uniformTestFailureMessage(
			"different waveform content", "nearly identical content", "waveformSpectrogramWaveform magnitude-only content change", waveformOriginal
		)
