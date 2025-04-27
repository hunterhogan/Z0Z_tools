"""test_waveform or test_spectrogram? if a spectrogram is involved at any point, then test_spectrogram."""
from typing import Any
from Z0Z_tools import readAudioFile, writeWAV, stft, waveformSpectrogramWaveform, loadSpectrograms
import pytest
import numpy
from numpy.typing import NDArray
from numpy.testing import assert_allclose
from tests.conftest import uniformTestFailureMessage, standardizedEqualTo, prototype_numpyAllClose, prototype_numpyArrayEqual
from pathlib import Path


class TestLoadSpectrograms:
	"""Test suite for loadSpectrograms functionality."""

	def test_loadSpectrograms_returnsCorrectShapes(self, listPathFilenamesArrayWaveforms: list[Path]) -> None:
		"""Test that loadSpectrograms returns arrays with expected shapes based on the input files."""
		# Acquire
		sampleRateTarget = 44100

		# Act
		arraySpectrograms, dictionaryWaveformMetadata = loadSpectrograms(listPathFilenamesArrayWaveforms, sampleRateTarget)

		# Assert
		# The spectrogram array should have shape (freq_bins, time_frames, channels, count_files)
		assert len(arraySpectrograms.shape) == 4
		assert arraySpectrograms.shape[-1] == len(listPathFilenamesArrayWaveforms)
		assert len(dictionaryWaveformMetadata) == len(listPathFilenamesArrayWaveforms)

	def test_loadSpectrograms_complexOutputValues(self, listPathFilenamesArrayWaveforms: list[Path]) -> None:
		"""Test that loadSpectrograms returns complex-valued spectrograms."""
		# Acquire
		sampleRateTarget = 44100

		# Act
		arraySpectrograms, dictionaryWaveformMetadata = loadSpectrograms(listPathFilenamesArrayWaveforms, sampleRateTarget)

		# Assert
		assert numpy.issubdtype(arraySpectrograms.dtype, numpy.complexfloating)
		assert not numpy.isnan(arraySpectrograms).any()
		assert not numpy.isinf(arraySpectrograms).any()

	@pytest.mark.parametrize("lengthWindowingFunction,lengthHop", [
		(1024, 256),
		(2048, 512),
		(4096, 1024)
	])
	def test_loadSpectrograms_customParameters(self, listPathFilenamesArrayWaveforms: list[Path], lengthWindowingFunction: int, lengthHop: int) -> None:
		"""Test that loadSpectrograms correctly applies custom STFT parameters."""
		# Acquire
		sampleRateTarget = 44100

		# Act
		arraySpectrograms, dictionaryWaveformMetadata = loadSpectrograms(
			listPathFilenamesArrayWaveforms,
			sampleRateTarget,
			lengthWindowingFunction=lengthWindowingFunction,
			lengthHop=lengthHop
		)

		# Get expected shape by computing a single spectrogram with the same parameters
		waveform = readAudioFile(listPathFilenamesArrayWaveforms[0], sampleRateTarget)
		spectrogramExpected = stft(
			waveform,
			sampleRate=sampleRateTarget,
			lengthWindowingFunction=lengthWindowingFunction,
			lengthHop=lengthHop
		)

		# Assert: The first dimensions should match the expected spectrogram shape
		assert arraySpectrograms.shape[:-1] == spectrogramExpected.shape

	def test_loadSpectrograms_singleFile(self, listPathFilenamesArrayWaveforms: list[Path]) -> None:
		"""Test loading a spectrogram from a single file."""
		# Acquire
		sampleRateTarget = 44100
		pathFilenameSingle = listPathFilenamesArrayWaveforms[0]

		# Act
		arraySpectrograms, dictionaryWaveformMetadata = loadSpectrograms([pathFilenameSingle], sampleRateTarget)

		# Compute directly for comparison
		waveform = readAudioFile(pathFilenameSingle, sampleRateTarget)
		spectrogramExpected = stft(waveform, sampleRate=sampleRateTarget)

		# Assert
		assert arraySpectrograms.shape[:-1] == spectrogramExpected.shape
		assert arraySpectrograms.shape[-1] == 1
		assert len(dictionaryWaveformMetadata) == 1
		assert pathFilenameSingle.name in dictionaryWaveformMetadata[0]['pathFilename']

	@pytest.mark.parametrize("sampleRateTarget", [22050, 44100, 48000])
	def test_loadSpectrograms_differentSampleRates(self, listPathFilenamesArrayWaveforms: list[Path], sampleRateTarget: int) -> None:
		"""Test loading spectrograms with different target sample rates."""
		# Act
		arraySpectrograms, dictionaryWaveformMetadata = loadSpectrograms(
			listPathFilenamesArrayWaveforms,
			sampleRateTarget
		)

		# Assert - Sample rate should affect the time dimension
		waveform = readAudioFile(listPathFilenamesArrayWaveforms[0], sampleRateTarget)
		spectrogramSingle = stft(waveform, sampleRate=sampleRateTarget)

		assert arraySpectrograms.shape[:-1] == spectrogramSingle.shape

	def test_loadSpectrograms_preservesWaveformSampleRate(self, listPathFilenamesArrayWaveforms: list[Path]) -> None:
		"""Test that loadSpectrograms correctly resamples and preserves metadata."""
		# Acquire
		sampleRateTarget = 44100

		# Act
		arraySpectrograms, dictionaryWaveformMetadata = loadSpectrograms(
			listPathFilenamesArrayWaveforms,
			sampleRateTarget
		)

		# Assert - Verify that the returned metadata contains the expected length
		for index, pathFilename in enumerate(listPathFilenamesArrayWaveforms):
			waveform = readAudioFile(pathFilename, sampleRateTarget)
			assert dictionaryWaveformMetadata[index]['lengthWaveform'] == waveform.shape[1]

	def test_loadSpectrograms_roundTrip(self, listPathFilenamesArrayWaveforms: list[Path]) -> None:
		"""Test that loadSpectrograms produces spectrograms that can be inverted back to similar waveforms."""
		# Acquire
		sampleRateTarget = 44100
		indexFile = 0

		# Act
		arraySpectrograms, dictionaryWaveformMetadata = loadSpectrograms(
			listPathFilenamesArrayWaveforms,
			sampleRateTarget
		)

		# Get original waveform
		waveformOriginal = readAudioFile(listPathFilenamesArrayWaveforms[indexFile], sampleRateTarget)
		spectrogramSingle = arraySpectrograms[..., indexFile]

		# Invert the spectrogram back to a waveform
		waveformReconstructed = stft(
			spectrogramSingle,
			inverse=True,
			lengthWaveform=dictionaryWaveformMetadata[indexFile]['lengthWaveform'],
			sampleRate=sampleRateTarget
		)

		# Assert - The reconstructed waveform should be close to the original
		# Note: Due to STFT-ISTFT transformation loss, we use a higher tolerance
		assert waveformOriginal.shape == waveformReconstructed.shape
		assert numpy.allclose(waveformOriginal, waveformReconstructed, atol=1e-2, rtol=1e-2)

	def test_loadSpectrograms_emptyInput(self) -> None:
		"""Test that loadSpectrograms handles empty input correctly."""
		# Act & Assert
		with pytest.raises(ValueError):
			loadSpectrograms([], 44100)

	def test_loadSpectrograms_metadataConsistency(self, listPathFilenamesArrayWaveforms: list[Path]) -> None:
		"""Test that the metadata returned by loadSpectrograms is consistent with file properties."""
		# Acquire
		sampleRateTarget = 44100

		# Act
		arraySpectrograms, dictionaryWaveformMetadata = loadSpectrograms(
			listPathFilenamesArrayWaveforms,
			sampleRateTarget
		)

		# Assert - Check that every file has corresponding metadata
		for index, pathFilename in enumerate(listPathFilenamesArrayWaveforms):
			metadata = dictionaryWaveformMetadata[index]
			assert str(pathFilename) == metadata['pathFilename']
			assert 'lengthWaveform' in metadata
			assert 'samplesLeading' in metadata
			assert 'samplesTrailing' in metadata
			assert isinstance(metadata['lengthWaveform'], int)

