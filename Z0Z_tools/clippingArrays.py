"""NOTE not fully implemented"""
from typing import Any
from numpy import absolute, complexfloating, float64, floating
from numpy import ones_like
from numpy.typing import ArrayLike, NDArray

def applyHardLimit(arrayTarget: NDArray[Any], comparand: ArrayLike = 1.0) -> NDArray[Any]:
	"""
	Apply a hard limit to the elements of the target array based on the comparand value.

	Parameters
		arrayTarget: The target array to which the hard limit will be applied.
		comparand (1.0): The value or array to compare against. Defaults to 1.0.

	Returns
		arrayClipped: The modified target array with the hard limit applied.
	"""

	maskTrueAboveThreshold = absolute(comparand) - absolute(arrayTarget) < 0.0
	reduction = arrayTarget - (absolute(arrayTarget) - absolute(comparand))
	arrayTarget[maskTrueAboveThreshold] = reduction[maskTrueAboveThreshold]
	return arrayTarget

def applyHardLimitComplexValued(
	arrayTarget: NDArray[complexfloating[Any, Any]],
	comparand: NDArray[floating[Any] | complexfloating[Any, Any]],
	penalty: float = 1.0
	) -> NDArray[complexfloating[Any, Any]]:
	"""
	Applies a hard limit to a complex-valued array based on the magnitude of a comparand array.

	This function implements a magnitude-based limiting operation where the magnitude of the target array
	is constrained by the magnitude of the comparand array. When the magnitude of the target exceeds
	the comparand, the target is scaled down with an optional penalty factor.

	Parameters:
	----------
	arrayTarget : ndarray of complex values
		The input array to be limited.
	comparand : ndarray of real or complex values
		The array containing the magnitude threshold values.
	penalty : float, optional
		Exponent applied to the scaling factor when limiting is needed. Default is 1.0.
		Values greater than 1.0 result in more aggressive limiting.

	Returns:
	-------
	ndarray of complex values
		The limited array with the same shape and dtype as arrayTarget.

	Notes:
	-----
	The limiting operation is performed element-wise according to the formula:
		result = arrayTarget * (|comparand|/|arrayTarget|)^penalty
	where the scaling is only applied when |arrayTarget| > |comparand|.
	"""

	magnitudeArrayTarget: NDArray[float64] = absolute(arrayTarget, dtype=float64)
	magnitudeComparand: NDArray[float64] = absolute(comparand, dtype=float64)

	maskTrueAboveThreshold = magnitudeComparand - magnitudeArrayTarget < 0.0

	arrayCoefficients_Float64: NDArray[float64] = magnitudeComparand[maskTrueAboveThreshold] / magnitudeArrayTarget[maskTrueAboveThreshold]
	arrayCoefficients_ComplexValued: NDArray[complexfloating[Any, Any]] = ones_like(arrayTarget, dtype=arrayTarget.dtype)
	arrayCoefficients_ComplexValued[maskTrueAboveThreshold] = arrayCoefficients_Float64**penalty

	return arrayTarget * arrayCoefficients_ComplexValued
