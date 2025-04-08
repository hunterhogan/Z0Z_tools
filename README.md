# Z0Z_tools

A comprehensive collection of Python utilities for developers and audio processing enthusiasts. "Z0Z_" indicates a prototype package where individual components may eventually evolve into focused standalone packages.

## Why Choose Z0Z_tools?

Z0Z_tools solves common development challenges with clean, well-documented functions that emphasize self-explanatory code and robust error handling.

## Parameter Validation and Type Handling

### Simplify Boolean Parameter Handling

Convert string representations like "TRUE" or "false" to proper Python boolean values:

```python
from Z0Z_tools import oopsieKwargsie

def my_function(verbose="true"):
    # Converts "true", "True", "TRUE", etc. to Python's True
    is_verbose = oopsieKwargsie(verbose)
    if is_verbose:
        print("Detailed information follows...")
```

### Control Parallel Processing Intelligently

Fine-tune CPU usage with intuitive syntax:

```python
from Z0Z_tools import defineConcurrencyLimit

# Use 75% of available CPUs
workers = defineConcurrencyLimit(0.75)

# Use all CPUs except 2
workers = defineConcurrencyLimit(-2)

# Use exactly 8 CPUs
workers = defineConcurrencyLimit(8)
```

### Validate Integer Inputs Robustly

Convert and validate inputs to integers with clear error messages:

```python
from Z0Z_tools import intInnit

# Handles mixed input types with precise validation
validated_ids = intInnit(['1', 2, '3.0'], 'user_ids')

# Rejects non-integer values with helpful errors
try:
    intInnit([1.5, '2'], 'dimensions')
except ValueError as e:
    print(e)  # "I received 1.5, but dimensions must be an integer number."
```

## Data Structure Utilities

### Extract Data as Strings from Complex Structures

Recursively extract and convert values from nested data structures:

```python
from Z0Z_tools import stringItUp

mixed_data = [1, {'user': 'Alice'}, {3.14, 'math'}, b'bytes']
strings = stringItUp(mixed_data)  # ['1', 'user', 'Alice', '3.14', 'math', 'bytes']
```

### Merge Dictionary Lists with Flexible Options

Combine and clean dictionary data with control over duplicates and ordering:

```python
from Z0Z_tools import updateExtendPolishDictionaryLists

dict1 = {'colors': ['red', 'blue'], 'sizes': [1, 2]}
dict2 = {'colors': ['blue', 'green'], 'materials': ['wood']}

# Merge with duplicate removal and sorting
merged = updateExtendPolishDictionaryLists(
    dict1, dict2,
    destroyDuplicates=True,
    reorderLists=True
)
# Result: {'colors': ['blue', 'green', 'red'], 'sizes': [1, 2], 'materials': ['wood']}
```

### Create Compact, Self-Decoding Run-Length Encodings

Generate efficient string representations of large arrays:

```python
from Z0Z_tools import autoDecodingRLE
import numpy as np

array = np.array([1, 2, 3, 3, 3, 4, 5, 6])
encoded = autoDecodingRLE(array)  # '[1,2,[3]*3,4,5,6]'

# The string can be evaluated directly to recreate the data
import ast
decoded = ast.literal_eval(encoded)  # [1, 2, 3, 3, 3, 4, 5, 6]
```

## Audio Processing Made Simple

### Load and Save Audio Files

Read audio files with automatic stereo conversion and sample rate control:

```python
from Z0Z_tools import readAudioFile, writeWAV

# Load audio with sample rate conversion
waveform = readAudioFile('input.wav', sampleRate=44100)

# Save in WAV format (always 32-bit float)
writeWAV('output.wav', waveform)
```

### Process Multiple Audio Files at Once

Load and process batches of audio files:

```python
from Z0Z_tools import loadWaveforms

# Load multiple files with consistent formatting
array_waveforms = loadWaveforms(['file1.wav', 'file2.wav', 'file3.wav'])

# The result is a unified array with shape (channels, samples, file_count)
```

### Work with Spectrograms

Convert between waveforms and spectrograms:

```python
from Z0Z_tools import stft, halfsine

# Create a spectrogram with a half-sine window
spectrogram = stft(waveform, windowingFunction=halfsine(1024))

# Convert back to a waveform
reconstructed = stft(spectrogram, inverse=True, lengthWaveform=original_length)
```

### Process Audio in the Frequency Domain

Create functions that operate on spectrograms:

```python
from Z0Z_tools import waveformSpectrogramWaveform

def boost_low_frequencies(spectrogram):
    # Boost frequencies below 500 Hz
    spectrogram[:, :10, :] *= 2.0
    return spectrogram

# Create a processor that handles the STFT/ISTFT automatically
processor = waveformSpectrogramWaveform(boost_low_frequencies)

# Apply the processor to a waveform
processed_waveform = processor(original_waveform)
```

## File System Utilities

### Create Relative Paths Between Any Locations

Generate platform-independent relative paths:

```python
from Z0Z_tools import findRelativePath

# Works with files or directories on different branches
rel_path = findRelativePath('/path/to/source', '/path/to/different/target')
# Result: '../../different/target'
```

### Install Packages Lacking Setup Files

Install unpackaged Python code with a simple command:

```bash
# From your terminal or command prompt
python -m Z0Z_tools.pipAnything /path/to/unpackaged/code
```

## Testing Utilities

### Pre-Built Test Suites for Common Functions

Validate your implementations with ready-to-use test suites:

```python
from Z0Z_tools import PytestFor_intInnit
import pytest

# Test your custom integer validation function
@pytest.mark.parametrize("test_name,test_func",
                         PytestFor_intInnit(your_integer_validator))
def test_validator(test_name, test_func):
    test_func()  # Runs a comprehensive test suite
```

## Installation

```bash
pip install Z0Z_tools
```

## License

[![CC-BY-NC-4.0](https://github.com/hunterhogan/Z0Z_tools/blob/main/CC-BY-NC-4.0.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
