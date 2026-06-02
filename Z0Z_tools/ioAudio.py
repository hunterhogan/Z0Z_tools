"""Read, write, resample, and transform audio waveforms between time and frequency domains.

You can use this module to load audio files into NumPy arrays, resample waveforms, convert
between waveforms and spectrograms using the Short-Time Fourier Transform, and write
waveforms back to WAV files. All audio is normalized to stereo, 32-bit float `Waveform`
arrays shaped `(channels, samples)`. All spectrograms are complex 64-bit float
`Spectrogram` arrays shaped `(channels, frequencies, frames)`.

Contents
--------
Functions
    getWaveformMetadata
        Retrieve metadata for a collection of audio waveform files.
    loadSpectrograms
        Load spectrograms from a list of audio files.
    loadWaveforms
        Load a list of audio files into a single stacked NumPy array.
    readAudioFile
        Read an audio file and return stereo waveform data as a NumPy array.
    resampleWaveform
        Resample a waveform array to a target sample rate.
    spectrogramToWAV
        Write a complex spectrogram to a WAV file.
    stft
        Perform Short-Time Fourier Transform or its inverse on waveform or spectrogram data.
    waveformSpectrogramWaveform
        Decorate a spectrogram-processing callable to accept and return waveforms.
    writeWAV
        Write a waveform array to a WAV file.

"""
from __future__ import annotations

from hunterMakesPy.filesystemToolkit import makeDirsSafely
from math import ceil as ceiling, log2 as log_base2
from multiprocessing import set_start_method as multiprocessing_set_start_method
from numpy import complex64, dtype, float32, floating, ndarray
from scipy.signal import ShortTimeFFT
from tqdm.auto import tqdm
from typing import Any, BinaryIO, cast, Literal, overload, TYPE_CHECKING
from Z0Z_tools import (
	ArraySpectrograms, ArrayWaveforms, halfsine, ParametersShortTimeFFT, ParametersSTFT, ParametersUniversal, Spectrogram, Waveform,
	WaveformMetadata, WindowingFunction)
import numpy
import resampy
import soundfile

if TYPE_CHECKING:
	from collections.abc import Callable, Sequence
	from os import PathLike

# When to use multiprocessing.set_start_method https://github.com/hunterhogan/mapFolding/issues/6
if __name__ == '__main__':
	multiprocessing_set_start_method('spawn')

# Design coordinated, user-overridable universal parameter defaults for audio functions
# https://github.com/hunterhogan/Z0Z_tools/issues/5
universalDtypeWaveform = float32
"""Module-wide NumPy dtype for waveform arrays; controls memory layout and numeric precision."""
universalDtypeSpectrogram = complex64
"""Module-wide NumPy dtype for spectrogram arrays; complex 64-bit float balances precision and memory."""
parametersShortTimeFFTUniversal: ParametersShortTimeFFT = {'fft_mode': 'onesided'}
"""Module-wide keyword parameters passed to `scipy.signal.ShortTimeFFT` on construction."""
parametersSTFTUniversal: ParametersSTFT = {'padding': 'even', 'axis': -1}
"""Module-wide keyword parameters passed to `ShortTimeFFT.stft` and `ShortTimeFFT.istft` on each call."""

lengthWindowingFunctionDEFAULT = 1024
"""Default length in samples of the windowing function used when no override is provided."""
windowingFunctionCallableDEFAULT = halfsine
"""Default callable that constructs a `WindowingFunction` array from a length in samples."""
parametersDEFAULT = ParametersUniversal(
	lengthFFT=2048,
	lengthHop=512,
	lengthWindowingFunction=lengthWindowingFunctionDEFAULT,
	sampleRate=44100,
	windowingFunction=windowingFunctionCallableDEFAULT(lengthWindowingFunctionDEFAULT),
)
"""Factory `ParametersUniversal` applied when `setParametersUniversal` is `None`."""

setParametersUniversal = None
"""Override `ParametersUniversal` for all module functions; when `None`, `parametersDEFAULT` is used."""

