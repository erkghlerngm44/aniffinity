"""malaffinity calcs."""


from decimal import Decimal
from statistics import mean

from .exceptions import NoAffinityError


# Original code:
# https://github.com/scipy/scipy/blob/v0.19.1/scipy/stats/stats.py#L2975-L3021
# (Translated into normal python)
def pearson(x, y):
    """
    Pearson's correlation implementation without scipy or numpy.

    :param list x: Dataset x
    :param list y: Dataset y
    :return: Population pearson correlation coefficient
    :rtype: float
    """
    mx = Decimal(mean(x))
    my = Decimal(mean(y))

    xm = [Decimal(i) - mx for i in x]
    ym = [Decimal(j) - my for j in y]

    sx = [i ** 2 for i in xm]
    sy = [j ** 2 for j in ym]

    num = sum([a * b for a, b in zip(xm, ym)])
    den = Decimal(sum(sx) * sum(sy)).sqrt()

    # Stdev of one (or both) of the scores is zero if the
    # denominator is zero. Dividing by zero is impossible, so
    # just check if it is zero before we tell it to divide.
    if den == 0.0:
        # TODO: Better message
        raise NoAffinityError("Standard deviation of either "
                              "users' scores is zero")

    return float(num / den)
