"""aniffinity models."""


from collections import namedtuple


Affinity = namedtuple("Affinity", ["affinity", "shared"])
User = namedtuple("User", ["username", "service"])
