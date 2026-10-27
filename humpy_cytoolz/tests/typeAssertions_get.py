from __future__ import annotations

from collections.abc import Iterator, Sequence
from humpy_cytoolz.itertoolz import get, getter, pluck
from humpy_cytoolz.utils import no_default
from typing import assert_type, TYPE_CHECKING

if TYPE_CHECKING:
	from collections.abc import Mapping
	from optype import CanGetitem


def checkGetAnnotations(
	seq: Sequence[int], mapping: Mapping[str, int], tupleKeys: Mapping[tuple[int, int], str], structural: CanGetitem[int, str],
	default: str = 'missing'
) -> None:
	assert_type(get(2, seq), int)
	assert_type(get([2, 3], seq), tuple[int, ...])
	assert_type(get([2], seq), tuple[int, ...])
	assert_type(get(list[int](), seq), tuple[int, ...])
	assert_type(get(2, seq, None), int | None)
	assert_type(get([2, 3], seq, None), tuple[int | None, ...])
	assert_type(get(2, seq, default), int | str)
	assert_type(get([2, 3], seq, default), tuple[int | str, ...])
	assert_type(get('Norway', mapping), int)
	assert_type(get(['Norway', 'Kenya'], mapping), tuple[int, ...])
	assert_type(get(['Norway', 'Kenya'], mapping, None), tuple[int | None, ...])
	assert_type(get((2, 3), tupleKeys), str)
	assert_type(get([(2, 3)], tupleKeys), tuple[str, ...])
	assert_type(get(slice(2, 3), seq), Sequence[int])
	assert_type(get(2, structural), str)
	assert_type(get([2, 3], structural, None), tuple[str | None, ...])
	assert_type(get(2, seq, no_default), int)
	assert_type(get([2, 3], seq, no_default), tuple[int, ...])
	assert_type(getter(2)(seq), int)
	assert_type(getter([2, 3])(seq), tuple[int, ...])
	assert_type(getter('Norway')(mapping), int)
	assert_type(pluck(2, [seq]), Iterator[int])
	assert_type(pluck([2, 3], [seq]), Iterator[tuple[int, ...]])
	assert_type(pluck(2, [seq], None), Iterator[int | None])
	assert_type(pluck([2, 3], [seq], None), Iterator[tuple[int | None, ...]])
	assert_type(pluck((2, 3), [tupleKeys]), Iterator[str])
	assert_type(pluck(2, [structural]), Iterator[str])
