import humpy_toolz

__all__ = ['merge_with', 'merge']

@humpy_toolz.curry
def merge_with(func, d, *dicts, **kwargs):
    return humpy_toolz.merge_with(func, d, *dicts, **kwargs)

@humpy_toolz.curry
def merge(d, *dicts, **kwargs):
    return humpy_toolz.merge(d, *dicts, **kwargs)
merge_with.__doc__ = humpy_toolz.merge_with.__doc__
merge.__doc__ = humpy_toolz.merge.__doc__
