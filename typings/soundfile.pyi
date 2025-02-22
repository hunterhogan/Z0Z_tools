import _cffi_backend
from typing import ClassVar

__version__: str
SEEK_SET: int
SEEK_CUR: int
SEEK_END: int
_ffi: _cffi_backend.FFI
_str_types: dict
_formats: dict
_subtypes: dict
_endians: dict
_default_subtypes: dict
_ffi_types: dict
_bitrate_modes: dict
_packaged_libname: str
_path: str
_full_path: str
__libsndfile_version__: str
def read(file, frames: int = ..., start: int = ..., stop, dtype: str = ..., always_2d: bool = ..., fill_value, out, samplerate, channels, format, subtype, endian, closefd: bool = ...):
    """Provide audio data from a sound file as NumPy array.

    By default, the whole file is read from the beginning, but the
    position to start reading can be specified with *start* and the
    number of frames to read can be specified with *frames*.
    Alternatively, a range can be specified with *start* and *stop*.

    If there is less data left in the file than requested, the rest of
    the frames are filled with *fill_value*.
    If no *fill_value* is specified, a smaller array is returned.

    Parameters
    ----------
    file : str or int or file-like object
        The file to read from.  See `SoundFile` for details.
    frames : int, optional
        The number of frames to read. If *frames* is negative, the whole
        rest of the file is read.  Not allowed if *stop* is given.
    start : int, optional
        Where to start reading.  A negative value counts from the end.
    stop : int, optional
        The index after the last frame to be read.  A negative value
        counts from the end.  Not allowed if *frames* is given.
    dtype : {'float64', 'float32', 'int32', 'int16'}, optional
        Data type of the returned array, by default ``'float64'``.
        Floating point audio data is typically in the range from
        ``-1.0`` to ``1.0``.  Integer data is in the range from
        ``-2**15`` to ``2**15-1`` for ``'int16'`` and from ``-2**31`` to
        ``2**31-1`` for ``'int32'``.

        .. note:: Reading int values from a float file will *not*
            scale the data to [-1.0, 1.0). If the file contains
            ``np.array([42.6], dtype='float32')``, you will read
            ``np.array([43], dtype='int32')`` for ``dtype='int32'``.

    Returns
    -------
    audiodata : `numpy.ndarray` or type(out)
        A two-dimensional (frames x channels) NumPy array is returned.
        If the sound file has only one channel, a one-dimensional array
        is returned.  Use ``always_2d=True`` to return a two-dimensional
        array anyway.

        If *out* was specified, it is returned.  If *out* has more
        frames than available in the file (or if *frames* is smaller
        than the length of *out*) and no *fill_value* is given, then
        only a part of *out* is overwritten and a view containing all
        valid frames is returned.
    samplerate : int
        The sample rate of the audio file.

    Other Parameters
    ----------------
    always_2d : bool, optional
        By default, reading a mono sound file will return a
        one-dimensional array.  With ``always_2d=True``, audio data is
        always returned as a two-dimensional array, even if the audio
        file has only one channel.
    fill_value : float, optional
        If more frames are requested than available in the file, the
        rest of the output is be filled with *fill_value*.  If
        *fill_value* is not specified, a smaller array is returned.
    out : `numpy.ndarray` or subclass, optional
        If *out* is specified, the data is written into the given array
        instead of creating a new array.  In this case, the arguments
        *dtype* and *always_2d* are silently ignored!  If *frames* is
        not given, it is obtained from the length of *out*.
    samplerate, channels, format, subtype, endian, closefd
        See `SoundFile`.

    Examples
    --------
    >>> import soundfile as sf
    >>> data, samplerate = sf.read('stereo_file.wav')
    >>> data
    array([[ 0.71329652,  0.06294799],
           [-0.26450912, -0.38874483],
           ...
           [ 0.67398441, -0.11516333]])
    >>> samplerate
    44100

    """
