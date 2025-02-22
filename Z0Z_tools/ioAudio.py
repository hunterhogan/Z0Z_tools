"""
Provides utilities for reading, writing, and resampling audio waveforms.
"""
from numpy import complex64, complexfloating, dtype, float32, floating, ndarray, integer
from numpy.typing import NDArray
from scipy.signal import ShortTimeFFT
from scipy.signal._short_time_fft import PAD_TYPE, FFT_MODE_TYPE
from typing import Any, BinaryIO, Literal, TypedDict, cast, overload
from collections.abc import Sequence
from Z0Z_tools import halfsine, makeDirsSafely
import functools
import io
import math
import numpy
import numpy.typing
import os
import resampy
import soundfile

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

# TODO how should I handle these?
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
parametersUniversal = {}

windowingFunctionCallableUniversal = windowingFunctionCallableDEFAULT
if not parametersUniversal:
	parametersUniversal = parametersDEFAULT

def getWaveformMetadata(listPathFilenames: Sequence[str | os.PathLike[str]], sampleRate: float) -> dict[int, WaveformMetadata]:
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

def readAudioFile(pathFilename: str | os.PathLike[Any] | BinaryIO, sampleRate: float | None = None) -> ndarray[tuple[Literal[2], int], dtype[float32]]:
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
			waveform: NDArray[float32] = readSoundFile.read(dtype='float32', always_2d=True).astype(float32)
			# GitHub #3 Implement semantic axes for audio data
			axisTime = 0; axisChannels = 1
			waveform = resampleWaveform(waveform, sampleRateDesired=sampleRate, sampleRateSource=sampleRateSource, axisTime=axisTime)
			if waveform.shape[axisChannels] == 1:
				waveform = numpy.repeat(waveform, 2, axis=axisChannels)
			return numpy.transpose(waveform, axes=(axisChannels, axisTime))
	except soundfile.LibsndfileError as ERRORmessage:
		if 'System error' in str(ERRORmessage):
			raise FileNotFoundError(f"File not found: {pathFilename}") from ERRORmessage
		else:
			raise

def resampleWaveform(waveform: NDArray[floating[Any]], sampleRateDesired: float, sampleRateSource: float, axisTime: int = -1) -> NDArray[float32]:
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
		waveformResampled: NDArray[float32] = resampy.resample(waveform, sampleRateSource, sampleRateDesired, axis=axisTime)
		return waveformResampled
	else:
		return waveform

def loadWaveforms(listPathFilenames: Sequence[str | os.PathLike[str]], sampleRateTarget: float | None = None) -> ndarray[tuple[int, int, int], dtype[float32]]:
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
	dictionaryWaveformMetadata = getWaveformMetadata(listPathFilenames, sampleRateTarget)

	samplesTotalMaximum = max([entry['lengthWaveform'] + entry['samplesLeading'] + entry['samplesTrailing'] for entry in dictionaryWaveformMetadata.values()])
	axesSizes['axisTime'] = samplesTotalMaximum

	for keyName, axisSize in axesSizes.items():
		axisNormalized: int = (axisOrderMapping[keyName] + countAxes) % countAxes
		listShapeIndexToSize[axisNormalized] = axisSize
	tupleShapeArray = cast(tuple[int, int, int], tuple(listShapeIndexToSize))

	# `numpy.zeros` so that shorter waveforms are safely padded with zeros
	arrayWaveforms: ndarray[tuple[int, int, int], dtype[float32]] = numpy.zeros(tupleShapeArray, dtype=float32)

	for index, metadata in dictionaryWaveformMetadata.items():
		waveform = readAudioFile(metadata['pathFilename'], sampleRateTarget)
		samplesTrailing = metadata['lengthWaveform'] + metadata['samplesLeading'] - samplesTotalMaximum
		if samplesTrailing == 0:
			samplesTrailing = None
		# padding logic, entry['samplesLeading'] + entry['samplesTrailing'], goes here
		"""TODO padding logic; thoughts about the following statement.
		If my goal were to reduce the chances of an exception, especially a broadcast exception, in the next statement,
		then I would slice the insertion like this:
		`arrayWaveforms[:, metadata['samplesLeading'] : metadata['samplesLeading'] + waveform.shape[axisTime], index] = waveform`
		That would ensure that the exact length of the waveform that was just loaded would be used as the length of the slice.
		In rare cases, samplesLeading+lengthWaveform might be too long, which would cause an exception. And if that were to happen,
		the actual cause of the problem would almost certainly be upstream from here: that would make it harder to troubleshoot. Also,
		preallocating arrayWaveforms assumes precision; padding multiple waveforms with leading and or trailing requires precision:
		precision to the exact sample. The following statement doesn't affect precision, but if there is a precision problem,
		then the following statement could be affected by it and raise an exception: fail early. If the padding logic is implemented,
		I think the best form of the state will be:
		`arrayWaveforms[:, metadata['samplesLeading']:-metadata['samplesTrailing'], index] = waveform`
		If any of the upstream calculations is wrong, then the above statement would likely induce a broadcasting exception: fail early.

		I don't have padding logic right now, but I constructed the tedious `samplesTrailing` logic because it is slightly more likely
		to fail early than the alternative and because if I were to implement the padding logic, during refactoring, I would be more
		likely to notice this tedious logic and remember to implement the idea above.
		"""
		arrayWaveforms[:, metadata['samplesLeading']:samplesTrailing, index] = waveform

	return arrayWaveforms

