"""
Calculate affinity between two MyAnimeList users
"""

import copy

import bs4
import requests
import statistics

from . import calcs


# Meta stuff
from .__about__ import (
    __author__, __copyright__, __email__, __license__,
    __summary__, __title__, __uri__, __version__
)
__all__ = ["MALAffinity", "calculate_affinity",
           "NoAffinityError", "InvalidUsernameError",
           "MALRateLimitExceededError"]


# Custom exceptions.
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


class MALAffinity:
    _URL = "https://myanimelist.net/malappinfo.php"

    def __init__(self, base_user=None, round=False):
        """
        The MALAffinity class.

        To help with scripts that have the initialisation of this class
        and the actual affinity calculations in different areas, this class may
        be initialised without the `base_user` param, but the `init`
        function inside MUST be invoked before affinity calculations

        :param base_user: Base MAL username
        :type base_user: str or None
        
        :param round: Decimal places to round affinity values to
        :type round: int or False
        """

        # Will get overridden in `init` function.
        self._base_user = None
        self._round = round
        self._base_scores = {}

        if base_user:
            self.init(base_user)

    def _retrieve_scores(self, username, status="all", type="anime"):
        params = {
            "u": username,
            "status": status,
            "type": type
        }

        resp = requests.request("GET", self._URL, params=params)

        # Check if MAL's hitting you with a 429 and raise an exception if so.
        # TODO: Look into using `if not resp.ok:`
        if resp.status_code == requests.codes.too_many_requests:
            raise MALRateLimitExceededError("MAL rate limit exceeded. Slow down and try again.")

        resp = bs4.BeautifulSoup(resp.content, "xml")

        all_anime = resp.findAll("anime")

        # Check if there's actually any anime being returned to us.
        # If not, user probably doesn't exist.
        # MAL should do a better job of highlighting this, but eh.
        if not len(all_anime):
            raise InvalidUsernameError("User `{}` does not exist.".format(username))

        # TODO: Look into confusion with this and 'scores' var in 'calculate_affinity'
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
                scores.append({ "id": id, "score": score })

        # Check if there's actually anything in scores.
        # If not, user probably doesn't have any rated anime.
        if not len(scores):
            raise NoAffinityError("User `{}` hasn't rated any anime.".format(username))

        return scores

    # TODO: Rename this?
    def init(self, base_user):
        """
        Get the base user's list and create the `base scores` dict that
        other people's scores will be compared to

        Base scores will be saved to self._base_scores
        One may want to check that this is populated after invoking this function
        before running anything else here

        :param str base_user: Base username whose list others' lists will be compared to
        
        :return: Nothing
        """

        # Being a bit cheeky and setting self._base_user here instead of __init__
        self._base_user = base_user

        base_list = self._retrieve_scores(base_user)

        for anime in base_list:
            id    = anime["id"]
            score = anime["score"]

            self._base_scores[id] = [score]

        # TODO: Return self._base_scores?
        return

    def calculate_affinity(self, username):
        """
        Get the affinity between the base user and someone else

        Will either return the unrounded Pearson's correlation coefficient * 100,
        or rounded value, depending on the value of the `self._round` variable set
        at class initialisation

        :param str username: The username to compare the base user's scores to
        
        :return: (float affinity, int shared)
        :rtype: tuple
        """

        # Check if there's actually a base user to compare scores with.
        # `init` will assign the username to the `self._base_user` var and
        # populate the `self._base_scores` dict when it retrieves the base user's
        # scores, so we can test if those vars have been set.
        if not self._base_user or not self._base_scores:
            # Too lazy to make a custom exception for this.
            raise Exception("No base user has been specified. "
                            "Call the `init` function to retrieve a base user's scores.")

        # Create a local, deep-copy of the scores
        scores = copy.deepcopy(self._base_scores)

        # TODO: Rename "their_list" to a better var name
        their_list = self._retrieve_scores(username)

        for anime in their_list:
            id    = anime["id"]
            score = anime["score"]

            if id in scores:
                scores[id].append(score)

        # Forced to list so no errors when deleting keys.
        for key in list(scores.keys()):
            if not len(scores[key]) == 2:
                del scores[key]

        # Handle cases where the shared scores are <= 10 so
        # affinity can not be accurately calculated.
        if len(scores) <= 10:
            raise NoAffinityError(
                "Shared rated anime count between `{}` and `{}` is less than ten."
                    .format(self._base_user, username)
            )

        # Sort multiple rows of scores into two arrays for calculations.
        # E.G. [1,2], [3,4], [5,6] to [1,3,5], [2,4,6]
        values = scores.values()
        scores1, scores2 = list(zip(*values))

        # Check if standard deviation of scores1 or scores2 is zero. If so, affinity
        # can't be calculated as dividing by zero gives you NaN. (It's impossible)
        if not statistics.stdev(scores1) or not statistics.stdev(scores2):
            # TODO: Message
            raise NoAffinityError

        pearson = calcs.pearson(scores1, scores2)
        pearson *= 100

        if self._round is not False:
            pearson = round(pearson, self._round)

        return pearson, len(scores)


def calculate_affinity(user1, user2, round=False):
    """
    Quick one-off affinity calculations
    
    Creates an instance of the `MALAffinity` class with `user1`, 
    then calculates affinity with `user2`
    
    :param str user1: First user
    :param str user2: Second user
    
    :param round: Decimal places to round affinity values to
    :type round: int or False

    :return: (float affinity, int shared)
    :rtype: tuple
    """

    return MALAffinity(base_user=user1, round=round).calculate_affinity(user2)
