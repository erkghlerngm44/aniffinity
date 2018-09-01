"""malaffinity animelist endpoints."""


import bs4
import requests

from .const import ENDPOINT_URLS, ALIASES, GRAPHQL_QUERY
from .exceptions import (
    InvalidUsernameError, NoAffinityError,
    RateLimitExceededError
)


def main(user):
    """
    Determine whether or not to use AniList or MyAnimeList to get
    a users' list, and return their list using said service.

    :param user: A tuple containing the username and service to use
    :return: `id`, `score` pairs
    :rtype: list
    """
    if type(user) is tuple:
        username, service = user
    else:
        # TODO: Make this better as well idk
        username = user
        service = "MYANIMELIST"

    # TODO: Make this better idk
    # TODO: What if it's not a funct or str?
    # Allow `service` to be a function to use
    if callable(service):
        service_function = service
    elif service.upper() in ALIASES.MYANIMELIST:
        service_function = myanimelist
    elif service.upper() in ALIASES.ANILIST:
        service_function = anilist
    else:
        raise Exception("Unrecognised service.")

    return service_function(username)


def myanimelist(username):
    """
    Retrieve a users' animelist scores from MAL.

    Only anime scored > 0 will be returned, and all
    PTW entries are ignored, even if they are scored.

    :param str username: MAL username
    :return: `id`, `score` pairs
    :rtype: list
    """
    params = {
        "u": username,
        "status": "all",
        "type": "anime"
    }

    resp = requests.request("GET", ENDPOINT_URLS.MYANIMELIST, params=params)

    # Check if MAL's hitting you with a 429 and raise an exception if so.
    if resp.status_code == 429:  # pragma: no cover
        raise RateLimitExceededError("MAL rate limit exceeded")

    resp = bs4.BeautifulSoup(resp.content, "xml")

    all_anime = resp.find_all("anime")

    # Check if there's actually any anime being returned to us.
    # If not, user probably doesn't exist.
    # MAL should do a better job of highlighting this, but eh.
    if not len(all_anime):
        raise InvalidUsernameError("User `{}` does not exist"
                                   .format(username))

    scores = []

    for anime in all_anime:
        # See if anime is on their PTW and move on if so.
        # This makes sure rated anime that the user hasn't
        # seen does not get added to `scores`.
        # Why do people even do this?
        # PTW == status "6"
        if anime.my_status.string == "6":
            continue

        id = anime.series_animedb_id.string
        id = int(id)

        score = anime.my_score.string
        # Might need changing if MAL allows float scores.
        score = int(score)

        if score > 0:
            scores.append({"id": id, "score": score})

    # Check if there's actually anything in scores.
    # If not, user probably doesn't have any rated anime.
    if not len(scores):
        raise NoAffinityError("User `{}` hasn't rated any anime"
                              .format(username))

    return scores


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
