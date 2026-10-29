# Z0Z_tools

Typed Cython utilities for iterators, mappings, and function composition. The distribution
contains `humpy_cytoolz` and `Z0Z_tools`.
The audio processing modules previously in this repository now live in
[`hunterHearsPy`](https://github.com/hunterhogan/hunterHearsPy).

## humpy_cytoolz

`humpy_cytoolz` is a typed fork of [`cytoolz`](https://github.com/pytoolz/cytoolz). The core modules
`dicttoolz`, `functoolz`, `itertoolz`, `recipes`, and `utils` are built as extension
modules.

The Cython implementations and their type stubs are maintained directly. Functions with
matching maintained implementations use aliases from the standard library or `more-itertools`.
`humpy_toolz` and `humpy_tlz` remain in the repository as reference sources.

```python
from humpy_cytoolz import curry, groupby, merge
```

## Z0Z_tools utilities

`Z0Z_tools` provides membership predicates, ordering checks, sequence filtering, and mapping
utilities.

```python
from Z0Z_tools import between吗, exclude, reverseLookup
```

## Standard library `operator` module is "curried"

```python
from humpy_cytoolz.curried import operator
```

## Installation

```bash
pip install Z0Z_tools
```

## Sources

1. [toolz](https://github.com/pytoolz/toolz)
2. [cytoolz](https://github.com/pytoolz/cytoolz)
3. [toolz-stubs](https://github.com/mgrinshpon/toolz-stubs)
4. [cytoolz-stubs](https://github.com/OutSquareCapital/cytoolz-stubs)

## My recovery

[![Static Badge](https://img.shields.io/badge/2011_August-Homeless_since-blue?style=flat)](https://HunterThinks.com/support)
[![CC-BY-NC-4.0](https://raw.githubusercontent.com/hunterhogan/Z0Z_tools/refs/heads/main/.github/CC-BY-NC-4.0.png)](https://creativecommons.org/licenses/by-nc/4.0/)

By law, authors retain their copyrights unless they grant exceptions. The [Attribution-NonCommercial 4.0 International Deed](https://github.com/hunterhogan/Z0Z_tools#License-1-ov-file) outlines how you may use this work.

The restriction on commercial use (without a license) limits advantage-taking, unjust enrichment, and exploitation. You would be morally wrong if you were to enrich yourself by using this work while I am denied healthcare, housing, security of property, and the safety of my person.

To obtain and retain the right to use this work, you incur the cost of attributing the work to me. Your nominal cost might accrue as a benefit that mitigates my suffering or saves my life.
