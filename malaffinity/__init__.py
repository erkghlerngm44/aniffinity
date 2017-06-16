"""
Calculate affinity between two MyAnimeList users
"""


from .malaffinity import MALAffinity


# Meta stuff
from .__about__ import (
    __author__, __copyright__, __email__, __license__,
    __summary__, __title__, __uri__, __version__
)
__all__ = ["MALAffinity", "calculate_affinity",
           "NoAffinityError", "InvalidUsernameError",
           "MALRateLimitExceededError"]


# Custom exceptions.
class NoAffinityError(Exception):
    """
    Raised when either the shared rated anime between the base user
    and another user is less than 10, or the user does not have any rated anime
    """
    pass
class InvalidUsernameError(Exception):
    """Raised when username specified does not exist"""
    pass
class MALRateLimitExceededError(Exception):
    """
    Raised when MAL's blocking your request, because you're going over their
    rate limit of one request every two seconds. Slow down and try again
    """
    pass


def calculate_affinity(user1, user2, round=False):
    """
    Quick one-off affinity calculations
    
    Creates an instance of the `MALAffinity` class with `user1`, 
    then calculates affinity with `user2`
    
    :param str user1: First user
    :param str user2: Second user
    
    :param round: Decimal places to round affinity values to
    :type round: int or False

    :return: (float affinity, int shared)
    :rtype: tuple
    """

    return MALAffinity(base_user=user1, round=round).calculate_affinity(user2)
