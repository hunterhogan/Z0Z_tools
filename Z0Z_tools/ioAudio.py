"""
Provides utilities for reading, writing, and resampling audio waveforms.
NOTE stft and loadSpectrograms are still in testing
"""
from Z0Z_tools import halfsine
from numpy.typing import NDArray
from scipy.signal import ShortTimeFFT
from typing import Any, BinaryIO, Dict, List, Literal, Optional, Sequence, Tuple, Union, overload
import collections
import io
import math
import numpy
import numpy.typing
import os
import pathlib
import resampy
import soundfile

# TODO consider changing all sample rates to float
# convert loadSpectrograms to stft

def loadSpectrograms(listPathFilenames: Sequence[str] | Sequence[os.PathLike[Any]], sampleRateTarget: int = 44100, binsFFT: int = 2048, hopLength: int = 512) -> Tuple[NDArray[numpy.complex64], List[Dict[str, int]]]:
    """
    Load spectrograms from audio files.

    Parameters:
        listPathFilenames: A list of file paths.
        sampleRateTarget (44100): The target sample rate. Defaults to 44100.
        binsFFT (2048): The number of FFT bins. Defaults to 2048.
        hopLength (1024): The hop length for the STFT. Defaults to 1024.

    Returns:
        tupleSpectrogramsCOUNTsamples: A tuple containing the array of spectrograms and a list of metadata dictionaries for each spectrogram.
    """
    dictionaryMetadata = collections.defaultdict(dict)
    for pathFilename in listPathFilenames:
        waveform = readAudioFile(pathFilename, sampleRateTarget)
        COUNTsamples = waveform.shape[-1]
        COUNTchannels = 1 if len(waveform.shape) == 1 else waveform.shape[0]
        dictionaryMetadata[pathFilename] = {
            'COUNTchannels': COUNTchannels,
            'COUNTsamples': COUNTsamples,
            'samplesLeading': 0,
            'samplesTrailing': 0,
            'samplesTotal': COUNTsamples
        }

    samplesTotal = max(entry['samplesTotal'] for entry in dictionaryMetadata.values())

    COUNTchannels = max(entry['COUNTchannels'] for entry in dictionaryMetadata.values())
    spectrogramArchetype = stft(numpy.zeros(shape=(COUNTchannels, samplesTotal), dtype=numpy.float32), binsFFT=binsFFT, hopLength=hopLength)
    arraySpectrograms = numpy.zeros(shape=(*spectrogramArchetype.shape, len(dictionaryMetadata)), dtype=numpy.complex64)

    for index, (pathFilename, entry) in enumerate(dictionaryMetadata.items()):
        waveform = readAudioFile(pathFilename, sampleRateTarget)
        arraySpectrograms[..., index] = stft(waveform, binsFFT=binsFFT, hopLength=hopLength)

    return arraySpectrograms, [{'COUNTsamples': entry['COUNTsamples'], 'samplesLeading': entry['samplesLeading'], 'samplesTrailing': entry['samplesTrailing']} for entry in dictionaryMetadata.values()]

