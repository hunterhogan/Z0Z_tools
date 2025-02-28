"""test_waveform or test_spectrogram? if a spectrogram is involved at any point, then test_spectrogram."""
from tests.conftest import *
import pytest
import numpy
from numpy.testing import assert_allclose

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
	def test_identity_transform(self, waveform_data):
		"""Test that passing through identity function preserves waveform."""
		waveform = waveform_data['stereo']['waveform'].T # (channels, samples)

		@waveformSpectrogramWaveform
		def identity_transform(spectrogram):
			return spectrogram

		waveform_reconstructed = identity_transform(waveform)
		assert numpy.allclose(waveform, waveform_reconstructed, atol=1e-6)

	def test_phase_inversion(self, waveform_data):
		"""Test phase inversion through STFT-ISTFT."""
		waveform = waveform_data['stereo']['waveform'].T

		@waveformSpectrogramWaveform
		def invert_phase(spectrogram):
			return -spectrogram

		waveform_inverted = invert_phase(waveform)
		assert numpy.allclose(waveform, -waveform_inverted, atol=1e-6)

	def test_zero_transform(self, waveform_data):
		"""Test transform that zeros out the spectrogram."""
		waveform = waveform_data['stereo']['waveform'].T

		@waveformSpectrogramWaveform
		def zero_spectrogram(spectrogram):
			return numpy.zeros_like(spectrogram)

		waveform_zeroed = zero_spectrogram(waveform)
		assert numpy.allclose(waveform_zeroed, numpy.zeros_like(waveform), atol=1e-6)

	def test_shape_preservation(self, waveform_data):
		"""Test that output shape matches input shape."""
		waveform = waveform_data['stereo']['waveform'].T

		@waveformSpectrogramWaveform
		def pass_through(spectrogram):
			return spectrogram

		waveform_out = pass_through(waveform)
		assert waveform.shape == waveform_out.shape
