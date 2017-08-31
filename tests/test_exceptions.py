import mock
import pytest

import malaffinity

from . import const
from . import mocks
from . import vcr


exceptions = malaffinity.exceptions


def test_exception__calculate_affinity_without_init():
    """
    Test if `Exception` gets raised when calculating
    affinity without `init`ing
    """
    ma = malaffinity.MALAffinity()

    # TODO: Change if custom exception made for this
    with pytest.raises(Exception) as excinfo:
        ma.calculate_affinity("DUMMY_USER")

    assert "no base user has been specified" in str(excinfo.value).lower()


@vcr.use_cassette("test-invalid-user.yaml")
def test_exception__invalid_username():
    """
    Test if `InvalidUsernameError` gets raised if passing
    an invalid username
    """
    with pytest.raises(exceptions.InvalidUsernameError):
        malaffinity.MALAffinity("ALDDJFfnjegenfmekfmejfefep9re9444")


def test_exception__not_enough_shared():
    """
    Test if `NoAffinityError` gets raised if shared rated
    anime count is below threshold
    """
    ma = malaffinity.MALAffinity()

    # Enough MAL requests, we don't want them killing us
    ma._base_user = "DUMMY_USER"
    ma._base_scores = mocks.dummy_list_to_base_scores()

    with mock.patch("malaffinity.endpoints.myanimelist") as MockClass:
        MockClass.return_value = mocks.mock_mini_myanimelist_endpoint()

        with pytest.raises(exceptions.NoAffinityError) as excinfo:
            ma.calculate_affinity("DUMMY_USER_2")

        assert "shared rated anime count" in str(excinfo.value).lower()


@vcr.use_cassette("test-no-rated-user.yaml")
def test_exception__no_rated_anime():
    """
    Test if `NoAffinityError` gets raised on a user
    that hasn't rated any anime
    """
    with pytest.raises(exceptions.NoAffinityError) as excinfo:
        malaffinity.MALAffinity(const.TEST_NO_RATED_USERNAME)

    assert "hasn't rated any anime" in str(excinfo.value).lower()


def test_exception__zero_stdev():
    """
    Test if `NoAffinityError` gets raised when the
    stdev of one set of scores is zero
    """
    ma = malaffinity.MALAffinity()

    ma._base_user = "DUMMY_USER"
    ma._base_scores = mocks.dummy_list_to_base_scores()

    with mock.patch("malaffinity.endpoints.myanimelist") as MockClass:
        MockClass.return_value = mocks.mock_stdev_zero_myanimelist_endpoint()

        with pytest.raises(exceptions.NoAffinityError) as excinfo:
            ma.calculate_affinity("DUMMY_USER_2")

        assert "standard deviation of" in str(excinfo.value).lower()
