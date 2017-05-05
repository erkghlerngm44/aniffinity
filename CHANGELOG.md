# Changelog


## v1.0.3

#### Code:
* Change 'base user has been set' testing to also check if `self._base_scores`
  has been set as well
* Use `zip` to create the `scores1` and `scores2` arrays that calculations are done with
  * This used to be done manually
* Check if the standard deviation of `scores1` or `scores2` is zero, 
  and thrown an error if so
  * Dividing by zero is impossible, so `NaN` would previously be returned 
    if this was the case
* Use `scipy.asscalar` as opposed to `.item()` for numpy.float64 => float conversion

#### Docs:
* Highlight distinction between `calculate_affinity` function and method in `README`
* Fix wrong issue + pull request URL in `README` due to dodgy copypasta-ing
* Use `ma` as opposed to `a` as the `MALAffinity` instance variable name in examples
* Added badges and Kyubey gif to `README`
* Make example headers a bit bigger in `README`


## v1.0.2

#### Code:
* Better handling for numpy.float64 => float conversion
* Update docstrings to include types

#### Docs:
* Add `LICENSE` to `MANIFEST.in`
* Use better example when demonstrating how to handle exceptions in `README`
* Remove module name from examples
* Show how to separate affinity and shared count in examples


## v1.0.1

#### Code:
* Don't count rated anime on a user's PTW. MAL didn't count this,
  so our affinity values were a bit off when a user did this


## v1.0.0
* Konnichiwa, sekai!
