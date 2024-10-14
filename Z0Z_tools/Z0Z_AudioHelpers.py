from numpy.typing import NDArray
import librosa
import numpy

def alignWaveforms(dictionaryMetadata):
    """
    do not truncate data
    track the new length of each waveform
    """
    return dictionaryMetadata

def cutHighFrequencies(spectrogramInplace: NDArray, frequencyAttenuate: int, sampleRate: int, binsFFT: int, iWillSMASHyourArray = True) -> None:
    """In-place clipping of multiple spectrograms with shape (..., frequency bins, time frames, spectrograms)
    iWillSMASHyourArray is a warning that I am using refcheck=False.
    """

    # find the index number of the first bin that will be multiplied by a rolloff coefficient
    indexBinRolloff = numpy.searchsorted(librosa.fft_frequencies(n_fft=binsFFT, sr=sampleRate), frequencyAttenuate, side='right')
    if iWillSMASHyourArray:
        # eliminate all bins above the rolloff bins
        spectrogramInplace.resize((*spectrogramInplace.shape[:-3],
                                 indexBinRolloff + (SIZEbinsRolloff := int(0.05 * (binsFFT / 2))),
                                 *spectrogramInplace.shape[:-2]), refcheck=False)
    else:
        # spectrogramInplace = numpy.resize(spectrogramInplace, shapeSpectrogram)
        raise NotImplementedError("You can't reduce memory usage if you are copying arrays.")

    # Make an ndarray jig to rolloff the volume
    # Start with a symmetrical hanning window and keep the declining coefficients, hence bins*2 and only keep the right side
    jigRolloffCoefficients = (numpy.hanning(SIZEbinsRolloff * 2)[-SIZEbinsRolloff:]
                                ).reshape(*( # Reshape the jig so the coefficients target the cells on the frequency axis
                                        [1 for axis in range(spectrogramInplace.ndim - 3)] # Channels, if present
                                        + [SIZEbinsRolloff]
                                        + [1] # frames
                                        + [1])) # Spectrograms

    spectrogramInplace[..., indexBinRolloff:, : ,:] *= jigRolloffCoefficients