windowingFunctionCallableUniversal = windowingFunctionCallableDEFAULT
"""Active callable for constructing windowing functions; overridable at module level."""
if not setParametersUniversal:
	parametersUniversal: ParametersUniversal = parametersDEFAULT
	"""Active `ParametersUniversal` used by all functions when no per-call override is provided."""

def getWaveformMetadata(listPathFilenames: Sequence[str | PathLike[str]], sampleRate: float) -> dict[int, WaveformMetadata]:
	"""Retrieve metadata for a collection of audio waveform files.

	You can use this function to inspect the length of each audio file before loading
	waveforms into memory. `getWaveformMetadata` reads each file at `sampleRate`, measures
	the sample count, and returns one `WaveformMetadata` [1] record per file indexed by
	position in `listPathFilenames`. Each record's `samplesLeading` and `samplesTrailing`
	fields are initialized to `0`; callers may adjust them before passing the result to
	downstream loaders such as `loadWaveforms` or `loadSpectrograms`.

	Parameters
	----------
	listPathFilenames : Sequence[str | PathLike[str]]
		Sequence of paths to audio files.
	sampleRate : float
		Target sample rate used when reading each file to measure its length in samples.

	Returns
	-------
	dictionaryWaveformMetadata : dict[int, WaveformMetadata]
		Dictionary mapping each integer index to a `WaveformMetadata` [1] record. Each
		record contains `pathFilename` (string path), `lengthWaveform` (sample count at
		`sampleRate`), `samplesLeading` (initialized to `0`), and `samplesTrailing`
		(initialized to `0`).

	File Reading Progress
	---------------------
	`tqdm` [2] displays a progress bar in the terminal while `getWaveformMetadata` reads
	each file in `listPathFilenames`.

	References
	----------
	[1] `WaveformMetadata`

	[2] tqdm — fast, extensible progress bar for Python and CLI
		https://tqdm.github.io/

	"""
	axisTime: int = -1
	dictionaryWaveformMetadata: dict[int, WaveformMetadata] = {}
	for index, pathFilename in enumerate(tqdm(listPathFilenames)):
		lengthWaveform = readAudioFile(pathFilename, sampleRate).shape[axisTime]
		dictionaryWaveformMetadata[index] = WaveformMetadata(
			pathFilename=str(pathFilename),
			lengthWaveform=lengthWaveform,
			samplesLeading=0,
			samplesTrailing=0,
		)
	return dictionaryWaveformMetadata

def readAudioFile(pathFilename: str | PathLike[Any] | BinaryIO, sampleRate: float | None = None) -> Waveform:
	"""Read an audio file and return stereo waveform data as a NumPy array.

	You can use this function to load any audio file that `soundfile` [1] supports. The
	returned `Waveform` [2] is always shaped `(channels, samples)` where `channels` is `2`.
	When the source file is mono, `readAudioFile` duplicates the single channel to produce
	a stereo array. When `sampleRate` differs from the file's native sample rate,
	`readAudioFile` resamples using `resampleWaveform`.

	Parameters
	----------
	pathFilename : str | PathLike[Any] | BinaryIO
		Path to the audio file or a binary stream compatible with `soundfile` [1].
	sampleRate : float | None = None
		Target sample rate of the returned `Waveform` [2] in Hz. Defaults to `44100`
		when `None`.

	Returns
	-------
	waveform : Waveform
		Stereo audio data shaped `(2, samples)` as `float32`.

	Raises
	------
	FileNotFoundError
		When `pathFilename` does not exist on the filesystem.
	soundfile.LibsndfileError
		When `pathFilename` is an unsupported or corrupted audio format.

	References
	----------
	[1] soundfile — audio library based on libsndfile
		https://python-soundfile.readthedocs.io/en/0.12.1/

	[2] `Waveform`

	"""
	if sampleRate is None:
		sampleRate = parametersUniversal['sampleRate']
	try:
		with soundfile.SoundFile(str(pathFilename)) as readSoundFile:
			sampleRateSource: int = readSoundFile.samplerate
			waveform: Waveform = readSoundFile.read(dtype='float32', always_2d=True).astype(universalDtypeWaveform)
	except soundfile.LibsndfileError as ERRORmessage:
		if 'System error' in str(ERRORmessage):
			message = f"File not found: {pathFilename}"
			raise FileNotFoundError(message) from ERRORmessage
		else:  # noqa: RET506
			raise
	# GitHub #3 Implement semantic axes for audio data
	axisTime = 0
	axisChannels = 1
	waveform = cast('Waveform', resampleWaveform(waveform, sampleRateDesired=sampleRate, sampleRateSource=sampleRateSource, axisTime=axisTime))
	if waveform.shape[axisChannels] == 1:
		waveform = cast('Waveform', numpy.repeat(waveform, 2, axis=axisChannels))
	return cast('Waveform', numpy.transpose(waveform, axes=(axisChannels, axisTime)))

