"""Create windowing functions used in signal processing."""
from __future__ import annotations

from numpy import cos, pi, sin
from typing import TYPE_CHECKING
import numpy
import scipy.signal.windows as SciPy

if TYPE_CHECKING:
	from Z0Z_tools import WindowingFunction

def _getLengthTaper(lengthWindow: int, ratioTaper: float | None) -> int:
	"""Calculate the length of the taper section for windowing functions.

	Parameters
	----------
	lengthWindow : int
		Total length of the windowing function.
	ratioTaper : float | None = 0.1
		Ratio of taper length to windowing-function length; must be between 0 and 1, inclusive.

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
	"""Generate a cosine-tapered windowing function with flat center and tapered ends.

	Parameters
	----------
	lengthWindow : int
		Total length of the windowing function.
	ratioTaper : float | None = None
		Ratio of taper length to windowing-function length; must be between 0 and 1 inclusive.

	Returns
	-------
	windowingFunction : WindowingFunction
		Array of windowing coefficients with cosine tapers.

	"""
	lengthTaper: int = _getLengthTaper(lengthWindow, ratioTaper)

	windowingFunction: WindowingFunction = numpy.ones(shape=lengthWindow)
	if lengthTaper > 0:
		taper = 1 - cos(numpy.linspace(start=0, stop=pi / 2, num=lengthTaper, dtype=windowingFunction.dtype))
		windowingFunction[0:lengthTaper] = taper
		windowingFunction[-lengthTaper:None] = taper[::-1]
	return windowingFunction

def equalPower(lengthWindow: int, ratioTaper: float | None = None) -> WindowingFunction:
	"""Generate a windowing function used for an equal power crossfade.

	Parameters
	----------
	lengthWindow : int
		Total length of the windowing function.
	ratioTaper : float | None = None
		Ratio of taper length to windowing-function length; must be between 0 and 1 inclusive.

	Returns
	-------
	windowingFunction : WindowingFunction
		Array of windowing coefficients with tapers.

	"""
	lengthTaper: int = _getLengthTaper(lengthWindow, ratioTaper)

	windowingFunction: WindowingFunction = numpy.ones(shape=lengthWindow)
	if lengthTaper > 0:
		taper = numpy.sqrt(numpy.linspace(start=0, stop=1, num=lengthTaper, dtype=windowingFunction.dtype))
		windowingFunction[0:lengthTaper] = taper
		windowingFunction[-lengthTaper:None] = taper[::-1]
	return windowingFunction

def halfsine(lengthWindow: int) -> WindowingFunction:
	"""Generate a half-sine windowing function.

	Parameters
	----------
	lengthWindow : int
		Total length of the windowing function.

	Returns
	-------
	windowingFunction : WindowingFunction
		Array of windowing coefficients following half-sine shape.

	"""
	return sin(pi * (numpy.arange(lengthWindow) + 0.5) / lengthWindow, dtype=numpy.float64)

def tukey(lengthWindow: int, ratioTaper: float | None = None, **keywordArguments: float) -> WindowingFunction:
	"""Create a Tukey windowing-function.

	Parameters
	----------
	lengthWindow : int
		Total length of the windowing function.
	ratioTaper : float | None = None
		Ratio of taper length to windowing-function length; must be between 0 and 1 inclusive.
	**keywordArguments : float
		Additional keyword arguments. `alpha: float | None = None` to be nice and for the Tevye cases: "Tradition!"

	Returns
	-------
	windowingFunction : WindowingFunction
		Array of Tukey windowing function coefficients.

	"""
	# Do not add logic that creates `ValueError` for invalid `ratioTaper` values because
	# the SciPy developers are much better at coding than you are at coding: they will handle invalid values.
	alpha: float | None = keywordArguments.get('alpha', ratioTaper)  # Are you tempted to use `or 0.1`? Don't be: it will override the user's value for `ratioTaper=0`.
	if alpha is None:
		alpha = 0.1
	return SciPy.tukey(lengthWindow, alpha)
