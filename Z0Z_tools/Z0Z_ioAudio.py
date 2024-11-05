from concurrent.futures import ProcessPoolExecutor, as_completed
from numpy.typing import NDArray
from os import PathLike
from typing import BinaryIO, Collection
import librosa
import multiprocessing
import numpy
import pathlib
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
    # TODO: soundfile needs to go.
    try:
        if not isinstance(pathFilename, BinaryIO):
            pathlib.Path(pathFilename).parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    soundfile.write(file=pathFilename, data=waveform.T, samplerate=sampleRate, subtype='FLOAT', format='WAV')

def loadWaveforms(listPathFilenames: Collection[PathLike | BinaryIO], sampleRate: int = 44100) -> NDArray[numpy.float32]:
    """
    Load multiple audio waveforms from a list of file paths into a single NumPy array.

    Parameters:
        listPathFilenames: List of file paths to the audio files.
        sampleRate (44100): The sample rate to use when reading the audio files. Defaults to 44100.

    Returns:
        arrayWaveforms: The audio data in an array shaped (..., samples, COUNTwaveforms), where
            - (samples, COUNTwaveforms) if there is only one channel
            - or (channels, samples, COUNTwaveforms) if there is more than one channel
            - samples: Number of audio samples per channel.
            - COUNTwaveforms: Number of waveforms loaded (equal to the length of listPathFilenames).
    """
    listPathFilenames = list(listPathFilenames)
    COUNTwaveforms = len(listPathFilenames)
    arrayWaveforms = numpy.tile(readAudioFile(listPathFilenames[0], sampleRate=sampleRate)[..., numpy.newaxis], COUNTwaveforms)

    with ProcessPoolExecutor() as concurrencyManager:
        dictionaryConcurrency = {concurrencyManager.submit(readAudioFile, listPathFilenames[index], sampleRate=sampleRate): index for index in range(1, COUNTwaveforms)}
        for claimTicket in as_completed(dictionaryConcurrency):
            arrayWaveforms[..., dictionaryConcurrency[claimTicket]] = claimTicket.result()
    return arrayWaveforms
