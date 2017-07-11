import time

import malaffinity

from . import const
from . import mocks
from .mocks import hook_mock_endpoint_and_run_function


def test_unrounded_affinity_with_dummy():
    """
    Test affinity with DUMMY_LIST
    """

    time.sleep(5)

    # Get the test list
    ma = malaffinity.MALAffinity(const.TEST_USERNAME, round=False)

    def funct():
        affinity, shared = ma.calculate_affinity("DUMMY_USER")

        assert affinity == const.AFFINITY_WITH_DUMMY
        assert shared == const.SHARED_WITH_DUMMY

    hook_mock_endpoint_and_run_function(funct, mocks.mock_myanimelist_endpoint)


def test_rounded_affinity_with_dummy():
    """
    Test affinity with DUMMY_LIST, but rounded
    """

    time.sleep(5)

    ma = malaffinity.MALAffinity(const.TEST_USERNAME, round=2)

    def funct():
        affinity, shared = ma.calculate_affinity("DUMMY_USER")

        assert affinity == round(const.AFFINITY_WITH_DUMMY, 2)
        assert shared == const.SHARED_WITH_DUMMY

    hook_mock_endpoint_and_run_function(funct, mocks.mock_myanimelist_endpoint)


def test_affinity_with_self():
    """
    Test affinity with self, by calling `malaffinity.calculate_affinity`
    with the same username twice. Simulate this with a dummy
    to avoid repeated MAL requests
    """

    def funct():
        affinity, shared = \
            malaffinity.calculate_affinity("DUMMY_USER", "DUMMY_USER")

        assert affinity == 100.0
        assert shared == len(mocks.DUMMY_LIST)

    hook_mock_endpoint_and_run_function(funct, mocks.mock_myanimelist_endpoint)
