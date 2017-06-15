from statistics import pstdev, mean


# Original code: https://stackoverflow.com/a/17389980
def pearson(x, y):
    sx = []
    sy = []

    # Calculate mean and stdev now so we don't have to calculate
    # it every time we come across another value.
    # Size and content of `x` and `y` shouldn't change so this should be fine.
    mx = mean(x)
    my = mean(y)

    stdx = pstdev(x)
    stdy = pstdev(y)

    for i in x:
        sx.append((i - mx) / stdx)

    for j in y:
        sy.append((j - my) / stdy)

    return sum([i * j for i, j in zip(sx, sy)]) / len(x)
