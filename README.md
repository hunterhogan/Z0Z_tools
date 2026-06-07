# Z0Z_tools

Filesystem helpers plus the `humpy_toolz`, `humpy_cytoolz`, and `humpy_tlz` packages.
The audio processing modules previously in this repository now live in
[`hunterHearsPy`](https://github.com/hunterhogan/hunterHearsPy).

## Wishlist

- [ ] Build wheels in "pypiReleaseCython.yml" workflow.

## humpy_toolz

`humpy_toolz` is a typed fork of [`toolz`](https://github.com/pytoolz/toolz). It provides
composable functions for iterators, dictionaries, and function composition with type stubs.

```python
from humpy_toolz import compose_left, curry, merge, pipe

merged = merge({"a": 1}, {"b": 2})
transform = compose_left(lambda x: x + 1, lambda x: x * 2)
result = pipe(3, transform)
```

## humpy_cytoolz

`humpy_cytoolz` is the Cython-accelerated companion package. The core modules
`dicttoolz`, `functoolz`, `itertoolz`, `recipes`, and `utils` are built as extension
modules.

```python
from humpy_cytoolz import curry, groupby, merge
```

## humpy_tlz

`humpy_tlz` mirrors the `humpy_toolz` API and imports from `humpy_cytoolz` when available,
falling back to `humpy_toolz` otherwise.

```python
from humpy_tlz import curry, groupby, pipe
```

## Installation

```bash
pip install Z0Z_tools
```

## My recovery

[![Static Badge](https://img.shields.io/badge/2011_August-Homeless_since-blue?style=flat)](https://HunterThinks.com/support)
[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UC3Gx7kz61009NbhpRtPP7tw)](https://www.youtube.com/@HunterHogan)

[![CC-BY-NC-4.0](https://raw.githubusercontent.com/hunterhogan/Z0Z_tools/refs/heads/main/.github/CC-BY-NC-4.0.png)](https://creativecommons.org/licenses/by-nc/4.0/)
