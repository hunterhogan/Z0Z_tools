"""
Provides utilities for reading, writing, and resampling audio waveforms.
"""
from random import sample
from numpy import dtype, floating, ndarray, float32, complexfloating, complex64
from numpy.typing import NDArray
from scipy.signal import ShortTimeFFT
from typing import Any, BinaryIO, Dict, List, Literal, Optional, overload, Sequence, TypedDict, Tuple, Union
from Z0Z_tools import halfsine, makeDirsSafely
import collections
import functools
import io
import math
import numpy
import numpy.typing
import os
import pathlib
import resampy
import soundfile

class ParametersUniversal(TypedDict):
	lengthFFT: int
	lengthHop: int
	lengthWindowingFunction: int
	sampleRate: float
	windowingFunction: ndarray[Tuple[int], dtype[floating[Any]]]

lengthWindowDEFAULT = 1024
windowCallableDEFAULT = halfsine
parametersDEFAULT = ParametersUniversal (
	lengthFFT=2048,
	lengthHop=512,
	lengthWindowingFunction=lengthWindowDEFAULT,
	sampleRate=44100,
	windowingFunction=windowCallableDEFAULT(lengthWindowDEFAULT),
)

# No, I don't know how to implement this, but I might learn how to do it later.
# If you know how, you can help. :D
parametersUniversal = {}

windowCallableUniversal = windowCallableDEFAULT
if not parametersUniversal:
	parametersUniversal = parametersDEFAULT

# TODO
# change sample rates to float
# types
# docstrings
# semiotics: WAV means the file format; waveform is a data concept. Don't use "Wav" or "wav" anymore because it is ambiguous.
# semiotics: windowing function is the correct name for the array of numbers. "window" is a diminutive form used by programmers, and it creates ambiguity. (To be fair, the signal processing folks naming it "windowing function" was pretty lame.)
# semiotics: choose lengthWaveform or COUNTsamples

def readAudioFile(pathFilename: Union[str, os.PathLike[Any], BinaryIO], sampleRate: Optional[float] = None) -> ndarray[Tuple[Literal[2], int], dtype[float32]]:
	"""
	Reads an audio file and returns its data as a NumPy array. Mono is always converted to stereo.

	Parameters:
		pathFilename: The path to the audio file.
		sampleRate (44100): The sample rate to use when reading the file. Defaults to 44100.

	Returns:
		waveform: The audio data in an array shaped (channels, samples).
	"""
	if sampleRate is None:
		sampleRate = parametersUniversal['sampleRate']
	try:
		with soundfile.SoundFile(pathFilename) as readSoundFile:
			sampleRateSource: int = readSoundFile.samplerate
			waveform: NDArray[float32] = readSoundFile.read(dtype='float32', always_2d=True).astype(float32)
			waveform = resampleWaveform(waveform, sampleRateDesired=sampleRate, sampleRateSource=sampleRateSource, axisTime=0)
			# If the audio is mono (1 channel), convert it to stereo by duplicating the channel
			if waveform.shape[1] == 1:
				waveform = numpy.repeat(waveform, 2, axis=1)
			return waveform.T
	except soundfile.LibsndfileError as ERRORmessage:
		if 'System error' in str(ERRORmessage):
			raise FileNotFoundError(f"File not found: {pathFilename}") from ERRORmessage
		else:
			raise

def resampleWaveform(waveform: NDArray[float32], sampleRateDesired: float, sampleRateSource: float, axisTime: int = -1) -> NDArray[float32]:
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