def write(file, data, samplerate, subtype, endian, format, closefd: bool = ..., compression_level, bitrate_mode):
    """Write data to a sound file.

    .. note:: If *file* exists, it will be truncated and overwritten!

    Parameters
    ----------
    file : str or int or file-like object
        The file to write to.  See `SoundFile` for details.
    data : array_like
        The data to write.  Usually two-dimensional (frames x channels),
        but one-dimensional *data* can be used for mono files.
        Only the data types ``'float64'``, ``'float32'``, ``'int32'``
        and ``'int16'`` are supported.

        .. note:: The data type of *data* does **not** select the data
                  type of the written file. Audio data will be
                  converted to the given *subtype*. Writing int values
                  to a float file will *not* scale the values to
                  [-1.0, 1.0). If you write the value ``np.array([42],
                  dtype='int32')``, to a ``subtype='FLOAT'`` file, the
                  file will then contain ``np.array([42.],
                  dtype='float32')``.

    samplerate : int
        The sample rate of the audio data.
    subtype : str, optional
        See `default_subtype()` for the default value and
        `available_subtypes()` for all possible values.

    Other Parameters
    ----------------
    format, endian, closefd, compression_level, bitrate_mode
        See `SoundFile`.

    Examples
    --------
    Write 10 frames of random data to a new file:

    >>> import numpy as np
    >>> import soundfile as sf
    >>> sf.write('stereo_file.wav', np.random.randn(10, 2), 44100, 'PCM_24')

    """
def blocks(file, blocksize, overlap: int = ..., frames: int = ..., start: int = ..., stop, dtype: str = ..., always_2d: bool = ..., fill_value, out, samplerate, channels, format, subtype, endian, closefd: bool = ...):
    """Return a generator for block-wise reading.

    By default, iteration starts at the beginning and stops at the end
    of the file.  Use *start* to start at a later position and *frames*
    or *stop* to stop earlier.

    If you stop iterating over the generator before it's exhausted,
    the sound file is not closed. This is normally not a problem
    because the file is opened in read-only mode. To close the file
    properly, the generator's ``close()`` method can be called.

    Parameters
    ----------
    file : str or int or file-like object
        The file to read from.  See `SoundFile` for details.
    blocksize : int
        The number of frames to read per block.
        Either this or *out* must be given.
    overlap : int, optional
        The number of frames to rewind between each block.

    Yields
    ------
    `numpy.ndarray` or type(out)
        Blocks of audio data.
        If *out* was given, and the requested frames are not an integer
        multiple of the length of *out*, and no *fill_value* was given,
        the last block will be a smaller view into *out*.

    Other Parameters
    ----------------
    frames, start, stop
        See `read()`.
    dtype : {'float64', 'float32', 'int32', 'int16'}, optional
        See `read()`.
    always_2d, fill_value, out
        See `read()`.
    samplerate, channels, format, subtype, endian, closefd
        See `SoundFile`.

    Examples
    --------
    >>> import soundfile as sf
    >>> for block in sf.blocks('stereo_file.wav', blocksize=1024):
    >>>     pass  # do something with 'block'

    """

class _SoundFileInfo:
    def __init__(self, file, verbose) -> None: ...
    @property
    def _duration_str(self): ...
def info(file, verbose: bool = ...):
    """Returns an object with information about a `SoundFile`.

    Parameters
    ----------
    verbose : bool
        Whether to print additional information.
    """
def available_formats():
    """Return a dictionary of available major formats.

    Examples
    --------
    >>> import soundfile as sf
    >>> sf.available_formats()
    {'FLAC': 'FLAC (FLAC Lossless Audio Codec)',
     'OGG': 'OGG (OGG Container format)',
     'WAV': 'WAV (Microsoft)',
     'AIFF': 'AIFF (Apple/SGI)',
     ...
     'WAVEX': 'WAVEX (Microsoft)',
     'RAW': 'RAW (header-less)',
     'MAT5': 'MAT5 (GNU Octave 2.1 / Matlab 5.0)'}

    """