def loadWaveforms(listPathFilenames: Union[Sequence[str], Sequence[os.PathLike[str]]], sampleRate: int = 44100) -> NDArray[numpy.float32]:
    """
    Load a list of audio files into a single array.

    Parameters:
        listPathFilenames: List of file paths to the audio files.
        sampleRate (44100): Target sample rate for the waveforms; the function will resample if necessary. Defaults to 44100.
    Returns:
        arrayWaveforms: A single NumPy array of shape (COUNTchannels, COUNTsamplesMaximum, COUNTwaveforms)
    """
    axisOrderMapping: Dict[str, int] = {'indexingAxis': -1, 'axisTime': -2, 'axisChannels': 0}
    axesSizes: Dict[str, int] = {keyName: 1 for keyName in axisOrderMapping.keys()}
    COUNTaxes: int = len(axisOrderMapping)
    listShapeIndexToSize: List[int] = [9001] * COUNTaxes

    COUNTwaveforms: int = len(listPathFilenames)
    axesSizes['indexingAxis'] = COUNTwaveforms
    COUNTchannels: int = 2
    axesSizes['axisChannels'] = COUNTchannels

    listCOUNTsamples: List[int] = []
    axisTime: int = 0
    for pathFilename in listPathFilenames:
        try:
            with soundfile.SoundFile(pathFilename) as readSoundFile:
                sampleRateSoundFile: int = readSoundFile.samplerate
                waveform: NDArray[numpy.float32] = readSoundFile.read(dtype='float32', always_2d=True).astype(numpy.float32)
                if sampleRateSoundFile != sampleRate:
                    waveform = resampleWaveform(waveform, sampleRate, sampleRateSoundFile)
                listCOUNTsamples.append(waveform.shape[axisTime])
        except soundfile.LibsndfileError as ERRORmessage:
            if 'System error' in str(ERRORmessage):
                raise FileNotFoundError(f"File not found: {pathFilename}") from ERRORmessage
            else:
                raise

    COUNTsamplesMaximum: int = max(listCOUNTsamples)
    axesSizes['axisTime'] = COUNTsamplesMaximum

    for keyName, axisSize in axesSizes.items():
        axisNormalized: int = (axisOrderMapping[keyName] + COUNTaxes) % COUNTaxes
        listShapeIndexToSize[axisNormalized] = axisSize
    tupleShapeArray: Tuple[int, ...] = tuple(listShapeIndexToSize)

    # `numpy.zeros` so that shorter waveforms are safely padded with zeros
    arrayWaveforms: NDArray[numpy.float32] = numpy.zeros(tupleShapeArray, dtype=numpy.float32)

    for index in range(COUNTwaveforms):
        with soundfile.SoundFile(listPathFilenames[index]) as readSoundFile:
            sampleRateSoundFile: int = readSoundFile.samplerate
            waveform: NDArray[numpy.float32] = readSoundFile.read(dtype='float32', always_2d=True).astype(numpy.float32)

            if sampleRateSoundFile != sampleRate:
                waveform = resampleWaveform(waveform, sampleRate, sampleRateSoundFile)

            COUNTsamples: int = waveform.shape[axisTime]
            arrayWaveforms[:, 0:COUNTsamples, index] = waveform.T

    return arrayWaveforms

def readAudioFile(pathFilename: Union[str, os.PathLike[Any], BinaryIO], sampleRate: int = 44100
                    ) -> numpy.ndarray[Tuple[Literal[2], int], numpy.dtype[numpy.float32]]:
    """
    Reads an audio file and returns its data as a NumPy array. Mono is always converted to stereo.

    Parameters:
        pathFilename: The path to the audio file.
        sampleRate (44100): The sample rate to use when reading the file. Defaults to 44100.

    Returns:
        waveform: The audio data in an array shaped (channels, samples).
    """
    try:
        with soundfile.SoundFile(pathFilename) as readSoundFile:
            sampleRateSource: int = readSoundFile.samplerate
            waveform: NDArray[numpy.float32] = readSoundFile.read(dtype='float32', always_2d=True).astype(numpy.float32)
            waveform = resampleWaveform(waveform, sampleRateDesired=sampleRate, sampleRateSource=sampleRateSource)
            # If the audio is mono (1 channel), convert it to stereo by duplicating the channel
            if waveform.shape[1] == 1:
                waveform = numpy.repeat(waveform, 2, axis=1)
            return waveform.T
    except soundfile.LibsndfileError as ERRORmessage:
        if 'System error' in str(ERRORmessage):
            raise FileNotFoundError(f"File not found: {pathFilename}") from ERRORmessage
        else:
            raise

def resampleWaveform(waveform: NDArray[numpy.float32], sampleRateDesired: int, sampleRateSource: int) -> NDArray[numpy.float32]:
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
        waveformResampled: NDArray[numpy.float32] = resampy.resample(waveform, sampleRateSource, sampleRateDesired, axis=0)
        return waveformResampled
    else:
        return waveform

