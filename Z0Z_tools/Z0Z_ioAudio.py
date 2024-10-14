from collections import defaultdict
from numpy.typing import NDArray
from pathlib import Path
from typing import List, Optional, Dict, Tuple
import librosa
import numpy
import soundfile

def readAudioFile(pathFilename: str, sampleRate: int = 44100) -> NDArray:
    """
    Reads an audio file and returns its data as a NumPy array.

    Parameters:
        pathFilename (str): The path to the audio file.
        sampleRate (int, optional): The sample rate to use when reading the file. Defaults to 44100.

    Returns:
        NDArray: A NumPy array containing the audio data.
    """
    return librosa.load(path=pathFilename, sr=sampleRate, mono=False)[0]

def writeWav(pathFilename: str, waveform: NDArray, sampleRate: int = 44100) -> None:
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
        None

    """
    try:
        Path(pathFilename).parent.mkdir(parents=True, exist_ok=True)
    except Exception as ERRORmessage:
        pass
    soundfile.write(file=pathFilename, data=waveform.T, samplerate=sampleRate, subtype='FLOAT', format='WAV')

def loadSpectrograms(listPathFilenames: List[str] | str, sampleRateTarget: int = 44100, forceMonoChannel: bool = False, binsFFT: int = 2048, hopLength: int = 1024, frequencyAttenuate: Optional[int] = None, aligned: bool = False) -> Tuple[NDArray, List[Dict[str, int]]]:
    """
    Load spectrograms from audio files.

    Args:
        listPathFilenames (Union[List[str], str]): A list of file paths or a single file path.
        sampleRateTarget (int, optional): The target sample rate. Defaults to 44100.
        forceMonoChannel (bool, optional): Removed. Always False.
        binsFFT (int, optional): The number of FFT bins. Defaults to 2048.
        hopLength (int, optional): The hop length for the STFT. Defaults to 1024.
        frequencyAttenuate (Optional[int], optional): The frequency to attenuate. Defaults to None.
        aligned (bool, optional): Whether to align the waveforms. Defaults to False.
    Returns:
        Tuple (NDArray, List[Dict[str, int]]): A tuple containing the array of spectrograms and a list of metadata dictionaries for each spectrogram.
    """
    # Function implementation
    # whereToPadWaveformHARDCODED = 'trailing'
    # whereToPadWaveform = whereToPadWaveformHARDCODED
    # to unpack a request for a single spectrogram, maybe:
    # spectrogram.squeeze(), dictionarySamples[0] = loadSpectrograms(pathFilename)
    # spectrogram, dictionarySample = loadSpectrograms(pathFilename)
    # spectrogram = spectrogram.squeeze()

    if isinstance(listPathFilenames, str):
        listPathFilenames = [listPathFilenames]

    dictionaryMetadata: Dict[str, Dict[str, int]] = defaultdict(dict)
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

    if aligned:
        from Z0Z_tools.Z0Z_AudioHelpers import alignWaveforms
        dictionaryMetadata = alignWaveforms(dictionaryMetadata)

    samplesTotal = max(entry['samplesTotal'] for entry in dictionaryMetadata.values())
    # Padding logic
    # for entry in dictionaryMetadata.values():
    #     if whereToPadWaveform == 'trailing':
    #         entry['samplesTrailing'] = samplesTotal - entry['COUNTsamples']
    #     elif whereToPadWaveform == 'leading':
    #         entry['samplesLeading'] = samplesTotal - entry['COUNTsamples']
    #     elif whereToPadWaveform == 'both':
    #         remainingPadding = samplesTotal - entry['COUNTsamples']
    #         entry['samplesLeading'] = remainingPadding // 2
    #         entry['samplesTrailing'] = remainingPadding - entry['samplesLeading']
    #     entry['samplesTotal'] = entry['COUNTsamples'] + entry['samplesLeading'] + entry['samplesTrailing']

    COUNTchannels = max(entry['COUNTchannels'] for entry in dictionaryMetadata.values())
    arraySpectrograms = numpy.zeros(shape=(COUNTchannels, int(numpy.ceil(binsFFT / 2)) + 1, int(numpy.ceil(samplesTotal / hopLength)), len(dictionaryMetadata)), dtype=numpy.complex64)

    for index, (pathFilename, entry) in enumerate(dictionaryMetadata.items()):
        waveform = readAudioFile(pathFilename, sampleRateTarget)

        # paddedWaveform = numpy.pad(waveform, ((0, 0), (entry['samplesLeading'], entry['samplesTrailing'])), mode='constant')

        librosa.stft(y=waveform, n_fft=binsFFT, hop_length=hopLength, out=arraySpectrograms[..., index])

    if frequencyAttenuate is not None:
        from Z0Z_tools.Z0Z_AudioHelpers import cutHighFrequencies
        cutHighFrequencies(arraySpectrograms, frequencyAttenuate, sampleRateTarget, binsFFT)
    # the dictionary of samples is not tenable; how do other people handle this?
    return arraySpectrograms, [{'COUNTsamples': entry['COUNTsamples'], 'samplesLeading': entry['samplesLeading'], 'samplesTrailing': entry['samplesTrailing']} for entry in dictionaryMetadata.values()]

def spectrogramTOpathFilenameAudio(spectrogram: NDArray, pathFilename: str, binsFFT: int = 2048, hopLength: int = 1024, COUNTsamples: int = None, sampleRate: int = 44100) -> None:
    """
    Writes a complex spectrogram to a WAV file.

    Args:
        spectrogram (NDArray): The complex spectrogram to be written to the file. (Not mel-scaled.)
        pathFilename (str): Location for the file of the waveform output.
        binsFFT (int): How many FFT bins to convert the spectrogram. You want this to match the stft value. Defaults to 2048.
        hopLength (int): How many samples are in each time bin of the spectrogram. You want this to match the stft value. Defaults to 1024.
        COUNTsamples (int): The length of the output waveform in samples: if necessary, it will be zero-padded or truncated to this length. If `None`, then "a partial frame at the end of" the waveform will be truncated. See the documentation in the examples of librosa.istft(). Defaults to None. (Supply this value to avoid data loss.)
        sampleRate (int): The sample rate of the output waveform file. Defaults to 44100.

    Returns:
        None

    Note:
        If the windowing parameters for the istft do not match the stft, the waveform values will be distorted.
        Bitdepth is always 32-bit floating-point.
    """
    Path(pathFilename).parent.mkdir(parents=True, exist_ok=True)
    waveform = librosa.istft(stft_matrix=spectrogram, hop_length=hopLength, n_fft=binsFFT, length=COUNTsamples)
    writeWav(pathFilename, waveform, sampleRate)
