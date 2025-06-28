"""Type definitions mirroring scipy.signal short-time FFT constants.

(AI generated docstring)

This module defines type aliases that mirror the allowed values for parameters
and properties in scipy's short-time FFT implementation. These types ensure
type safety when interfacing with scipy.signal.ShortTimeFFT methods.

"""

from typing import Literal

PAD_TYPE = Literal['zeros', 'edge', 'even', 'odd']
"""Allowed values for parameter `padding` of method `ShortTimeFFT.stft()`.

(AI generated docstring)

Type literal defining the valid padding modes accepted by scipy's
`ShortTimeFFT.stft()` method for handling signal boundaries.

"""

FFT_MODE_TYPE = Literal['twosided', 'centered', 'onesided', 'onesided2X']
"""Allowed values for property `ShortTimeFFT.fft_mode`.

(AI generated docstring)

Type literal defining the valid FFT mode configurations for scipy's
`ShortTimeFFT` class property `fft_mode`.

"""

# TODO Automate a process to AST into scipy, check the status of the above types,
# update if needed, or notify me if scipy has made them public symbols.
