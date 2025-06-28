"""Provides utilities for reading, writing, and resampling audio waveforms.

Comprehensive audio processing module offering functions for file I/O, resampling,
and Short-Time Fourier Transform operations with consistent data shapes and types.

"""
from collections.abc import Callable, Sequence
from concurrent.futures import as_completed, ProcessPoolExecutor
from math import ceil as ceiling, log2 as log_base2
from multiprocessing import set_start_method as multiprocessing_set_start_method
from numpy import complex64, dtype, float32, floating, ndarray
from os import PathLike
from pathlib import Path
from scipy.signal import ShortTimeFFT
from tqdm.auto import tqdm
from typing import Any, BinaryIO, cast, Literal, overload
from Z0Z_tools import (
	ArraySpectrograms, ArrayWaveforms, halfsine, makeDirsSafely, ParametersShortTimeFFT, ParametersSTFT,
	ParametersUniversal, Spectrogram, Waveform, WaveformMetadata, WindowingFunction,
)
import io
import numpy
import resampy
import soundfile

# When to use multiprocessing.set_start_method https://github.com/hunterhogan/mapFolding/issues/6
if __name__ == '__main__':
	multiprocessing_set_start_method('spawn')

# Design coordinated, user-overridable universal parameter defaults for audio functions
# https://github.com/hunterhogan/Z0Z_tools/issues/5
universalDtypeWaveform = float32
universalDtypeSpectrogram = complex64
parametersShortTimeFFTUniversal: ParametersShortTimeFFT = {'fft_mode': 'onesided'}
parametersSTFTUniversal: ParametersSTFT = {'padding': 'even', 'axis': -1}

lengthWindowingFunctionDEFAULT = 1024
windowingFunctionCallableDEFAULT = halfsine
parametersDEFAULT = ParametersUniversal (
	lengthFFT=2048,
	lengthHop=512,
	lengthWindowingFunction=lengthWindowingFunctionDEFAULT,
	sampleRate=44100,
	windowingFunction=windowingFunctionCallableDEFAULT(lengthWindowingFunctionDEFAULT),
)

setParametersUniversal = None

windowingFunctionCallableUniversal = windowingFunctionCallableDEFAULT
if not setParametersUniversal:
	parametersUniversal: ParametersUniversal = parametersDEFAULT

def getWaveformMetadata(listPathFilenames: Sequence[str | PathLike[str]], sampleRate: float) -> dict[int, WaveformMetadata]:
	"""Retrieve metadata for a collection of audio waveform files.

	Reads each audio file, determines its length, and creates a `WaveformMetadata`
	object for each file, indexed by its position in the input list.

	Parameters
	----------
	listPathFilenames : Sequence[str | PathLike[str]]
		A sequence of paths to audio files.
	sampleRate : float
		The target sample rate for reading the audio files.

	Returns
	-------
	dictionaryWaveformMetadata : dict[int, WaveformMetadata]
		Dictionary mapping integer indices to
		`WaveformMetadata` objects. Each `WaveformMetadata` contains:
		- pathFilename: The string path to the audio file
		- lengthWaveform: The number of samples in the audio file
		- samplesLeading: Set to 0 by default
		- samplesTrailing: Set to 0 by default

	Notes
	-----
	This function uses `tqdm` to display a progress bar during processing.

	"""
	axisTime: int = -1
	dictionaryWaveformMetadata: dict[int, WaveformMetadata] = {}
	for index, pathFilename in enumerate(tqdm(listPathFilenames)):
		lengthWaveform = readAudioFile(pathFilename, sampleRate).shape[axisTime]
		dictionaryWaveformMetadata[index] = WaveformMetadata(
			pathFilename = str(pathFilename),
			lengthWaveform = lengthWaveform,
			samplesLeading = 0,
			samplesTrailing = 0,
		)
	return dictionaryWaveformMetadata

