"""malaffinity animelist endpoints."""

import bs4
import requests

from .const import ENDPOINT_URLS
from .exceptions import (
    InvalidUsernameError, NoAffinityError,
    MALRateLimitExceededError
)


# TODO: Make it easier for other services to be added in
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
        raise MALRateLimitExceededError("MAL rate limit exceeded")

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