def loadWaveforms(listPathFilenames: Union[Sequence[str], Sequence[os.PathLike[str]]], sampleRate: Optional[float] = None) -> ndarray[Tuple[int, int, int], dtype[float32]]:
	"""
	Load a list of audio files into a single array.

	Parameters:
		listPathFilenames: List of file paths to the audio files.
		sampleRate (44100): Target sample rate for the waveforms; the function will resample if necessary. Defaults to 44100.
	Returns:
		arrayWaveforms: A single NumPy array of shape (COUNTchannels, COUNTsamplesMaximum, COUNTwaveforms)
	"""
	if sampleRate is None:
		sampleRate = parametersUniversal['sampleRate']
	axisOrderMapping: Dict[str, int] = {'indexingAxis': -1, 'axisTime': -2, 'axisChannels': 0}
	axesSizes: Dict[str, int] = {keyName: 1 for keyName in axisOrderMapping.keys()}
	COUNTaxes: int = len(axisOrderMapping)
	listShapeIndexToSize: List[int] = [9001] * COUNTaxes

	COUNTwaveforms: int = len(listPathFilenames)
	axesSizes['indexingAxis'] = COUNTwaveforms
	COUNTchannels: int = 2
	axesSizes['axisChannels'] = COUNTchannels

	listCOUNTsamples: List[int] = []
	axisTime: int = -1
	for pathFilename in listPathFilenames:
		listCOUNTsamples.append(readAudioFile(pathFilename).shape[axisTime])

	COUNTsamplesMaximum: int = max(listCOUNTsamples)
	axesSizes['axisTime'] = COUNTsamplesMaximum

	for keyName, axisSize in axesSizes.items():
		axisNormalized: int = (axisOrderMapping[keyName] + COUNTaxes) % COUNTaxes
		listShapeIndexToSize[axisNormalized] = axisSize
	tupleShapeArray: Tuple[int, int, int] = tuple(listShapeIndexToSize) # type: ignore

	# `numpy.zeros` so that shorter waveforms are safely padded with zeros
	arrayWaveforms: ndarray[Tuple[int, int, int], dtype[float32]] = numpy.zeros(tupleShapeArray, dtype=float32)

	for index in range(COUNTwaveforms):
		waveform = readAudioFile(listPathFilenames[index], sampleRate)
		COUNTsamples: int = waveform.shape[axisTime]
		arrayWaveforms[:, 0:COUNTsamples, index] = waveform

	return arrayWaveforms

def writeWAV(pathFilename: Union[str, os.PathLike[Any], io.IOBase], waveform: NDArray[Any], sampleRate: Optional[float] = None) -> None:
	"""
	Writes a waveform to a WAV file.

	Parameters:
		pathFilename: The path and filename where the WAV file will be saved.
		waveform: The waveform data to be written to the WAV file. The waveform should be in the shape (channels, samples).
		sampleRate (44100): The sample rate of the waveform. Defaults to 44100 Hz.

	Notes:
		The function will create any necessary directories if they do not exist.
		The function will overwrite the file if it already exists without prompting or informing the user.

	Returns:
		None:
	"""
	if sampleRate is None:
		sampleRate = parametersUniversal['sampleRate']
	makeDirsSafely(pathFilename)
	soundfile.write(file=pathFilename, data=waveform.T, samplerate=sampleRate, subtype='FLOAT', format='WAV')

@overload #stft, one waveform
def stft(arrayTarget: ndarray[Tuple[int, int], dtype[floating[Any]]]
		, *
		, sampleRate: Optional[float] = None
		, lengthHop: Optional[int] = None
		, windowingFunction: Optional[ndarray[Tuple[int], dtype[floating[Any]]]] = None
		, lengthWindowingFunction: Optional[int] = None
		, lengthFFT: Optional[int] = None
		, inverse: Literal[False] = False
		, lengthWaveform: None = None
		, indexingAxis: Literal[None] = None
		) -> ndarray[Tuple[int, int, int], dtype[complexfloating[Any, Any]]]: ...

@overload #stft, array of waveforms
def stft(arrayTarget: ndarray[Tuple[int, int, int], dtype[floating[Any]]]
		, *
		, sampleRate: Optional[float] = None
		, lengthHop: Optional[int] = None
		, windowingFunction: Optional[ndarray[Tuple[int], dtype[floating[Any]]]] = None
		, lengthWindowingFunction: Optional[int] = None
		, lengthFFT: Optional[int] = None
		, inverse: Literal[False] = False
		, lengthWaveform: None = None
		, indexingAxis: int = -1
		) -> ndarray[Tuple[int, int, int, int], dtype[complexfloating[Any, Any]]]: ...

@overload #istft, one spectrogram
def stft(arrayTarget: ndarray[Tuple[int, int, int], dtype[complexfloating[Any, Any]]]
		, *
		, sampleRate: Optional[float] = None
		, lengthHop: Optional[int] = None
		, windowingFunction: Optional[ndarray[Tuple[int], dtype[floating[Any]]]] = None
		, lengthWindowingFunction: Optional[int] = None
		, lengthFFT: Optional[int] = None
		, inverse: Literal[True]
		, lengthWaveform: int
		, indexingAxis: Literal[None] = None
		) -> ndarray[Tuple[int, int], dtype[floating[Any]]]: ...

