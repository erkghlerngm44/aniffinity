"""malaffinity class."""


import copy

from . import calcs
from . import endpoints

from .exceptions import (
    NoAffinityError,
)


class MALAffinity:
    """
    The MALAffinity class.

    The purpose of this class is to store a "base user"'s scores, so
    affinity with other users can be calculated easily.

    For the user ``Xinil``, the class can be initialised as follows:

    .. code-block:: python

        from malaffinity import MALAffinity

        ma = MALAffinity("Xinil")

    The instance, stored in ``ma``, will now hold ``Xinil``'s scores.

    :meth:`.comparison` and :meth:`.calculate_affinity` can now be called,
    to perform operations on this data.
    """

    def __init__(self, base_user=None, round=False):
        """
        Initialise an instance of `MALAffinity`.

        .. note:: To avoid dealing with dodgy globals, this class MAY
                  be initialised without the ``base_user`` argument,
                  in the global scope (if you wish), but :meth:`.init`
                  MUST be called sometime afterwards, with a ``base_user``
                  passed, before affinity calculations take place.

                  Example (for the user ``Xinil``):

                  .. code-block:: python

                      from malaffinity import MALAffinity

                      ma = MALAffinity()

                      ma.init("Xinil")

                  The class should then be good to go.

        :param base_user: Base MAL username
        :type base_user: str or None
        :param round: Decimal places to round affinity values to.
            Specify ``False`` for no rounding
        :type round: int or False
        """
        self._base_user = None
        self._base_scores = {}
        self._round = round

        if base_user:
            self.init(base_user)

    def __repr__(self):  # noqa: D105  # pragma: no cover
        return "{}(base_user={!r}, round={!r})" \
            .format(self.__class__.__name__, self._base_user, self._round)

    def init(self, base_user):
        """
        Retrieve a "base user"'s list, and store it in :attr:`._base_scores`.

        :param str base_user: Base users' username
        """
        self._base_user = base_user

        # Modify this for multiple services support when the time comes
        base_list = endpoints.myanimelist(base_user)

        for anime in base_list:
            id = anime["id"]
            score = anime["score"]

            self._base_scores[id] = [score]

        return self

    def comparison(self, username):
        """
        Get a comparison of scores between the "base user" and ``username``.

        A Key-Value returned will consist of the following:

        .. code-block:: none

            {
                ANIME_ID: [BASE_USER_SCORE, OTHER_USER_SCORE],
                ...
            }

        Example:

        .. code-block:: none

            {
                30831: [3, 8],
                31240: [4, 7],
                32901: [1, 5],
                ...
            }

        .. warning:: The JSON returned isn't valid JSON. The keys are stored
                     as integers instead of the JSON standard of strings.
                     You'll want to force the keys to strings if you'll be
                     using the ids elsewhere.

        :param str username: The username to compare the base users' scores to
        :return: Key-value pairs as described above
        :rtype: dict
        """
        # Check if there's actually a base user to compare scores with.
        if not self._base_user or not self._base_scores:
            raise Exception("No base user has been specified. Call the `init` "
                            "function to retrieve a base users' scores")

        # Create a local, deep-copy of the scores for modification
        scores = copy.deepcopy(self._base_scores)

        their_list = endpoints.myanimelist(username)

        for anime in their_list:
            id = anime["id"]
            score = anime["score"]

            if id in scores:
                scores[id].append(score)

        # Force to list so no errors when deleting keys.
        for key in list(scores.keys()):
            if not len(scores[key]) == 2:
                del scores[key]

        return scores

    def calculate_affinity(self, username):
        """
        Get the affinity between the "base user" and ``username``.

        .. note:: The data returned will be a tuple, with the affinity
                  and shared rated anime. This can easily be separated
                  as follows (using the user ``Luna`` as ``username``):

                  .. code-block:: python

                      affinity, shared = ma.calculate_affinity("Luna")

        .. note:: The final affinity value may or may not be rounded,
                  depending on the value of :attr:`._round`, set at
                  class initialisation.

        :param str username: The username to calculate affinity with
        :return: (float affinity, int shared)
        :rtype: tuple
        """
        scores = self.comparison(username)

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

        pearson = calcs.pearson(scores1, scores2)
        pearson *= 100

        if self._round is not False:
            pearson = round(pearson, self._round)

        return pearson, len(scores)
