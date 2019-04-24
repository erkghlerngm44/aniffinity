Changelog
=========


v0.2.0 (2019-04-24)
-------------------

* Make ``.calcs.pearson`` raise a ``ZeroDivisionError`` when the standard
  deviation of one/both sets of data is zero. This will be caught by
  ``Aniffinity.calculate_affinity`` and will then raise the usual
  ``NoAffinityError``, so scripts using this package will not need to
  be modified.
* Fix the faulty URL resolving in the resolving function. Valid usernames
  starting with "http" will now be handled correctly, instead of having an
  exception raised when no accompanying service is specified.
* Move the user/service resolving functions to ``resolver.py``, and rename
  these functions to more meaningful names. Additionally, make these functions
  non-protected, adding in official support for them.
* Change the repr of the ``Aniffinity`` class to make it more accurate.
* Update various docstrings to make more sense and be more accurate.
* Bump the version for the dependency ``json-api-doc`` to ``v0.7.x``.
* Handle the ``Decimal`` handling in ``.calcs.pearson`` better, by converting
  all of the values in each list to strings before passing them to
  ``decimal.Decimal``.
* Round affinity values by default to 10dp, so floating-point issues no longer
  need to be accounted for. This can be bypassed by the user, should they wish
  to do so.
* Don't convert the scores lists to ``list``-s to make them non-lazy, as this
  is already done.
* Allow the username & service to be specified as a string, in the
  form ``service:username``.
* Resolve the ``user`` before raising exceptions, allowing the exception
  messages to include the service as well as the username.
* Include the relevant usernames in the "standard deviation is zero"
  exception message in ``NoAffinityError``.


v0.1.2 (2019-04-15)
-------------------

* No code changes have been made. This release is to confirm that Travis has
  been fixed. (third time lucky, hopefully)


v0.1.1 (2019-04-15)
-------------------

* No code changes have been made. This release is to confirm that Travis has
  been fixed.


v0.1.0 (2019-04-15)
-------------------

* Discontinue Python 2 support.
* Rename this package to ``Aniffinity`` and replace all occurances with this.
* Add AniList and Kitsu endpoints and support.
* Rename exception ``MALRateLimitExceededError`` to ``RateLimitExceededError``.
* Add in a way to specify which service to use, either through the ``service``
  param, using a tuple with the username and service, or passing the URL to a
  users' profile.
* Create the ``User`` namedtuple.
* Make AniList the default service to use (as it's the most stable).
* Rename the ``affinity`` field in the ``Affinity`` namedtuple to ``value``.
* Rename exception ``InvalidUsernameError`` to ``InvalidUserError``.
* Force the ``_base_scores`` ``id`` keys to strings.
* Change the MyAnimeList API to an official-yet-unofficial semi-working one.
* Speed up the creation of the ``comparison`` dict.
* Add the service name to all service-specific exceptions.
* Add the ``wait_time`` arg to the ``Aniffinity`` class to slow down paginated
  requests.


For older changes, read the `changelog <https://github.com/erkghlerngm44/malaffinity/blob/master/CHANGELOG.rst>`__
at `erkghlerngm44/malaffinity <https://github.com/erkghlerngm44/malaffinity>`__.
