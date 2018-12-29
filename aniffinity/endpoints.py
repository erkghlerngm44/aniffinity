"""malaffinity animelist endpoints."""


import re
import warnings

import requests

from .const import DEFAULT_SERVICE, ENDPOINT_URLS, GRAPHQL_QUERY
from .exceptions import (
    InvalidUsernameError, NoAffinityError,
    RateLimitExceededError
)


def _figure_out_service(user, service=None):
    """
    Resolve the `user` and `service` into "proper" values.

    As these params can take different types and formats, this
    function resolves all that to return just the username, and the
    full name of the service to use.

    :param user: A user
    :param str service: The service to use. If no value is specified
                        for this param, specify the service in the
                        `user` param, either as part of a url regex, or
                        in a tuple
    :return: Tuple containing username and service name
    """
    username = None
    service_name_resolved = None

    if service:
        # `service` already specified so we don't need to do much work
        username = user
        service = service.upper()

        if service in services:
            # Fastest option - service name fully specified so no
            # need to do any more work
            service_name_resolved = service
        else:
            # Check aliases to see which service is intended to be used
            for service_name, service_data in services.items():
                if service in service_data["aliases"]:
                    service_name_resolved = service_name
                    break
            else:
                raise InvalidUsernameError("Invalid service name")

    elif type(user) is str:
        # `user` should be a url regex then, we just need to figure out
        # which service the regex matches
        for service_name, service_data in services.items():
            match = re.search(service_data["url_regex"], user, re.I)

            if match:
                username = match.group(1)
                service_name_resolved = service_name
                break
        else:
            # Maybe it's just a URL and we don't have an endpoint for that
            # particular service. Check this before assuming anything else.
            if user.startswith("http"):
                raise InvalidUsernameError("Invalid service URL")

            # `user` may just be the username, so let's assume that and
            # use the default service. We really shouldn't, but hey...
            warnings.warn("No service has been specified, so assuming the "
                          "default '{}'. To stop this warning from appearing "
                          "again, please specify a service to use."
                          .format(DEFAULT_SERVICE), Warning)
            username = user
            service_name_resolved = DEFAULT_SERVICE

    # If `user` is a tuple as `(username, service)`
    elif isinstance(user, tuple) and len(user) == 2:
        # Unpack the tuple and pass the values back to this function.
        # Can't see anything going wrong with this... [](#yuishrug)
        return _figure_out_service(*user)

    # Incorrect usage
    else:
        raise InvalidUsernameError("Invalid usage - check your `user`"
                                   "and `service` values")

    return username, service_name_resolved


def _main(user, service=None):
    """
    Determine which endpoint to use and return a users' scores from that.

    :param user: A user
    :param str service: The service to use. If no value is specified
                        for this param, specify the service in the
                        `user` param, either as part of a url regex, or
                        in a tuple
    :return: `id`, `score` pairs
    :rtype: list
    """
    # Should be fine doing this.
    # If we've already passed the data to `figure_out_service` and passed
    # the result back in, it'll just throw the info back to us
    username, service = _figure_out_service(user, service)

    # We don't need to worry about invalid services here, as
    # `figure_out_service` will raise the exception itself if it is invalid.
    service_data = services.get(service)
    return service_data["endpoint"](username)


def anilist(username):
    """
    Retrieve a users' animelist scores from AniList.

    Only anime scored > 0 will be returned, and all
    PTW entries are ignored, even if they are scored.

    :param str username: AniList username
    :return: `id`, `score` pairs
    :rtype: list
    """
    params = {
        "query": GRAPHQL_QUERY,
        "variables": {"userName": username}
    }

    resp = requests.request("POST", ENDPOINT_URLS.ANILIST, json=params)

    if resp.status_code == 429:  # pragma: no cover
        raise RateLimitExceededError("AniList rate limit exceeded")

    # TODO: Handling for stuff
    # TODO: Consistency vars and stuff

    mlc = resp.json()["data"]["MediaListCollection"]

    if not mlc:
        # Is this the only reason for not having anything in the MLC?
        raise InvalidUsernameError("User `{}` does not exist"
                                   .format(username))

    scores = []

    for lst in mlc["lists"]:
        # FIXME: Surely there's a better way to do this
        # (Can't figure out how to GraphQL...)
        if lst["name"] == "Planning":
            continue

        entries = lst["entries"]

        for entry in entries:
            id = entry["media"]["idMal"]  # Use MAL ids becs AL's are diff
            score = entry["score"]

            if score > 0:
                scores.append({"id": id, "score": score})

    if not len(scores):
        raise NoAffinityError("User `{}` hasn't rated any anime"
                              .format(username))

    return scores


# We can't move this to `.const` as referencing the endpoints from there
# will get pretty messy...
# TODO: Move the `ENDPOINT_URLS here as well???
services = {
    "ANILIST": {
        "aliases": {"ANILIST", "AL", "A"},
        "url_regex": r"^https?://anilist\.co/user/([a-z0-9_-]+)(?:\/(?:animelist)?)?$",  # noqa: E501
        "endpoint": anilist
    }
}
