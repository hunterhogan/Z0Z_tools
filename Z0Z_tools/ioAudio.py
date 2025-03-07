"""
Provides utilities for reading, writing, and resampling audio waveforms.
"""
from collections.abc import Callable, Sequence
from math import ceil as ceiling, log2 as log_base2
from numpy import dtype, float32, floating, ndarray, complex64
from os import PathLike
from scipy.signal import ShortTimeFFT
from typing import Any, BinaryIO, Literal, cast, overload
from Z0Z_tools import halfsine, makeDirsSafely
from Z0Z_tools import Waveform, ArrayWaveforms, Spectrogram, ArraySpectrograms, ParametersSTFT, ParametersShortTimeFFT, ParametersUniversal, WaveformMetadata, WindowingFunction
import io
import numpy
import resampy
import soundfile

# TODO how should I handle these?
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

# No, I don't know how to implement this, but I might learn how to do it later.
# If you know how, you can help. :D
setParametersUniversal = None

windowingFunctionCallableUniversal = windowingFunctionCallableDEFAULT
if not setParametersUniversal:
	parametersUniversal: ParametersUniversal = parametersDEFAULT

def getWaveformMetadata(listPathFilenames: Sequence[str | PathLike[str]], sampleRate: float) -> dict[int, WaveformMetadata]:
	axisTime: int = -1
	dictionaryWaveformMetadata: dict[int, WaveformMetadata] = {}
	for index, pathFilename in enumerate(listPathFilenames):
		lengthWaveform = readAudioFile(pathFilename, sampleRate).shape[axisTime]
		dictionaryWaveformMetadata[index] = WaveformMetadata(
			pathFilename = str(pathFilename),
			lengthWaveform = lengthWaveform,
			samplesLeading = 0,
			samplesTrailing = 0,
		)
	return dictionaryWaveformMetadata

def readAudioFile(pathFilename: str | PathLike[Any] | BinaryIO, sampleRate: float | None = None) -> Waveform:
	"""
	Reads an audio file and returns its data as a NumPy array. Mono is always converted to stereo.

	Parameters:
		pathFilename: The path to the audio file.
		sampleRate (44100): The sample rate of the returned waveform. Defaults to 44100.

	Returns:
		waveform: The audio data in an array shaped (channels, samples).
	"""
	if sampleRate is None:
		sampleRate = parametersUniversal['sampleRate']
	try:
		with soundfile.SoundFile(pathFilename) as readSoundFile:
			sampleRateSource: int = readSoundFile.samplerate
			waveform: Waveform = readSoundFile.read(dtype=str(universalDtypeWaveform.__name__), always_2d=True).astype(universalDtypeWaveform)
			# GitHub #3 Implement semantic axes for audio data
			axisTime = 0; axisChannels = 1
			waveform = cast(Waveform, resampleWaveform(waveform, sampleRateDesired=sampleRate, sampleRateSource=sampleRateSource, axisTime=axisTime))
			if waveform.shape[axisChannels] == 1:
				waveform = numpy.repeat(waveform, 2, axis=axisChannels)
			return numpy.transpose(waveform, axes=(axisChannels, axisTime))
	except soundfile.LibsndfileError as ERRORmessage:
		if 'System error' in str(ERRORmessage):
			raise FileNotFoundError(f"File not found: {pathFilename}") from ERRORmessage
		else:
			raise

def resampleWaveform(waveform: ndarray[tuple[int, ...], dtype[floating[Any]]], sampleRateDesired: float, sampleRateSource: float, axisTime: int = -1) -> ndarray[tuple[int, ...], dtype[floating[Any]]]:
	"""
	Resamples the waveform to the desired sample rate using resampy.

	Parameters:
		waveform: The input audio data.
		sampleRateDesired: The desired sample rate.
		sampleRateSource: The original sample rate of the waveform.

	Returns:
		waveformResampled: The resampled waveform.
	"""
	if sampleRateSource != sampleRateDesired:
		sampleRateDesired = round(sampleRateDesired)
		sampleRateSource = round(sampleRateSource)
		waveformResampled: ndarray[tuple[int, ...], dtype[floating[Any]]] = resampy.resample(waveform, sampleRateSource, sampleRateDesired, axis=axisTime)
		return waveformResampled
	else:
		return waveform

