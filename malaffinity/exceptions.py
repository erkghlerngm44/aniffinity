"""
malaffinity exceptions
"""


class MALAffinityException(Exception):
    """Base class for MALAffinity exceptions"""
    pass


class NoAffinityError(MALAffinityException):
    """
    Raised when either the shared rated anime between the base user
    and another user is less than 10, the user does not have any rated
    anime, or the standard deviation of either users' scores is zero
    """
    pass


class InvalidUsernameError(MALAffinityException):
    """Raised when username specified does not exist"""
    pass


class MALRateLimitExceededError(MALAffinityException):
    """
    Raised when MAL's blocking your request, because you're going over their
    rate limit of one request every two seconds. Slow down and try again
    """
    pass
