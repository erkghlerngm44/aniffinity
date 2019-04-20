"""aniffinity animelist endpoints."""


import time
import urllib.parse

import json_api_doc
import requests

from .const import ENDPOINT_URLS, GRAPHQL_QUERY
from .exceptions import (
    InvalidUserError, NoAffinityError,
    RateLimitExceededError
)


TOO_MANY_REQUESTS = requests.codes.TOO_MANY_REQUESTS


def anilist(username, **kws):
    """
    Retrieve a users' animelist scores from AniList.

    Only anime scored > 0 will be returned, and all
    PTW entries are ignored, even if they are scored.

    :param str username: AniList username
    :return: Mapping of ``id`` to ``score``
    :rtype: dict
    """
    params = {
        "query": GRAPHQL_QUERY,
        "variables": {"userName": username}
    }

    resp = requests.request("POST", ENDPOINT_URLS.ANILIST, json=params)

    if resp.status_code == TOO_MANY_REQUESTS:  # pragma: no cover
        raise RateLimitExceededError("AniList rate limit exceeded")

    # TODO: Handling for stuff
    # TODO: Consistency vars and stuff

    mlc = resp.json()["data"]["MediaListCollection"]

    if not mlc:
        # Is this the only reason for not having anything in the MLC?
        raise InvalidUserError("User `{}` does not exist on AniList"
                               .format(username))

    scores = {}

    for lst in mlc["lists"]:
        entries = lst["entries"]

        for entry in entries:
            id = str(entry["media"]["idMal"])
            score = entry["score"]

            if score > 0:
                scores[id] = score

    if not len(scores):
        raise NoAffinityError("User `{}` hasn't rated any anime on AniList"
                              .format(username))

    return scores


def kitsu(user_slug_or_id, **kws):
    """
    Retrieve a users' animelist scores from Kitsu.

    Only anime scored > 0 will be returned, and all
    PTW entries are ignored, even if they are scored.

    :param str user_slug_or_id: Kitsu user slug or user id
    :return: Mapping of ``id`` to ``score``
    :rtype: dict
    """
    # TODO: Move this somewhere else?
    def get_pages(params):
        session = requests.Session()

        # Convert params dict to url string and add it onto the URL,
        # as the `next_url` pagination links include the updated params
        # already, so we want to avoid either duplicating the params,
        # updating the params ourselves, or clearing the params after
        # the first run.
        next_url = ENDPOINT_URLS.KITSU + "?" + urllib.parse.urlencode(params)
        while next_url:
            # Kitsu's API doesn't really need the limiting, but just in case..
            time.sleep(kws.get("wait_time", 0))

            resp = session.request("GET", next_url)

            # TODO: Handle other exceptions, etc
            if resp.status_code == TOO_MANY_REQUESTS:  # pragma: no cover
                raise RateLimitExceededError("Kitsu rate limit exceeded")

            json = resp.json()

            # The API silently fails if the user id is invalid,
            # which is a PITA, but hey...
            if not json["data"]:
                raise InvalidUserError("User `{}` does not exist on Kitsu"
                                       .format(user_slug_or_id))

            yield json
            next_url = json["links"].get("next")

    if not user_slug_or_id.isdigit():
        # Username is the "slug". The API is incapable of letting us pass
        # a slug filter to the `library-entries` endpoint, so we need to
        # get the user id first...
        # TODO: Tidy this up
        user_id = requests.request(
            "GET",
            "https://kitsu.io/api/edge/users",
            params={"filter[slug]": user_slug_or_id}
        ).json()["data"]
        if not user_id:
            raise InvalidUserError("User `{}` does not exist on Kitsu"
                                   .format(user_slug_or_id))
        user_id = user_id[0]["id"]  # assume it's the first one, idk
    else:
        # Assume that if the username is all digits, then the user id is
        # passed so we can just send this straight into `library-entries`
        user_id = user_slug_or_id

    params = {
        "fields[anime]": "id,mappings",
        # TODO: Find a way to specify username instead of user_id.
        "filter[user_id]": user_id,
        "filter[kind]": "anime",
        "filter[status]": "completed,current,dropped,on_hold",
        "include": "anime,anime.mappings",
        "page[offset]": "0",
        "page[limit]": "500"
    }

    scores = {}
    for page in get_pages(params):
        for entry in json_api_doc.parse(page):
            # Our request returns mappings with various services, we need
            # to find the MAL one to get the MAL id to use.
            for mapping in entry["anime"]["mappings"]:
                if mapping["externalSite"] == "myanimelist/anime":
                    id = mapping["externalId"]
                    break
            else:
                # Eh, if there isn't a MAL mapping, then the entry probably
                # doesn't exist there. Not much we can do if that's the case..
                continue

            score = entry["ratingTwenty"]

            # Why does this API do `score == None` when it's not rated?
            # Whatever happened to 0?
            if score is not None:
                scores[id] = score

    if not len(scores):
        raise NoAffinityError("User `{}` hasn't rated any anime on Kitsu"
                              .format(user_slug_or_id))

    return scores


def myanimelist(username, **kws):
    """
    Retrieve a users' animelist scores from MyAnimeList.

    Only anime scored > 0 will be returned, and all
    PTW entries are ignored, even if they are scored.

    :param str username: MyAnimeList username
    :return: Mapping of ``id`` to ``score``
    :rtype: dict
    """
    def get_pages(url):
        session = requests.Session()
        params = {
            "status": "7",  # all entries
            "offset": 0
        }
        # This endpoint only returns 300 items at a time :(
        offset_amount = 300

        list_entries = 1
        while list_entries > 0:
            time.sleep(kws.get("wait_time", 0))

            resp = session.request("GET", url, params=params)

            if resp.status_code == TOO_MANY_REQUESTS:  # pragma: no cover
                raise RateLimitExceededError("MyAnimeList rate limit exceeded")

            json = resp.json()
            if "errors" in json:
                # TODO: Better error handling
                raise InvalidUserError("User `{}` does not exist on "
                                       "MyAnimeList".format(username))

            yield json
            list_entries = len(json)
            params["offset"] += offset_amount

    scores = {}
    url = ENDPOINT_URLS.MYANIMELIST.format(username=username)
    for page in get_pages(url):
        for entry in page:
            if entry["status"] == 6:
                # Entry in PTW, skip
                continue

            id = str(entry["anime_id"])
            score = entry["score"]

            if score > 0:
                scores[id] = score

    if not len(scores):
        raise NoAffinityError("User `{}` hasn't rated any anime on MyAnimeList"
                              .format(username))

    return scores


SERVICES = {
    "ANILIST": {
        "aliases": {"AL", "A"},
        "url_regex": r"^https?://anilist\.co/user/([a-z0-9_-]+)(?:\/(?:animelist)?)?$",  # noqa: E501
        "endpoint": anilist
    },
    "KITSU": {
        "aliases": {"K"},
        "url_regex": r"^https?://kitsu\.io/users/([a-z0-9_-]+)(?:/(?:library(?:\?media=anime)?)?)?$",  # noqa: E501
        "endpoint": kitsu
    },
    "MYANIMELIST": {
        "aliases": {"MAL", "M"},
        "url_regex": r"^https?://myanimelist\.net/(?:profile|animelist)/([a-z0-9_-]+)/?(?:\?status=\d)?",  # noqa: E501
        "endpoint": myanimelist
    }
}