def readAudioFile(pathFilename: str | PathLike[Any] | BinaryIO, sampleRate: float | None = None) -> Waveform:
	"""Read an audio file and return its data as a NumPy array.

	Mono audio is always converted to stereo for consistent output shape.

	Parameters
	----------
	pathFilename : str | PathLike[Any] | BinaryIO
		The path to the audio file or binary stream.
	sampleRate : float | None = None
		The sample rate of the returned waveform. Defaults to 44100 if `None`.

	Returns
	-------
	waveform : Waveform
		The audio data in an array shaped (channels, samples).

	Raises
	------
	FileNotFoundError
		When the audio file cannot be found.
	soundfile.LibsndfileError
		When the file format is unsupported or corrupted.

	"""
	if sampleRate is None:
		sampleRate = parametersUniversal['sampleRate']
	try:
		with soundfile.SoundFile(pathFilename) as readSoundFile:
			sampleRateSource: int = readSoundFile.samplerate
			waveform: Waveform = readSoundFile.read(dtype=str(universalDtypeWaveform.__name__), always_2d=True).astype(universalDtypeWaveform)
			# GitHub #3 Implement semantic axes for audio data
			axisTime = 0
			axisChannels = 1
			waveform = cast("Waveform", resampleWaveform(waveform, sampleRateDesired=sampleRate, sampleRateSource=sampleRateSource, axisTime=axisTime))
			if waveform.shape[axisChannels] == 1:
				waveform = numpy.repeat(waveform, 2, axis=axisChannels)
			return numpy.transpose(waveform, axes=(axisChannels, axisTime))
	except soundfile.LibsndfileError as ERRORmessage:
		if 'System error' in str(ERRORmessage):
			message = f"File not found: {pathFilename}"
			raise FileNotFoundError(message) from ERRORmessage
		else:  # noqa: RET506
			raise

def resampleWaveform(waveform: ndarray[tuple[int, ...], dtype[floating[Any]]], sampleRateDesired: float, sampleRateSource: float, axisTime: int = -1) -> ndarray[tuple[int, ...], dtype[floating[Any]]]:
	"""Resample the waveform to the desired sample rate using resampy.

	Parameters
	----------
	waveform : ndarray[tuple[int, ...], dtype[floating[Any]]]
		The input audio data.
	sampleRateDesired : float
		The desired sample rate.
	sampleRateSource : float
		The original sample rate of the waveform.
	axisTime : int = -1
		The time axis along which to perform resampling.

	Returns
	-------
	waveformResampled : ndarray[tuple[int, ...], dtype[floating[Any]]]
		The resampled waveform.

	"""
	if sampleRateSource != sampleRateDesired:
		sampleRateDesired = round(sampleRateDesired)
		sampleRateSource = round(sampleRateSource)
		waveformResampled: ndarray[tuple[int, ...], dtype[floating[Any]]] = resampy.resample(waveform, sampleRateSource, sampleRateDesired, axis=axisTime)
		return waveformResampled
	return waveform