def resampleWaveform(waveform: ndarray[tuple[int, ...], dtype[floating[Any]]], sampleRateDesired: float, sampleRateSource: float, axisTime: int = -1) -> ndarray[tuple[int, ...], dtype[floating[Any]]]:
	"""Resample a waveform array to a target sample rate using `resampy` [1].

	You can use this function to change the sample rate of any floating-point NumPy array [2].
	`resampleWaveform` passes `waveform` to `resampy.resample` [1] along the `axisTime` axis.
	When `sampleRateSource` equals `sampleRateDesired`, `resampleWaveform` returns `waveform`
	unchanged without invoking `resampy`.

	Parameters
	----------
	waveform : ndarray[tuple[int, ...], dtype[floating[Any]]]
		Input audio data as any floating-point NumPy array [2].
	sampleRateDesired : float
		Target sample rate in Hz.
	sampleRateSource : float
		Original sample rate of `waveform` in Hz.
	axisTime : int = -1
		Axis along which resampling is performed. Negative values index from the last axis.

	Returns
	-------
	waveformResampled : ndarray[tuple[int, ...], dtype[floating[Any]]]
		Waveform resampled to `sampleRateDesired`. Returns `waveform` unchanged when
		`sampleRateSource` equals `sampleRateDesired`.

	Sample Rate Rounding
	--------------------
	Both `sampleRateDesired` and `sampleRateSource` are rounded to the nearest integer
	before passing to `resampy.resample` [1]. `resampy` expects integer sample rates.

	References
	----------
	[1] resampy — efficient signal resampling
		https://resampy.readthedocs.io/en/stable/

	[2] numpy.ndarray
		https://numpy.org/doc/stable/reference/index.html

	"""
	if sampleRateSource != sampleRateDesired:
		sampleRateDesired = round(sampleRateDesired)
		sampleRateSource = round(sampleRateSource)
		waveformResampled: ndarray[tuple[int, ...], dtype[floating[Any]]] = resampy.resample(waveform, sampleRateSource, sampleRateDesired, axis=axisTime)
		return waveformResampled
	return waveform

