"""aniffinity exceptions."""


class RateLimitExceededError(Exception):  # noqa: D204, D205, D400
    """
    Raised when the service is blocking your request, because you're going
    over their rate limit. Slow down and try again.
    """
    pass


class AniffinityException(Exception):  # noqa: D204
    """Base class for Aniffinity exceptions."""
    pass


class InvalidUserError(AniffinityException):  # noqa: D204, D205, D400
    """
    Raised when username specified does not exist in the service,
    or the service does not exist.
    """
    pass


class NoAffinityError(AniffinityException):  # noqa: D204, D205, D400
    """
    Raised when either the shared rated anime between the base user
    and another user is less than 11, the user does not have any rated
    anime, or the standard deviation of either users' scores is zero.
    """
    pass
