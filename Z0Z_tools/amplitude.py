from Z0Z_tools import ArrayWaveforms, NormalizationReverter, Waveform
from numpy import max as numpy_max

# TODO think about divide by zero

def normalizeWaveform(waveform: Waveform, amplitudeNorm: float = 1.0) -> tuple[Waveform, NormalizationReverter]:
	peakAbsolute = abs(float(numpy_max([waveform.max(), -waveform.min()])))
	amplitudeAdjustment = amplitudeNorm / peakAbsolute
	waveformNormalized = waveform * amplitudeAdjustment
	revertNormalization: NormalizationReverter = lambda waveformDescendant: waveformDescendant / amplitudeAdjustment
	return waveformNormalized, revertNormalization

def normalizeArrayWaveforms(arrayWaveforms: ArrayWaveforms, amplitudeNorm: float = 1.0) -> tuple[ArrayWaveforms, list[NormalizationReverter]]:
	listRevertNormalization: list[NormalizationReverter] = [lambda Pylance: Pylance] * arrayWaveforms.shape[-1]
	for index in range(arrayWaveforms.shape[-1]):
		arrayWaveforms[..., index], listRevertNormalization[index] = normalizeWaveform(arrayWaveforms[..., index], amplitudeNorm)
	return arrayWaveforms, listRevertNormalization
