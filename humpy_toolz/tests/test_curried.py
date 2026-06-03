from collections import defaultdict
from humpy_toolz.curried import first, merge, merge_with, operator as cop, reduce, second, sorted, take
from importlib import import_module
from operator import add
import humpy_toolz
import humpy_toolz.curried

def test_take() -> None:
    assert list(take(2)([1, 2, 3])) == [1, 2]

def test_first() -> None:
    assert first is humpy_toolz.itertoolz.first

def test_merge() -> None:
    assert merge(factory=lambda: defaultdict(int))({1: 1}) == {1: 1}
    assert merge({1: 1}) == {1: 1}
    assert merge({1: 1}, factory=lambda: defaultdict(int)) == {1: 1}

def test_merge_with() -> None:
    assert merge_with(sum)({1: 1}, {1: 2}) == {1: 3}

def test_merge_with_list() -> None:
    assert merge_with(sum, [{'a': 1}, {'a': 2}]) == {'a': 3}

def test_sorted() -> None:
    assert sorted(key=second)([(1, 2), (2, 1)]) == [(2, 1), (1, 2)]

def test_reduce() -> None:
    assert reduce(add)((1, 2, 3)) == 6

def test_module_name() -> None:
    assert humpy_toolz.curried.__name__ == 'humpy_toolz.curried'

def should_curry(func: object) -> bool:
    if not callable(func) or isinstance(func, humpy_toolz.curry):
        return False
    nargs = humpy_toolz.functoolz.num_required_args(func)
    if nargs is None or nargs > 1:
        return True
    return nargs == 1 and humpy_toolz.functoolz.has_keywords(func)

def test_curried_operator() -> None:
    import operator
    for k, v in vars(cop).items():
        if not callable(v):
            continue
        if not isinstance(v, humpy_toolz.curry):
            try:
                v(1)
            except TypeError:
                try:
                    v('x')
                except TypeError:
                    pass
                else:
                    continue
                raise AssertionError('humpy_toolz.curried.operator.%s is not curried!' % k)
        assert should_curry(getattr(operator, k)) == isinstance(v, humpy_toolz.curry), k
    assert len(set(vars(cop)) & {'add', 'sub', 'mul'}) == 3

def test_curried_namespace() -> None:
    exceptions = import_module('humpy_toolz.curried.exceptions')
    namespace = {}

    def curry_namespace(ns):
        return {name: humpy_toolz.curry(f) if should_curry(f) else f for name, f in ns.items() if '__' not in name}
    from_toolz = curry_namespace(vars(humpy_toolz))
    from_exceptions = curry_namespace(vars(exceptions))
    namespace.update(humpy_toolz.merge(from_toolz, from_exceptions))
    namespace = humpy_toolz.valfilter(callable, namespace)
    curried_namespace = humpy_toolz.valfilter(callable, humpy_toolz.curried.__dict__)
    if namespace != curried_namespace:
        missing = set(namespace) - set(curried_namespace)
        if missing:
            raise AssertionError('There are missing functions in humpy_toolz.curried:\n    %s' % '    \n'.join(sorted(missing)))
        extra = set(curried_namespace) - set(namespace)
        if extra:
            raise AssertionError('There are extra functions in humpy_toolz.curried:\n    %s' % '    \n'.join(sorted(extra)))
        unequal = humpy_toolz.merge_with(list, namespace, curried_namespace)
        unequal = humpy_toolz.valfilter(lambda x: x[0] != x[1], unequal)
        messages = []
        for name, (orig_func, auto_func) in sorted(unequal.items()):
            if name in from_exceptions:
                messages.append('%s should come from humpy_toolz.curried.exceptions' % name)
            elif should_curry(getattr(humpy_toolz, name)):
                messages.append('%s should be curried from humpy_toolz' % name)
            else:
                messages.append('%s should come from humpy_toolz and NOT be curried' % name)
        raise AssertionError('\n'.join(messages))
