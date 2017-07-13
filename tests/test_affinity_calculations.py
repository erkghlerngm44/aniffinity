import time

import mock

import malaffinity

from . import const
from . import mocks


def test_unrounded_affinity_with_dummy():
    """
    Test affinity with DUMMY_LIST
    """

    time.sleep(5)

    # Get the test list
    ma = malaffinity.MALAffinity(const.TEST_USERNAME, round=False)

    with mock.patch("malaffinity.endpoints.myanimelist") as MockClass:
        MockClass.return_value = mocks.mock_myanimelist_endpoint()

        affinity, shared = ma.calculate_affinity("DUMMY_USER")

        assert affinity == const.AFFINITY_WITH_DUMMY
        assert shared == const.SHARED_WITH_DUMMY


def test_rounded_affinity_with_dummy():
    """
    Test affinity with DUMMY_LIST, but rounded
    """

    time.sleep(5)

    ma = malaffinity.MALAffinity(const.TEST_USERNAME, round=2)

    with mock.patch("malaffinity.endpoints.myanimelist") as MockClass:
        MockClass.return_value = mocks.mock_myanimelist_endpoint()

        affinity, shared = ma.calculate_affinity("DUMMY_USER")

        assert affinity == round(const.AFFINITY_WITH_DUMMY, 2)
        assert shared == const.SHARED_WITH_DUMMY


@mock.patch("malaffinity.endpoints.myanimelist")
def test_affinity_with_self(mock_class):
    """
    Test affinity with self, by calling `malaffinity.calculate_affinity`
    with the same username twice. Simulate this with a dummy
    to avoid repeated MAL requests
    """

    mock_class.return_value = mocks.mock_myanimelist_endpoint()

    affinity, shared = \
        malaffinity.calculate_affinity("DUMMY_USER", "DUMMY_USER")

    assert affinity == 100.0
    assert shared == len(mocks.DUMMY_LIST)
