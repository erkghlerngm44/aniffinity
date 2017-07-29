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


Test Suite
----------

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

Though, you might want to consider letting Travis and Coveralls handle
all that. Just send over a PR and let it do its thing. That's what they're
there for, right?
