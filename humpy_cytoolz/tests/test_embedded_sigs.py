# from .dev_skip_test import dev_skip_test
# from humpy_cytoolz import curry, identity, keyfilter, merge_with, valfilter
# from types import BuiltinFunctionType, FunctionType
# import humpy_cytoolz
# import inspect

# @curry
# def isfrommod(modname, func):
#     mod = getattr(func, '__module__', '') or ''
#     return mod.startswith(modname) or 'toolz.functoolz.curry' in str(type(func))

# @dev_skip_test
# def test_class_sigs():
#     """ Test that all ``cdef class`` extension types in ``humpy_cytoolz`` have
#         correctly embedded the function signature as done in ``humpy_toolz``.
#     """
#     import humpy_toolz
#     toolz_dict = valfilter(isfrommod('humpy_toolz'), humpy_toolz.__dict__)
#     cytoolz_dict = valfilter(isfrommod('humpy_cytoolz'), humpy_cytoolz.__dict__)
#     cytoolz_dict = valfilter(lambda x: not isinstance(x, BuiltinFunctionType), cytoolz_dict)
#     toolz_dict = keyfilter(lambda x: x in cytoolz_dict, toolz_dict)
#     cytoolz_dict = keyfilter(lambda x: x in toolz_dict, cytoolz_dict)

#     class wrap:
#         """e.g., allow `factory=<class 'dict'>` to instead be `factory=dict` in signature"""

#         def __init__(self, obj):
#             self.obj = obj

#         def __repr__(self):
#             return getattr(self.obj, '__name__', repr(self.obj))
#     d = merge_with(identity, toolz_dict, cytoolz_dict)
#     for key, (toolz_func, cytoolz_func) in d.items():
#         if key in {'__getattr__'}:
#             continue
#         if isinstance(toolz_func, FunctionType):
#             toolz_spec = inspect.signature(toolz_func)
#         elif isinstance(toolz_func, humpy_toolz.curry):
#             toolz_spec = inspect.signature(toolz_func.func)
#         else:
#             toolz_spec = inspect.signature(toolz_func.__init__)
#         toolz_spec = toolz_spec.replace(parameters=[v.replace(default=wrap(v.default)) if v.default is not inspect._empty else v for v in toolz_spec.parameters.values()])
#         doc = cytoolz_func.__doc__
#         doc_alt = doc.replace('Py_ssize_t ', '').replace("=u'", "='")
#         toolz_sig = toolz_func.__name__ + str(toolz_spec)
#         if not (toolz_sig in doc or toolz_sig in doc_alt):
#             message = 'cytoolz.%s does not have correct function signature.\n\nExpected: %s\n\nDocstring in cytoolz is:\n%s' % (key, toolz_sig, cytoolz_func.__doc__)
#             assert False, message
# skip_sigs = ['identity']
# aliases = {'comp': 'compose'}

# @dev_skip_test
# def test_sig_at_beginning():
#     """ Test that the function signature is at the beginning of the docstring
#         and is followed by exactly one blank line.
#     """
#     cytoolz_dict = valfilter(isfrommod('humpy_cytoolz'), humpy_cytoolz.__dict__)
#     cytoolz_dict = keyfilter(lambda x: x not in skip_sigs, cytoolz_dict)
#     for key, val in cytoolz_dict.items():
#         if key in {'__getattr__'}:
#             continue
#         doclines = val.__doc__.splitlines()
#         assert len(doclines) > 2, f'cytoolz.{key} docstring too short:\n\n{val.__doc__}'
#         sig = '%s(' % aliases.get(key, key)
#         assert sig in doclines[0], 'cytoolz.%s docstring missing signature at beginning:\n\n%s' % (key, val.__doc__)
#         assert not doclines[1], 'cytoolz.%s docstring missing blank line after signature:\n\n%s' % (key, val.__doc__)
#         assert doclines[2], 'cytoolz.%s docstring too many blank lines after signature:\n\n%s' % (key, val.__doc__)
