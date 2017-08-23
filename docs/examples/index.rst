Examples
========


This section will show the various ways the ``MALAffinity`` class can be
initialised with the user ``Xinil`` (MAL creator), and used to calculate
affinity or get a comparison with the user ``Luna`` (MAL database admin).


----


Initialising the Class
----------------------

The class can be initialised in either one of two ways:

Method 1: Normal initialisation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The class is initialised, with a "base user" passed as an argument to ``MALAffinity``.

.. code-block:: python

    ma = MALAffinity("Xinil")

Method 2: Specifying a "base user" after initialisation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The class is initialised, with a "base user" passed sometime later
after initialisation, which may be useful in scripts where creating
globals inside functions or classes or different files is a pain.

.. code-block:: python

    ma = MALAffinity()

    # This can be done anywhere, as long as it has access to ``ma``,
    # but MUST be done before ``calculate_affinity`` or ``comparison``
    # are called
    ma.init("Xinil")

Rounding of the final affinity value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note:: This doesn't affect :meth:`.comparison`, so don't worry about
          it if you're just using that.

Do note that the class also has a ``round`` parameter, which is
used to round the final affinity value. This must be specified at class
initialisation if wanted, as it isn't available in :meth:`.init`.
A value for this can be passed as follows:

.. code-block:: python

    # To round to two decimal places
    ma = MALAffinity("Xinil", round=2)

    # Alternatively, the following can also work, if you decide to follow
    # method 2 for initialising the class
    ma = MALAffinity(round=2)
    ma.init("Xinil")


-----


Doing Things with the Initialised Class
---------------------------------------

The initialised class, now stored in ``ma``, can now perform the following actions:

Calculate affinity with a user
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note:: Values may or may not be rounded, depending on the value you passed
          for the ``round`` parameter at class initialisation.

.. code-block:: python

    print(ma.calculate_affinity("Luna"))
    # Affinity(affinity=37.06659111674594, shared=171)

Note that what is being returned is a namedtuple, containing the affinity and shared
rated anime. This can be separated into different variables as follows:

.. code-block:: python

    affinity, shared = ma.calculate_affinity("Luna")

    print(affinity)
    # 37.06659111674594
    print(shared)
    # 171

Alternatively, the following also works (as this is a namedtuple):

.. code-block:: python

    affinity = ma.calculate_affinity("Luna")

    print(affinity.affinity)
    # 37.06659111674594
    print(affinity.shared)
    # 171

Comparing scores with a user
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    comparison = ma.comparison("Luna")

    print(comparison)
    # Note: this won't be prettified for you. Run it
    # through a prettifier if you want it to look nice.
    # {
    #     1: [10, 6],
    #     5: [8, 6],
    #     6: [10, 7],
    #     15: [7, 9],
    #     16: [8, 5],
    #     ...
    # }

This can now be manipulated in whatever way you like, to suit your needs.
I like to just get the arrays on their own, zip them and plot a graph with it.


Extras
------

One-off affinity calculations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is mainly used if you don't want the "base user"'s scores saved to a variable,
and you're only interested in the affinity with one person.

.. warning:: This sends two GET requests over to MAL in a short amount of time,
             with no wait inbetween them. If you're getting in trouble with them
             for breaking their rate limit, you might have a few problems getting
             this to work without ``MALRateLimitExceededError`` getting raised.

.. code-block:: python

    # Note that ``round`` can also be specified here if needed.
    affinity, shared = calculate_affinity("Xinil", "Luna")

    print(affinity)
    # 37.06659111674594
    print(shared)
    # 171


    # Alternatively...
    affinity = calculate_affinity("Xinil", "Luna")

    print(affinity.affinity)
    # 37.06659111674594
    print(affinity.shared)
    # 171

.. note:: Don't use this if you're planning on calculating affinity again with one of
          the users you've specified when using this.

          It's better to create an instance of the ``MALAffinity`` class with said user,
          and calculating affinity with the other user(s) that way.

          That instance will hold said users' scores, so they won't have to be retrieved
          again. See the other examples.

One-off comparison of scores
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is mainly used if you don't want the "base user"'s scores saved to a variable,
and you're only interested in getting a comparison of scores with another user.

.. warning:: This sends two GET requests over to MAL in a short amount of time,
             with no wait inbetween them. If you're getting in trouble with them
             for breaking their rate limit, you might have a few problems getting
             this to work without ``MALRateLimitExceededError`` getting raised.

.. code-block:: python

    print(comparison("Xinil", "Luna"))

    # Note: this won't be prettified for you. Run it
    # through a prettifier if you want it to look nice.
    # {
    #     1: [10, 6],
    #     5: [8, 6],
    #     6: [10, 7],
    #     15: [7, 9],
    #     16: [8, 5],
    #     ...
    # }
