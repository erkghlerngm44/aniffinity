Changelog
=========


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