@overload
def stft(arrayTarget: NDArray[numpy.floating[Any]], *, sampleRate: float = 44100.0,
        hopLength: int = 512, window: Optional[NDArray[numpy.floating[Any]]] = None,
        lengthWindow: Optional[int] = None, binsFFT: Optional[int] = None,
        inverse: Literal[False] = False, lengthWaveform: None = None,
        indexingAxis: Optional[int] = None) -> NDArray[numpy.complexfloating[Any, Any]]: ...

@overload
def stft(arrayTarget: NDArray[numpy.complexfloating[Any, Any]], *, sampleRate: float = 44100.0,
        hopLength: int = 512, window: Optional[NDArray[numpy.floating[Any]]] = None,
        lengthWindow: Optional[int] = None, binsFFT: Optional[int] = None,
        inverse: Literal[True], lengthWaveform: int,
        indexingAxis: Optional[int] = None) -> NDArray[numpy.floating[Any]]: ...

def stft(arrayTarget: NDArray[numpy.floating[Any] | numpy.complexfloating[Any, Any]], *,
        sampleRate: float = 44100.0, hopLength: int = 512,
        window: Optional[NDArray[numpy.floating[Any]]] = None,
        lengthWindow: Optional[int] = None, binsFFT: Optional[int] = None,
        inverse: bool = False, lengthWaveform: Optional[int] = None,
        indexingAxis: Optional[int] = None) -> NDArray[numpy.floating[Any] | numpy.complexfloating[Any, Any]]:
    """
    Short-Time Fourier Transform with unified interface for forward and inverse transforms.

    Parameters:
        arrayTarget: Input array for transformation.
        sampleRate (44100): Sample rate of the signal.
        hopLength (512): Number of samples between successive frames.
        window (halfsine*): Window function array. Defaults to halfsine if None.
        lengthWindow (1024*): Length of the window. Used if window is None.
        binsFFT: Number of FFT bins. Defaults to next power of 2 >= lengthWindow.
        inverse (False*): Whether to perform inverse transform.
        lengthWaveform: Required output length for inverse transform.
        indexingAxis (None): Axis containing multiple signals to transform.

    Returns:
        arrayTransformed: The transformed signal(s).
    """
    if lengthWindow is None:
        lengthWindow = 1024

    if window is None:
        window = halfsine(lengthWindow)

    if binsFFT is None:
        binsFFT = 2 ** math.ceil(math.log2(lengthWindow))

    if inverse and lengthWaveform is None:
        raise ValueError("lengthWaveform must be specified for inverse transform")

    STFTmanager = ShortTimeFFT(win=window, hop=hopLength, fs=sampleRate, fft_mode='onesided', mfft=binsFFT)

    def applyTransform(arrayInput: NDArray) -> NDArray:
        if inverse:
            return STFTmanager.istft(S=arrayInput, k1=lengthWaveform)
        return STFTmanager.stft(x=arrayInput, padding='even')

    if indexingAxis is None:
        return applyTransform(arrayTarget)

    arrayTARGET = numpy.moveaxis(arrayTarget, indexingAxis, -1)
    arrayTransformed = numpy.tile(applyTransform(arrayTARGET[..., 0])[..., numpy.newaxis], arrayTARGET.shape[-1])

    for index in range(1, arrayTARGET.shape[-1]):
        arrayTransformed[..., index] = applyTransform(arrayTARGET[..., index])

    return numpy.moveaxis(arrayTransformed, -1, indexingAxis)

def writeWAV(pathFilename: Union[str, os.PathLike[Any], io.IOBase], waveform: NDArray[Any], sampleRate: int = 44100) -> None:
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
    if not isinstance(pathFilename, io.IOBase):
        try:
            pathlib.Path(pathFilename).parent.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass
    soundfile.write(file=pathFilename, data=waveform.T, samplerate=sampleRate, subtype='FLOAT', format='WAV')
