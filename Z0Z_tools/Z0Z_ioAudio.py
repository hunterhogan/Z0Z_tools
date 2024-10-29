from concurrent.futures import ProcessPoolExecutor, as_completed
from numpy.typing import NDArray
from os import PathLike
from pathlib import Path
from typing import BinaryIO, List
import librosa
import numpy
import soundfile

def readAudioFile(pathFilename: PathLike | BinaryIO, sampleRate: int = 44100) -> NDArray[numpy.float32]:
    """
    Reads an audio file and returns its data as a NumPy array.

    Parameters:
        pathFilename (str | Path): The path to the audio file.
        sampleRate (int, optional): The sample rate to use when reading the file. Defaults to 44100.

    Returns:
        waveform (NDArray[numpy.float32]): The audio data in an array shaped (samples,) if there is only one channel or (channels, samples) if there is more than one channel.
    """
    # TODO: librosa needs to go.
    return librosa.load(path=pathFilename, sr=sampleRate, mono=False)[0]

def writeWav(pathFilename: PathLike | BinaryIO, waveform: NDArray, sampleRate: int = 44100) -> None:
    """
    Writes a waveform to a WAV file.

    Parameters:
        pathFilename: (str): The path and filename where the WAV file will be saved.
        waveform: (NDArray): The waveform data to be written to the WAV file. The waveform should be in the shape (channels, samples).
        sampleRate: (int, optional): The sample rate of the waveform. Defaults to 44100 Hz.

    Notes:
        The function will create any necessary directories if they do not exist.
        The function will overwrite the file if it already exists without prompting or informing the user.

    Returns:
        None:

    """
    try:
        if not isinstance(pathFilename, BinaryIO):
            Path(pathFilename).parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    soundfile.write(file=pathFilename, data=waveform.T, samplerate=sampleRate, subtype='FLOAT', format='WAV')

def loadWaveforms(listPathFilenames: List[PathLike | BinaryIO], sampleRate: int = 44100) -> NDArray[numpy.float32]:
    """
    Load multiple audio waveforms from a list of file paths into a single NumPy array.

    Parameters:
        listPathFilenames (List[str | Path]): List of file paths to the audio files.
        sampleRate (int, optional): The sample rate to use when reading the audio files. Defaults to 44100.

    Returns:
        arrayWaveforms (NDArray[numpy.float32]): The audio data in an array shaped (..., samples, COUNTwaveforms), where
            - (samples, COUNTwaveforms) if there is only one channel
            - or (channels, samples, COUNTwaveforms) if there is more than one channel
            - samples: Number of audio samples per channel.
            - COUNTwaveforms: Number of waveforms loaded (equal to the length of listPathFilenames).
    """
    COUNTwaveforms = len(listPathFilenames)
    arrayWaveforms = numpy.tile(readAudioFile(listPathFilenames[0], sampleRate=sampleRate)[..., numpy.newaxis], COUNTwaveforms)

    with ProcessPoolExecutor() as concurrencyManager:
        dictionaryConcurrency = {concurrencyManager.submit(readAudioFile, listPathFilenames[index]): index for index in range(1, COUNTwaveforms)}
        for claimTicket in as_completed(dictionaryConcurrency):
            arrayWaveforms[..., dictionaryConcurrency[claimTicket]] = claimTicket.result()
    return arrayWaveforms
