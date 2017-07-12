Changelog
=========


v2.2.0 (2017-07-??)
-------------------

* Create the ``comparison`` method, and have ``calculate_affinity`` use that
  to retrieve both sets of scores
* Rewrite the docstrings in the ``MALAffinity`` class, to be more useful and
  more compliant with le Sphinx syntax
* Add docs to the project, and have them hosted on readthedocs.io
* Add (badly written) tests, and hook them up to Travis and Coveralls
* Get rid of Markdown altogether, and rewrite the README, as most of the info
  is now in the docs


v2.1.0 (2017-07-08)
-------------------

* Fix a typo in the ``calcs.pearson`` docstring, which incorrectly said
  the ``:rtype`` was a bool
* Use the ``find_all`` BS4 method instead of ``findAll``
* Fix a typo in the "Shared rated anime count is less than required" exception
  message, which incorrectly stated that the minimum required was ten, when it's
  actually eleven
* Add a docstring for ``.__about__``
* Add a docstring for ``MALAffinity._retrieve_scores``
* Remove the useless kwargs from ``MALAffinity._retrieve_scores``
* Make the ``statistics`` pypi package a requirement for all Python versions
* Add a ``__repr__`` to the ``MALAffinity`` class
* Move the ``_retrieve_scores`` method in the ``MALAffinity`` class
  to its own file (``endpoints.py``)
* Create a ``const.py`` file for constants
* Add a ``# NOQA`` comment to the ``.__about__`` imports in ``__init__``, to suppress
  the F401 flake8 warnings


v2.0.0 (2017-06-20)
-------------------

* Move the MALAffinity class to its own separate file (``malaffinity.malaffinity``)
  and import that into the ``malaffinity`` namespace via ``__init__``
* Move exceptions to its own separate file (``malaffinity.exceptions``)
* Modify description of the package slightly ("Calculate affinity between
  **two** MyAnimeList users" => "Calculate affinity between MyAnimeList users")
* Add exception message for when the standard deviation of one of the two users'
  scores is zero, and affinity can't be calculated
* Create the base ``MALAffinityException`` class and derive all malaffinity
  exceptions from that
* Add docstrings for ``malaffinity.calcs``
* Modify docstrings to remove typos and unnecessary information,
  and reword some sections
* Reword exception messages to be more useful
* Have the ``init`` method return ``self``, to allow for
  `chaining <https://en.wikipedia.org/wiki/Method_chaining>`__
* Make all code PEP8-compliant (ignoring F401 for meta reasons)


v1.1.0 (2017-06-15)
-------------------

* Remove scipy (and numpy) as a dependency. Pearson's correlation code is now in
  ``malaffinity.calcs`` and stdev checking is handled by the ``statistics`` module
* Use ``lxml`` for XML parsing, instead of the default ``html.parser``
* Add return types for components inside the return tuple into the docstring


v1.0.3 (2017-05-05)
-------------------

* Change 'base user has been set' testing to also check if ``self._base_scores``
  has been set as well
* Use ``zip`` to create the ``scores1`` and ``scores2`` arrays that calculations are done with
* Check if the standard deviation of ``scores1`` or ``scores2`` is zero,
  and thrown an error if so
* Use ``scipy.asscalar`` as opposed to ``.item()`` for numpy.float64 => float conversion


v1.0.2 (2017-04-17)
-------------------

* Better handling for numpy.float64 => float conversion
* Update docstrings to include types

v1.0.1 (2017-04-12)
-------------------

* Don't count rated anime on a user's PTW. MAL didn't count this,
  so our affinity values were a bit off when a user did this

v1.0.0 (2017-04-09)
-------------------
* Konnichiwa, sekai!
