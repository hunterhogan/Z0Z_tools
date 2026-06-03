import humpy_cytoolz

__all__ = ['merge', 'merge_with']

@humpy_cytoolz.curry
def merge(d, *dicts, **kwargs):
    return humpy_cytoolz.merge(d, *dicts, **kwargs)

@humpy_cytoolz.curry
def merge_with(func, d, *dicts, **kwargs):
    return humpy_cytoolz.merge_with(func, d, *dicts, **kwargs)
merge.__doc__ = humpy_cytoolz.merge.__doc__
merge_with.__doc__ = humpy_cytoolz.merge_with.__doc__
