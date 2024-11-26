from Z0Z_tools import readAudioFile, loadWaveforms, writeWav
from Z0Z_tools.Z0Z_ioAudio import resampleWaveform
from numpy.typing import NDArray
import numpy
import pathlib 
import soundfile
import unittest
import tempfile
import os


class TestReadAudioFile(unittest.TestCase):

    def setUp(self):
        self.test_data_dir = pathlib.Path("unittests/dataSamples")
        self.mono_file = self.test_data_dir / "testWooWooMono16kHz32integerClipping9sec.wav"
        self.stereo_file = self.test_data_dir / "testSine2ch5sec.wav"
        self.non_audio_file = self.test_data_dir / "testVideo11sec.mkv"  #Assuming this file exists for the test.

    def test_read_mono_audio_file(self):
        waveform = readAudioFile(self.mono_file)
        self.assertIsInstance(waveform, numpy.ndarray)
        self.assertEqual(waveform.ndim, 2)  # Mono should be converted to stereo, hence 2 dimensions
        self.assertEqual(waveform.shape[0], 2) # Verify stereo output

    def test_read_stereo_audio_file(self):
        waveform = readAudioFile(self.stereo_file)
        self.assertIsInstance(waveform, numpy.ndarray)
        self.assertEqual(waveform.ndim, 2)
        self.assertEqual(waveform.shape[0], 2)

    def test_read_audio_file_resampling(self):
        waveform_original_sr = readAudioFile(self.mono_file, sampleRate=16000) # Original Sample Rate
        waveform_resampled_sr = readAudioFile(self.mono_file, sampleRate=44100) # Resampled
        self.assertNotEqual(waveform_original_sr.shape[1], waveform_resampled_sr.shape[1])


    def test_invalid_file(self):
        with self.assertRaises(FileNotFoundError): # Or appropriate exception from soundfile library
            readAudioFile("nonexistent_file.wav")
        with self.assertRaises(soundfile.LibsndfileError): # Or a more specific exception type
            readAudioFile(self.non_audio_file)


class TestLoadWaveforms(unittest.TestCase):

    def setUp(self):
        self.test_data_dir = pathlib.Path("unittests/dataSamples")
        self.mono_files = [self.test_data_dir / f"testWooWooMono16kHz32integerClipping9secCopy{i}.wav" for i in range(1,4)]
        self.stereo_files = [self.test_data_dir / f"testSine2ch5secCopy{i}.wav" for i in range(1,5)]


    def test_load_waveforms_mono(self):
        array_waveforms = loadWaveforms(self.mono_files, sampleRate=44100)
        self.assertEqual(array_waveforms.shape, (2, 396900, 3))

    def test_load_waveforms_stereo(self):
        array_waveforms = loadWaveforms(self.stereo_files, sampleRate=44100)
        self.assertEqual(array_waveforms.shape, (2, 220500, 4))

    def test_load_waveforms_mixed_channels(self):
        mixed_files = self.mono_files[:1] + self.stereo_files[:1]
        array_waveforms = loadWaveforms(mixed_files, sampleRate=44100)
        self.assertEqual(array_waveforms.shape, (2, 396900, 2))

    def test_load_waveforms_empty_list(self):
        with self.assertRaises(ValueError): # Or a more appropriate exception
            loadWaveforms([])

    def test_load_waveforms_invalid_file(self):
        invalid_files = self.mono_files + ["invalid_file.wav"]
        with self.assertRaises(FileNotFoundError) as context: # Or a more specific exception
            loadWaveforms(invalid_files) # type: ignore
        # Optionally check the error message for more precise testing
