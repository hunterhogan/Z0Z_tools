"""
A comprehensive toolkit for Python development and audio processing with modular, self-documenting solutions.

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

Parameter Validation and Type Handling
-------------------------------------
Robust functions for validating and converting parameter types:

- defineConcurrencyLimit: Intelligently determines CPU count for parallel processing.
  Example: cpuCount = defineConcurrencyLimit(0.5)  # Use 50% of available CPUs
           cpuCount = defineConcurrencyLimit(-2)   # Use all CPUs except 2
           cpuCount = defineConcurrencyLimit(8)    # Use exactly 8 CPUs

- intInnit: Rigorously validates and converts values to integers.
  Example: integers = intInnit(['1', '2.0', 3], 'my_parameter')

- oopsieKwargsie: Converts string representations to proper boolean or None values.
  Example: trueValue = oopsieKwargsie('True')  # Returns Python's True

Data Structure Utilities
-----------------------
Functions for manipulating complex data structures:

- stringItUp: Extracts string representations from nested data structures.
  Example: strings = stringItUp([1, {'a': 2}, {3, 4.5}])

- updateExtendPolishDictionaryLists: Merges dictionaries containing lists.
  Example: mergedDict = updateExtendPolishDictionaryLists(dict1, dict2, destroyDuplicates=True)

- autoDecodingRLE: Creates compact, self-decoding run-length encoded representations.
  Example: encoded = autoDecodingRLE(largeArray)

File System Operations
---------------------
Utilities for working with files and paths:

- findRelativePath: Computes platform-independent relative paths between locations.
  Example: relativePath = findRelativePath(sourceDir, targetDir)

- makeDirsSafely: Creates directory structures without raising errors.
  Example: makeDirsSafely('/path/to/new/directory')

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

Testing Support
--------------
Pre-built test suites for validating function behavior:

- PytestFor_defineConcurrencyLimit: Tests for concurrency limit calculation.
- PytestFor_intInnit: Tests for integer validation and conversion.
- PytestFor_oopsieKwargsie: Tests for string-to-boolean conversion.

Example:
  from Z0Z_tools import PytestFor_intInnit

  @pytest.mark.parametrize("nameOfTest,callablePytest",
                           PytestFor_intInnit(my_custom_function))
  def test_function(nameOfTest, callablePytest):
      callablePytest()
"""
try:
	from Z0Z_tools.optionalPyTorch import def_asTensor
	# `@def_asTensor` callables not recognized by Pylance https://github.com/hunterhogan/Z0Z_tools/issues/2
	from Z0Z_tools.windowingFunctions import halfsineTensor as halfsineTensor, tukeyTensor as tukeyTensor, cosineWingsTensor as cosineWingsTensor, equalPowerTensor as equalPowerTensor # type: ignore
except (ImportError, ModuleNotFoundError):
	from Z0Z_tools.optionalPyTorchAlternative import def_asTensor

from Z0Z_tools.scipyDOTsignalDOT_short_time_fft import PAD_TYPE, FFT_MODE_TYPE
from Z0Z_tools.theTypes import (
	ArraySpectrograms as ArraySpectrograms,
	ArrayType,
	ArrayWaveforms as ArrayWaveforms,
	NormalizationReverter as NormalizationReverter,
	ParametersShortTimeFFT,
	ParametersSTFT,
	ParametersUniversal,
	str_nameDOTname as str_nameDOTname,
	Spectrogram as Spectrogram,
	Waveform as Waveform,
	WaveformMetadata,
	WindowingFunction as WindowingFunction,
)

from Z0Z_tools.amplitude import normalizeWaveform as normalizeWaveform, normalizeArrayWaveforms as normalizeArrayWaveforms

from Z0Z_tools.autoRevert import moveToAxisOfOperation as moveToAxisOfOperation

from Z0Z_tools.windowingFunctions import halfsine as halfsine, tukey as tukey, cosineWings as cosineWings, equalPower as equalPower

from Z0Z_tools.filesystemToolkit import (
	dataTabularTOpathFilenameDelimited as dataTabularTOpathFilenameDelimited,
	findRelativePath as findRelativePath,
	makeDirsSafely as makeDirsSafely,
	writeStringToHere as writeStringToHere,
)

from Z0Z_tools.dataStructures import autoDecodingRLE as autoDecodingRLE, stringItUp as stringItUp, updateExtendPolishDictionaryLists as updateExtendPolishDictionaryLists

from Z0Z_tools.ioAudio import (
	loadSpectrograms as loadSpectrograms,
	loadWaveforms as loadWaveforms,
	readAudioFile as readAudioFile,
	resampleWaveform as resampleWaveform,
	spectrogramToWAV as spectrogramToWAV,
	stft as stft,
	waveformSpectrogramWaveform as waveformSpectrogramWaveform,
	writeWAV as writeWAV,
	)

from Z0Z_tools.parseParameters import (
	defineConcurrencyLimit as defineConcurrencyLimit,
	intInnit as intInnit,
	oopsieKwargsie as oopsieKwargsie
)

from Z0Z_tools.pipAnything import installPackageTarget as installPackageTarget, makeListRequirementsFromRequirementsFile as makeListRequirementsFromRequirementsFile

try:
	# NOTE `Pytest` is an optional dependency
	from Z0Z_tools.pytestForYourUse import (
		PytestFor_defineConcurrencyLimit as PytestFor_defineConcurrencyLimit,
		PytestFor_intInnit as PytestFor_intInnit,
		PytestFor_oopsieKwargsie as PytestFor_oopsieKwargsie,
		)
except (ImportError, ModuleNotFoundError):
	pass

"""
Semiotics:
WAV: is a file format. Don't use ambiguous: "Wav", "wav".
waveform: is a data concept.
windowing function: is the correct name for the array of numbers. Don't use ambiguous: "window" (diminutive form).
"""
