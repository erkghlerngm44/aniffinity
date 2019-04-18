|ftb1| |ftb2| |ftb3|


aniffinity
==========

|pypi| |travis| |rtd|

*"An-knee-fin-knee-tea"*.

Calculate affinity between anime list users.


What is this?
-------------

Calculate affinity between a user and another user on anime list
services. Refer to the `docs <#documentation>`__ for more info.


Install
-------

..  code-block:: bash

    pip install aniffinity


Dependencies
------------

* json-api-doc
* requests


Example Usage
-------------

..  code-block:: python

    from aniffinity import Aniffinity

    af = Aniffinity("Xinil", base_service="MyAnimeList")

    affinity, shared = af.calculate_affinity("Josh", service="AniList")

    print(affinity)
    # 32.15230953451651
    print(shared)
    # 31


Available Services
------------------

* `AniList <https://anilist.co>`__
* `Kitsu <https://kitsu.io>`__
* `MyAnimeList <https://myanimelist.net>`__

For more info, read the `docs <#documentation>`__.


Documentation
-------------

Documentation at https://aniffinity.readthedocs.io


Legal Stuff
-----------

Licensed under MIT. See `LICENSE <LICENSE>`__ for more info.


Cat Gif
-------

..  figure:: https://i.imgur.com/sq42SnU.gif
    :alt:


..  |ftb1| image:: http://forthebadge.com/images/badges/made-with-python.svg
    :target: http://forthebadge.com
..  |ftb2| image:: http://forthebadge.com/images/badges/contains-cat-gifs.svg
    :target: http://forthebadge.com
..  |ftb3| image:: http://forthebadge.com/images/badges/built-with-love.svg
    :target: http://forthebadge.com

..  |pypi| image:: https://img.shields.io/pypi/v/aniffinity.svg
    :target: https://pypi.org/project/aniffinity/
..  |travis| image:: https://travis-ci.org/erkghlerngm44/aniffinity.svg?branch=master
    :target: https://travis-ci.org/erkghlerngm44/aniffinity?branch=master
..  |rtd| image:: https://readthedocs.org/projects/aniffinity/badge/?version=latest
    :target: https://aniffinity.readthedocs.io/en/latest/
