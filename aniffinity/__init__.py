"""Calculate affinity between MyAnimeList users."""


from .aniffinity import Aniffinity


# Meta stuff
from .__about__ import (  # noqa: F401
    __author__, __copyright__, __email__, __license__,
    __summary__, __title__, __uri__, __version__
)


def comparison(user1, user2):  # pragma: no cover
    """
    Quick one-off scores comparison between two users.

    Creates an instance of the ``MALAffinity`` class with ``user1``,
    then returns a comparison of scores with ``user2``.

    As there are no params to specify which service to use for each user,
    specify this information for ``user1`` and ``user2`` by passing a tuple
    to each of these, containing: (username, service).

    :param tuple user1: First user
    :param tuple user2: Second user
    :return: Key-value pairs as described in ``MALAffinity.comparison``
    :rtype: dict
    """
    return Aniffinity(base_user=user1).comparison(user2)


def calculate_affinity(user1, user2, round=False):  # pragma: no cover
    """
    Quick one-off affinity calculations.

    Creates an instance of the ``MALAffinity`` class with ``user1``,
    then calculates affinity with ``user2``.

    As there are no params to specify which service to use for each user,
    specify this information for ``user1`` and ``user2`` by passing a tuple
    to each of these, containing: (username, service).

    :param tuple user1: First user
    :param tuple user2: Second user
    :param round: Decimal places to round affinity values to.
        Specify ``False`` for no rounding
    :type round: int or False
    :return: (float affinity, int shared)
    :rtype: tuple
    """
    return Aniffinity(base_user=user1, round=round).calculate_affinity(user2)