# All of the test functions below here are TERRIBLE and obviously do not follow the instructions.
#Test cases for stft
def test_stft_forward():
	# Test with a simple sine wave
	signal = numpy.sin(2 * numpy.pi * 1000 * numpy.arange(44100) / 44100)
	stft_result = stft(signal)
	assert stft_result.shape[0] > 0  # check if the result is not empty
	assert numpy.issubdtype(stft_result.dtype, numpy.complexfloating)  # check if the result is complex

def test_stft_inverse():
	# Test with a simple sine wave
	signal = numpy.sin(2 * numpy.pi * 1000 * numpy.arange(44100) / 44100)
	stft_result = stft(signal)
	istft_result = stft(stft_result, inverse=True, lengthWaveform=len(signal))
	assert_allclose(signal, istft_result, atol=1e-2) # Check for near equality.  Higher tolerance due to different STFT implementation

def test_stft_multichannel():
	# Test with a multichannel signal
	signal = numpy.random.rand(2, 44100)
	stft_result = stft(signal)
	assert stft_result.shape[0] > 0 #check if the result is not empty.
	assert stft_result.shape[1] > 0 #check if the result is not empty.

def test_stft_invalid_input():
	with pytest.raises(AttributeError):
		stft("invalid input") # type: ignore

def test_stft_custom_window():
	# Test with a custom window function
	signal = numpy.random.rand(44100)
	window = numpy.hanning(1024)
	stft_result = stft(signal, windowingFunction=window, lengthWindowingFunction=len(window))
	assert stft_result.shape[0] > 0 #check if the result is not empty.
	assert isinstance(stft_result[0,0], complex) #check if the result is complex

