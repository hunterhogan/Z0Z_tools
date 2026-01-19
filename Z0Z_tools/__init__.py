"""A comprehensive toolkit for Python development and audio processing with modular, self-documenting solutions.

Z0Z_tools provides well-designed utilities that address common challenges in several domains:

Audio Processing
---------------
Functions for loading, manipulating, and saving audio data:

- readAudioFile: Reads audio files with automatic stereo conversion and sample rate control.
  Example: waveform = readAudioFile('input.wav', sampleRate=44100)

- writeWAV: Writes audio data to WAV files with consistent formatting.
  Example: writeWAV('output.wav', waveform, sampleRate=44100)

- loadWaveforms: Loads multiple audio files into a unified array for batch processing.
  Example: arrayWaveforms = loadWaveforms(['file1.wav', 'file2.wav'])

- loadSpectrograms: Converts multiple audio files into spectrograms for analysis.
  Example: arraySpectrograms, metadata = loadSpectrograms(['file1.wav', 'file2.wav'])

- resampleWaveform: Changes the sample rate of audio data.
  Example: waveformResampled = resampleWaveform(waveform, 48000, 44100)

- stft/istft: Performs Short-Time Fourier Transform and its inverse for frequency analysis.
  Example: spectrogram = stft(waveform)
           original = stft(spectrogram, inverse=True, lengthWaveform=length)

- spectrogramToWAV: Converts a spectrogram directly to a WAV file.
  Example: spectrogramToWAV(spectrogram, 'output.wav', lengthWaveform)

- waveformSpectrogramWaveform: Higher-order function for spectrogram-domain processing.
  Example: processor = waveformSpectrogramWaveform(mySpectrogramFilter)

- normalizeWaveform/normalizeArrayWaveforms: Normalizes audio amplitude with reversion capability.
  Example: waveformNormalized, revertFunction = normalizeWaveform(waveform)

Windowing Functions
------------------
Standard signal processing window functions for audio analysis:

- halfsine: Creates a half-sine (Hann) windowing function.
- tukey: Creates a Tukey (tapered cosine) windowing function.
- cosineWings: Creates a windowing function with cosine-tapered ends and flat center.
- equalPower: Creates an equal-power windowing function for crossfades.

File System Operations
---------------------
Utilities for working with files and paths:

- findRelativePath: Computes platform-independent relative paths between locations.
  Example: relativePath = findRelativePath(sourceDir, targetDir)

- dataTabularTOpathFilenameDelimited: Writes tabular data to delimited files.
  Example: dataTabularTOpathFilenameDelimited(data, 'output.csv', ',')

Package Installation Utilities
-----------------------------
Tools for installing packages from non-standard sources:

- installPackageTarget: Installs a Python package from a directory.
  Example: installPackageTarget('/path/to/package')

- makeListRequirementsFromRequirementsFile: Extracts valid requirements from files.
  Example: requirements = makeListRequirementsFromRequirementsFile('requirements.txt')

Array Manipulation
-----------------
Utilities for working with arrays:

- moveToAxisOfOperation: Context manager for temporarily moving array axes.
  Example: with moveToAxisOfOperation(array, 0, -1) as arrayModified:
               # Work with last axis as the operation axis

"""

# pyright: reportUnusedImport=false
# isort: split
from Z0Z_tools.scipyDOTsignalDOT_short_time_fft import FFT_MODE_TYPE, PAD_TYPE

# isort: split
from Z0Z_tools.theTypes import (
	ArraySpectrograms as ArraySpectrograms, ArrayType, ArrayWaveforms as ArrayWaveforms,
	NormalizationReverter as NormalizationReverter, ParametersShortTimeFFT, ParametersSTFT, ParametersUniversal,
	Spectrogram as Spectrogram, Waveform as Waveform, WaveformMetadata, WindowingFunction as WindowingFunction)

# isort: split
from Z0Z_tools.amplitude import (
	normalizeArrayWaveforms as normalizeArrayWaveforms, normalizeWaveform as normalizeWaveform)

# isort: split
from Z0Z_tools.autoRevert import moveToAxisOfOperation as moveToAxisOfOperation

# isort: split
from Z0Z_tools.windowingFunctions import (
	cosineWings as cosineWings, equalPower as equalPower, halfsine as halfsine, tukey as tukey)

# isort: split
import contextlib

with contextlib.suppress(ImportError, ModuleNotFoundError):
	from Z0Z_tools.optionalPyTorch import (
		cosineWingsTensor as cosineWingsTensor, equalPowerTensor as equalPowerTensor, halfsineTensor as halfsineTensor,
		tukeyTensor as tukeyTensor)

# isort: split
from Z0Z_tools.filesystemToolkit import (
	dataTabularTOpathFilenameDelimited as dataTabularTOpathFilenameDelimited, findRelativePath as findRelativePath)

# isort: split
from Z0Z_tools.ioAudio import (
	loadSpectrograms as loadSpectrograms, loadWaveforms as loadWaveforms, readAudioFile as readAudioFile,
	resampleWaveform as resampleWaveform, spectrogramToWAV as spectrogramToWAV, stft as stft,
	waveformSpectrogramWaveform as waveformSpectrogramWaveform, writeWAV as writeWAV)

"""
Semiotics:
WAV: is a file format. Don't use ambiguous: "Wav", "wav".
waveform: is a data concept.
windowing function: is the correct name for the array of numbers. Don't use ambiguous: "window" (diminutive form).
"""