def loadWaveforms(listPathFilenames: Sequence[str | PathLike[str]], sampleRateTarget: float | None = None) -> ArrayWaveforms:
	"""Load a list of audio files into a single stacked NumPy array.

	You can use this function to batch-load multiple audio files into one `ArrayWaveforms` [1]
	array. All waveforms are resampled to `sampleRateTarget`, converted to stereo when
	necessary, and zero-padded on the trailing edge to match the length of the longest
	waveform. The resulting array is shaped `(channels, lengthWaveformMaximum, countFiles)`.

	Parameters
	----------
	listPathFilenames : Sequence[str | PathLike[str]]
		List of paths to audio files.
	sampleRateTarget : float | None = None
		Target sample rate in Hz. Defaults to `44100` when `None`.

	Returns
	-------
	arrayWaveforms : ArrayWaveforms
		Stacked waveform data shaped `(2, lengthWaveformMaximum, countFiles)` as `float32`,
		where `lengthWaveformMaximum` is the maximum sample count across all files at
		`sampleRateTarget`.

	Zero-Padding
	------------
	Waveforms shorter than `lengthWaveformMaximum` are zero-padded on the trailing edge.
	Leading padding is applied when `WaveformMetadata.samplesLeading` [2] is non-zero;
	`getWaveformMetadata` initializes `samplesLeading` to `0` by default.

	References
	----------
	[1] `ArrayWaveforms`

	[2] `WaveformMetadata`
	"""
	if sampleRateTarget is None:
		sampleRateTarget = parametersUniversal['sampleRate']

	# GitHub #3 Implement semantic axes for audio data
	axisOrderMapping: dict[str, int] = {'indexingAxis': -1, 'axisTime': -2, 'axisChannels': 0}
	axesSizes: dict[str, int] = dict.fromkeys(axisOrderMapping.keys(), 1)
	countAxes: int = len(axisOrderMapping)
	listShapeIndexToSize: list[int] = [9001] * countAxes

	countWaveforms: int = len(listPathFilenames)
	axesSizes['indexingAxis'] = countWaveforms
	countChannels: int = 2
	axesSizes['axisChannels'] = countChannels

	axisTime: int = -1  # pyright: ignore[reportUnusedVariable] # noqa: F841
	dictionaryWaveformMetadata: dict[int, WaveformMetadata] = getWaveformMetadata(listPathFilenames, sampleRateTarget)
	samplesTotalMaximum = max(entry['lengthWaveform'] + entry['samplesLeading'] + entry['samplesTrailing'] for entry in dictionaryWaveformMetadata.values())
	axesSizes['axisTime'] = samplesTotalMaximum

	for keyName, axisSize in axesSizes.items():
		axisNormalized: int = (axisOrderMapping[keyName] + countAxes) % countAxes
		listShapeIndexToSize[axisNormalized] = axisSize
	tupleShapeArray: tuple[int, int, int] = cast('tuple[int, int, int]', tuple(listShapeIndexToSize))

	arrayWaveforms: ArrayWaveforms = numpy.zeros(tupleShapeArray, dtype=universalDtypeWaveform)

	for index, metadata in dictionaryWaveformMetadata.items():
		waveform: Waveform = readAudioFile(metadata['pathFilename'], sampleRateTarget)
		samplesTrailing = metadata['lengthWaveform'] + metadata['samplesLeading'] - samplesTotalMaximum
		if samplesTrailing == 0:
			samplesTrailing = None
		# GitHub #4 Add padding logic to `loadWaveforms` and `loadSpectrograms`
		arrayWaveforms[:, metadata['samplesLeading']:samplesTrailing, index] = waveform

	return arrayWaveforms

def writeWAV(pathFilename: str | PathLike[Any] | BinaryIO, waveform: Waveform, sampleRate: float | None = None) -> None:
	"""Write a waveform array to a WAV file.

	You can use this function to save a `Waveform` [1] or any compatible NumPy array to a
	32-bit float WAV file. `writeWAV` creates any missing parent directories before writing
	using `makeDirsSafely` from `hunterMakesPy` [2].

	Parameters
	----------
	pathFilename : str | PathLike[Any] | BinaryIO
		Destination path for the WAV file, or a binary stream.
	waveform : Waveform
		Audio data shaped `(channels, samples)` or `(samples,)`.
	sampleRate : float | None = None
		Sample rate of `waveform` in Hz. Defaults to `44100` when `None`.

	File Overwrite and Format
	-------------------------
	`writeWAV` overwrites any existing file at `pathFilename` without prompting. All files
	are written as 32-bit float WAV using `soundfile.write` [3].

	References
	----------
	[1] `Waveform`

	[2] hunterMakesPy — makeDirsSafely
		https://context7.com/hunterhogan/huntermakespy

	[3] soundfile — audio library based on libsndfile
		https://python-soundfile.readthedocs.io/en/0.12.1/

	"""
	if sampleRate is None:
		sampleRate = parametersUniversal['sampleRate']
	makeDirsSafely(pathFilename)
	soundfile.write(file=pathFilename, data=waveform.T, samplerate=int(sampleRate), subtype='FLOAT', format='WAV')

