"""malaffinity class."""


import copy

from . import calcs
from . import endpoints
from . import models
from .exceptions import NoAffinityError


class Aniffinity:
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

    def __init__(self, base_user=None, base_service=None, round=False):
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

        :param base_user: Base user. Specify as a tuple containing the
            username and service to use
        :param round: Decimal places to round affinity values to.
            Specify ``False`` for no rounding
        :type round: int or False
        """
        self._base_username = None
        self._base_service = None
        self._base_scores = {}
        self._round = round

        if base_user:
            self.init(base_user, base_service)

    def __repr__(self):  # noqa: D105  # pragma: no cover
        return "{}(base_username={!r}, base_service={!r}, round={!r})" \
            .format(self.__class__.__name__, self._base_username,
                    self._base_service, self._round)

    def init(self, base_user, base_service=None):
        """
        Retrieve a "base user"'s list, and store it in :attr:`._base_scores`.

        :param base_user: Base user. Specify as a tuple containing the
            username and service to use
        """
        # Figure out the service ourselves, instead of just passing this to
        # `endpoints.main` (and letting it handle everything), as we want
        # to set `self._base_service`.
        base_username, base_service = \
            endpoints._figure_out_service(base_user, base_service)

        self._base_username = base_username
        self._base_service = base_service

        base_list = endpoints._main(base_username, base_service)

        for anime in base_list:
            id = anime["id"]
            score = anime["score"]

            self._base_scores[id] = [score]

        return self

    def comparison(self, user, service=None):
        """
        Get a comparison of scores between the "base user" and ``user``.

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

        :param user: The user to compare the base users' scores to.
            Specify as a tuple containing the username and service to use
        :return: Key-value pairs as described above
        :rtype: dict
        """
        # Check if there's actually a base user to compare scores with.
        if not self._base_username or not self._base_scores:
            raise Exception("No base user has been specified. Call the `init` "
                            "function to retrieve a base users' scores")

        # Create a local, deep-copy of the scores for modification
        scores = copy.deepcopy(self._base_scores)

        user_list = endpoints._main(user, service)

        for anime in user_list:
            id = anime["id"]
            score = anime["score"]

            if id in scores:
                scores[id].append(score)

        # Force to list so no errors when deleting keys.
        for key in list(scores.keys()):
            if not len(scores[key]) == 2:
                del scores[key]

        return scores

    def calculate_affinity(self, user, service=None):
        """
        Get the affinity between the "base user" and ``user``.

        .. note:: The data returned will be a namedtuple, with the affinity
                  and shared rated anime. This can easily be separated
                  as follows (using the user ``Luna`` as ``user``):

                  .. code-block:: python

                      affinity, shared = ma.calculate_affinity("Luna")

                  Alternatively, the following also works:

                  .. code-block:: python

                      affinity = ma.calculate_affinity("Luna")

                  with the affinity and shared available as
                  ``affinity.affinity`` and ``affinity.shared`` respectively.

        .. note:: The final affinity value may or may not be rounded,
                  depending on the value of :attr:`._round`, set at
                  class initialisation.

        :param user: The user to calculate affinity with.
            Specify as a tuple containing the username and service to use
        :return: (float affinity, int shared)
        :rtype: tuple
        """
        scores = self.comparison(user, service)

        # Handle cases where the shared scores are <= 10 so
        # affinity can not be accurately calculated.
        if len(scores) <= 10:
            raise NoAffinityError("Shared rated anime count between "
                                  "`{}` and `{}` is less than eleven"
                                  .format(self._base_username, user))

        # Sort multiple rows of scores into two arrays for calculations.
        # E.G. [1,2], [3,4], [5,6] to [1,3,5], [2,4,6]
        values = scores.values()
        scores1, scores2 = list(zip(*values))

        pearson = calcs.pearson(scores1, scores2)
        pearson *= 100

        if self._round is not False:
            pearson = round(pearson, self._round)

        return models.Affinity(affinity=pearson, shared=len(scores))
