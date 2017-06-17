"""
malaffinity exceptions
"""


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
