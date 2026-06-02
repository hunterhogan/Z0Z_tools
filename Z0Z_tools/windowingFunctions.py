"""Generate windowing functions for signal processing.

Contents
--------
Functions
	cosineWings
		Generate a cosine-tapered windowing function with a flat center and tapered ends.
	equalPower
		Generate an equal-power taper for crossfades.
	halfsine
		Generate a half-sine windowing function.
	tukey
		Generate a Tukey windowing function with optional taper control.
"""
from __future__ import annotations

from numpy import cos, pi, sin
from typing import TYPE_CHECKING
import numpy
import scipy.signal.windows as SciPy

if TYPE_CHECKING:
	from Z0Z_tools import WindowingFunction

def _getLengthTaper(lengthWindow: int, ratioTaper: float | None) -> int:
	"""I use this shared subroutine to split a window length into taper sections.

	This function converts a whole window length and a taper ratio into the number of samples in one
	edge taper. Public window constructors call it so they can share the same taper-length logic.

	Parameters
	----------
	lengthWindow : int
		Total length of the windowing function.
	ratioTaper : float | None
		Ratio of taper length to windowing-function length. When `None`, the default taper ratio is
		used.

	Returns
	-------
	lengthTaper : int
		Number of samples in one taper section.
	"""  # noqa: DOC501
	if ratioTaper is None:
		lengthTaper = int(lengthWindow * 0.1 / 2)
	elif 0 <= ratioTaper <= 1:
		lengthTaper = int(lengthWindow * ratioTaper / 2)
	else:
		message: str = f"I received `{ratioTaper = }`. If set, `ratioTaper` must be between 0 and 1, inclusive."
		raise ValueError(message)
	return lengthTaper

def cosineWings(lengthWindow: int, ratioTaper: float | None = None) -> WindowingFunction:
	"""Generate a cosine-tapered windowing function with a flat center and tapered ends.

	This function creates a NumPy array [1] of coefficients that rise smoothly from 0 to 1, stay
	flat in the middle, and mirror the taper at the end. It uses `numpy.linspace` [2] to sample the
	taper and `numpy.cos` [3] to shape it. It acts on `lengthWindow` and `ratioTaper` and returns
	the windowing coefficients.

	Parameters
	----------
	lengthWindow : int
		Total length of the windowing function.
	ratioTaper : float | None = None
		Ratio of taper length to windowing-function length. The value must be between 0 and 1,
		inclusive.

	Returns
	-------
	windowingFunction : WindowingFunction
		NumPy array of windowing coefficients with cosine tapers.

	See Also
	--------
	`Z0Z_tools.optionalPyTorch.cosineWingsTensor`
		Tensor version of this windowing function.

	References
	----------
	[1] NumPy `ndarray`.
		https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html
	[2] NumPy `linspace`.
		https://numpy.org/doc/stable/reference/generated/numpy.linspace.html
	[3] NumPy `cos`.
		https://numpy.org/doc/stable/reference/generated/numpy.cos.html

	"""
	lengthTaper: int = _getLengthTaper(lengthWindow, ratioTaper)

	windowingFunction: WindowingFunction = numpy.ones(shape=lengthWindow)
	if 0 < lengthTaper:
		taper = 1 - cos(numpy.linspace(start=0, stop=pi / 2, num=lengthTaper, dtype=windowingFunction.dtype))
		windowingFunction[0:lengthTaper] = taper
		windowingFunction[-lengthTaper:None] = taper[::-1]
	return windowingFunction

def equalPower(lengthWindow: int, ratioTaper: float | None = None) -> WindowingFunction:
	"""Generate an equal-power taper for crossfades.

	This function creates a NumPy array [1] of coefficients that follow a square-root taper at both
	ends and a flat center. It uses `numpy.linspace` [2] to sample the taper and `numpy.sqrt` [3] to
	convert it to equal-power scaling. It acts on `lengthWindow` and `ratioTaper` and returns the
	windowing coefficients.

	Parameters
	----------
	lengthWindow : int
		Total length of the windowing function.
	ratioTaper : float | None = None
		Ratio of taper length to windowing-function length. The value must be between 0 and 1,
		inclusive.

	Returns
	-------
	windowingFunction : WindowingFunction
		NumPy array of windowing coefficients with tapers.

	See Also
	--------
	`Z0Z_tools.optionalPyTorch.equalPowerTensor`
		Tensor version of this windowing function.

	References
	----------
	[1] NumPy `ndarray`.
		https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html
	[2] NumPy `linspace`.
		https://numpy.org/doc/stable/reference/generated/numpy.linspace.html
	[3] NumPy `sqrt`.
		https://numpy.org/doc/stable/reference/generated/numpy.sqrt.html

	"""
	lengthTaper: int = _getLengthTaper(lengthWindow, ratioTaper)

	windowingFunction: WindowingFunction = numpy.ones(shape=lengthWindow)
	if 0 < lengthTaper:
		taper = numpy.sqrt(numpy.linspace(start=0, stop=1, num=lengthTaper, dtype=windowingFunction.dtype))
		windowingFunction[0:lengthTaper] = taper
		windowingFunction[-lengthTaper:None] = taper[::-1]
	return windowingFunction

def halfsine(lengthWindow: int) -> WindowingFunction:
	"""Generate a half-sine windowing function.

	This function creates a NumPy array [1] of coefficients that follow a half-sine profile across
	the requested length. It uses `numpy.arange` [2] and `numpy.sin` [3] to place the samples. It
	acts on `lengthWindow` and returns the windowing coefficients.

	Parameters
	----------
	lengthWindow : int
		Total length of the windowing function.

	Returns
	-------
	windowingFunction : WindowingFunction
		NumPy array of windowing coefficients following a half-sine shape.

	See Also
	--------
	`Z0Z_tools.optionalPyTorch.halfsineTensor`
		Tensor version of this windowing function.

	References
	----------
	[1] NumPy `ndarray`.
		https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html
	[2] NumPy `arange`.
		https://numpy.org/doc/stable/reference/generated/numpy.arange.html
	[3] NumPy `sin`.
		https://numpy.org/doc/stable/reference/generated/numpy.sin.html

	"""
	return sin(pi * (numpy.arange(lengthWindow) + 0.5) / lengthWindow, dtype=numpy.float64)

def tukey(lengthWindow: int, ratioTaper: float | None = None, **keywordArguments: float) -> WindowingFunction:
	"""Generate a Tukey windowing function with optional SciPy keyword overrides.

	This function creates a NumPy array [1] by delegating to SciPy's Tukey window implementation
	[2]. It accepts `lengthWindow`, `ratioTaper`, and extra keyword arguments, then returns the
	windowing coefficients.

	Parameters
	----------
	lengthWindow : int
		Total length of the windowing function.
	ratioTaper : float | None = None
		Ratio of taper length to windowing-function length. The value must be between 0 and 1,
		inclusive.
	**keywordArguments : float
		Additional keyword arguments. `alpha` overrides `ratioTaper` when provided, matching SciPy's
		API.

	Returns
	-------
	windowingFunction : WindowingFunction
		NumPy array of Tukey windowing function coefficients.

	References
	----------
	[1] NumPy `ndarray`.
		https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html
	[2] SciPy Tukey window.
		https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.windows.tukey.html

	"""
	alpha: float | None = keywordArguments.get('alpha', ratioTaper)  # Are you tempted to use `or 0.1`? Don't be: it will override the user's value for `ratioTaper=0`.
	if alpha is None:
		alpha = 0.1
	return SciPy.tukey(lengthWindow, alpha)
