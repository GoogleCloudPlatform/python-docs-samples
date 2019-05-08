# Copyright 2019 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np


class ZeroCenterer(object):
    """Stores means of each column of a matrix and uses them for preprocessing.
    """

    def __init__(self):
        """On initialization, is not tied to any distribution."""
        self._means = None

    def preprocess(self, data):
        """Transforms a matrix.

        The first time this is called, it stores the means of each column of
        the input. Then it transforms the input so each column has mean 0. For
        subsequent calls, it subtracts the stored means from each column. This
        lets you 'center' data at prediction time based on the distribution of
        the original training data.

        Args:
            data: A NumPy matrix of numerical data.

        Returns:
            A transformed matrix with the same dimensions as the input.
        """
        if self._means is None:  # during training only
            self._means = np.mean(data, axis=0)
        return data - self._means