def writeWAV(pathFilename: str | os.PathLike[Any] | io.IOBase, waveform: ndarray[tuple[int, ...], dtype[floating[Any] | integer[Any]]], sampleRate: float | None = None) -> None:
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
	soundfile.write(file=pathFilename, data=waveform.T, samplerate=sampleRate, subtype='FLOAT', format='WAV')

@overload # stft, one waveform
def stft(arrayTarget: ndarray[tuple[int, int], dtype[floating[Any] | integer[Any]]]
		, *
		, sampleRate: float | None = None
		, lengthHop: int | None = None
		, windowingFunction: ndarray[tuple[int], dtype[floating[Any]]] | None = None
		, lengthWindowingFunction: int | None = None
		, lengthFFT: int | None = None
		, inverse: Literal[False] = False
		, lengthWaveform: None = None
		, indexingAxis: Literal[None] = None
		) -> ndarray[tuple[int, int, int], dtype[complexfloating[Any, Any]]]: ...

@overload # stft, array of waveforms
def stft(arrayTarget: ndarray[tuple[int, int, int], dtype[floating[Any] | integer[Any]]]
		, *
		, sampleRate: float | None = None
		, lengthHop: int | None = None
		, windowingFunction: ndarray[tuple[int], dtype[floating[Any]]] | None = None
		, lengthWindowingFunction: int | None = None
		, lengthFFT: int | None = None
		, inverse: Literal[False] = False
		, lengthWaveform: None = None
		, indexingAxis: int = -1
		) -> ndarray[tuple[int, int, int, int], dtype[complexfloating[Any, Any]]]: ...

@overload # istft, one spectrogram
def stft(arrayTarget: ndarray[tuple[int, int, int], dtype[complexfloating[Any, Any] | floating[Any]]]
		, *
		, sampleRate: float | None = None
		, lengthHop: int | None = None
		, windowingFunction: ndarray[tuple[int], dtype[floating[Any]]] | None = None
		, lengthWindowingFunction: int | None = None
		, lengthFFT: int | None = None
		, inverse: Literal[True]
		, lengthWaveform: int
		, indexingAxis: Literal[None] = None
		) -> ndarray[tuple[int, int], dtype[floating[Any]]]: ...

@overload # istft, array of spectrograms
def stft(arrayTarget: ndarray[tuple[int, int, int, int], dtype[complexfloating[Any, Any]]]
		, *
		, sampleRate: float | None = None
		, lengthHop: int | None = None
		, windowingFunction: ndarray[tuple[int], dtype[floating[Any]]] | None = None
		, lengthWindowingFunction: int | None = None
		, lengthFFT: int | None = None
		, inverse: Literal[True]
		, lengthWaveform: int
		, indexingAxis: int = -1
		) -> ndarray[tuple[int, int, int], dtype[floating[Any]]]: ...