def test_stft_indexing_axis():
	# Test with indexing axis
	signal = numpy.random.rand(2,44100)
	stft_result = stft(signal, indexingAxis=0)
	assert stft_result.shape[0] > 0 #check if the result is not empty.
	assert stft_result.shape[1] > 0 #check if the result is not empty.

def test_stft_zero_signal():
	signal = numpy.zeros(44100)
	result = stft(signal)
	assert numpy.allclose(result, 0)

def test_stft_reconstruction_accuracy():
	# Test reconstruction accuracy with different window types
	signal = numpy.random.rand(44100)
	windows = [None, numpy.hanning(1024), numpy.hamming(1024)]

	for window in windows:
		spec = stft(signal, windowingFunction=window)
		reconstructed = stft(spec, inverse=True, lengthWaveform=len(signal), windowingFunction=window)
		assert_allclose(signal, reconstructed, atol=1e-2)

def test_stft_batch_processing():
	# Test processing multiple signals simultaneously
	batch_size = 3
	signals = numpy.random.rand(batch_size, 44100)

	# Process as batch
	result_batch = stft(signals, indexingAxis=0)

	# Process individually
	results_individual = numpy.stack([stft(sig) for sig in signals], axis=0, dtype=numpy.complex128)

	assert_allclose(result_batch, results_individual, atol=1e-7)

def test_stft_dtype_handling():
	# Test different input dtypes
	dtypes = [numpy.float32, numpy.float64]
	signal = numpy.random.rand(44100)

	for dtype in dtypes:
		sig = signal.astype(dtype)
		result = stft(sig)
		assert result.dtype == numpy.complex128 or result.dtype == numpy.complex64

def test_stft_inverse_without_length():
	signal = numpy.random.rand(44100)
	spec = stft(signal)
	with pytest.raises(ValueError):
		stft(spec, inverse=True)  # lengthWaveform is required for inverse # type: ignore

def test_stft_withNaNvalues():
	"""Test stft with input containing NaN values"""
	arrayWaveform = numpy.random.rand(44100)
	arrayWaveform[22050] = numpy.nan  # Introduce a NaN value
	arrayTransformed = stft(arrayWaveform)
	assert numpy.isnan(arrayTransformed).any()

def test_stft_withInfValues():
	"""Test stft with input containing Inf values"""
	arrayWaveform = numpy.random.rand(44100)
	arrayWaveform[22050] = numpy.inf  # Introduce an Inf value
	arrayTransformed = stft(arrayWaveform)
	assert numpy.isinf(arrayTransformed).any()

