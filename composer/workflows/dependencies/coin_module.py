# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A custom Python package example.

This package requires that your environment has the scipy PyPI package
installed. """

import numpy as np  # numpy is installed by default in Composer.
from scipy import special  # scipy is not.


def flip_coin():
    """Return "Heads" or "Tails" depending on a calculation."""
    # Returns a 2x2 randomly sampled array of values in the range [-5, 5]
    rand_array = 10 * np.random.random((2, 2)) - 5
    # Computes the average of this
    avg = rand_array.mean()
    # Returns the Gaussian CDF of this average
    ndtr = special.ndtr(avg)
    return "Heads" if ndtr > .5 else "Tails"
