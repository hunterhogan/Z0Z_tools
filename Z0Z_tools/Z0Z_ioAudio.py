from numpy.typing import NDArray
from os import PathLike
from typing import BinaryIO, Sequence
import librosa
import multiprocessing
import numpy
import pathlib
import samplerate
import soundfile

if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')

def readAudioFile(pathFilename: PathLike | BinaryIO, sampleRate: int = 44100) -> NDArray[numpy.float32]:
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

def writeWav(pathFilename: PathLike | BinaryIO, waveform: NDArray, sampleRate: int = 44100) -> None:
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

# def loadWaveforms(listPathFilenames: Iterable[PathLike], sampleRate: int = 44100) -> NDArray[numpy.float32]:
#     """
#     Load multiple audio waveforms from a list of file paths into a single NumPy array.

#     Parameters:
#         listPathFilenames: List of file paths to the audio files.
#         sampleRate (44100): The sample rate to use when reading the audio files. Defaults to 44100.

#     Returns:
#         arrayWaveforms: The audio data in an array shaped (..., samples, COUNTwaveforms), where
#             - (samples, COUNTwaveforms) if there is only one channel
#             - or (channels, samples, COUNTwaveforms) if there is more than one channel
#             - samples: Number of audio samples per channel.
#             - COUNTwaveforms: Number of waveforms loaded (equal to the length of listPathFilenames).
#     """
#     listPathFilenames = list(listPathFilenames)
#     listPathFilenames = [pathlib.Path(pathFilename) for pathFilename in listPathFilenames]
#     COUNTwaveforms = len(listPathFilenames)
#     arrayWaveforms = numpy.tile(readAudioFile(listPathFilenames[0], sampleRate=sampleRate)[..., numpy.newaxis], COUNTwaveforms)

#     with ProcessPoolExecutor() as concurrencyManager:
#         dictionaryConcurrency = {concurrencyManager.submit(readAudioFile, listPathFilenames[index], sampleRate=sampleRate): index for index in range(1, COUNTwaveforms)}
#         for claimTicket in as_completed(dictionaryConcurrency):
#             arrayWaveforms[..., dictionaryConcurrency[claimTicket]] = claimTicket.result()
#     return arrayWaveforms

def loadWaveforms(listPathFilenames: Sequence[PathLike], sampleRate: int = 44100) -> NDArray[numpy.float32]:
    """
    Load a list of audio files into a single array.
    Parameters:
        listPathFilenames: List of file paths to the audio files.
        sampleRate (44100): Target sample rate for the waveforms; the function will resample if necessary. Defaults to 44100.
    Returns:
        arrayWaveforms: A single NumPy array of shape (channels, COUNTsamplesMaximum, COUNTwaveforms) such that
            - channels: always 2; mono is converted to stereo if necessary,
            - COUNTsamplesMaximum: shorter waveforms are appended with zeros if necessary,
            - COUNTwaveforms: waveforms are indexed on the last axis, for example, `[..., index]`.
    """
    axesOrdering = {'indexingAxis': -1, 'axisTime': -2, 'axisChannels': 0}
    axesSizes: dict[str, int] = {keyName: 1 for keyName in axesOrdering.keys()}
    COUNTaxes = len(axesOrdering)
    listShapeIndexToSize = [9001] * COUNTaxes

    COUNTwaveforms = len(listPathFilenames)
    axesSizes['indexingAxis'] = COUNTwaveforms
    channels = 2
    axesSizes['axisChannels'] = channels

    def resampleWaveform(waveform: NDArray[numpy.float32], sampleRateTarget: int, sampleRateActual: int) -> NDArray[numpy.float32]:
        converter = 'sinc_best'
        if sampleRateActual != sampleRateTarget:
            ratio = sampleRateTarget / sampleRateActual
            return samplerate.resample(waveform, ratio, converter)
        else:
            return waveform

    listCOUNTsamples = []
    # Find the maximum number of samples in the list of waveforms
    axisTime = 0
    for pathFilename in listPathFilenames:
        with soundfile.SoundFile(pathFilename) as readSoundFile:
            sampleRateSoundFile = readSoundFile.samplerate
            waveform = readSoundFile.read(dtype='float32', always_2d=True).astype(numpy.float32)
            if sampleRateSoundFile != sampleRate:
                waveform = resampleWaveform(waveform, sampleRate, sampleRateSoundFile)
            listCOUNTsamples.append(waveform.shape[axisTime])
    COUNTsamplesMaximum = max(listCOUNTsamples)
    axesSizes['axisTime'] = COUNTsamplesMaximum

    for keyName, axisSize in axesSizes.items():
        axisNormalized = (axesOrdering[keyName] + COUNTaxes) % COUNTaxes
        listShapeIndexToSize[axisNormalized] = axisSize
    tupleShapeArray = tuple(listShapeIndexToSize)

    arrayWaveforms = numpy.zeros(tupleShapeArray, dtype=numpy.float32)

    for index in range(COUNTwaveforms):
        with soundfile.SoundFile(listPathFilenames[index]) as readSoundFile:
            sampleRateSoundFile = readSoundFile.samplerate
            waveform = readSoundFile.read(dtype='float32', always_2d=True).astype(numpy.float32)

            if sampleRateSoundFile != sampleRate:
                waveform = resampleWaveform(waveform, sampleRate, sampleRateSoundFile)

            COUNTsamples = waveform.shape[axisTime]
            arrayWaveforms[:, 0:COUNTsamples, index] = waveform.T  # Direct assignment to the pre-allocated array

    return arrayWaveforms
