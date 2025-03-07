"""
A collection of utilities for audio processing, parameter validation, and data structure manipulation.

This package provides several modules with distinct functionality:

Audio Processing (ioAudio):
	- loadWaveforms: Load multiple audio files into a single array
	- readAudioFile: Read a single audio file with automatic stereo conversion
	- writeWAV: Write audio data to WAV files
	Example:
		from Z0Z_tools import readAudioFile, writeWAV
		waveform = readAudioFile('input.wav', sampleRate=44100)
		writeWAV('output.wav', waveform)

Parameter Validation (parseParameters):
	- defineConcurrencyLimit: Smart CPU count management
	- intInnit: Robust integer list validation
	- oopsieKwargsie: String parameter interpretation
	Example:
		from Z0Z_tools import defineConcurrencyLimit, intInnit
		cpuCount = defineConcurrencyLimit(0.5)  # Use 50% of CPUs
		integers = intInnit(['1', '2.0', 3], 'my_parameter')

Data Structure Utilities (dataStructures):
	- stringItUp: Convert nested data structures to strings
	- updateExtendPolishDictionaryLists: Merge dictionary lists
	Example:
		from Z0Z_tools import stringItUp
		strings = stringItUp([1, {'a': 2}, {3, 4.5}])

File Operations (Z0Z_io):
	- findRelativePath: Compute relative paths between locations
	- dataTabularTOpathFilenameDelimited: Write tabular data to files

Package Installation (pipAnything):
	- installPackageTarget: Install packages from directories
	- makeListRequirementsFromRequirementsFile: Parse requirements files

Testing Support:
	Some functions come with ready-to-use test suites:
	```
	from Z0Z_tools.pytest_parseParameters import PytestFor_intInnit

	test_functions = PytestFor_intInnit(Z0Z_tools.intInnit)
	for nameOfTest, callablePytest in test_functions:
		callablePytest()  # Runs each test case
	```
"""
try:
	from Z0Z_tools.optionalPyTorch import def_asTensor
	# GitHub #2
	from Z0Z_tools.windowingFunctions import halfsineTensor, tukeyTensor, cosineWingsTensor, equalPowerTensor # type: ignore
except (ImportError, ModuleNotFoundError):
	from Z0Z_tools.optionalPyTorchAlternative import def_asTensor

from Z0Z_tools.scipyDOTsignalDOT_short_time_fft import PAD_TYPE, FFT_MODE_TYPE
from Z0Z_tools.theTypes import *

from Z0Z_tools.amplitude import *

from Z0Z_tools.autoRevert import *
from Z0Z_tools.windowingFunctions import *
from Z0Z_tools.Z0Z_io import *
from Z0Z_tools.clippingArrays import *
from Z0Z_tools.dataStructures import *
from Z0Z_tools.ioAudio import *
from Z0Z_tools.parseParameters import *
from Z0Z_tools.pipAnything import *

try:
	# NOTE `Pytest` is an optional dependency
	from Z0Z_tools.pytestForYourUse import *
except (ImportError, ModuleNotFoundError):
	pass

"""
Semiotics:
WAV: is a file format. Don't use ambiguous: "Wav", "wav".
waveform: is a data concept.
windowing function: is the correct name for the array of numbers. Don't use ambiguous: "window" (diminutive form).
"""