def loadWaveforms(listPathFilenames: Sequence[str | PathLike[str]], sampleRateTarget: float | None = None) -> ArrayWaveforms:
	"""
	Load a list of audio files into a single array.

	Parameters:
		listPathFilenames: List of file paths to the audio files.
		sampleRate (44100): Target sample rate for the waveforms; the function will resample if necessary. Defaults to 44100.
	Returns:
		arrayWaveforms: A single NumPy array of shape (countChannels, lengthWaveformMaximum, countWaveforms)
	"""
	if sampleRateTarget is None:
		sampleRateTarget = parametersUniversal['sampleRate']

	# GitHub #3 Implement semantic axes for audio data
	axisOrderMapping: dict[str, int] = {'indexingAxis': -1, 'axisTime': -2, 'axisChannels': 0}
	axesSizes: dict[str, int] = {keyName: 1 for keyName in axisOrderMapping.keys()}
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
	tupleShapeArray: tuple[int, int, int] = cast(tuple[int, int, int], tuple(listShapeIndexToSize))

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
	"""
	Writes a waveform to a WAV file.

	Parameters:
		pathFilename: The path and filename where the WAV file will be saved.
		waveform: The waveform data to be written to the WAV file. The waveform should be in the shape (channels, samples) or (samples,).
		sampleRate (44100): The sample rate of the waveform. Defaults to 44100 Hz.

	Returns:
		None:

	### Note well
		The function overwrites existing files without prompting or informing the user.

	Notes
		All files are saved as 32-bit float.
		The function will attempt to create the directory structure, if applicable.
	"""
	if sampleRate is None:
		sampleRate = parametersUniversal['sampleRate']
	makeDirsSafely(pathFilename)
	soundfile.write(file=pathFilename, data=waveform.T, samplerate=int(sampleRate), subtype='FLOAT', format='WAV')

@overload # stft
def stft(arrayTarget: Waveform, *, sampleRate: float | None = None, lengthHop: int | None = None, windowingFunction: WindowingFunction | None = None, lengthWindowingFunction: int | None = None, lengthFFT: int | None = None, inverse: Literal[False] = False, lengthWaveform: None = None, indexingAxis: None = None) -> Spectrogram: ...

@overload # stft
def stft(arrayTarget: ArrayWaveforms, *, sampleRate: float | None = None, lengthHop: int | None = None, windowingFunction: WindowingFunction | None = None, lengthWindowingFunction: int | None = None, lengthFFT: int | None = None, inverse: Literal[False] = False, lengthWaveform: None = None, indexingAxis: int = -1) -> ArraySpectrograms: ...

@overload # istft
def stft(arrayTarget: Spectrogram, *, sampleRate: float | None = None, lengthHop: int | None = None, windowingFunction: WindowingFunction | None = None, lengthWindowingFunction: int | None = None, lengthFFT: int | None = None, inverse: Literal[True] = True, lengthWaveform: int, indexingAxis: None = None) -> Waveform: ...

@overload # istft
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
	"""
	Short-Time Fourier Transform with unified interface for forward and inverse transforms.

	Parameters:
		arrayTarget: Input array for transformation.
		sampleRate (44100): Sample rate of the signal.
		lengthHop (512): Number of samples between successive frames.
		windowingFunction (halfsine): Windowing function array. Defaults to halfsine if None.
		lengthWindowingFunction (1024): Length of the windowing function. Used if windowingFunction is None.
		lengthFFT (2048*): Length of the FFT. Defaults to 2048 or the next power of 2 >= lengthWindowingFunction.
		inverse (False): Whether to perform inverse transform.
		lengthWaveform: Required output length for inverse transform.
		indexingAxis (None, -1): Axis containing multiple signals to transform.

	Returns:
		arrayTransformed: The transformed signal(s).
	"""
	if sampleRate is None: sampleRate = parametersUniversal['sampleRate']
	if lengthHop is None: lengthHop = parametersUniversal['lengthHop']

	if windowingFunction is None:
		if lengthWindowingFunction is not None and windowingFunctionCallableUniversal:
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
		raise ValueError("lengthWaveform must be specified for inverse transform")

	stftWorkhorse = ShortTimeFFT(win=windowingFunction, hop=lengthHop, fs=sampleRate, mfft=lengthFFT, **parametersShortTimeFFTUniversal)

	def doTransformation(arrayInput: Waveform | Spectrogram, lengthWaveform: int | None, inverse: bool) -> Waveform | Spectrogram:
		if inverse:
			return cast(Waveform, stftWorkhorse.istft(S=arrayInput, k1=lengthWaveform))
		return cast(Spectrogram, stftWorkhorse.stft(x=arrayInput, **parametersSTFTUniversal))

	if indexingAxis is None:
		singleton: Waveform | Spectrogram = cast(Waveform | Spectrogram, arrayTarget)
		return doTransformation(singleton, lengthWaveform=lengthWaveform, inverse=inverse)
	else:
		arrayTARGET: ArrayWaveforms | ArraySpectrograms = cast(ArrayWaveforms | ArraySpectrograms, numpy.moveaxis(arrayTarget, indexingAxis, -1))
		index = 0
		arrayTransformed: ArrayWaveforms | ArraySpectrograms = cast(ArrayWaveforms | ArraySpectrograms, numpy.tile(doTransformation(arrayTARGET[..., index], lengthWaveform, inverse)[..., numpy.newaxis], arrayTARGET.shape[-1]))

		for index in range(1, arrayTARGET.shape[-1]):
			arrayTransformed[..., index] = doTransformation(arrayTARGET[..., index], lengthWaveform, inverse)

		return cast(ArrayWaveforms | ArraySpectrograms, numpy.moveaxis(arrayTransformed, -1, indexingAxis))

