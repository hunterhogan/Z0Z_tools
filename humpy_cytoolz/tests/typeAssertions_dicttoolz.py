from __future__ import annotations

from collections import UserDict
from collections.abc import Mapping, MutableMapping
from humpy_cytoolz.dicttoolz import get_in, merge, merge_with
from typing import assert_type, TypedDict

class Metadata(TypedDict):
    description: str
    offset: int
    valuesKnown: dict[int, int]

def checkMergeAnnotations(dicts: tuple[Mapping[int, int], Mapping[int, int]]) -> None:
    assert_type(merge(*dicts), dict[int, int])
    assert_type(merge(dicts), dict[int, int])
    assert_type(merge(iter(dicts)), dict[int, int])
    assert_type(merge(dicts, factory=dict[int, int]), dict[int, int])
    assert_type(merge(*dicts, factory=UserDict[int, int]), MutableMapping[int, int])
    assert_type(merge(dicts, factory=UserDict[int, int]), MutableMapping[int, int])

def checkMergeWithAnnotations(dicts: tuple[Mapping[int, int], Mapping[int, int]], nested: Mapping[int, Mapping[int, int]]) -> None:
    assert_type(merge_with(tuple, *dicts), dict[int, tuple[int, ...]])
    assert_type(merge_with(tuple, dicts), dict[int, tuple[int, ...]])
    assert_type(merge_with(tuple, iter(dicts)), dict[int, tuple[int, ...]])
    assert_type(merge_with(list[int].copy, *dicts), dict[int, list[int]])
    assert_type(merge_with(tuple, dicts, factory=dict[int, tuple[int, ...]]), dict[int, tuple[int, ...]])
    assert_type(merge_with(tuple, *dicts, factory=UserDict[int, tuple[int, ...]]), MutableMapping[int, tuple[int, ...]])
    assert_type(merge_with(tuple, dicts, factory=UserDict[int, tuple[int, ...]]), MutableMapping[int, tuple[int, ...]])
    assert_type(merge_with(merge, nested, nested), dict[int, dict[int, int]])
    assert_type(merge_with(merge, (nested, nested)), dict[int, dict[int, int]])

def checkGetInAnnotations(metadata: Mapping[str, Metadata], default: dict[int, int]) -> None:
    assert_type(get_in(('A123456',), metadata, dict[str, dict[int, int]]()).get('valuesKnown', default), dict[int, int])
    assert_type(get_in(('A123456',), metadata), Metadata | None)
    assert_type(get_in((), metadata), Mapping[str, Metadata])
    assert_type(get_in(('A123456',), metadata, no_default=True), Metadata)
    assert_type(get_in(('A123456',), metadata, default, no_default=True), Metadata)
    assert_type(get_in(('A123456',), metadata, default, True), Metadata)
