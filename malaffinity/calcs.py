from statistics import pstdev, mean
from decimal import Decimal


# Original code: https://stackoverflow.com/a/17389980
def pearson(x, y):
    # Fix floating point shit
    x = [Decimal(i) for i in x]
    y = [Decimal(j) for j in y]

    sx = []
    sy = []

    # Calculate mean and stdev now so we don't have to calculate
    # it every time we come across another value.
    # Size and content of `x` and `y` shouldn't change so this should be fine.
    mx = Decimal(mean(x))
    my = Decimal(mean(y))

    stdx = Decimal(pstdev(x))
    stdy = Decimal(pstdev(y))

    for i in x:
        sx.append((i - mx) / stdx)

    for j in y:
        sy.append((j - my) / stdy)

    r = sum([i * j for i, j in zip(sx, sy)]) / len(x)

    return float(r)