class TestResampleWaveform(unittest.TestCase):

    def setUp(self):
        pathDirectoryTestData: pathlib.Path = pathlib.Path("unittests/dataSamples")
        self.pathFilenameMono: pathlib.Path = pathDirectoryTestData / "testWooWooMono16kHz32integerClipping9sec.wav"
        self.pathFilenameStereo: pathlib.Path = pathDirectoryTestData / "testSine2ch5sec.wav"

        # Load real audio files
        self.arrayWaveformMono: NDArray[numpy.float32]
        self.sampleRateMono: int
        self.arrayWaveformMono, self.sampleRateMono = soundfile.read(self.pathFilenameMono, dtype='float32') # type: ignore
        self.arrayWaveformMono = self.arrayWaveformMono.astype(numpy.float32)

        self.arrayWaveformStereo: NDArray[numpy.float32]
        self.sampleRateStereo: int
        self.arrayWaveformStereo, self.sampleRateStereo = soundfile.read(self.pathFilenameStereo, dtype='float32') # type: ignore
        self.arrayWaveformStereo = self.arrayWaveformStereo.astype(numpy.float32)

    def testResampleWaveformUpsampleMono(self):
        """
        Test resampling a mono waveform from a lower sample rate to a higher sample rate.
        """
        sampleRateDesired: int = 44100
        arrayWaveformResampled: NDArray[numpy.float32] = resampleWaveform(
            waveform=self.arrayWaveformMono,
            sampleRateDesired=sampleRateDesired,
            sampleRateSource=self.sampleRateMono
        )
        countSamplesExpected: int = int(self.arrayWaveformMono.shape[0] * (sampleRateDesired / self.sampleRateMono))
        self.assertEqual(arrayWaveformResampled.shape[0], countSamplesExpected)

    def testResampleWaveformDownsampleStereo(self):
        """
        Test resampling a stereo waveform from a higher sample rate to a lower sample rate.
        """
        sampleRateDesired: int = 22050
        arrayWaveformResampled: NDArray[numpy.float32] = resampleWaveform(
            waveform=self.arrayWaveformStereo,
            sampleRateDesired=sampleRateDesired,
            sampleRateSource=self.sampleRateStereo
        )
        countSamplesExpected: int = int(self.arrayWaveformStereo.shape[0] * (sampleRateDesired / self.sampleRateStereo))
        self.assertEqual(arrayWaveformResampled.shape[0], countSamplesExpected)

    def testResampleWaveformEqualSampleRate(self):
        """
        Test that the waveform is unchanged if sample rates are equal.
        """
        arrayWaveformResampled: NDArray[numpy.float32] = resampleWaveform(
            waveform=self.arrayWaveformStereo,
            sampleRateDesired=self.sampleRateStereo,
            sampleRateSource=self.sampleRateStereo
        )
        self.assertTrue(numpy.array_equal(arrayWaveformResampled, self.arrayWaveformStereo))

    def testResampleWaveformInvalidInput(self):
        """
        Test resampling with invalid input types.
        """
        with self.assertRaises(AttributeError):
            resampleWaveform('invalidInput', 44100, 22050) # type: ignore

    def testResampleWaveformNegativeSampleRate(self):
        """
        Test resampling with a negative sample rate.
        """
        with self.assertRaises(ValueError):
            resampleWaveform(self.arrayWaveformStereo, -44100, self.sampleRateStereo)
class TestWriteWav(unittest.TestCase):
    def test_write_wav_mono(self):
        waveform = numpy.random.rand(1, 1000)  #Example mono waveform
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            filepath = temp_file.name
            writeWav(filepath, waveform)
            self.assertTrue(os.path.exists(filepath))
            # Add assertions to check file content if necessary (using soundfile to read it back)

    def test_write_wav_stereo(self):
        waveform = numpy.random.rand(2, 1000) #Example stereo waveform
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            filepath = temp_file.name
            writeWav(filepath, waveform)
            self.assertTrue(os.path.exists(filepath))
            # Add assertions to check file content

    def test_write_wav_directory_creation(self):
        waveform = numpy.random.rand(2,1000)
        temp_dir = tempfile.mkdtemp()
        filepath = os.path.join(temp_dir, "test.wav")
        writeWav(filepath, waveform)
        self.assertTrue(os.path.exists(filepath))


if __name__ == "__main__":
    unittest.main()
