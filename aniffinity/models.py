"""aniffinity models."""


from collections import namedtuple


Affinity = namedtuple("Affinity", ["value", "shared"])
User = namedtuple("User", ["username", "service"])
