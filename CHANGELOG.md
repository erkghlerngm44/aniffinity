# Changelog


## v1.1.0 (2017-06-15)
* Removed scipy (and numpy) as a dependency
  * Pearson's correlation code is now in `malaffinity.calcs` and stdev checking is handled
    by the `statistics` module
* Use `lxml` for XML parsing, instead of the default `html.parser`

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
