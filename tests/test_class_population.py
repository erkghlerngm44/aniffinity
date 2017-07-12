import time

import malaffinity

from . import const


def test_normal_population():
    """
    Population via normal methods (passing `base_user`
    to `malaffinity.MALAffinity.__init__`
    """

    time.sleep(5)

    ma = malaffinity.MALAffinity(const.TEST_USERNAME)

    # Check it returned the correct amount of items
    assert len(ma._base_scores) == const.TEST_LIST_LENGTH


def test_population_via_init():
    """
    Population via the `init` method in `malaffinity.MALAffinity`
    """

    time.sleep(5)

    ma = malaffinity.MALAffinity()

    # init it
    ma.init(const.TEST_USERNAME)

    assert len(ma._base_scores) == const.TEST_LIST_LENGTH