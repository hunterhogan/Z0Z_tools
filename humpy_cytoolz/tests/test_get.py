from __future__ import annotations

from humpy_cytoolz.itertoolz import get
from humpy_cytoolz.utils import no_default
from typing import TYPE_CHECKING
import pytest

if TYPE_CHECKING:
	from optype import CanGetitem


@pytest.mark.parametrize(
	'ind, seq, default, expected',
	(
		pytest.param(2, (3, 5, 7, 11), no_default, 7, id='scalar-index'),
		pytest.param([2, 3], (3, 5, 7, 11), no_default, (7, 11), id='multiple-indices'),
		pytest.param([2], (3, 5, 7, 11), no_default, (7,), id='single-index-list'),
		pytest.param([], (3, 5, 7, 11), no_default, (), id='empty-indices'),
		pytest.param([], 13, no_default, (), id='empty-indices-without-indexable-container'),
		pytest.param([2, 7], (3, 5, 7, 11), None, (7, None), id='missing-index-default'),
		pytest.param(7, (3, 5, 7, 11), 'missing', 'missing', id='scalar-default-different-type'),
		pytest.param('Norway', {'Norway': 13, 'Kenya': 17}, None, 13, id='string-key-is-scalar'),
		pytest.param(['Norway', 'Kenya'], {'Norway': 13, 'Kenya': 17}, no_default, (13, 17), id='multiple-string-keys'),
		pytest.param(['Norway', 'Kenya'], {'Norway': 13}, None, (13, None), id='missing-key-default'),
		pytest.param((2, 3), {(2, 3): 17}, no_default, 17, id='tuple-key-is-scalar'),
		pytest.param([(2, 3)], {(2, 3): 17}, no_default, (17,), id='list-of-tuple-keys'),
		pytest.param((2, 3), 'Norway', None, None, id='tuple-does-not-request-multiple-indices'),
		pytest.param(b'\x02\x03', (3, 5, 7, 11), None, None, id='bytes-do-not-request-multiple-indices'),
		pytest.param(dict[str, int](), (3, 5, 7, 11), None, None, id='invalid-scalar-index-default'),
		pytest.param(slice(2, 4), (3, 5, 7, 11), no_default, (7, 11), id='slice-is-scalar'),
	),
)
def test_get[Key, Value, ValueDefault](
	ind: Key | list[Key],
	seq: CanGetitem[Key, Value],
	default: ValueDefault,
	expected: Value | ValueDefault | tuple[Value | ValueDefault, ...],
) -> None:
	actual: Value | ValueDefault | tuple[Value | ValueDefault, ...] = get(ind, seq, default)
	message: str = f'I received `actual = {actual!r}` from `get` with `ind = {ind!r}`, `seq = {seq!r}`, and `default = {default!r}`; I expected `expected = {expected!r}`.'
	assert actual == expected, message


@pytest.mark.parametrize(
	'ind, seq, default, expected',
	(
		pytest.param(7, (3, 5, 7, 11), no_default, IndexError, id='missing-scalar-index'),
		pytest.param([2, 7], (3, 5, 7, 11), no_default, IndexError, id='missing-list-index'),
		pytest.param('Kenya', {'Norway': 13}, no_default, KeyError, id='missing-scalar-key'),
		pytest.param(['Norway', 'Kenya'], {'Norway': 13}, no_default, KeyError, id='missing-list-key'),
		pytest.param((2, 3), 'Norway', no_default, TypeError, id='tuple-is-not-a-multiple-index-request'),
		pytest.param(dict[str, int](), (3, 5, 7, 11), no_default, TypeError, id='invalid-scalar-index'),
		pytest.param([dict[str, int]()], {'Norway': 13}, None, TypeError, id='invalid-list-key-does-not-use-default'),
		pytest.param([2], 13, None, TypeError, id='non-indexable-container'),
	),
)
def test_getError[Key, Value, ValueDefault](
	ind: Key | list[Key], seq: CanGetitem[Key, Value], default: ValueDefault, expected: type[Exception]
) -> None:
	with pytest.raises(expected):
		get(ind, seq, default)