def test_stft_extremeHopLengths():
	"""Test stft with very small and very large hop lengths"""
	arrayWaveform = numpy.random.rand(44100)
	listHopLengths = [1, len(arrayWaveform) // 2, len(arrayWaveform)]
	for hopLength in listHopLengths:
		arrayTransformed = stft(arrayWaveform, lengthHop=hopLength)
		assert arrayTransformed.shape[1] > 0

def test_stft_oddLengthSignal():
	"""Test stft with odd-length signal"""
	arrayWaveform = numpy.random.rand(44101)  # Odd-length signal
	arrayTransformed = stft(arrayWaveform)
	arrayReconstructed = stft(arrayTransformed, inverse=True, lengthWaveform=len(arrayWaveform))
	assert_allclose(arrayWaveform, arrayReconstructed, atol=1e-2)

def test_stft_realOutputInverse():
	"""Test that inverse stft of real-valued stft returns a signal different from the original"""
	arrayWaveform = numpy.random.rand(44100)
	arrayTransformed = stft(arrayWaveform)
	arrayMagnitude = numpy.abs(arrayTransformed)
	arrayReconstructed = stft(arrayMagnitude, inverse=True, lengthWaveform=len(arrayWaveform))
	# Since phase information is lost, reconstructed signal won't match original
	assert not numpy.allclose(arrayWaveform, arrayReconstructed, atol=1e-2)

def test_stft_differentSampleRates():
	"""Test stft with different sample rates"""
	arrayWaveform = numpy.random.rand(44100)
	listSampleRates = [8000, 16000, 44100, 48000]
	for sampleRate in listSampleRates:
		arrayTransformed = stft(arrayWaveform, sampleRate=sampleRate)
		assert arrayTransformed.shape[1] > 0  # Ensure that frames are computed

def test_stft_largeDataset():
	"""Test stft with a large input signal"""
	arrayWaveform = numpy.random.rand(10 * 44100)  # 10 seconds of audio at 44.1kHz
	arrayTransformed = stft(arrayWaveform)
	assert arrayTransformed.shape[1] > 0

def test_stft_nonStandardWindowFunction():
	"""Test stft with a custom non-standard window function"""
	arrayWaveform = numpy.random.rand(44100)
	lengthWindowingFunction = 1024
	arrayWindowingFunction = numpy.blackman(lengthWindowingFunction)
	arrayTransformed = stft(arrayWaveform, windowingFunction=arrayWindowingFunction, lengthWindowingFunction=lengthWindowingFunction)
	arrayReconstructed = stft(arrayTransformed, inverse=True, lengthWaveform=len(arrayWaveform), windowingFunction=arrayWindowingFunction)
	assert_allclose(arrayWaveform, arrayReconstructed, atol=1e-2)

class TestStftIstft:
	def test_identity_transform(self, waveform_dataRTFStyleGuide: dict[str, dict[str, NDArray[numpy.float32] | int]]):
		"""Test that passing through identity function preserves waveform."""
		waveform = waveform_dataRTFStyleGuide['stereo']['waveform'].T # (channels, samples)

		@waveformSpectrogramWaveform
		def identity_transform(spectrogram):
			return spectrogram

		waveform_reconstructed = identity_transform(waveform)
		assert numpy.allclose(waveform, waveform_reconstructed, atol=1e-6)

	def test_phase_inversion(self, waveform_dataRTFStyleGuide: dict[str, dict[str, NDArray[numpy.float32] | int]]):
		"""Test phase inversion through STFT-ISTFT."""
		waveform = waveform_dataRTFStyleGuide['stereo']['waveform'].T

		@waveformSpectrogramWaveform
		def invert_phase(spectrogram):
			return -spectrogram

		waveform_inverted = invert_phase(waveform)
		assert numpy.allclose(waveform, -waveform_inverted, atol=1e-6)

	def test_zero_transform(self, waveform_dataRTFStyleGuide: dict[str, dict[str, NDArray[numpy.float32] | int]]):
		"""Test transform that zeros out the spectrogram."""
		waveform = waveform_dataRTFStyleGuide['stereo']['waveform'].T

		@waveformSpectrogramWaveform
		def zero_spectrogram(spectrogram):
			return numpy.zeros_like(spectrogram)

		waveform_zeroed = zero_spectrogram(waveform)
		assert numpy.allclose(waveform_zeroed, numpy.zeros_like(waveform), atol=1e-6)

	def test_shape_preservation(self, waveform_dataRTFStyleGuide: dict[str, dict[str, NDArray[numpy.float32] | int]]):
		"""Test that output shape matches input shape."""
		waveform = waveform_dataRTFStyleGuide['stereo']['waveform'].T

		@waveformSpectrogramWaveform
		def pass_through(spectrogram):
			return spectrogram

		waveform_out = pass_through(waveform)
		assert waveform.shape == waveform_out.shape
