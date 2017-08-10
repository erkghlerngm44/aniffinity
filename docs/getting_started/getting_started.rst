Getting Started
===============


Install
-------

.. code-block:: bash

    $ pip install malaffinity

Alternatively, download this repo and run:

.. code-block:: bash

    $ python setup.py install

To use the development version (please don't), run:

.. code-block:: bash

    $ pip install --upgrade https://github.com/erkghlerngm44/malaffinity/archive/master.zip


Dependencies
------------

* ``BeautifulSoup4``
* ``lxml``
* ``Requests``

These should be installed when you install this package, so no need to worry about them.

``lxml`` is a bit wonky sometimes. If install fails:

.. code-block:: bash

    $ pip install --upgrade pip
    $ pip install --upgrade lxml

If all else fails and you're on Windows, download the
`wheel <http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml>`__
yourself and:

.. code-block:: bash

    $ pip install /path/to/wheel.whl


Development
-----------

This section demonstrates how documentation can be built and tests run.
These should not be used unless you're contributing to the package.

.. _build-docs:

Documentation
~~~~~~~~~~~~~

To install the dependencies needed to build the docs, run:

.. code-block:: bash

    $ pip install .[doc]

The docs can then be built by navigating to the ``docs``
directory, and running:

.. code-block:: bash

    $ make html

The built docs will now be in ``./_build/html``. You can either run them
by clicking and viewing them, or by running a server in that directory,
which you can view in your browser.

.. note:: Any warnings that show up when building will be interpreted as errors
          when the tests get run on Travis, which will cause the build to fail.
          You'll want to make sure these are taken care of.

.. _run-tests:

Test Suite
~~~~~~~~~~

To install the dependencies needed for the test suite, run:

.. code-block:: bash

    $ pip install .[test]

It is advised to run the test suite through ``coverage``, so a
coverage report can be generated as well. To do this, run:

.. code-block:: bash

    $ coverage run --source malaffinity setup.py test

The tests should then run. You can view the coverage report by running:

.. code-block:: bash

    $ coverage report

You should be aiming for 100% coverage when running the tests.