@overload  # stft 1 ndarray
def stft(arrayTarget: Waveform, *, sampleRate: float | None = None, lengthHop: int | None = None, windowingFunction: WindowingFunction | None = None, lengthWindowingFunction: int | None = None, lengthFFT: int | None = None, inverse: Literal[False] = False, lengthWaveform: None = None, indexingAxis: None = None) -> Spectrogram: ...

@overload  # stft many ndarray
def stft(arrayTarget: ArrayWaveforms, *, sampleRate: float | None = None, lengthHop: int | None = None, windowingFunction: WindowingFunction | None = None, lengthWindowingFunction: int | None = None, lengthFFT: int | None = None, inverse: Literal[False] = False, lengthWaveform: None = None, indexingAxis: int = -1) -> ArraySpectrograms: ...

@overload  # istft 1 ndarray
def stft(arrayTarget: Spectrogram, *, sampleRate: float | None = None, lengthHop: int | None = None, windowingFunction: WindowingFunction | None = None, lengthWindowingFunction: int | None = None, lengthFFT: int | None = None, inverse: Literal[True] = True, lengthWaveform: int, indexingAxis: None = None) -> Waveform: ...

@overload  # istft many ndarray
def stft(arrayTarget: ArraySpectrograms, *, sampleRate: float | None = None, lengthHop: int | None = None, windowingFunction: WindowingFunction | None = None, lengthWindowingFunction: int | None = None, lengthFFT: int | None = None, inverse: Literal[True] = True, lengthWaveform: int, indexingAxis: int = -1) -> ArrayWaveforms: ...

