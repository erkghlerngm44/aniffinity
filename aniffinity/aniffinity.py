"""aniffinity class."""


from . import calcs
from . import models
from . import resolver
from .exceptions import NoAffinityError


class Aniffinity:
    """
    The Aniffinity class.

    The purpose of this class is to store a "base user"'s scores, so
    affinity with other users can be calculated easily.

    For the username ``Josh`` on the service ``AniList``, the class can
    be initialised as follows:

    ..  code-block:: python

        from aniffinity import Aniffinity

        af = Aniffinity("Josh", base_service="AniList")

    There are multiple ways of specifying this information, and multiple
    ways to initialise this class. For more info, read the documentation.

    The instance, stored in ``af``, will now hold ``Josh``'s scores.

    :meth:`.comparison` and :meth:`.calculate_affinity` can now be called,
    to perform operations on this data.
    """

    def __init__(self, base_user=None, base_service=None, round=10, **kws):
        """
        Initialise an instance of ``Aniffinity``.

        The information required to retrieve a users' score from a service
        are their "username" and "service". For a list of "service"s,
        read the documentation.

        ..  note::
            As this applies to the "base" user, the params used are
            ``base_user`` and ``base_service`` respectively.

        There are multiple ways of specifying the above information,
        and multiple aliases for services that can be used as shorthand.
        As docstrings are annoying to write, please refer to the
        documentation for a list of these. For an example of the simplest
        method to use, refer to the docstring for the :class:`Aniffinity`
        class.

        ..  note::
            To avoid dealing with dodgy globals, this class MAY be
            initialised without the ``base_user`` argument, in the global
            scope (if you wish), but :meth:`.init` MUST be called sometime
            afterwards, with a ``base_user`` and ``base_service`` passed,
            before affinity calculations take place.

            Example (for the username ``Josh`` on the service ``AniList``):

            ..  code-block:: python

                from aniffinity import Aniffinity

                af = Aniffinity()

                ma.init("Josh", base_service="AniList")

            The class should then be good to go.

        :param base_user: Base user
        :type base_user: str or tuple
        :param base_service: The service to use. If no value is specified
            for this param, specify the service in the ``base_user`` param,
            either as part of a url, or in a tuple
        :type base_service: str or None
        :param round: Decimal places to round affinity values to.
            Specify ``False`` for no rounding
        :type round: int or False
        :param int wait_time: Wait time in seconds between paginated
            requests (default: 2)
        """
        self._base_username = None
        self._base_service = None
        self._base_scores = {}
        self._round = round
        self._wait_time = kws.get("wait_time", 2)

        if base_user:
            self.init(base_user, base_service)

    def __repr__(self):  # noqa: D105  # pragma: no cover
        return "{}(base_user={!r}, base_service={!r}, round={!r})" \
            .format(self.__class__.__name__, self._base_username,
                    self._base_service, self._round)

    def init(self, base_user, base_service=None):
        """
        Retrieve a "base user"'s list, and store it in :attr:`._base_scores`.

        :param base_user: Base user
        :type base_user: str or tuple
        :param base_service: The service to use. If no value is specified
            for this param, specify the service in the ``base_user`` param,
            either as part of a url, or in a tuple
        :type base_service: str or None
        """
        # Figure out the service ourselves, instead of just passing this to
        # `resolver.resolve_and_call` (and letting it handle everything),
        # as we want to set `self._base_service`.
        base_username, base_service = \
            resolver.resolve_user(base_user, base_service)

        base_scores = resolver.resolve_and_call(base_username, base_service,
                                                wait_time=self._wait_time)

        self._base_username = base_username
        self._base_service = base_service
        self._base_scores = base_scores

        return self

    def comparison(self, user, service=None):
        """
        Get a comparison of scores between the "base user" and ``user``.

        A Key-Value returned will consist of the following:

        ..  code-block:: none

            {
                "ANIME_ID": [BASE_USER_SCORE, OTHER_USER_SCORE],
                ...
            }

        Example:

        ..  code-block:: none

            {
                "30831": [3, 8],
                "31240": [4, 7],
                "32901": [1, 5],
                ...
            }

        ..  note::
            The ``ANIME_ID`` s will be the MyAnimeList anime ids. As annoying
            as it is, cross-compatibility is needed between services to get
            this module to work, and MAL ids are the best ones to use as other
            APIs are able to specify it. If you wish to use the anime ids for
            the service you specified, set the param
            ``<TO BE IMPLEMENTED>`` to ``<TO BE IMPLEMENTED>``.

        :param user: The user to compare the base users' scores to.
        :type user: str or tuple
        :param service: The service to use. If no value is specified
            for this param, specify the service in the ``user`` param,
            either as part of a url, or in a tuple
        :type service: str or None
        :return: Mapping of ``id`` to ``score`` as described above
        :rtype: dict
        """
        # Check if there's actually a base user to compare scores with.
        if not self._base_username or not self._base_scores:
            raise Exception("No base user has been specified. Call the `init` "
                            "function to retrieve a base users' scores")

        user_list = resolver.resolve_and_call(user, service,
                                              wait_time=self._wait_time)

        comparison_dict = {}

        for key in (self._base_scores.keys() & user_list.keys()):
            comparison_dict[key] = [self._base_scores[key], user_list[key]]

        return comparison_dict

    def calculate_affinity(self, user, service=None):
        """
        Get the affinity between the "base user" and ``user``.

        ..  note::
            The data returned will be a namedtuple, with the affinity
            and shared rated anime. This can easily be separated
            as follows:

            ..  code-block:: python

                affinity, shared = af.calculate_affinity(...)

            Alternatively, the following also works:

            ..  code-block:: python

                affinity = af.calculate_affinity(...)

            with the affinity and shared available as ``affinity.value`` and
            ``affinity.shared`` respectively.

        ..  note::
            The final affinity value may or may not be rounded, depending on
            the value of :attr:`._round`, set at class initialisation.

        :param user: The user to calculate affinity with.
        :type user: str or tuple
        :param service: The service to use. If no value is specified
            for this param, specify the service in the ``user`` param,
            either as part of a url, or in a tuple
        :type service: str or None
        :return: (float affinity, int shared)
        :rtype: tuple
        """
        scores = self.comparison(user, service)

        # Handle cases where the shared scores are <= 10 so
        # affinity can not be accurately calculated.
        if len(scores) <= 10:
            # FIXME: Ok I can't think of a clean way of doing this, so this
            # will have to do until I find a good implementation...
            res_username, res_service = \
                resolver.resolve_user(user, service)
            raise NoAffinityError(
                "Shared rated anime count between `{}:{}` and `{}:{}` is "
                "less than eleven"
                .format(self._base_service, self._base_username,
                        res_service, res_username)
            )

        # Sort multiple rows of scores into two arrays for calculations.
        # E.G. [1,2], [3,4], [5,6] to [1,3,5], [2,4,6]
        scores1, scores2 = zip(*scores.values())

        try:
            pearson = calcs.pearson(scores1, scores2)
        except ZeroDivisionError:
            # denominator is zero. catch this and raise our own exception.
            # FIXME: Ditto
            res_username, res_service = \
                resolver.resolve_user(user, service)
            raise NoAffinityError(
                "Standard deviation of `{}:{}` or `{}:{}` scores is zero"
                .format(self._base_service, self._base_username,
                        res_service, res_username)
            )

        pearson *= 100

        if self._round is not False:
            pearson = round(pearson, self._round)

        return models.Affinity(value=pearson, shared=len(scores))
