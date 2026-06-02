"""Clip and limit array values using magnitude-based hard limits.

(AI generated docstring)

You can use this module to apply hard clipping [1] to NumPy [2] arrays, constraining element
magnitudes within bounds defined by a comparand array. The module is not yet fully implemented
and may not correctly handle all cases.

Contents
--------
Functions
	applyHardLimit
		Clip the elements of a real-valued array to stay within the magnitude of a comparand.
	applyHardLimitComplexValued
		Clip the elements of a complex-valued array using magnitude-based scaling.

References
----------
[1] Clipping (signal processing) - Wikipedia
	https://en.wikipedia.org/wiki/Clipping_(signal_processing)

[2] NumPy
	https://numpy.org/doc/stable/
"""
from __future__ import annotations

from numpy import absolute, complexfloating, float64, floating, ones_like
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
	from numpy.typing import ArrayLike, NDArray

def applyHardLimit(arrayTarget: NDArray[Any], comparand: ArrayLike = 1.0) -> NDArray[Any]:
	"""Clip the elements of `arrayTarget` to the magnitude bounds defined by `comparand`.

	This function applies a hard amplitude limit element-wise to `arrayTarget`. Elements whose
	magnitude exceeds the corresponding magnitude of `comparand` are reduced toward zero until
	the element magnitude equals the comparand magnitude. The operation modifies `arrayTarget`
	in place and returns a reference to it.

	Parameters
	----------
	arrayTarget : NDArray[Any]
		The array to clip. Modified in place.
	comparand : ArrayLike = 1.0
		The magnitude threshold. Elements of `arrayTarget` whose magnitude strictly exceeds the
		corresponding magnitude in `comparand` are clipped to that comparand magnitude.

	Returns
	-------
	arrayClipped : NDArray[Any]
		A reference to the modified `arrayTarget`.

	See Also
	--------
	`applyHardLimitComplexValued`
		Clip complex-valued array elements using magnitude-based scaling.

	References
	----------
	[1] Clipping (signal processing) - Wikipedia
		https://en.wikipedia.org/wiki/Clipping_(signal_processing)

	[2] numpy.typing.NDArray
		https://numpy.org/doc/stable/reference/typing.html#numpy.typing.NDArray

	[3] numpy.typing.ArrayLike
		https://numpy.org/doc/stable/reference/typing.html#numpy.typing.ArrayLike

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
	"""Clip the elements of complex-valued `arrayTarget` by scaling magnitudes to stay within `comparand`.

	This function applies a magnitude-based hard limit to each element of `arrayTarget`. When the
	magnitude of an element strictly exceeds the corresponding value in `comparand`, the element is
	scaled down by a power of the ratio of comparand magnitude to target magnitude. Elements whose
	magnitudes are within the limit are left unchanged. This function returns a new array and does
	not modify `arrayTarget` in place.

	Parameters
	----------
	arrayTarget : NDArray[complexfloating[Any, Any]]
		The complex-valued array to clip.
	comparand : NDArray[floating[Any] | complexfloating[Any, Any]]
		The magnitude threshold array. Only the magnitudes of `comparand` values are used.
	penalty : float = 1.0
		Exponent applied to the scaling factor when limiting is needed. Values greater than 1.0
		produce more aggressive clipping; values between 0.0 and 1.0 produce less aggressive clipping.

	Returns
	-------
	arrayResult : NDArray[complexfloating[Any, Any]]
		A new array with the same shape and dtype as `arrayTarget`, with element magnitudes
		clipped according to `comparand`.

	See Also
	--------
	`applyHardLimit`
		Clip real-valued array elements to stay within the magnitude of a comparand.

	Mathematics
	-----------
	magnitude scaling : equation
	```
		Let  a ≜ `arrayTarget`,  c ≜ `comparand`,  p ≜ `penalty`,
		     s ≜ (|cᵢ| / |aᵢ|)

		For each element i where |aᵢ| > |cᵢ|:
			resultᵢ = aᵢ × sᵖ

		For each element i where |aᵢ| ≤ |cᵢ|:
			resultᵢ = aᵢ
	```

	References
	----------
	[1] Clipping (signal processing) - Wikipedia
		https://en.wikipedia.org/wiki/Clipping_(signal_processing)

	[2] numpy.typing.NDArray
		https://numpy.org/doc/stable/reference/typing.html#numpy.typing.NDArray

	"""
	magnitudeArrayTarget: NDArray[float64] = absolute(arrayTarget, dtype=float64)
	magnitudeComparand: NDArray[float64] = absolute(comparand, dtype=float64)

	maskTrueAboveThreshold = magnitudeComparand - magnitudeArrayTarget < 0.0

	arrayCoefficients_Float64: NDArray[float64] = magnitudeComparand[maskTrueAboveThreshold] / magnitudeArrayTarget[maskTrueAboveThreshold]
	arrayCoefficients_ComplexValued: NDArray[complexfloating[Any, Any]] = ones_like(arrayTarget, dtype=arrayTarget.dtype)
	arrayCoefficients_ComplexValued[maskTrueAboveThreshold] = arrayCoefficients_Float64**penalty

	return arrayTarget * arrayCoefficients_ComplexValued
