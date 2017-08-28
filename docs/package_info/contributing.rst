Contributing
============


In the unlikely event that someone finds this package, and in the even unlikelier
event that someone wants to contribute,
send me a `pull request <https://github.com/erkghlerngm44/malaffinity/pulls>`__
or create an `issue <https://github.com/erkghlerngm44/malaffinity/issues>`__.

.. note:: Please :doc:`contact` and notify me if you use the above, as this isn't my
          main GitHub account, so I won't be checking it that much. I'll probably see
          it weeks/months later if you don't.

Feel free to use those for anything regarding the package, they're there to be used,
I guess.


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


Notes and Stuff
---------------

I had a whole section on conventions to follow and other stuff, but that
seemed a bit weird, so I just scratched it. If someone out there wants to
contribute to this package in any way, shape or form, have at it. I'd prefer
the changes to be non-breaking (i.e. existing functionality is not affected),
but breaking changes are still welcome.

I only ask that you try to adhere to :pep:`8` and :pep:`257` (if you can), and
try to achieve 100% coverage in tests (again, if you can). For information on how
to check if you're adhering to those conventions, see :ref:`conventions`.

For information on how to build docs and run tests, see :ref:`build-docs` and
:ref:`run-tests` respectively.

This package is based off a
`class <https://github.com/erkghlerngm44/r-anime-soulmate-finder/blob/v1.0.0/affinity_gatherer.py#L25-L112>`__
I wrote for ``erkghlerngm44/r-anime-soulmate-finder``, and while I have tried to
modify it for general uses (and tried to clean the bad code up a bit), there are
still a few iffy bits around. I'd appreciate any PRs to fix this up.

I think the package is mostly complete, so my main focus right now is making it
as fast as can-be, as every fraction of a second counts when you're using this
to calculate affinity with tens of thousands of people. PRs regarding this are
especially welcome.


That's it, I guess. :doc:`contact` me if you need help or anything.

.. figure:: https://i.imgur.com/gEOKk0P.jpg
   :alt:
