import pytest
import numpy
import soundfile
import io
from pathlib import Path
from numpy.typing import NDArray
from Z0Z_tools.ioAudio import readAudioFile, loadWaveforms, writeWav, resampleWaveform

# Test data paths
DATA_DIR = Path("tests/dataSamples")
PATHS = {
    'mono': DATA_DIR / "testWooWooMono16kHz32integerClipping9sec.wav",
    'stereo': DATA_DIR / "testSine2ch5sec.wav",
    'video': DATA_DIR / "testVideo11sec.mkv",
    'mono_copies': [DATA_DIR / f"testWooWooMono16kHz32integerClipping9secCopy{i}.wav" for i in range(1, 4)],
    'stereo_copies': [DATA_DIR / f"testSine2ch5secCopy{i}.wav" for i in range(1, 5)]
}

@pytest.fixture
def waveform_data():
    """Fixture providing sample waveform data and sample rates."""
    mono_data, mono_sr = soundfile.read(PATHS['mono'], dtype='float32')
    stereo_data, stereo_sr = soundfile.read(PATHS['stereo'], dtype='float32')
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

@pytest.fixture
def temp_wav_file(tmp_path):
    """Fixture providing a temporary WAV file path."""
    return tmp_path / "test_output.wav"

# readAudioFile tests
class TestReadAudioFile:
    def test_mono_to_stereo_conversion(self):
        """Test that mono files are properly converted to stereo."""
        waveform = readAudioFile(PATHS['mono'])
        assert waveform.shape[0] == 2  # Should be stereo (2 channels)

    def test_stereo_file_reading(self):
        """Test reading a stereo file directly."""
        waveform = readAudioFile(PATHS['stereo'])
        assert waveform.shape[0] == 2

    @pytest.mark.parametrize("sample_rate", [16000, 44100, 48000])
    def test_resampling(self, sample_rate):
        """Test resampling functionality with different sample rates."""
        waveform = readAudioFile(PATHS['mono'], sampleRate=sample_rate)
        expected_length = int(sample_rate * 9)  # 9-second file
        assert waveform.shape[1] == pytest.approx(expected_length, rel=0.1)

    @pytest.mark.parametrize("invalid_input", [
        "nonexistent_file.wav",
        PATHS['video']
    ])
    def test_invalid_inputs(self, invalid_input):
        """Test handling of invalid inputs."""
        with pytest.raises((FileNotFoundError, soundfile.LibsndfileError)):
            readAudioFile(invalid_input)

# loadWaveforms tests
class TestLoadWaveforms:
    @pytest.mark.parametrize("file_list,expected_shape", [
        (PATHS['mono_copies'], (2, 396900, 3)),
        (PATHS['stereo_copies'], (2, 220500, 4))
    ])
    def test_batch_loading(self, file_list, expected_shape):
        """Test loading multiple files of the same type."""
        array_waveforms = loadWaveforms(file_list)
        assert array_waveforms.shape == expected_shape

    def test_mixed_file_types(self):
        """Test loading a mix of mono and stereo files."""
        mixed_files = [PATHS['mono_copies'][0], PATHS['stereo_copies'][0]]
        array_waveforms = loadWaveforms(mixed_files)
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
    def test_resampling_rates(self, waveform_data, source_rate, target_rate, expected_factor):
        """Test resampling with different rate combinations."""
        waveform = waveform_data['mono']['waveform']
        resampled = resampleWaveform(waveform, target_rate, source_rate)
        expected_length = int(waveform.shape[0] * expected_factor)
        assert resampled.shape[0] == expected_length

    def test_same_rate_no_change(self, waveform_data):
        """Test that no resampling occurs when rates match."""
        waveform = waveform_data['stereo']['waveform']
        rate = waveform_data['stereo']['sample_rate']
        resampled = resampleWaveform(waveform, rate, rate)
        assert numpy.array_equal(resampled, waveform)

    @pytest.mark.parametrize("invalid_input", [
        ('not_an_array', 44100, 22050),
        (numpy.array([1, 2, 3]), -44100, 22050)
    ])
    def test_invalid_inputs(self, invalid_input):
        """Test handling of invalid inputs."""
        with pytest.raises((AttributeError, ValueError)):
            resampleWaveform(*invalid_input)

# writeWav tests
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
    def test_write_and_verify(self, temp_wav_file, test_case):
        """Test writing WAV files and verifying their contents."""
        # Input waveform shape: (channels, samples)
        waveform = numpy.random.rand(test_case['channels'], test_case['samples']).astype(numpy.float32)
        writeWav(temp_wav_file, waveform)
        
        # soundfile.read returns shape (samples,) for mono or (samples, channels) for stereo
        read_waveform, sr = soundfile.read(temp_wav_file)
        
        assert sr == 44100  # Default sample rate
        assert read_waveform.shape == test_case['expected_shape'], \
            f"Shape mismatch for {test_case['description']}: " \
            f"expected {test_case['expected_shape']}, got {read_waveform.shape}"
            
        # For comparison, we need to handle mono and stereo cases differently
        if test_case['channels'] == 1:
            assert numpy.allclose(read_waveform, waveform.flatten())
        else:
            assert numpy.allclose(read_waveform, waveform.T)

    def test_directory_creation(self, tmp_path):
        """Test automatic directory creation."""
        nested_path = tmp_path / "nested" / "dirs" / "test.wav"
        waveform = numpy.random.rand(2, 1000).astype(numpy.float32)
        writeWav(nested_path, waveform)
        assert nested_path.exists()

    def test_file_overwrite(self, temp_wav_file):
        """Test overwriting existing files."""
        waveform1 = numpy.ones((2, 1000), dtype=numpy.float32)
        waveform2 = numpy.zeros((2, 1000), dtype=numpy.float32)
        
        writeWav(temp_wav_file, waveform1)
        writeWav(temp_wav_file, waveform2)
        
        read_waveform, _ = soundfile.read(temp_wav_file)
        assert numpy.allclose(read_waveform.T, waveform2)

    def test_binary_stream(self):
        """Test writing to a binary stream."""
        waveform = numpy.random.rand(2, 1000).astype(numpy.float32)
        bio = io.BytesIO()
        writeWav(bio, waveform)
        assert bio.getvalue()  # Verify that data was written