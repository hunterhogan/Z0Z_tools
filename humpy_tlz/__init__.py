"""``humpy_tlz`` mirrors the ``humpy_toolz`` API and uses ``humpy_cytoolz`` if possible.

The ``humpy_tlz`` package is installed when ``humpy_toolz`` is installed.  It provides
a convenient way to use functions from ``humpy_cytoolz``--a faster Cython
implementation of ``humpy_toolz``--if it is installed, otherwise it uses
functions from ``humpy_toolz``.
"""
from __future__ import annotations

from . import _build_tlz  # pyright: ignore[reportUnusedImport]
