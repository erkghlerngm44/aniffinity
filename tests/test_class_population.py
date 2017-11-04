import malaffinity

from . import const
from . import vcr


@vcr.use_cassette("test-user.yaml")
def test_population__normal():
    """
    Population via normal methods (passing `base_user`
    to `malaffinity.MALAffinity.__init__`
    """
    ma = malaffinity.MALAffinity(const.TEST_USERNAME)

    # Check it returned the correct amount of items
    assert len(ma._base_scores) == const.TEST_LIST_LENGTH


@vcr.use_cassette("test-user.yaml")
def test_population__init():
    """
    Population via the `init` method in `malaffinity.MALAffinity`
    """
    ma = malaffinity.MALAffinity()

    ma.init(const.TEST_USERNAME)

    assert len(ma._base_scores) == const.TEST_LIST_LENGTH
