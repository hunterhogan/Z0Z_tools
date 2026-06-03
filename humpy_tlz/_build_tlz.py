from importlib import import_module
from importlib.machinery import ModuleSpec
import humpy_toolz
import sys
import types

class TlzLoader:
    """ Finds and loads ``humpy_tlz`` modules when added to sys.meta_path"""

    def __init__(self):
        self.always_from_toolz = {humpy_toolz.pipe}

    def _load_toolz(self, fullname):
        rv = {}
        package, dot, submodules = fullname.partition('.')
        try:
            module_name = ''.join(['humpy_cytoolz', dot, submodules])
            rv['humpy_cytoolz'] = import_module(module_name)
        except ImportError:
            pass
        try:
            module_name = ''.join(['humpy_toolz', dot, submodules])
            rv['humpy_toolz'] = import_module(module_name)
        except ImportError:
            pass
        if not rv:
            raise ImportError(fullname)
        return rv

    def find_module(self, fullname, path=None):
        package, dot, submodules = fullname.partition('.')
        if package == 'humpy_tlz':
            return self

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        spec = ModuleSpec(fullname, self)
        module = self.create_module(spec)
        sys.modules[fullname] = module
        self.exec_module(module)
        return module

    def find_spec(self, fullname, path, target=None):
        package, dot, submodules = fullname.partition('.')
        if package == 'humpy_tlz':
            return ModuleSpec(fullname, self)

    def create_module(self, spec):
        return types.ModuleType(spec.name)

    def exec_module(self, module):
        toolz_mods = self._load_toolz(module.__name__)
        fast_mod = toolz_mods.get('humpy_cytoolz') or toolz_mods['humpy_toolz']
        slow_mod = toolz_mods.get('humpy_toolz') or toolz_mods['humpy_cytoolz']
        module.__dict__.update(humpy_toolz.merge(fast_mod.__dict__, module.__dict__))
        package = fast_mod.__package__
        if package is not None:
            package, dot, submodules = package.partition('.')
            module.__package__ = ''.join(['humpy_tlz', dot, submodules])
        if not module.__doc__:
            module.__doc__ = fast_mod.__doc__
        try:
            module.__file__ = slow_mod.__file__
        except AttributeError:
            pass
        for k, v in fast_mod.__dict__.items():
            tv = slow_mod.__dict__.get(k)
            try:
                hash(tv)
            except TypeError:
                tv = None
            if tv in self.always_from_toolz:
                module.__dict__[k] = tv
            elif isinstance(v, types.ModuleType) and v.__package__ == fast_mod.__name__:
                package, dot, submodules = v.__name__.partition('.')
                module_name = ''.join(['humpy_tlz', dot, submodules])
                submodule = import_module(module_name)
                module.__dict__[k] = submodule
tlz_loader = TlzLoader()
sys.meta_path.append(tlz_loader)
tlz_loader.exec_module(sys.modules['humpy_tlz'])
