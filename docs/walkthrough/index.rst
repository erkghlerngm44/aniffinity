Walkthrough
===========


This section will show the various ways the :class:`.Aniffinity` class can be
initialised with the username ``Foobar`` on the service ``AniList``, and used to
calculate affinity or get a comparison with the user ``baz`` on the service ``Kitsu``.


----


Passing Arguments to the Class and its Methods
----------------------------------------------

As multiple services can be used in this package, there needs to be a way of
telling it which service to use.

In general, the data that needs to be passed to the class and its methods are
a user's "username" and the "service", so that the package can decide which
service endpoint to call.

When initialising the class for the "base" user, the names of these params
will be ``base_user`` and ``base_service``, to denote that this information
applies only to the "base" user. When using the methods inside the class,
these params will be called ``user`` and ``service``.

Using the class method :meth:`.Aniffinity.calculate_affinity` to demonstrate,
which has the ``user`` and ``service`` params, the various ways of passing this
info are as follows:

Method 1: Using the respective arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is by far the fastest method, with the least amount of computing
done to determine which service to use.

..  code-block:: python

    af.calculate_affinity("baz", service="Kitsu")

Method 2: Passing a tuple
~~~~~~~~~~~~~~~~~~~~~~~~~

If a tuple is passed, it must take the form ``(username, service)``.

..  code-block:: python

    user = ("baz", "Kitsu")
    af.calculate_affinity(user)

..  note::
    A namedtuple exists in ``aniffinity.models``, which is created for this
    very purpose. If you wish to use it, this can be created as follows:

    ..  code-block:: python

        user = models.User(username="baz", service="Kitsu")

    This can then be passed where necessary.

Method 3: Passing a URL
~~~~~~~~~~~~~~~~~~~~~~~

..  code-block:: python

    # Do note that this method is somewhat lenient, and also somewhat strict,
    # in the types of URL that it will take. A link to either the user's
    # profile, or their anime list will work.
    af.calculate_affinity("https://kitsu.io/users/baz")

Method 4: Passing a string
~~~~~~~~~~~~~~~~~~~~~~~~~~

If a string is passed that is not a URL, it should take one of the following forms:

* ``SERVICE:USERNAME``
* ``SERVICE/USERNAME``

..  note::
    Note the lack of a space between the ``:`` and ``/``. This will not work if
    there are any spaces between these characters.

..  code-block:: python

    af.calculate_affinity("Kitsu:baz")
    # or
    af.calculate_affinity("Kitsu/baz")

Method 5: Passing a username only
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  warning::
    This is highly unrecommended - the behaviour of this cannot be
    guaranteed, but if you are in a rush then this option does exist.

If a username and no service is passed, the package will use the default
service which, at the time of writing, is `AniList <https://anilist.co>`__.

..  code-block:: python

    af.calculate_affinity("baz")

Aliases
~~~~~~~

For methods 1, 2 and 4, there exist aliases for the service names, which
can be used in place of the full service name. For a list of aliases and
services, see :ref:`available-services`.


----


Initialising the Class
----------------------

The class can be initialised in either one of two ways:

Method 1: Normal initialisation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The class is initialised, with the necessary arguments passed to the
:class:`.Aniffinity` class.

..  code-block:: python

    af = Aniffinity("Foobar", service="AniList")

Method 2: Specifying the arguments after initialisation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The class is initialised, with a the necessary arguments passed sometime
later after initialisation, which may be useful in scripts where creating
globals inside functions or classes or different files is a pain.

..  code-block:: python

    af = Aniffinity()

    # This can be done anywhere, as long as it has access to ``af``,
    # but MUST be done before ``calculate_affinity`` or ``comparison``
    # are called
    af.init("Foobar", service="AniList")

Rounding of the final affinity value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  note::
    This doesn't affect :meth:`.comparison`, so don't worry about
    it if you're just using that.

Do note that the class also has a ``round`` parameter, which is
used to round the final affinity value. This must be specified at class
initialisation if wanted, as it isn't available in :meth:`.init`.
A value for this can be passed as follows:

