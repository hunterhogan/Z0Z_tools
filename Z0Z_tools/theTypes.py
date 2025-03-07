from collections.abc import Callable
from numpy import complexfloating, dtype, floating, ndarray
from typing import Any, Literal, TypedDict, TypeAlias
from Z0Z_tools import PAD_TYPE, FFT_MODE_TYPE

WindowingFunctionDtype: TypeAlias = floating[Any]
WindowingFunction: TypeAlias = ndarray[tuple[int], dtype[WindowingFunctionDtype]]

WaveformDtype: TypeAlias = floating[Any]
Waveform: TypeAlias = ndarray[tuple[int, int], dtype[WaveformDtype]]
ArrayWaveforms: TypeAlias = ndarray[tuple[int, int, int], dtype[WaveformDtype]]

SpectrogramDtype: TypeAlias = complexfloating[Any, Any]
Spectrogram: TypeAlias = ndarray[tuple[int, int, int], dtype[SpectrogramDtype]]
ArraySpectrograms: TypeAlias = ndarray[tuple[int, int, int, int], dtype[SpectrogramDtype]]

class ParametersSTFT(TypedDict, total=False):
	padding: PAD_TYPE
	axis: int

class ParametersShortTimeFFT(TypedDict, total=False):
	fft_mode: FFT_MODE_TYPE
	scale_to: Literal['magnitude', 'psd']

class ParametersUniversal(TypedDict):
	lengthFFT: int
	lengthHop: int
	lengthWindowingFunction: int
	sampleRate: float
	windowingFunction: WindowingFunction

class WaveformMetadata(TypedDict):
	pathFilename: str
	lengthWaveform: int
	samplesLeading: int
	samplesTrailing: int

NormalizationReverter: TypeAlias = Callable[[Waveform], Waveform]
