"""aniffinity endpoints resolver."""


import re
import warnings

from . import endpoints
from .const import DEFAULT_SERVICE
from .exceptions import InvalidUserError


def resolve_user(user, service=None):
    """
    Resolve the `user` and `service` into "proper" values.

    As these params can take different types and formats, this
    function resolves all that to return just the username, and the
    full name of the service to use.

    :param user: A user
    :type user: str or tuple
    :param service: The service to use. If no value is specified
        for this param, specify the service in the ``user`` param,
        either as part of a url regex, or in a tuple
    :type service: str or None
    :return: (username, service)
    :rtype: tuple
    """
    username = None
    service_name_resolved = None

    if service:
        # `service` already specified so we don't need to do much work
        username = user
        service = service.upper()

        if service in endpoints.SERVICES:
            # Fastest option - service name fully specified so no
            # need to do any more work
            service_name_resolved = service
        else:
            # Check aliases to see which service is intended to be used
            for service_name, service_data in endpoints.SERVICES.items():
                if service in service_data["aliases"]:
                    service_name_resolved = service_name
                    break
            else:
                raise InvalidUserError("Invalid service name")

    elif type(user) is str:
        # `user` may be a url, we need to figure out which
        # service the regex matches
        for service_name, service_data in endpoints.SERVICES.items():
            match = re.search(service_data["url_regex"], user, re.I)

            if match:
                username = match.group(1)
                service_name_resolved = service_name
                break
        else:
            # Maybe it's just a URL and we don't have an endpoint for that
            # particular service. Check this before assuming anything else.
            if re.match(r"https?://", user):
                raise InvalidUserError("Invalid service URL")

            # Maybe it's a username/service in the form `SERVICE:username`
            # or `SERVICE/username`...
            match = re.match(r"(?P<service>\w+)[:/](?P<user>[a-z0-9_-]+)$",
                             user, flags=re.I)
            if match:
                return resolve_user(**match.groupdict())

            # There aren't any more supported resolving techniques.
            # `user` may just be the username, so let's assume that and
            # use the default service.
            warnings.warn("No service has been specified, so assuming the "
                          "default '{}'. To stop this warning from appearing "
                          "again, please specify a service to use."
                          .format(DEFAULT_SERVICE), Warning, stacklevel=3)
            username = user
            service_name_resolved = DEFAULT_SERVICE

    # If `user` is a tuple as `(username, service)`
    elif isinstance(user, tuple) and len(user) == 2:
        # Unpack the tuple and pass the values back to this function.
        # Can't see anything going wrong with this... [](#yuishrug)
        return resolve_user(*user)

    # Incorrect usage
    else:
        raise InvalidUserError("Invalid usage - check your `user` "
                               "and `service` values")

    return username, service_name_resolved


def resolve_and_call(user, service=None, **kws):
    """
    Determine which endpoint to use and return a users' scores from that.

    Resolve the `user` and `service` to find an endpoint,
    and call that endpoint.

    :param user: A user
    :type user: str or tuple
    :param service: The service to use. If no value is specified
        for this param, specify the service in the ``user`` param,
        either as part of a url regex, or in a tuple
    :type service: str or None
    :param int wait_time: Wait time in seconds between paginated
        requests
    :return: Mapping of ``id`` to ``score``
    :rtype: dict
    """
    # Should be fine doing this.
    # If we've already passed the data to `_resolve_service` and passed
    # the result back in, it'll just throw the info back to us
    username, service = resolve_user(user, service)

    # We don't need to worry about invalid services here, as
    # `resolve_user` will raise the exception itself if it is invalid.
    service_data = endpoints.SERVICES.get(service)
    return service_data["endpoint"](username, **kws)
