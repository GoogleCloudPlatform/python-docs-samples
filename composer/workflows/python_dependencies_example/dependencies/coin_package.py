# This custom PyPI package requires your environment to have the 
# scipy PyPI package installed.

import numpy as np  # numpy is installed by default in Composer.
from scipy import special # scipy is not.


# Returns "Heads" or "Tails" depending on a calculation
def flip_coin():
  # Returns a 2x2 randomly sampled array of values in the range [-5, 5]
  rand_array = 10 * np.random.random((2, 2)) - 5
  # Computes the average of this
  avg = rand_array.mean()
  # Returns the Gaussian CDF of this average
  ndtr = special.ndtr(avg)
  return "Heads" if ndtr > .5 else "Tails"
