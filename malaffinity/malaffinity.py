"""
malaffinity class
"""


import copy

import bs4
import requests
import statistics

from . import calcs

# Lines are getting too long, best to import the exceptions
# manually, instead of just importing `exceptions`
from .exceptions import (
    InvalidUsernameError, NoAffinityError,
    MALRateLimitExceededError
)


class MALAffinity:
    """
    The MALAffinity class

    Stores a `base user`s' scores, to be compared with
    other users' scores
    """

    _URL = "https://myanimelist.net/malappinfo.php"

    def __init__(self, base_user=None, round=False):
        """
        Initialise an instance of `MALAffinity`

        If `base_user` is `None`, the `init` function MUST be
        called sometime after initialisation, with a `base_user`
        provided, before affinity calculations take place

        :param base_user: Base MAL username
        :type base_user: str or None

        :param round: Decimal places to round affinity values to
        :type round: int or False
        """

        # Will get overridden in `init` function.
        self._base_user = None
        self._base_scores = {}
        self._round = round

        if base_user:
            self.init(base_user)

    def __repr__(self):
        # TODO: Surely there has to be a better way of doing this...
        # TODO: Make this look less ugly
        return 'MALAffinity(base_user={}, round={})' \
               .format(repr(self._base_user), repr(self._round))

    def _retrieve_scores(self, username):
        """
        Retrieve a users' animelist scores

        Only anime scored > 0 will be returned, and all 
        PTW entries are ignored, even if they are scored

        :param str username: MAL username
        :return: `id`, `score` pairs
        :rtype: list
        """

        params = {
            "u": username,
            "status": "all",
            "type": "anime"
        }

        resp = requests.request("GET", self._URL, params=params)

        # Check if MAL's hitting you with a 429 and raise an exception if so.
        if resp.status_code == requests.codes.too_many_requests:
            raise MALRateLimitExceededError("MAL rate limit exceeded")

        resp = bs4.BeautifulSoup(resp.content, "xml")

        all_anime = resp.find_all("anime")

        # Check if there's actually any anime being returned to us.
        # If not, user probably doesn't exist.
        # MAL should do a better job of highlighting this, but eh.
        if not len(all_anime):
            raise InvalidUsernameError("User `{}` does not exist"
                                       .format(username))

        # TODO: Generator?
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

    # TODO: Rename this?
    def init(self, base_user):
        """
        Get the base users' list and create the `base scores`
        dict that other people's scores will be compared to

        Base scores will be saved to self._base_scores
        You may want to check that this is populated after
        running this function, before running anything else

        :param str base_user: Base users' username
        """

        self._base_user = base_user

        base_list = self._retrieve_scores(base_user)

        for anime in base_list:
            id = anime["id"]
            score = anime["score"]

            self._base_scores[id] = [score]

        return self

    def calculate_affinity(self, username):
        """
        Get the affinity between the base user and another user

        Will either return the unrounded Pearson's correlation
        coefficient * 100, or rounded value, depending on the
        value of the `self._round` variable

        :param str username: The username to compare the base users' scores to

        :return: (float affinity, int shared)
        :rtype: tuple
        """

        # Check if there's actually a base user to compare scores with.
        # `init` will assign the username to the `self._base_user` var and
        # populate the `self._base_scores` dict when it retrieves the
        # base user's scores, so we can test if those vars have been set.
        if not self._base_user or not self._base_scores:
            # Too lazy to make a custom exception for this.
            raise Exception("No base user has been specified. Call the `init` "
                            "function to retrieve a base users' scores")

        # Create a local, deep-copy of the scores
        scores = copy.deepcopy(self._base_scores)

        their_list = self._retrieve_scores(username)

        for anime in their_list:
            id = anime["id"]
            score = anime["score"]

            if id in scores:
                scores[id].append(score)

        # Force to list so no errors when deleting keys.
        for key in list(scores.keys()):
            if not len(scores[key]) == 2:
                del scores[key]

        # Handle cases where the shared scores are <= 10 so
        # affinity can not be accurately calculated.
        if len(scores) <= 10:
            raise NoAffinityError("Shared rated anime count between "
                                  "`{}` and `{}` is less than eleven"
                                  .format(self._base_user, username))

        # Sort multiple rows of scores into two arrays for calculations.
        # E.G. [1,2], [3,4], [5,6] to [1,3,5], [2,4,6]
        values = scores.values()
        scores1, scores2 = list(zip(*values))

        # Check if standard deviation of scores1 or scores2 is zero. If so,
        # affinity can't be calculated as dividing by zero is impossible
        if not statistics.stdev(scores1) or not statistics.stdev(scores2):
            raise NoAffinityError("Standard deviation of `{}` "
                                  "or `{}`'s scores is zero"
                                  .format(self._base_user, username))

        pearson = calcs.pearson(scores1, scores2)
        pearson *= 100

        if self._round is not False:
            pearson = round(pearson, self._round)

        return pearson, len(scores)
