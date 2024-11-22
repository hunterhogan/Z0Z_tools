from Z0Z_tools import readAudioFile, loadWaveforms
import numpy
import pathlib 
import unittest

class TestReadAudioFile(unittest.TestCase):

    def setUp(self):
        self.test_data_dir = pathlib.Path("unittests/dataSamples")
        self.mono_file = self.test_data_dir / "testWooWooMono16kHz32integerClipping9sec.wav"
        self.stereo_file = self.test_data_dir / "testSine2ch5sec.wav"
        self.non_audio_file = self.test_data_dir / "testVideo11sec.mkv"

    def test_read_mono_audio_file(self):
        waveform = readAudioFile(self.mono_file)
        self.assertIsInstance(waveform, numpy.ndarray)
        self.assertEqual(waveform.ndim, 2)  # Mono should have 1 dimension

    def test_read_stereo_audio_file(self):
        waveform = readAudioFile(self.stereo_file)
        self.assertIsInstance(waveform, numpy.ndarray)
        self.assertEqual(waveform.ndim, 2)  # Stereo should have 2 dimensions
        self.assertEqual(waveform.shape[0], 2)  # First dimension should be 2 for stereo

class TestLoadWaveforms(unittest.TestCase):

    def test_load_waveforms_mono(self):
        """Test loading mono waveforms with different sample rates."""
        path_filenames = [
            pathlib.Path("unittests/dataSamples/testWooWooMono16kHz32integerClipping9secCopy1.wav"),
            pathlib.Path("unittests/dataSamples/testWooWooMono16kHz32integerClipping9secCopy2.wav"),
            pathlib.Path("unittests/dataSamples/testWooWooMono16kHz32integerClipping9secCopy3.wav"),
        ]
        array_waveforms = loadWaveforms(path_filenames, sampleRate=44100)
        self.assertEqual(array_waveforms.shape, (2, 396900, 3))

    def test_load_waveforms_stereo(self):
        """Test loading stereo waveforms with different sample rates."""
        path_filenames = [
            pathlib.Path("unittests/dataSamples/testSine2ch5secCopy1.wav"),
            pathlib.Path("unittests/dataSamples/testSine2ch5secCopy2.wav"),
            pathlib.Path("unittests/dataSamples/testSine2ch5secCopy3.wav"),
            pathlib.Path("unittests/dataSamples/testSine2ch5secCopy4.wav"),
        ]
        array_waveforms = loadWaveforms(path_filenames, sampleRate=44100)
        self.assertEqual(array_waveforms.shape, (2, 220500, 4))

    def test_load_waveforms_mixed_channels(self):
        """Test loading a mix of mono and stereo waveforms."""
        path_filenames = [
            pathlib.Path("unittests/dataSamples/testWooWooMono16kHz32integerClipping9sec.wav"),
            pathlib.Path("unittests/dataSamples/testSine2ch5sec.wav")
        ]
        array_waveforms = loadWaveforms(path_filenames, sampleRate=44100)
        self.assertEqual(array_waveforms.shape, (2, 396900, 2))


if __name__ == "__main__":
    unittest.main()