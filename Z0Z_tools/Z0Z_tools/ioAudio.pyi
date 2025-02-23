import io
import os
from Z0Z_tools import halfsine as halfsine, makeDirsSafely as makeDirsSafely
from _typeshed import Incomplete
from collections.abc import Sequence
from numpy import complex64 as complex64, complexfloating, dtype, float32, floating, integer, ndarray
from numpy.typing import NDArray as NDArray
from scipy.signal._short_time_fft import FFT_MODE_TYPE as FFT_MODE_TYPE, PAD_TYPE as PAD_TYPE
from typing import Any, BinaryIO, Literal, TypedDict, overload

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
    windowingFunction: ndarray[tuple[int], dtype[floating[Any]]]

class WaveformMetadata(TypedDict):
    pathFilename: str
    lengthWaveform: int
    samplesLeading: int
    samplesTrailing: int

parametersShortTimeFFTUniversal: ParametersShortTimeFFT
parametersSTFTUniversal: ParametersSTFT
lengthWindowingFunctionDEFAULT: int
windowingFunctionCallableDEFAULT = halfsine
parametersDEFAULT: Incomplete
setParametersUniversal: Incomplete
windowingFunctionCallableUniversal = windowingFunctionCallableDEFAULT
parametersUniversal: ParametersUniversal

def getWaveformMetadata(listPathFilenames: Sequence[str | os.PathLike[str]], sampleRate: float) -> dict[int, WaveformMetadata]: ...
def readAudioFile(pathFilename: str | os.PathLike[Any] | BinaryIO, sampleRate: float | None = None) -> ndarray[tuple[Literal[2], int], dtype[float32]]: ...
def resampleWaveform(waveform: NDArray[floating[Any]], sampleRateDesired: float, sampleRateSource: float, axisTime: int = -1) -> NDArray[float32]: ...
def loadWaveforms(listPathFilenames: Sequence[str | os.PathLike[str]], sampleRateTarget: float | None = None) -> ndarray[tuple[int, int, int], dtype[float32]]: ...
def writeWAV(pathFilename: str | os.PathLike[Any] | io.IOBase, waveform: ndarray[tuple[int, ...], dtype[floating[Any] | integer[Any]]], sampleRate: float | None = None) -> None: ...
@overload
def stft(arrayTarget: ndarray[tuple[int, int], dtype[floating[Any] | integer[Any]]], *, sampleRate: float | None = None, lengthHop: int | None = None, windowingFunction: ndarray[tuple[int], dtype[floating[Any]]] | None = None, lengthWindowingFunction: int | None = None, lengthFFT: int | None = None, inverse: Literal[False] = False, lengthWaveform: None = None, indexingAxis: Literal[None] = None) -> ndarray[tuple[int, int, int], dtype[complexfloating[Any, Any]]]: ...
@overload
def stft(arrayTarget: ndarray[tuple[int, int, int], dtype[floating[Any] | integer[Any]]], *, sampleRate: float | None = None, lengthHop: int | None = None, windowingFunction: ndarray[tuple[int], dtype[floating[Any]]] | None = None, lengthWindowingFunction: int | None = None, lengthFFT: int | None = None, inverse: Literal[False] = False, lengthWaveform: None = None, indexingAxis: int = -1) -> ndarray[tuple[int, int, int, int], dtype[complexfloating[Any, Any]]]: ...
@overload
def stft(arrayTarget: ndarray[tuple[int, int, int], dtype[complexfloating[Any, Any] | floating[Any]]], *, sampleRate: float | None = None, lengthHop: int | None = None, windowingFunction: ndarray[tuple[int], dtype[floating[Any]]] | None = None, lengthWindowingFunction: int | None = None, lengthFFT: int | None = None, inverse: Literal[True], lengthWaveform: int, indexingAxis: Literal[None] = None) -> ndarray[tuple[int, int], dtype[floating[Any]]]: ...
@overload
def stft(arrayTarget: ndarray[tuple[int, int, int, int], dtype[complexfloating[Any, Any]]], *, sampleRate: float | None = None, lengthHop: int | None = None, windowingFunction: ndarray[tuple[int], dtype[floating[Any]]] | None = None, lengthWindowingFunction: int | None = None, lengthFFT: int | None = None, inverse: Literal[True], lengthWaveform: int, indexingAxis: int = -1) -> ndarray[tuple[int, int, int], dtype[floating[Any]]]: ...
def loadSpectrograms(listPathFilenames: Sequence[str | os.PathLike[str]], sampleRateTarget: float | None = None, **parametersSTFT: Any) -> tuple[ndarray[tuple[int, int, int, int], dtype[complex64]], dict[int, WaveformMetadata]]: ...
def spectrogramToWAV(spectrogram: ndarray[tuple[int, int, int], dtype[complexfloating[Any, Any] | floating[Any]]], pathFilename: str | os.PathLike[Any] | io.IOBase, lengthWaveform: int, sampleRate: float | None = None, **parametersSTFT: Any) -> None: ...
def waveformSpectrogramWaveform(callableNeedsSpectrogram): ...
