from numpy.typing import NDArray
from pathlib import Path
from Z0Z_tools.Z0Z_ioAudio import readAudioFile
import numpy
import unittest

class TestReadAudioFile(unittest.TestCase):

    def setUp(self):
        self.test_data_dir = Path("C:/data/tests")
        self.mono_file = self.test_data_dir / "testWooWooMono16kHz32integerClipping9sec.wav"
        self.stereo_file = self.test_data_dir / "testSine2ch5sec.wav"
        self.non_audio_file = self.test_data_dir / "testVideo11sec.mkv"

    def test_read_mono_audio_file(self):
        waveform = readAudioFile(self.mono_file)
        self.assertIsInstance(waveform, numpy.ndarray)
        self.assertEqual(waveform.ndim, 1)  # Mono should have 1 dimension

    def test_read_stereo_audio_file(self):
        waveform = readAudioFile(self.stereo_file)
        self.assertIsInstance(waveform, numpy.ndarray)
        self.assertEqual(waveform.ndim, 2)  # Stereo should have 2 dimensions
        self.assertEqual(waveform.shape[0], 2)  # First dimension should be 2 for stereo

    def test_read_non_audio_file(self):
        with self.assertRaises(Exception):
            readAudioFile(self.non_audio_file)

if __name__ == "__main__":
    unittest.main()