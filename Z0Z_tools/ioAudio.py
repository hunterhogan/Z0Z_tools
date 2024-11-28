import io
import os
import pathlib
from typing import Any, BinaryIO, Dict, List, Sequence, Tuple, Union

import numpy
import resampy
import soundfile
from numpy.typing import NDArray


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

def readAudioFile(pathFilename: Union[str, os.PathLike[Any], BinaryIO], sampleRate: int = 44100) -> NDArray[numpy.float32]:
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

def writeWav(pathFilename: Union[str, os.PathLike[Any], io.IOBase], waveform: NDArray[Any], sampleRate: int = 44100) -> None:
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
