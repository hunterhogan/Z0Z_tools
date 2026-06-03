from collections.abc import Callable, Iterable, Iterator
from functools import partial
from humpy_toolz.itertoolz import (
	accumulate, concat, concatv, cons, count, diff, drop, first, frequencies, get, getter, groupby, interleave, interpose, isdistinct,
	isiterable, iterate, join, last, mapcat, merge_sorted, nth, partition, partition_all, peek, peekn, pluck, random_sample, reduceby, remove,
	rest, second, sliding_window, tail, take, take_nth, topk, unique)
from humpy_toolz.utils import raises
from itertools import starmap
from operator import add, mul
from pickle import dumps, loads
from random import Random
from typing import Any, NoReturn
import itertools

no_default2 = loads(dumps('__no__default__'))

def identity(x: object) -> object:
    return x

def iseven(x: int) -> bool:
    return x % 2 == 0

def isodd(x: int) -> bool:
    return x % 2 == 1

def inc(x: int) -> int:
    return x + 1

def double(x: int) -> int:
    return 2 * x

def test_remove() -> None:
    r: Iterable[int] = remove(iseven, range(5))
    assert type(r) is not list
    assert list(r) == list(filter(isodd, range(5)))

def test_groupby() -> None:
    assert groupby(iseven, [1, 2, 3, 4]) == {True: [2, 4], False: [1, 3]}

def test_groupby_non_callable() -> None:
    assert groupby(0, [(1, 2), (1, 3), (2, 2), (2, 4)]) == {1: [(1, 2), (1, 3)], 2: [(2, 2), (2, 4)]}
    assert groupby([0], [(1, 2), (1, 3), (2, 2), (2, 4)]) == {(1,): [(1, 2), (1, 3)], (2,): [(2, 2), (2, 4)]}
    assert groupby([0, 0], [(1, 2), (1, 3), (2, 2), (2, 4)]) == {(1, 1): [(1, 2), (1, 3)], (2, 2): [(2, 2), (2, 4)]}

