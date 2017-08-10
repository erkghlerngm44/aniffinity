Contributing
============


In the unlikely event that someone finds this package, and in the even unlikelier
event that someone wants to contribute,
send me a `pull request <https://github.com/erkghlerngm44/malaffinity/pulls>`__
or create an `issue <https://github.com/erkghlerngm44/malaffinity/issues>`__.

.. note:: This isn't my main GitHub account, so :doc:`contact` me on Reddit if you do
          use those services, otherwise I probably won't see it for weeks/months.


How to Contribute
-----------------

* Fork the `repo <https://github.com/erkghlerngm44/malaffinity>`__.
* ``git clone https://github.com/YOUR_USERNAME/malaffinity.git``
* ``cd malaffinity``
* ``git checkout -b new_feature``
* Make changes.
* ``git commit -am "Commit message"``
* ``git push origin new_feature``
* Navigate to https://github.com/YOUR_USERNAME/malaffinity
* Create a pull request.


Conventions
-----------

This package aims to follow `PEP8 <https://www.python.org/dev/peps/pep-0008/>`__
and `PEP257 <https://www.python.org/dev/peps/pep-0257/>`__, and also aims to
have 100% coverage in its tests. The ``flake8``, ``pydocstyle`` and ``coverage``
packages are used to make sure these are being adhered to.

The ``# noqa`` (for PEP8, PEP257) and ``# pragma: no cover`` (for coverage)
comments may be added in to sections of code where these guidelines can't be
adhered to, for some reason.

Please note the following additional conventions, which can be found in the code:

Code Layout
~~~~~~~~~~~

* Two blank lines between the top-level docstring and the imports.
* Two blank lines between the imports and the code itself.

Documentation and Docstrings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See :ref:`build-docs` for info on how to build the docs.

* Both are written in reST, using `Sphinx <http://www.sphinx-doc.org/>`__.

Tests
~~~~~

Tests should ideally cover all code in the package (giving 100% coverage),
unless told not to test specific sections (in which case the offending parts
should have the appropriate "ignore" comments next to them).
To run tests, see :ref:`run-tests`.

* Tests use the ``DUMMY_LIST`` (found in
  `tests/mocks/__init__.py <https://github.com/erkghlerngm44/malaffinity/blob/master/tests/mocks/__init__.py>`__)
  where possible, to reduce the number of requests sent over to MAL. This should
  ideally be used anywhere where the aim of the test is NOT to test that a users'
  list can be retrieved from the site.
* The user ``testmalacct0000`` has been created to be used by tests that check
  if a users' list can be retrieved from MAL. The list and scores should not change,
  so any constants that can be extracted from the list and be tested against should
  be added to
  `tests/const.py <https://github.com/erkghlerngm44/malaffinity/blob/master/tests/const.py>`__.
* A mock ``malaffinity.endpoints.myanimelist`` function may be added to
  ``tests/mocks/__init__.py``, if the ``DUMMY_LIST`` needs to be modified
  in any way for a test. If this is not the case, the endpoint should be patched
  with ``mocks.mock_myanimelist_endpoint``, which will just return the list.


That's it, I guess. :doc:`contact` me if you need anything.

.. figure:: https://i.imgur.com/gEOKk0P.jpg
   :alt:
