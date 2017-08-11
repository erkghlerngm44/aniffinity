Examples
========


This section will show the various ways the ``MALAffinity`` class can be
initialised with ``Xinil`` (MAL creator)'s list, saved to the variable ``ma``,
and used to calculate affinity with ``Luna`` (MAL database admin).


Example 1: Basic Usage
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    ma = MALAffinity("Xinil")

    affinity, shared = ma.calculate_affinity("Luna")

    print(affinity)
    # 37.06659111674594
    print(shared)
    # 171


Example 2: Basic Usage, but specifying a "base user" after class initialisation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    ma = MALAffinity()

    # This can be done anywhere, as long as it has access to ``ma``,
    # but MUST be done before ``calculate_affinity`` or ``comparison``
    # are called
    ma.init("Xinil")

    affinity, shared = ma.calculate_affinity("Luna")

    print(affinity)
    # 37.06659111674594
    print(shared)
    # 171


Example 3: Round affinities to two decimal places
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    ma = MALAffinity("Xinil", round=2)

    affinity, shared = ma.calculate_affinity("Luna")

    print(affinity)
    # 37.07
    print(shared)
    # 171


Example 4: One-off affinity calculations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Note that ``round`` can also be specified here if needed.
    affinity, shared = calculate_affinity("Xinil", "Luna")

    print(affinity)
    # 37.06659111674594
    print(shared)
    # 171

.. note:: Don't use this if you're planning on calculating affinity again with one of
          the users you've specified when using this.

          It's better to create an instance of the ``MALAffinity`` class with said user,
          and calculating affinity with the other user(s) that way.

          That instance will hold said users' scores, so they won't have to be retrieved
          again. See examples 1-3.
