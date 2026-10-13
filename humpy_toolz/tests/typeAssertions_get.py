from __future__ import annotations

from collections.abc import Sequence
from humpy_toolz.itertoolz import get
from humpy_toolz.utils import no_default
from typing import assert_type, TYPE_CHECKING

if TYPE_CHECKING:
	from collections.abc import Mapping
	from optype import CanGetitem

def checkGetAnnotations(
	seq: Sequence[int], mapping: Mapping[str, int], tupleKeys: Mapping[tuple[int, int], str], structural: CanGetitem[int, str]
) -> None:
	assert_type(get(2, seq), int)
	assert_type(get([2, 3], seq), tuple[int, ...])
	assert_type(get([2], seq), tuple[int, ...])
	assert_type(get([], seq), tuple[int, ...])
	assert_type(get(2, seq, None), int | None)
	assert_type(get([2, 3], seq, None), tuple[int | None, ...])
	assert_type(get(2, seq, 'missing'), int | str)
	assert_type(get([2, 3], seq, 'missing'), tuple[int | str, ...])
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
