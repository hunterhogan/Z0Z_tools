"""Audio waveform amplitude normalization utilities.

(AI generated docstring)

This module provides functions for normalizing waveforms to specified peak amplitudes.
It handles both individual waveforms and arrays of multiple waveforms, with support
for reverting normalization operations on derived waveforms.

"""
from numpy import finfo as numpy_finfo, max as numpy_max
from typing import cast
from Z0Z_tools import ArrayWaveforms, NormalizationReverter, Waveform
import warnings

def normalizeWaveform(waveform: Waveform, amplitudeNorm: float = 1.0) -> tuple[Waveform, NormalizationReverter]:
	"""Normalize a waveform to have a specified peak amplitude.

	(AI generated docstring)

	This function scales a waveform so that its peak absolute value equals the specified
	amplitude normalization value. It also returns a function that can revert the
	normalization on derived waveforms.

	Parameters
	----------
	waveform : Waveform
		The input waveform to normalize.
	amplitudeNorm : float = 1.0
		The target peak amplitude.

	Returns
	-------
	waveformNormalized : Waveform
		The normalized waveform with peak amplitude of `amplitudeNorm`.
	revertNormalization : NormalizationReverter
		A function that can be used to revert normalization on derived waveforms.

	Warnings
	--------
	If `amplitudeNorm` is 0, it will be changed to a very small positive value.
	If the input `waveform` contains only zeros, the function will return
	the original waveform and provide a normalization reverter that
	divides by `amplitudeNorm`.

	Notes
	-----
	The normalization is based on the absolute maximum value in the waveform.
	The `NormalizationReverter` is a callable that can be applied to waveforms
	derived from the normalized waveform to restore their original scale.

	"""
	if amplitudeNorm == 0:
		numpyPrecision = waveform.dtype
		verySmallNonZeroPositiveValue = float(numpy_finfo(numpyPrecision).tiny.astype(numpyPrecision))
		warnings.warn(f"I received `{amplitudeNorm = }`, which would cause a divide by zero error, therefore, I am changing it to `{verySmallNonZeroPositiveValue = }`.", stacklevel=6)
		amplitudeNorm = verySmallNonZeroPositiveValue

	peakAbsolute = abs(float(numpy_max([waveform.max(), -waveform.min()])))
	if peakAbsolute == 0:
		amplitudeAdjustment = amplitudeNorm
		warnings.warn(f"I received `waveform` and all its values are zeros (i.e., the waveform is silent). You may want to confirm that the following effects are what you want. 1) The return value, `waveformNormalized`, will be the same as the input `waveform`: all zeros. 2) The return value, `revertNormalization`, \
				will normalize `waveformDescendant` by dividing it by `{amplitudeAdjustment = }`.", stacklevel=6)
	else:
		amplitudeAdjustment = amplitudeNorm / peakAbsolute

	waveformNormalized = cast(Waveform, waveform * amplitudeAdjustment)
	def revertNormalization(waveformDescendant: Waveform) -> Waveform:
		return cast(Waveform, waveformDescendant / amplitudeAdjustment)
	return waveformNormalized, revertNormalization

def normalizeArrayWaveforms(arrayWaveforms: ArrayWaveforms, amplitudeNorm: float = 1.0) -> tuple[ArrayWaveforms, list[NormalizationReverter]]:
	"""Normalize multiple waveforms in an array to a specified amplitude.

	(AI generated docstring)

	This function normalizes each waveform in the input array to have a peak amplitude of `amplitudeNorm`.
	It processes each waveform independently and returns both the normalized array and a list of functions
	that can revert the normalization.

	Parameters
	----------
	arrayWaveforms : ArrayWaveforms
		Array containing multiple waveforms to be normalized.
		The last axis represents different waveforms.
	amplitudeNorm : float = 1.0
		Target peak amplitude for normalization.

	Returns
	-------
	arrayWaveformsNormalized : ArrayWaveforms
		The normalized array of waveforms.
	listRevertNormalization : list[NormalizationReverter]
		A list of functions, each capable of reverting the normalization for the corresponding waveform.

	"""
	listRevertNormalization: list[NormalizationReverter] = [lambda makeTypeCheckerHappy: makeTypeCheckerHappy] * arrayWaveforms.shape[-1]
	for index in range(arrayWaveforms.shape[-1]):
		arrayWaveforms[..., index], listRevertNormalization[index] = normalizeWaveform(cast(Waveform, arrayWaveforms[..., index]), amplitudeNorm)
	return arrayWaveforms, listRevertNormalization