@overload #istft, array of spectrograms
def stft(arrayTarget: ndarray[Tuple[int, int, int, int], dtype[complexfloating[Any, Any]]]
		, *
		, sampleRate: Optional[float] = None
		, lengthHop: Optional[int] = None
		, windowingFunction: Optional[ndarray[Tuple[int], dtype[floating[Any]]]] = None
		, lengthWindowingFunction: Optional[int] = None
		, lengthFFT: Optional[int] = None
		, inverse: Literal[True]
		, lengthWaveform: int
		, indexingAxis: int = -1
		) -> ndarray[Tuple[int, int, int], dtype[floating[Any]]]: ...

def stft(arrayTarget: Union[ndarray[Tuple[int, int], 		   dtype[floating[Any]]]
						,   ndarray[Tuple[int, int, int], 	   dtype[floating[Any]]]
						,   ndarray[Tuple[int, int, int], 	   dtype[complexfloating[Any, Any]]]
						,   ndarray[Tuple[int, int, int, int], dtype[complexfloating[Any, Any]]]]
		, *
		, sampleRate: Optional[float] = None
		, lengthHop: Optional[int] = None
		, windowingFunction: Optional[ndarray[Tuple[int], dtype[floating[Any]]]] = None
		, lengthWindowingFunction: Optional[int] = None
		, lengthFFT: Optional[int] = None
		, inverse: bool = False
		, lengthWaveform: Optional[int] = None
		, indexingAxis: Optional[int] = None
		) -> Union[ndarray[Tuple[int, int], 		  dtype[floating[Any]]]
				,  ndarray[Tuple[int, int, int], 	  dtype[floating[Any]]]
				,  ndarray[Tuple[int, int, int], 	  dtype[complexfloating[Any, Any]]]
				,  ndarray[Tuple[int, int, int, int], dtype[complexfloating[Any, Any]]]]:
	"""
	Short-Time Fourier Transform with unified interface for forward and inverse transforms.

	Parameters:
		arrayTarget: Input array for transformation.
		sampleRate (44100): Sample rate of the signal.
		lengthHop (512): Number of samples between successive frames.
		windowingFunction (halfsine): Windowing function array. Defaults to halfsine if None.
		lengthWindowingFunction (1024): Length of the windowing function. Used if windowingFunction is None.
		lengthFFT (2048): Number of FFT bins. Defaults to next power of 2 >= lengthWindowingFunction.
		inverse (False): Whether to perform inverse transform.
		lengthWaveform: Required output length for inverse transform.
		indexingAxis (None): Axis containing multiple signals to transform.

	Returns:
		arrayTransformed: The transformed signal(s).
	"""
	if sampleRate is None: sampleRate = parametersUniversal['sampleRate']
	if lengthHop is None: lengthHop = parametersUniversal['lengthHop']

	if windowingFunction is None:
		if lengthWindowingFunction is not None and (PylanceIsConfused := True) and windowCallableUniversal:
			windowingFunction = windowCallableUniversal(lengthWindowingFunction)
		else:
			windowingFunction = parametersUniversal['windowingFunction']

	if lengthFFT is None:
		lengthWindowingFunction = windowingFunction.size
		lengthFFT = 2 ** math.ceil(math.log2(lengthWindowingFunction))

	if inverse and lengthWaveform is None:
		raise ValueError("lengthWaveform must be specified for inverse transform")

	stftWorkhorse = ShortTimeFFT(win=windowingFunction, hop=lengthHop, fs=sampleRate, fft_mode='onesided', mfft=lengthFFT)

	def applyTransform(arrayInput: NDArray) -> NDArray:
		if inverse:
			return stftWorkhorse.istft(S=arrayInput, k1=lengthWaveform)
		return stftWorkhorse.stft(x=arrayInput, padding='even')

	if indexingAxis is None:
		return applyTransform(arrayTarget)

	arrayTARGET = numpy.moveaxis(arrayTarget, indexingAxis, -1)
	arrayTransformed = numpy.tile(applyTransform(arrayTARGET[..., 0])[..., numpy.newaxis], arrayTARGET.shape[-1])

	for index in range(1, arrayTARGET.shape[-1]):
		arrayTransformed[..., index] = applyTransform(arrayTARGET[..., index])

	return numpy.moveaxis(arrayTransformed, -1, indexingAxis)

