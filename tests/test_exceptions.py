import time

import pytest

import malaffinity

# from . import const
from . import mocks
from .mocks import hook_mock_endpoint_and_run_function


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

    def funct():
        with pytest.raises(exceptions.NoAffinityError) as excinfo:
            ma.calculate_affinity("DUMMY_USER_2")

        assert "shared rated anime count" in str(excinfo.value).lower()

    hook_mock_endpoint_and_run_function(
        funct, mocks.mock_mini_myanimelist_endpoint
    )


def test_exception__no_rated_anime():
    """
    Test if `NoAffinityError` gets raised on a user
    that hasn't rated any anime

    Note: User here may rate anime one day.
    If this test fails, that's probably why

    TODO: Make account with no rated anime
    """
    time.sleep(5)

    # Hm, if this fails, it's probably because the user
    # specified here actually decided to rate some anime
    # TODO: Make account with anime in it, but not rated, so we don't
    # have to rely on another account we have no control over
    with pytest.raises(exceptions.NoAffinityError) as excinfo:
        malaffinity.MALAffinity("TheGreatAtario")

    assert "hasn't rated any anime" in str(excinfo.value).lower()


def test_exception__zero_stdev():
    """
    Test if `NoAffinityError` gets raised when the
    stdev of one set of scores is zero
    """
    ma = malaffinity.MALAffinity()

    ma._base_user = "DUMMY_USER"
    ma._base_scores = mocks.dummy_list_to_base_scores()

    def funct():
        with pytest.raises(exceptions.NoAffinityError) as excinfo:
            ma.calculate_affinity("DUMMY_USER_2")

        assert "standard deviation of" in str(excinfo.value).lower()

    hook_mock_endpoint_and_run_function(
        funct, mocks.mock_stdev_zero_myanimelist_endpoint
    )
