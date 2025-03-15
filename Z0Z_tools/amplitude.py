from Z0Z_tools import ArrayWaveforms, NormalizationReverter, Waveform
from numpy import finfo as numpy_finfo, max as numpy_max

def normalizeWaveform(waveform: Waveform, amplitudeNorm: float = 1.0) -> tuple[Waveform, NormalizationReverter]:
	if amplitudeNorm == 0:
		numpyPrecision = waveform.dtype
		verySmallNonZeroPositiveValue = float(numpy_finfo(numpyPrecision).tiny.astype(numpyPrecision))
		import warnings
		warnings.warn(f"I received {amplitudeNorm=}, which would cause a divide by zero error, therefore, I am changing it to {verySmallNonZeroPositiveValue=}.")
		amplitudeNorm = verySmallNonZeroPositiveValue

	peakAbsolute = abs(float(numpy_max([waveform.max(), -waveform.min()])))
	if peakAbsolute == 0:
		amplitudeAdjustment = amplitudeNorm
		import warnings
		warnings.warn(f"I received `waveform` and all its values are zeros (i.e., it is silent). You may want to confirm that the following effects are what you want. 1) The return value, `waveformNormalized`, will be the same as the input `waveform`: all zeros. 2) The return value, `revertNormalization`, will normalize `waveformDescendant` by dividing it by {amplitudeAdjustment=}.")
	else:
		amplitudeAdjustment = amplitudeNorm / peakAbsolute

	waveformNormalized = waveform * amplitudeAdjustment
	revertNormalization: NormalizationReverter = lambda waveformDescendant: waveformDescendant / amplitudeAdjustment
	return waveformNormalized, revertNormalization

def normalizeArrayWaveforms(arrayWaveforms: ArrayWaveforms, amplitudeNorm: float = 1.0) -> tuple[ArrayWaveforms, list[NormalizationReverter]]:
	listRevertNormalization: list[NormalizationReverter] = [lambda makeTypeCheckerHappy: makeTypeCheckerHappy] * arrayWaveforms.shape[-1]
	for index in range(arrayWaveforms.shape[-1]):
		arrayWaveforms[..., index], listRevertNormalization[index] = normalizeWaveform(arrayWaveforms[..., index], amplitudeNorm)
	return arrayWaveforms, listRevertNormalization
