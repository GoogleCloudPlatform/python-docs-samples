# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https: // www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START aiplatform_sklearn_model]
# [START aiplatform_sklearn_model_imports]
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
# [END aiplatform_sklearn_model_imports]


# [START aiplatform_sklearn_model_polynomial_model]
def polynomial_model(
    degree: int,
    alpha: int
) -> Pipeline:
    """Returns a scikit learn pipeline for the given hyperparameters"""
    return Pipeline(
        [
            ("polynomial features", PolynomialFeatures(degree=degree)),
            ("ridge regression", Ridge(alpha=alpha)),
        ]
    )
# [END aiplatform_sklearn_model_polynomial_model]
# [END aiplatform_sklearn_model]