..  code-block:: python

    # To round to two decimal places
    af = Aniffinity(..., round=2)

    # Alternatively, the following can also work, if you decide to follow
    # method 2 for initialising the class
    af = Aniffinity(round=2)
    af.init(...)


----


Doing Things with the Initialised Class
---------------------------------------

The initialised class, now stored in ``af``, can now perform the following actions:

Calculate affinity with a user
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  note::
    Values may or may not be rounded, depending on the value you passed
    for the ``round`` parameter at class initialisation.

..  code-block:: python

    print(af.calculate_affinity("baz", service="Kitsu"))
    # Affinity(value=37.06659111674594, shared=171)

Note that what is being returned is a namedtuple, containing the affinity value
and shared rated anime. This can be separated into different variables as follows:

..  code-block:: python

    affinity, shared = af.calculate_affinity("baz", service="Kitsu")

    print(affinity)
    # 37.06659111674594
    print(shared)
    # 171

Alternatively, the following also works (as this is a namedtuple):

..  code-block:: python

    affinity = af.calculate_affinity("baz", service="Kitsu")

    print(affinity.value)
    # 37.06659111674594
    print(affinity.shared)
    # 171

Comparing scores with a user
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  code-block:: python

    comparison = af.comparison("baz", service="Kitsu")

    print(comparison)
    # Note: this won't be prettified for you. Run it
    # through a prettifier if you want it to look nice.
    # {
    #     "1": [10, 6],
    #     "5": [8, 6],
    #     "6": [10, 7],
    #     "15": [7, 9],
    #     "16": [8, 5],
    #     ...
    # }

Note that a key-value pair returned here consist of:
``"MYANIMELIST_ID": [BASE_USER_SCORE, OTHER_USER_SCORE]``.

..  note::
    MyAnimeList IDs are used here as a cross-service-compatible identifier
    is needed to match up each anime across services, as the anime ids
    used in different services may differ from each other.

    If you wish to use the anime ids for the service you specify, set
    the param <TO_BE_IMPLEMENTED> to <TO_BE_IMPLEMENTED>

This data can now be manipulated in whatever way you like, to suit your needs.
I like to just get the arrays on their own, zip them and plot a graph with it.


----


Extras
------

..  warning::
    These send a request over to each service in a short amount of time,
    with no wait inbetween them. If you're getting in trouble with them
    for breaking their rate limit, you might have a few problems getting
    these to work without :exc:`.exceptions.RateLimitExceededError`
    getting raised.

..  note::
    Don't use these if you're planning on calculating affinity or getting a comparison
    again with one of the users you've specified when using these.

    It's better to create an instance of the :class:`.Aniffinity` class with
    said user, and using that with the other user(s) that way.

    That instance will hold said users' scores, so they won't have to be retrieved
    again. See the other examples.

For each of these functions below, assume the following variables were set in advance:

..  code-block:: python

    user1 = models.User("Foobar", service="AniList")
    user2 = models.User("Baz", service="Kitsu")

..  note::
    As there are no params to specify which service to use for each user,
    specify this information for both ``user1`` and ``user2`` by passing
    a tuple for each of these, containing (username, service).

One-off affinity calculations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is mainly used if you don't want the "base user"'s scores saved to a variable,
and you're only interested in the affinity with one person.

..  code-block:: python

    # Note that ``round`` can also be specified here if needed.
    affinity, shared = calculate_affinity(user1, user2)

    print(affinity)
    # 37.06659111674594
    print(shared)
    # 171

One-off comparison of scores
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is mainly used if you don't want the "base user"'s scores saved to a variable,
and you're only interested in getting a comparison of scores with another user.

..  code-block:: python

    print(comparison(user1, user2))

    # Note: this won't be prettified for you. Run it
    # through a prettifier if you want it to look nice.
    # {
    #     "1": [10, 6],
    #     "5": [8, 6],
    #     "6": [10, 7],
    #     "15": [7, 9],
    #     "16": [8, 5],
    #     ...
    # }