def available_subtypes(format):
    """Return a dictionary of available subtypes.

    Parameters
    ----------
    format : str
        If given, only compatible subtypes are returned.

    Examples
    --------
    >>> import soundfile as sf
    >>> sf.available_subtypes('FLAC')
    {'PCM_24': 'Signed 24 bit PCM',
     'PCM_16': 'Signed 16 bit PCM',
     'PCM_S8': 'Signed 8 bit PCM'}

    """
def check_format(format, subtype, endian):
    """Check if the combination of format/subtype/endian is valid.

    Examples
    --------
    >>> import soundfile as sf
    >>> sf.check_format('WAV', 'PCM_24')
    True
    >>> sf.check_format('FLAC', 'VORBIS')
    False

    """
def default_subtype(format):
    """Return the default subtype for a given format.

    Examples
    --------
    >>> import soundfile as sf
    >>> sf.default_subtype('WAV')
    'PCM_16'
    >>> sf.default_subtype('MAT5')
    'DOUBLE'

    """

class SoundFile:
    _file: ClassVar[None] = ...
    def __init__(self, file, mode: str = ..., samplerate, channels, subtype, endian, format, closefd: bool = ..., compression_level, bitrate_mode) -> None:
        '''Open a sound file.

        If a file is opened with `mode` ``\'r\'`` (the default) or
        ``\'r+\'``, no sample rate, channels or file format need to be
        given because the information is obtained from the file. An
        exception is the ``\'RAW\'`` data format, which always requires
        these data points.

        File formats consist of three case-insensitive strings:

        * a *major format* which is by default obtained from the
          extension of the file name (if known) and which can be
          forced with the format argument (e.g. ``format=\'WAVEX\'``).
        * a *subtype*, e.g. ``\'PCM_24\'``. Most major formats have a
          default subtype which is used if no subtype is specified.
        * an *endian-ness*, which doesn\'t have to be specified at all in
          most cases.

        A `SoundFile` object is a *context manager*, which means
        if used in a "with" statement, `close()` is automatically
        called when reaching the end of the code block inside the "with"
        statement.

        Parameters
        ----------
        file : str or int or file-like object
            The file to open.  This can be a file name, a file
            descriptor or a Python file object (or a similar object with
            the methods ``read()``/``readinto()``, ``write()``,
            ``seek()`` and ``tell()``).
        mode : {\'r\', \'r+\', \'w\', \'w+\', \'x\', \'x+\'}, optional
            Open mode.  Has to begin with one of these three characters:
            ``\'r\'`` for reading, ``\'w\'`` for writing (truncates *file*)
            or ``\'x\'`` for writing (raises an error if *file* already
            exists).  Additionally, it may contain ``\'+\'`` to open
            *file* for both reading and writing.
            The character ``\'b\'`` for *binary mode* is implied because
            all sound files have to be opened in this mode.
            If *file* is a file descriptor or a file-like object,
            ``\'w\'`` doesn\'t truncate and ``\'x\'`` doesn\'t raise an error.
        samplerate : int
            The sample rate of the file.  If `mode` contains ``\'r\'``,
            this is obtained from the file (except for ``\'RAW\'`` files).
        channels : int
            The number of channels of the file.
            If `mode` contains ``\'r\'``, this is obtained from the file
            (except for ``\'RAW\'`` files).
        subtype : str, sometimes optional
            The subtype of the sound file.  If `mode` contains ``\'r\'``,
            this is obtained from the file (except for ``\'RAW\'``
            files), if not, the default value depends on the selected
            `format` (see `default_subtype()`).
            See `available_subtypes()` for all possible subtypes for
            a given `format`.
        endian : {\'FILE\', \'LITTLE\', \'BIG\', \'CPU\'}, sometimes optional
            The endian-ness of the sound file.  If `mode` contains
            ``\'r\'``, this is obtained from the file (except for
            ``\'RAW\'`` files), if not, the default value is ``\'FILE\'``,
            which is correct in most cases.
        format : str, sometimes optional
            The major format of the sound file.  If `mode` contains
            ``\'r\'``, this is obtained from the file (except for
            ``\'RAW\'`` files), if not, the default value is determined
            from the file extension.  See `available_formats()` for
            all possible values.
        closefd : bool, optional
            Whether to close the file descriptor on `close()`. Only
            applicable if the *file* argument is a file descriptor.
        compression_level : float, optional
            The compression level on \'write()\'. The compression level
            should be between 0.0 (minimum compression level) and 1.0
            (highest compression level).
            See `libsndfile document <https://github.com/libsndfile/libsndfile/blob/c81375f070f3c6764969a738eacded64f53a076e/docs/command.md>`__.
        bitrate_mode : {\'CONSTANT\', \'AVERAGE\', \'VARIABLE\'}, optional
            The bitrate mode on \'write()\'. 
            See `libsndfile document <https://github.com/libsndfile/libsndfile/blob/c81375f070f3c6764969a738eacded64f53a076e/docs/command.md>`__.

        Examples
        --------
        >>> from soundfile import SoundFile

        Open an existing file for reading:

        >>> myfile = SoundFile(\'existing_file.wav\')
        >>> # do something with myfile
        >>> myfile.close()

        Create a new sound file for reading and writing using a with
        statement:

        >>> with SoundFile(\'new_file.wav\', \'x+\', 44100, 2) as myfile:
        >>>     # do something with myfile
        >>>     # ...
        >>>     assert not myfile.closed
        >>>     # myfile.close() is called automatically at the end
        >>> assert myfile.closed

        '''
    def __del__(self) -> None: ...
    def __enter__(self): ...
    def __exit__(self, *args): ...
    def __setattr__(self, name, value):
        """Write text meta-data in the sound file through properties."""
    def __getattr__(self, name):
        """Read text meta-data in the sound file through properties."""
    def __len__(self) -> int: ...
    def __bool__(self) -> bool: ...
    def __nonzero__(self): ...
    def seekable(self):
        """Return True if the file supports seeking."""
    def seek(self, frames, whence: int = ...):
        """Set the read/write position.

        Parameters
        ----------
        frames : int
            The frame index or offset to seek.
        whence : {SEEK_SET, SEEK_CUR, SEEK_END}, optional
            By default (``whence=SEEK_SET``), *frames* are counted from
            the beginning of the file.
            ``whence=SEEK_CUR`` seeks from the current position
            (positive and negative values are allowed for *frames*).
            ``whence=SEEK_END`` seeks from the end (use negative value
            for *frames*).

        Returns
        -------
        int
            The new absolute read/write position in frames.

        Examples
        --------
        >>> from soundfile import SoundFile, SEEK_END
        >>> myfile = SoundFile('stereo_file.wav')

        Seek to the beginning of the file:

        >>> myfile.seek(0)
        0

        Seek to the end of the file:

        >>> myfile.seek(0, SEEK_END)
        44100  # this is the file length

        """
    def tell(self):
        """Return the current read/write position."""
    def read(self, frames: int = ..., dtype: str = ..., always_2d: bool = ..., fill_value, out):
        """Read from the file and return data as NumPy array.

        Reads the given number of frames in the given data format
        starting at the current read/write position.  This advances the
        read/write position by the same number of frames.
        By default, all frames from the current read/write position to
        the end of the file are returned.
        Use `seek()` to move the current read/write position.

        Parameters
        ----------
        frames : int, optional
            The number of frames to read. If ``frames < 0``, the whole
            rest of the file is read.
        dtype : {'float64', 'float32', 'int32', 'int16'}, optional
            Data type of the returned array, by default ``'float64'``.
            Floating point audio data is typically in the range from
            ``-1.0`` to ``1.0``. Integer data is in the range from
            ``-2**15`` to ``2**15-1`` for ``'int16'`` and from
            ``-2**31`` to ``2**31-1`` for ``'int32'``.

            .. note:: Reading int values from a float file will *not*
                scale the data to [-1.0, 1.0). If the file contains
                ``np.array([42.6], dtype='float32')``, you will read
                ``np.array([43], dtype='int32')`` for
                ``dtype='int32'``.

        Returns
        -------
        audiodata : `numpy.ndarray` or type(out)
            A two-dimensional NumPy (frames x channels) array is
            returned. If the sound file has only one channel, a
            one-dimensional array is returned. Use ``always_2d=True``
            to return a two-dimensional array anyway.

            If *out* was specified, it is returned. If *out* has more
            frames than available in the file (or if *frames* is
            smaller than the length of *out*) and no *fill_value* is
            given, then only a part of *out* is overwritten and a view
            containing all valid frames is returned.

        Other Parameters
        ----------------
        always_2d : bool, optional
            By default, reading a mono sound file will return a
            one-dimensional array. With ``always_2d=True``, audio data
            is always returned as a two-dimensional array, even if the
            audio file has only one channel.
        fill_value : float, optional
            If more frames are requested than available in the file,
            the rest of the output is be filled with *fill_value*. If
            *fill_value* is not specified, a smaller array is
            returned.
        out : `numpy.ndarray` or subclass, optional
            If *out* is specified, the data is written into the given
            array instead of creating a new array. In this case, the
            arguments *dtype* and *always_2d* are silently ignored! If
            *frames* is not given, it is obtained from the length of
            *out*.

        Examples
        --------
        >>> from soundfile import SoundFile
        >>> myfile = SoundFile('stereo_file.wav')

        Reading 3 frames from a stereo file:

        >>> myfile.read(3)
        array([[ 0.71329652,  0.06294799],
               [-0.26450912, -0.38874483],
               [ 0.67398441, -0.11516333]])
        >>> myfile.close()

        See Also
        --------
        buffer_read, .write

        """
    def buffer_read(self, frames: int = ..., dtype):
        """Read from the file and return data as buffer object.

        Reads the given number of *frames* in the given data format
        starting at the current read/write position.  This advances the
        read/write position by the same number of frames.
        By default, all frames from the current read/write position to
        the end of the file are returned.
        Use `seek()` to move the current read/write position.

        Parameters
        ----------
        frames : int, optional
            The number of frames to read. If ``frames < 0``, the whole
            rest of the file is read.
        dtype : {'float64', 'float32', 'int32', 'int16'}
            Audio data will be converted to the given data type.

        Returns
        -------
        buffer
            A buffer containing the read data.

        See Also
        --------
        buffer_read_into, .read, buffer_write

        """
    def buffer_read_into(self, buffer, dtype):
        """Read from the file into a given buffer object.

        Fills the given *buffer* with frames in the given data format
        starting at the current read/write position (which can be
        changed with `seek()`) until the buffer is full or the end
        of the file is reached.  This advances the read/write position
        by the number of frames that were read.

        Parameters
        ----------
        buffer : writable buffer
            Audio frames from the file are written to this buffer.
        dtype : {'float64', 'float32', 'int32', 'int16'}
            The data type of *buffer*.

        Returns
        -------
        int
            The number of frames that were read from the file.
            This can be less than the size of *buffer*.
            The rest of the buffer is not filled with meaningful data.

        See Also
        --------
        buffer_read, .read

        """
    def write(self, data):
        """Write audio data from a NumPy array to the file.

        Writes a number of frames at the read/write position to the
        file. This also advances the read/write position by the same
        number of frames and enlarges the file if necessary.

        Note that writing int values to a float file will *not* scale
        the values to [-1.0, 1.0). If you write the value
        ``np.array([42], dtype='int32')``, to a ``subtype='FLOAT'``
        file, the file will then contain ``np.array([42.],
        dtype='float32')``.

        Parameters
        ----------
        data : array_like
            The data to write. Usually two-dimensional (frames x
            channels), but one-dimensional *data* can be used for mono
            files. Only the data types ``'float64'``, ``'float32'``,
            ``'int32'`` and ``'int16'`` are supported.

            .. note:: The data type of *data* does **not** select the
                  data type of the written file. Audio data will be
                  converted to the given *subtype*. Writing int values
                  to a float file will *not* scale the values to
                  [-1.0, 1.0). If you write the value ``np.array([42],
                  dtype='int32')``, to a ``subtype='FLOAT'`` file, the
                  file will then contain ``np.array([42.],
                  dtype='float32')``.

        Examples
        --------
        >>> import numpy as np
        >>> from soundfile import SoundFile
        >>> myfile = SoundFile('stereo_file.wav')

        Write 10 frames of random data to a new file:

        >>> with SoundFile('stereo_file.wav', 'w', 44100, 2, 'PCM_24') as f:
        >>>     f.write(np.random.randn(10, 2))

        See Also
        --------
        buffer_write, .read

        """
    def buffer_write(self, data, dtype):
        """Write audio data from a buffer/bytes object to the file.

        Writes the contents of *data* to the file at the current
        read/write position.
        This also advances the read/write position by the number of
        frames that were written and enlarges the file if necessary.

        Parameters
        ----------
        data : buffer or bytes
            A buffer or bytes object containing the audio data to be
            written.
        dtype : {'float64', 'float32', 'int32', 'int16'}
            The data type of the audio data stored in *data*.

        See Also
        --------
        .write, buffer_read

        """
    def blocks(self, blocksize, overlap: int = ..., frames: int = ..., dtype: str = ..., always_2d: bool = ..., fill_value, out):
        """Return a generator for block-wise reading.

        By default, the generator yields blocks of the given
        *blocksize* (using a given *overlap*) until the end of the file
        is reached; *frames* can be used to stop earlier.

        Parameters
        ----------
        blocksize : int
            The number of frames to read per block. Either this or *out*
            must be given.
        overlap : int, optional
            The number of frames to rewind between each block.
        frames : int, optional
            The number of frames to read.
            If ``frames < 0``, the file is read until the end.
        dtype : {'float64', 'float32', 'int32', 'int16'}, optional
            See `read()`.

        Yields
        ------
        `numpy.ndarray` or type(out)
            Blocks of audio data.
            If *out* was given, and the requested frames are not an
            integer multiple of the length of *out*, and no
            *fill_value* was given, the last block will be a smaller
            view into *out*.


        Other Parameters
        ----------------
        always_2d, fill_value, out
            See `read()`.
        fill_value : float, optional
            See `read()`.
        out : `numpy.ndarray` or subclass, optional
            If *out* is specified, the data is written into the given
            array instead of creating a new array. In this case, the
            arguments *dtype* and *always_2d* are silently ignored!

        Examples
        --------
        >>> from soundfile import SoundFile
        >>> with SoundFile('stereo_file.wav') as f:
        >>>     for block in f.blocks(blocksize=1024):
        >>>         pass  # do something with 'block'

        """
    def truncate(self, frames):
        """Truncate the file to a given number of frames.

        After this command, the read/write position will be at the new
        end of the file.

        Parameters
        ----------
        frames : int, optional
            Only the data before *frames* is kept, the rest is deleted.
            If not specified, the current read/write position is used.

        """
    def flush(self):
        """Write unwritten data to the file system.

        Data written with `write()` is not immediately written to
        the file system but buffered in memory to be written at a later
        time.  Calling `flush()` makes sure that all changes are
        actually written to the file system.

        This has no effect on files opened in read-only mode.

        """
    def close(self):
        """Close the file.  Can be called multiple times."""
    def _open(self, file, mode_int, closefd):
        """Call the appropriate sf_open*() function from libsndfile."""
    def _init_virtual_io(self, file):
        """Initialize callback functions for sf_open_virtual()."""
    def _getAttributeNames(self):
        """Return all attributes used in __setattr__ and __getattr__.

        This is useful for auto-completion (e.g. IPython).

        """
    def _check_if_closed(self):
        """Check if the file is closed and raise an error if it is.

        This should be used in every method that uses self._file.

        """
    def _check_frames(self, frames, fill_value):
        """Reduce frames to no more than are available in the file."""
    def _check_buffer(self, data, ctype):
        """Convert buffer to cdata and check for valid size."""
    def _create_empty_array(self, frames, always_2d, dtype):
        """Create an empty array with appropriate shape."""
    def _check_dtype(self, dtype):
        """Check if dtype string is valid and return ctype string."""
    def _array_io(self, action, array, frames):
        """Check array and call low-level IO function."""
    def _cdata_io(self, action, data, ctype, frames):
        """Call one of libsndfile's read/write functions."""
    def _update_frames(self, written):
        """Update self.frames after writing."""
    def _prepare_read(self, start, stop, frames):
        """Seek to start frame and calculate length."""
    def copy_metadata(self):
        """Get all metadata present in this SoundFile

        Returns
        -------

        metadata: dict[str, str]
            A dict with all metadata. Possible keys are: 'title', 'copyright',
            'software', 'artist', 'comment', 'date', 'album', 'license',
            'tracknumber' and 'genre'.
        """
    def _set_bitrate_mode(self, bitrate_mode):
        """Call libsndfile's set bitrate mode function."""
    def _set_compression_level(self, compression_level):
        """Call libsndfile's set compression level function."""
    @property
    def name(self): ...
    @property
    def mode(self): ...
    @property
    def samplerate(self): ...
    @property
    def frames(self): ...
    @property
    def channels(self): ...
    @property
    def format(self): ...
    @property
    def subtype(self): ...
    @property
    def endian(self): ...
    @property
    def format_info(self): ...
    @property
    def subtype_info(self): ...
    @property
    def sections(self): ...
    @property
    def closed(self): ...
    @property
    def _errorcode(self): ...
    @property
    def compression_level(self): ...
    @property
    def bitrate_mode(self): ...
    @property
    def extra_info(self): ...
