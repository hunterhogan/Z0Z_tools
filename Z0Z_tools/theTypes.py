"""Type definitions for audio signal processing and waveform analysis.

(AI generated docstring)

This module defines type aliases and typed dictionaries for NumPy arrays,
waveforms, spectrograms, and parameter structures used throughout the audio
signal processing library.

"""
from collections.abc import Callable
from numpy import complexfloating, dtype, floating, ndarray
from typing import Any, Literal, TypeAlias, TypedDict, TypeVar
from Z0Z_tools import FFT_MODE_TYPE, PAD_TYPE

ArrayType = TypeVar('ArrayType', bound=ndarray[Any, Any], covariant=True)
WindowingFunctionDtype: TypeAlias = floating[Any]
WindowingFunction: TypeAlias = ndarray[tuple[int], dtype[WindowingFunctionDtype]]
WaveformDtype: TypeAlias = floating[Any]
Waveform: TypeAlias = ndarray[tuple[int, int], dtype[WaveformDtype]]
"""Two-dimensional NumPy `ndarray` representing audio waveforms.

A NumPy `ndarray` of audio waveform data with shape (channels, samples). For mono audio, `channels` = 1.

"""

ArrayWaveforms: TypeAlias = ndarray[tuple[int, int, int], dtype[WaveformDtype]]
"""Three-dimensional NumPy `ndarray` representing multiple waveforms.

A NumPy `ndarray` containing `ndarray` of type `Waveform` indexed on the last axis: shape is (channels, samples, `Waveform`).

"""

SpectrogramDtype: TypeAlias = complexfloating[Any, Any]
Spectrogram: TypeAlias = ndarray[tuple[int, int, int], dtype[SpectrogramDtype]]
"""Three-dimensional `ndarray` representing a spectrogram.

A NumPy `ndarray` of spectrogram data with shape (channels, frequency_bins, time_frames). For mono audio, `channels` = 1.

"""

ArraySpectrograms: TypeAlias = ndarray[tuple[int, int, int, int], dtype[SpectrogramDtype]]
"""Four-dimensional NumPy `ndarray` representing multiple spectrograms.

A NumPy `ndarray` containing `ndarray` of type `Spectrogram` indexed on the last axis: shape is (channels, frequency_bins, time_frames, `Spectrogram`).

"""

class ParametersSTFT(TypedDict, total=False):
	"""Optional parameters for Short-Time Fourier Transform operations.

	(AI generated docstring)

	TypedDict defining optional configuration parameters for STFT computations.
	All fields are optional due to `total=False`.

	"""

	padding: PAD_TYPE
	axis: int

class ParametersShortTimeFFT(TypedDict, total=False):
	"""Optional parameters for Short-Time FFT operations.

	(AI generated docstring)

	TypedDict defining optional configuration parameters for short-time FFT.
	All fields are optional due to `total=False`.

	"""

	fft_mode: FFT_MODE_TYPE
	scale_to: Literal['magnitude', 'psd']

class ParametersUniversal(TypedDict):
	"""Required parameters for universal audio processing operations.

	(AI generated docstring)

	TypedDict defining required configuration parameters used across multiple
	audio processing functions. All fields must be provided.

	"""

	lengthFFT: int
	lengthHop: int
	lengthWindowingFunction: int
	sampleRate: float
	windowingFunction: WindowingFunction

class WaveformMetadata(TypedDict):
	"""Metadata describing waveform file properties and processing state.

	(AI generated docstring)

	TypedDict containing information about a waveform's source file and
	any padding or trimming applied during processing.

	"""

	pathFilename: str
	lengthWaveform: int
	samplesLeading: int
	samplesTrailing: int

NormalizationReverter: TypeAlias = Callable[[Waveform], Waveform]
"""Function type for reversing normalization operations.

(AI generated docstring)

Type alias for callable objects that accept a normalized waveform and
return the waveform restored to its original amplitude scale.

"""

identifierDotAttribute: TypeAlias = str
"""String representing a dotted attribute identifier.

Type alias for strings containing object attribute paths using dot notation,
such as 'scipy.signal.windows' for dynamic attribute access.

"""
