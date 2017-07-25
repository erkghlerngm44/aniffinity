Handling Exceptions
===================


The types of exceptions that can be raised when calculating affinities are:

.. autoclass:: malaffinity.exceptions.NoAffinityError

.. autoclass:: malaffinity.exceptions.InvalidUsernameError

.. autoclass:: malaffinity.exceptions.MALRateLimitExceededError


----


:class:`.exceptions.NoAffinityError` and :class:`.exceptions.InvalidUsernameError`
are descendants of:

.. autoclass:: malaffinity.exceptions.MALAffinityException

which means if that base exception gets raised, you know you won't be able to
calculate affinity with that person for some reason, so your script should
just move on.


----


:class:`.exceptions.MALRateLimitExceededError` rarely gets raised if you abide
by the rate limit of one request every two seconds. If it does get raised,
the following should happen:

* Halt the script for a few seconds. I recommend five.
* Try again.
* If you get roadblocked again, just give up. MAL obviously hates you.

This can be achieved via something along these lines:

.. code-block:: python

    success = False

    for _ in range(2):
        try:
            affinity, shared = ma.calculate_affinity("OTHER_USERNAME")

        # Rate limit exceeded. Halt your script and try again
        except malaffinity.exceptions.MALRateLimitExceededError:
            time.sleep(5)
            continue

        # Any other malaffinity exception.
        # Affinity can't be calculated for some reason.
        # ``MALAffinityException`` is the base exception class for
        # all malaffinity exceptions
        except malaffinity.exceptions.MALAffinityException:
            break

        # General exceptions not covered by malaffinity. Not sure what
        # you could do here. Feel free to handle however you like
        except Exception as e:
            # ...

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
