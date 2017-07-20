"""malaffinity exceptions."""


class MALAffinityException(Exception):  # noqa
    """Base class for MALAffinity exceptions."""
    pass


class NoAffinityError(MALAffinityException):  # noqa
    """
    Raised when either the shared rated anime between the base user
    and another user is less than 10, the user does not have any rated
    anime, or the standard deviation of either users' scores is zero.
    """
    pass


class InvalidUsernameError(MALAffinityException):  # noqa
    """Raised when username specified does not exist."""
    pass


class MALRateLimitExceededError(MALAffinityException):  # noqa
    """
    Raised when MAL's blocking your request, because you're going over their
    rate limit of one request every two seconds. Slow down and try again.
    """
    pass
