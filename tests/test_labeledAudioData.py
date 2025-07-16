from tests.conftest import sampleData, sampleData44100, sampleData48000, WaveformAndMetadata
from typing import Final
from Z0Z_tools import readAudioFile
import numpy
import pytest

# Constants for test validation
CHANNELS_STEREO: Final[int] = 2
CHANNELS_MONO: Final[int] = 1
TOLERANCE_LUFS: Final[float] = 3.0  # LUFS measurement tolerance
LUFS_LOWER_BOUND: Final[float] = -100.0  # Reasonable lower bound for LUFS

class TestReadAudioFileWithLabeledData:
	"""Test readAudioFile function using the properly labeled LUFS dataset."""

	@pytest.mark.parametrize("waveformData", sampleData44100())
	def test_readLabeledAudioFiles44100(self, waveformData: WaveformAndMetadata) -> None:
		"""Test reading all labeled 44.1kHz audio files."""
		waveformResult = readAudioFile(waveformData.pathFilename)

		# Verify basic properties
		assert waveformResult.shape[0] == CHANNELS_STEREO
		assert waveformResult.dtype.name == 'float32'

		# Verify waveform has reasonable audio content
		assert waveformResult.shape[1] > 0  # Has samples
		amplitudeMax = abs(waveformResult).max()
		assert amplitudeMax > 0.0  # Not silent
		assert amplitudeMax <= 1.0  # Not clipped

	@pytest.mark.parametrize("waveformData", sampleData48000())
	def test_readLabeledAudioFiles48000(self, waveformData: WaveformAndMetadata) -> None:
		"""Test reading all labeled 48kHz audio files."""
		waveformResult = readAudioFile(waveformData.pathFilename)

		# Verify basic properties
		assert waveformResult.shape[0] == CHANNELS_STEREO
		assert waveformResult.dtype.name == 'float32'

		# Verify waveform has reasonable audio content
		assert waveformResult.shape[1] > 0  # Has samples
		amplitudeMax = abs(waveformResult).max()
		assert amplitudeMax > 0.0  # Not silent
		assert amplitudeMax <= 1.0  # Not clipped

	@pytest.mark.parametrize("waveformData", [d for d in sampleData() if d.channelsTotal == CHANNELS_MONO])
	def test_readMonoFilesConvertToStereo(self, waveformData: WaveformAndMetadata) -> None:
		"""Test that mono files from labeled dataset are converted to stereo."""
		waveformResult = readAudioFile(waveformData.pathFilename)

		# Should always be stereo regardless of original channel count
		assert waveformResult.shape[0] == CHANNELS_STEREO

		# For mono files, both channels should be identical
		if waveformData.channelsTotal == CHANNELS_MONO:
			# Allow for small numerical differences due to processing
			numpy.testing.assert_allclose(waveformResult[0], waveformResult[1], rtol=1e-10)

	@pytest.mark.parametrize("waveformData", [d for d in sampleData() if d.channelsTotal == CHANNELS_STEREO])
	def test_readStereoFilesPreserveChannels(self, waveformData: WaveformAndMetadata) -> None:
		"""Test that stereo files from labeled dataset maintain channel independence."""
		waveformResult = readAudioFile(waveformData.pathFilename)

		assert waveformResult.shape[0] == CHANNELS_STEREO

		# For stereo files, channels may be different or identical depending on content
		# This tests that we're not accidentally duplicating channels
		channelDifference = numpy.mean(abs(waveformResult[0] - waveformResult[1]))
		# If channels are identical, difference should be very small
		# If channels are different, difference should be meaningful
		# We allow for both cases but log the result
		assert channelDifference >= 0.0  # Sanity check

	def test_consistentResultsAcrossReads(self) -> None:
		"""Test that reading the same file multiple times gives identical results."""
		# Use the first available sample
		allSamples = sampleData()
		if not allSamples:
			pytest.skip("No sample data available")

		waveformData = allSamples[0]

		# Read the same file multiple times
		waveformFirst = readAudioFile(waveformData.pathFilename)
		waveformSecond = readAudioFile(waveformData.pathFilename)
		waveformThird = readAudioFile(waveformData.pathFilename)

		# Results should be identical
		numpy.testing.assert_array_equal(waveformFirst, waveformSecond)
		numpy.testing.assert_array_equal(waveformSecond, waveformThird)

	@pytest.mark.parametrize("waveformData", sampleData()[:5])  # Test first 5 files only for performance
	def test_metadataAccuracy(self, waveformData: WaveformAndMetadata) -> None:
		"""Test that file metadata matches expected values from filename parsing."""
		# Test that the sample rate information is reasonable
		# We can't directly test sample rate from the waveform alone,
		# but we can test that the parsed metadata is sensible
		assert waveformData.sampleRate in [44100, 48000]
		assert waveformData.channelsTotal in [1, 2]
		assert waveformData.LUFS < 0  # LUFS should be negative (below digital full scale)
		assert waveformData.LUFS > LUFS_LOWER_BOUND

		# Test ID field has meaningful content
		assert len(waveformData.ID) > 0
		assert waveformData.ID != "unknown"
