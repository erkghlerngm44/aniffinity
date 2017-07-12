|forthebadge1| |forthebadge2| |forthebadge3|


malaffinity
===========

|travis| |coveralls| |rtd|

Calculate affinity between MyAnimeList users


What is this?
-------------

Calculate the affinity (Pearson's Correlation \* 100) between a "base"
user and another user. Refer to the `docs <#documentation>`__ for more info.


Install
-------

.. code-block:: bash

    pip install malaffinity


Dependencies
------------

* BeautifulSoup4
* lxml
* Requests


Examples
--------

.. code-block:: python

    from malaffinity import MALAffinity

    ma = MALAffinity("YOUR_USERNAME")

    affinity, shared = ma.calculate_affinity("OTHER_USERNAME")

    print(affinity)
    # 79.00545465639877
    print(shared)
    # 82

.. code-block:: python

    import malaffinity

    affinity, shared = malaffinity.calculate_affinity("YOUR_USERNAME", "OTHER_USERNAME")

    # ...


Documentation
-------------

Documentation at https://malaffinity.readthedocs.io


Legal Stuff
-----------

Licensed under MIT. See `LICENSE <LICENSE>`__ for more info.


Cat Gif
-------

.. figure:: https://i.imgur.com/sq42SnU.gif
   :alt:


.. |forthebadge1| image:: http://forthebadge.com/images/badges/fuck-it-ship-it.svg
   :target: http://forthebadge.com
.. |forthebadge2| image:: http://forthebadge.com/images/badges/contains-cat-gifs.svg
   :target: http://forthebadge.com
.. |forthebadge3| image:: http://forthebadge.com/images/badges/built-with-love.svg
   :target: http://forthebadge.com

.. |travis| image:: https://travis-ci.org/erkghlerngm44/malaffinity.svg?branch=master
   :target: https://travis-ci.org/erkghlerngm44/malaffinity?branch=master
.. |coveralls| image:: https://coveralls.io/repos/github/erkghlerngm44/malaffinity/badge.svg?branch=master
   :target: https://coveralls.io/github/erkghlerngm44/malaffinity?branch=master
.. |rtd| image:: https://readthedocs.org/projects/malaffinity/badge/?version=latest
   :target: http://malaffinity.readthedocs.io/en/latest/
