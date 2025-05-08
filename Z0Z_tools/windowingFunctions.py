"""
Generate various windowing functions used in signal processing.
"""

from numpy import cos, pi, sin
from Z0Z_tools import def_asTensor, WindowingFunction
import numpy
import scipy.signal.windows as SciPy

def _getLengthTaper(lengthWindow: int, ratioTaper: float | None) -> int:
	"""
	Calculate the length of the taper section for windowing functions.

	Parameters:
		lengthWindow: Total length of the windowing function.
		ratioTaper (0.1): Ratio of taper length to windowing-function length; must be between 0 and 1, inclusive.

	Returns:
		lengthTaper: Number of samples in one taper section.
	"""
	if ratioTaper is None:
		lengthTaper = int(lengthWindow * 0.1 / 2)
	elif 0 <= ratioTaper <= 1:
		lengthTaper = int(lengthWindow * ratioTaper / 2)
	else:
		raise ValueError(f"I received `{ratioTaper = }`. If set, `ratioTaper` must be between 0 and 1, inclusive.")
	return lengthTaper

@def_asTensor
def cosineWings(lengthWindow: int, ratioTaper: float | None = None) -> WindowingFunction:
	"""
	Generate a cosine-tapered windowing function with flat center and tapered ends.

	Parameters:
		lengthWindow: Total length of the windowing function.
		ratioTaper (0.1): Ratio of taper length to windowing-function length; must be between 0 and 1 inclusive.

	Returns:
		windowingFunction: Array of windowing coefficients with cosine tapers.
	"""
	lengthTaper = _getLengthTaper(lengthWindow, ratioTaper)

	windowingFunction = numpy.ones(shape=lengthWindow)
	if lengthTaper > 0:
		taper = 1 - cos(numpy.linspace(start=0, stop=pi / 2, num=lengthTaper))
		windowingFunction[0:lengthTaper] = taper
		windowingFunction[-lengthTaper:None] = taper[::-1]
	return windowingFunction

@def_asTensor
def equalPower(lengthWindow: int, ratioTaper: float | None = None) -> WindowingFunction:
	"""
	Generate a windowing function used for an equal power crossfade.

	Parameters:
		lengthWindow: Total length of the windowing function.
		ratioTaper (0.1): Ratio of taper length to windowing-function length; must be between 0 and 1 inclusive.

	Returns:
		windowingFunction: Array of windowing coefficients with tapers.
	"""
	lengthTaper = _getLengthTaper(lengthWindow, ratioTaper)

	windowingFunction = numpy.ones(shape=lengthWindow)
	if lengthTaper > 0:
		taper = numpy.absolute(numpy.sqrt(numpy.linspace(start=0, stop=1, num=lengthTaper)))
		windowingFunction[0:lengthTaper] = taper
		windowingFunction[-lengthTaper:None] = taper[::-1]
	return windowingFunction

@def_asTensor
def halfsine(lengthWindow: int) -> WindowingFunction:
	"""
	Generate a half-sine windowing function.

	Parameters:
		lengthWindow: Total length of the windowing function.

	Returns:
		windowingFunction: Array of windowing coefficients following half-sine shape.
	"""
	return sin(pi * (numpy.arange(lengthWindow) + 0.5) / lengthWindow)

@def_asTensor
def tukey(lengthWindow: int, ratioTaper: float | None = None, **keywordArguments: float) -> WindowingFunction:
	"""
	Create a Tukey windowing-function.

	Parameters:
		lengthWindow: Total length of the windowing function.
		ratioTaper (0.1): Ratio of taper length to windowing-function length; must be between 0 and 1 inclusive.
		**keywordArguments: `alpha: float | None = None` to be nice and for the Tevye cases: "Tradition!"

	Returns:
		windowingFunction: Array of Tukey windowing function coefficients.
	"""
	# Do not add logic that creates `ValueError` for invalid `ratioTaper` values because
	# the SciPy developers are much better at coding than you are at coding: they will handle invalid values.
	alpha = keywordArguments.get('alpha', ratioTaper) # Are you tempted to use `or 0.1`? Don't be: it will override the user's value for `ratioTaper=0`.
	if alpha is None:
		alpha = 0.1
	return SciPy.tukey(lengthWindow, alpha)
