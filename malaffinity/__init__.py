"""Calculate affinity between MyAnimeList users."""


from .malaffinity import MALAffinity


# Meta stuff
from .__about__ import (  # NOQA
    __author__, __copyright__, __email__, __license__,
    __summary__, __title__, __uri__, __version__
)


def calculate_affinity(user1, user2, round=False):
    """
    Quick one-off affinity calculations.

    Creates an instance of the `MALAffinity` class with `user1`,
    then calculates affinity with `user2`.

    :param str user1: First user
    :param str user2: Second user
    :param round: Decimal places to round affinity values to.
        Specify ``False`` for no rounding
    :type round: int or False
    :return: (float affinity, int shared)
    :rtype: tuple
    """
    return MALAffinity(base_user=user1, round=round).calculate_affinity(user2)
