
# [START ai_platform_utils]
# [START ai_platform_utils_imports]
import typing
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
# [END ai_platform_utils_imports]


# [START ai_platform_utils_load_data]
def load_data(
    input_path: str
) -> typing.Tuple[np.array, np.array, np.array, np.array]:
    """Loads data from GCS bucket into training and testing dataframes"""
    # Download data from GCS bucket and load data into dataframes
    df = pd.read_csv(input_path)
    df = df.drop(df.columns[0], axis=1)  # drop index column
    # [END ai_platform_utils_load_data]

    # [START ai_platform_utils_extract_ft]
    # Extract feature and target columns
    feature_col = df.iloc[:, :-1]
    target_col = df.iloc[:, -1:]
    # [END ai_platform_utils_extract_ft]

    # [START ai_platform_utils_split]
    # Split datasets into training and testing data. This will return four sets of data
    train_feature, eval_feature, train_target, eval_target = \
        train_test_split(feature_col, target_col, test_size=0.2)

    return train_feature, eval_feature, train_target, eval_target
    # [END ai_platform_utils_split]

# [END ai_platform_utils]