def loadSpectrograms(listPathFilenames: Sequence[str | PathLike[str]], sampleRateTarget: float | None = None, **parametersSTFT: Any) -> tuple[ArraySpectrograms, dict[int, WaveformMetadata]]:
	"""
	Load spectrograms from audio files.

	Parameters:
		listPathFilenames: A list of WAV path and filenames.
		sampleRateTarget (44100): The target sample rate. If necessary, a file will be resampled to the target sample rate. Defaults to 44100.
		**parametersSTFT: Keyword-parameters for the Short-Time Fourier Transform, see `stft`.

	Returns:
		tupleSpectrogramsLengthsWaveform: A tuple containing the array of spectrograms and a list of metadata dictionaries for each spectrogram.
	"""
	if sampleRateTarget is None:
		sampleRateTarget = parametersUniversal['sampleRate']

	dictionaryWaveformMetadata: dict[int, WaveformMetadata] = getWaveformMetadata(listPathFilenames, sampleRateTarget)

	samplesTotalMaximum: int = max([entry['lengthWaveform'] + entry['samplesLeading'] + entry['samplesTrailing'] for entry in dictionaryWaveformMetadata.values()])
	countChannels = 2
	waveformTemplate: Waveform = numpy.zeros(shape=(countChannels, samplesTotalMaximum), dtype=universalDtypeWaveform)
	spectrogramTemplate: Spectrogram = stft(waveformTemplate, sampleRate=sampleRateTarget, **parametersSTFT)

	arraySpectrograms: ArraySpectrograms = numpy.zeros(shape=(*spectrogramTemplate.shape, len(dictionaryWaveformMetadata)), dtype=universalDtypeSpectrogram)

	for index, metadata in dictionaryWaveformMetadata.items():
		# All waveforms have the same shape so that all spectrograms have the same shape.
		waveform = waveformTemplate.copy()
		# GitHub #4 Add padding logic to `loadWaveforms` and `loadSpectrograms`
		lengthWaveform = metadata['lengthWaveform'] + metadata['samplesLeading'] + metadata['samplesTrailing']
		# All shorter waveforms are forced to have trailing zeros.
		waveform[:, 0:lengthWaveform] = readAudioFile(metadata['pathFilename'], sampleRateTarget)
		arraySpectrograms[..., index] = stft(waveform, sampleRate=sampleRateTarget, **parametersSTFT)

	return arraySpectrograms, dictionaryWaveformMetadata

def spectrogramToWAV(spectrogram: Spectrogram, pathFilename: str | PathLike[Any] | io.IOBase, lengthWaveform: int, sampleRate: float | None = None, **parametersSTFT: Any) -> None:
	"""
	Writes a complex spectrogram to a WAV file.

	Parameters:
		spectrogram: The complex spectrogram to be written to the file.
		pathFilename: Location for the file of the waveform output.
		lengthWaveform: n.b. Not optional: the length of the output waveform in samples.
		sampleRate (44100): The sample rate of the output waveform file. Defaults to 44100.
		**parametersSTFT: Keyword-parameters for the inverse Short-Time Fourier Transform, see `stft`.

	Returns:
		None: But see `writeWAV` for additional notes and caveats.
	"""
	if sampleRate is None:
		sampleRate = parametersUniversal['sampleRate']

	waveform: Waveform = stft(spectrogram, inverse=True, lengthWaveform=lengthWaveform, sampleRate=sampleRate, **parametersSTFT)
	writeWAV(pathFilename, waveform, sampleRate)

def waveformSpectrogramWaveform(callableNeedsSpectrogram: Callable[[Spectrogram], Spectrogram]) -> Callable[[Waveform], Waveform]:
	def stft_istft(waveform: Waveform) -> Waveform:
		axisTime = -1
		arrayTarget = stft(waveform)
		spectrogram = callableNeedsSpectrogram(arrayTarget)
		return stft(spectrogram, inverse=True, indexingAxis=None, lengthWaveform=waveform.shape[axisTime])
	return stft_istft
