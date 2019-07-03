import random

import numpy

import aniffinity


# TODO: Numpy to extras_require.test


def test_general_calcs__pearson():
    """
    Generate two pseudo-random samples and compare PMCC from .calcs and numpy.
    """
    sample1 = [random.randrange(10) for _ in range(100)]
    sample2 = [random.randrange(10) for _ in range(100)]

    calcs_pearson = aniffinity.calcs.pearson(sample1, sample2)
    numpy_pearson = numpy.asscalar(numpy.corrcoef(sample1, sample2)[0, 1])

    # 10dp accuracy should be more than enough.
    assert round(calcs_pearson, 10) == round(numpy_pearson, 10)
