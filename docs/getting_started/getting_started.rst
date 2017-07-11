Getting Started
===============


Install
-------

.. code-block:: bash

    pip install malaffinity

Alternatively, download this repo and run:

.. code-block:: bash

    python setup.py install

To use the development version (please don't), run:

.. code-block:: bash

    pip install --upgrade https://github.com/erkghlerngm44/malaffinity/archive/master.zip


Dependencies
------------

* ``BeautifulSoup4``
* ``lxml``
* ``Requests``

These should be installed when you install this package, so no need to worry about them.

``lxml`` is a bit wonky sometimes. If install fails:

.. code-block:: bash

    pip install --upgrade pip
    pip install --upgrade lxml

If all else fails and you're on Windows, download the
`wheel <http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml>`__
yourself and:

.. code-block:: bash

    pip install /path/to/wheel.whl