def loadSpectrograms(listPathFilenames: Sequence[str] | Sequence[os.PathLike[Any]]
					, sampleRateTarget: Optional[float] = None
					, lengthHop: Optional[int] = None
					, windowingFunction: Optional[ndarray[Tuple[int], dtype[floating[Any]]]] = None
					, lengthWindowingFunction: Optional[int] = None
					, lengthFFT: Optional[int] = None
					) -> Tuple[ndarray[Tuple[int, int, int, int], dtype[complex64]], List[Dict[str, int]]]:
	"""
	Load spectrograms from audio files.

	Parameters:
		listPathFilenames: A list of file paths.
		sampleRateTarget (44100): The target sample rate. Defaults to 44100.
		lengthFFT (2048): The number of FFT bins. Defaults to 2048.
		lengthHop (1024): The hop length for the STFT. Defaults to 1024.

	Returns:
		tupleSpectrogramsCOUNTsamples: A tuple containing the array of spectrograms and a list of metadata dictionaries for each spectrogram.
	"""
	if sampleRateTarget is None:
		sampleRateTarget = parametersUniversal['sampleRate']

	parametersSTFT = {
		'sampleRate': sampleRateTarget,
		'lengthHop': lengthHop,
		'windowingFunction': windowingFunction,
		'lengthWindowingFunction': lengthWindowingFunction,
		'lengthFFT': lengthFFT,
	}

	# TODO listCOUNTsamples from loadWaveforms and dictionaryMetadata need to
	# converge and use the same code. dictionaryMetadata is setup to allow the calling
	# function to choose how to pad the waveforms. listCOUNTsamples enforces trailing zeros.
	dictionaryMetadata = collections.defaultdict(dict)
	axisTime: int = -1
	for pathFilename in listPathFilenames:
		COUNTsamples = readAudioFile(pathFilename).shape[axisTime]
		dictionaryMetadata[pathFilename] = {
			'COUNTsamples': COUNTsamples,
			'samplesLeading': 0,
			'samplesTrailing': 0,
			'samplesTotal': COUNTsamples
		}

	samplesTotal = max(entry['samplesTotal'] for entry in dictionaryMetadata.values())

	COUNTchannels = 2
	spectrogramArchetype = stft(numpy.zeros(shape=(COUNTchannels, samplesTotal), dtype=float32), **parametersSTFT)
	arraySpectrograms = numpy.zeros(shape=(*spectrogramArchetype.shape, len(dictionaryMetadata)), dtype=numpy.complex64)

	for index, (pathFilename, entry) in enumerate(dictionaryMetadata.items()):
		waveform = readAudioFile(pathFilename, sampleRateTarget)
		arraySpectrograms[..., index] = stft(waveform, **parametersSTFT)

	return arraySpectrograms, [{'COUNTsamples': entry['COUNTsamples'], 'samplesLeading': entry['samplesLeading'], 'samplesTrailing': entry['samplesTrailing']} for entry in dictionaryMetadata.values()]

def spectrogramToWAV(spectrogram: NDArray
					, pathFilename: Union[str, os.PathLike[Any], io.IOBase]
					, lengthWaveform: int
					, sampleRate: Optional[float] = None
					, lengthHop: Optional[int] = None
					, windowingFunction: Optional[ndarray[Tuple[int], dtype[floating[Any]]]] = None
					, lengthWindowingFunction: Optional[int] = None
					, lengthFFT: Optional[int] = None
					) -> None:
	"""
	Writes a complex spectrogram to a WAV file.

	Parameters:
		spectrogram: The complex spectrogram to be written to the file.
		pathFilename: Location for the file of the waveform output.
		COUNTsamples: n.b. Not optional: the length of the output waveform in samples.
		sampleRate (44100): The sample rate of the output waveform file. Defaults to 44100.

	Returns:
		None:
	"""
	if sampleRate is None:
		sampleRate = parametersUniversal['sampleRate']

	makeDirsSafely(pathFilename)
	waveform = stft(spectrogram, inverse=True, lengthWaveform=lengthWaveform, sampleRate=sampleRate, lengthHop=lengthHop, windowingFunction=windowingFunction, lengthWindowingFunction=lengthWindowingFunction, lengthFFT=lengthFFT)
	writeWAV(pathFilename, waveform, sampleRate)

def waveformSpectrogramWaveform(callableNeedsSpectrogram):
	@functools.wraps(wrapped=callableNeedsSpectrogram)
	def stft_istft(waveform):
		axisTime=-1
		parametersSTFT={}
		arrayTarget = stft(waveform, inverse=False, indexingAxis=None, **parametersSTFT)
		spectrogram = callableNeedsSpectrogram(arrayTarget)
		return stft(spectrogram, inverse=True, indexingAxis=None, lengthWaveform=waveform.shape[axisTime], **parametersSTFT)
	return stft_istft