def stft(arrayTarget: Waveform | ArrayWaveforms | Spectrogram | ArraySpectrograms
		, *
		, sampleRate: float | None = None
		, lengthHop: int | None = None
		, windowingFunction: WindowingFunction | None = None
		, lengthWindowingFunction: int | None = None
		, lengthFFT: int | None = None
		, inverse: bool = False
		, lengthWaveform: int | None = None
		, indexingAxis: int | None = None
		) -> Waveform | ArrayWaveforms | Spectrogram | ArraySpectrograms:
	"""Perform Short-Time Fourier Transform or its inverse on waveform or spectrogram data.

	You can use this function to convert a `Waveform` [1] to a `Spectrogram` [2] or reverse
	the transformation with `inverse=True`. Pass `ArrayWaveforms` [3] or
	`ArraySpectrograms` [4] with an `indexingAxis` to transform a batch of signals at once.
	All transform behavior is governed by `scipy.signal.ShortTimeFFT` [5].

	Four overloads determine the return type from `arrayTarget` and `inverse`:
	- `Waveform` [1] → `Spectrogram` [2] (single forward transform)
	- `ArrayWaveforms` [3] → `ArraySpectrograms` [4] (batch forward transform)
	- `Spectrogram` [2] → `Waveform` [1] (single inverse transform)
	- `ArraySpectrograms` [4] → `ArrayWaveforms` [3] (batch inverse transform)

	Parameters
	----------
	arrayTarget : Waveform | ArrayWaveforms | Spectrogram | ArraySpectrograms
		Input array for transformation.
	sampleRate : float | None = None
		Sample rate of the signal in Hz. Defaults to `44100` when `None`.
	lengthHop : int | None = None
		Number of samples between successive analysis frames. Defaults to `512` when `None`.
	windowingFunction : WindowingFunction | None = None
		Windowing function array [6]. When `None`, `windowingFunctionCallableUniversal` is
		called with `lengthWindowingFunction`, or the universal default is used.
	lengthWindowingFunction : int | None = None
		Length of the windowing function in samples. Used only when `windowingFunction` is
		`None`. Defaults to `1024` when `None`.
	lengthFFT : int | None = None
		Length of the FFT in samples. Defaults to `2048` or the next power of two ≥
		`lengthWindowingFunction` when `None`.
	inverse : bool = False
		When `True`, perform inverse STFT. When `False`, perform forward STFT.
	lengthWaveform : int | None = None
		Required output length in samples for inverse transform. Must be provided when
		`inverse` is `True`.
	indexingAxis : int | None = None
		Axis along which multiple signals are stacked. Use `None` for single-signal input.

	Returns
	-------
	arrayTransformed : Waveform | ArrayWaveforms | Spectrogram | ArraySpectrograms
		Transformed signal or batch of signals. Return type mirrors `arrayTarget` with
		forward and inverse swapped.

	Raises
	------
	ValueError
		When `inverse` is `True` and `lengthWaveform` is not provided.

	References
	----------
	[1] `Waveform`

	[2] `Spectrogram`

	[3] `ArrayWaveforms`

	[4] `ArraySpectrograms`

	[5] scipy.signal.ShortTimeFFT
		https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.ShortTimeFFT.html

	[6] `WindowingFunction`

	"""
	if sampleRate is None:
		sampleRate = parametersUniversal['sampleRate']
	if lengthHop is None:
		lengthHop = parametersUniversal['lengthHop']

	if windowingFunction is None:
		if lengthWindowingFunction is not None and windowingFunctionCallableUniversal:  # pyright: ignore[reportUnnecessaryComparison]
			windowingFunction = windowingFunctionCallableUniversal(lengthWindowingFunction)
		else:
			windowingFunction = parametersUniversal['windowingFunction']
		if lengthFFT is None:
			lengthFFTSherpa = parametersUniversal['lengthFFT']
			if lengthFFTSherpa >= windowingFunction.size:
				lengthFFT = lengthFFTSherpa

	if lengthFFT is None:
		lengthWindowingFunction = windowingFunction.size
		lengthFFT = 2 ** ceiling(log_base2(lengthWindowingFunction))

	if inverse and not lengthWaveform:
		message = "lengthWaveform must be specified for inverse transform"
		raise ValueError(message)

	stftWorkhorse = ShortTimeFFT(win=windowingFunction, hop=lengthHop, fs=sampleRate, mfft=lengthFFT, **parametersShortTimeFFTUniversal)

	def doTransformation(arrayInput: Waveform | Spectrogram, lengthWaveform: int | None, inverse: bool) -> Waveform | Spectrogram:  # noqa: FBT001
		if inverse:
			return cast('Waveform', stftWorkhorse.istft(S=arrayInput, k1=lengthWaveform))
		return cast('Spectrogram', stftWorkhorse.stft(x=arrayInput, **parametersSTFTUniversal))

	if indexingAxis is None:
		singleton: Waveform | Spectrogram = cast('Waveform | Spectrogram', arrayTarget)
		return doTransformation(singleton, lengthWaveform=lengthWaveform, inverse=inverse)
	else:
		arrayTARGET: ArrayWaveforms | ArraySpectrograms = cast('ArrayWaveforms | ArraySpectrograms', numpy.moveaxis(arrayTarget, indexingAxis, -1))
		index = 0
		arrayTransformed: ArrayWaveforms | ArraySpectrograms = cast('ArrayWaveforms | ArraySpectrograms', numpy.tile(doTransformation(cast('Waveform | Spectrogram', arrayTARGET[..., index]), lengthWaveform, inverse)[..., numpy.newaxis], arrayTARGET.shape[-1]))

		for index in range(1, arrayTARGET.shape[-1]):
			arrayTransformed[..., index] = doTransformation(cast('Waveform | Spectrogram', arrayTARGET[..., index]), lengthWaveform, inverse)

		return numpy.moveaxis(arrayTransformed, -1, indexingAxis)

