Examples
========


Example 1: Basic Usage
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    ma = MALAffinity("YOUR_USERNAME")

    affinity, shared = ma.calculate_affinity("OTHER_USERNAME")

    print(affinity)
    # 79.00545465639877
    print(shared)
    # 82


Example 2: Basic Usage, but specifying a "base user" after class initialisation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    ma = MALAffinity()

    ma.init("YOUR_USERNAME")

    affinity, shared = ma.calculate_affinity("OTHER_USERNAME")

    print(affinity)
    # 79.00545465639877
    print(shared)
    # 82


Example 3: Round affinities to two decimal places
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    ma = MALAffinity("YOUR_USERNAME")

    affinity, shared = ma.calculate_affinity("OTHER_USERNAME")

    print(affinity)
    # 79.01
    print(shared)
    # 82


Example 4: One-off affinity calculations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    affinity, shared = calculate_affinity("YOUR_USERNAME", "OTHER_USERNAME")

    print(affinity)
    # 79.00545465639877
    print(shared)
    # 82

.. note:: Don't use this if you're planning on calculating affinity again with one of
          the users you've specified when using this.

          It's better to create an instance of the ``MALAffinity`` class with said user,
          and calculating affinity with the other user(s) that way.

          That instance will hold said users' scores, so they won't have to be retrieved
          again. See examples 1-3.