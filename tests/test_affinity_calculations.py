import mock

import malaffinity

from . import const
from . import mocks
from . import vcr


@vcr.use_cassette("test-user.yaml")
def test_affinity__unrounded_with_dummy():
    """
    Test affinity with DUMMY_LIST
    """
    # Get the test list
    ma = malaffinity.MALAffinity(const.TEST_USERNAME, round=False)

    with mock.patch("malaffinity.endpoints.myanimelist") as MockClass:
        MockClass.return_value = mocks.mock_myanimelist_endpoint()

        affinity, shared = ma.calculate_affinity("DUMMY_USER")

        # Technically, we're supposed to test the *unrounded* affinity,
        # but because floating point shit is a thing, we'll just have
        # to make do with 10dp. It's not like anyone'll need
        # anything more accurate.
        assert round(affinity, 10) == round(const.AFFINITY_WITH_DUMMY, 10)
        assert shared == const.SHARED_WITH_DUMMY


@vcr.use_cassette("test-user.yaml")
def test_affinity__rounded_with_dummy():
    """
    Test affinity with DUMMY_LIST, but rounded
    """
    ma = malaffinity.MALAffinity(const.TEST_USERNAME, round=2)

    with mock.patch("malaffinity.endpoints.myanimelist") as MockClass:
        MockClass.return_value = mocks.mock_myanimelist_endpoint()

        affinity, shared = ma.calculate_affinity("DUMMY_USER")

        assert affinity == round(const.AFFINITY_WITH_DUMMY, 2)
        assert shared == const.SHARED_WITH_DUMMY


@mock.patch("malaffinity.endpoints.myanimelist")
def test_affinity__with_self(mock_class):
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