def _getSpectrogram(waveform: Waveform, metadata: WaveformMetadata, sampleRateTarget: float, **parametersSTFT: Any) -> Spectrogram:
	"""I use this to load a single audio file into a pre-allocated waveform buffer and compute its spectrogram.

	(AI generated docstring)

	I use this shared subroutine inside `loadSpectrograms` to avoid reallocating a waveform
	buffer for each file. `_getSpectrogram` copies audio data from `metadata['pathFilename']`
	into the caller-provided `waveform` buffer at the position described by `metadata`, then
	computes `stft` with `sampleRateTarget` and any additional `parametersSTFT`. The caller
	must pass a fresh copy of the buffer for each iteration.

	Parameters
	----------
	waveform : Waveform
		Pre-allocated buffer into which audio data is copied before the STFT. The caller
		must pass a separate copy for each file to prevent data from accumulating across
		iterations.
	metadata : WaveformMetadata
		Record describing `pathFilename`, `lengthWaveform`, `samplesLeading`, and
		`samplesTrailing` for the audio file being loaded.
	sampleRateTarget : float
		Target sample rate passed to `readAudioFile`.
	**parametersSTFT : Any
		Keyword parameters forwarded to `stft`.

	Returns
	-------
	spectrogram : Spectrogram
		Complex spectrogram of `waveform` after copying the audio file into the buffer.

	"""
	# All waveforms have the same shape so that all spectrograms have the same shape.
	# GitHub #4 Add padding logic to `loadWaveforms` and `loadSpectrograms`
	lengthWaveform = metadata['lengthWaveform'] + metadata['samplesLeading'] + metadata['samplesTrailing']
	# All shorter waveforms are forced to have trailing zeros.
	waveform[:, 0:lengthWaveform] = readAudioFile(metadata['pathFilename'], sampleRateTarget)
	return stft(waveform, sampleRate=sampleRateTarget, **parametersSTFT)

def loadSpectrograms(listPathFilenames: Sequence[str | PathLike[str]], sampleRateTarget: float | None = None, **parametersSTFT: Any) -> tuple[ArraySpectrograms, dict[int, WaveformMetadata]]:
	"""Load spectrograms from a list of audio files.

	You can use this function to batch-convert audio files to spectrograms in a single call.
	`loadSpectrograms` reads each file, pads all waveforms to the same length, computes the
	Short-Time Fourier Transform for each, and stacks the results into one
	`ArraySpectrograms` [1] array. The function also returns a `WaveformMetadata` [2]
	dictionary that describes each file's original length and padding.

	Parameters
	----------
	listPathFilenames : Sequence[str | PathLike[str]]
		List of paths to audio files.
	sampleRateTarget : float | None = None
		Target sample rate in Hz. Defaults to `44100` when `None`.
	**parametersSTFT : Any
		Keyword parameters forwarded to `stft`, such as `lengthWindowingFunction` and
		`lengthHop`.

	Returns
	-------
	tupleSpectrogramsMetadata : tuple[ArraySpectrograms, dict[int, WaveformMetadata]]
		A two-element `tuple`. The first element is `ArraySpectrograms` [1] shaped
		`(channels, frequencies, frames, countFiles)` as `complex64`. The second element
		is a `dict` mapping integer file indices to `WaveformMetadata` [2] records.

	File Reading Progress
	---------------------
	`tqdm` [3] displays a progress bar in the terminal during the spectrogram computation
	loop.

	References
	----------
	[1] `ArraySpectrograms`

	[2] `WaveformMetadata`

	[3] tqdm — fast, extensible progress bar for Python and CLI
		https://tqdm.github.io/

	"""
	if sampleRateTarget is None:
		sampleRateTarget = parametersUniversal['sampleRate']

	max_workersHARDCODED: int = 3
	max_workers = max_workersHARDCODED  # pyright: ignore[reportUnusedVariable] # noqa: F841

	dictionaryWaveformMetadata: dict[int, WaveformMetadata] = getWaveformMetadata(listPathFilenames, sampleRateTarget)

	samplesTotalMaximum: int = max(entry['lengthWaveform'] + entry['samplesLeading'] + entry['samplesTrailing'] for entry in dictionaryWaveformMetadata.values())
	countChannels = 2
	waveformTemplate: Waveform = numpy.zeros(shape=(countChannels, samplesTotalMaximum), dtype=universalDtypeWaveform)
	spectrogramTemplate: Spectrogram = stft(waveformTemplate, sampleRate=sampleRateTarget, **parametersSTFT)

	arraySpectrograms: ArraySpectrograms = numpy.zeros(shape=(*spectrogramTemplate.shape, len(dictionaryWaveformMetadata)), dtype=universalDtypeSpectrogram)

	for index, metadata in tqdm(dictionaryWaveformMetadata.items()):
		arraySpectrograms[..., index] = _getSpectrogram(waveformTemplate.copy(), metadata, sampleRateTarget, **parametersSTFT)

	# with ProcessPoolExecutor(max_workers) as concurrencyManager:
	# 	dictionaryConcurrency = {concurrencyManager.submit(
	# 		_getSpectrogram, waveformTemplate.copy(), metadata, sampleRateTarget, **parametersSTFT): index
	# 			for index, metadata in dictionaryWaveformMetadata.items()}

	# 	for claimTicket in tqdm(as_completed(dictionaryConcurrency), total=len(dictionaryConcurrency)):
	# 		arraySpectrograms[..., dictionaryConcurrency[claimTicket]] = claimTicket.result()  # noqa: ERA001

	return arraySpectrograms, dictionaryWaveformMetadata

