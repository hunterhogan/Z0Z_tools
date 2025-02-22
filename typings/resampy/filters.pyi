__all__ = ['get_filter', 'clear_cache', 'sinc_window']

def sinc_window(num_zeros: int = ..., precision: int = ..., window, rolloff: float = ...):
    """Construct a windowed sinc interpolation filter

    Parameters
    ----------
    num_zeros : int > 0
        The number of zero-crossings to retain in the sinc filter
    precision : int > 0
        The number of filter coefficients to retain for each zero-crossing
    window : callable
        The window function.  By default, uses a Hann window.
    rolloff : float > 0
        The roll-off frequency (as a fraction of nyquist)

    Returns
    -------
    interp_window: np.ndarray [shape=(num_zeros * num_table + 1)]
        The interpolation window (right-hand side)
    num_bits: int
        The number of bits of precision to use in the filter table
    rolloff : float > 0
        The roll-off frequency of the filter, as a fraction of Nyquist

    Raises
    ------
    TypeError
        if `window` is not callable or `None`
    ValueError
        if `num_zeros < 1`, `precision < 1`,
        or `rolloff` is outside the range `(0, 1]`.

    Examples
    --------
    >>> import scipy, scipy.signal
    >>> import resampy
    >>> np.set_printoptions(threshold=5, suppress=False)
    >>> # A filter with 10 zero-crossings, 32 samples per crossing, and a
    >>> # Hann window for tapering.
    >>> halfwin, prec, rolloff = resampy.filters.sinc_window(num_zeros=10, precision=5,
    ...                                                      window=scipy.signal.windows.hann)
    >>> halfwin
    array([  9.450e-01,   9.436e-01, ...,  -7.455e-07,  -0.000e+00])
    >>> prec
    32
    >>> rolloff
    0.945

    >>> # Or using sinc-window filter construction directly in resample
    >>> y = resampy.resample(x, sr_orig, sr_new, filter='sinc_window',
    ...                      num_zeros=10, precision=5,
    ...                      window=scipy.signal.windows.hann)      # doctest: +SKIP
    """
def get_filter(name_or_function, **kwargs):
    """Retrieve a window given its name or function handle.

    Parameters
    ----------
    name_or_function : str or callable
        If a function, returns `name_or_function(**kwargs)`.

        If a string, and it matches the name of one of the defined
        filter functions, the corresponding function is called with `**kwargs`.

        If a string, and it matches the name of a pre-computed filter,
        the corresponding filter is retrieved, and kwargs is ignored.

        Valid pre-computed filter names are:
            - 'kaiser_fast'
            - 'kaiser_best'

    **kwargs
        Additional keyword arguments passed to `name_or_function` (if callable)

    Returns
    -------
    half_window : np.ndarray
        The right wing of the interpolation filter
    precision : int > 0
        The number of samples between zero-crossings of the filter
    rolloff : float > 0
        The roll-off frequency of the filter as a fraction of Nyquist

    Raises
    ------
    NotImplementedError
        If `name_or_function` cannot be found as a filter.
    """
def clear_cache():
    """Clear the filter cache.

    Calling this function will ensure that packaged filters are reloaded
    upon the next usage.
    """
