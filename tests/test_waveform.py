from typing import Any, Literal
from tests.conftest import *
import io
import numpy
import pathlib
import pytest
import soundfile

# readAudioFile tests
class TestReadAudioFile:
	def test_mono_to_stereo_conversion(self):
		"""Test that mono files are properly converted to stereo."""
		pathFilename = dumbassDictionaryPathFilenamesAudioFiles['mono']
		if isinstance(pathFilename, list):
			pathFilename = pathFilename[0]
		waveform = readAudioFile(pathFilename)
		assert waveform.shape[0] == 2  # Should be stereo (2 channels)

	def test_stereo_file_reading(self):
		"""Test reading a stereo file directly."""
		pathFilename = dumbassDictionaryPathFilenamesAudioFiles['stereo']
		if isinstance(pathFilename, list):
			pathFilename = pathFilename[0]
		waveform = readAudioFile(pathFilename)
		assert waveform.shape[0] == 2

	@pytest.mark.parametrize("sample_rate", [16000, 44100, 48000])
	def test_resampling(self, sample_rate: float) -> None:
		"""Test resampling functionality with different sample rates."""
		pathFilename = dumbassDictionaryPathFilenamesAudioFiles['mono']
		if isinstance(pathFilename, list):
			pathFilename = pathFilename[0]
		waveform = readAudioFile(pathFilename, sampleRate=sample_rate)
		expected_length = int(sample_rate * 9)  # 9-second file
		assert waveform.shape[1] == pytest.approx(expected_length, rel=0.1)

	@pytest.mark.parametrize("invalid_input", [
		"nonexistent_file.wav",
		dumbassDictionaryPathFilenamesAudioFiles['video']
	])
	def test_invalid_inputs(self, invalid_input: Any | Literal['nonexistent_file.wav']):
		"""Test handling of invalid inputs."""
		with pytest.raises((FileNotFoundError, soundfile.LibsndfileError)):
			readAudioFile(invalid_input)

# loadWaveforms tests
class TestLoadWaveforms:
	@pytest.mark.parametrize("file_list,expected_shape", [
		(dumbassDictionaryPathFilenamesAudioFiles['mono_copies'], (2, 396900, 3)),
		(dumbassDictionaryPathFilenamesAudioFiles['stereo_copies'], (2, 220500, 4))
	])
	def test_batch_loading(self, file_list: Any, expected_shape: tuple[int]):
		"""Test loading multiple files of the same type."""
		array_waveforms = loadWaveforms(file_list)
		assert array_waveforms.shape == expected_shape

	def test_mixed_file_types(self):
		"""Test loading a mix of mono and stereo files."""
		mono_files: pathlib.Path | list[pathlib.Path] = dumbassDictionaryPathFilenamesAudioFiles['mono_copies']
		stereo_files: pathlib.Path | list[pathlib.Path] = dumbassDictionaryPathFilenamesAudioFiles['stereo_copies']
		mixed_files: list[pathlib.Path] = [mono_files[0] if isinstance(mono_files, list) else mono_files,
					stereo_files[0] if isinstance(stereo_files, list) else stereo_files]
		array_waveforms:ndarray[tuple[int, int, int], dtype[float32]] = loadWaveforms(mixed_files)
		assert array_waveforms.shape[0] == 2  # Should be stereo
		assert array_waveforms.shape[2] == 2  # Two files

	def test_empty_input(self):
		"""Test handling of empty input list."""
		with pytest.raises(ValueError):
			loadWaveforms([])

# resampleWaveform tests
class TestResampleWaveform:
	@pytest.mark.parametrize("source_rate,target_rate,expected_factor", [
		(16000, 44100, 2.75625),
		(44100, 22050, 0.5),
		(44100, 44100, 1.0)
	])
	def test_resampling_rates(self, waveform_data: dict[str, dict[str, Any]], source_rate: Literal[16000] | Literal[44100], target_rate: Literal[44100] | Literal[22050], expected_factor: float):
		"""Test resampling with different rate combinations."""
		waveform = waveform_data['mono']['waveform']
		resampled = resampleWaveform(waveform, target_rate, source_rate)
		expected_length = int(waveform.shape[0] * expected_factor)
		assert resampled.shape[0] == expected_length

	def test_same_rate_no_change(self, waveform_data: dict[str, dict[str, Any]]):
		"""Test that no resampling occurs when rates match."""
		waveform = waveform_data['stereo']['waveform']
		rate = waveform_data['stereo']['sample_rate']
		resampled = resampleWaveform(waveform, rate, rate)
		assert numpy.array_equal(resampled, waveform)

	@pytest.mark.parametrize("invalid_input", [
		('not_an_array', 44100, 22050),
		(numpy.array([1, 2, 3]), -44100, 22050)
	])
	def test_invalid_inputs(self, invalid_input: Any) -> None:
		"""Test handling of invalid inputs."""
		with pytest.raises((AttributeError, ValueError)):
			resampleWaveform(*invalid_input)

class TestWriteWav:
	@pytest.mark.parametrize("test_case", [
		{
			'channels': 1,
			'samples': 1000,
			'description': "mono audio",
			'expected_shape': (1000,)  # Mono should be 1D array
		},
		{
			'channels': 2,
			'samples': 1000,
			'description': "stereo audio",
			'expected_shape': (1000, 2)  # Stereo should be 2D array (samples, channels)
		}
	])
	def test_write_and_verify(self, pathFilenameTmpTesting: pathlib.Path, test_case: Any) -> None:
		"""Test writing WAV files and verifying their contents."""
		# Input waveform shape: (channels, samples)
		waveform = numpy.random.rand(test_case['channels'], test_case['samples']).astype(numpy.float32)
		writeWAV(pathFilenameTmpTesting, waveform)

		# soundfile.read returns shape (samples,) for mono or (samples, channels) for stereo
		read_waveform, sr = soundfile.read(pathFilenameTmpTesting)

		assert sr == 44100  # Default sample rate
		assert read_waveform.shape == test_case['expected_shape'], \
			f"Shape mismatch for {test_case['description']}: " \
			f"expected {test_case['expected_shape']}, got {read_waveform.shape}"

		# For comparison, we need to handle mono and stereo cases differently
		if test_case['channels'] == 1:
			assert numpy.allclose(read_waveform, waveform.flatten())
		else:
			assert numpy.allclose(read_waveform, waveform.T)

	def test_directory_creation(self, pathTmpTesting: pathlib.Path) -> None:
		"""Test automatic directory creation."""
		nested_path: pathlib.Path = pathTmpTesting / "nested" / "dirs" / "test.wav"
		waveform = numpy.random.rand(2, 1000).astype(numpy.float32)
		writeWAV(nested_path, waveform)
		assert nested_path.exists()

	def test_file_overwrite(self, pathFilenameTmpTesting: pathlib.Path) -> None:
		"""Test overwriting existing files."""
		waveform1 = numpy.ones((2, 1000), dtype=numpy.float32)
		waveform2 = numpy.zeros((2, 1000), dtype=numpy.float32)

		writeWAV(pathFilenameTmpTesting, waveform1)
		writeWAV(pathFilenameTmpTesting, waveform2)

		read_waveform, _ = soundfile.read(pathFilenameTmpTesting)
		assert numpy.allclose(read_waveform.T, waveform2)

	def test_binary_stream(self):
		"""Test writing to a binary stream."""
		waveform = numpy.random.rand(2, 1000).astype(numpy.float32)
		bio = io.BytesIO()
		writeWAV(bio, waveform)
		assert bio.getvalue()  # Verify that data was written
