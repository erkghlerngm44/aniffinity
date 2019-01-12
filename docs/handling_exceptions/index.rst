Handling Exceptions
===================


Which exceptions can be raised?
-------------------------------

The types of exceptions that can be raised when calculating affinities are:

..  autoexception:: aniffinity.exceptions.NoAffinityError

..  autoexception:: aniffinity.exceptions.InvalidUserError

..  autoexception:: aniffinity.exceptions.RateLimitExceededError

If you're planning on using this package in an automated or unsupervised script,
you'll want to make sure you account for these getting raised, as not doing so
will mean you'll be bumping into a lot of exceptions, unless you can guarantee
none of the above will get raised. For an example snippet of code that can
demonstrate this, see :ref:`exception-handling-snippet`.


----


AniffinityException
-------------------

:exc:`.exceptions.NoAffinityError` and :exc:`.exceptions.InvalidUserError`
are descendants of:

..  autoexception:: aniffinity.exceptions.AniffinityException

which means if that base exception gets raised, you know you won't be able to
calculate affinity with that person for some reason, so your script should
just move on.


----


What to do if RateLimitExceededError gets raised
------------------------------------------------

:exc:`.exceptions.RateLimitExceededError` rarely gets raised if you abide
by the rate limits of the services you are using. This may be something like
one request a second, or one request every two seconds. If it does get raised,
the following should happen:

* Halt the script for a few seconds. I recommend five.
* Try again.
* If you get roadblocked again, just give up.

..  note::
    The name of the service ratelimiting you will be in the exception
    message, should this be of any use to you.


----


..  _exception-handling-snippet:

Exception Handling Snippet
--------------------------

The above can be demonstrated via something along these lines. Do note that
this probably isn't the best method, but it works.

This should be placed in the section where you are attempting to calculate
affinity, or get a comparison, with another user.

..  code-block:: python

    time.sleep(2)

    success = False

    for _ in range(2):
        try:
            affinity, shared = af.calculate_affinity("Baz", service="Kitsu")

        # Rate limit exceeded. Halt your script and try again
        except aniffinity.exceptions.RateLimitExceededError:
            time.sleep(5)
            continue

        # Any other aniffinity exception.
        # Affinity can't be calculated for some reason.
        # ``AniffinityException`` is the base exception class for
        # all aniffinity exceptions
        except aniffinity.exceptions.AniffinityException:
            break

        # Exceptions not covered by aniffinity. Not sure what
        # you could do here. Feel free to handle however you like
        except Exception as e:
            print("Exception: `{}`".format(e))
            break

        # Success!
        else:
            success = True
            break

    # ``success`` will still be ``False`` if affinity can't been calculated.
    # If this is the case, you'll want to stop doing anything with this person
    # and move onto the next, so use the statement that will best accomplish this,
    # given the layout of your script
    if not success:
        return

    # Assume from here on that ``affinity`` and ``shared`` hold their corresponding
    # values, and feel free to do whatever you want with them

Feel free to use a ``while`` loop instead of the above. I'm just a bit wary of them,
in case something happens and the script gets stuck in an infinite loop. Your choice.

To see the above snippet in action, visit
`erkghlerngm44/r-anime-soulmate-finder <https://github.com/erkghlerngm44/r-anime-soulmate-finder/blob/v4.2.0/soulmate_finder/__main__.py#L80-L113>`__.
