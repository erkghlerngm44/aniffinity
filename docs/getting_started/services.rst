Services
========


..  _available-services:

Available Services
------------------

The following anime list services can be used with Aniffinity:

* `Anilist <https://anilist.co>`__

  * **Aliases**: ``AL``, ``A``

* `Kitsu <https://kitsu.io>`__ [1]_ [2]_

  * **Aliases**: ``K``

* `MyAnimeList <https://myanimelist.net>`__ [3]_

  * **Aliases**: ``MAL``, ``M``

..  note::
    Do note, this package is designed for cross-service compatibility.
    You are able to, say, calculate affinity (or compare scores) with
    one user on AniList and another on Kitsu, for example.

    There's nothing restricting you to stick with users from one
    service, unless that's your intention.


----


..  [1]
    Incredibly slow, due to constraints by the service API itself
    and not this package. Nothing I can do about it, sorry.

..  [2]
    When passing a username to Kitsu, use the "slug" (from the
    "profile url") instead of the "display name" as "display name"s
    aren't unique in Kitsu.
    The "slug" refers to this part of the user's profile URL:
    ``https://kitsu.io/users/<SLUG>``.

..  [3]
    The MyAnimeList API being used is undocumented by them (probably
    because it's only meant to be used internally) and may change at
    any time without warning. Not much I can do about that, if MAL
    decides to cough up a real API in the (distant) future, I'll
    change it over to that.
    **Until then, if this API fails and I can't fix it, I'll just
    remove MyAnimeList support altogether.**
