from numpy.typing import NDArray
from typing import Any, BinaryIO, Dict, List, Sequence, Tuple, Union
import librosa
import numpy
import os
import pathlib
import samplerate
import soundfile

def readAudioFile(pathFilename: Union[os.PathLike[Any], BinaryIO], sampleRate: int = 44100) -> NDArray[numpy.float32]:
    """
    Reads an audio file and returns its data as a NumPy array.

    Parameters:
        pathFilename: The path to the audio file.
        sampleRate (44100): The sample rate to use when reading the file. Defaults to 44100.

    Returns:
        waveform: The audio data in an array shaped (samples,) if there is only one channel or (channels, samples) if there is more than one channel.
    """
    # TODO: librosa needs to go.
    return librosa.load(path=pathFilename, sr=sampleRate, mono=False)[0]

def writeWav(pathFilename: Union[os.PathLike[Any], BinaryIO], waveform: NDArray[numpy.float64], sampleRate: int = 44100) -> None:
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
    try:
        if not isinstance(pathFilename, BinaryIO):
            pathlib.Path(pathFilename).parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    soundfile.write(file=pathFilename, data=waveform.T, samplerate=sampleRate, subtype='FLOAT', format='WAV')


def loadWaveforms(listPathFilenames: Sequence[os.PathLike[str]], sampleRate: int = 44100) -> NDArray[numpy.float32]:
    """
    Load a list of audio files into a single array.
    Parameters:
        listPathFilenames: List of file paths to the audio files.
        sampleRate (44100): Target sample rate for the waveforms; the function will resample if necessary. Defaults to 44100.
    Returns:
        arrayWaveforms: A single NumPy array of shape (channels, COUNTsamplesMaximum, COUNTwaveforms)
    """
    axesOrdering: Dict[str, int] = {'indexingAxis': -1, 'axisTime': -2, 'axisChannels': 0}
    axesSizes: Dict[str, int] = {keyName: 1 for keyName in axesOrdering.keys()}
    COUNTaxes: int = len(axesOrdering)
    listShapeIndexToSize: List[int] = [9001] * COUNTaxes

    COUNTwaveforms: int = len(listPathFilenames)
    axesSizes['indexingAxis'] = COUNTwaveforms
    channels: int = 2
    axesSizes['axisChannels'] = channels

    def resampleWaveform(waveform: NDArray[numpy.float32], sampleRateTarget: int, sampleRateActual: int) -> NDArray[numpy.float32]:
        converter: str = 'sinc_best'
        if sampleRateActual != sampleRateTarget:
            ratio: float = sampleRateTarget / sampleRateActual
            return samplerate.resample(waveform, ratio, converter)
        else:
            return waveform

    listCOUNTsamples: List[int] = []
    axisTime: int = 0
    
    for pathFilename in listPathFilenames:
        with soundfile.SoundFile(pathFilename) as readSoundFile:
            sampleRateSoundFile: int = readSoundFile.samplerate
            waveform: NDArray[numpy.float32] = readSoundFile.read(dtype='float32', always_2d=True).astype(numpy.float32)
            if sampleRateSoundFile != sampleRate:
                waveform = resampleWaveform(waveform, sampleRate, sampleRateSoundFile)
            listCOUNTsamples.append(waveform.shape[axisTime])
            
    COUNTsamplesMaximum: int = max(listCOUNTsamples)
    axesSizes['axisTime'] = COUNTsamplesMaximum

    for keyName, axisSize in axesSizes.items():
        axisNormalized: int = (axesOrdering[keyName] + COUNTaxes) % COUNTaxes
        listShapeIndexToSize[axisNormalized] = axisSize
    tupleShapeArray: Tuple[int, ...] = tuple(listShapeIndexToSize)

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