def stft(arrayTarget: (ndarray[tuple[int, int], 		   dtype[floating[Any] | integer[Any]]]
						 |   ndarray[tuple[int, int, int], 	   dtype[floating[Any] | integer[Any]]]
						 |   ndarray[tuple[int, int, int], 	   dtype[complexfloating[Any, Any] | floating[Any]]]
						 |   ndarray[tuple[int, int, int, int], dtype[complexfloating[Any, Any]]])
		, *
		, sampleRate: float | None = None
		, lengthHop: int | None = None
		, windowingFunction: ndarray[tuple[int], dtype[floating[Any]]] | None = None
		, lengthWindowingFunction: int | None = None
		, lengthFFT: int | None = None
		, inverse: bool = False
		, lengthWaveform: int | None = None
		, indexingAxis: int | None = None
		) -> (ndarray[tuple[int, int], 		  dtype[floating[Any]]]
				 |  ndarray[tuple[int, int, int], 	  dtype[floating[Any]]]
				 |  ndarray[tuple[int, int, int], 	  dtype[complexfloating[Any, Any]]]
				 |  ndarray[tuple[int, int, int, int], dtype[complexfloating[Any, Any]]]):
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
		lengthFFT = 2 ** math.ceil(math.log2(lengthWindowingFunction))

	if inverse and not lengthWaveform:
		raise ValueError("lengthWaveform must be specified for inverse transform")

	stftWorkhorse = ShortTimeFFT(win=windowingFunction, hop=lengthHop, fs=sampleRate, mfft=lengthFFT, **parametersShortTimeFFTUniversal)

	@overload
	def doTransformation(arrayInput: 	   ndarray[tuple[int, int, int], 	   dtype[complexfloating[Any, Any] | floating[Any]]]
										, lengthWaveform: int, inverse: Literal[True] = True
								) -> 	   ndarray[tuple[int, int], 		   dtype[floating[Any]]]: ...
	@overload
	def doTransformation(arrayInput: 	   ndarray[tuple[int, int], 		   dtype[floating[Any] | integer[Any]]]
										, lengthWaveform: Literal[None] = None, inverse: Literal[False] = False
								) -> 	   ndarray[tuple[int, int, int],	   dtype[complexfloating[Any, Any]]]: ...
	def doTransformation(arrayInput: (ndarray[tuple[int, int], 		   dtype[floating[Any] | integer[Any]]]
										 |  ndarray[tuple[int, int, int], 	   dtype[complexfloating[Any, Any] | floating[Any]]])
										, lengthWaveform: int | None = lengthWaveform, inverse: bool | None = inverse
								) -> (ndarray[tuple[int, int], 		   dtype[floating[Any]]]
										 |  ndarray[tuple[int, int, int], 	   dtype[complexfloating[Any, Any]]]):
		if inverse:
			return stftWorkhorse.istft(S=arrayInput, k1=lengthWaveform)
		return stftWorkhorse.stft(x=arrayInput, **parametersSTFTUniversal)

	# No overloads for "doTransformation" match the provided arguments Pylance(reportCallIssue)
	# Pylance, why do you hate me?
	if indexingAxis is None:
		return doTransformation(arrayTarget, inverse=inverse, lengthWaveform=lengthWaveform) # type: ignore

	arrayTARGET = numpy.moveaxis(arrayTarget, indexingAxis, -1)
	index = 0
	arrayTransformed = numpy.tile(doTransformation(arrayTARGET[..., index], inverse, lengthWaveform)[..., numpy.newaxis], arrayTARGET.shape[-1]) # type: ignore

	for index in range(1, arrayTARGET.shape[-1]):
		arrayTransformed[..., index] = doTransformation(arrayTARGET[..., index], inverse, lengthWaveform) # type: ignore

	return numpy.moveaxis(arrayTransformed, -1, indexingAxis)

def loadSpectrograms(listPathFilenames: Sequence[str | os.PathLike[str]]
					, sampleRateTarget: float | None = None
					, **parametersSTFT: Any
					) -> tuple[ndarray[tuple[int, int, int, int], dtype[complex64]], dict[int, WaveformMetadata]]:
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

	# TODO padding logic
	dictionaryWaveformMetadata = getWaveformMetadata(listPathFilenames, sampleRateTarget)

	samplesTotalMaximum = max([entry['lengthWaveform'] + entry['samplesLeading'] + entry['samplesTrailing'] for entry in dictionaryWaveformMetadata.values()])

	countChannels = 2
	spectrogramArchetype: ndarray[tuple[int, int, int], dtype[complex64]] = stft(numpy.zeros(shape=(countChannels, samplesTotalMaximum), dtype=float32), sampleRate=sampleRateTarget, **parametersSTFT)
	arraySpectrograms = numpy.zeros(shape=(*spectrogramArchetype.shape, len(dictionaryWaveformMetadata)), dtype=numpy.complex64)

	for index, metadata in dictionaryWaveformMetadata.items():
		waveform = readAudioFile(metadata['pathFilename'], sampleRateTarget)
		# padding logic, entry['samplesLeading'] + entry['samplesTrailing'], goes here
		arraySpectrograms[..., index] = stft(waveform, sampleRate=sampleRateTarget, **parametersSTFT)

	return arraySpectrograms, dictionaryWaveformMetadata

def spectrogramToWAV( spectrogram: ndarray[tuple[int, int, int], dtype[complexfloating[Any, Any] | floating[Any]]]
					, pathFilename: str | os.PathLike[Any] | io.IOBase
					, lengthWaveform: int
					, sampleRate: float | None = None
					, **parametersSTFT: Any
					) -> None:
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

	makeDirsSafely(pathFilename)
	waveform = stft(spectrogram, inverse=True, lengthWaveform=lengthWaveform, sampleRate=sampleRate, **parametersSTFT)
	writeWAV(pathFilename, waveform, sampleRate)

# TODO inspect this for integration
def waveformSpectrogramWaveform(callableNeedsSpectrogram):
	@functools.wraps(wrapped=callableNeedsSpectrogram)
	def stft_istft(waveform):
		axisTime=-1
		parametersSTFT={} # uh, I think this will be universal or default settings
		arrayTarget = stft(waveform, inverse=False, indexingAxis=None, **parametersSTFT)
		spectrogram = callableNeedsSpectrogram(arrayTarget)
		return stft(spectrogram, inverse=True, indexingAxis=None, lengthWaveform=waveform.shape[axisTime], **parametersSTFT)
	return stft_istft
