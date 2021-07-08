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

# [START aiplatform_utils]
# [START aiplatform_utils_imports]
import typing

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
# [END aiplatform_utils_imports]


# [START aiplatform_utils_load_data]
def load_data(
    input_path: str
) -> typing.Tuple[np.array, np.array, np.array, np.array]:
    """Loads data from GCS bucket into training and testing dataframes"""
    # Download data from GCS bucket and load data into dataframes
    df = pd.read_csv(input_path)
    df = df.drop(df.columns[0], axis=1)  # drop index column
    # [END aiplatform_utils_load_data]

    # [START aiplatform_utils_extract_ft]
    # Extract feature and target columns
    feature_col = df.iloc[:, :10]
    target_col = df.iloc[:, 10:]
    # [END aiplatform_utils_extract_ft]

    # [START aiplatform_utils_split]
    # Split datasets into training and testing data. This will return four sets of data
    train_feature, eval_feature, train_target, eval_target = \
        train_test_split(feature_col, target_col, test_size=0.2)

    return train_feature, eval_feature, train_target, eval_target
    # [END aiplatform_utils_split]

# [END aiplatform_utils]