def loadWaveforms(listPathFilenames: Sequence[str | PathLike[str]], sampleRateTarget: float | None = None) -> ArrayWaveforms:
	"""Load a list of audio files into a single array.

	Parameters
	----------
	listPathFilenames : Sequence[str | PathLike[str] | Path]
		List of file paths to the audio files.
	sampleRateTarget : float | None = None
		Target sample rate for the waveforms; the
		function will resample if necessary. Defaults to 44100 if `None`.

	Returns
	-------
	arrayWaveforms : ArrayWaveforms
		A single NumPy array of shape (countChannels, lengthWaveformMaximum, countWaveforms).

	Raises
	------
	ValueError
		When the list of path filenames is empty.

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

	axisTime: int = -1
	dictionaryWaveformMetadata: dict[int, WaveformMetadata] = getWaveformMetadata(listPathFilenames, sampleRateTarget)
	samplesTotalMaximum = max([entry['lengthWaveform'] + entry['samplesLeading'] + entry['samplesTrailing'] for entry in dictionaryWaveformMetadata.values()])
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

def writeWAV(pathFilename: str | PathLike[Any] | io.IOBase, waveform: Waveform, sampleRate: float | None = None) -> None:
	"""Write a waveform to a WAV file.

	Parameters
	----------
	pathFilename : str | PathLike[Any] | io.IOBase
		The path and filename where the WAV file will be saved.
	waveform : Waveform
		The waveform data to be written to the WAV file. The waveform should be in the shape (channels, samples) or (samples,).
	sampleRate : float | None = None
		The sample rate of the waveform. Defaults to 44100 Hz if `None`.

	Returns
	-------
	None

	Notes
	-----
	The function overwrites existing files without prompting or informing the user.
	All files are saved as 32-bit float.
	The function will attempt to create the directory structure, if applicable.

	"""
	if sampleRate is None:
		sampleRate = parametersUniversal['sampleRate']
	makeDirsSafely(pathFilename)
	soundfile.write(file=pathFilename, data=waveform.T, samplerate=int(sampleRate), subtype='FLOAT', format='WAV')

@overload # stft 1 ndarray
def stft(arrayTarget: Waveform, *, sampleRate: float | None = None, lengthHop: int | None = None, windowingFunction: WindowingFunction | None = None, lengthWindowingFunction: int | None = None, lengthFFT: int | None = None, inverse: Literal[False] = False, lengthWaveform: None = None, indexingAxis: None = None) -> Spectrogram: ...  # noqa: E501

@overload # stft many ndarray
def stft(arrayTarget: ArrayWaveforms, *, sampleRate: float | None = None, lengthHop: int | None = None, windowingFunction: WindowingFunction | None = None, lengthWindowingFunction: int | None = None, lengthFFT: int | None = None, inverse: Literal[False] = False, lengthWaveform: None = None, indexingAxis: int = -1) -> ArraySpectrograms: ...  # noqa: E501

@overload # istft 1 ndarray
def stft(arrayTarget: Spectrogram, *, sampleRate: float | None = None, lengthHop: int | None = None, windowingFunction: WindowingFunction | None = None, lengthWindowingFunction: int | None = None, lengthFFT: int | None = None, inverse: Literal[True] = True, lengthWaveform: int, indexingAxis: None = None) -> Waveform: ...  # noqa: E501

@overload # istft many ndarray
def stft(arrayTarget: ArraySpectrograms, *, sampleRate: float | None = None, lengthHop: int | None = None, windowingFunction: WindowingFunction | None = None, lengthWindowingFunction: int | None = None, lengthFFT: int | None = None, inverse: Literal[True] = True, lengthWaveform: int, indexingAxis: int = -1) -> ArrayWaveforms: ...  # noqa: E501

def stft(arrayTarget: Waveform | ArrayWaveforms | Spectrogram | ArraySpectrograms  # noqa: C901, PLR0913
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
	"""Perform Short-Time Fourier Transform with unified interface for forward and inverse transforms.

	Parameters
	----------
	arrayTarget : Waveform | ArrayWaveforms | Spectrogram | ArraySpectrograms
		Input array for transformation.
	sampleRate : float | None = None
		Sample rate of the signal. Defaults to 44100 if `None`.
	lengthHop : int | None = None
		Number of samples between successive frames. Defaults to 512 if `None`.
	windowingFunction : WindowingFunction | None = None
		Windowing function array. Defaults to halfsine if `None`.
	lengthWindowingFunction : int | None = None
		Length of the windowing function. Used if `windowingFunction` is `None`. Defaults to 1024 if `None`.
	lengthFFT : int | None = None
		Length of the FFT. Defaults to 2048 or the next power of 2 >= `lengthWindowingFunction`.
	inverse : bool = False
		Whether to perform inverse transform.
	lengthWaveform : int | None = None
		Required output length for inverse transform.
	indexingAxis : int | None = None
		Axis containing multiple signals to transform. Use `None` for single signals.

	Returns
	-------
	arrayTransformed : Waveform | ArrayWaveforms | Spectrogram | ArraySpectrograms
		The transformed signal(s).

	Raises
	------
	ValueError
		When `lengthWaveform` is not specified for inverse transform.

	"""
	if sampleRate is None:
		sampleRate = parametersUniversal['sampleRate']
	if lengthHop is None:
		lengthHop = parametersUniversal['lengthHop']

	if windowingFunction is None:
		if lengthWindowingFunction is not None and windowingFunctionCallableUniversal: # pyright: ignore[reportUnnecessaryComparison]  # noqa: SIM108
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
	else:  # noqa: RET505
		arrayTARGET: ArrayWaveforms | ArraySpectrograms = cast('ArrayWaveforms | ArraySpectrograms', numpy.moveaxis(arrayTarget, indexingAxis, -1))
		index = 0
		arrayTransformed: ArrayWaveforms | ArraySpectrograms = cast('ArrayWaveforms | ArraySpectrograms', numpy.tile(doTransformation(cast('Waveform | Spectrogram', arrayTARGET[..., index]), lengthWaveform, inverse)[..., numpy.newaxis], arrayTARGET.shape[-1]))

		for index in range(1, arrayTARGET.shape[-1]):
			arrayTransformed[..., index] = doTransformation(cast('Waveform | Spectrogram', arrayTARGET[..., index]), lengthWaveform, inverse)

		return cast('ArrayWaveforms | ArraySpectrograms', numpy.moveaxis(arrayTransformed, -1, indexingAxis))

def _getSpectrogram(waveform: Waveform, metadata: WaveformMetadata, sampleRateTarget: float, **parametersSTFT: Any) -> Spectrogram:
	# All waveforms have the same shape so that all spectrograms have the same shape.
	# GitHub #4 Add padding logic to `loadWaveforms` and `loadSpectrograms`
	lengthWaveform = metadata['lengthWaveform'] + metadata['samplesLeading'] + metadata['samplesTrailing']
	# All shorter waveforms are forced to have trailing zeros.
	waveform[:, 0:lengthWaveform] = readAudioFile(metadata['pathFilename'], sampleRateTarget)
	return stft(waveform, sampleRate=sampleRateTarget, **parametersSTFT)

def loadSpectrograms(listPathFilenames: Sequence[str | PathLike[str]], sampleRateTarget: float | None = None, **parametersSTFT: Any) -> tuple[ArraySpectrograms, dict[int, WaveformMetadata]]:
	"""Load spectrograms from audio files.

	Parameters
	----------
	listPathFilenames : Sequence[str | PathLike[str]]
		A list of WAV path and filenames.
	sampleRateTarget : float | None = None
		The target sample rate. If necessary, a file will be resampled to the target sample rate. Defaults to 44100 if `None`.
	**parametersSTFT : Any
		Keyword parameters for the Short-Time Fourier Transform, see `stft`.

	Returns
	-------
	tupleSpectrogramsMetadata : tuple[ArraySpectrograms, dict[int, WaveformMetadata]]
		A tuple containing the array of spectrograms and a dictionary of metadata for each spectrogram.

	"""
	if sampleRateTarget is None:
		sampleRateTarget = parametersUniversal['sampleRate']

	max_workersHARDCODED: int = 3
	max_workers = max_workersHARDCODED

	dictionaryWaveformMetadata: dict[int, WaveformMetadata] = getWaveformMetadata(listPathFilenames, sampleRateTarget)

	samplesTotalMaximum: int = max([entry['lengthWaveform'] + entry['samplesLeading'] + entry['samplesTrailing'] for entry in dictionaryWaveformMetadata.values()])
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
	# 		arraySpectrograms[..., dictionaryConcurrency[claimTicket]] = claimTicket.result()

	return arraySpectrograms, dictionaryWaveformMetadata

def spectrogramToWAV(spectrogram: Spectrogram, pathFilename: str | PathLike[Any] | io.IOBase, lengthWaveform: int, sampleRate: float | None = None, **parametersSTFT: Any) -> None:
	"""Write a complex spectrogram to a WAV file.

	Parameters
	----------
	spectrogram : Spectrogram
		The complex spectrogram to be written to the file.
	pathFilename : str | PathLike[Any] | io.IOBase
		Location for the file of the waveform output.
	lengthWaveform : int
		The length of the output waveform in samples. This parameter is not optional.
	sampleRate : float | None = None
		The sample rate of the output waveform file. Defaults to 44100 if `None`.
	**parametersSTFT : Any
		Keyword parameters for the inverse Short-Time Fourier Transform, see `stft`.

	Returns
	-------
	None

	Notes
	-----
	See `writeWAV` for additional notes and caveats.

	"""
	if sampleRate is None:
		sampleRate = parametersUniversal['sampleRate']

	waveform: Waveform = stft(spectrogram, inverse=True, lengthWaveform=lengthWaveform, sampleRate=sampleRate, **parametersSTFT)
	writeWAV(pathFilename, waveform, sampleRate)

def waveformSpectrogramWaveform(callableNeedsSpectrogram: Callable[[Spectrogram], Spectrogram]) -> Callable[[Waveform], Waveform]:
	"""Decorate a function to convert a waveform to a spectrogram, applies a transformation on the spectrogram, and converts the transformed spectrogram back to a waveform.

	This is a higher-order function that takes a function operating on spectrograms
	and returns a function that operates on waveforms by applying the Short-Time
	Fourier Transform and its inverse.

	Parameters
	----------
	callableNeedsSpectrogram : Callable[[Spectrogram], Spectrogram]
		A function that takes a spectrogram and returns a transformed spectrogram.

	Returns
	-------
	stft_istft : Callable[[Waveform], Waveform]
		A function that takes a waveform, transforms it into a spectrogram, applies the provided spectrogram transformation, and converts it back to a waveform.

	Notes
	-----
	The time axis is assumed to be the last axis (-1) of the waveform array.

	"""
	def stft_istft(waveform: Waveform) -> Waveform:
		axisTime = -1
		arrayTarget = stft(waveform)
		spectrogram = callableNeedsSpectrogram(arrayTarget)
		return stft(spectrogram, inverse=True, indexingAxis=None, lengthWaveform=waveform.shape[axisTime])
	return stft_istft
