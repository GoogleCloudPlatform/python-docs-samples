# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np


def normalize_embedding(embedding_np: np.ndarray) -> np.ndarray:
    """
    Normalizes an embedding array to have a magnitude (L2 norm) of 1.

    Args:
        embedding_np: The input NumPy array to be normalized.

    Returns:
        The normalized NumPy array with a magnitude of 1.
        Returns the original array if its magnitude is 0.
    """
    # Calculate the L2 norm (magnitude) of the array
    norm = np.linalg.norm(embedding_np)

    # Avoid division by zero if the array is all zeros
    #
    # An all-zeros embedding array does not exist in theroy
    if norm == 0:
        return embedding_np

    # Divide the array by its norm to normalize it
    return embedding_np / norm
