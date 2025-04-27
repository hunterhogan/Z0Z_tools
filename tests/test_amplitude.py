from Z0Z_tools import normalizeWaveform, normalizeArrayWaveforms
from Z0Z_tools import Waveform, ArrayWaveforms
from tests.conftest import sampleData, rtolDEFAULT, amplitudeNorm
import numpy
import pytest

@pytest.mark.parametrize("ID, waveform, sampleRate, LUFS, channelsTotal", [(dataSample.ID, dataSample.waveform, dataSample.sampleRate, dataSample.LUFS, dataSample.channelsTotal) for dataSample in sampleData()])
def test_normalize_peak_amplitude(ID: str, waveform: Waveform, sampleRate: float, LUFS: float, channelsTotal: int) -> None:
    """Test that normalize() scales waveform to have peak amplitude equal to amplitudeNorm."""
    waveformNormalized, _DISCARDrevertFunction = normalizeWaveform(waveform)

    peakAbsolute = numpy.max(numpy.abs(waveformNormalized))
    assert numpy.isclose(peakAbsolute, amplitudeNorm, rtol=1e-5), f"Peak amplitude {peakAbsolute} should equal {amplitudeNorm} for {ID}"

@pytest.mark.parametrize("ID, waveform, sampleRate, LUFS, channelsTotal", [(dataSample.ID, dataSample.waveform, dataSample.sampleRate, dataSample.LUFS, dataSample.channelsTotal) for dataSample in sampleData()])
def test_normalize_reversion(ID: str, waveform: Waveform, sampleRate: float, LUFS: float, channelsTotal: int):
    """Test that normalize() returns a reversion function that restores the original waveform."""
    waveformNormalized, revertNormalization = normalizeWaveform(waveform.copy())

    waveformReverted = revertNormalization(waveformNormalized)

    assert numpy.allclose(waveformReverted, waveform, rtol=1e-5), f"Reverted waveform should match original for {ID}"

@pytest.mark.parametrize("ID, waveform, sampleRate, LUFS, channelsTotal", [(dataSample.ID, dataSample.waveform, dataSample.sampleRate, dataSample.LUFS, dataSample.channelsTotal) for dataSample in sampleData()])
def test_normalize_preserves_relative_amplitudes(ID: str, waveform: Waveform, sampleRate: float, LUFS: float, channelsTotal: int):
    """Test that normalize() preserves relative amplitudes between samples."""
    # Create reference points to compare
    indexReference1, indexReference2 = 1000, 2000
    if indexReference2 >= waveform.shape[1]:
        indexReference1, indexReference2 = 10, 20

    if waveform.shape[0] >= 2:
        # For stereo or multichannel
        ratioOriginal = waveform[0, indexReference1] / (waveform[1, indexReference2] + 1e-10)

        waveformNormalized, _DISCARDrevertFunction = normalizeWaveform(waveform.copy())
        ratioNormalized = waveformNormalized[0, indexReference1] / (waveformNormalized[1, indexReference2] + 1e-10)

        assert numpy.isclose(ratioOriginal, ratioNormalized, rtol=1e-5), f"Relative amplitudes should be preserved for {ID}"

def test_normalize_edge_cases():
    """Test normalize() with edge cases."""
    # Test with zero waveform
    shapeWaveform = (2, 1000)  # Sample stereo shape
    waveformZeros = numpy.zeros(shapeWaveform, dtype=numpy.float32)

    # Since division by zero would occur, this should ideally handle it gracefully
    # or raise a specific error. Let's check both possibilities.
    try:
        waveformNormalized, _revertNormalization = normalizeWaveform(waveformZeros)
        # If it doesn't raise an error, the result should be zeros
        assert numpy.allclose(waveformNormalized, waveformZeros), \
            f"Zero waveform should normalize to zeros"
    except Exception as ERRORmessage:
        # If it raises an error, it should be a specific error about division by zero
        assert "division" in str(ERRORmessage).lower() or "zero" in str(ERRORmessage).lower(), \
            f"Expected division by zero error, got: {ERRORmessage}"

def test_normalizeArrayWaveforms(array44100_ch2_sec5_Sine: ArrayWaveforms):
    """Test that normalizeArrayWaveforms scales multiple waveforms to have peak amplitude equal to amplitudeNorm."""
    # Save a copy of the original array for comparison after reversion
    arrayOriginal = array44100_ch2_sec5_Sine.copy()

    # Apply normalization to all waveforms in the array
    arrayNormalized, listRevertNormalization = normalizeArrayWaveforms(array44100_ch2_sec5_Sine.copy())

    # Test 1: Check that each waveform is normalized to the correct peak amplitude
    for indexWaveform in range(arrayNormalized.shape[-1]):
        waveformCurrent = arrayNormalized[..., indexWaveform]
        peakAbsolute = numpy.max(numpy.abs(waveformCurrent))
        assert numpy.isclose(peakAbsolute, amplitudeNorm, rtol=rtolDEFAULT), \
            f"Peak amplitude {peakAbsolute} should equal {amplitudeNorm} for waveform at index {indexWaveform}"

    # Test 2: Check that reversion functions restore original waveforms
    arrayReverted = arrayNormalized.copy()
    for indexWaveform in range(arrayReverted.shape[-1]):
        arrayReverted[..., indexWaveform] = listRevertNormalization[indexWaveform](arrayReverted[..., indexWaveform])

    assert numpy.allclose(arrayReverted, arrayOriginal, rtol=rtolDEFAULT), \
        "Reverted array should match the original array"
