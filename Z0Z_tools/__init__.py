"""
A collection of utilities for audio processing, parameter validation, and data structure manipulation.

This package provides several modules with distinct functionality:

Audio Processing (ioAudio):
    - loadWaveforms: Load multiple audio files into a single array
    - readAudioFile: Read a single audio file with automatic stereo conversion
    - writeWav: Write audio data to WAV files
    Example:
        from Z0Z_tools import readAudioFile, writeWav
        waveform = readAudioFile('input.wav', sampleRate=44100)
        writeWav('output.wav', waveform)

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
        from Z0Z_tools.pytest_parseParameters import makeTestSuiteIntInnit
        dictionaryTests = makeTestSuiteIntInnit(my_integer_function)
"""

from Z0Z_tools.dataStructures import stringItUp, updateExtendPolishDictionaryLists
from Z0Z_tools.ioAudio import writeWav, readAudioFile, loadWaveforms
from Z0Z_tools.parseParameters import defineConcurrencyLimit, oopsieKwargsie, intInnit
from Z0Z_tools.pipAnything import installPackageTarget, makeListRequirementsFromRequirementsFile
from Z0Z_tools.Z0Z_io import dataTabularTOpathFilenameDelimited, findRelativePath

__all__ = [
    'dataTabularTOpathFilenameDelimited',
    'defineConcurrencyLimit',
    'findRelativePath',
    'installPackageTarget',
    'intInnit',
    'loadWaveforms',
    'makeListRequirementsFromRequirementsFile',
    'oopsieKwargsie',
    'readAudioFile',
    'stringItUp',
    'updateExtendPolishDictionaryLists',
    'writeWav',
]
