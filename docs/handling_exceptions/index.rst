Handling Exceptions
===================


.. note:: As of v2.0.0, these exceptions are now contained in the ``exceptions`` file.
          Make sure to reference them properly if you'll be going down this path.

Three types of exceptions can be raised while calculating affinities:

* ``NoAffinityError``: Raised when either the shared rated anime between the base user
  and another user is less than 10, or the other user does not have any rated anime.
* ``InvalidUsernameError``: Raised when username specified does not exist.
* ``MALRateLimitExceededError``: Raised when MAL's blocking your request, because you're
  going over their rate limit of one request every two seconds. Slow down and try again.

Not much you can do about the first two, so you're best off giving up if you
run into one of those. The third, however, rarely happens if you abide by the
rate limit, but the following should happen in case it does:

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