def test_merge_sorted() -> None:
    assert list(merge_sorted([1, 2, 3], [1, 2, 3])) == [1, 1, 2, 2, 3, 3]
    assert list(merge_sorted([1, 3, 5], [2, 4, 6])) == [1, 2, 3, 4, 5, 6]
    assert list(merge_sorted([1], [2, 4], [3], [])) == [1, 2, 3, 4]
    assert list(merge_sorted([5, 3, 1], [6, 4, 3], [], key=lambda x: -x)) == [6, 5, 4, 3, 3, 1]
    assert list(merge_sorted([2, 1, 3], [1, 2, 3], key=lambda x: x // 3)) == [2, 1, 1, 2, 3, 3]
    assert list(merge_sorted([2, 3], [1, 3], key=lambda x: x // 3)) == [2, 1, 3, 3]
    assert ''.join(merge_sorted('abc', 'abc', 'abc')) == 'aaabbbccc'
    assert ''.join(merge_sorted('abc', 'abc', 'abc', key=ord)) == 'aaabbbccc'
    assert ''.join(merge_sorted('cba', 'cba', 'cba', key=lambda x: -ord(x))) == 'cccbbbaaa'
    assert list(merge_sorted([1], [2, 3, 4], key=identity)) == [1, 2, 3, 4]
    data: list[list[tuple[int, int]]] = [[(1, 2), (0, 4), (3, 6)], [(5, 3), (6, 5), (8, 8)], [(9, 1), (9, 8), (9, 9)]]
    assert list(merge_sorted(*data, key=lambda x: x[1])) == [(9, 1), (1, 2), (5, 3), (0, 4), (6, 5), (3, 6), (8, 8), (9, 8), (9, 9)]
    assert list(merge_sorted()) == []
    assert list(merge_sorted([1, 2, 3])) == [1, 2, 3]
    assert list(merge_sorted([1, 4, 5], [2, 3])) == [1, 2, 3, 4, 5]
    assert list(merge_sorted([1, 4, 5], [2, 3], key=identity)) == [1, 2, 3, 4, 5]
    assert list(merge_sorted([1, 5], [2], [4, 7], [3, 6], key=identity)) == [1, 2, 3, 4, 5, 6, 7]

def test_interleave() -> None:
    assert ''.join(interleave(('ABC', '123'))) == 'A1B2C3'
    assert ''.join(interleave(('ABC', '1'))) == 'A1BC'

def test_unique() -> None:
    assert tuple(unique((1, 2, 3))) == (1, 2, 3)
    assert tuple(unique((1, 2, 1, 3))) == (1, 2, 3)
    assert tuple(unique((1, 2, 3), key=iseven)) == (1, 2)

def test_isiterable() -> None:

    class IterIterable:

        def __iter__(self) -> Iterator[str]:
            return iter(['a', 'b', 'c'])

    class GetItemIterable:

        def __getitem__(self, item: int) -> str:
            return ['a', 'b', 'c'][item]

    class NotIterable:
        __iter__ = None

    class NotIterableEvenWithGetItem:
        __iter__ = None

        def __getitem__(self, item: int) -> str:
            return ['a', 'b', 'c'][item]
    assert isiterable([1, 2, 3]) is True
    assert isiterable('abc') is True
    assert isiterable(IterIterable()) is True
    assert isiterable(GetItemIterable()) is True
    assert isiterable(5) is False
    assert isiterable(NotIterable()) is False
    assert isiterable(NotIterableEvenWithGetItem()) is False

def test_isdistinct() -> None:
    assert isdistinct([1, 2, 3]) is True
    assert isdistinct([1, 2, 1]) is False
    assert isdistinct('Hello') is False
    assert isdistinct('World') is True
    assert isdistinct(iter([1, 2, 3])) is True
    assert isdistinct(iter([1, 2, 1])) is False

def test_nth() -> None:
    assert nth(2, 'ABCDE') == 'C'
    assert nth(2, iter('ABCDE')) == 'C'
    assert nth(1, (3, 2, 1)) == 2
    assert nth(0, {'foo': 'bar'}) == 'foo'
    assert raises(StopIteration, lambda: nth(10, {10: 'foo'}))
    assert nth(-2, 'ABCDE') == 'D'
    assert raises(ValueError, lambda: nth(-2, iter('ABCDE')))

def test_first() -> None:
    assert first('ABCDE') == 'A'
    assert first((3, 2, 1)) == 3
    assert isinstance(first({0: 'zero', 1: 'one'}), int)

def test_second() -> None:
    assert second('ABCDE') == 'B'
    assert second((3, 2, 1)) == 2
    assert isinstance(second({0: 'zero', 1: 'one'}), int)

def test_last() -> None:
    assert last('ABCDE') == 'E'
    assert last((3, 2, 1)) == 1
    assert isinstance(last({0: 'zero', 1: 'one'}), int)

def test_rest() -> None:
    assert list(rest('ABCDE')) == list('BCDE')
    assert list(rest((3, 2, 1))) == list((2, 1))

def test_take() -> None:
    assert list(take(3, 'ABCDE')) == list('ABC')
    assert list(take(2, (3, 2, 1))) == list((3, 2))

def test_tail() -> None:
    assert list(tail(3, 'ABCDE')) == list('CDE')
    assert list(tail(3, iter('ABCDE'))) == list('CDE')
    assert list(tail(2, (3, 2, 1))) == list((2, 1))

def test_drop() -> None:
    assert list(drop(3, 'ABCDE')) == list('DE')
    assert list(drop(1, (3, 2, 1))) == list((2, 1))

def test_take_nth() -> None:
    assert list(take_nth(2, 'ABCDE')) == list('ACE')

def test_get() -> None:
    assert get(1, 'ABCDE') == 'B'
    assert list(get([1, 3], 'ABCDE')) == list('BD')
    assert get('a', {'a': 1, 'b': 2, 'c': 3}) == 1
    assert get(['a', 'b'], {'a': 1, 'b': 2, 'c': 3}) == (1, 2)
    assert get('foo', {}, default='bar') == 'bar'
    assert get({}, [1, 2, 3], default='bar') == 'bar'
    assert get([0, 2], 'AB', 'C') == ('A', 'C')
    assert get([0], 'AB') == ('A',)
    assert get([], 'AB') == ()
    assert raises(IndexError, lambda: get(10, 'ABC'))
    assert raises(KeyError, lambda: get(10, {'a': 1}))
    assert raises(TypeError, lambda: get({}, [1, 2, 3]))
    assert raises(TypeError, lambda: get([1, 2, 3], 1, None))
    assert raises(KeyError, lambda: get('foo', {}, default=no_default2))

def test_mapcat() -> None:
    assert list(mapcat(identity, [[1, 2, 3], [4, 5, 6]])) == [1, 2, 3, 4, 5, 6]
    assert list(mapcat(reversed, [[3, 2, 1, 0], [6, 5, 4], [9, 8, 7]])) == list(range(10))
    inc = lambda i: i + 1
    assert [4, 5, 6, 7, 8, 9] == list(mapcat(partial(map, inc), [[3, 4, 5], [6, 7, 8]]))

def test_cons() -> None:
    assert list(cons(1, [2, 3])) == [1, 2, 3]

def test_concat() -> None:
    assert list(concat([[], [], []])) == []
    assert list(take(5, concat([['a', 'b'], range(1000000000)]))) == ['a', 'b', 0, 1, 2]

def test_concatv() -> None:
    assert list(concatv([], [], [])) == []
    assert list(take(5, concatv(['a', 'b'], range(1000000000)))) == ['a', 'b', 0, 1, 2]

def test_interpose() -> None:
    assert 'a' == first(rest(interpose('a', range(1000000000))))
    assert 'tXaXrXzXaXn' == ''.join(interpose('X', 'tarzan'))
    assert list(interpose(0, itertools.repeat(1, 4))) == [1, 0, 1, 0, 1, 0, 1]
    assert list(interpose('.', ['a', 'b', 'c'])) == ['a', '.', 'b', '.', 'c']

def test_frequencies() -> None:
    assert frequencies(['cat', 'pig', 'cat', 'eel', 'pig', 'dog', 'dog', 'dog']) == {'cat': 2, 'eel': 1, 'pig': 2, 'dog': 3}
    assert frequencies([]) == {}
    assert frequencies('onomatopoeia') == {'a': 2, 'e': 1, 'i': 1, 'm': 1, 'o': 4, 'n': 1, 'p': 1, 't': 1}

def test_reduceby() -> None:
    data: list[int] = [1, 2, 3, 4, 5]
    iseven = lambda x: x % 2 == 0
    assert reduceby(iseven, add, data, 0) == {False: 9, True: 6}
    assert reduceby(iseven, mul, data, 1) == {False: 15, True: 8}
    projects = [{'name': 'build roads', 'state': 'CA', 'cost': 1000000}, {'name': 'fight crime', 'state': 'IL', 'cost': 100000}, {'name': 'help farmers', 'state': 'IL', 'cost': 2000000}, {'name': 'help farmers', 'state': 'CA', 'cost': 200000}]
    assert reduceby(lambda x: x['state'], lambda acc, x: acc + x['cost'], projects, 0) == {'CA': 1200000, 'IL': 2100000}
    assert reduceby('state', lambda acc, x: acc + x['cost'], projects, 0) == {'CA': 1200000, 'IL': 2100000}

def test_reduce_by_init() -> None:
    assert reduceby(iseven, add, [1, 2, 3, 4]) == {True: 2 + 4, False: 1 + 3}
    assert reduceby(iseven, add, [1, 2, 3, 4], no_default2) == {True: 2 + 4, False: 1 + 3}

def test_reduce_by_callable_default() -> None:

    def set_add(s: set[int], i: int) -> set[int]:
        s.add(i)
        return s
    assert reduceby(iseven, set_add, [1, 2, 3, 4, 1, 2], set) == {True: {2, 4}, False: {1, 3}}

def test_iterate() -> None:
    assert list(itertools.islice(iterate(inc, 0), 0, 5)) == [0, 1, 2, 3, 4]
    assert list(take(4, iterate(double, 1))) == [1, 2, 4, 8]

def test_accumulate() -> None:
    assert list(accumulate(add, [1, 2, 3, 4, 5])) == [1, 3, 6, 10, 15]
    assert list(accumulate(mul, [1, 2, 3, 4, 5])) == [1, 2, 6, 24, 120]
    assert list(accumulate(add, [1, 2, 3, 4, 5], -1)) == [-1, 0, 2, 5, 9, 14]

    def binop(a: object, b: object) -> NoReturn:
        raise AssertionError('binop should not be called')
    start: object = object()
    assert list(accumulate(binop, [], start)) == [start]
    assert list(accumulate(binop, [])) == []
    assert list(accumulate(add, [1, 2, 3], no_default2)) == [1, 3, 6]

def test_accumulate_works_on_consumable_iterables() -> None:
    assert list(accumulate(add, iter((1, 2, 3)))) == [1, 3, 6]

def test_sliding_window() -> None:
    assert list(sliding_window(2, [1, 2, 3, 4])) == [(1, 2), (2, 3), (3, 4)]
    assert list(sliding_window(3, [1, 2, 3, 4])) == [(1, 2, 3), (2, 3, 4)]

def test_sliding_window_of_short_iterator() -> None:
    assert list(sliding_window(3, [1, 2])) == []
    assert list(sliding_window(7, [1, 2])) == []

def test_partition() -> None:
    assert list(partition(2, [1, 2, 3, 4])) == [(1, 2), (3, 4)]
    assert list(partition(3, range(7))) == [(0, 1, 2), (3, 4, 5)]
    assert list(partition(3, range(4), pad=-1)) == [(0, 1, 2), (3, -1, -1)]
    assert list(partition(2, [])) == []

def test_partition_all() -> None:
    assert list(partition_all(2, [1, 2, 3, 4])) == [(1, 2), (3, 4)]
    assert list(partition_all(3, range(5))) == [(0, 1, 2), (3, 4)]
    assert list(partition_all(2, [])) == []

    class NoCompare:

        def __eq__(self, other: object) -> bool:
            if self.__class__ == other.__class__:
                return True
            raise ValueError
    obj: NoCompare = NoCompare()
    result: list[tuple[NoCompare, ...]] = [(obj, obj, obj, obj), (obj, obj, obj)]
    assert list(partition_all(4, [obj] * 7)) == result
    assert list(partition_all(4, iter([obj] * 7))) == result

    class ListWithBadLength(list):

        def __init__(self, contents: list[int], off_by: int = 1) -> None:
            self.off_by = off_by
            super().__init__(contents)

        def __len__(self) -> int:
            return super().__len__() + self.off_by
    too_long_list: ListWithBadLength = ListWithBadLength([1, 2], off_by=+1)
    assert raises(LookupError, lambda: list(partition_all(5, too_long_list)))
    too_short_list: ListWithBadLength = ListWithBadLength([1, 2], off_by=-1)
    assert raises(LookupError, lambda: list(partition_all(5, too_short_list)))

def test_count() -> None:
    assert count((1, 2, 3)) == 3
    assert count([]) == 0
    assert count(iter((1, 2, 3, 4))) == 4
    assert count('hello') == 5
    assert count(iter('hello')) == 5

def test_pluck() -> None:
    assert list(pluck(0, [[0, 1], [2, 3], [4, 5]])) == [0, 2, 4]
    assert list(pluck([0, 1], [[0, 1, 2], [3, 4, 5]])) == [(0, 1), (3, 4)]
    assert list(pluck(1, [[0], [0, 1]], None)) == [None, 1]
    data = [{'id': 1, 'name': 'cheese'}, {'id': 2, 'name': 'pies', 'price': 1}]
    assert list(pluck('id', data)) == [1, 2]
    assert list(pluck('price', data, 0)) == [0, 1]
    assert list(pluck(['id', 'name'], data)) == [(1, 'cheese'), (2, 'pies')]
    assert list(pluck(['name'], data)) == [('cheese',), ('pies',)]
    assert list(pluck(['price', 'other'], data, 0)) == [(0, 0), (1, 0)]
    assert raises(IndexError, lambda: list(pluck(1, [[0]])))
    assert raises(KeyError, lambda: list(pluck('name', [{'id': 1}])))
    assert list(pluck(0, [[0, 1], [2, 3], [4, 5]], no_default2)) == [0, 2, 4]
    assert raises(IndexError, lambda: list(pluck(1, [[0]], no_default2)))

def test_join() -> None:
    names: list[tuple[int, str]] = [(1, 'one'), (2, 'two'), (3, 'three')]
    fruit: list[tuple[str, int]] = [('apple', 1), ('orange', 1), ('banana', 2), ('coconut', 2)]

    def addpair(pair: tuple[Any, Any]) -> Any:
        return pair[0] + pair[1]
    result: set[tuple[int, str, str, int]] = set(starmap(add, join(first, names, second, fruit)))
    expected: set[tuple[int, str, str, int]] = {(1, 'one', 'apple', 1), (1, 'one', 'orange', 1), (2, 'two', 'banana', 2), (2, 'two', 'coconut', 2)}
    assert result == expected
    result = set(starmap(add, join(first, names, second, fruit, left_default=no_default2, right_default=no_default2)))
    assert result == expected

def test_getter() -> None:
    assert getter(0)('Alice') == 'A'
    assert getter([0])('Alice') == ('A',)
    assert getter([])('Alice') == ()

def test_key_as_getter() -> None:
    squares: list[tuple[int, int]] = [(i, i ** 2) for i in range(5)]
    pows: list[tuple[int, int, int]] = [(i, i ** 2, i ** 3) for i in range(5)]
    assert set(join(0, squares, 0, pows)) == set(join(lambda x: x[0], squares, lambda x: x[0], pows))
    get = lambda x: (x[0], x[1])
    assert set(join([0, 1], squares, [0, 1], pows)) == set(join(get, squares, get, pows))
    get = lambda x: (x[0],)
    assert set(join([0], squares, [0], pows)) == set(join(get, squares, get, pows))

def test_join_double_repeats() -> None:
    names: list[tuple[int, str]] = [(1, 'one'), (2, 'two'), (3, 'three'), (1, 'uno'), (2, 'dos')]
    fruit: list[tuple[str, int]] = [('apple', 1), ('orange', 1), ('banana', 2), ('coconut', 2)]
    result: set[tuple[int, str, str, int]] = set(starmap(add, join(first, names, second, fruit)))
    expected: set[tuple[int, str, str, int]] = {(1, 'one', 'apple', 1), (1, 'one', 'orange', 1), (2, 'two', 'banana', 2), (2, 'two', 'coconut', 2), (1, 'uno', 'apple', 1), (1, 'uno', 'orange', 1), (2, 'dos', 'banana', 2), (2, 'dos', 'coconut', 2)}
    assert result == expected

def test_join_missing_element() -> None:
    names: list[tuple[int, str]] = [(1, 'one'), (2, 'two'), (3, 'three')]
    fruit: list[tuple[str, int]] = [('apple', 5), ('orange', 1)]
    result: set[tuple[int, str, str, int]] = set(starmap(add, join(first, names, second, fruit)))
    expected: set[tuple[int, str, str, int]] = {(1, 'one', 'orange', 1)}
    assert result == expected

def test_left_outer_join() -> None:
    result: set[tuple[int | None, int | None]] = set(join(identity, [1, 2], identity, [2, 3], left_default=None))
    expected: set[tuple[int | None, int | None]] = {(2, 2), (None, 3)}
    assert result == expected

def test_right_outer_join() -> None:
    result: set[tuple[int | None, int | None]] = set(join(identity, [1, 2], identity, [2, 3], right_default=None))
    expected: set[tuple[int | None, int | None]] = {(2, 2), (1, None)}
    assert result == expected

def test_outer_join() -> None:
    result: set[tuple[int | None, int | None]] = set(join(identity, [1, 2], identity, [2, 3], left_default=None, right_default=None))
    expected: set[tuple[int | None, int | None]] = {(2, 2), (1, None), (None, 3)}
    assert result == expected

def test_diff() -> None:
    assert raises(TypeError, lambda: list(diff()))
    assert raises(TypeError, lambda: list(diff([1, 2])))
    assert raises(TypeError, lambda: list(diff([1, 2], 3)))
    assert list(diff([1, 2], (1, 2), iter([1, 2]))) == []
    assert list(diff([1, 2, 3], (1, 10, 3), iter([1, 2, 10]))) == [(2, 10, 2), (3, 3, 10)]
    assert list(diff([1, 2], [10])) == [(1, 10)]
    assert list(diff([1, 2], [10], default=None)) == [(1, 10), (2, None)]
    assert raises(TypeError, lambda: list(diff([])))
    assert raises(TypeError, lambda: list(diff([[]])))
    assert raises(TypeError, lambda: list(diff([[1, 2]])))
    assert raises(TypeError, lambda: list(diff([[1, 2], 3])))
    assert list(diff([(1, 2), (1, 3)])) == [(2, 3)]
    data1: list[dict[str, int | str]] = [{'cost': 1, 'currency': 'dollar'}, {'cost': 2, 'currency': 'dollar'}]
    data2: list[dict[str, int | str]] = [{'cost': 100, 'currency': 'yen'}, {'cost': 300, 'currency': 'yen'}]
    conversions: dict[str, float] = {'dollar': 1, 'yen': 0.01}

    def indollars(item: dict[str, int | str]) -> int | float:
        return conversions[item['currency']] * item['cost']
    list(diff(data1, data2, key=indollars)) == [({'cost': 2, 'currency': 'dollar'}, {'cost': 300, 'currency': 'yen'})]

def test_topk() -> None:
    assert topk(2, [4, 1, 5, 2]) == (5, 4)
    assert topk(2, [4, 1, 5, 2], key=lambda x: -x) == (1, 2)
    assert topk(2, iter([5, 1, 4, 2]), key=lambda x: -x) == (1, 2)
    assert topk(2, [{'a': 1, 'b': 10}, {'a': 2, 'b': 9}, {'a': 10, 'b': 1}, {'a': 9, 'b': 2}], key='a') == ({'a': 10, 'b': 1}, {'a': 9, 'b': 2})
    assert topk(2, [{'a': 1, 'b': 10}, {'a': 2, 'b': 9}, {'a': 10, 'b': 1}, {'a': 9, 'b': 2}], key='b') == ({'a': 1, 'b': 10}, {'a': 2, 'b': 9})
    assert topk(2, [(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)], 0) == ((4, 0), (3, 1))

def test_topk_is_stable() -> None:
    assert topk(4, [5, 9, 2, 1, 5, 3], key=lambda x: 1) == (5, 9, 2, 1)

def test_peek() -> None:
    alist: list[str] = ['Alice', 'Bob', 'Carol']
    element, blist = peek(alist)
    assert element == alist[0]
    assert list(blist) == alist
    assert raises(StopIteration, lambda: peek([]))

def test_peekn() -> None:
    alist: tuple[str, str, str] = ('Alice', 'Bob', 'Carol')
    elements, blist = peekn(2, alist)
    assert elements == alist[:2]
    assert tuple(blist) == alist
    elements, blist = peekn(len(alist) * 4, alist)
    assert elements == alist
    assert tuple(blist) == alist

def test_random_sample() -> None:
    alist: list[int] = list(range(100))
    assert list(random_sample(prob=1, seq=alist, random_state=2016)) == alist
    mk_rsample: Callable[..., list[int]] = lambda rs=1: list(random_sample(prob=0.1, seq=alist, random_state=rs))
    rsample1: list[int] = mk_rsample()
    assert rsample1 == mk_rsample()
    rsample2: list[int] = mk_rsample(1984)
    randobj: Random = Random(1984)
    assert rsample2 == mk_rsample(randobj)
    assert rsample1 != rsample2
    assert mk_rsample(hash(object)) == mk_rsample(hash(object))
    assert mk_rsample(hash(object)) != mk_rsample(hash(object()))
    assert mk_rsample(b'a') == mk_rsample('a')
    assert raises(TypeError, lambda: mk_rsample([]))
