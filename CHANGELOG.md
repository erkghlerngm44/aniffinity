# Changelog


## [UNRELEASED] v2.1.0 (2017-07-**??**)
* Fix a typo in the `calcs.pearson` docstring, which incorrectly said 
  the `:rtype` was a bool
* Use the `find_all` BS4 method instead of `findAll`
  * No actual changes to the inner workings of the script. It just looks nicer
* Fix a typo in the "Shared rated anime count is less than required" exception
  message, which incorrectly stated that the minimum required was ten, when it's
  actually eleven
* Add a docstring for `.__about__`
* Add a docstring for `MALAffinity._retrieve_scores`
* Remove the useless kwargs from `MALAffinity._retrieve_scores`
* Make the `statistics` pypi package a requirement for all Python versions
* Add a `__repr__` to the `MALAffinity` class

**TODO:**
* Proper Sphinx docstrings
 
## v2.0.0 (2017-06-20)
* Move the MALAffinity class to its own separate file (`malaffinity.malaffinity`)
  and import that into the `malaffinity` namespace via `__init__`
* Move exceptions to its own separate file (`malaffinity.exceptions`)
  * These won't be imported into the `malaffinity` namespace, so all references
    to them will have to be changed to point to the `exceptions` file
* Modify description of the package slightly
  * "Calculate affinity between **two** MyAnimeList users" =>
    "Calculate affinity between MyAnimeList users"
* Add exception message for when the standard deviation of one of the two users'
  scores is zero, and affinity can't be calculated
* Create the base `MALAffinityException` class and derive all malaffinity
  exceptions from that
* Add docstrings for `malaffinity.calcs`
* Modify docstrings to remove typos and unnecessary information, 
  and reword some sections
* Reword exception messages to be more useful
* Have the `init` method return `self`, to allow for 
  [chaining](https://en.wikipedia.org/wiki/Method_chaining)
* Make all code PEP8-compliant (ignoring F401 for meta reasons)

## v1.1.0 (2017-06-15)
* Remove scipy (and numpy) as a dependency
  * Pearson's correlation code is now in `malaffinity.calcs` and stdev checking is handled
    by the `statistics` module
* Use `lxml` for XML parsing, instead of the default `html.parser`
* Add return types for components inside the return tuple into the docstring

## v1.0.3 (2017-05-05)
* Change 'base user has been set' testing to also check if `self._base_scores`
  has been set as well
* Use `zip` to create the `scores1` and `scores2` arrays that calculations are done with
  * This used to be done manually
* Check if the standard deviation of `scores1` or `scores2` is zero, 
  and thrown an error if so
  * Dividing by zero is impossible, so `NaN` would previously be returned 
    if this was the case
* Use `scipy.asscalar` as opposed to `.item()` for numpy.float64 => float conversion

## v1.0.2 (2017-04-17)
* Better handling for numpy.float64 => float conversion
* Update docstrings to include types

## v1.0.1 (2017-04-12)
* Don't count rated anime on a user's PTW. MAL didn't count this,
  so our affinity values were a bit off when a user did this

## v1.0.0 (2017-04-09)
* Konnichiwa, sekai!
