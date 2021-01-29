# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis/
#
# Most of this work is copyright (C) 2013-2021 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.
#
# END HEADER

import pytest

from hypothesis import settings
from hypothesis.errors import Unsatisfiable
from hypothesis.strategies import lists

from tests.common import standard_types
from tests.common.debug import minimal
from tests.common.utils import flaky


@pytest.mark.parametrize("spec", standard_types, ids=list(map(repr, standard_types)))
@flaky(min_passes=1, max_runs=2)
def test_can_collectively_minimize(spec):
    """This should generally exercise strategies' strictly_simpler heuristic by
    putting us in a state where example cloning is required to get to the
    answer fast enough."""
    n = 10

    try:
        xs = minimal(
            lists(spec, min_size=n, max_size=n),
            lambda x: len(set(map(repr, x))) >= 2,
            settings(max_examples=2000),
        )
        assert len(xs) == n
        assert 2 <= len(set(map(repr, xs))) <= 3
    except Unsatisfiable:
        pass