def _error_check(err, prefix: str = ...):
    """Raise LibsndfileError if there is an error."""
def _format_int(format, subtype, endian):
    """Return numeric ID for given format|subtype|endian combo."""
def _check_mode(mode):
    """Check if mode is valid and return its integer representation."""
def _create_info_struct(file, mode, samplerate, channels, format, subtype, endian):
    """Check arguments and create SF_INFO struct."""
def _get_format_from_filename(file, mode):
    """Return a format string obtained from file (or file.name).

    If file already exists (= read mode), an empty string is returned on
    error.  If not, an exception is raised.
    The return type will always be str or unicode (even if
    file/file.name is a bytes object).

    """
def _format_str(format_int):
    """Return the string representation of a given numeric format."""
def _format_info(format_int, format_flag: int = ...):
    """Return the ID and short description of a given format."""
def _available_formats_helper(count_flag, format_flag):
    """Helper for available_formats() and available_subtypes()."""
def _check_format(format_str):
    """Check if `format_str` is valid and return format ID."""
def _has_virtual_io_attrs(file, mode_int):
    """Check if file has all the necessary attributes for virtual IO."""

class SoundFileError(Exception): ...
class SoundFileRuntimeError(SoundFileError, RuntimeError): ...

class LibsndfileError(SoundFileRuntimeError):
    def __init__(self, code, prefix: str = ...) -> None: ...
    @property
    def error_string(self): ...
