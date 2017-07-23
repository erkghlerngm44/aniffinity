"""malaffinity calcs."""


from decimal import Decimal
from statistics import mean


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

    return float(num / den)
