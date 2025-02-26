from typing import Literal

#: Allowed values for parameter `padding` of method `ShortTimeFFT.stft()`:
PAD_TYPE = Literal['zeros', 'edge', 'even', 'odd']

#: Allowed values for property `ShortTimeFFT.fft_mode`:
FFT_MODE_TYPE = Literal['twosided', 'centered', 'onesided', 'onesided2X']

# TODO
# Automate a process to AST into scipy, check the status of the above types,
# update if needed, or notify me if scipy has made them public symbols.
