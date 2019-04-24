"""Calculate affinity between anime list users."""


from .aniffinity import Aniffinity


# Meta stuff
from .__about__ import (  # noqa: F401
    __author__, __copyright__, __email__, __license__,
    __summary__, __title__, __uri__, __version__
)


def comparison(user1, user2, **kws):  # pragma: no cover
    """
    Quick one-off scores comparison between two users.

    Creates an instance of the ``Aniffinity`` class with ``user1``,
    then returns a comparison of scores with ``user2``.

    As there are no params to specify which service to use for each user,
    specify this information for both ``user1`` and ``user2`` by passing
    a tuple for each of these, containing (username, service), or by
    passing a string in the format ``SERVICE:username``.

    :param user1: First user
    :type user1: str or tuple
    :param user2: Second user
    :type user2: str or tuple
    :param int wait_time: Wait time in seconds between paginated
        requests (default: 2)
    :return: Key-value pairs as described in ``Aniffinity.comparison``
    :rtype: dict
    """
    return Aniffinity(base_user=user1, **kws).comparison(user2)


def calculate_affinity(user1, user2, **kws):  # pragma: no cover
    """
    Quick one-off affinity calculations.

    Creates an instance of the ``Aniffinity`` class with ``user1``,
    then calculates affinity with ``user2``.

    As there are no params to specify which service to use for each user,
    specify this information for both ``user1`` and ``user2`` by passing
    a tuple for each of these, containing (username, service), or by
    passing a string in the format ``SERVICE:username``.

    :param user1: First user
    :type user1: str or tuple
    :param user2: Second user
    :type user2: str or tuple
    :param round: Decimal places to round affinity values to.
        Specify ``False`` for no rounding.
    :type round: int or False
    :param int wait_time: Wait time in seconds between paginated
        requests (default: 2)
    :return: (float affinity, int shared)
    :rtype: tuple
    """
    return Aniffinity(base_user=user1, **kws).calculate_affinity(user2)
