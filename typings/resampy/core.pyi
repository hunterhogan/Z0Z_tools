__all__ = ['resample', 'resample_nu']

def resample(x, sr_orig, sr_new, axis: int = ..., filter: str = ..., parallel: bool = ..., **kwargs):
    """Resample a signal x from sr_orig to sr_new along a given axis.

    Parameters
    ----------
    x : np.ndarray, dtype=np.float*
        The input signal(s) to resample.

    sr_orig : int > 0
        The sampling rate of x

    sr_new : int > 0
        The target sampling rate of the output signal(s)

        If `sr_new == sr_orig`, then a copy of `x` is returned with no
        interpolation performed.

    axis : int
        The target axis along which to resample `x`

    filter : optional, str or callable
        The resampling filter to use.

        By default, uses the `kaiser_best` (pre-computed filter).

    parallel : optional, bool
        Enable/disable parallel computation exploiting multi-threading.

        Default: False.

    **kwargs
        additional keyword arguments provided to the specified filter

    Returns
    -------
    y : np.ndarray
        `x` resampled to `sr_new`

    Raises
    ------
    ValueError
        if `sr_orig` or `sr_new` is not positive
    TypeError
        if the input signal `x` has an unsupported data type.

    Examples
    --------
    >>> import resampy
    >>> np.set_printoptions(precision=3, suppress=True)
    >>> # Generate a sine wave at 440 Hz for 5 seconds
    >>> sr_orig = 44100.0
    >>> x = np.sin(2 * np.pi * 440.0 / sr_orig * np.arange(5 * sr_orig))
    >>> x
    array([ 0.   ,  0.063, ..., -0.125, -0.063])
    >>> # Resample to 22050 with default parameters
    >>> resampy.resample(x, sr_orig, 22050)
    array([ 0.011,  0.122,  0.25 , ..., -0.366, -0.25 , -0.122])
    >>> # Resample using the fast (low-quality) filter
    >>> resampy.resample(x, sr_orig, 22050, filter='kaiser_fast')
    array([ 0.012,  0.121,  0.251, ..., -0.365, -0.251, -0.121])
    >>> # Resample using a high-quality filter
    >>> resampy.resample(x, sr_orig, 22050, filter='kaiser_best')
    array([ 0.011,  0.122,  0.25 , ..., -0.366, -0.25 , -0.122])
    >>> # Resample using a Hann-windowed sinc filter
    >>> import scipy.signal
    >>> resampy.resample(x, sr_orig, 22050, filter='sinc_window',
    ...                  window=scipy.signal.windows.hann)
    array([ 0.011,  0.123,  0.25 , ..., -0.366, -0.25 , -0.123])

    >>> # Generate stereo data
    >>> x_right = np.sin(2 * np.pi * 880.0 / sr_orig * np.arange(len(x)))
    >>> x_stereo = np.stack([x, x_right])
    >>> x_stereo.shape
    (2, 220500)
    >>> # Resample along the time axis (1)
    >>> y_stereo = resampy.resample(x_stereo, sr_orig, 22050, axis=1)
    >>> y_stereo.shape
    (2, 110250)
    """
def resample_nu(x, sr_orig, t_out, axis: int = ..., filter: str = ..., parallel: bool = ..., **kwargs):
    """Interpolate a signal x at specified positions (t_out) along a given axis.

    Parameters
    ----------
    x : np.ndarray, dtype=np.float*
        The input signal(s) to resample.

    sr_orig : float
        Sampling rate of the input signal (x).

    t_out : np.ndarray, dtype=np.float*
        Position of the output samples.

    axis : int
        The target axis along which to resample `x`

    filter : optional, str or callable
        The resampling filter to use.

        By default, uses the `kaiser_best` (pre-computed filter).

    parallel : optional, bool
        Enable/disable parallel computation exploiting multi-threading.

        Default: True.

    **kwargs
        additional keyword arguments provided to the specified filter

    Returns
    -------
    y : np.ndarray
        `x` resampled to `t_out`

    Raises
    ------
    TypeError
        if the input signal `x` has an unsupported data type.

    Notes
    -----
    Differently form the `resample` function the filter `rolloff`
    is not automatically adapted in case of subsampling.
    For this reason results obtained with the `resample_nu` could be slightly
    different form the ones obtained with `resample` if the filter
    parameters are not carefully set by the user.

    Examples
    --------
    >>> import resampy
    >>> np.set_printoptions(precision=3, suppress=True)
    >>> # Generate a sine wave at 100 Hz for 5 seconds
    >>> sr_orig = 100.0
    >>> f0 = 1
    >>> t = np.arange(5 * sr_orig) / sr_orig
    >>> x = np.sin(2 * np.pi * f0 * t)
    >>> x
    array([ 0.   ,  0.063,  0.125, ..., -0.187, -0.125, -0.063])
    >>> # Resample to non-uniform sampling
    >>> t_new = np.log2(1 + t)[::5] - t[0]
    >>> resampy.resample_nu(x, sr_orig, t_new)
    array([ 0.001,  0.427,  0.76 , ..., -0.3  , -0.372, -0.442])
    """
