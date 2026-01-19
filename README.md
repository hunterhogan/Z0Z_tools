# Z0Z_tools

A comprehensive collection of Python utilities for developers and audio processing enthusiasts. "Z0Z_" indicates a prototype
package where individual components may eventually evolve into focused standalone packages or move to existing packages. Please
suggest a good home for the audio processing tools or any of the other functions.

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

### Install Packages Lacking Setup Files

Install unpackaged Python code with a simple command:

```bash
# From your terminal or command prompt
python -m Z0Z_tools.pipAnything /path/to/unpackaged/code
```

## Installation

```bash
pip install Z0Z_tools
```

## My recovery

[![Static Badge](https://img.shields.io/badge/2011_August-Homeless_since-blue?style=flat)](https://HunterThinks.com/support)
[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UC3Gx7kz61009NbhpRtPP7tw)](https://www.youtube.com/@HunterHogan)

## How to code

Coding One Step at a Time:

0. WRITE CODE.
1. Don't write stupid code that's hard to revise.
2. Write good code.
3. When revising, write better code.

[![CC-BY-NC-4.0](https://raw.githubusercontent.com/hunterhogan/Z0Z_tools/refs/heads/main/.github/CC-BY-NC-4.0.png)](https://creativecommons.org/licenses/by-nc/4.0/)