def spectrogramToWAV(spectrogram: Spectrogram, pathFilename: str | PathLike[Any] | BinaryIO, lengthWaveform: int, sampleRate: float | None = None, **parametersSTFT: Any) -> None:
	"""Write a complex spectrogram to a WAV file by computing the inverse STFT.

	You can use this function to reconstruct a waveform from a `Spectrogram` [1] and save
	it directly to a WAV file. `spectrogramToWAV` calls `stft` with `inverse=True` to
	obtain the reconstructed `Waveform` [2], then passes it to `writeWAV`.

	Parameters
	----------
	spectrogram : Spectrogram
		Complex spectrogram to convert back to a waveform.
	pathFilename : str | PathLike[Any] | BinaryIO
		Destination path for the WAV file, or a binary stream.
	lengthWaveform : int
		Number of samples in the output waveform. The inverse STFT cannot recover the
		original length from the spectrogram alone, so `lengthWaveform` is required.
	sampleRate : float | None = None
		Sample rate for the output WAV file in Hz. Defaults to `44100` when `None`.
	**parametersSTFT : Any
		Keyword parameters forwarded to `stft`, such as `lengthWindowingFunction` and
		`lengthHop`.

	File Overwrite and Format
	-------------------------
	See `writeWAV` for file overwrite behavior and output format details.

	References
	----------
	[1] `Spectrogram`

	[2] `Waveform`

	"""
	if sampleRate is None:
		sampleRate = parametersUniversal['sampleRate']

	waveform: Waveform = stft(spectrogram, inverse=True, lengthWaveform=lengthWaveform, sampleRate=sampleRate, **parametersSTFT)
	writeWAV(pathFilename, waveform, sampleRate)

def waveformSpectrogramWaveform(callableNeedsSpectrogram: Callable[[Spectrogram], Spectrogram]) -> Callable[[Waveform], Waveform]:
	"""Decorate a spectrogram-processing callable to accept and return waveforms.

	You can use this function as a decorator when you have a function that transforms
	`Spectrogram` [1] data and you want a version that operates directly on `Waveform` [2]
	data. The returned function applies `stft` to convert the input `Waveform` [2] to a
	`Spectrogram` [1], calls `callableNeedsSpectrogram`, then applies inverse `stft` to
	convert the result back to a `Waveform` [2] of the original length.

	Parameters
	----------
	callableNeedsSpectrogram : Callable[[Spectrogram], Spectrogram]
		A function that accepts and returns a `Spectrogram` [1].

	Returns
	-------
	stft_istft : Callable[[Waveform], Waveform]
		A function that accepts a `Waveform` [2], converts it to a `Spectrogram` [1],
		applies `callableNeedsSpectrogram`, and returns the reconstructed `Waveform` [2]
		at the original length.

	Time Axis Assumption
	--------------------
	The inner function `stft_istft` assumes the time axis of the input `Waveform` [2] is
	the last axis (`-1`). This matches the `(channels, samples)` shape convention.

	References
	----------
	[1] `Spectrogram`

	[2] `Waveform`

	"""
	def stft_istft(waveform: Waveform) -> Waveform:
		axisTime = -1
		arrayTarget = stft(waveform)
		spectrogram = callableNeedsSpectrogram(arrayTarget)
		return stft(spectrogram, inverse=True, indexingAxis=None, lengthWaveform=waveform.shape[axisTime])
	return stft_istft
