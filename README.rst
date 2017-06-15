|forthebadge1| |forthebadge2| |forthebadge3| |forthebadge4|

malaffinity
===========

Calculate affinity between two MyAnimeList users

What is this?
-------------

Calculate the affinity (Pearson's Correlation \* 100) between a "base"
user and another user.

This script is meant to be used in bulk, where one user (the "base")'s
scores are compared against multiple people, but there's nothing
stopping you from using this as a one-off.

**In all files here, the "base" user refers to the user whose scores
other scores will be compared to (and affinities to said scores
calculated for). I don't have a better name to describe this, so please
bear with me.**

**In most cases, just assume that the "base" user is referring to you,
or the person who will be running your script**

Install
-------

::

    $ pip install malaffinity

Alternatively, download this repo and run:

::

    $ python setup.py install

Or copypasta the ``malaffinity`` directory to
Python:raw-latex:`\site`-packages and install the
`dependencies <#dependencies>`__ yourself.

Dependencies
------------

-  BeautifulSoup4
-  Requests

These should be installed when you install this script, so no need to
worry about them.

Usage
-----

1. Create an instance of the ``MALAffinity`` class, providing the param
   ``base_user``, and an optional ``round`` to it.

   -  The ``base_user`` is the username whose scores other scores will
      be compared to.
   -  Rounding of the final affinity is determined by the ``round``
      param. To round results, provide a number of decimal places to
      round to. For no rounding, specify ``False``
   -  *Note that the class can be initialised without the ``base_user``
      param, but a ``base_user`` **MUST** be passed to the ``init``
      function before any affinity calculations take place. (See
      `example 2 <#example-2>`__)*

2. Calculate affinity between the "base user" and another user by
   calling the ``calculate_affinity`` method with the username of the
   person you wish to calculate affinity with.

   -  This will return a tuple, containing the affinity, and the number
      of shared rated anime.

3. Calculate more affinities by repeating Step 2.

Examples
--------

Using ``ma`` as the name of the initialised class, because I can't think
of a better name that won't shadow anything that already/will exist(s).

Example 1
~~~~~~~~~

**Basic usage**

::

    >>> ma = MALAffinity("YOUR_USERNAME")

    >>> affinity, shared = ma.calculate_affinity("OTHER_USERNAME")

    >>> print(affinity)
    79.00545465639877
    >>> print(shared)
    82

Example 2
~~~~~~~~~

**Basic usage, but specifying a "base user" AFTER initialising the
class**

::

    >>> ma = MALAffinity()

    # This can be done anywhere as long as the place you're doing this from has access to `ma`.
    >>> ma.init("YOUR_USERNAME")

    >>> affinity, shared = ma.calculate_affinity("OTHER_USERNAME")

    >>> print(affinity)
    79.00545465639877
    >>> print(shared)
    82

Example 3
~~~~~~~~~

**Round affinities to two decimal places**

::

    >>> ma = MALAffinity("YOUR_USERNAME", round=2)

    >>> affinity = ma.calculate_affinity("OTHER_USERNAME")

    >>> print(affinity)
    79.01
    >>> print(shared)
    82

Example 4
~~~~~~~~~

**One-off affinity calculations**

Note that the ``calculate_affinity`` function is being used here - not
the method.

::

    >>> affinity = calculate_affinity("YOUR_USERNAME", "OTHER_USERNAME")

    >>> print(affinity)
    79.00545465639877
    >>> print(shared)
    82

*Don't use this if you're planning on calculating affinity again with
one of the users you've specified when doing this. It's better to create
an instance of the ``MALAffinity`` class with said user, and calculating
affinity with the other user(s) that way. That instance will hold said
users' scores, so they won't have to be retrieved again. See examples
1-3*

Handling exceptions
-------------------

Three types of exceptions can be raised while calculating affinities:

-  ``NoAffinityError``: Raised when either the shared rated anime
   between the base user and another user is less than 10, or the other
   user does not have any rated anime.
-  ``InvalidUsernameError``: Raised when username specified does not
   exist.
-  ``MALRateLimitExceededError``: Raised when MAL's blocking your
   request, because you're going over their rate limit of one request
   every two seconds. Slow down and try again.

Not much you can do about the first two, so you're best off giving up if
you run into one of those. The third, however, rarely happens if you
abide by the rate limit, but the following should happen in case it
does:

-  Halt the script for a few seconds. I recommend five.
-  Try again.
-  If you get roadblocked again, just give up. MAL obviously hates you.

I'm thinking about hardcoding the rate limit handling in, but I'm
worried about handling cases where MAL keeps blocking you - I don't want
to run into infinite loops. I'll look into this one day.

Feel free to use a loop though. Don't blame me if anything bad happens
because of it.

FAQ
---

**Q: Why didn't you use Numpy? You won't need to use Scipy, so there's
one less dependency to install...**

.. figure:: https://i.imgur.com/r1o1lS6.jpg
   :alt: 

So the correlation between two *exactly* identical bits of data is
99.999...8%?

Bullshit.

Concerns, problems, fixes, feedback, yada yada
----------------------------------------------

Contact me on
`Reddit <https://www.reddit.com/message/compose/?to=erkghlerngm44>`__ or
by `Email <mailto:erkghlerngm44@protonmail.com>`__, or create an
`issue <https://github.com/erkghlerngm44/malaffinity/issues>`__ or `pull
request <https://github.com/erkghlerngm44/malaffinity/pulls>`__.

The email I specified isn't my main one, and this isn't my main Github
account, so if you do use those services, send me a message on Reddit,
notifying me, otherwise you'll probably receive a reply weeks/months
after you contact me.

Legal stuff
-----------

Licensed under MIT. See ```LICENSE`` <LICENSE>`__ for more info.

As promised, one cute cat gif coming up!
----------------------------------------

.. figure:: https://i.imgur.com/sq42SnU.gif
   :alt: 

.. |forthebadge1| image:: http://forthebadge.com/images/badges/fuck-it-ship-it.svg
   :target: http://forthebadge.com
.. |forthebadge2| image:: http://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg
   :target: http://forthebadge.com
.. |forthebadge3| image:: http://forthebadge.com/images/badges/contains-cat-gifs.svg
   :target: http://forthebadge.com
.. |forthebadge4| image:: http://forthebadge.com/images/badges/built-with-love.svg
   :target: http://forthebadge.com
