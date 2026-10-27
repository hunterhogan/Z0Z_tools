"""Supply shared pytest parameters for inclusive bounds and container membership.

(AI generated docstring)

Contents
--------
parametersAbsence
	Describe whether a value is absent from a container.
parametersAbsentFilter
	Select values absent from a container.
parametersBounds
	Describe whether a value lies within inclusive bounds.
parametersBoundsFilter
	Select values within inclusive bounds.
parametersMemberFilter
	Select values present in a container.
parametersMembership
	Describe whether a container contains a value.
"""

import pytest


parametersBounds = (
	pytest.param(5, 11, 3, False, id='below-floor'),
	pytest.param(5, 11, 5, True, id='at-floor'),
	pytest.param(5, 11, 7, True, id='within-bounds'),
	pytest.param(5, 11, 11, True, id='at-ceiling'),
	pytest.param(5, 11, 13, False, id='above-ceiling'),
	pytest.param(-11, -5, -7, True, id='negative-within-bounds'),
	pytest.param(-11, -5, -13, False, id='negative-below-floor'),
	pytest.param(-11, -5, -3, False, id='negative-above-ceiling'),
	pytest.param(7, 7, 7, True, id='equal-bounds-match'),
	pytest.param(7, 7, 5, False, id='equal-bounds-miss'),
	pytest.param(11, 5, 7, False, id='reversed-bounds'),
	pytest.param(2.5, 7.5, 5.5, True, id='fractional-within-bounds'),
	pytest.param('delta', 'lambda', 'gamma', True, id='text-within-bounds'),
	pytest.param('delta', 'lambda', 'omega', False, id='text-above-ceiling'),
)

parametersMembership = (
	pytest.param((5, 7, 11), 7, True, id='tuple-present'),
	pytest.param((5, 7, 11), 13, False, id='tuple-absent'),
	pytest.param((), 7, False, id='empty-tuple'),
	pytest.param(['delta', 'lambda'], 'lambda', True, id='list-present'),
	pytest.param(['delta', 'lambda'], 'omega', False, id='list-absent'),
	pytest.param({5, 7, 11}, 7, True, id='set-present'),
	pytest.param(frozenset((5, 7, 11)), 13, False, id='frozenset-absent'),
	pytest.param({'delta': 5, 'lambda': 7}, 'lambda', True, id='mapping-key'),
	pytest.param({'delta': 5, 'lambda': 7}, 7, False, id='mapping-value'),
	pytest.param('delta lambda', 'lambda', True, id='substring'),
	pytest.param('delta lambda', '', True, id='empty-substring'),
	pytest.param(range(5, 12, 2), 7, True, id='range-present'),
	pytest.param(range(5, 12, 2), 8, False, id='range-absent'),
	pytest.param((None, 7), None, True, id='none-present'),
)

parametersAbsence = (
	pytest.param((5, 7, 11), 7, False, id='tuple-present'),
	pytest.param((5, 7, 11), 13, True, id='tuple-absent'),
	pytest.param((), 7, True, id='empty-tuple'),
	pytest.param(['delta', 'lambda'], 'lambda', False, id='list-present'),
	pytest.param(['delta', 'lambda'], 'omega', True, id='list-absent'),
	pytest.param({5, 7, 11}, 7, False, id='set-present'),
	pytest.param(frozenset((5, 7, 11)), 13, True, id='frozenset-absent'),
	pytest.param({'delta': 5, 'lambda': 7}, 'lambda', False, id='mapping-key'),
	pytest.param({'delta': 5, 'lambda': 7}, 7, True, id='mapping-value'),
	pytest.param('delta lambda', 'lambda', False, id='substring'),
	pytest.param('delta lambda', '', False, id='empty-substring'),
	pytest.param(range(5, 12, 2), 7, False, id='range-present'),
	pytest.param(range(5, 12, 2), 8, True, id='range-absent'),
	pytest.param((None, 7), None, False, id='none-present'),
)

parametersBoundsFilter = (
	pytest.param(5, 11, (13, 5, 3, 11, 7, 5), (5, 11, 7, 5), id='bounds-order-and-repetition'),
	pytest.param(-11, -5, (-13, -11, -7, -5, -3), (-11, -7, -5), id='negative-bounds'),
	pytest.param(-5, 5, range(-7, 8), (-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5), id='retain-zero'),
	pytest.param(7, 7, (5, 7, 7, 11), (7, 7), id='equal-bounds'),
	pytest.param(11, 5, range(3, 14), (), id='reversed-bounds'),
	pytest.param(5, 11, (2, 3, 13, 17), (), id='no-matches'),
	pytest.param(5, 11, (), (), id='empty-input'),
	pytest.param(2.5, 7.5, [8.5, 7.5, 2.5, 5.5, 1.5], (7.5, 2.5, 5.5), id='fractional-bounds'),
	pytest.param('delta', 'lambda', ('omega', 'delta', 'gamma', 'lambda', 'beta'),
		('delta', 'gamma', 'lambda'), id='text-bounds'),
)

parametersMemberFilter = (
	pytest.param((5, 7, 11), (13, 7, 5, 7, 17, 11), (7, 5, 7, 11), id='order-and-repetition'),
	pytest.param([], (5, 7), (), id='empty-container'),
	pytest.param({'delta': 5, 'lambda': 7}, ('omega', 'lambda', 'delta', 'lambda'),
		('lambda', 'delta', 'lambda'), id='mapping-keys'),
	pytest.param({'delta': 5, 'lambda': 7}, (5, 'delta', 7, 'lambda'),
		('delta', 'lambda'), id='mapping-values-excluded'),
	pytest.param('delta lambda', ('lambda', 'omega', '', 'delta'),
		('lambda', '', 'delta'), id='substrings-retain-empty-text'),
	pytest.param(range(5, 12, 2), (11, 8, 7, 5, 13), (11, 7, 5), id='range'),
	pytest.param(frozenset((5, 7, 11)), [13, 7, 5, 7], (7, 5, 7), id='frozenset'),
	pytest.param((None, 7), (None, 5, 7, None), (None, 7, None), id='retain-none'),
	pytest.param({0, 7}, (5, 0, 7, 0, 11), (0, 7, 0), id='retain-zero'),
	pytest.param((5, 7, 11), (), (), id='empty-input'),
)

parametersAbsentFilter = (
	pytest.param((5, 7, 11), (13, 7, 5, 7, 17, 11), (13, 17), id='order-and-repetition'),
	pytest.param([], (5, 7), (5, 7), id='empty-container'),
	pytest.param({'delta': 5, 'lambda': 7}, ('omega', 'lambda', 'delta', 'lambda'),
		('omega',), id='mapping-keys'),
	pytest.param({'delta': 5, 'lambda': 7}, (5, 'delta', 7, 'lambda'),
		(5, 7), id='mapping-values-retained'),
	pytest.param('delta lambda', ('lambda', 'omega', '', 'delta'), ('omega',), id='substrings'),
	pytest.param(range(5, 12, 2), (11, 8, 7, 5, 13), (8, 13), id='range'),
	pytest.param(frozenset((5, 7, 11)), [13, 7, 5, 13], (13, 13), id='frozenset'),
	pytest.param((None, 7), (None, 5, 7, None), (5,), id='none-present'),
	pytest.param({5, 7}, (0, 5, 7, 0, 11), (0, 0, 11), id='retain-zero'),
	pytest.param((5, 7, 11), (), (), id='empty-input'),
)
