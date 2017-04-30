# Changelog


## v1.0.3
* Highlight distinction between `calculate_affinity` function and method in docs
* Fix wrong issue + pull request URL in `README` due to dodgy copypasta-ing
* Change 'base user has been set' testing to also check if `self._base_scores`
  has been set as well
* Use `ma` as opposed to `a` as the `MALAffinity` instance variable name in examples
* **???**

## v1.0.2
* Better handling for numpy.float64 => float conversion.
* Add `LICENSE` to `MANIFEST.in`.
* Update docstrings to include types
* Use better example when demonstrating how to handle exceptions
* Remove module name from examples
* Show how to separate affinity and shared count in examples

## v1.0.1
* Don't count rated anime on a user's PTW. MAL didn't count this,
  so our affinity values were a bit off when a user did this.
  
## v1.0.0
* Konnichiwa, sekai!
