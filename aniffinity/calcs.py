"""aniffinity calcs."""


from decimal import Decimal, DivisionByZero, InvalidOperation
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
    x = [Decimal(str(i)) for i in x]
    y = [Decimal(str(j)) for j in y]

    mx = mean(x)
    my = mean(y)

    xm = [i - mx for i in x]
    ym = [j - my for j in y]

    sx = [i ** 2 for i in xm]
    sy = [j ** 2 for j in ym]

    num = sum(a * b for a, b in zip(xm, ym))
    den = (sum(sx) * sum(sy)).sqrt()

    # `decimal` module handles division by zero weirdly, raising different
    # exceptions if either the denominator is zero, or if the numerator and
    # denominator are zero. As `decimal` is only used internally within
    # this function, with normal floats going in and out, we should treat
    # this to behave the same way if one were to do `n/0` (n >= 0) in normal
    # python. The best way to accomplish this is to catch the
    # `decimal`-specific exceptions and throw the generic `ZeroDivisionError`.
    try:
        return float(num / den)
    except (DivisionByZero, InvalidOperation):
        raise ZeroDivisionError("division by zero")
