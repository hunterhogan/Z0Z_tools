from Z0Z_tools import def_asTensor
from numpy.typing import NDArray
import numpy
import numpy.typing
import scipy.signal.windows as SciPy

@def_asTensor
def cosineWings(lengthWindow: int, ratioTaper: float | None = None) -> NDArray[numpy.float64]:
    """
    Generates a cosine-tapered window.

    Parameters:
        lengthWindow: The length of the window.
        ratioTaper (0.1): The ratio of the total tapering to the total window length. Defaults to 0.1.

    Returns:
        window: The generated cosine-tapered window.
    """
    from numpy import cos, pi

    if ratioTaper is None:
        lengthTaper = int(lengthWindow * 0.1 / 2)
    elif 0 <= ratioTaper <= 1:
        lengthTaper = int(lengthWindow * ratioTaper / 2)
    else:
        raise ValueError(f"Parameter `ratioTaper` is {ratioTaper}. If set, `ratioTaper` must be between 0 and 1.")

    window = numpy.ones(shape=lengthWindow)
    # Apply cosine taper to the beginning and end
    if lengthTaper > 0:
        window[0:lengthTaper] = 1 - cos(numpy.linspace(start=0, stop=pi / 2, num=lengthTaper))
        window[-lengthTaper:None] = 1 + cos(numpy.linspace(start=pi / 2, stop=pi, num=lengthTaper))
    return window

@def_asTensor
def equalPower(lengthWindow: int, ratioTaper: float | None = None) -> NDArray[numpy.float64]:
    if ratioTaper is None:
        lengthTaper = int(lengthWindow * 0.1 / 2)
    elif 0 <= ratioTaper <= 1:
        lengthTaper = int(lengthWindow * ratioTaper / 2)
    else:
        raise ValueError(f"Parameter `ratioTaper` is {ratioTaper}. If set, `ratioTaper` must be between 0 and 1.")

    window = numpy.ones(shape=lengthWindow)
    if lengthTaper > 0:
        window[0:lengthTaper] = numpy.sqrt(numpy.linspace(start=0, stop=1, num=lengthTaper))
        window[-lengthTaper:None] = numpy.sqrt(numpy.linspace(start=1, stop=0, num=lengthTaper))
    return numpy.absolute(window)

@def_asTensor
def halfsine(lengthWindow: int) -> NDArray:
    from numpy import sin, pi
    return sin(pi * (numpy.arange(lengthWindow) + 0.5) / lengthWindow)

@def_asTensor
def tukey(lengthWindow: int, ratioTaper: float | None = None, **keywordArguments) -> NDArray[numpy.float64]:
    """
    Create a Tukey windowing-function.

    Parameters:
        lengthWindow: The total length of the window.
        ratioTaper (0.1): The ratio of the total tapering to the total window length. Defaults to 0.1.
        **keywordArguments: Additional keyword arguments. Can include 'alpha' for backward compatibility.

    Returns:
        windowingFunction: The generated Tukey windowing-function.
    """
    # Do not add logic that creates ValueError for invalid ratioTaper values because
    # the scipy developers are much better at coding than you are at coding,
    # and they will handle the errors.
    alpha = keywordArguments.get('alpha', ratioTaper)
    if alpha is None:
        alpha = 0.1
    return SciPy.tukey(lengthWindow, alpha)
